// Verifica escenas reales, sus fuentes locales y navegación en ambas campañas.
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const siteURL=new URL(process.env.ARGHAST_TEST_URL||pathToFileURL(path.join(root,'arghast.html')).href);
const html=await fs.readFile(fileURLToPath(siteURL),'utf8');
const archive=JSON.parse(html.match(/<script id="xoltacan-data" type="application\/json">(.*?)<\/script>/s)[1]);
const datasets={xoltacan:archive,kuroto:archive.campaigns.kuroto};
const output=path.join(root,'.pruebas/rol');await fs.mkdir(output,{recursive:true});
const profile=path.join(output,'perfil-'+Date.now());await fs.mkdir(profile,{recursive:true});
const browser=spawn('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',['--headless=new','--no-sandbox','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'],{windowsHide:true,stdio:'ignore'});
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
let ws,id=0;const pending=new Map(),errors=[],checks=[];
const deadline=setTimeout(()=>{browser.kill();throw new Error('La prueba de rol superó el plazo de 120 segundos.');},120000);
try {
  let info;for(let i=0;i<100;i++){try{info=(await fs.readFile(path.join(profile,'DevToolsActivePort'),'utf8')).trim().split('\n');break;}catch{await sleep(150);}}
  if(!info)throw new Error('Edge no abrió su puerto local de pruebas.');
  ws=new WebSocket('ws://127.0.0.1:'+info[0]+info[1]);
  await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true});});
  ws.addEventListener('message',event=>{const m=JSON.parse(String(event.data));if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result);}});
  const send=(method,params={},sessionId)=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params,...(sessionId?{sessionId}:{})}));});
  const target=await send('Target.createTarget',{url:'about:blank'});
  const {sessionId}=await send('Target.attachToTarget',{targetId:target.targetId,flatten:true});
  const call=(method,params={})=>send(method,params,sessionId);
  await call('Runtime.enable');await call('Page.enable');
  const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
  const check=async(name,expression)=>{if(!await evaluate(expression)){
    const detail=await evaluate(`({width:innerWidth,scroll:document.documentElement.scrollWidth,elements:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>321&&r.left>=0}).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,100),right:e.getBoundingClientRect().right})).slice(0,20)})`);
    await fs.writeFile(path.join(output,'error.json'),JSON.stringify({name,detail},null,2));
    const shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await fs.writeFile(path.join(output,'error.png'),Buffer.from(shot.data,'base64'));
    throw new Error('Fallo: '+name+' '+JSON.stringify(detail));
  }checks.push(name);};
  const route=async hash=>{await evaluate('location.hash='+JSON.stringify(hash));await sleep(160);};
  const ready=async expression=>{for(let i=0;i<80;i++){try{if(await evaluate(expression))return;}catch{}await sleep(100);}throw new Error('La interfaz no quedó lista: '+expression);};
  const screenshot=async name=>{const r=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await fs.writeFile(path.join(output,name+'.png'),Buffer.from(r.data,'base64'));};
  for(const [campaign,data] of Object.entries(datasets)){
    const scenes=data.writtenRole?.scenes||[];
    if(!scenes.length)throw new Error('No hay escenas reales de '+campaign+' para comprobar.');
    if(scenes.some(s=>s.fuentes))throw new Error('Los mensajes completos deben cargarse por escena.');
    const url=new URL(siteURL);url.searchParams.set('campana',campaign);url.hash='inicio';
    await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1080,deviceScaleFactor:1,mobile:false});
    await call('Page.navigate',{url:url.href});await ready('!!document.querySelector(".hero")');
    // Un nombre presente solo en mensajes también debe salir en la barra principal.
    await route('#rol');
    await evaluate('(()=>{const input=document.getElementById("role-search");input.value="tsugami";input.dispatchEvent(new Event("input",{bubbles:true}));})()');
    const roleMatches=await evaluate('[...document.querySelectorAll(".role-card")].map(a=>a.hash).sort()');
    if(!roleMatches.length)throw new Error('Falta el caso real de Tsugami en '+campaign);
    await evaluate('(()=>{const input=document.getElementById("global-search");input.focus();input.value="tsugami";input.dispatchEvent(new Event("input",{bubbles:true}));})()');
    await ready('location.hash==="#busqueda/tsugami"&&!!document.querySelector("[data-filter=searchType]")');
    if(campaign==='xoltacan')await check('xoltacan: el filtro nuevo conserva el rótulo de Ambystoma','document.querySelector("[data-filter=searchType]").closest("label").querySelector(".campaign-lettering").textContent==="Contenido"');
    await check(campaign+': búsqueda principal conserva foco','document.activeElement.id==="global-search"');
    await check(campaign+': buscar no descarga originales de las escenas','!globalThis.arghastWrittenRoleSources');
    await evaluate('(()=>{const select=document.querySelector("[data-filter=searchType]");select.value="rol";select.dispatchEvent(new Event("change",{bubbles:true}));})()');
    await check(campaign+': Tsugami encuentra las mismas escenas que el buscador de rol',`JSON.stringify([...document.querySelectorAll('.search-result[data-search-type="rol"]')].map(a=>a.hash).filter(hash=>hash.split('/').length===2).sort())===${JSON.stringify(JSON.stringify(roleMatches))}`);
    const originalOnly=roleMatches.find(hash=>{const scene=scenes.find(s=>hash==='#rol/'+s.id);return !JSON.stringify([scene.titulo,scene.resumen,scene.relato,scene.participantes]).toLowerCase().includes('tsugami');});
    if(!originalOnly)throw new Error('No hay una coincidencia exclusiva de los mensajes originales en '+campaign);
    await check(campaign+': incluye nombres ausentes del título y del relato',`[...document.querySelectorAll('.search-result')].some(a=>a.hash===${JSON.stringify(originalOnly)})`);
    await call('Emulation.setDeviceMetricsOverride',{width:320,height:780,deviceScaleFactor:1,mobile:true});
    await sleep(350);
    await check(campaign+': resultados y filtros caben en móvil','document.documentElement.scrollWidth<=320');
    await screenshot(campaign+'-busqueda-tsugami');
    await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1080,deviceScaleFactor:1,mobile:false});
    await evaluate('(()=>{const input=document.getElementById("global-search");input.value="TSÚGAMI";input.dispatchEvent(new Event("input",{bubbles:true}));})()');
    await ready('document.getElementById("search-status").textContent.includes("TSÚGAMI")');
    await check(campaign+': la consulta nueva restablece el filtro de contenido','document.querySelector("[data-filter=searchType]").value===""');
    await evaluate('(()=>{const select=document.querySelector("[data-filter=searchType]");select.value="rol";select.dispatchEvent(new Event("change",{bubbles:true}));})()');
    await check(campaign+': búsqueda ignora mayúsculas y tildes',`JSON.stringify([...document.querySelectorAll('.search-result')].map(a=>a.hash).filter(hash=>hash.split('/').length===2).sort())===${JSON.stringify(JSON.stringify(roleMatches))}`);
    await evaluate(`[...document.querySelectorAll('.search-result')].find(a=>a.hash===${JSON.stringify(originalOnly)}).click()`);
    const originalScene=scenes.find(s=>originalOnly==='#rol/'+s.id);
    await ready('document.querySelectorAll(".role-message").length==='+originalScene.mensajes);
    await check(campaign+': el resultado abre sus mensajes originales','document.querySelector(".role-transcript").textContent.toLowerCase().includes("tsugami")');
    await check(campaign+': las escenas encontradas pertenecen a la campaña elegida',`location.search.includes('campana=${campaign}')&&${JSON.stringify(roleMatches)}.every(hash=>hash.startsWith('#rol/${campaign==='xoltacan'?'x':'k'}-'))`);
    await call('Page.navigate',{url:'about:blank'});await ready('!document.getElementById("xoltacan-data")');
    await call('Page.navigate',{url:url.href});await ready('!!document.querySelector(".hero")');
    const search=async(query,type)=>{
      await evaluate('(()=>{const input=document.getElementById("global-search");input.value='+JSON.stringify(query)+';input.dispatchEvent(new Event("input",{bubbles:true}));})()');
      await ready('document.getElementById("search-status").textContent.endsWith('+JSON.stringify('resultados para '+query)+')');
      await evaluate('(()=>{const select=document.querySelector("[data-filter=searchType]");select.value='+JSON.stringify(type)+';select.dispatchEvent(new Event("change",{bubbles:true}));})()');
    };
    const searchedChapter=data.chapters[0],searchedEntity=data.entities[0],searchedQuestion=data.seguimiento.preguntas[0];
    for(const [name,query,type,href] of [
      ['crónicas',searchedChapter.titulo,'capitulo','#capitulo/'+searchedChapter.capitulo],
      ['historia de las fichas',searchedEntity.description||searchedEntity.name,searchedEntity.type,'#entidad/'+encodeURIComponent(searchedEntity.name)],
      ['preguntas y respuestas',searchedQuestion.pregunta,'pregunta','#pregunta/'+searchedQuestion.id],
      ['documentos de misiones','Misiones','documento','#misiones']
    ]){
      await search(query,type);
      await check(campaign+': búsqueda principal encuentra '+name,`[...document.querySelectorAll('.search-result')].some(a=>a.getAttribute('href')===${JSON.stringify(href)})`);
    }
    await search('metodo','documento');
    await check(campaign+': la búsqueda no ofrece la página de método',`![...document.querySelectorAll('.search-result')].some(a=>a.hash==='#metodo'||a.hash==='#documento/metodo')`);
    await search('a','rol');
    const firstPage=await evaluate('[...document.querySelectorAll(".search-result")].map(a=>a.hash)');
    await evaluate(`document.querySelector('[data-page="2"]').click()`);
    await check(campaign+': paginación incluye más resultados de rol',`document.querySelector('.pagination').textContent.includes('Página 2')&&[...document.querySelectorAll('.search-result')].every(a=>!${JSON.stringify(firstPage)}.includes(a.hash))`);
    await evaluate('document.querySelector("[data-reset]").click()');
    await check(campaign+': restablecer limpia filtros y vuelve a la primera página','document.querySelector("[data-filter=searchType]").value===""&&document.querySelector(".pagination").textContent.includes("Página 1")');
    await search('zzsincoincidencias987654321','');
    await check(campaign+': consulta sin resultados muestra un estado vacío','document.querySelector(".count").textContent==="0 resultados"&&!!document.querySelector(".empty")');
    await evaluate('document.getElementById("search-clear").click()');
    await ready('!!document.querySelector(".hero")');
    await check(campaign+': limpiar búsqueda vuelve a portada','document.getElementById("global-search").value===""&&document.getElementById("search-status").textContent===""');
    await check(campaign+': portada y pie sin página de método',`!document.querySelector('a[href="#metodo"]')`);
    for(const type of ['personaje','lugar','faccion','objeto']){
      const entity=data.entities.find(e=>e.type===type&&scenes.some(s=>(s.participantes||[]).some(p=>p===e.name||e.aliases.includes(p))))||data.entities.find(e=>e.type===type);
      await route('#entidad/'+encodeURIComponent(entity.name));
      await check(campaign+': '+type+' muestra sus apartados sin desplegables','!document.querySelector("#content details")&&[...document.querySelectorAll("[data-section-target]")].every(b=>!!document.getElementById(b.dataset.sectionTarget))');
      const paragraphs=(entity.history?.etapas||[]).map(stage=>stage.texto);
      await check(campaign+': '+type+' conserva todo su relato',`JSON.stringify([...document.querySelectorAll('.narrative-story .story-prose>p')].map(p=>p.textContent))===${JSON.stringify(JSON.stringify(paragraphs))}`);
      if(type==='personaje'){
        await check(campaign+': rol escrito antes de los registros de vídeo','!!document.querySelector(".role-card")&&!!(document.querySelector(".role-block").compareDocumentPosition(document.getElementById("entity-evidence-title"))&Node.DOCUMENT_POSITION_FOLLOWING)');
        await evaluate(`document.querySelector('[data-section-target="entity-role-title"]').click()`);
        await check(campaign+': saltar al rol conserva la ficha y lleva el foco al apartado','document.activeElement.id==="entity-role-title"&&location.hash.startsWith("#entidad/")&&document.activeElement.getBoundingClientRect().top>=0&&document.activeElement.getBoundingClientRect().top<innerHeight');
        await screenshot(campaign+'-perfil-rol-visible');
        await call('Emulation.setDeviceMetricsOverride',{width:320,height:780,deviceScaleFactor:1,mobile:true});await sleep(350);
        await evaluate('window.scrollTo({top:0,behavior:"instant"})');
        await check(campaign+': apartados de ficha y navegación caben en móvil','document.documentElement.scrollWidth<=320');
        await screenshot(campaign+'-perfil-apartados-movil');
        await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1080,deviceScaleFactor:1,mobile:false});
      }
    }
    for(const section of ['atlas','facciones']){
      await route('#'+section);
      await check(campaign+': '+section+' ofrece un acceso visible a su contexto',`[...document.querySelectorAll('.catalogue-views a')].some(a=>a.hash==='#documento/${section}')&&!document.querySelector('#content details')`);
      await route('#documento/'+section);
      await check(campaign+': contexto de '+section+' visible y situado en su sección',`document.querySelector('.document').innerText.length>100&&!document.querySelector('#content details')&&document.querySelector('#sidebar a.active').hash==='#${section}'`);
    }
    await route('#inicio');
    await check(campaign+': la portada lleva directamente a leer la historia','document.querySelector(".hero .primary-button").hash==="#lectura"&&document.querySelector(".hero .primary-button").textContent.includes("Leer historia")');
    await evaluate('document.querySelector(".hero .primary-button").click()');await ready('!!document.querySelector(".reading-stream")');
    await check(campaign+': el salto queda flotante desde el inicio','(()=>{const e=document.querySelector(".reading-jump"),r=e.getBoundingClientRect();return getComputedStyle(e).position==="fixed"&&r.top>=0&&r.bottom<=innerHeight&&r.right<=innerWidth})()');
    const total=data.chapters.length+scenes.length;
    await check(campaign+': empieza con varios relatos y carga solo el bloque necesario',`document.querySelectorAll('.reading-entry').length>=6&&document.querySelectorAll('.reading-entry').length<${total}&&Number(document.querySelector('.reading-stream').dataset.readingTotal)===${total}`);
    await evaluate('document.querySelector("[data-reading-jump-toggle]").click()');
    await check(campaign+': el índice llega a los relatos que aún no están cargados',`document.querySelectorAll('.reading-jump-results a').length===${total}&&document.querySelectorAll('.reading-entry').length<${total}`);
    await evaluate('document.querySelector("[data-reading-jump-close]").click()');
    await check(campaign+': lectura sin controles de paginación','!document.querySelector(".reading-pagination,#reading-page-select,[data-reading-next],[data-reading-previous]")');
    const initial=await evaluate('document.querySelectorAll(".reading-entry").length');
    await evaluate(`globalThis.__readingFirst=document.querySelector('.reading-entry');globalThis.__readingContext=__readingFirst.querySelector('.reading-context');window.scrollTo({behavior:"instant",top:Math.max(0,scrollY+document.querySelector('.reading-status').getBoundingClientRect().top-innerHeight-500)});globalThis.__readingY=scrollY`);
    await ready('document.querySelectorAll(".reading-entry").length>'+initial);
    await check(campaign+': añade relatos sin sustituir los ya abiertos','document.querySelector(".reading-entry")===globalThis.__readingFirst&&document.querySelector(".reading-entry .reading-context")===globalThis.__readingContext');
    await check(campaign+': conserva la posición al añadir contenido','Math.abs(scrollY-globalThis.__readingY)<3');
    await evaluate(`(async()=>{for(let i=0;i<${Math.ceil(total/6)+2};i++){const end=document.querySelector('.reading-status');if(end.dataset.finished==='true')return;window.scrollTo({behavior:"instant",top:Math.max(0,scrollY+end.getBoundingClientRect().top-innerHeight-500)});await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));}throw new Error('No termina la lectura continua');})()`);
    const options=await evaluate('[...document.querySelectorAll(".reading-entry")].map(e=>"#lectura/"+e.dataset.readingKind+"/"+e.dataset.readingId)');
    const expected=[...data.chapters.map(c=>'#lectura/capitulo/'+c.capitulo),...scenes.map(s=>'#lectura/rol/'+s.id)];
    if(options.length!==expected.length||new Set(options).size!==options.length||expected.some(href=>!options.includes(href)))throw new Error('La lectura no conserva todas las entradas de '+campaign);
    checks.push(campaign+': la carga completa conserva todos los capítulos y escenas una sola vez');
    for(const scene of scenes){
      const at=options.indexOf('#lectura/rol/'+scene.id),before=options.indexOf('#lectura/capitulo/'+scene.intervalo.anterior),after=options.indexOf('#lectura/capitulo/'+scene.intervalo.siguiente);
      if((before>=0&&at<=before)||(after>=0&&at>=after))throw new Error('Escena fuera de su intervalo: '+scene.id);
    }
    checks.push(campaign+': los bloques conservan todos los intervalos entre capítulos');
    await check(campaign+': el final detiene la carga y conserva un único aviso','document.querySelectorAll(".reading-status").length===1&&document.querySelector(".reading-status").dataset.finished==="true"&&document.querySelector(".reading-status").textContent.includes("Fin del contenido disponible")');
    await check(campaign+': el salto sigue visible tras recorrer la historia','(()=>{const r=document.querySelector("[data-reading-jump-toggle]").getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight})()');
    await evaluate('document.querySelector("[data-reading-jump-toggle]").click()');
    await check(campaign+': el índice incluye también capítulos y escenas no cargados',`!document.getElementById('reading-jump-panel').hidden&&document.querySelectorAll('.reading-jump-results a').length===${total}&&document.activeElement.id==='reading-jump-search'`);
    const lastChapter=data.chapters.at(-1);
    const query='Capítulo '+lastChapter.capitulo;
    await evaluate('(()=>{const input=document.getElementById("reading-jump-search");input.value='+JSON.stringify(query)+';input.dispatchEvent(new Event("input",{bubbles:true}));})()');
    await check(campaign+': buscar en el índice conserva foco y encuentra el capítulo',`document.activeElement.id==='reading-jump-search'&&[...document.querySelectorAll('.reading-jump-results a')].some(a=>a.hash===${JSON.stringify('#lectura/capitulo/'+lastChapter.capitulo)})`);
    await call('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape'});await sleep(100);
    await check(campaign+': Escape cierra el índice y devuelve el foco al botón','document.getElementById("reading-jump-panel").hidden&&document.activeElement.hasAttribute("data-reading-jump-toggle")');
    await evaluate('document.querySelector("[data-reading-jump-toggle]").click();[...document.querySelectorAll(".reading-jump-results a")].find(a=>a.hash==='+JSON.stringify('#lectura/capitulo/'+lastChapter.capitulo)+').click()');await sleep(200);
    await check(campaign+': el salto abre el capítulo elegido en la lectura continua',`location.hash===${JSON.stringify('#lectura/capitulo/'+lastChapter.capitulo)}&&document.querySelector('.reading-entry').dataset.readingId===${JSON.stringify(String(lastChapter.capitulo))}&&document.getElementById('reading-jump-panel').hidden`);
    const firstChapter=data.chapters.find(c=>c.history?.etapas?.length)||data.chapters[0];
    await route('#lectura/capitulo/'+firstChapter.capitulo);
    const chapterParagraphs=firstChapter.history?.etapas?.length?firstChapter.history.etapas.flatMap(s=>s.texto.split(/\n\s*\n/).filter(Boolean)):(firstChapter.resumen||'').split(/\n\s*\n/).filter(Boolean);
    await check(campaign+': el enlace al capítulo conserva su relato completo',`JSON.stringify([...document.querySelectorAll('.reading-entry:first-child .reading-prose p')].map(p=>p.textContent))===${JSON.stringify(JSON.stringify(chapterParagraphs))}`);
    await check(campaign+': fuentes y contexto visibles durante la lectura','!!document.querySelector("section.reading-context")&&!document.querySelector(".reading-context").closest("details")&&!!document.querySelector(".reading-context a")');
    await check(campaign+': leer el relato no descarga los mensajes originales','!globalThis.arghastWrittenRoleSources');
    await screenshot(campaign+'-lectura-escritorio');
    await evaluate('globalThis.__originalReadingObserver=globalThis.IntersectionObserver;globalThis.IntersectionObserver=undefined');
    await route('#lectura');
    const withoutObserver=await evaluate('document.querySelectorAll(".reading-entry").length');
    await evaluate('window.scrollTo({behavior:"instant",top:Math.max(0,scrollY+document.querySelector(".reading-status").getBoundingClientRect().top-innerHeight-500)})');
    await ready('document.querySelectorAll(".reading-entry").length>'+withoutObserver);
    checks.push(campaign+': la carga por desplazamiento también funciona sin IntersectionObserver');
    await evaluate('globalThis.IntersectionObserver=globalThis.__originalReadingObserver;delete globalThis.__originalReadingObserver');
    const storyScene=scenes.find(s=>s.relato.includes('\n\n'))||scenes[0];
    await route('#lectura/rol/'+storyScene.id);
    await check(campaign+': la escena conserva todo su relato editorial',`JSON.stringify([...document.querySelectorAll('.reading-entry:first-child .reading-prose p')].map(p=>p.textContent))===${JSON.stringify(JSON.stringify((storyScene.relato||storyScene.resumen).split(/\n\s*\n/).filter(Boolean)))}`);
    await check(campaign+': la escena enlaza sus mensajes originales',`document.querySelector('.reading-context a').hash===${JSON.stringify('#rol/'+storyScene.id)}`);
    await call('Emulation.setDeviceMetricsOverride',{width:320,height:780,deviceScaleFactor:1,mobile:true});await sleep(200);
    await check(campaign+': la lectura continua cabe a 320 píxeles','document.documentElement.scrollWidth<=320');
    await screenshot(campaign+'-lectura-movil');
    await evaluate('document.querySelector("[data-reading-jump-toggle]").click()');
    await check(campaign+': el índice flotante cabe y se puede usar en móvil','(()=>{const r=document.querySelector(".reading-jump-panel").getBoundingClientRect();return !document.getElementById("reading-jump-panel").hidden&&r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight&&document.documentElement.scrollWidth<=320})()');
    await screenshot(campaign+'-indice-movil');
    const jumpScene=scenes.at(-1);
    await evaluate('(()=>{const input=document.getElementById("reading-jump-search");input.value='+JSON.stringify(jumpScene.titulo)+';input.dispatchEvent(new Event("input",{bubbles:true}));})()');
    await check(campaign+': el índice permite encontrar una escena concreta',`[...document.querySelectorAll('.reading-jump-results a')].some(a=>a.hash===${JSON.stringify('#lectura/rol/'+jumpScene.id)})`);
    await evaluate('[...document.querySelectorAll(".reading-jump-results a")].find(a=>a.hash==='+JSON.stringify('#lectura/rol/'+jumpScene.id)+').click()');await sleep(200);
    await check(campaign+': el salto móvil comienza en la escena elegida',`document.querySelector('.reading-entry').dataset.readingId===${JSON.stringify(jumpScene.id)}&&document.getElementById('reading-jump-panel').hidden`);
    await route('#lectura/rol/'+storyScene.id);
    await evaluate('document.getElementById("menu-toggle").click()');
    await check(campaign+': el menú lateral queda por delante del salto','getComputedStyle(document.querySelector(".reading-jump")).visibility==="hidden"');
    await evaluate('document.getElementById("menu-toggle").click()');
    const mobileCount=await evaluate('document.querySelectorAll(".reading-entry").length');
    await evaluate('window.scrollTo({behavior:"instant",top:Math.max(0,scrollY+document.querySelector(".reading-status").getBoundingClientRect().top-innerHeight-500)})');
    await ready('document.querySelectorAll(".reading-entry").length>'+mobileCount);
    checks.push(campaign+': también carga nuevos relatos al desplazar la vista móvil');
    await route(options.at(-1));
    await check(campaign+': el enlace al último relato termina sin duplicarlo','document.querySelectorAll(".reading-entry").length===1&&document.querySelector(".reading-status").dataset.finished==="true"');
    const futureStory=scenes.find(s=>s.intervalo.ambito==='despues_del_catalogo');
    if(futureStory){await route('#lectura/rol/'+futureStory.id);await check(campaign+': la historia avisa de los vídeos intermedios ausentes','document.querySelector(".reading-entry").textContent.includes("Posterior al último vídeo incorporado")');}
    await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1080,deviceScaleFactor:1,mobile:false});
    await route('#rol');await ready('document.querySelectorAll(".role-card").length==='+scenes.length);
    await check(campaign+': un selector sustituye los botones repetidos','document.querySelectorAll(".chronicle-views").length===1&&document.querySelectorAll(".chronicle-views a").length===3&&!document.querySelector(".role-block .secondary-button")');
    await check(campaign+': listado completo sin duplicados',`document.querySelectorAll('.role-card').length===${scenes.length}&&new Set([...document.querySelectorAll('.role-card')].map(e=>e.dataset.roleId)).size===${scenes.length}`);
    await check(campaign+': los originales se abren al entrar en una escena','!globalThis.arghastWrittenRoleSources');
    const selected=scenes.find(s=>s.mensajes>10&&s.intervalo.ambito!=='despues_del_catalogo')||scenes[0];
    await route('#rol/'+selected.id);await ready('document.querySelectorAll(".role-message").length==='+selected.mensajes);
    await check(campaign+': mensajes íntegros de la escena',`document.querySelectorAll('.role-message').length===${selected.mensajes}&&globalThis.arghastWrittenRoleSources[${JSON.stringify(campaign+'/'+selected.id)}].length===${selected.mensajes}`);
    await check(campaign+': evidencias y relato visibles','document.querySelectorAll(".role-prose p").length>0&&document.querySelectorAll("[data-role-message]").length>0');
    await check(campaign+': ningún mensaje introduce HTML ejecutable','!document.querySelector("#content script,#content iframe,#content object")');
    await check(campaign+': las evidencias escritas se ven sin desplegarlas','!!document.querySelector(".role-evidence")&&!document.querySelector(".role-evidence").closest("details")');
    await evaluate('document.querySelector("[data-role-message]").click()');
    await check(campaign+': evidencia conserva la escena',`location.hash===${JSON.stringify('#rol/'+selected.id)}`);
    await check(campaign+': fuentes de horario separadas del relato','[...document.querySelectorAll(".context-details summary")].some(e=>e.textContent==="Fuentes de las fechas")');
    await screenshot(campaign+'-escena-escritorio');
    await call('Emulation.setDeviceMetricsOverride',{width:320,height:780,deviceScaleFactor:1,mobile:true});await sleep(350);
    await check(campaign+': escena sin desbordamiento a 320 píxeles','document.documentElement.scrollWidth<=320');
    await screenshot(campaign+'-escena-movil');
    await route('#rol');
    await evaluate('const i=document.getElementById("role-search");i.value='+JSON.stringify(selected.participantes[0]||selected.titulo.split(' ')[0])+';i.dispatchEvent(new Event("input",{bubbles:true}))');
    await check(campaign+': búsqueda conserva foco y muestra la escena',`document.activeElement.id==='role-search'&&[...document.querySelectorAll('.role-card')].some(e=>e.dataset.roleId===${JSON.stringify(selected.id)})`);
    await route('#capitulos');
    await check(campaign+': capítulos y escenas tienen accesos visibles y contadores',`!document.querySelector('.chapter-grid details')&&[...document.querySelectorAll('.chronicle-views a')].some(a=>a.hash==='#rol'&&a.querySelector('.chronicle-view-count').textContent==='${scenes.length}')`);
    await check(campaign+': crónicas sin desbordamiento a 320 píxeles','document.documentElement.scrollWidth<=320');
    const numbers=data.chapters.map(c=>c.capitulo);
    await check(campaign+': ningún enlace inventa un capítulo',`[...document.querySelectorAll('#content a[href^="#capitulo/"]')].every(e=>${JSON.stringify(numbers)}.includes(Number(e.hash.split('/')[1])))`);
    const future=scenes.find(s=>s.intervalo.ambito==='despues_del_catalogo');
    if(future){
      await route('#rol/'+future.id);await ready('document.querySelectorAll(".role-message").length==='+future.mensajes);
      await check(campaign+': rol futuro distingue los vídeos pendientes','document.getElementById("content").textContent.includes("Posterior al último vídeo incorporado")');
    }
    const audio=scenes.find(s=>s.notas_de_voz>0);
    if(audio){
      await route('#rol/'+audio.id);await ready('document.querySelectorAll(".role-message").length==='+audio.mensajes);
      await check(campaign+': todas las notas de voz distinguen transcripción automática',`document.querySelectorAll('.role-audio-transcript').length===${audio.notas_de_voz}&&document.querySelector('.role-audio-transcript').textContent.includes('Puede contener errores')`);
    }
    if(data.writtenRole.integration?.length){
      for(const section of ['misiones','misterios','relaciones','nombres']){
        await route('#'+section);
        await check(campaign+': '+section+' enlaza el seguimiento del rol','document.querySelectorAll(".role-followup-entry").length>0');
        await check(campaign+': seguimiento de '+section+' visible sin desplegables','!!document.querySelector("section.role-followup")&&[...document.querySelectorAll(".role-followup-entry")].every(e=>!e.closest("details"))');
        await check(campaign+': seguimiento de '+section+' cabe a 320 píxeles','document.documentElement.scrollWidth<=320');
      }
      const href=await evaluate('document.querySelector(".role-followup-sources a").getAttribute("href")');
      await route(href);await ready('!!document.getElementById("mensaje-'+href.split('/').at(-1)+'")');await sleep(200);
      await check(campaign+': el seguimiento abre el mensaje preciso','(()=>{const id=location.hash.split("/").at(-1),r=document.getElementById("mensaje-"+id).getBoundingClientRect();return r.top<innerHeight&&r.bottom>0})()');
    }
  }
  if(errors.length)throw new Error(JSON.stringify(errors));
  const report={resultado:'OK',comprobaciones:checks.length,pruebas:checks};
  await fs.writeFile(path.join(output,'revision.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));await send('Browser.close');
} finally {clearTimeout(deadline);if(ws)ws.close();browser.kill();}
