// Copia solo el lector público de cada campaña y verifica su uso sin el repositorio.
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {cerrarProceso,eliminarTemporal} from './temporales_pruebas.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const output=path.join(root,'.pruebas/autonomia');
const fixture=path.join(root,'.pruebas','autonomia-'+Date.now());
const profile=path.join(output,'perfil-'+Date.now());
await fs.mkdir(profile,{recursive:true});
const browser=spawn('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',[
  '--headless=new','--no-sandbox','--disable-gpu','--no-first-run','--no-default-browser-check',
  '--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'
],{windowsHide:true,stdio:'ignore'});
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
let ws,id=0;const pending=new Map(),errors=[],requests=[],checks=[];
const deadline=setTimeout(()=>{browser.kill();throw new Error('La prueba de autonomía superó 120 segundos.');},120000);
try{
  let info;
  for(let i=0;i<100;i++){try{info=(await fs.readFile(path.join(profile,'DevToolsActivePort'),'utf8')).trim().split('\n');break;}catch{await sleep(150);}}
  if(!info)throw new Error('Edge no abrió su puerto de pruebas.');
  ws=new WebSocket('ws://127.0.0.1:'+info[0]+info[1]);
  await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true});});
  ws.addEventListener('message',event=>{
    const m=JSON.parse(String(event.data));
    if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);
    if(m.method==='Network.requestWillBeSent')requests.push(m.params.request.url);
    if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result);}
  });
  const send=(method,params={},sessionId)=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params,...(sessionId?{sessionId}:{})}));});
  const target=await send('Target.createTarget',{url:'about:blank'});
  const {sessionId}=await send('Target.attachToTarget',{targetId:target.targetId,flatten:true});
  const call=(method,params={})=>send(method,params,sessionId);
  await call('Runtime.enable');await call('Page.enable');await call('Network.enable');
  const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
  const ready=async expression=>{for(let i=0;i<100;i++){if(await evaluate(expression))return;await sleep(100);}throw new Error('No quedó lista: '+expression);};
  const check=async(name,expression)=>{if(!await evaluate(expression))throw new Error('Fallo: '+name);checks.push(name);};
  for(const campaign of ['xoltacan','kuroto']){
    const copy=path.join(fixture,campaign);
    await fs.cp(path.join(root,'campanas',campaign,'publico'),copy,{recursive:true});
    requests.length=0;
    await call('Page.navigate',{url:pathToFileURL(path.join(copy,'index.html')).href});
    await ready('!!document.querySelector(".hero")');
    await check(campaign+': abre su campaña por defecto',`document.body.dataset.campaign===${JSON.stringify(campaign)}`);
    await check(campaign+': carga únicamente sus datos',`Object.keys(globalThis.arghastCampaigns).join()===${JSON.stringify(campaign)}`);
    const chapter=await evaluate('JSON.parse(document.getElementById("xoltacan-data").textContent).chapters[0].capitulo');
    await evaluate('location.hash='+JSON.stringify('#capitulo/'+chapter));
    await ready('!!document.querySelector("[data-tab=transcripcion]")');
    await evaluate('document.querySelector("[data-tab=transcripcion]").click()');
    await ready('document.querySelectorAll(".transcript-row").length>0');
    await check(campaign+': abre y busca en su transcripción','!!document.getElementById("transcript-search")');
    const scene=await evaluate('JSON.parse(document.getElementById("xoltacan-data").textContent).writtenRole.scenes[0].id');
    await evaluate('location.hash='+JSON.stringify('#rol/'+scene));
    await ready('document.querySelectorAll(".role-message").length>0');
    await check(campaign+': abre los mensajes originales de su escena','document.querySelector(".role-transcript").textContent.length>0');
    const scenes=await evaluate('JSON.parse(document.getElementById("xoltacan-data").textContent).writtenRole.scenes');
    let attachment;
    for(const candidate of scenes){
      if((await fs.readFile(path.join(copy,candidate.sourceFile),'utf8')).includes('"adjuntos":[{')){attachment=candidate;break;}
    }
    if(!attachment)throw new Error('Falta una escena con adjuntos: '+campaign);
    await evaluate('location.hash='+JSON.stringify('#rol/'+attachment.id));
    await ready('document.querySelectorAll(".role-message").length>0&&location.hash==='+JSON.stringify('#rol/'+attachment.id));
    const link=await evaluate('[...document.querySelectorAll(".role-transcript a")].map(a=>a.href).find(h=>h.includes("/rol_escrito/adjuntos/"))');
    if(!link||!link.startsWith(pathToFileURL(copy+path.sep).href))throw new Error('Adjunto fuera de la campaña: '+link);
    await fs.access(fileURLToPath(link));checks.push(campaign+': adjunto conservado dentro de la copia');
    await sleep(150);
    const prefix=pathToFileURL(copy+path.sep).href;
    const outside=requests.filter(url=>!url.startsWith(prefix)&&!url.startsWith('data:'));
    if(outside.length)throw new Error('Dependencias fuera de '+campaign+': '+JSON.stringify(outside));
    checks.push(campaign+': ninguna petición fuera de su directorio');
  }
  if(errors.length)throw new Error(JSON.stringify(errors));
  const report={resultado:'OK',comprobaciones:checks.length,pruebas:checks};
  await fs.writeFile(path.join(output,'revision.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report,null,2));await send('Browser.close');
}finally{
  clearTimeout(deadline);if(ws)ws.close();await cerrarProceso(browser);
  await eliminarTemporal(profile);await eliminarTemporal(fixture);
}
