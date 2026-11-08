import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const workspace=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const testRoot=path.join(workspace,'.pruebas');

export async function cerrarProceso(process){
  if(!process||process.exitCode!==null||process.signalCode)return;
  await new Promise(resolve=>{
    const finish=()=>{clearTimeout(timeout);process.removeListener('exit',finish);process.removeListener('error',finish);resolve();};
    const timeout=setTimeout(finish,5000);
    process.once('exit',finish);process.once('error',finish);process.kill();
  });
}

export async function eliminarTemporal(target){
  const absolute=path.resolve(target);
  const relative=path.relative(testRoot,absolute);
  if(!relative||relative==='..'||relative.startsWith('..'+path.sep)||path.isAbsolute(relative)
      ||!/^(perfil(?:-\d+)?|edicion-\d+|autonomia-\d+)$/.test(path.basename(absolute))){
    throw new Error('Temporal fuera de los directorios de pruebas: '+absolute);
  }
  try{
    const actual=await fs.realpath(absolute),base=path.join(await fs.realpath(workspace),'.pruebas');
    const checked=path.relative(base,actual);
    if(!checked||checked==='..'||checked.startsWith('..'+path.sep)||path.isAbsolute(checked)
        ||(await fs.lstat(absolute)).isSymbolicLink())throw new Error('No se eliminan enlaces fuera de las pruebas: '+absolute);
  }catch(error){if(error.code==='ENOENT')return;throw error;}
  await fs.rm(absolute,{recursive:true,force:true,maxRetries:10,retryDelay:150});
}
