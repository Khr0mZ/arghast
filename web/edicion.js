/* Edición sobre el contenido, sin diálogos ni selector de campos. */
window.createArchiveEditor=function({data,campaignId,content,refresh,lettering}) {
  const clone=v=>JSON.parse(JSON.stringify(v));
  const escape=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const keys=['chapters','facts','entities','seguimiento','documents'];
  const original=Object.fromEntries(keys.map(k=>[k,clone(data[k])]));
  original.chapters.forEach(c=>c._source=String(c.capitulo));
  const sourceRows={...data.transcripts},sourceFiles={...data.transcriptFiles};
  let token='',revision=0,versions=[],loaded=false,active=null,sequence='',rememberedName='',syncGeneration=0;
  const footer=document.querySelector('.footer');
  const toggle=document.createElement('button');toggle.type='button';toggle.className='secondary-button editor-exit';toggle.textContent='Salir de edición';toggle.hidden=true;footer.append(toggle);
  const status=document.createElement('span');status.className='editor-status';status.setAttribute('role','status');footer.append(status);
  const snapshot=()=>Object.fromEntries(keys.map(k=>[k,clone(data[k])]));
  const service=location.hostname==='khr0mz.github.io'?'https://arghast-editor.ivan-osorio440384.chatgpt.site':'';
  async function request(path,body){
    const response=await fetch(service+'/api/editor'+path,{method:body?'POST':'GET',cache:'no-store',headers:body?{'Content-Type':'application/json',...(token?{Authorization:'Bearer '+token}:{})}:{},...(body?{body:JSON.stringify(body)}:{})});
    let result;try{result=await response.json();}catch{throw new Error('No se ha podido conectar con el servicio de edición.');}
    if(!response.ok){if(response.status===401){token='';toggle.hidden=true;if(!active)refresh();}throw new Error(result.error||'No se ha podido guardar.');}return result;
  }
  function apply(result){
    if(result.original)result={...result,content:clone(original)};
    for(const c of data.chapters){const rows=data.transcripts[String(c.capitulo)];if(rows?.length)sourceRows[c._source??String(c.capitulo)]=rows;}
    revision=result.revision;versions=result.history;for(const k of keys)data[k]=result.content[k];
    data.transcripts={};data.transcriptFiles={};
    for(const c of data.chapters)if(c._source!=null){data.transcripts[String(c.capitulo)]=sourceRows[c._source]||[];if(sourceFiles[c._source])data.transcriptFiles[String(c.capitulo)]=sourceFiles[c._source];}
    refresh();
  }
  async function sync(){
    if(active||location.protocol==='file:')return false;
    const generation=++syncGeneration;
    try{const result=await request('/document/'+campaignId+(loaded?'?since='+revision:''));if(active||generation!==syncGeneration)return false;loaded=true;if(!result.unchanged)apply(result);status.textContent='';return true;}
    catch(error){if(generation!==syncGeneration)return false;loaded=false;if(token)status.textContent=error.message;if(!active)refresh();return false;}
  }
  async function authorize(code){
    if(location.protocol==='file:'){status.textContent='Abre la versión con el servicio local para guardar los cambios.';return;}
    try{const result=await request('/unlock',{code});token=result.token;toggle.hidden=false;if(!active){await sync();refresh();}else status.textContent='Edición activada. Puedes guardar tu borrador.';}
    catch(error){status.textContent=error.message;}
  }
  toggle.onclick=async()=>{
    if(active){active.message.textContent='Guarda o cancela los cambios antes de salir de la edición.';return;}
    try{await request('/lock',{});token='';toggle.hidden=true;refresh();}catch(error){status.textContent=error.message;}
  };
  document.addEventListener('keydown',event=>{
    if(event.ctrlKey||event.metaKey||event.altKey||event.target.closest('input,textarea,select,[contenteditable]'))return;
    if(event.key.length!==1){sequence='';return;}sequence=(sequence+event.key.toLowerCase()).slice(-14);
    if(sequence==='showmethemoney'){sequence='';if(!token)authorize('showmethemoney');}
  });
  document.addEventListener('click',event=>{
    const link=event.target.closest('a[href]');
    if(active&&link&&!link.target){event.preventDefault();event.stopImmediatePropagation();active.message.textContent='Guarda o cancela los cambios antes de navegar.';}
  },true);
  window.addEventListener('beforeunload',event=>{if(active){event.preventDefault();event.returnValue='';}});
    const groups={capitulo:['chapters','capitulo','Crónicas'],entidad:['entities','name','Fichas'],registro:['facts','id','Acontecimientos'],pregunta:['questions','id','Misterios'],documento:['documents',null,'Documentos'],archivo:[null,null,'Archivo de campaña']};
  const collection=(s,kind)=>kind==='pregunta'?s.seguimiento.preguntas:s[groups[kind][0]];
  function find(s,kind,identity){if(kind==='archivo')return s;if(kind==='documento')return s.documents[identity];return collection(s,kind).find(o=>String(o[groups[kind][1]])===String(identity));}
  const names={capitulo:'Capítulo',id:'Identificador',titulo:'Título',url:'Enlace del episodio',resumen:'Resumen',estado:'Estado',registros:'Registros',misiones:'Misiones',preguntas:'Preguntas',contradicciones:'Contradicciones',nombres:'Nombres',duracion:'Duración',history:'Relato por etapas',etapas:'Etapas',texto:'Texto',referencias:'Referencias',revisado_hasta:'Revisado hasta',name:'Nombre',facts:'Acontecimientos relacionados',aliases:'Alias',note:'Identificación',type:'Tipo de ficha',description:'Descripción',references:'Referencias',tipo:'Tipo de evidencia',afirmacion:'Relato del acontecimiento',inicio:'Inicio',fin:'Fin',cita:'Cita',entidades:'Entidades',ambito:'Ámbito',confianza:'Confianza',limitacion:'Alcance de la evidencia',pregunta:'Pregunta',respuesta:'Respuesta',pendiente:'Sigue pendiente',title:'Título',text:'Contenido',seguimiento:'Seguimiento de misterios',chapters:'Crónicas',entities:'Fichas',documents:'Documentos',evidencia_cue:'Localización de la cita',etiquetas_originales:'Etiquetas',_source:'Transcripción original'};
  Object.assign(names,{indice:'Orden de la pregunta',requiere_actualizacion:'Necesita revisar sesiones posteriores',referencias_origen:'Fuentes de la pregunta',sha256_pregunta:'Huella de la pregunta',fuente_transcripcion:'Procedencia de la transcripción',comprobacion_subtitulos:'Disponibilidad de subtítulos',transcripcion_disponible:'Hay transcripción disponible',informacion_adicional:'Información adicional',id:'Código de la entrada'});
  const label=k=>names[k]||String(k).replaceAll('_',' ');
  const choiceLabels={personaje:'Personaje',lugar:'Lugar',faccion:'Facción',objeto:'Vestigio',resuelta:'Resuelto',parcial:'Parcialmente resuelto',pendiente:'Pendiente',sin_revisar:'Sin revisar',revisado:'Revisado',hecho_confirmado:'Acción confirmada',declaracion_personaje:'Declaración de un personaje',explicacion_director:'Explicación del director',especulacion_jugadores:'Teoría de los jugadores',desconocido:'Sin confirmar',alta:'Alta',media:'Media',baja:'Baja'};
  const hints={id:'Este código identifica la entrada y sus enlaces. Al cambiarlo se actualizan sus referencias.',history:'Añade las etapas de su historia y ordénalas según ocurrieron.',facts:'Elige los acontecimientos que forman parte de esta ficha.',references:'Elige las fuentes que respaldan esta información.',referencias:'Busca el acontecimiento por su título o por la sesión.',inicio:'Momento del vídeo: horas, minutos y segundos.',fin:'Final del intervalo en el vídeo.',aliases:'Otros nombres por los que se conoce a esta entidad.',revisado_hasta:'Última sesión que se ha tenido en cuenta para este relato.',note:'Aclaraciones sobre quién o qué representa esta ficha.'};
  function replaceReferences(s,oldValue,newValue,fields){
    function walk(o){if(!o||typeof o!=='object')return;for(const [k,v]of Object.entries(o)){if(fields.includes(k)&&Array.isArray(v))o[k]=v.flatMap(x=>x===oldValue?(newValue===null?[]:[newValue]):[x]);else walk(v);}}walk(s);
  }
  function reconcile(s,kind,before,after){
    if(kind==='entidad'&&before.name!==after.name){replaceReferences(s,before.name,after.name,['entidades']);if(!after.aliases.includes(before.name))after.aliases.push(before.name);}
    if(kind==='registro'&&before.id!==after.id)replaceReferences(s,before.id,after.id,['registros','facts','references','referencias','referencias_origen']);
    if(kind==='capitulo'&&before.capitulo!==after.capitulo)for(const row of [...s.facts,...s.seguimiento.preguntas])if(row.capitulo===before.capitulo)row.capitulo=after.capitulo;
  }
  function remove(s,kind,identity){
    const before=find(s,kind,identity);
    if(kind==='documento'){delete s.documents[identity];return;}
    if(kind==='capitulo'){
      for(const f of s.facts.filter(f=>f.capitulo===before.capitulo))replaceReferences(s,f.id,null,['registros','facts','references','referencias','referencias_origen']);
      s.facts=s.facts.filter(f=>f.capitulo!==before.capitulo);s.seguimiento.preguntas=s.seguimiento.preguntas.filter(q=>q.capitulo!==before.capitulo);
    }
    if(kind==='registro')replaceReferences(s,before.id,null,['registros','facts','references','referencias','referencias_origen']);
    if(kind==='entidad')replaceReferences(s,before.name,null,['entidades']);
    const rows=collection(s,kind);rows.splice(rows.indexOf(before),1);
  }
  const blank=value=>Array.isArray(value)?[]:value&&typeof value==='object'?Object.fromEntries(Object.entries(value).map(([k,v])=>[k,blank(v)])):typeof value==='number'?0:typeof value==='boolean'?false:'';
  function newEntry(s,kind){
    if(kind==='capitulo')return {capitulo:Math.max(0,...s.chapters.map(c=>c.capitulo))+1,id:'nuevo-'+Date.now(),titulo:'Nueva sesión',url:'',resumen:'',estado:'pendiente',registros:[],misiones:[],preguntas:[],contradicciones:[],nombres:[],duracion:'',seguimiento:[],history:null,_source:null};
    if(kind==='entidad')return {name:'Nueva ficha '+Date.now(),facts:[],aliases:[],note:'',type:'personaje',description:'',references:[],history:null};
    if(kind==='registro')return {id:'nuevo-'+Date.now(),titulo:'Nuevo acontecimiento',tipo:'hecho_confirmado',afirmacion:'',inicio:'00:00:00',fin:'00:00:00',cita:'',entidades:[],ambito:'',confianza:'',capitulo:s.chapters[0]?.capitulo||1,etiquetas_originales:[]};
    if(kind==='pregunta')return {id:'pregunta-'+Date.now(),capitulo:s.chapters[0]?.capitulo||1,indice:0,pregunta:'Nuevo misterio',estado:'pendiente',respuesta:'',referencias:[],pendiente:'',revisado_hasta:0,referencias_origen:[],requiere_actualizacion:false};
    return {title:'Nuevo documento',text:''};
  }


  function start(kind,identity,trigger,isNew=false){
    if(active)return;
    if(!loaded){status.textContent='No se ha podido cargar la campaña guardada. Espera a que se sincronice o recarga la página antes de editar.';return;}
    ++syncGeneration;
    const draft=snapshot(),before=isNew?null:clone(find(draft,kind,identity));
    let item=isNew?newEntry(draft,kind):clone(before),deleted=false,busy=false;
    if(!item)return;
    const card=trigger?.closest('.editor-card-shell');
    let host=card||trigger?.closest('.event-body')||content;
    if(isNew){host=document.createElement('section');host.className='editor-new-entry document';content.prepend(host);}
    const template=host.cloneNode(true),startRevision=revision;
    host.classList.add('editor-session');
    if(card)card.classList.add('editor-card-expanded');
    let controls=[],operations=[],pickers=[],area,form,message,selected=[];
    const get=(o,p)=>p.reduce((v,k)=>v[k],o);
    const set=(o,p,v)=>{if(!p.length)item=v;else get(o,p.slice(0,-1))[p.at(-1)]=v;};
    function read(){for(const {node,path,type}of controls)set(item,path,type==='boolean'?node.checked:type==='number'?Number(node.value):node.value);}
    const session={host,message:null};active=session;
    content.querySelectorAll('.editor-inline').forEach(n=>n.disabled=true);
    const disabled=[document.getElementById('global-search'),document.getElementById('campaign-selector')].filter(Boolean);
    disabled.forEach(n=>n.disabled=true);
    function finish(){active=null;disabled.forEach(n=>n.disabled=false);host.classList.remove('editor-session','editor-card-expanded');refresh();}
        function referenceList(value,path,title){
      const entities=path.at(-1)==='entidades';
      const choices=entities?draft.entities.map(e=>[e.name,e.name]):draft.facts.map(f=>[f.id,`Sesión ${f.capitulo} · ${f.titulo} · ${f.inicio}`]);
      const titles=new Map(choices),index=pickers.push({choices,path})-1;
      const rows=value.map((id,i)=>{const del=operations.push(()=>get(item,path).splice(i,1))-1;const up=operations.push(()=>{const a=get(item,path);[a[i-1],a[i]]=[a[i],a[i-1]];})-1;const down=operations.push(()=>{const a=get(item,path);[a[i+1],a[i]]=[a[i],a[i+1]];})-1;return `<li><span>${escape(titles.get(id)||id)}</span><div class="editor-actions"><button type="button" data-op="${del}" aria-label="Quitar ${escape(titles.get(id)||id)}">Quitar</button>${i?`<button type="button" data-op="${up}" aria-label="Subir ${escape(titles.get(id)||id)}">Subir</button>`:''}${i<value.length-1?`<button type="button" data-op="${down}" aria-label="Bajar ${escape(titles.get(id)||id)}">Bajar</button>`:''}</div></li>`;}).join('');
      return `<fieldset class="editor-reference-list"><legend>${escape(title)}</legend><ul>${rows||'<li>No se han añadido referencias.</li>'}</ul><label>Buscar ${entities?'una entidad':'un acontecimiento'}<input type="search" data-picker-search="${index}" placeholder="${entities?'Nombre de la entidad':'Título o número de sesión'}"></label><label>${entities?'Entidad':'Acontecimiento'}<select data-picker-select="${index}"></select></label><button type="button" class="secondary-button" data-picker-add="${index}">Añadir selección</button><p data-picker-status="${index}" role="status" aria-live="polite"></p></fieldset>`;
    }
    function choicesFor(value,path){
      if(path[0]==='informacion_adicional')return null;
      const key=path.at(-1);
      if(key==='type')return ['personaje','lugar','faccion','objeto'].map(v=>[v,choiceLabels[v]]);
      if(key==='tipo')return ['hecho_confirmado','declaracion_personaje','explicacion_director','especulacion_jugadores','desconocido'].map(v=>[v,choiceLabels[v]]);
      if(key==='estado')return ((kind==='pregunta'||typeof get(item,path.slice(0,-1)).pregunta==='string')?['resuelta','parcial','pendiente','sin_revisar']:['revisado','pendiente']).map(v=>[v,choiceLabels[v]]);
      if(key==='confianza')return ['alta','media','baja'].map(v=>[v,choiceLabels[v]]);
      if(key==='revisado_hasta'||(key==='capitulo'&&!(kind==='capitulo'&&path.length===1)))return [[0,'Sin sesión indicada'],...draft.chapters.map(c=>[c.capitulo,`Sesión ${c.capitulo} · ${c.titulo}`])];
      return null;
    }
    function tree(value,path,title){
      if(path.at(-1)==='_source')return `<p>${escape(title)} · ${escape(value??'Sin transcripción')}</p>`;
      if(value===null){const i=operations.push(()=>set(item,path,path.at(-1)==='history'?{revisado_hasta:0,etapas:[]}:''))-1;return `<p>${escape(title)} <button type="button" data-op="${i}">Añadir</button></p>`;}
      if(Array.isArray(value)){
        if(path[0]!=='informacion_adicional'&&['facts','references','referencias','referencias_origen','registros','entidades'].includes(path.at(-1))&&value.every(v=>typeof v==='string')&&!(kind==='archivo'&&path.length===1))return referenceList(value,path,title);
        const rows=value.map((v,i)=>{const del=operations.push(()=>get(item,path).splice(i,1))-1;const up=operations.push(()=>{const a=get(item,path);[a[i-1],a[i]]=[a[i],a[i-1]];})-1;const down=operations.push(()=>{const a=get(item,path);[a[i+1],a[i]]=[a[i],a[i+1]];})-1;return `<fieldset class="editor-list-item"><legend>${path.at(-1)==='etapas'?'Etapa':escape(title)} ${i+1}</legend>${tree(v,[...path,i],typeof v==='object'?'Información':'Texto')}<div class="editor-actions"><button type="button" data-op="${del}">Quitar</button>${i?`<button type="button" data-op="${up}">Subir</button>`:''}${i<value.length-1?`<button type="button" data-op="${down}">Bajar</button>`:''}</div></fieldset>`;}).join('');
        const add=operations.push(()=>{const a=get(item,path);a.push(blank(a[0]??(path.at(-1)==='etapas'?{titulo:'',texto:'',referencias:[]}:'')));})-1;
        return `<fieldset><legend>${escape(title)}</legend>${rows}<button class="secondary-button" type="button" data-op="${add}">${path.at(-1)==='etapas'?'Añadir etapa':'Añadir elemento'}</button></fieldset>`;
      }
      if(typeof value==='object'){
        const custom=path[0]==='informacion_adicional';
        const body=Object.entries(value).map(([k,v])=>{
          const field=tree(v,[...path,k],label(k));if(!custom)return field;
          const del=operations.push(()=>{delete get(item,path)[k];})-1;
          const rename=operations.push(()=>{const name=area.querySelector(`[data-rename="${rename}"]`).value.trim(),obj=get(item,path);if(!name||['__proto__','constructor','prototype'].includes(name)||(name!==k&&Object.hasOwn(obj,name))){message.textContent='Elige un nombre distinto para el campo.';return;}if(name!==k){obj[name]=obj[k];delete obj[k];}})-1;
          return `<div class="editor-custom-field">${field}<details><summary>Opciones del campo</summary><label>Nombre del campo<input data-rename="${rename}" value="${escape(k)}" maxlength="80"></label><button type="button" data-op="${rename}">Cambiar nombre</button><button type="button" data-op="${del}">Quitar campo</button></details></div>`;
        }).join('');
        const add=custom?operations.push(()=>{const box=area.querySelector(`[data-group-name="${add}"]`),name=box.value.trim(),obj=get(item,path);if(!name||['__proto__','constructor','prototype'].includes(name)||Object.hasOwn(obj,name)){message.textContent='Escribe un nombre nuevo para el campo.';return;}obj[name]=newValue(area.querySelector(`[data-group-type="${add}"]`).value);})-1:null;
        return `<fieldset><legend>${escape(title)}</legend>${body}${custom?`<label>Nombre del nuevo campo<input data-group-name="${add}" maxlength="80" placeholder="Por ejemplo: Rasgos"></label><label>Contenido<select data-group-type="${add}"><option value="text">Texto</option><option value="list">Lista</option><option value="group">Grupo de campos</option><option value="number">Número</option><option value="boolean">Sí o no</option></select></label><button type="button" class="secondary-button" data-op="${add}">Añadir campo</button>`:''}</fieldset>`;
      }
      const index=controls.push({path,type:typeof value})-1;
      const choices=choicesFor(value,path),hint=hints[path.at(-1)],name=path.length===selected.length?'name="value"':'';
      let input;
      if(choices){if(!choices.some(([v])=>String(v)===String(value)))choices.unshift([value,choiceLabels[value]||String(value)||'Sin indicar']);input=`<select ${name} data-control="${index}">${choices.map(([v,text])=>`<option value="${escape(v)}" ${String(v)===String(value)?'selected':''}>${escape(text)}</option>`).join('')}</select>`;}
      else if(typeof value==='boolean')input=`<input type="checkbox" ${name} data-control="${index}" ${value?'checked':''}>`;
      else if(typeof value==='number')input=`<input type="number" ${name} step="any" data-control="${index}" value="${value}">`;
      else if(['id','url','inicio','fin','duracion'].includes(path.at(-1)))input=`<input ${name} type="${path.at(-1)==='url'?'url':'text'}" data-control="${index}" value="${escape(value)}" ${['inicio','fin','duracion'].includes(path.at(-1))?'placeholder="00:12:34"':''}>`;
      else input=`<textarea ${name} data-control="${index}" rows="${String(value).length>140?8:2}">${escape(value)}</textarea>`;
      return `<label><span class="editor-field-label">${escape(title)}</span>${input}${hint?`<small class="editor-help">${escape(hint)}</small>`:''}</label>`;
    }


    function renderFields(){
      const scroll=window.scrollY;controls=[];operations=[];pickers=[];
      host.replaceChildren();form=document.createElement('form');form.className='editor-inline-form';host.append(form);area=form;
      const toolbar=document.createElement('div');toolbar.className='editor-actions editor-inline-toolbar';toolbar.innerHTML='<button class="primary-button" type="submit">Guardar cambios</button><button class="secondary-button" type="button" data-cancel>Cancelar</button>';toolbar.querySelector('[data-cancel]').onclick=finish;form.append(toolbar);
      const view=document.createElement('div');view.className='editor-inline-content';view.innerHTML=template.innerHTML;
      view.querySelectorAll('[data-edit-kind],.editor-additional').forEach(n=>n.remove());
      view.querySelectorAll('button').forEach(n=>n.type='button');
      // Una tarjeta en edición deja de ser un enlace; los campos ocupan su lugar.
      view.querySelectorAll('a.entity-card,a.chapter-card').forEach(link=>{const article=document.createElement('article');article.className=link.className;article.innerHTML=link.innerHTML;link.replaceWith(article);});
      form.append(view);
      const used=new Set(),mounts=[];
      function field(target,path,style=''){
        if(!target)return false;
        if(get(item,path)&&typeof get(item,path)==='object'&&['P','SPAN'].includes(target.tagName)){const block=document.createElement('div');block.className=target.className;target.replaceWith(block);target=block;}
        target.replaceChildren();target.classList.add('editor-field-slot');if(style)target.classList.add(style);
        target.innerHTML=tree(get(item,path),path,label(path.at(-1)));used.add(path[0]);mounts.push(target);return true;
      }
      function insert(path,after,title){const section=document.createElement('section');section.className='editor-inline-section';section.innerHTML=tree(get(item,path),path,title||label(path.at(-1)));if(after)after.after(section);else view.append(section);used.add(path[0]);return section;}
      function narrative(){
        const old=view.querySelector('.narrative-story');
        if(!item.history){if(old)old.remove();return;}
        used.add('history');const story=document.createElement('section');story.className='character-story narrative-story editor-story';
        const emblem=old?.querySelector('.story-emblem')?.outerHTML||'';
        story.innerHTML=`<header class="story-heading">${emblem}<div><h2>${kind==='capitulo'?'Relato de la sesión':'Historia'}</h2>${tree(item.history.revisado_hasta,['history','revisado_hasta'],'Revisado hasta')}</div></header><div class="story-stages">${item.history.etapas.map((stage,i)=>{
          const remove=operations.push(()=>item.history.etapas.splice(i,1))-1;
          const up=operations.push(()=>{const a=item.history.etapas;[a[i-1],a[i]]=[a[i],a[i-1]];})-1;
          const down=operations.push(()=>{const a=item.history.etapas;[a[i+1],a[i]]=[a[i],a[i+1]];})-1;
          return `<article class="story-stage"><div class="story-step">${String(i+1).padStart(2,'0')}</div><div class="story-prose"><h3 class="editor-field-slot">${tree(stage.titulo,['history','etapas',i,'titulo'],'Título de la etapa')}</h3><div class="editor-story-text">${tree(stage.texto,['history','etapas',i,'texto'],'Relato')}</div><div class="story-sources">${tree(stage.referencias,['history','etapas',i,'referencias'],'Fuentes de esta etapa')}</div>${Object.keys(stage).filter(k=>!['titulo','texto','referencias'].includes(k)).map(k=>tree(stage[k],['history','etapas',i,k],label(k))).join('')}<div class="editor-actions">${i?`<button type="button" data-op="${up}">Subir</button>`:''}${i<item.history.etapas.length-1?`<button type="button" data-op="${down}">Bajar</button>`:''}<button type="button" data-op="${remove}">Quitar etapa</button></div></div></article>`;
        }).join('')}</div>`;
        const add=operations.push(()=>item.history.etapas.push({titulo:'',texto:'',referencias:[]}))-1;
        story.insertAdjacentHTML('beforeend',`<button type="button" class="secondary-button" data-op="${add}">Añadir etapa</button>${Object.keys(item.history).filter(k=>!['etapas','revisado_hasta'].includes(k)).map(k=>tree(item.history[k],['history',k],label(k))).join('')}`);
        if(old)old.replaceWith(story);else (view.querySelector('.card-copy,.entity-intro,.chapter-summary')||view.lastElementChild)?.after(story);
        if(!story.isConnected)view.append(story);
      }
      if(kind==='entidad'){
        field(view.querySelector('.card-title,.section-head h1'),['name'],'editor-name-control');
        field(view.querySelector('.card-tag,.section-head .eyebrow'),['type']);
        item.description??='';const description=view.querySelector('.card-copy,.entity-intro,.chapter-summary');
        if(!field(description,['description']))insert(['description'],view.querySelector('.section-head'));
        narrative();
        if(item.references!==undefined)field(view.querySelector('.entity-identification .document > p:nth-child(2)'),['references']);
        if(item.note!==undefined)field(view.querySelector('.entity-identification .document > p'),['note']);
      }else if(kind==='capitulo'){
        field(view.querySelector('.card-title,.section-head h1'),['titulo'],'editor-name-control');
        field(view.querySelector('.card-copy,.chapter-summary'),['resumen']);narrative();
      }else if(kind==='registro'){
        field(view.querySelector('h3'),['titulo'],'editor-name-control');field(view.querySelector(':scope > p'),['afirmacion']);
        field(view.querySelector('.quote'),['cita']);
      }else if(kind==='pregunta'){
        field(view.querySelector('h3'),['pregunta'],'editor-name-control');field(view.querySelector(':scope > p'),['respuesta']);
        field(view.querySelector('.badge'),['estado']);
      }else if(kind==='documento'){
        view.replaceChildren();for(const k of ['title','text'])insert([k]);
      }
      const rest=document.createElement('section');rest.className='editor-inline-section editor-other-fields';
      // Todos los datos restantes se muestran juntos, sin elegir un campo primero.
      const remaining=Object.keys(item).filter(k=>!used.has(k)&&k!=='_source');
      if(remaining.length){rest.innerHTML='<h3>Datos de la ficha</h3>'+remaining.map(k=>tree(item[k],[k],label(k))).join('');view.append(rest);}
      const options=document.createElement('details');options.className='editor-add-information';options.innerHTML='<summary>Añadir información</summary><label>Qué quieres añadir<select name="optional"></select></label><div data-custom-field><label>Nombre<input name="newLabel" maxlength="80" placeholder="Por ejemplo: Apariencia"></label><label>Contenido<select name="newType"><option value="text">Texto</option><option value="list">Lista</option><option value="group">Grupo de campos</option><option value="number">Número</option><option value="boolean">Sí o no</option></select></label></div><button class="secondary-button" type="button" data-add-field>Añadir campo</button><p role="status" data-add-status></p>';
      form.append(options);
      const samples={};for(const row of (kind==='archivo'?[]:kind==='documento'?Object.values(original.documents):collection(original,kind)))for(const [k,v]of Object.entries(row))if(v!==null&&k!=='_source')samples[k]=v;
      const missing=Object.keys(samples).filter(k=>!(k in item));
      form.elements.optional.innerHTML=missing.map(k=>`<option value="${escape(k)}">${escape(label(k))}</option>`).join('')+'<option value="__custom">Otro campo</option>';
      form.elements.optional.onchange=()=>options.querySelector('[data-custom-field]').hidden=form.elements.optional.value!=='__custom';form.elements.optional.onchange();
      options.querySelector('[data-add-field]').onclick=()=>{
        read();rememberedName=form.elements.author.value;const reason=form.elements.reason.value,k=form.elements.optional.value;
        if(k==='__custom'){const name=form.elements.newLabel.value.trim();if(!name||['__proto__','constructor','prototype'].includes(name)){options.querySelector('[data-add-status]').textContent='Escribe el nombre de la información que quieres añadir.';return;}item.informacion_adicional??={};if(Object.hasOwn(item.informacion_adicional,name)){options.querySelector('[data-add-status]').textContent='Ya existe un campo con ese nombre.';return;}item.informacion_adicional[name]=newValue(form.elements.newType.value);}
        else item[k]=blank(samples[k]);renderFields();form.elements.reason.value=reason;
      };
      const metadata=document.createElement('section');metadata.className='editor-save-section';metadata.innerHTML=`<label>Tu nombre<input name="author" required maxlength="100" value="${escape(rememberedName)}" autocomplete="nickname"></label><label>Motivo de la corrección<textarea name="reason" required maxlength="1000" rows="2"></textarea></label><p role="status" aria-live="polite" data-save-status></p><div class="editor-actions editor-save-actions"><button class="primary-button" type="submit">Guardar cambios</button><button class="secondary-button" type="button" data-cancel>Cancelar</button>${kind!=='archivo'&&!isNew?'<button class="secondary-button" type="button" data-delete>Eliminar entrada</button>':''}</div>`;
      form.append(metadata);message=metadata.querySelector('[data-save-status]');session.message=message;
      metadata.querySelector('[data-cancel]').onclick=finish;
      function updateDeleteState(){
        form.querySelectorAll('[type=submit]').forEach(button=>button.textContent=deleted?'Guardar eliminación':'Guardar cambios');
        const button=metadata.querySelector('[data-delete]');if(button)button.textContent=deleted?'Deshacer eliminación':'Eliminar entrada';
        message.textContent=deleted?'La entrada está marcada para eliminar. Solo se eliminará al guardar; Cancelar conserva la entrada.':'';
      }
      metadata.querySelector('[data-delete]')?.addEventListener('click',event=>{
        read();if(deleted){deleted=false;updateDeleteState();lettering();return;}
        const trigger=event.currentTarget,warning=document.createElement('dialog');warning.className='editor-delete-dialog';
        warning.setAttribute('aria-labelledby','editor-delete-title');warning.setAttribute('aria-describedby','editor-delete-description');
        const name=item.name||item.titulo||item.title||item.pregunta||identity;
        warning.innerHTML=`<h2 id="editor-delete-title">¿Eliminar esta entrada?</h2><p id="editor-delete-description">Vas a eliminar «${escape(name)}». ${kind==='capitulo'?'También se eliminarán sus acontecimientos y misterios, y se retirarán sus referencias.':'Se retirará de la campaña y se actualizarán sus referencias.'}</p><p>La eliminación se aplicará cuando pulses «Guardar eliminación». La transcripción y los archivos originales se conservan.</p><div class="editor-actions"><button type="button" class="secondary-button" data-delete-cancel autofocus>Cancelar</button><button type="button" class="primary-button" data-delete-confirm>Eliminar entrada</button></div>`;
        document.body.append(warning);
        warning.querySelector('[data-delete-cancel]').onclick=()=>warning.close();
        warning.querySelector('[data-delete-confirm]').onclick=()=>{deleted=true;updateDeleteState();lettering();warning.close();};
        warning.addEventListener('close',()=>{warning.remove();if(trigger.isConnected)trigger.focus();},{once:true});
        warning.showModal();lettering();
      });
      const history=document.createElement('details');history.innerHTML='<summary>Historial de la entrada</summary>';
      const candidates=[{content:original,author:'Archivo original',reason:'Versión de partida'},...versions];
      candidates.forEach((v,i)=>{const button=document.createElement('button');button.type='button';button.className='secondary-button';button.dataset.version=String(i);button.textContent='Usar versión de '+v.author;button.onclick=async()=>{try{const saved=v.content||(await request('/document/'+campaignId+'?revision='+v.revision)).content;const prior=find(saved,kind,identity);if(!prior){message.textContent='La entrada no existía en esta versión.';return;}item=clone(prior);deleted=false;renderFields();form.elements.reason.value='Restaurar versión: '+v.author;}catch(error){message.textContent=error.message;}};history.append(button);});form.append(history);
      const create=document.createElement('details');create.innerHTML='<summary>Crear otra entrada</summary><button type="button" class="secondary-button" data-new>Nueva entrada</button>';create.querySelector('button').onclick=()=>{finish();start(kind,kind==='documento'?'documento-'+Date.now():'nuevo',null,true);};form.append(create);
      bind();updateDeleteState();lettering();window.scrollTo(0,scroll);
    }
    const newValue=type=>({text:'',list:[],group:{},number:0,boolean:false})[type];
    function bind(){
      area.querySelectorAll('[data-control]').forEach(node=>{const control=controls[Number(node.dataset.control)];control.node=node;node.dataset.fieldPath=JSON.stringify(control.path);if(node.tagName==='TEXTAREA'){const resize=()=>{node.style.height='auto';node.style.height=Math.max(55,node.scrollHeight+4)+'px';};node.addEventListener('input',resize);resize();}});
      area.querySelectorAll('[data-op]').forEach(button=>{button.classList.add('secondary-button');button.onclick=()=>{read();rememberedName=form.elements.author.value;const reason=form.elements.reason.value;operations[Number(button.dataset.op)]();renderFields();form.elements.reason.value=reason;};});
      pickers.forEach((picker,i)=>{
        const search=area.querySelector(`[data-picker-search="${i}"]`),select=area.querySelector(`[data-picker-select="${i}"]`),add=area.querySelector(`[data-picker-add="${i}"]`),info=area.querySelector(`[data-picker-status="${i}"]`);
        const fold=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
        const filter=()=>{const chosen=get(item,picker.path),terms=fold(search.value).split(/\s+/).filter(Boolean),rows=picker.choices.filter(([id,text])=>!chosen.includes(id)&&terms.every(t=>fold(text).includes(t)));select.innerHTML=rows.map(([id,text])=>`<option value="${escape(id)}">${escape(text)}</option>`).join('');select.disabled=add.disabled=!rows.length;info.textContent=rows.length?`${rows.length} opciones disponibles`:'No hay coincidencias.';};
        search.oninput=filter;filter();add.onclick=()=>{read();if(select.value){get(item,picker.path).push(select.value);rememberedName=form.elements.author.value;const reason=form.elements.reason.value;renderFields();form.elements.reason.value=reason;}};
      });
      form.onsubmit=async event=>{
        event.preventDefault();if(busy)return;read();busy=true;
        const locked=[...form.querySelectorAll('input,textarea,select,button')].map(node=>[node,node.disabled]);locked.forEach(([node])=>node.disabled=true);
        try{
          let updated=draft,nextIdentity=identity;
          if(deleted)remove(updated,kind,identity);else if(kind==='archivo')updated=item;else if(kind==='documento')updated.documents[identity]=item;
          else{const rows=collection(updated,kind);if(isNew)rows.push(item);else{rows[rows.indexOf(find(updated,kind,identity))]=item;reconcile(updated,kind,before,item);}nextIdentity=String(item[groups[kind][1]]);}
          await request('/save-document',{campaign:campaignId,content:updated,revision:startRevision,author:form.elements.author.value,reason:form.elements.reason.value});
          rememberedName=form.elements.author.value;active=null;disabled.forEach(n=>n.disabled=false);
          if(!card||deleted||isNew)window.history.replaceState(null,'',deleted?'#'+({capitulo:'capitulos',entidad:'personajes',registro:'cronologia',pregunta:'misterios',documento:'inicio'}[kind]):'#'+(kind==='documento'?(['atlas','facciones'].includes(nextIdentity)?'documento/':'')+nextIdentity:kind+'/'+encodeURIComponent(nextIdentity)));
          const synced=await sync();host.classList.remove('editor-session','editor-card-expanded');refresh();status.textContent=synced?'Cambios guardados para todos.':'Cambios guardados. No se ha podido actualizar la vista; recarga la página.';
        }catch(error){message.textContent=error.message;}finally{busy=false;locked.forEach(([node,wasDisabled])=>node.disabled=wasDisabled);}
      };
    }
    renderFields();form.querySelector('[data-control]')?.focus({preventScroll:true});
  }

    function decorate([route,identity]){
    const documentKey=route==='documento'?identity:route;
    function additional(parent,obj){
      if(!parent||!obj?.informacion_adicional||parent.querySelector(':scope > .editor-additional'))return;
      function valueNode(value){
        if(Array.isArray(value)){const ul=document.createElement('ul');for(const child of value){const li=document.createElement('li');li.append(valueNode(child));ul.append(li);}if(!value.length)ul.textContent='Sin entradas';return ul;}
        if(value&&typeof value==='object'){const dl=document.createElement('dl');for(const [name,child]of Object.entries(value)){const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=name;dd.append(valueNode(child));dl.append(dt,dd);}return dl;}
        const text=document.createElement('span');text.textContent=typeof value==='boolean'?(value?'Sí':'No'):String(value??'Sin indicar');return text;
      }
      const section=document.createElement('section');section.className='editor-additional document';const title=document.createElement('h3');title.textContent='Información adicional';section.append(title,valueNode(obj.informacion_adicional));parent.append(section);
    }
    content.querySelectorAll('.event[id^="fact-"]').forEach(article=>additional(article.querySelector('.event-body'),data.facts.find(f=>f.id===article.id.slice(5))));
    content.querySelectorAll('.question-card[data-question]').forEach(article=>additional(article.querySelector('.event-body'),data.seguimiento.preguntas.find(q=>q.id===article.dataset.question)));
    if(route==='entidad')additional(content,data.entities.find(e=>e.name===identity||e.aliases.includes(identity)));
    else if(route==='capitulo')additional(content,data.chapters.find(c=>String(c.capitulo)===identity));
    else if(data.documents[documentKey])additional(content.querySelector('.document'),data.documents[documentKey]);
    if(!token||!loaded)return;
    function button(kind,id,name){
      const node=document.createElement('button');node.className='secondary-button editor-inline';node.type='button';node.textContent='Editar';
      node.dataset.editKind=kind;node.dataset.editIdentity=id;node.setAttribute('aria-label','Editar '+name);
      node.onclick=async event=>{event.preventDefault();event.stopPropagation();if(token)start(kind,id,node);};
      return node;
    }
    function beside(heading,kind,id,name){
      if(!heading||heading.parentElement.querySelector(':scope > .editor-inline'))return;
      const row=document.createElement('div');row.className='editor-title-row';heading.before(row);row.append(heading,button(kind,id,name));
    }
    // El botón es hermano del enlace: editar una tarjeta no navega ni anida controles.
    content.querySelectorAll('a.entity-card,a.chapter-card').forEach(card=>{
      const kind=card.classList.contains('entity-card')?'entidad':'capitulo';
      const id=decodeURIComponent(card.hash.split('/').slice(1).join('/'));
      const shell=document.createElement('div');shell.className='editor-card-shell';card.before(shell);shell.append(card,button(kind,id,card.querySelector('.card-title')?.textContent||id));
    });
    content.querySelectorAll('.event[id^="fact-"]').forEach(article=>{
      const id=article.id.slice(5);beside(article.querySelector('.event-body > h3'),'registro',id,article.querySelector('h3')?.textContent||id);
    });
    content.querySelectorAll('.question-card[data-question]').forEach(article=>{
      const id=article.dataset.question;beside(article.querySelector('.event-body > h3'),'pregunta',id,id);
    });
    if(route==='entidad'){
      const entity=data.entities.find(e=>e.name===identity||e.aliases.includes(identity));
      if(entity)beside(content.querySelector('.section-head h1'),'entidad',entity.name,entity.name);
    }else if(route==='capitulo')beside(content.querySelector('.section-head h1'),'capitulo',identity,'capítulo '+identity);
    else if(data.documents[documentKey])beside(content.querySelector('.document h1'),'documento',documentKey,data.documents[documentKey].title);
  }

  sync();setInterval(()=>{if(!active&&!document.hidden)sync();},30000);
  return {decorate,isEditing:()=>Boolean(active)};
};
