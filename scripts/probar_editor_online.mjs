/* Verifica el contrato real del Worker sin escribir en las campañas publicadas. */
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';

const root=resolve(import.meta.dirname,'..');
const source=await readFile(resolve(root,'.pruebas/editor-online/worker/index.js'),'utf8');
const worker=(await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'))).default;
const html=await readFile(resolve(root,'arghast.html'),'utf8');
const world=JSON.parse(html.match(/<script id="xoltacan-data" type="application\/json">(.*?)<\/script>/s)[1]);
class Bucket {
  objects=new Map();
  async get(key){
    const obj=this.objects.get(key);if(!obj)return null;
    const bytes=Buffer.from(obj.bytes);
    return {...obj,key,body:new Blob([bytes]).stream(),text:async()=>bytes.toString(),json:async()=>JSON.parse(bytes.toString())};
  }
  async put(key,value,options={}){
    const bytes=typeof value==='string'?Buffer.from(value):Buffer.from(await new Response(value).arrayBuffer());
    const existing=this.objects.get(key),condition=options.onlyIf;
    if(condition?.etagMatches && existing?.etag!==condition.etagMatches)return null;
    if(condition?.etagDoesNotMatch==='*' && existing)return null;
    const obj={bytes,etag:createHash('sha256').update(bytes).digest('hex'),uploaded:new Date()};
    this.objects.set(key,obj);return obj;
  }
  async delete(keys){for(const key of Array.isArray(keys)?keys:[keys])this.objects.delete(key);}
  async list({prefix,limit}){return {objects:[...this.objects].filter(([key])=>key.startsWith(prefix)).slice(0,limit).map(([key,obj])=>({...obj,key}))};}
}
const env={BUCKET:new Bucket(),ARGHAST_EDIT_CODE:'codigo-solo-de-prueba'},pending=[];
const ctx={waitUntil:p=>pending.push(p)};
async function request(path,body,token='',origin='https://khr0mz.github.io',method=body?'POST':'GET'){
  const response=await worker.fetch(new Request('https://editor.example/api/editor'+path,{method,headers:{Origin:origin,'Content-Type':'application/json',Authorization:'Bearer '+token},...(body?{body:JSON.stringify(body)}:{})}),env,ctx);
  // El cuerpo que entrega el Worker debe ser JSON. Workers aplica por su cuenta
  // Content-Encoding al transmitir: descomprimir aquí ocultaba la doble compresión.
  assert.equal(response.headers.get('Content-Encoding'),null);
  const result=response.status===204?null:await response.json();
  return {status:response.status,result,headers:response.headers};
}
assert.equal((await request('/unlock',{code:'incorrecto'})).status,403);
assert.equal((await request('/unlock',{code:env.ARGHAST_EDIT_CODE},'','https://otra.example')).status,403);
assert.equal((await request('/unlock',undefined,'','https://khr0mz.github.io','OPTIONS')).status,204);
const unlocked=await request('/unlock',{code:env.ARGHAST_EDIT_CODE}),token=unlocked.result.token;
assert.equal(unlocked.status,200);assert.equal(unlocked.headers.get('Access-Control-Allow-Origin'),'https://khr0mz.github.io');
for(const [campaign,data] of [['xoltacan',world],['kuroto',world.campaigns.kuroto]]){
  const content=structuredClone(Object.fromEntries(['chapters','facts','entities','seguimiento','documents'].map(k=>[k,data[k]])));
  content.chapters.forEach(c=>c._source=String(c.capitulo));
  const baseline=await request('/document/'+campaign);assert.equal(baseline.result.original,true);
  const body={campaign,content,revision:0,author:'Prueba local',reason:'Verificar el guardado remoto con el documento real'};
  assert.equal((await request('/save-document',body)).status,401);
  assert.equal((await request('/save-document',{...body,content:{...content,transcripts:{}}},token)).status,400);
  const damaged=structuredClone(content);damaged.chapters[0]._source='no-existe';
  assert.equal((await request('/save-document',{...body,content:damaged},token)).status,400);
  const invalid=structuredClone(content);invalid.entities[0].facts=['referencia-rota'];
  assert.equal((await request('/save-document',{...body,content:invalid},token)).status,400);
  const concurrent=await Promise.all([request('/save-document',body,token),request('/save-document',body,token)]);
  assert.deepEqual(concurrent.map(r=>r.status).sort(),[200,409]);
  const saved=await request('/document/'+campaign);assert.equal(saved.status,200);
  assert.equal(saved.result.content.entities[0].name,content.entities[0].name);
  assert.equal(saved.result.history.length,1);assert.equal(Object.hasOwn(saved.result.content,'transcripts'),false);
  const revision=saved.result.revision;
  assert.equal((await request('/document/'+campaign+'?since='+revision)).result.unchanged,true);
  assert.deepEqual((await request('/document/'+campaign+'?revision='+revision)).result.content,saved.result.content);
  assert.equal((await request('/save-document',body,token)).status,409);
  // Una nueva instancia del Worker lee los mismos objetos persistentes.
  const second=(await import('data:text/javascript;base64,'+Buffer.from(source+'\n// restart').toString('base64'))).default;
  const response=await second.fetch(new Request('https://editor.example/api/editor/document/'+campaign+'?since='+revision),env,ctx);
  assert.equal((await response.json()).unchanged,true);
  const changed=structuredClone(saved.result.content);changed.facts[0].cita='Corrección posterior a la primera versión';
  assert.equal((await request('/save-document',{...body,content:changed,revision},token)).status,200);
  const updated=await request('/document/'+campaign);
  assert.equal(updated.result.content.facts[0].cita,changed.facts[0].cita);
  assert.equal(updated.result.history.length,2);
  assert.notEqual(updated.result.revision,revision);
  assert.deepEqual((await request('/document/'+campaign+'?revision='+revision)).result.content,saved.result.content);
  assert.equal((await request('/save-document',{...body,revision},token)).status,409);
  console.log(campaign+': guardado completo, concurrencia, historial, persistencia y transcripciones protegidas');
}
assert.equal((await request('/lock',{},token)).status,200);
assert.equal((await request('/save-document',{},token)).status,401);
for(let i=0;i<8;i++)assert.equal((await request('/unlock',{code:'incorrecto'})).status,403);
assert.equal((await request('/unlock',{code:env.ARGHAST_EDIT_CODE})).status,429);
await Promise.all(pending);
console.log('Contrato de edición online verificado. No se ha escrito ningún dato en servicios externos.');
