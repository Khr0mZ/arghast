(() => {
  'use strict';
  const config=/* LOADING_CONFIG */{};
  const root=document.documentElement;
  let generation=0,label='';
  const shells=()=>[document.getElementById('sidebar'),document.querySelector('.workspace')].filter(Boolean);
  function setLabel(node,text){
    if(!node)return;
    node.textContent=text;
    const key=root.dataset.loadingCampaign==='xoltacan'?config.lettering?.[text]:null;
    node.classList.toggle('loading-lettering',Boolean(key));
    if(key)node.dataset.lettering=key;else delete node.dataset.lettering;
  }
  function start(target=location.href){
    generation++;
    const url=new URL(target,location.href);
    const id=url.searchParams.get('campana')||config.defaultCampaign;
    const campaign=url.hash==='#campanas'?'':Object.hasOwn(config.names,id)?id:'';
    root.dataset.loadingCampaign=campaign;
    label='Cargando '+(config.names[campaign]||'Arghast')+'…';
    root.classList.add('archive-loading');
    const screen=document.getElementById('loading-screen');if(screen)screen.hidden=false;
    setLabel(document.getElementById('loading-label'),label);
    setLabel(document.getElementById('loading-retry-label'),'Volver a intentar');
    const spinner=document.getElementById('loading-spinner');if(spinner)spinner.hidden=false;
    const retry=document.getElementById('loading-retry');if(retry)retry.hidden=true;
    shells().forEach(node=>{node.inert=true;node.setAttribute('aria-busy','true');});
  }
  async function ready(){
    const current=++generation;
    await document.fonts.ready;
    await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
    if(current!==generation)return;
    shells().forEach(node=>{node.inert=false;node.removeAttribute('aria-busy');});
    document.getElementById('loading-screen').hidden=true;
    root.classList.remove('archive-loading');
  }
  function fail(message){
    generation++;
    document.getElementById('loading-spinner').hidden=true;
    setLabel(document.getElementById('loading-label'),message);
    document.getElementById('loading-retry').hidden=false;
  }
  function mount(){
    setLabel(document.getElementById('loading-label'),label);
    setLabel(document.getElementById('loading-retry-label'),'Volver a intentar');
    document.getElementById('loading-retry').addEventListener('click',()=>location.reload());
  }
  document.addEventListener('click',event=>{
    if(event.defaultPrevented||event.button!==0||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
    const link=event.target.closest('a[href]');
    if(!link||link.hasAttribute('download')||(link.target&&link.target!=='_self'))return;
    const target=new URL(link.href,location.href);
    if(target.origin===location.origin&&target.pathname===location.pathname&&target.search!==location.search&&Object.hasOwn(config.names,target.searchParams.get('campana'))){
      start(target.href);
    }
  });
  window.addEventListener('pageshow',event=>{if(event.persisted)ready();});
  window.archiveLoading={start,ready,fail,mount};
  start();
})();
