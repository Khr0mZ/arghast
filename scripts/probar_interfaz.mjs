// Prueba real en Chrome/Edge de la interfaz autónoma mediante su protocolo local.
import fs from 'node:fs/promises';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const output=path.join(root,'.pruebas','interfaz');
const chapterSources=await fs.readdir(path.join(root,'conocimiento/capitulos'));
const expectedChapters=await Promise.all(chapterSources.filter(name=>/^\d+\.json$/.test(name)).map(async name=>JSON.parse(await fs.readFile(path.join(root,'conocimiento/capitulos',name),'utf8'))));
const expectedFacts=expectedChapters.reduce((total,chapter)=>total+chapter.afirmaciones.length,0);
const questionCount=expectedChapters.reduce((total,chapter)=>total+chapter.preguntas.length,0);
const suppliedPalettes=JSON.parse(await fs.readFile(path.join(root,'config/paletas_campanas.json'),'utf8')).campanas;
const expectedMaterialKeys=Object.fromEntries(await Promise.all(['xoltacan','kuroto'].map(async id=>{
  const uri='data:image/webp;base64,'+(await fs.readFile(path.join(root,'web/assets',id+'-panel-paleta.webp'))).toString('base64');
  return [id,uri.length+':'+uri.slice(-64)];
})));

