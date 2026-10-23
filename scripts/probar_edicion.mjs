// Prueba de dos lectores, código, guardado, historial y persistencia en un navegador real.
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const output=path.join(root,'.pruebas','edicion-'+Date.now());
await fs.mkdir(output,{recursive:true});
const db=path.join(output,'test.sqlite3');
const python=process.env.ARGHAST_PYTHON||'python';
const server=spawn(python,['-u','-c',"import sys; sys.path.insert(0,'scripts'); from servidor_edicion import ArchiveServer, ROOT; s=ArchiveServer(('127.0.0.1',0),ROOT,sys.argv[1],'showmethemoney'); print(s.server_port,flush=True); s.serve_forever()",db],{cwd:root,windowsHide:true,stdio:['ignore','pipe','pipe']});
let browser,ws;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const checks=[];
try {
  const port=await new Promise((resolve,reject)=>{let buffer='';server.stdout.on('data',chunk=>{buffer+=chunk;if(buffer.includes('\n'))resolve(Number(buffer.trim()));});server.on('error',reject);server.on('exit',code=>reject(new Error('Servidor detenido: '+code)));server.stderr.on('data',chunk=>process.stderr.write(chunk));});
  let binary;
  for(const candidate of ['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','C:/Program Files/Google/Chrome/Application/chrome.exe']){try{await fs.access(candidate);binary=candidate;break;}catch{}}
  if(!binary)throw new Error('No se encontró Chrome/Edge.');
  const profile=path.join(output,'perfil');
  browser=spawn(binary,['--headless=new','--no-sandbox','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'],{windowsHide:true,stdio:'ignore'});
  let info;
  for(let i=0;i<100;i++){try{info=(await fs.readFile(path.join(profile,'DevToolsActivePort'),'utf8')).trim().split('\n');break;}catch{await sleep(150);}}
  if(!info)throw new Error('No se pudo iniciar el navegador.');
  ws=new WebSocket('ws://127.0.0.1:'+info[0]+info[1]);
  await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true});});
  let id=0;const pending=new Map();
  ws.addEventListener('message',event=>{const result=JSON.parse(String(event.data));if(pending.has(result.id)){const p=pending.get(result.id);pending.delete(result.id);result.error?p.reject(new Error(JSON.stringify(result.error))):p.resolve(result.result);}});
  const send=(method,params={},sessionId)=>new Promise((resolve,reject)=>{const next=++id;pending.set(next,{resolve,reject});ws.send(JSON.stringify({id:next,method,params,...(sessionId?{sessionId}:{})}));});
  const {targetId}=await send('Target.createTarget',{url:`http://127.0.0.1:${port}/?campana=xoltacan#capitulo/1`});
  const {sessionId}=await send('Target.attachToTarget',{targetId,flatten:true});
  const call=(method,params={})=>send(method,params,sessionId);
  const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
  async function waitFor(expression){for(let i=0;i<100;i++){try{if(await evaluate(expression))return;}catch(error){if(!/Inspected target navigated|Cannot find context|Execution context was destroyed/.test(error.message))throw error;}await sleep(100);}throw new Error('Tiempo agotado: '+expression);}
  async function check(name,expression){if(!await evaluate(expression))throw new Error(name);checks.push(name);}
  await call('Runtime.enable');await call('Page.enable');
  await waitFor('!!document.querySelector(".editor-status")');
  async function route(hash){await evaluate('location.hash='+JSON.stringify(hash));await sleep(100);}
  async function unlock(){await evaluate('document.activeElement?.blur()');for(const key of 'showmethemoney')await call('Input.dispatchKeyEvent',{type:'keyDown',key,text:key});await waitFor('!!document.querySelector(".editor-inline")');}
  async function edit(kind){await evaluate('document.querySelector("[data-edit-kind='+kind+']").click()');await waitFor('!!document.querySelector(".editor-session [data-control]")');}
  async function set(path,value){await evaluate(`(()=>{const node=[...document.querySelectorAll('.editor-session [data-field-path]')].find(n=>n.dataset.fieldPath===${JSON.stringify(JSON.stringify(path))});if(!node)throw new Error('Campo no encontrado: '+${JSON.stringify(path.join('.'))});if(node.type==='checkbox')node.checked=${JSON.stringify(value)};else node.value=${JSON.stringify(value)};node.dispatchEvent(new Event('input',{bubbles:true}));})()`);}
  async function save(){await evaluate('(()=>{const f=document.querySelector(".editor-session form");f.elements.author.value="Jugador";f.elements.reason.value="Corrección de la sesión";f.requestSubmit();})()');await waitFor('!document.querySelector(".editor-session")');}
  async function cancel(){await evaluate('document.querySelector(".editor-session [data-cancel]").click()');await waitFor('!document.querySelector(".editor-session")');}
  // Reproducir una revisión ilegible y una lectura que llega después de abrir
  // un borrador; el servidor Python sigue usando una base de datos temporal.
  const {identifier:syncTestScript}=await call('Page.addScriptToEvaluateOnNewDocument',{source:`(()=>{
    const realFetch=window.fetch.bind(window),realInterval=window.setInterval.bind(window);
    window.__editorTestMode='unreadable';
    window.setInterval=(fn,delay,...args)=>{if(delay===30000)window.__editorTestSync=fn;return realInterval(fn,delay,...args);};
    window.fetch=async(input,init)=>{
      if(String(input).includes('/api/editor/document/xoltacan')){
        if(window.__editorTestMode==='unreadable')return new Response('documento comprimido ilegible',{headers:{'Content-Type':'application/json'}});
        if(window.__editorTestMode==='delayed'){const url=new URL(input,location.href);url.searchParams.delete('since');const response=await realFetch(url,init);return new Promise(resolve=>window.__editorTestRelease=()=>resolve(response));}
      }
      return realFetch(input,init);
    };
  })();`});
  await call('Page.reload');await waitFor('window.__editorTestMode==="unreadable" && !!document.querySelector(".editor-status")');
  await check('No se crean diálogos, tampoco para introducir el código','!document.querySelector("dialog")');
  await check('El lector consulta sin controles de edición','!document.querySelector(".editor-inline")');
  await check('No hay acceso visible para activar la edicion','!document.querySelector(".editor-auth") && document.querySelector(".editor-exit").hidden && ![...document.querySelectorAll("button")].some(b=>b.textContent.includes("Activar"))');
  for(const key of 'showmethemoney')await call('Input.dispatchKeyEvent',{type:'keyDown',key,text:key});
  await waitFor('!document.querySelector(".editor-exit").hidden && document.querySelector(".editor-status").textContent.includes("No se ha podido")');
  await check('Una revisión ilegible impide editar con una revisión inicial incorrecta','!document.querySelector(".editor-inline,.editor-session")');
  await evaluate('window.__editorTestMode="normal";window.__editorTestSync()');await waitFor('!!document.querySelector(".editor-inline")');
  await check('La edición vuelve a estar disponible al recuperar la revisión','document.querySelector(".editor-status").textContent===""');
  await call('Page.removeScriptToEvaluateOnNewDocument',{identifier:syncTestScript});
  for(const section of ['personajes','atlas','facciones','objetos']){
    await route('#'+section);await waitFor('!!document.querySelector("a.entity-card")');
    await check('Xoltacan · '+section+' tiene un Editar independiente por tarjeta','[...document.querySelectorAll("a.entity-card")].every(a=>a.parentElement.querySelectorAll(":scope > [data-edit-kind=entidad]").length===1) && !document.querySelector("a.entity-card button")');
  }
  await route('#personajes');
  const originalName=await evaluate('document.querySelector("a.entity-card .card-title").textContent');
  await evaluate('window.__editorTestMode="delayed";window.__editorTestSync()');await waitFor('typeof window.__editorTestRelease==="function"');
  await edit('entidad');
  await check('Editar convierte la tarjeta en editable en el mismo catálogo','location.hash==="#personajes" && !!document.querySelector(".editor-card-shell.editor-session article.entity-card") && !document.querySelector("dialog,[name=field],[name=structure]")');
  await check('Nombre, descripción e historia se editan a la vez y en su lugar','!!document.querySelector(".editor-session .card-title textarea") && !!document.querySelector(".editor-session .card-copy textarea") && !!document.querySelector(".editor-session .story-prose textarea")');
  await set(['name'],'Borrador que se cancela');
  await evaluate('window.__editorTestMode="normal";window.__editorTestRelease()');await sleep(150);
  await check('Una sincronización tardía conserva el borrador y su formulario','document.querySelector(".editor-session .card-title textarea")?.value==="Borrador que se cancela"');
  await cancel();
  await check('Cancelar recupera la tarjeta sin guardar','document.querySelector("a.entity-card .card-title").textContent==='+JSON.stringify(originalName));
  await edit('entidad');await evaluate('document.querySelector(".editor-session [data-delete]").click()');
  await waitFor('!!document.querySelector("dialog[open] [data-delete-confirm]")');
  await check('Eliminar muestra un aviso con el nombre y el paso de guardado','document.querySelector("dialog").textContent.includes('+JSON.stringify(originalName)+') && document.querySelector("dialog").textContent.includes("Guardar eliminación")');
  await evaluate('document.querySelector("[data-delete-cancel]").click()');await waitFor('!document.querySelector("dialog")');
  await check('Cancelar el aviso no marca la eliminación','[...document.querySelectorAll(".editor-session [type=submit]")].every(b=>b.textContent==="Guardar cambios")');
  await evaluate('document.querySelector(".editor-session [data-delete]").click()');await waitFor('!!document.querySelector("dialog[open]")');
  await call('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});await call('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});await waitFor('!document.querySelector("dialog")');
  await check('Escape también cancela el aviso','[...document.querySelectorAll(".editor-session [type=submit]")].every(b=>b.textContent==="Guardar cambios")');
  await evaluate('document.querySelector(".editor-session [data-delete]").click()');await waitFor('!!document.querySelector("dialog[open]")');
  await evaluate('document.querySelector("[data-delete-confirm]").click()');await waitFor('!document.querySelector("dialog")');
  await check('La confirmación cambia ambos botones de guardar a Guardar eliminación','document.querySelectorAll(".editor-session [type=submit]").length===2 && [...document.querySelectorAll(".editor-session [type=submit]")].every(b=>b.textContent==="Guardar eliminación")');
  await check('Confirmar el aviso todavía no escribe en la campaña','(async()=>{const r=await (await fetch("/api/editor/document/xoltacan")).json();return r.revision===0})()');
  await evaluate('document.querySelector(".editor-session [data-delete]").click()');
  await check('Se puede deshacer la marca antes de guardar','[...document.querySelectorAll(".editor-session [type=submit]")].every(b=>b.textContent==="Guardar cambios")');await cancel();
  await edit('entidad');await set(['name'],'Nombre corregido inline');await set(['description'],'Descripción corregida en la tarjeta');await set(['history','etapas',0,'texto'],'Historia corregida en su propio lugar.');
  await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1080,deviceScaleFactor:1,mobile:false});await sleep(350);await evaluate('document.querySelector(".editor-session").scrollIntoView({block:"start"})');
  const desktop=await call('Page.captureScreenshot',{format:'png'});await fs.writeFile(path.join(output,'tarjeta-inline.png'),Buffer.from(desktop.data,'base64'));
  await save();
  await check('Guardar actualiza la tarjeta y mantiene el catálogo','location.hash==="#personajes" && [...document.querySelectorAll("a.entity-card .card-title")].some(n=>n.textContent==="Nombre corregido inline")');
  await call('Page.reload');await waitFor('!!document.querySelector(".editor-status") && !document.querySelector(".editor-inline") && [...document.querySelectorAll("a.entity-card .card-title")].some(n=>n.textContent==="Nombre corregido inline")');
  await check('Los cambios se conservan al recargar sin código','!document.querySelector(".editor-inline")');
  await unlock();await route('#entidad/'+encodeURIComponent('Nombre corregido inline'));await edit('entidad');
  await check('La ficha permite editar el nombre y el relato dentro de su diseño','!!document.querySelector(".editor-session .section-head h1 textarea") && !!document.querySelector(".editor-session .entity-intro textarea") && !!document.querySelector(".editor-session .story-stage .story-prose textarea")');
  const allKeys=await evaluate('(()=>{const names=new Set([...document.querySelectorAll(".editor-session [data-field-path]")].map(n=>JSON.parse(n.dataset.fieldPath)[0]));return [...names];})()');
  if(!['name','description','type','note','aliases','history'].every(k=>allKeys.includes(k)))throw new Error('No están disponibles todos los datos de la ficha: '+allKeys);
  checks.push('Los datos se presentan juntos sin selector de campo');
  await set(['history','etapas',0,'titulo'],'Etapa modificada inline');
  await evaluate('(()=>{const f=document.querySelector(".editor-session form");f.elements.optional.value="__custom";f.elements.optional.dispatchEvent(new Event("change"));f.elements.newLabel.value="Apariencia";f.elements.newType.value="text";document.querySelector("[data-add-field]").click();})()');
  await set(['informacion_adicional','Apariencia'],'Sombrero coral');
  await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});await sleep(400);
  await check('La ficha en edición no desborda el móvil','document.documentElement.scrollWidth<=innerWidth');
  await evaluate('document.querySelector(".editor-session .section-head").scrollIntoView()');
  const shot=await call('Page.captureScreenshot',{format:'png'});await fs.writeFile(path.join(output,'ficha-inline-movil.png'),Buffer.from(shot.data,'base64'));
  await save();
  await check('Se guardan juntos la etapa y los campos añadidos','document.querySelector(".story-prose h3").textContent==="Etapa modificada inline" && document.querySelector(".editor-additional").textContent.includes("Sombrero coral")');
  const firstFact=await evaluate('JSON.parse(document.getElementById("xoltacan-data").textContent).facts[0].id');
  await route('#registro/'+firstFact);await edit('registro');
  await check('La cita y el acontecimiento también se editan sobre el contenido','!!document.querySelector(".editor-session .quote textarea") && !document.querySelector(".transcript textarea,.transcript [contenteditable]")');
  await set(['cita'],'Cita corregida inline');await save();
  await check('La cita corregida se muestra tras guardar','document.querySelector(".quote").textContent==="Cita corregida inline"');
  await edit('registro');await evaluate('document.querySelector(".editor-session [data-delete]").click()');await waitFor('!!document.querySelector("dialog[open]")');await evaluate('document.querySelector("[data-delete-confirm]").click()');await waitFor('!document.querySelector("dialog")');await save();
  await check('La eliminación se aplica al guardar y se limpian las referencias','(async()=>{const r=await (await fetch("/api/editor/document/xoltacan")).json();return !r.content.facts.some(f=>f.id==='+JSON.stringify(firstFact)+')})()');
  await call('Page.navigate',{url:`http://127.0.0.1:${port}/?campana=kuroto#personajes`});await waitFor('document.body?.dataset.campaign==="kuroto" && !!document.querySelector(".editor-status")');await unlock();
  for(const section of ['personajes','atlas','facciones','objetos']){
    await route('#'+section);await waitFor('!!document.querySelector("a.entity-card")');await edit('entidad');
    await check('Kuroto · '+section+' se edita inline sin diálogo','!!document.querySelector(".editor-session .card-title textarea") && !document.querySelector("dialog,[name=field]")');await cancel();
  }
  await route('#capitulo/1');await evaluate('document.querySelector("[data-tab=transcripcion]").click()');await waitFor('document.querySelectorAll(".transcript-row").length>0');await edit('capitulo');
  await check('La transcripción continúa de solo lectura mientras se edita el capítulo','document.querySelectorAll(".transcript-row").length>0 && !document.querySelector(".transcript textarea,.transcript input:not([type=search]),.transcript [contenteditable]")');
  await cancel();
  await evaluate('document.querySelector(".footer > button").click()');await waitFor('!document.querySelector(".editor-inline")');
  for(const key of 'showmethemoney')await call('Input.dispatchKeyEvent',{type:'keyDown',key,text:key});await waitFor('!!document.querySelector(".editor-inline")');
  await check('El código tecleado activa el modo sin diálogos','!document.querySelector("dialog")');
  await route('#documento/atlas');await waitFor('!!document.querySelector(".document h1")');await edit('documento');
  const originalContext=await evaluate('JSON.parse(document.getElementById("xoltacan-data").textContent).campaigns.kuroto.documents.atlas.text');
  await set(['text'],originalContext+'\n\nNota de contexto de la prueba.');await save();
  await check('Editar el contexto conserva su vista y el documento visible','location.hash==="#documento/atlas"&&document.querySelector(".document").innerText.includes("Nota de contexto de la prueba.")&&document.querySelector("#sidebar a.active").hash==="#atlas"');
  console.log(JSON.stringify({checks,output},null,2));
} finally {
  ws?.close();browser?.kill();server.kill();
}
