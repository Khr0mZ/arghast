// Prueba real en Chrome/Edge de la interfaz autónoma mediante su protocolo local.
import fs from 'node:fs/promises';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const output=path.join(root,'.pruebas','interfaz');
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
  const target=await send('Target.createTarget',{url:pathToFileURL(path.join(root,'xoltacan.html')).href});
  const {sessionId}=await send('Target.attachToTarget',{targetId:target.targetId,flatten:true});
  const call=(method,params={})=>send(method,params,sessionId);
  await call('Runtime.enable');await call('Page.enable');
  const evaluate=async expression=>{const result=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(result.exceptionDetails)throw new Error(JSON.stringify(result.exceptionDetails));return result.result.value;};
  const check=async(name,expression)=>{if(!await evaluate(expression))throw new Error('Fallo: '+name);checks.push(name);};
  const route=async hash=>{await evaluate('location.hash='+JSON.stringify(hash));await sleep(160);};
  const screenshot=async name=>{const shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await fs.writeFile(path.join(output,name+'.png'),Buffer.from(shot.data,'base64'));};
  const checks=[];
  for(let i=0;i<70;i++){if(await evaluate('!!document.querySelector(".hero")'))break;await sleep(150);}
  await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1080,deviceScaleFactor:1,mobile:false});
  await check('Portada cargada desde archivo local','!!document.querySelector(".hero-title") && !!document.querySelector(".hero-art")');
  await check('Paisaje selvático integrado y decodificable sin conexión','(async()=>{const url=getComputedStyle(document.querySelector(".hero-art")).backgroundImage.slice(5,-2);if(!url.startsWith("data:image/webp;base64,"))return false;const image=new Image();image.src=url;await image.decode();return image.naturalWidth>1000})()');
  await check('Accesos de exploración de la isla','document.querySelectorAll(".expedition-links a").length===3');
  await check('39 episodios y 946 registros reales','(()=>{const d=JSON.parse(document.getElementById("xoltacan-data").textContent);return d.chapters.length===39&&d.facts.length===946&&Object.keys(d.transcripts).length===39})()');
  await check('Sin categoría editorial de contradicciones','![...document.querySelectorAll("#sidebar a")].some(a=>a.hash==="#contradicciones")');
  await check('Una ficha por nombre canónico','(()=>{const d=JSON.parse(document.getElementById("xoltacan-data").textContent);const n=d.entities.map(e=>e.name.normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").toLowerCase());return n.length===new Set(n).size})()');
  await check('Personajes y objetos separados','(()=>{const d=JSON.parse(document.getElementById("xoltacan-data").textContent);return d.entities.find(e=>e.name==="Patata Hammer").type==="objeto"&&d.entities.find(e=>e.name==="Patata").type==="personaje"&&d.entities.filter(e=>e.name==="Coyote").length===1})()');
  await screenshot('portada-escritorio');
  await evaluate('document.getElementById("global-search").value="Ilikar";document.getElementById("global-search").dispatchEvent(new Event("input",{bubbles:true}))');await sleep(350);
  await check('Búsqueda global de Ilikar','document.getElementById("content").innerText.includes("Ilikar") && document.querySelectorAll(".event").length>0');
  await evaluate('document.querySelector("[data-filter=chapter]").value="38";document.querySelector("[data-filter=chapter]").dispatchEvent(new Event("change",{bubbles:true}))');
  await check('Filtro por capítulo','[...document.querySelectorAll(".event-time strong")].every(e=>e.textContent==="38")');
  await route('#capitulos');await check('Catálogo completo navegable','document.querySelectorAll(".chapter-card").length===39');
  await check('Navegar retira el estado de búsqueda anterior','document.getElementById("search-status").textContent==="" && document.getElementById("global-search").value===""');
  await route('#capitulo/39');await check('El capítulo abre con el relato de su sesión','document.querySelector("[data-tab=relato]").classList.contains("active")&&document.querySelectorAll(".story-stage").length===4');
  await evaluate('document.querySelector("[data-tab=hechos]").click()');
  await check('Acontecimientos del capítulo 39','document.querySelectorAll(".event").length===20');
  await check('Notas de fuentes integradas en el capítulo','!!document.querySelector("details.context-details")&&!document.querySelector("[data-tab=contradicciones]")');
  await evaluate('document.querySelector("[data-tab=preguntas]").click()');
  await check('Cada pregunta de capítulo tiene seguimiento','document.querySelectorAll(".question-card").length===5&&[...document.querySelectorAll(".question-card")].every(e=>e.dataset.status==="pendiente")');
  await evaluate('document.querySelector("[data-tab=transcripcion]").click()');
  await check('Transcripción integrada y paginada','document.querySelectorAll(".transcript-row").length===120');
  await evaluate('document.getElementById("transcript-search").value="serpiente";document.getElementById("transcript-search").dispatchEvent(new Event("input",{bubbles:true}))');
  await check('Búsqueda en transcripción','document.querySelectorAll(".transcript-row").length>0&&[...document.querySelectorAll(".transcript-row p")].every(e=>e.textContent.toLowerCase().includes("serpiente"))');
  await route('#registro/39-010');
  await check('Cita y enlace al minuto','document.querySelector(".quote").textContent.length>0 && document.querySelector(".evidence a").href.includes("&t=")');
  await check('Contexto disponible','document.querySelectorAll(".context-details .transcript-row").length>0');
  await screenshot('evidencia-escritorio');
  for(const section of ['misterios','misiones','relaciones','nombres','metodo']){await route('#'+section);if(section==='misterios')await evaluate('document.querySelector("details.context-details").open=true');await check('Documento '+section,'document.querySelector(".document").innerText.length>100');}
  for(const [section,type] of [['personajes','personaje'],['atlas','lugar'],['facciones','faccion'],['objetos','objeto']]){
    await route('#'+section);
    await check('Catálogo exclusivo de '+section,`(()=>{const d=JSON.parse(document.getElementById("xoltacan-data").textContent);const names=[...document.querySelectorAll(".entity-card .card-title")].map(e=>e.textContent);return names.length>0&&names.every(n=>d.entities.find(e=>e.name===n).type===${JSON.stringify(type)})})()`);
    await check('Sin selector de categorías duplicado en '+section,'!document.querySelector("[data-filter=entityType]")');
  }
  await check('Menú sin catálogo general duplicado','![...document.querySelectorAll("#sidebar a")].some(a=>a.hash==="#entidades")');
  await route('#entidad/'+encodeURIComponent('Shiaru'));
  await check('Lugar vuelve a su sección y la resalta','document.querySelector("#content>.source-link").hash==="#atlas"&&document.querySelector("#sidebar a.active").hash==="#atlas"');
  await route('#entidad/'+encodeURIComponent('Marina'));
  await check('Facción vuelve a su sección y la resalta','document.querySelector("#content>.source-link").hash==="#facciones"&&document.querySelector("#sidebar a.active").hash==="#facciones"');
  await route('#misterios');await check('Misterios con referencias navegables','document.querySelectorAll(".document a[href*=registro]").length>10');
  await check('228 preguntas cotejadas con cierre completo del catálogo','(()=>{const s=JSON.parse(document.getElementById("xoltacan-data").textContent).seguimiento;return s.preguntas.length===228&&!s.estados.sin_revisar&&s.por_actualizar===0})()');
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
  await check('Contexto geográfico integrado','document.querySelector(".document").textContent.length>100');
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
  await check('Historia narrativa antes de las evidencias','document.querySelectorAll(".story-stage").length===4&&document.querySelector(".character-story").compareDocumentPosition(document.querySelector(".event"))===Node.DOCUMENT_POSITION_FOLLOWING');
  await screenshot('historia-personaje-escritorio');
  await evaluate('document.querySelector(".story-sources a").click()');await sleep(180);
  await check('Fuentes del relato abren la evidencia original','location.hash.startsWith("#registro/")&&!!document.querySelector(".quote")&&document.querySelector(".evidence a").href.includes("&t=")');
  await route('#capitulo/39');await screenshot('capitulo-escritorio');
  await route('#capitulos');await screenshot('capitulos-escritorio');
  for(const width of [320,768]){
    await call('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:width<560});
    for(const section of ['personajes','capitulo/39','misterios','entidad/Ione','entidad/Shiaru','entidad/Marina','entidad/Zampaolas']){
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
  await route('#personajes');await screenshot('personajes-movil');
  await route('#entidad/Ione');await screenshot('historia-personaje-movil');
  await route('#entidad/Zampaolas');await screenshot('relato-objeto-movil');
  await route('#entidad/Shiaru');await screenshot('relato-lugar-movil');
  if(errors.length)throw new Error('Errores JavaScript: '+JSON.stringify(errors));
  console.log(JSON.stringify({resultado:'OK',comprobaciones:checks.length,pruebas:checks,capturas:output},null,2));
  await send('Browser.close');
} finally {if(ws)ws.close();browser.kill();}
