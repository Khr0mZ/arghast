// Retiene los datos en un servidor local para comprobar el estado que ve el usuario.
import fs from 'node:fs/promises';
import http from 'node:http';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {cerrarProceso,eliminarTemporal} from './temporales_pruebas.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const palettes=Object.fromEntries(await Promise.all(['xoltacan','kuroto'].map(async id=>[id,JSON.parse(await fs.readFile(path.join(root,'campanas',id,'config/paleta.json'),'utf8')).campanas[id].map(hex=>'rgb('+[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)).join(', ')+')')])));
const output=path.join(root,'.pruebas/carga');
const profile=path.join(output,'perfil-'+Date.now());
await fs.mkdir(profile,{recursive:true});
let held=[],blocked=true,failNext=false;
const server=http.createServer(async(req,res)=>{
  const name=new URL(req.url,'http://localhost').pathname;
  if(name==='/api/editor/document/xoltacan'||name==='/api/editor/document/kuroto'){res.writeHead(404);res.end('{}');return;}
  if(name!=='/arghast.html'&&!/^\/campanas\/(xoltacan|kuroto)\/publico\/datos\.js$/.test(name)){res.writeHead(404);res.end();return;}
  if(name.endsWith('datos.js')&&failNext){failNext=false;res.writeHead(404);res.end();return;}
  const serve=async()=>{
    try{const data=await fs.readFile(path.join(root,name));res.writeHead(200,{'Content-Type':name.endsWith('.js')?'application/javascript':'text/html; charset=utf-8','Cache-Control':'no-store'});res.end(data);}
    catch{res.writeHead(500);res.end();}
  };
  if(name.endsWith('datos.js')&&blocked)held.push(serve);else await serve();
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const base='http://127.0.0.1:'+server.address().port+'/arghast.html';
const release=async()=>{blocked=false;const queue=held;held=[];await Promise.all(queue.map(serve=>serve()));};
const browser=spawn('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',[
  '--headless=new','--no-sandbox','--disable-gpu','--no-first-run','--no-default-browser-check',
  '--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'
],{windowsHide:true,stdio:'ignore'});
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
let ws,id=0;const pending=new Map(),errors=[],checks=[];
const deadline=setTimeout(()=>{browser.kill();throw new Error('La prueba de carga superó 120 segundos.');},120000);
try{
  let info;
  for(let i=0;i<100;i++){try{info=(await fs.readFile(path.join(profile,'DevToolsActivePort'),'utf8')).trim().split('\n');break;}catch{await sleep(150);}}
  if(!info)throw new Error('Edge no abrió su puerto de pruebas.');
  ws=new WebSocket('ws://127.0.0.1:'+info[0]+info[1]);
  await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true});});
  ws.addEventListener('message',event=>{
    const m=JSON.parse(String(event.data));if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);
    if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result);}
  });
  const send=(method,params={},sessionId)=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params,...(sessionId?{sessionId}:{})}));});
  const target=await send('Target.createTarget',{url:'about:blank'});
  const {sessionId}=await send('Target.attachToTarget',{targetId:target.targetId,flatten:true});
  const call=(method,params={})=>send(method,params,sessionId);
  await call('Runtime.enable');await call('Page.enable');
  const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
  const ready=async expression=>{for(let i=0;i<120;i++){try{if(await evaluate(expression))return;}catch{}await sleep(100);}throw new Error('No quedó lista: '+expression);};
  const check=async(name,expression)=>{if(!await evaluate(expression))throw new Error('Fallo: '+name);checks.push(name);};
  const screenshot=async name=>{const shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await fs.writeFile(path.join(output,name+'.png'),Buffer.from(shot.data,'base64'));};
  const loaded=()=>ready('!document.documentElement.classList.contains("archive-loading")');
  const checkFont=async(name,selector,expected)=>{
    await evaluate('document.fonts.ready');await call('DOM.enable');await call('CSS.enable');
    const {root:dom}=await call('DOM.getDocument',{depth:0});
    const {nodeId}=await call('DOM.querySelector',{nodeId:dom.nodeId,selector});
    const {fonts}=await call('CSS.getPlatformFontsForNode',{nodeId});
    const names=fonts.map(f=>f.familyName.replace(/\s+/g,'').toLowerCase());
    if(!fonts.length||!fonts.every(f=>f.isCustomFont)||!names.some(n=>n.includes(expected))||names.some(n=>!n.includes(expected)&&!n.includes('kaiseitokumin')))throw new Error('Fuente incorrecta en '+name+': '+JSON.stringify(fonts));
    checks.push(name+': fuente local real '+fonts.map(f=>f.familyName).join(', '));
  };
  const loading=async(name,label,campaign)=>{
    await ready('!!document.getElementById("loading-screen")&&!document.getElementById("loading-screen").hidden');
    for(let i=0;i<100&&held.length<2;i++)await sleep(50);
    if(held.length!==2)throw new Error('Falta retener los datos: '+name);
    await check(name+': spinner visible antes de recibir los datos',`document.getElementById('loading-label').textContent===${JSON.stringify('Cargando '+label+'…')}&&getComputedStyle(document.getElementById('loading-spinner')).animationName==='archive-spin'`);
    await check(name+': la interfaz intermedia está oculta e inerte','[document.getElementById("sidebar"),document.querySelector(".workspace")].every(n=>n.inert&&n.getAttribute("aria-busy")==="true"&&getComputedStyle(n).visibility==="hidden")');
    await check(name+': color de la campaña de destino',`document.documentElement.dataset.loadingCampaign===${JSON.stringify(campaign)}`);
    if(campaign){
      await check(name+': fondo, texto y spinner usan la paleta oficial',`(()=>{const allowed=${JSON.stringify(palettes[campaign])},screen=getComputedStyle(document.getElementById('loading-screen')),spinner=getComputedStyle(document.getElementById('loading-spinner'));return [screen.backgroundColor,screen.color,spinner.borderTopColor,spinner.borderBottomColor].every(c=>allowed.includes(c))})()`);
    }
  };
  await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
  await call('Page.navigate',{url:base+'#campanas'});
  await loading('Arghast','Arghast','');await checkFont('Arghast','#loading-label','imfellenglishsc');await screenshot('arghast');await release();await loaded();
  await check('Al terminar se muestra el archivo y se habilitan sus controles','document.getElementById("loading-screen").hidden&&document.querySelectorAll(".world-campaign").length===2&&!document.getElementById("sidebar").inert&&!document.querySelector(".workspace").hasAttribute("aria-busy")');
  blocked=true;
  await evaluate('document.querySelector(".world-campaign-xoltacan").click()');
  await loading('Enlace a Xoltacan','Xoltacan','xoltacan');
  await check('Xoltacan: Ambystoma como gráfico con texto accesible','(async()=>{const label=document.getElementById("loading-label"),style=getComputedStyle(label,"::after");if(label.textContent!=="Cargando Xoltacan…"||!label.classList.contains("loading-lettering")||getComputedStyle(label).webkitTextFillColor!=="rgba(0, 0, 0, 0)"||!style.maskImage.startsWith(\'url("data:image/png;base64,\'))return false;const image=new Image();image.src=style.maskImage.slice(5,-2);await image.decode();return image.naturalWidth>100})()');
  await screenshot('xoltacan');
  await call('Emulation.setDeviceMetricsOverride',{width:320,height:780,deviceScaleFactor:1,mobile:true});
  await check('Xoltacan: el rótulo cabe en el móvil','(()=>{const r=document.getElementById("loading-label").getBoundingClientRect();return r.left>=24&&r.right<=innerWidth-24&&document.documentElement.scrollWidth===innerWidth})()');
  await screenshot('xoltacan-movil');
  await release();await loaded();
  await check('El enlace termina en la portada de Xoltacan','document.body.dataset.campaign==="xoltacan"&&!!document.querySelector(".hero")');
  blocked=true;
  await evaluate('(()=>{const select=document.getElementById("campaign-selector");select.value="kuroto";select.dispatchEvent(new Event("change",{bubbles:true}));})()');
  await loading('Selector a Kuroto','Kuroto','kuroto');
  await checkFont('Kuroto','#loading-label','karate');
  await call('Emulation.setDeviceMetricsOverride',{width:320,height:780,deviceScaleFactor:1,mobile:true});
  await check('El indicador cubre el móvil sin desbordamiento','(()=>{const r=document.getElementById("loading-screen").getBoundingClientRect();return r.width===innerWidth&&r.height===innerHeight&&document.documentElement.scrollWidth===innerWidth})()');
  await screenshot('kuroto-movil');
  await call('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
  await check('Respeta la preferencia de movimiento reducido','getComputedStyle(document.getElementById("loading-spinner")).animationName==="none"');
  await release();await loaded();
  await check('El selector termina en la portada de Kuroto','document.body.dataset.campaign==="kuroto"&&!!document.querySelector(".kuroto-hero")');
  blocked=false;failNext=true;
  await call('Page.navigate',{url:base+'?campana=xoltacan#inicio'});
  await ready('!!document.getElementById("loading-retry")&&!document.getElementById("loading-retry").hidden');
  await check('Un error ofrece reintentar y detiene el spinner','document.getElementById("loading-label").textContent.includes("No se pudieron abrir los datos")&&document.getElementById("loading-spinner").hidden&&document.querySelector(".workspace").inert');
  await check('Xoltacan: el botón de reintento también usa Ambystoma','document.getElementById("loading-retry-label").classList.contains("loading-lettering")&&getComputedStyle(document.getElementById("loading-retry-label"),"::after").maskImage.startsWith(\'url("data:image/png;base64,\')&&!document.getElementById("loading-label").classList.contains("loading-lettering")');
  await screenshot('error-movil');await evaluate('document.getElementById("loading-retry").click()');await loaded();
  await check('Reintentar recupera el archivo','document.body.dataset.campaign==="xoltacan"&&!!document.querySelector(".hero")');
  if(errors.length)throw new Error(JSON.stringify(errors));
  const report={resultado:'OK',comprobaciones:checks.length,pruebas:checks};
  await fs.writeFile(path.join(output,'revision.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report,null,2));await send('Browser.close');
}finally{
  clearTimeout(deadline);if(ws)ws.close();await release();await cerrarProceso(browser);
  await new Promise(resolve=>server.close(resolve));await eliminarTemporal(profile);
}
