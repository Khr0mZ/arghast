/* API alojada: objetos persistentes, historial y escrituras condicionales R2. */
import {validate} from './modelo.mjs';
import {sources} from './sources.mjs';

const allowedOrigin='https://khr0mz.github.io';
const conflict='Otro jugador ha guardado cambios en esta campaña. Copia tu borrador, cierra y vuelve a abrir el editor para comparar.';
const encoder=new TextEncoder();
const hash=async value=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',encoder.encode(value))),b=>b.toString(16).padStart(2,'0')).join('');
const json=(value,status=200)=>Response.json(value,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
const fail=(status,message)=>json({error:message},status);
const keyFor=campaign=>`campaigns/${campaign}/head.json`;
async function head(bucket,campaign){const obj=await bucket.get(keyFor(campaign));return {etag:obj?.etag,value:obj?await obj.json():{revision:0,history:[]}};}
async function limit(bucket,ip){
  const minute=Math.floor(Date.now()/60000),key=`attempts/${minute}/${await hash(ip)}`;
  for(let i=0;i<5;i++){
    const obj=await bucket.get(key),count=obj?Number(await obj.text()):0;
    if(count>=10)return false;
    if(await bucket.put(key,String(count+1),{onlyIf:obj?{etagMatches:obj.etag}:{etagDoesNotMatch:'*'}})) return true;
  }
  return false;
}
async function cleanup(bucket){
  // Borrar solo objetos de autenticación caducados; nunca documentos o historial.
  const now=Date.now(),pages=await Promise.all(['sessions/','attempts/'].map(prefix=>bucket.list({prefix,limit:1000})));
  const keys=pages.flatMap(page=>page.objects).filter(o=>now-new Date(o.uploaded).getTime()>9*3600000).map(o=>o.key);
  if(keys.length)await bucket.delete(keys);
}
async function handle(request,env,ctx){
  const url=new URL(request.url),path=url.pathname,bucket=env.BUCKET;
  if(path==='/health' && request.method==='GET')return json({ok:!!bucket && !!env.ARGHAST_EDIT_CODE});
  if(request.method==='GET' && path.startsWith('/api/editor/document/')){
    const campaign=path.slice('/api/editor/document/'.length);
    if(!Object.hasOwn(sources,campaign))return fail(404,'Campaña desconocida.');
    const {value}=await head(bucket,campaign),selected=url.searchParams.get('revision');
    if(selected!==null){
      const version=value.history.find(r=>String(r.revision)===selected);
      if(!version)return fail(404,'Versión no disponible.');
      const obj=await bucket.get(`campaigns/${campaign}/versions/${version.revision}.json.gz`);
      if(!obj)return fail(503,'No se ha podido recuperar esta versión.');
      return new Response(obj.body,{headers:{'Content-Type':'application/json; charset=utf-8','Content-Encoding':'gzip','Cache-Control':'no-store'}});
    }
    if(url.searchParams.get('since')===String(value.revision))return json({unchanged:true});
    if(value.revision===0)return json({original:true,revision:0,history:[]});
    const obj=await bucket.get(`campaigns/${campaign}/versions/${value.revision}.json.gz`);
    if(!obj)return fail(503,'No se ha podido recuperar la campaña.');
    return new Response(obj.body,{headers:{'Content-Type':'application/json; charset=utf-8','Content-Encoding':'gzip','Cache-Control':'no-store'}});
  }
  if(request.method!=='POST')return fail(404,'Ruta no disponible.');
  if(!['/api/editor/unlock','/api/editor/lock','/api/editor/save-document'].includes(path))return fail(404,'Ruta no disponible.');
  if(request.headers.get('Content-Type')?.split(';')[0]!=='application/json')return fail(415,'Se requiere JSON.');
  if(Number(request.headers.get('Content-Length'))>15000000)return fail(413,'El documento es demasiado grande.');
  const raw=await request.text();
  if(encoder.encode(raw).length>15000000)return fail(413,'El documento es demasiado grande.');
  let body;try{body=JSON.parse(raw);}catch{return fail(400,'Solicitud no válida.');}
  if(!body || typeof body!=='object' || Array.isArray(body))return fail(400,'Solicitud no válida.');
  if(path==='/api/editor/unlock'){
    if(!env.ARGHAST_EDIT_CODE)return fail(503,'El servicio de edición no está configurado.');
    if(!await limit(bucket,request.headers.get('CF-Connecting-IP')||'anonymous'))return fail(429,'Espera un minuto antes de volver a intentarlo.');
    if(typeof body.code!=='string' || await hash(body.code)!==await hash(env.ARGHAST_EDIT_CODE))return fail(403,'Código incorrecto.');
    const token=crypto.randomUUID()+crypto.randomUUID();
    await bucket.put('sessions/'+await hash(token),String(Date.now()+8*3600000));
    ctx.waitUntil(cleanup(bucket).catch(()=>{}));
    return json({token});
  }
  const token=request.headers.get('Authorization')?.replace(/^Bearer /,''),sessionKey='sessions/'+await hash(token||'');
  const session=token?await bucket.get(sessionKey):null;
  if(!session || Number(await session.text())<=Date.now())return fail(401,'Introduce el código para activar la edición.');
  if(path==='/api/editor/lock'){await bucket.delete(sessionKey);return json({ok:true});}
  const {campaign,author,reason}=body;
  if(typeof campaign!=='string' || !Object.hasOwn(sources,campaign))return fail(400,'Campaña desconocida.');
  if(![author,reason].every(v=>typeof v==='string' && v.trim()) || author.length>100 || reason.length>1000)return fail(400,'Escribe tu nombre y el motivo del cambio.');
  const current=await head(bucket,campaign);
  if(body.revision!==current.value.revision)return fail(409,conflict);
  let content;try{content=validate(body.content,sources[campaign]);}catch(error){return fail(400,error.message||'Contenido no válido.');}
  const revision=Date.now()*1000+crypto.getRandomValues(new Uint32Array(1))[0]%1000;
  const history=[...current.value.history,{revision,campaign,author:author.trim(),reason:reason.trim(),created:Date.now()/1000}];
  const versionKey=`campaigns/${campaign}/versions/${revision}.json.gz`;
  const bytes=await new Response(new Blob([JSON.stringify({content,revision,history})]).stream().pipeThrough(new CompressionStream('gzip'))).arrayBuffer();
  if(!await bucket.put(versionKey,bytes,{onlyIf:{etagDoesNotMatch:'*'}}))return fail(409,conflict);
  const saved=await bucket.put(keyFor(campaign),JSON.stringify({revision,history}),{onlyIf:current.etag?{etagMatches:current.etag}:{etagDoesNotMatch:'*'}});
  if(!saved){await bucket.delete(versionKey);return fail(409,conflict);}
  return json({ok:true});
}
export default {
  async fetch(request,env,ctx){
    const origin=request.headers.get('Origin');
    if(origin && origin!==allowedOrigin && origin!==new URL(request.url).origin)return fail(403,'Origen no permitido.');
    let response;
    if(request.method==='OPTIONS') response=new Response(null,{status:204});
    else try{response=await handle(request,env,ctx);}catch{response=fail(503,'El servicio de edición no está disponible. Conserva tu borrador y vuelve a intentarlo.');}
    const headers=new Headers(response.headers);
    if(origin){headers.set('Access-Control-Allow-Origin',origin);headers.set('Vary','Origin');}
    headers.set('Access-Control-Allow-Methods','GET, POST, OPTIONS');
    headers.set('Access-Control-Allow-Headers','Content-Type, Authorization');
    headers.set('Access-Control-Max-Age','86400');
    return new Response(response.body,{status:response.status,headers});
  }
};
