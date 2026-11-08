import fs from 'node:fs/promises';
import path from 'node:path';

export async function leerArchivo(root){
  const html=await fs.readFile(path.join(root,'arghast.html'),'utf8');
  const manifest=JSON.parse(html.match(/<script id="xoltacan-data" type="application\/json">(.*?)<\/script>/s)[1]);
  if(!manifest.campaignFiles)return manifest;
  const campaigns={};
  for(const [id,file] of Object.entries(manifest.campaignFiles)){
    const text=await fs.readFile(path.join(root,file),'utf8');
    const prefix='globalThis.arghastCampaigns['+JSON.stringify(id)+']=';
    const data=JSON.parse(text.split(prefix)[1].trim().replace(/;$/,''));
    campaigns[id]={...data,resourceBase:path.posix.dirname(file)+'/'};
  }
  const primary=manifest.rootCampaignId||'xoltacan';
  return {...campaigns[primary],...manifest,campaigns:Object.fromEntries(Object.entries(campaigns).filter(([id])=>id!==primary))};
}