await fs.mkdir(output,{recursive:true});
const binaries=['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','C:/Program Files/Google/Chrome/Application/chrome.exe'];
let binary;for(const candidate of binaries){try{await fs.access(candidate);binary=candidate;break;}catch{}}
if(!binary)throw new Error('No se encontró Chrome/Edge para verificar la interfaz.');
const profile=path.join(output,'perfil-'+Date.now());
await fs.mkdir(profile,{recursive:true});
const browser=spawn(binary,['--headless=new','--no-sandbox','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'],{windowsHide:true,stdio:'ignore'});
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
let ws;const pending=new Map();let id=0;const errors=[];
try {
  let info;for(let i=0;i<120;i++){try{info=(await fs.readFile(path.join(profile,'DevToolsActivePort'),'utf8')).trim().split('\n');break;}catch{await sleep(150);}}
  if(!info)throw new Error('El navegador no abrió el puerto local de pruebas.');
  ws=new WebSocket('ws://127.0.0.1:'+info[0]+info[1]);
  await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true});});
  ws.addEventListener('message',event=>{const message=JSON.parse(String(event.data));if(message.method==='Runtime.exceptionThrown')errors.push(message.params.exceptionDetails);if(message.id&&pending.has(message.id)){const {resolve,reject}=pending.get(message.id);pending.delete(message.id);message.error?reject(new Error(JSON.stringify(message.error))):resolve(message.result);}});
  const send=(method,params={},sessionId)=>new Promise((resolve,reject)=>{const next=++id;pending.set(next,{resolve,reject});ws.send(JSON.stringify({id:next,method,params,...(sessionId?{sessionId}:{})}));});
  const siteURL=new URL(process.env.ARGHAST_TEST_URL||pathToFileURL(path.join(root,'arghast.html')).href);
  siteURL.searchParams.set('campana','xoltacan');
  const target=await send('Target.createTarget',{url:siteURL.href});
  const {sessionId}=await send('Target.attachToTarget',{targetId:target.targetId,flatten:true});
  const call=(method,params={})=>send(method,params,sessionId);
  await call('Runtime.enable');await call('Page.enable');
  const evaluate=async expression=>{const result=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(result.exceptionDetails)throw new Error(JSON.stringify(result.exceptionDetails));return result.result.value;};
  const check=async(name,expression)=>{if(!await evaluate(expression))throw new Error('Fallo: '+name);checks.push(name);};
  const route=async hash=>{await evaluate('location.hash='+JSON.stringify(hash));await sleep(160);};
  const screenshot=async name=>{const shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await fs.writeFile(path.join(output,name+'.png'),Buffer.from(shot.data,'base64'));};
  const checks=[];
  const checkThematicFont=async(family,weight,selector,text='Cr\u00f3nicas \u00c1\u00c9\u00cd\u00d3\u00da\u00dc\u00d1 \u00e1\u00e9\u00ed\u00f3\u00fa\u00fc\u00f1 \u00bf\u00a1')=>{
    await call('DOM.enable');await call('CSS.enable');
    await evaluate(`(async()=>{await document.fonts.load(${JSON.stringify(weight+' 24px "'+family+'"')},${JSON.stringify(text)});await document.fonts.ready;const p=document.createElement('span');p.id='font-probe';p.textContent=${JSON.stringify(text)};Object.assign(p.style,{fontFamily:${JSON.stringify(family)},fontWeight:${JSON.stringify(String(weight))},fontSize:'24px',fontSynthesis:'none',position:'absolute',left:'-10000px'});document.body.append(p);p.getBoundingClientRect();await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))})()`);
    const {root:dom}=await call('DOM.getDocument',{depth:0});
    const {nodeId}=await call('DOM.querySelector',{nodeId:dom.nodeId,selector:'#font-probe'});
    const {fonts}=await call('CSS.getPlatformFontsForNode',{nodeId});
    if(!fonts.length)throw new Error('No se renderizo la muestra de '+family);
    const normalized=family.replace(/\s+/g,'').toLowerCase();
    await check(family+' carga localmente y dibuja la muestra sin sustituciones: '+fonts.map(f=>f.familyName).join(', '),JSON.stringify(fonts.length>0&&fonts.every(f=>f.isCustomFont&&f.familyName.replace(/\s+/g,'').toLowerCase().includes(normalized))));
    await check('El titulo usa '+family,'getComputedStyle(document.querySelector('+JSON.stringify(selector)+')).fontFamily.includes('+JSON.stringify(family)+')');
    await evaluate('document.getElementById("font-probe").remove()');
  };

  const checkSuppliedPalette=async id=>{
    await check('Los 16 HEX de '+id+' coinciden con los proporcionados','(()=>{const style=getComputedStyle(document.body);return '+JSON.stringify(suppliedPalettes[id])+'.every((hex,i)=>style.getPropertyValue("--palette-"+String(i+1).padStart(2,"0")).trim().toUpperCase()===hex)})()');
    const allowed=suppliedPalettes[id].map(hex=>'rgb('+[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)).join(', ')+')');
    await check('Texto, cifras y bordes principales usan la paleta de '+id,'(()=>{const allowed='+JSON.stringify(allowed)+';return [".hero-title",".hero-copy",".stat strong",".stat span"].every(s=>allowed.includes(getComputedStyle(document.querySelector(s)).color))&&[".stat",".expedition-link"].every(s=>allowed.includes(getComputedStyle(document.querySelector(s)).borderTopColor))})()');
  };

  const checkViewFinish=async()=>{
    await check('Scrollbar fina con colores de la vista','getComputedStyle(document.documentElement).scrollbarWidth==="thin"&&getComputedStyle(document.getElementById("sidebar")).scrollbarWidth==="thin"&&getComputedStyle(document.documentElement).scrollbarColor!=="auto"');
    await check('Drawer alineado a la derecha','getComputedStyle(document.getElementById("sidebar")).backgroundPositionX.split(",").every(p=>p.trim()==="100%")');
  };

  const paletteContrast=()=>{
    const luminance=color=>{const rgb=color.match(/[\d.]+/g).slice(0,3).map(Number).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4;});return rgb[0]*.2126+rgb[1]*.7152+rgb[2]*.0722;};
    const ratio=(a,b)=>{const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);};
    return ['.primary-button','.secondary-button','.stat span','.hero-copy','.nav-links a.active'].every(selector=>{
      const element=document.querySelector(selector),style=getComputedStyle(element);
      const surface=selector==='.stat span'?getComputedStyle(element.closest('.stat')):selector==='.hero-copy'?getComputedStyle(element.closest('.hero')):style;
      const stops=surface.backgroundImage.match(/rgb\([^)]+\)/g)||[surface.backgroundColor];
      return stops.every(color=>ratio(style.color,color)>=4.5);
    });
  };

  const checkCover=async()=>{
    await check('Portada completa sin texto ni botones superpuestos', '(()=>{const art=document.querySelector(".hero-art"),copy=document.querySelector(".hero>div:first-child"),a=art.getBoundingClientRect(),b=copy.getBoundingClientRect();return getComputedStyle(art).backgroundSize==="contain"&&(a.left>=b.right-1||a.bottom<=b.top+1||a.top>=b.bottom-1)})()');
  };
  const sectionNames={personajes:'Personajes',atlas:'Lugares',facciones:'Facciones',objetos:'Vestigios',misiones:'Misiones',relaciones:'Relaciones',misterios:'Misterios y desenlaces'};
  const homeNavigation=()=>JSON.stringify({actions:[...document.querySelectorAll('.hero .hero-actions a')].map(a=>[a.textContent.trim(),a.getAttribute('href'),a.getAttribute('target')||'']),categories:[...document.querySelectorAll('.expedition-link')].map(a=>[a.querySelector('strong').textContent,a.getAttribute('href')]),stats:[...document.querySelectorAll('.stat')].map(a=>[a.querySelector('span').textContent,a.getAttribute('href')]),menu:[...document.querySelectorAll('#sidebar .nav-links a')].map(a=>[a.textContent.trim(),a.getAttribute('href')]),archive:[...document.querySelectorAll('.archive-actions a')].map(a=>[a.textContent,a.getAttribute('href')])});
  for(let i=0;i<70;i++){if(await evaluate('!!document.querySelector(".hero")'))break;await sleep(150);}
  await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1080,deviceScaleFactor:1,mobile:false});
  await check('Portada cargada desde archivo local','!!document.querySelector(".hero-title") && !!document.querySelector(".hero-art")');
  await check('Paisaje selvático integrado y decodificable sin conexión','(async()=>{const url=getComputedStyle(document.querySelector(".hero-art")).backgroundImage.slice(5,-2);if(!url.startsWith("data:image/webp;base64,"))return false;const image=new Image();image.src=url;await image.decode();return image.naturalWidth>1000})()');
  await check('Accesos a las seis secciones comunes de la campaña','document.querySelectorAll(".expedition-links a").length===6');
  await check('La portada abre la historia y los misterios dentro del archivo','JSON.stringify([...document.querySelectorAll(".hero .hero-actions a")].map(a=>a.getAttribute("href")))===JSON.stringify(["#lectura","#misterios"])&&![...document.querySelectorAll(".hero .hero-actions a")].some(a=>a.target==="_blank")');
  const xoltacanHomeNavigation=await evaluate('('+homeNavigation.toString()+')()');
  await check('Todos los episodios, registros y transcripciones coinciden con las fichas locales',`(()=>{const d=JSON.parse(document.getElementById("xoltacan-data").textContent);return d.chapters.length===${expectedChapters.length}&&d.facts.length===${expectedFacts}&&Object.keys(d.transcripts).length===${expectedChapters.length}})()`);
  await check('Sin categoría editorial de contradicciones','![...document.querySelectorAll("#sidebar a")].some(a=>a.hash==="#contradicciones")');
  await check('Una ficha por nombre canónico','(()=>{const d=JSON.parse(document.getElementById("xoltacan-data").textContent);const n=d.entities.map(e=>e.name.normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").toLowerCase());return n.length===new Set(n).size})()');
  await check('Personajes y objetos separados','(()=>{const d=JSON.parse(document.getElementById("xoltacan-data").textContent);return d.entities.find(e=>e.name==="Patata Hammer").type==="objeto"&&d.entities.find(e=>e.name==="Patata").type==="personaje"&&d.entities.filter(e=>e.name==="Coyote").length===1})()');
  await screenshot('portada-escritorio');
  await evaluate('document.getElementById("global-search").value="Ilikar";document.getElementById("global-search").dispatchEvent(new Event("input",{bubbles:true}))');await sleep(350);
  await check('Búsqueda global de Ilikar','document.getElementById("content").innerText.includes("Ilikar") && document.querySelectorAll(".event").length>0');
  await evaluate('document.querySelector("[data-filter=chapter]").value="38";document.querySelector("[data-filter=chapter]").dispatchEvent(new Event("change",{bubbles:true}))');
  await check('Filtro por capítulo','[...document.querySelectorAll(".event-time strong")].every(e=>e.textContent==="38")');
  await route('#capitulos');await check('Catálogo completo navegable',`document.querySelectorAll(".chapter-card").length===${expectedChapters.length}`);
  await check('Navegar retira el estado de búsqueda anterior','document.getElementById("search-status").textContent==="" && document.getElementById("global-search").value===""');
  await route('#capitulo/39');await check('El capítulo abre con el relato de su sesión','document.querySelector("[data-tab=relato]").classList.contains("active")&&document.querySelectorAll(".story-stage").length===4');
  await evaluate('document.querySelector("[data-tab=hechos]").click()');
  await check('Acontecimientos del capítulo 39','document.querySelectorAll(".event").length===20');
  await check('Notas de fuentes visibles en el capítulo','!!document.querySelector("section.chapter-source-notes")&&!document.querySelector(".chapter-source-notes").closest("details")&&!document.querySelector("[data-tab=contradicciones]")');
  await evaluate('document.querySelector("[data-tab=preguntas]").click()');
  await check('Cada pregunta de capítulo tiene seguimiento actualizado','(()=>{const q=JSON.parse(document.getElementById("xoltacan-data").textContent).seguimiento.preguntas.filter(q=>q.capitulo===39);const cards=[...document.querySelectorAll(".question-card")];return cards.length===q.length&&cards.every((card,i)=>card.dataset.status===q[i].estado)})()');
  await evaluate('document.querySelector("[data-tab=transcripcion]").click()');
  await check('Transcripción integrada y paginada','document.querySelectorAll(".transcript-row").length===120');
  await evaluate('document.getElementById("transcript-search").value="serpiente";document.getElementById("transcript-search").dispatchEvent(new Event("input",{bubbles:true}))');
  await check('Búsqueda en transcripción','document.querySelectorAll(".transcript-row").length>0&&[...document.querySelectorAll(".transcript-row p")].every(e=>e.textContent.toLowerCase().includes("serpiente"))');
  await route('#registro/39-010');
  await check('Cita y enlace al minuto','document.querySelector(".quote").textContent.length>0 && document.querySelector(".evidence a").href.includes("&t=")');
  await check('Contexto disponible','document.querySelectorAll(".context-details .transcript-row").length>0');
  await screenshot('evidencia-escritorio');
  await route('#capitulo/40');
  await check('El capítulo 40 abre su relato completo en ocho etapas','document.querySelector("[data-tab=relato]").classList.contains("active")&&document.querySelectorAll(".story-stage").length===8&&document.getElementById("content").innerText.includes("Tortas")');
  await screenshot('capitulo-40-escritorio');
  await evaluate('document.querySelector("[data-tab=hechos]").click()');
  await check('El capítulo 40 incluye sus 42 evidencias','document.querySelectorAll(".event").length===42');
  await route('#registro/40-035');
  await check('La entrega del veneno enlaza el vídeo y su contexto','document.querySelector(".quote").textContent.length>0&&document.querySelector(".evidence a").href.includes("LBuXKKhfGlY")&&document.querySelectorAll(".context-details .transcript-row").length>0');
  await route('#capitulo/41');
  await check('El capítulo 41 abre su relato completo en diez etapas','document.querySelector("[data-tab=relato]").classList.contains("active")&&document.querySelectorAll(".story-stage").length===10&&document.getElementById("content").innerText.includes("Tentacol")');
  await check('El directo de julio y la publicación de octubre aparecen separados','document.querySelector(".chapter-dates").innerText.includes("03/07/2026")&&document.querySelector(".chapter-dates").innerText.includes("20/10/2026")&&document.querySelector(".chapter-dates dt").textContent==="Directo en Twitch"');
  await check('La fuente de Twitch enlaza el anuncio original de julio','[...document.querySelectorAll(".date-sources a")].some(a=>a.href.endsWith("/1522672340213694706"))');
  await screenshot('capitulo-41-escritorio');
  await evaluate('document.querySelector("[data-tab=hechos]").click()');
  await check('El capítulo 41 incluye sus 55 evidencias','document.querySelectorAll(".event").length===55');
  await evaluate('document.querySelector("[data-tab=preguntas]").click()');
  await check('Las once preguntas del capítulo 41 conservan seguimiento','document.querySelectorAll(".question-card").length===11&&[...document.querySelectorAll(".question-card")].every(card=>card.dataset.status==="pendiente")');
  await route('#registro/41-023');
  await check('La muerte de la infiltrada enlaza la nueva fuente y su contexto','document.querySelector(".quote").textContent.length>0&&document.querySelector(".evidence a").href.includes("vB6Y1LQ2IaM")&&document.querySelectorAll(".context-details .transcript-row").length>0');
  await route('#entidad/Tentacol');
  await check('Tentacol tiene historia y fuentes navegables','document.querySelectorAll(".story-stage").length===2&&document.querySelectorAll(".story-sources a").length>0&&document.getElementById("content").innerText.includes("Chopito")');
  await route('#pregunta/P40-007');
  await check('Cipo queda localizado y el fragmento sigue pendiente','document.querySelector(".question-card").dataset.status==="parcial"&&document.getElementById("content").innerText.includes("Tentacol")&&document.getElementById("content").innerText.includes("fragmento de espada")');
  await route('#entidad/Tortas');
  await check('Tortas conserva su historia actualizada y las edades discrepantes','document.querySelectorAll(".story-stage").length===JSON.parse(document.getElementById("xoltacan-data").textContent).entities.find(e=>e.name==="Tortas").history.etapas.length&&document.getElementById("content").innerText.includes("77")');
  for(const section of ['misterios','misiones','relaciones','nombres']){await route('#'+section);await check('Documento '+section,'document.querySelector(".document").innerText.length>100');}
  await route('#metodo');await check('La antigua página de método vuelve a portada',`location.hash==='#inicio'&&!!document.querySelector('.hero')&&!document.querySelector('a[href="#metodo"]')`);
  await route('#capitulo/21');
  await check('El día aceptado se muestra como fecha y conserva los avisos alternativos','document.querySelector(".chapter-dates dd").dataset.dateStatus==="asumida"&&document.querySelector(".chapter-dates dd").textContent==="01/04/2026"&&document.querySelector(".date-sources").textContent.includes("02/04/2026")&&document.querySelector(".chapter-dates dd time").getAttribute("datetime")==="2026-04-01"');
  await route('#capitulo/38');
  await check('El capítulo 38 adopta el día aceptado y enlaza su calendario','document.querySelector(".chapter-dates dd").textContent==="15/06/2026"&&document.querySelector(".date-programming").textContent.includes("15/06/2026")&&document.querySelector(".date-programming a").href.includes("/946724149383024690/")&&document.querySelector(".chapter-dates dd").dataset.dateStatus==="asumida"');
  await route('#capitulo/40');
  await check('El capítulo 40 distingue fecha asumida y programación de las 20:00','document.querySelector(".chapter-dates dd").textContent==="02/07/2026"&&document.querySelector(".chapter-dates dd").dataset.dateStatus==="asumida"&&document.querySelector(".date-programming").textContent.includes("20:00")&&document.querySelector(".date-programming").textContent.includes("no acredita")');
  await screenshot('fechas-estimadas-escritorio');
  await evaluate('document.querySelector(".date-sources").open=true');
  await check('La fuente abierta conserva la diferencia entre día probable y hora prevista','document.querySelector(".date-sources").innerText.includes("confianza")&&document.querySelector(".date-programming").innerText.includes("hora real de inicio")');
  await screenshot('fechas-programacion-escritorio');
  await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});
  await sleep(350);
  await check('El calendario desplegado cabe en móvil','document.documentElement.scrollWidth<=390&&document.querySelector(".date-programming").getBoundingClientRect().right<=390');
  await screenshot('fechas-programacion-movil');
  await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1080,deviceScaleFactor:1,mobile:false});
  await route('#capitulo/39');
  await check('Un aviso sin fecha del vídeo se identifica como aviso YouTube','[...document.querySelectorAll(".chapter-dates dt")].some(e=>e.textContent==="Aviso de YouTube")&&document.querySelector(".date-sources").textContent.includes("publicación exacta sigue por confirmar")');
  await route('#capitulo/1');
  await evaluate('document.querySelector(".date-sources").open=true');
  await check('Se conserva la fecha del vídeo aunque el bot avise dos días después','document.querySelector(".chapter-dates").textContent.includes("07/04/2026")&&document.querySelector(".date-sources").textContent.includes("9/4/26")');
  for(const [section,type] of [['personajes','personaje'],['atlas','lugar'],['facciones','faccion'],['objetos','objeto']]){
    await route('#'+section);
    await check('Nombre común de la sección '+section+' en Xoltacan','document.getElementById("page-title").textContent==='+JSON.stringify(sectionNames[section])+'&&document.querySelector("#content h1").textContent==='+JSON.stringify(sectionNames[section]));
    await check('Catálogo exclusivo de '+section,`(()=>{const d=JSON.parse(document.getElementById("xoltacan-data").textContent);const names=[...document.querySelectorAll(".entity-card .card-title")].map(e=>e.textContent);return names.length>0&&names.every(n=>d.entities.find(e=>e.name===n).type===${JSON.stringify(type)})})()`);
    await check('Sin selector de categorías duplicado en '+section,'!document.querySelector("[data-filter=entityType]")');
  }
  await check('Menú sin catálogo general duplicado','![...document.querySelectorAll("#sidebar a")].some(a=>a.hash==="#entidades")');
  await route('#entidad/'+encodeURIComponent('Shiaru'));
  await check('Lugar vuelve a su sección y la resalta','document.querySelector("#content>.source-link").hash==="#atlas"&&document.querySelector("#sidebar a.active").hash==="#atlas"');
  await route('#entidad/'+encodeURIComponent('Marina'));
  await check('Facción vuelve a su sección y la resalta','document.querySelector("#content>.source-link").hash==="#facciones"&&document.querySelector("#sidebar a.active").hash==="#facciones"');
  await route('#misterios');await check('Misterios con referencias navegables','document.querySelectorAll(".document a[href*=registro]").length>10');
  await check('Todas las preguntas cotejadas hasta el último capítulo',`(()=>{const s=JSON.parse(document.getElementById("xoltacan-data").textContent).seguimiento;return s.preguntas.length===${questionCount}&&!s.estados.sin_revisar&&s.por_actualizar===0})()`);
  await check('Seguimiento paginado','document.querySelectorAll(".question-card").length===20');
  await evaluate('document.querySelector("[data-filter=questionStatus]").value="resuelta";document.querySelector("[data-filter=questionStatus]").dispatchEvent(new Event("change",{bubbles:true}))');
  await check('Filtro de preguntas resueltas','document.querySelectorAll(".question-card").length>0&&[...document.querySelectorAll(".question-card")].every(e=>e.dataset.status==="resuelta")');
  await evaluate('document.querySelector("[data-filter=questionStatus]").value="";document.querySelector("[data-filter=questionStatus]").dispatchEvent(new Event("change",{bubbles:true}));document.getElementById("question-search").value="mondadientes";document.getElementById("question-search").dispatchEvent(new Event("input",{bubbles:true}))');
  await check('Buscar respuestas posteriores','document.querySelectorAll(".question-card").length>0&&document.getElementById("content").innerText.includes("14-003")');
  await evaluate('document.querySelector(".question-card h3 a").click()');await sleep(180);
  await check('Ficha de pregunta con evidencia y minutos','location.hash.startsWith("#pregunta/")&&!!document.querySelector(".quote")&&document.querySelector(".evidence a").href.includes("&t=")');
  await screenshot('seguimiento-escritorio');
  await route('#personajes');await check('Personajes renderizados','document.querySelectorAll(".entity-card").length===36');
  const jackAlias=await evaluate('JSON.parse(document.getElementById("xoltacan-data").textContent).entities.find(e=>e.name==="Jack").aliases[0]');
  await route('#entidad/'+encodeURIComponent(jackAlias));
  await check('Alias antiguo conduce a la ficha única','document.getElementById("page-title").textContent==="Jack"&&document.querySelectorAll(".event").length>0');
  await route('#entidades');await check('Enlace antiguo redirigido','location.hash==="#personajes"');
  await evaluate('document.getElementById("entity-search").value="Naór";document.getElementById("entity-search").dispatchEvent(new Event("input",{bubbles:true}))');
  await check('Equivalencias y acentos','document.querySelectorAll(".entity-card").length>0 && document.getElementById("content").innerText.includes("Naór")');
  await evaluate('document.querySelector(".entity-card").click()');await sleep(160);await check('Ficha de entidad','document.querySelectorAll(".event").length>0');
  await route('#atlas');await check('Búsqueda local se limpia al cambiar de sección','document.getElementById("entity-search").value===""&&document.querySelectorAll(".entity-card").length>0');
  await evaluate(`document.querySelector('.catalogue-views a[href="#documento/atlas"]').click()`);await sleep(180);
  await check('Contexto geográfico con vista propia y texto visible','location.hash==="#documento/atlas"&&document.querySelector(".document").innerText.length>100&&!document.querySelector(".document").closest("details")&&document.querySelector("#sidebar a.active").hash==="#atlas"');
  await route('#busqueda/zzzzxoltacansindatos');await check('Búsqueda sin coincidencias','!!document.querySelector(".empty")');
  await route('#personajes');await screenshot('personajes-escritorio');
  await check('Todas las categorías tienen relatos con referencias','JSON.parse(document.getElementById("xoltacan-data").textContent).entities.every(e=>e.history?.etapas.length&&e.history.etapas.every(s=>s.referencias.length))');
  await check('Los relatos de capítulo conservan el resumen íntegro','JSON.parse(document.getElementById("xoltacan-data").textContent).chapters.every(c=>c.history.etapas.map(s=>s.texto).join(" ")===c.resumen)');
  for(const [name,kind,title] of [['Shiaru','lugar','Historia y acontecimientos'],['Marina','faccion','Intereses y evolución'],['Zampaolas','objeto','Origen y recorrido']]){
    await route('#entidad/'+encodeURIComponent(name));
    await check('Relato específico de '+kind,`document.querySelector('.narrative-story').dataset.storyKind===${JSON.stringify(kind)}&&document.querySelector('.story-heading h2').textContent===${JSON.stringify(title)}&&document.querySelectorAll('.story-sources a').length>0`);
    await screenshot('relato-'+kind+'-escritorio');
    await evaluate('document.querySelector(".story-sources a").click()');await sleep(180);
    await check('Citas navegables de '+kind,'location.hash.startsWith("#registro/")&&!!document.querySelector(".quote")');
  }
  await check('Cada personaje tiene historia editorial con fuentes','JSON.parse(document.getElementById("xoltacan-data").textContent).entities.filter(e=>e.type==="personaje").every(e=>e.history?.etapas.length&&e.history.etapas.every(s=>s.texto.length>40&&s.referencias.length>0))');
  await route('#entidad/Ione');
  await check('Historia narrativa antes de las evidencias','document.querySelectorAll(".story-stage").length===JSON.parse(document.getElementById("xoltacan-data").textContent).entities.find(e=>e.name==="Ione").history.etapas.length&&document.querySelector(".character-story").compareDocumentPosition(document.querySelector(".event"))===Node.DOCUMENT_POSITION_FOLLOWING');
  await screenshot('historia-personaje-escritorio');
  await evaluate('document.querySelector(".story-sources a").click()');await sleep(180);
  await check('Fuentes del relato abren la evidencia original','location.hash.startsWith("#registro/")&&!!document.querySelector(".quote")&&document.querySelector(".evidence a").href.includes("&t=")');
  await route('#capitulo/39');await screenshot('capitulo-escritorio');
  await route('#capitulos');await screenshot('capitulos-escritorio');
  for(const width of [320,768]){
    await call('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:width<560});
    for(const section of ['personajes','capitulo/39','capitulo/40','capitulo/41','misterios','entidad/Ione','entidad/Tortas','entidad/Tentacol','entidad/Shiaru','entidad/Marina','entidad/Zampaolas']){
      await route('#'+section);
      await check('Códice sin desbordamiento a '+width+' px en '+section,'document.documentElement.scrollWidth<=window.innerWidth');
    }
  }
  await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});
  await route('#inicio');await screenshot('portada-movil');
  await check('Móvil sin desbordamiento','document.documentElement.scrollWidth<=window.innerWidth');
  await evaluate('document.getElementById("menu-toggle").click()');await sleep(250);
  await check('Menú móvil accesible','document.getElementById("sidebar").classList.contains("open") && document.getElementById("menu-toggle").getAttribute("aria-expanded")==="true"');
  await evaluate('document.querySelector("#sidebar a[href*=misterios]").click()');await sleep(200);
  await check('Menú se cierra al navegar','!document.getElementById("sidebar").classList.contains("open")');
  await check('Tabla desplazable en móvil','document.documentElement.scrollWidth<=window.innerWidth');
  await check('Seguimiento legible en móvil','document.querySelectorAll(".question-card").length===20&&document.documentElement.scrollWidth<=window.innerWidth');
  await evaluate('document.dispatchEvent(new KeyboardEvent("keydown",{key:"k",ctrlKey:true,bubbles:true,cancelable:true}))');
  await check('Atajo de búsqueda por teclado','document.activeElement.id==="global-search"');
  await screenshot('misterios-movil');
  await route('#capitulo/39');await screenshot('capitulo-movil');
  await route('#capitulo/40');await screenshot('capitulo-40-movil');
  await route('#capitulo/41');await screenshot('capitulo-41-movil');
  await route('#personajes');await screenshot('personajes-movil');
  await route('#entidad/Ione');await screenshot('historia-personaje-movil');
  await route('#entidad/Zampaolas');await screenshot('relato-objeto-movil');
  await route('#entidad/Shiaru');await screenshot('relato-lugar-movil');
  const chooseCampaign=async id=>{
    await evaluate(`document.getElementById('campaign-selector').value=${JSON.stringify(id)};document.getElementById('campaign-selector').dispatchEvent(new Event('change',{bubbles:true}))`);
    let ready=false;
    for(let i=0;i<100;i++){try{ready=await evaluate(`document.body.dataset.campaign===${JSON.stringify(id)}&&document.body.dataset.view==='campaign'&&!!document.querySelector('.hero')`);}catch{}if(ready)break;await sleep(150);}
    if(!ready)throw new Error('No cargó la campaña '+id);
  };
  await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1080,deviceScaleFactor:1,mobile:false});
  await route('#inicio');
  const sharedComponentStyles=()=>JSON.stringify(['body','.topbar','#campaign-selector','.nav-links a.active','.primary-button','.secondary-button','.stat','.expedition-link'].map(selector=>{const style=getComputedStyle(document.querySelector(selector));return ['backgroundColor','backgroundImage','color','borderRadius','borderColor','fontFamily','fontSize','padding','boxShadow'].map(key=>style[key]);}));
  const xoltacanComponents=await evaluate('('+sharedComponentStyles.toString()+')()');
  const backgroundInfo=async(selector,pseudo=null)=>{const style=getComputedStyle(document.querySelector(selector),pseudo);const match=style.backgroundImage.match(/url\("?(data:image\/webp;base64,[^")]+)"?\)/);if(!match)return null;const img=new Image();img.src=match[1];await img.decode();return {width:img.naturalWidth,height:img.naturalHeight,key:match[1].length+':'+match[1].slice(-64),position:style.position,pointerEvents:style.pointerEvents};};
  const readBackground=(selector,pseudo=null)=>evaluate('('+backgroundInfo.toString()+')('+JSON.stringify(selector)+','+JSON.stringify(pseudo)+')');
  const xoltacanBackground=await readBackground('.workspace','::before');
  const xoltacanDrawer=await readBackground('#sidebar');
  const xoltacanCover=await readBackground('.hero-art');
  const xoltacanMaterial=await readBackground('.hero');
  await checkThematicFont('Macondo',400,'.hero-title');
  await check('Xoltacan usa su titulo grafico incrustado','getComputedStyle(document.querySelector(".hero-title"),"::after").maskImage.includes("data:image/png;base64,")');
  await check('Ambystoma llega a todos los enlaces del sidebar, topbar y botones','[...document.querySelectorAll(".nav-links a,#page-title,.primary-button,.secondary-button,.expedition-link strong")].every(e=>!!e.querySelector(".campaign-lettering"))');
  await check('El selector de Xoltacan tambien muestra su rotulo de campaña','getComputedStyle(document.querySelector("#campaign-selector")).backgroundImage.includes("data:image/png;base64,")');
  await check('Los rotulos conservan texto accesible e imagenes locales decodificables','(async()=>{const nodes=[...document.querySelectorAll(".campaign-lettering")];return nodes.length>20&&(await Promise.all(nodes.map(async e=>{const mask=getComputedStyle(e,"::after").maskImage;const url=mask.match(/url\\([\"\u0027]?(data:image\\/png;base64,[^\"\u0027)]+)[\"\u0027]?\\)/)?.[1];if(!url||!e.textContent.trim())return false;const img=new Image();img.src=url;await img.decode();return img.naturalWidth>0}))).every(Boolean)})()');
  const xoltacanHeader=await readBackground('.topbar');
  await check('La topbar de Xoltacan carga su textura exclusiva',JSON.stringify(!!xoltacanHeader&&xoltacanHeader.width>1500&&xoltacanHeader.key!==xoltacanMaterial.key));
  await check('Xoltacan abre la textura recoloreada con la paleta aportada',JSON.stringify(xoltacanMaterial?.key===expectedMaterialKeys.xoltacan));
  await check('Xoltacan tiene material ilustrado propio en los paneles',JSON.stringify(!!xoltacanMaterial&&xoltacanMaterial.key!==xoltacanCover.key&&xoltacanMaterial.key!==xoltacanBackground.key));
  await check('Bordes y cifras coherentes en Xoltacan','new Set([...document.querySelectorAll(".stat")].map(e=>getComputedStyle(e).borderTopColor)).size===1&&new Set([...document.querySelectorAll(".stat strong")].map(e=>getComputedStyle(e).color)).size===1&&new Set([...document.querySelectorAll(".expedition-link")].map(e=>getComputedStyle(e).borderLeftColor)).size===1');
  await checkViewFinish();
  await check('Portada directa sin lemas decorativos','document.querySelector(".hero-title").textContent==="Xoltacan"&&!document.querySelector(".brand-subtitle,.topbar-seal,.sidebar-note")');
  await check('Textos y controles de Xoltacan conservan contraste legible','('+paletteContrast.toString()+')()');
  await check('Xoltacan usa el amarillo oficial','getComputedStyle(document.querySelector(".primary-button")).backgroundImage.includes("rgb(233, 230, 38)")');
  await checkSuppliedPalette('xoltacan');
  await checkCover();
  await check('Logo de Lichpol integrado y decodificable sin conexi\u00f3n','(async()=>{const img=document.querySelector(".brand-symbol");await img.decode();return img.tagName==="IMG"&&img.naturalWidth===176&&img.src.startsWith("data:image/webp;base64,")})()');
  await screenshot('xoltacan-fondos-escritorio');
  await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});
  await evaluate('document.getElementById("menu-toggle").click()');await sleep(250);
  await checkCover();
  await screenshot('xoltacan-drawer-movil');
  await evaluate('document.getElementById("menu-toggle").click()');
  await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1080,deviceScaleFactor:1,mobile:false});
  await check('Xoltacan tiene fondo selvático en toda el área de contenido',JSON.stringify(!!xoltacanBackground&&xoltacanBackground.width>1000&&xoltacanBackground.position==='fixed'&&xoltacanBackground.pointerEvents==='none'));
  await route('#campanas');
  await check('Arghast tiene un selector y dos campañas independientes','document.title==="Arghast · Archivo de campañas"&&document.querySelectorAll(".world-campaign").length===2&&document.getElementById("campaign-selector").value===""');
  const worldBackground=await readBackground('.workspace','::before');
  const worldSidebar=await readBackground('#sidebar');
  await checkThematicFont('IM Fell English SC',400,'.world-hero h1');
  await check('Arghast utiliza su fuente en sidebar, topbar y controles','[...document.querySelectorAll(".brand-name,#page-title,#campaign-context,#campaign-selector,.campaign-picker>a,.campaign-enter,.footer a")].every(e=>getComputedStyle(e).fontFamily.includes("IM Fell English SC"))');
  await check('El selector de Arghast conserva las tipografias de las campañas','getComputedStyle(document.querySelector(".world-campaign-kuroto h2")).fontFamily.startsWith("Karate")&&getComputedStyle(document.querySelector(".world-campaign-xoltacan h2"),"::after").maskImage.includes("data:image/png;base64,")');
  const worldHeader=await readBackground('.topbar');
  const worldHero=await readBackground('.world-hero');
  await check('Arghast tiene textura de topbar y atlas propios',JSON.stringify(!!worldHeader&&!!worldHero&&worldHeader.key!==worldHero.key&&worldHero.key!==worldBackground.key));
  await check('El atlas resume las campanas y cronicas reales','(()=>{const archive=JSON.parse(document.getElementById("xoltacan-data").textContent);const campaigns=[archive,...Object.values(archive.campaigns)];const totals=[...document.querySelectorAll(".world-summary strong")].map(node=>Number(node.textContent));return totals[0]===campaigns.length&&totals[1]===campaigns.reduce((total,campaign)=>total+campaign.chapters.length,0)})()');
  await checkViewFinish();
  await check('Arghast conserva el mapa oficial en el contenido y una ilustración exclusiva en el drawer',JSON.stringify(!!worldBackground&&!!worldSidebar&&worldBackground.width===2048&&worldBackground.height===1536&&worldBackground.key!==worldSidebar.key));
  await check('Arghast usa los colores del mapa y conserva su color original','getComputedStyle(document.body).backgroundColor==="rgb(41, 62, 67)"&&getComputedStyle(document.querySelector(".workspace"),"::before").filter==="none"');
  await check('Enlaces de campaña conservan la selección en la URL','[...document.querySelectorAll(".world-campaign")].every(a=>new URL(a.href).searchParams.has("campana"))');
  await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});
  await sleep(300);await screenshot('arghast-movil');
  await evaluate('document.getElementById("menu-toggle").click()');await sleep(250);
  await screenshot('arghast-drawer-movil');
  await evaluate('document.getElementById("menu-toggle").click()');
  await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1080,deviceScaleFactor:1,mobile:false});
  await screenshot('arghast-escritorio');
  await chooseCampaign('kuroto');
  await check('Las portadas comparten nombres, categorías y destinos de botones','('+homeNavigation.toString()+')()==='+JSON.stringify(xoltacanHomeNavigation));
  const kurotoBackground=await readBackground('.workspace','::before');
  const kurotoDrawer=await readBackground('#sidebar');
  const kurotoCover=await readBackground('.hero-art');
  const kurotoMaterial=await readBackground('.hero');
  await checkThematicFont('Kaisei Tokumin',700,'.nav-links a');
  await checkThematicFont('Karate',400,'.hero-title','Kuroto');
  await check('Karate llega al sidebar, topbar, botones y pestañas','[...document.querySelectorAll(".nav-links a,#page-title,.primary-button,.secondary-button,.expedition-link strong,#campaign-selector")].every(e=>getComputedStyle(e).fontFamily.startsWith("Karate"))');
  const kurotoHeader=await readBackground('.topbar');
  await check('Cada topbar tiene una textura diferente',JSON.stringify(!!kurotoHeader&&new Set([xoltacanHeader.key,worldHeader.key,kurotoHeader.key]).size===3&&kurotoHeader.key!==kurotoMaterial.key));
  await check('Kuroto abre la textura recoloreada con la paleta aportada',JSON.stringify(kurotoMaterial?.key===expectedMaterialKeys.kuroto));
  await check('Kuroto tiene material ilustrado distinto de Xoltacan y su portada',JSON.stringify(!!kurotoMaterial&&kurotoMaterial.key!==kurotoCover.key&&kurotoMaterial.key!==kurotoBackground.key&&kurotoMaterial.key!==xoltacanMaterial.key));
  await check('Bordes y cifras coherentes en Kuroto','new Set([...document.querySelectorAll(".stat")].map(e=>getComputedStyle(e).borderTopColor)).size===1&&new Set([...document.querySelectorAll(".stat strong")].map(e=>getComputedStyle(e).color)).size===1&&new Set([...document.querySelectorAll(".expedition-link")].map(e=>getComputedStyle(e).borderLeftColor)).size===1');
  await checkViewFinish();
  await check('Textos y controles de Kuroto conservan contraste legible','('+paletteContrast.toString()+')()');
  await checkCover();
  await check('Los tres drawers cargan ilustraciones verticales sin conexión',JSON.stringify([worldSidebar,xoltacanDrawer,kurotoDrawer].every(b=>b&&b.width<b.height&&b.width>700)));
  await check('Las cinco imágenes nuevas son exclusivas de sus respectivos usos',JSON.stringify(new Set([worldSidebar,xoltacanDrawer,kurotoDrawer,xoltacanBackground,kurotoBackground].map(b=>b.key)).size===5));
  await check('Las portadas conservan ilustraciones diferentes de los fondos y drawers',JSON.stringify(!!xoltacanCover&&!!kurotoCover&&new Set([worldSidebar,xoltacanDrawer,kurotoDrawer,xoltacanBackground,kurotoBackground,xoltacanCover,kurotoCover,worldBackground].map(b=>b.key)).size===8));
  await check('Kuroto tiene fondo oriental propio en toda el área de contenido',JSON.stringify(!!kurotoBackground&&kurotoBackground.width>1000&&kurotoBackground.position==='fixed'&&kurotoBackground.pointerEvents==='none'));
  await check('Cada ámbito utiliza su propia imagen de fondo',JSON.stringify(new Set([xoltacanBackground.key,worldBackground.key,kurotoBackground.key]).size===3));
  await check('Kuroto conserva una identidad distinta en botones, navegación y paneles','('+sharedComponentStyles.toString()+')()!=='+JSON.stringify(xoltacanComponents));
  await check('Kuroto usa el coral oficial','getComputedStyle(document.querySelector(".primary-button")).backgroundImage.includes("rgb(236, 141, 133)")');
  await checkSuppliedPalette('kuroto');
  await check('Selector abre Kuroto con su propia portada','location.search.includes("campana=kuroto")&&document.title.includes("Kuroto")&&!!document.querySelector(".kuroto-hero")');
  await check('Kuroto muestra el alcance real de la revisión','(()=>{const d=JSON.parse(document.getElementById("xoltacan-data").textContent).campaigns.kuroto;const reviewed=d.chapters.filter(c=>c.estado==="revisado").length;const status=document.querySelector(".campaign-status");return reviewed===d.chapters.length?!status:!!status&&status.textContent.includes(String(reviewed)+" ")&&status.textContent.includes("pendientes de lectura editorial")})()');
  await check('Las 181 sesiones tienen relato completo y evidencias propias','(()=>{const d=JSON.parse(document.getElementById("xoltacan-data").textContent).campaigns.kuroto;return d.chapters.length===181&&d.chapters.every(c=>c.estado==="revisado"&&c.resumen.split(/\\s+/).length>300&&c.history?.etapas.length&&c.history.etapas.map(s=>s.texto).join(" ")===c.resumen&&c.history.etapas.every(s=>s.referencias.every(r=>Number(r.split("-")[0])===c.capitulo)))})()');
  await check('Personajes, lugares, facciones y objetos de Kuroto tienen historia con fuentes','(()=>{const d=JSON.parse(document.getElementById("xoltacan-data").textContent).campaigns.kuroto;return ["personaje","lugar","faccion","objeto"].every(t=>d.entities.some(e=>e.type===t))&&d.entities.every(e=>e.history?.etapas.length&&e.history.etapas.every(s=>s.texto.length>30&&s.referencias.length))})()');
  await check('La ilustración de Kuroto está integrada y abre sin conexión','(async()=>{const background=getComputedStyle(document.querySelector(".kuroto-hero .hero-art")).backgroundImage;const urls=[...background.matchAll(/url\\("?(data:image\\/webp;base64,[^"\\)]+)"?\\)/g)];if(!urls.length)return false;const image=new Image();image.src=urls[0][1];await image.decode();return image.naturalWidth>1000})()');
  await check('Los alias reúnen las historias de Gelbreak y R3 en una ficha','(()=>{const es=JSON.parse(document.getElementById("xoltacan-data").textContent).campaigns.kuroto.entities;return es.filter(e=>e.name.startsWith("Gelbreak")).length===1&&es.filter(e=>e.name.startsWith("R3 (")).length===1&&es.find(e=>e.name.startsWith("Gelbreak")).history.etapas.some(s=>s.referencias.some(r=>r.startsWith("168-")))})()');
  await screenshot('kuroto-escritorio');
  await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});
  await evaluate('document.getElementById("menu-toggle").click()');await sleep(250);
  await checkCover();
  await screenshot('kuroto-drawer-movil');
  await evaluate('document.getElementById("menu-toggle").click()');
  await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1080,deviceScaleFactor:1,mobile:false});
  await route('#capitulos');
  await check('Catálogo completo de Kuroto sin renumerar','(()=>{const cards=[...document.querySelectorAll(".chapter-card")];return cards.length===181&&cards.some(a=>a.hash==="#capitulo/182")&&!cards.some(a=>a.hash==="#capitulo/92")})()');
  await check('Las tarjetas de Kuroto distinguen Twitch y YouTube','document.querySelectorAll(".chapter-dates-compact").length===181');
  await check('169 y 170 siguen orden numérico','(()=>{const links=[...document.querySelectorAll(".chapter-card")].map(a=>Number(a.hash.split("/")[1]));return links.indexOf(169)<links.indexOf(170)})()');
  await evaluate('document.getElementById("chapter-search").value="bosque";document.getElementById("chapter-search").dispatchEvent(new Event("input",{bubbles:true}))');
  await check('Buscar capítulos de Kuroto','document.querySelectorAll(".chapter-card").length>0&&[...document.querySelectorAll(".chapter-card .card-title")].every(e=>e.textContent.toLowerCase().includes("bosque"))');
  await route('#capitulo/1');
  await check('Los mismos números de capítulo no mezclan campañas','document.getElementById("page-title").textContent==="El Bosque de Cuchillas"&&document.querySelectorAll(".story-stage").length===5&&document.querySelector("a[target=_blank]").href.includes("KkZZR81onIw")');
  await check('Kuroto conserva su propia fecha del directo original','document.querySelector(".chapter-dates").textContent.includes("20/03/2024")&&!document.querySelector(".chapter-dates").textContent.includes("28/01/2026")');
  await screenshot('kuroto-fechas-escritorio');
  await route('#capitulo/55');
  await check('Kuroto 55 adopta el 9 conservando el aviso original del 10 y su discrepancia','document.querySelector(".date-discrepancy").textContent.includes("9 de octubre")&&document.querySelector(".chapter-dates dd").textContent==="09/10/2024"&&document.querySelector(".chapter-dates dd").dataset.dateStatus==="asumida"&&[...document.querySelectorAll(".date-sources a")].some(a=>a.href.endsWith("/1294002567352811644"))');
  for(const [number,day,notice] of [[49,'24/09/2024','1288206046950588457'],[56,'10/10/2024','1293642162625577123'],[134,'02/07/2025','1390030497551487016']]){
    await route('#capitulo/'+number);
    await check('Kuroto '+number+' tiene día asumido y conserva su aviso contradictorio',`document.querySelector('.chapter-dates dd').textContent===${JSON.stringify(day)}&&document.querySelector('.chapter-dates dd').dataset.dateStatus==='asumida'&&[...document.querySelectorAll('.date-sources a')].some(a=>a.href.endsWith('/'+${JSON.stringify(notice)}))`);
  }
  await route('#capitulo/1');
  await evaluate('document.querySelector("[data-tab=transcripcion]").click()');
  for(let i=0;i<100;i++){if(await evaluate('!!document.querySelector(".transcript-row")'))break;await sleep(150);}
  await check('Transcripción original de Kuroto cargada por sesión','document.querySelectorAll(".transcript-row").length===120&&document.querySelector(".transcript-row a").href.includes("KkZZR81onIw")&&Object.keys(globalThis.arghastTranscripts).length===1');
  await evaluate('document.getElementById("transcript-search").value="cuchillas";document.getElementById("transcript-search").dispatchEvent(new Event("input",{bubbles:true}))');
  await check('Búsqueda en la transcripción recuperada','document.querySelectorAll(".transcript-row").length>0&&[...document.querySelectorAll(".transcript-row p")].every(p=>p.textContent.toLowerCase().includes("cuchillas"))');
  await route('#capitulo/182');
  await evaluate('document.querySelector("[data-tab=transcripcion]").click()');
  for(let i=0;i<100;i++){if(await evaluate('!!document.querySelector(".transcript-row")'))break;await sleep(150);}
  await check('La última sesión abre su propio archivo de subtítulos','document.querySelectorAll(".transcript-row").length===120&&document.querySelector(".transcript-row a").href.includes("iop3TS6EwO8")');
  for(const number of [96,135,136]){
    await route('#capitulo/'+number);
    await evaluate('document.querySelector("[data-tab=transcripcion]").click()');
    for(let i=0;i<100;i++){if(await evaluate('!!document.querySelector(".transcript-row")'))break;await sleep(150);}
    await check('La sesión '+number+' identifica su transcripción local','document.querySelectorAll(".transcript-row").length===120&&document.getElementById("content").textContent.includes("Whisper")');
  }
  await check('Todas las preguntas de Kuroto están cotejadas hasta el epílogo','(()=>{const s=JSON.parse(document.getElementById("xoltacan-data").textContent).campaigns.kuroto.seguimiento;return s.preguntas.length>700&&s.por_actualizar===0&&!s.estados.sin_revisar&&s.preguntas.every(q=>q.revisado_hasta===182&&!q.requiere_actualizacion)})()');
  for(const section of ['personajes','atlas','facciones','objetos','misterios','misiones','relaciones','busqueda/Ione']){
    await route('#'+section);
    if(sectionNames[section])await check('Nombre común de la sección '+section+' en Kuroto','document.getElementById("page-title").textContent==='+JSON.stringify(sectionNames[section])+'&&document.querySelector("#content h1").textContent==='+JSON.stringify(sectionNames[section]));
    await check('Kuroto aislado en '+section,'document.body.dataset.campaign==="kuroto"&&![...document.querySelectorAll(".entity-card .card-title,.event h3")].some(node=>/Ione|Bonnie|Shiaru/.test(node.textContent))');
  }
  await route('#entidad/Tokugawa');
  await screenshot('kuroto-ficha-paleta');
  await check('Historia del personaje con alcance y evidencias','document.querySelectorAll(".story-stage").length>=3&&(()=>{const d=JSON.parse(document.getElementById("xoltacan-data").textContent).campaigns.kuroto;const h=d.entities.find(e=>e.name==="Tokugawa").history;return document.querySelector(".story-heading").textContent.includes("Hasta el capítulo "+h.revisado_hasta)})()');
  await evaluate('document.querySelector(".story-sources a").click()');await sleep(250);
  await check('Las evidencias enlazan el vídeo de Kuroto','!!document.querySelector(".quote")&&document.querySelector(".evidence a").href.includes("KkZZR81onIw")');
  await route('#capitulo/2');
  await check('La segunda sesión tiene su propio relato completo','document.querySelectorAll(".story-stage").length===6&&document.getElementById("content").textContent.includes("reparar")');
  await route('#facciones');
  await check('La facción documentada tiene ficha propia','[...document.querySelectorAll(".entity-card .card-title")].some(node=>node.textContent.includes("Familia Baki"))');
  await route('#pregunta/K01-P03');
  await check('Una pregunta anterior se resuelve con evidencia posterior','document.querySelector(".question-card").dataset.status==="resuelta"&&document.getElementById("content").textContent.includes("cincuenta monedas de plata")&&[...document.querySelectorAll(".evidence a")].some(a=>a.href.includes("5d8fEcawLU0"))');
  await route('#busqueda/Bonnie');
  await check('Buscar Bonnie en Kuroto no devuelve hechos de Xoltacan','!document.querySelector(".event")');
  for(const width of [320,390,768]){
    await call('Emulation.setDeviceMetricsOverride',{width,height:844,deviceScaleFactor:1,mobile:width<560});
    for(const section of ['campanas','inicio','capitulos','capitulo/1']){
      await route('#'+section);
      await check('Arghast y Kuroto sin desbordamiento a '+width+' px en '+section,'document.documentElement.scrollWidth<=window.innerWidth');
    }
  }
  await route('#inicio');await screenshot('kuroto-movil');
  await chooseCampaign('xoltacan');
  const restoredBackground=await readBackground('.workspace','::before');
  await check('Volver a Xoltacan recupera su fondo sin arrastrar el de Kuroto',JSON.stringify(restoredBackground?.key===xoltacanBackground.key));
  await check('Volver a Xoltacan restaura sus datos y limpia la búsqueda','!!document.querySelector(".hero-art")&&!document.querySelector(".kuroto-hero")&&document.getElementById("global-search").value===""');
  await route('#capitulo/1');
  await check('La ficha 1 de Xoltacan vuelve a ser la correcta','document.getElementById("page-title").textContent.includes("barco estampado")&&document.querySelector("a[target=_blank]").href.includes("ZXhsunFOVdQ")');
  const directKuroto=new URL('kuroto.html',siteURL);
  await call('Page.navigate',{url:directKuroto.href});
  for(let i=0;i<100;i++){try{if(await evaluate('location.pathname.endsWith("/kuroto.html")&&document.body.dataset.campaign==="kuroto"&&!!document.querySelector(".kuroto-hero")'))break;}catch{}await sleep(150);}
  await check('Kuroto tiene una entrada propia con su campaña seleccionada','location.pathname.endsWith("/kuroto.html")&&document.getElementById("campaign-selector").value==="kuroto"&&!!document.querySelector(".kuroto-hero")');
  if(errors.length)throw new Error('Errores JavaScript: '+JSON.stringify(errors));
  console.log(JSON.stringify({resultado:'OK',comprobaciones:checks.length,pruebas:checks,capturas:output},null,2));
  await send('Browser.close');
} finally {if(ws)ws.close();browser.kill();}
