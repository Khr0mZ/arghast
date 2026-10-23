(() => {
  'use strict';
  const archive = JSON.parse(document.getElementById('xoltacan-data').textContent);
  const campaignMetadata=archive.campaignMetadata||{xoltacan:{id:'xoltacan',name:'Xoltacan',tagline:'Entre la selva y el mar'}};
  const requestedCampaign=new URLSearchParams(location.search).get('campana')||(location.pathname.endsWith('/kuroto.html')?'kuroto':null);
  const campaignId=Object.hasOwn(campaignMetadata,requestedCampaign)?requestedCampaign:'xoltacan';
  const campaign=campaignMetadata[campaignId];
  const data = campaignId==='xoltacan'?archive:archive.campaigns[campaignId];
  let reviewedCount=data.chapters.filter(chapter=>chapter.estado==='revisado').length;
  const content = document.getElementById('content');
  const searchInput = document.getElementById('global-search');
  const facts = new Map(data.facts.map(f => [f.id, f]));
  const questions = new Map((data.seguimiento?.preguntas || []).map(q=>[q.id,q]));
  const questionStates = {resuelta:'Resuelta',parcial:'Parcialmente resuelta',pendiente:'Pendiente',sin_revisar:'Sin revisar'};
  const chapters = new Map(data.chapters.map(c => [c.capitulo, c]));
  const entities = new Map(data.entities.map(e => [e.name, e]));
  const entityAliases = new Map(data.entities.flatMap(e=>e.aliases.map(label=>[label,e])));
  const sections={inicio:'Portada',capitulos:'Crónicas',cronologia:'Acontecimientos',personajes:'Personajes',atlas:'Lugares',facciones:'Facciones',objetos:'Vestigios',misiones:'Misiones',misterios:'Misterios y desenlaces',relaciones:'Relaciones',nombres:'Nombres y equivalencias'};
  const campaignLettering = /* ROTULOS_XOLTACAN */{};
  function applyCampaignLettering() {
    if(campaignId!=='xoltacan'||document.body.dataset.view!=='campaign') {
      document.querySelectorAll('.campaign-lettering').forEach(span=>span.replaceWith(document.createTextNode(span.textContent)));
      return;
    }
    const selectors='.nav-links a,.nav-label,.campaign-picker label,.campaign-picker>a,#campaign-context,#page-title,.primary-button,.secondary-button,.expedition-link strong,.detail-tabs a,.detail-tabs button,.section-head h1,.section-head h2,.section-head>a,.footer a,.story-heading h2,.context-details>summary,.filters label,.chapter-nav a,.document h1,.document-section>h2,.role-block-title,.chronicle-views a,.reading-jump h2,.reading-jump label,.section-navigation button,.section-navigation>span,.reading-context>h3,.role-audio-transcript>h3';
    document.querySelectorAll(selectors).forEach(element=>{
      for(const node of [...element.childNodes]) {
        if(node.nodeType!==Node.TEXT_NODE)continue;
        const text=node.textContent.trim();
        const label=text.replace(/^[←↗→]\s*|\s*[←↗→]$/g,'');
        const variant=element.closest('.nav-links')&&label==='Misterios y desenlaces'?label+'|sidebar':label;
        const key=Object.hasOwn(campaignLettering,variant)?campaignLettering[variant]:null;
        if(!key)continue;
        const span=document.createElement('span');
        span.className='campaign-lettering';span.dataset.lettering=key;span.textContent=label;
        const leading=node.textContent.slice(0,node.textContent.indexOf(label));
        const trailing=node.textContent.slice(node.textContent.indexOf(label)+label.length);
        node.replaceWith(document.createTextNode(leading),span,document.createTextNode(trailing));
      }
    });
  }
  document.querySelectorAll('#sidebar .nav-links a').forEach(link=>{
    const label=sections[link.hash.slice(1)];
    if(label)link.replaceChildren(link.querySelector('.nav-symbol'),document.createTextNode(label));
  });
  const categories = {
    personaje:{route:'personajes',title:sections.personajes,copy:'Protagonistas, habitantes y criaturas, con sus apariciones y evolución.',search:'Buscar un personaje'},
    lugar:{route:'atlas',title:sections.atlas,copy:'Ciudades, regiones, ruinas y establecimientos documentados.',search:'Buscar un lugar',document:'atlas',overview:'Contexto geográfico y rutas'},
    faccion:{route:'facciones',title:sections.facciones,copy:'Organizaciones, tribus y autoridades, con sus intereses y conflictos.',search:'Buscar una facción',document:'facciones',overview:'Contexto político y conflictos'},
    objeto:{route:'objetos',title:sections.objetos,copy:'Armas, artefactos, embarcaciones y otros objetos con historia.',search:'Buscar un vestigio'}
  };
  const labels = {hecho_confirmado:'Acción confirmada',declaracion_personaje:'Declaración',explicacion_director:'Dirección',especulacion_jugadores:'Teoría',desconocido:'Sin confirmar'};
  const classes = {hecho_confirmado:'confirmed',declaracion_personaje:'statement',explicacion_director:'director',especulacion_jugadores:'speculation',desconocido:'speculation'};
  const icons = {arrow:'↗', book:'◈', search:'⌕'};
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const fold = value => String(value ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  const secs = time => { const [h,m,s]=String(time).split(':').map(Number); return h*3600+m*60+s; };
  const clock = time => String(time).split('.')[0];
  const chapterName = n => `Capítulo ${String(n).padStart(2,'0')}`;
  const routeEntity = name => '#entidad/'+encodeURIComponent(name);
  const sourceURL = f => chapters.get(f.capitulo).url+'&t='+Math.floor(secs(f.evidencia_cue?.inicio || f.inicio))+'s';
  const badge = f => `<span class="badge ${classes[f.tipo] || ''}">${esc(labels[f.tipo] || f.tipo)}</span>`;
  const chip = name => entities.has(name)?`<a class="entity-chip" href="${routeEntity(name)}">${esc(name)}</a>`:'';
  const short = (text,size=165) => text.length>size ? text.slice(0,size).replace(/\s\S*$/,'')+'…' : text;
  let state={page:1,chapter:'',kind:'',searchType:'',chapterQuery:'',entityQuery:'',questionQuery:'',questionStatus:'',roleQuery:'',tab:'relato',transcriptQuery:'',transcriptLimit:120};
  let searchTimer;
  const transcriptLoads=new Map();
  const transcriptErrors=new Set();
  function loadTranscript(n) {
    const number=String(n),file=data.transcriptFiles?.[number];
    if(!file || data.transcripts[number]?.length || transcriptLoads.has(number) || transcriptErrors.has(number))return;
    const script=document.createElement('script');
    transcriptLoads.set(number,script);
    script.src=new URL(file,location.href).href;
    const finish=ok=>{
      const sourceNumber=chapters.get(n)?._source??number;
      const rows=globalThis.arghastTranscripts?.[campaignId+'/'+sourceNumber];
      if(ok&&Array.isArray(rows)&&rows.length)data.transcripts[number]=rows;
      else transcriptErrors.add(number);
      transcriptLoads.delete(number);script.remove();
      const [route,arg]=current();
      if((route==='capitulo'&&Number(arg)===n)||(route==='registro'&&facts.get(arg)?.capitulo===n))render();
    };
    script.onload=()=>finish(true);script.onerror=()=>finish(false);
    document.head.append(script);
  }
  function transcriptLoading(n) {
    loadTranscript(n);
    return transcriptErrors.has(String(n))?`<div class="empty"><h2>No se pudo abrir la transcripción</h2><p>Comprueba la conexión o que la carpeta transcripciones acompañe al HTML.</p><button class="secondary-button" data-transcript-retry="${n}">Volver a intentar</button></div>`:'<p class="notice" role="status">Abriendo la transcripción de esta sesión…</p>';
  }
  const searchIndex = data.facts.map(f => ({fact:f,text:fold([f.titulo,f.afirmacion,f.cita,f.ambito,f.limitacion,...(f.etiquetas_originales||[]),...f.entidades,...f.entidades.flatMap(name=>entities.get(name)?.aliases || [])].join(' '))}));
  const matched = (query,chapter='',kind='') => { const terms=fold(query).trim().split(/\s+/).filter(Boolean); return searchIndex.filter(item=>(!chapter || item.fact.capitulo===Number(chapter))&&(!kind || item.fact.tipo===kind)&&terms.every(term=>item.text.includes(term))).map(item=>item.fact); };
  const searchTypes={registro:'Acontecimientos',capitulo:'Crónicas',personaje:'Personajes',lugar:'Lugares',faccion:'Facciones',objeto:'Vestigios',rol:'Rol escrito',pregunta:'Misterios y desenlaces',documento:'Misiones, relaciones y otros documentos'};
  let campaignSearchIndex;
  function roleSearchText(scene) {
    return fold([scene.titulo,scene.resumen,scene.relato,scene.busqueda,...(scene.participantes||[]),...(scene.fuentes||[]).map(source=>source.texto)].join(' '));
  }
  function campaignEntries() {
    if(campaignSearchIndex)return campaignSearchIndex;
    const entries=[];
    const scenes=roleScenes(),scenesById=new Map(scenes.map(scene=>[scene.id,scene]));
    const add=(type,title,href,body,chapterNumbers=[],extra='',meta='')=>entries.push({type,title,href,body:String(body||''),chapters:[...new Set(chapterNumbers)],text:fold([title,body,extra].join(' ')),titleText:fold(title),meta});
    const historyText=history=>(history?.etapas||[]).map(stage=>stage.titulo+' '+stage.texto).join(' ');
    const referenceChapters=ids=>ids.map(id=>facts.get(id)?.capitulo).filter(n=>n!=null);
    for(const item of searchIndex)entries.push({type:'registro',title:item.fact.titulo,titleText:fold(item.fact.titulo),text:item.text,chapters:[item.fact.capitulo],fact:item.fact});
    for(const c of data.chapters)add('capitulo',c.titulo,'#capitulo/'+c.capitulo,c.resumen,[c.capitulo],[chapterName(c.capitulo),historyText(c.history),...(c.misiones||[]),...(c.misiones_editoriales||[]).map(m=>typeof m==='string'?m:[m.titulo,m.descripcion,m.estado].join(' ')),...(c.preguntas||[]),...(c.contradicciones||[]),...(c.nombres||[])].join(' '),chapterName(c.capitulo));
    for(const e of data.entities)add(e.type,e.name,routeEntity(e.name),[e.description,historyText(e.history),e.note].filter(Boolean).join(' '),referenceChapters([...e.facts,...(e.history?.etapas||[]).flatMap(stage=>stage.referencias)]),e.aliases.join(' '),searchTypes[e.type]);
    for(const scene of scenes)add('rol',scene.titulo,roleRoute(scene),scene.relato||scene.resumen,[scene.intervalo?.anterior,scene.intervalo?.siguiente].filter(n=>chapters.has(n)),roleSearchText(scene),'Rol escrito · '+roleDate(scene));
    for(const q of questions.values())add('pregunta',q.pregunta,'#pregunta/'+encodeURIComponent(q.id),[q.respuesta,q.pendiente].filter(Boolean).join(' '),[q.capitulo,...referenceChapters(q.referencias)],q.id+' '+q.referencias.join(' '),questionStates[q.estado]);
    for(const [key,doc] of Object.entries(data.documents))if(key!=='metodo')add('documento',sections[key]||doc.title,['atlas','facciones'].includes(key)?'#documento/'+key:'#'+key,doc.text,[],doc.title);
    for(const report of data.writtenRole?.integration||[])for(const category of ['identidades','arcos','pendientes','relaciones'])for(const item of report[category]||[]) {
      const source=item.fuentes_rol?.[0]||item.cotejo_posterior?.fuentes_rol?.[0];
      if(!source)continue;
      const scene=scenesById.get(source.escena);
      if(!scene)continue;
      add('rol',item.nombre||item.pregunta||(item.personas||[]).join(' · '),roleRoute(scene)+'/'+encodeURIComponent(source.mensaje_id),[item.avance,item.desarrollo,item.nota,item.cotejo_posterior?.respuesta,item.cotejo_posterior?.pendiente].filter(Boolean).join(' '),[scene.intervalo?.anterior,scene.intervalo?.siguiente].filter(n=>chapters.has(n)),(item.alias||[]).join(' '),'Rol escrito · '+report.hilo);
    }
    campaignSearchIndex=entries;
    return entries;
  }
  function heading(title,trail='Enciclopedia') {
    document.getElementById('page-title').textContent=title;
    document.getElementById('breadcrumbs').textContent=trail;
    document.title=title+' · '+campaign.name+' · Arghast';
  }
  function sectionNavigation(items) {
    return `<nav class="section-navigation" aria-label="Ir a un apartado"><span>Saltar a</span>${items.map(([id,label])=>`<button type="button" data-section-target="${esc(id)}">${esc(label)}</button>`).join('')}</nav>`;
  }
  function documentSection(id,title,body,classes='') {
    return `<section class="document-section ${classes}" aria-labelledby="${esc(id)}"><h2 id="${esc(id)}" tabindex="-1">${esc(title)}</h2>${body}</section>`;
  }
  function catalogueViews(type,overview=false) {
    const category=categories[type];
    if(!category.document||!data.documents[category.document])return '';
    return `<nav class="chronicle-views catalogue-views" aria-label="Vistas de ${esc(category.title)}"><a href="#${category.route}"${overview?'':' aria-current="page"'}>${esc(category.title)}</a><a href="#documento/${category.document}"${overview?' aria-current="page"':''}>${esc(category.overview)}</a></nav>`;
  }
  function campaignURL(id) {
    const url=new URL(location.href);
    url.searchParams.set('campana',id);
    url.hash='inicio';
    return url.href;
  }
  function worldHome() {
    heading('Campañas','Arghast');
    document.title='Arghast · Archivo de campañas';
    const worlds=Object.values(campaignMetadata).map(meta=>meta.id==='xoltacan'?archive:archive.campaigns[meta.id]);
    const worldChapters=worlds.reduce((total,dataset)=>total+dataset.chapters.length,0);
    content.innerHTML=`<section class="world-hero"><h1>Arghast</h1><p>Selecciona una campaña.</p><div class="world-summary" aria-label="Contenido del archivo"><span><strong>${worlds.length}</strong> campañas</span><span><strong>${worldChapters}</strong> crónicas</span></div></section><div class="world-campaigns">${Object.values(campaignMetadata).map(meta=>{const dataset=meta.id==='xoltacan'?archive:archive.campaigns[meta.id];const reviewed=dataset.chapters.filter(c=>c.estado==='revisado').length;return `<a class="world-campaign world-campaign-${meta.id}" href="${esc(campaignURL(meta.id))}"><div class="campaign-landscape" aria-hidden="true"></div><div class="campaign-card-body"><span class="eyebrow">${esc(meta.setting)}</span><h2>${esc(meta.name)}</h2><div class="campaign-progress"><span>${reviewed} crónicas revisadas</span></div><span class="campaign-enter">Explorar ${esc(meta.name)} <span aria-hidden="true">→</span></span></div></a>`;}).join('')}</div>`;
  }
  function pendingSection(title,copy) {
    heading(title,campaign.name+' · Archivo en preparación');
    content.innerHTML=`<div class="section-head"><div><p class="eyebrow">${esc(campaign.name)}</p><h1>${esc(title)}</h1></div></div><div class="empty pending-content"><h2>Contenido pendiente de revisión</h2><p>${esc(copy||'El catálogo está incorporado. Falta recuperar y revisar las transcripciones antes de redactar fichas y relatos con evidencias.')}</p><a class="primary-button" href="#capitulos">Explorar los capítulos →</a></div>`;
  }
  function event(f,detail=false) {
    return `<article class="event" id="fact-${esc(f.id)}"><div class="event-time"><strong>${String(f.capitulo).padStart(2,'0')}</strong><small>${clock(f.inicio)}</small></div><div class="event-body"><div class="card-meta">${badge(f)}<span>${esc(f.id)}</span></div><h3><a href="#registro/${f.id}">${esc(f.titulo)}</a></h3><p>${esc(detail?f.afirmacion:short(f.afirmacion,300))}</p>${detail?`<div class="evidence"><span class="eyebrow">Cita literal de los subtítulos</span><blockquote class="quote">${esc(f.cita)}</blockquote><a class="source-link" href="${sourceURL(f)}" target="_blank" rel="noopener noreferrer">Ver en YouTube · ${clock(f.evidencia_cue?.inicio || f.inicio)} ${icons.arrow}</a></div>${f.limitacion?`<p class="limitations"><strong>Alcance de la evidencia.</strong> ${esc(f.limitacion)}</p>`:''}<div class="chips">${f.entidades.map(chip).join('')}</div>`:`<a class="source-link" href="#registro/${f.id}">Consultar evidencia ${icons.arrow}</a>`}</div></article>`;
  }
  function entityCard(e) {
    const storyRefs=e.history?.etapas.flatMap(stage=>stage.referencias)||[];
    const ns=[...new Set([...e.facts,...storyRefs].map(id=>facts.get(id).capitulo))].sort((a,b)=>a-b);
    const preview=e.history?.etapas[0]?.texto || e.description || facts.get(e.facts[0])?.titulo || '';
    const invitation={personaje:'Leer su historia',lugar:'Conocer el lugar',faccion:'Conocer la facción',objeto:'Seguir su recorrido'}[e.type];
    return `<a class="card entity-card" data-kind="${esc(e.type)}" href="${routeEntity(e.name)}">${crest(e.type)}<span class="card-tag">${entityType(e.name)}</span><h3 class="card-title">${esc(e.name)}</h3><p class="card-copy">${esc(short(preview,240))}</p>${e.history?`<span class="story-invitation">${invitation} <span aria-hidden="true">↗</span></span>`:''}<div class="card-meta"><span>${e.facts.length} ${e.facts.length===1?'registro':'registros'}</span><span>Cap. ${String(ns[0]).padStart(2,'0')}–${String(ns.at(-1)).padStart(2,'0')} ${icons.arrow}</span></div></a>`;
  }
  function crest(type) {
    const paths={
      personaje:'<path d="M8 26c0-7 3-10 8-10s8 3 8 10M5 27h22M11 9a5 5 0 1 0 10 0 5 5 0 1 0-10 0M8 23l4 4m12-4-4 4"/>',
      lugar:'<path d="M16 28V13m0 10C5 24 3 15 5 7c8 1 12 6 11 13m0 0c-1-9 3-14 11-16 2 9-2 17-11 18M5 29h22M9 13l7 9m7-11-7 9"/>',
      faccion:'<path d="m16 3 11 4v10c0 6-7 11-11 13C12 28 5 23 5 17V7Zm0 5 4 6-4 9-4-9Zm-7 2v7c0 4 4 7 7 9"/>',
      objeto:'<path d="m22 3 7 7-15 15-7-7Zm-3 3 7 7M5 16l11 11M4 28l6-6M3 25l4 4M19 12l3 3M16 15l3 3"/>'
    };
    return `<span class="card-crest" aria-hidden="true"><svg viewBox="0 0 32 32">${paths[type]||paths.personaje}</svg></span>`;
  }
  function entityType(name) {
    return categories[entities.get(name)?.type]?.title || 'Referencia del pasaje';
  }
  function filters(global=false) {
    return `<div class="filters">${global?`<label>Contenido<select class="filter-select" data-filter="searchType"><option value="">Todo el contenido</option>${Object.entries(searchTypes).map(([key,label])=>`<option value="${key}" ${state.searchType===key?'selected':''}>${esc(label)}</option>`).join('')}</select></label>`:''}<label>Capítulo<select class="filter-select" data-filter="chapter"><option value="">Todos los capítulos</option>${data.chapters.map(c=>`<option value="${c.capitulo}" ${String(c.capitulo)===state.chapter?'selected':''}>${String(c.capitulo).padStart(2,'0')} · ${esc(short(c.titulo,45))}</option>`).join('')}</select></label><label>Evidencia<select class="filter-select" data-filter="kind"><option value="">Todos los tipos</option>${Object.entries(labels).map(([key,label])=>`<option value="${key}" ${state.kind===key?'selected':''}>${label}</option>`).join('')}</select></label><button class="secondary-button" data-reset>Restablecer</button></div>`;
  }
  function paginated(list,render=event,size=35) {
    const count=Math.ceil(list.length/size);
    state.page=Math.min(Math.max(1,state.page),Math.max(1,count));
    const start=(state.page-1)*size;
    const empty='<div class="empty"><h3>No hay resultados</h3><p>Prueba otra grafía del nombre o quita algún filtro. Una búsqueda vacía no prueba que el dato falte en la campaña.</p></div>';
    return `<div class="toolbar"><span class="count">${list.length} ${list.length===1?'resultado':'resultados'}</span>${list.length?`<span>Mostrando ${start+1}–${Math.min(start+size,list.length)}</span>`:''}</div><div class="${render===entityCard?'grid':'list'}">${list.length?list.slice(start,start+size).map(f=>render(f)).join(''):empty}</div>${count>1?`<nav class="pagination" aria-label="Paginación"><button class="secondary-button" data-page="${state.page-1}" ${state.page===1?'disabled':''}>← Anterior</button><span>Página ${state.page} de ${count}</span><button class="secondary-button" data-page="${state.page+1}" ${state.page===count?'disabled':''}>Siguiente →</button></nav>`:''}`;
  }
  function homeActions() {
    return `<div class="hero-actions"><a class="primary-button" href="#lectura">Leer historia <span aria-hidden="true">→</span></a><a class="secondary-button" href="#misterios">Seguir los misterios</a></div>`;
  }
  function campaignHero() {
    const kuroto=campaignId==='kuroto';
    const title=esc(campaign.name);
    const copy='Crónicas y transcripciones de la partida.';
    const landscape='<div class="hero-art" role="img" aria-label="Portada de '+esc(campaign.name)+'"></div>';
    return `<section class="hero${kuroto?' kuroto-hero':''}"><div><h1 class="hero-title">${title}</h1><p class="hero-copy">${copy}</p>${homeActions()}</div>${landscape}</section>`;
  }
  function homeStats() {
    const items=[['capitulos',data.chapters.length],['cronologia',data.facts.length],['personajes',data.entities.filter(e=>e.type==='personaje').length],['atlas',data.entities.filter(e=>e.type==='lugar').length]];
    return `<div class="stat-grid">${items.map(([route,count])=>`<a class="stat" href="#${route}"><strong>${count}</strong><span>${sections[route]}</span></a>`).join('')}</div>`;
  }
  function homeShortcuts() {
    const items=[...Object.entries(categories).map(([type,category])=>({route:category.route,type,copy:{personaje:'Sus historias y caminos',lugar:'Escenarios de la aventura',faccion:'Alianzas, poderes y conflictos',objeto:'Objetos con historia'}[type]})),{route:'misiones',type:'objeto',copy:'Objetivos y consecuencias'},{route:'relaciones',type:'faccion',copy:'Los vínculos de la campaña'}];
    return `<nav class="expedition-links" aria-label="Explorar la campaña">${items.map(item=>`<a class="expedition-link" href="#${item.route}">${crest(item.type)}<div><strong>${sections[item.route]}</strong></div><span aria-hidden="true">↗</span></a>`).join('')}</nav>`;
  }
  function home() {
    heading(sections.inicio,'Arghast · '+campaign.name);
    const available=data.chapters.filter(chapter=>chapter.transcripcion_disponible||data.transcriptFiles?.[String(chapter.capitulo)]||data.transcripts[String(chapter.capitulo)]?.length).length;
    const progress=reviewedCount<data.chapters.length?`<div class="campaign-status"><span class="eyebrow">Progreso del archivo</span><h2>Revisión pendiente</h2><p>${available} de ${data.chapters.length} transcripciones disponibles. ${reviewedCount} sesiones revisadas; ${data.chapters.length-reviewedCount} pendientes de lectura editorial.</p></div>`:'';
    const latest=data.chapters.filter(chapter=>chapter.estado==='revisado').at(-1);
    const latestStory=latest?`<section class="home-latest"><div class="section-head"><div><p class="eyebrow">Última crónica · ${chapterName(latest.capitulo)}</p><h2>${esc(latest.titulo)}</h2><p>${esc(short(latest.resumen,420))}</p></div><a class="primary-button" href="#capitulo/${latest.capitulo}">Leer el relato →</a></div></section>`:'';
    content.innerHTML=campaignHero()+homeStats()+progress+homeShortcuts()+latestStory+`<nav class="hero-actions archive-actions" aria-label="Consultar el archivo"><a class="secondary-button" href="#campanas">Elegir campaña</a></nav>`;
  }
  function civilDate(value) {
    if(!value)return 'Fecha por confirmar';
    return new Intl.DateTimeFormat('es-ES',{timeZone:'UTC',day:'2-digit',month:'2-digit',year:'numeric'}).format(new Date(value+'T12:00:00Z'));
  }
  function announcementTime(value) {
    return new Intl.DateTimeFormat('es-ES',{timeZone:'Europe/Madrid',dateStyle:'short',timeStyle:'short'}).format(new Date(value));
  }
  function twitchDateLabel(t) {
    if(t.fecha)return civilDate(t.fecha);
    const estimate=t.estimacion;
    if(!estimate)return 'Fecha por confirmar';
    return estimate.fecha_probable?'Aprox. '+civilDate(estimate.fecha_probable):civilDate(estimate.desde)+'–'+civilDate(estimate.hasta)+' (estimado)';
  }
  function chapterDates(c,compact=false) {
    const entry=c.emision;if(!entry)return '';
    const t=entry.twitch,y=entry.youtube,estimate=t.estimacion;
    const youtubeLabel=y.fecha?'Publicación en YouTube':y.fecha_aviso?'Aviso de YouTube':'Publicación en YouTube';
    const youtubeDate=y.fecha||y.fecha_aviso;
    if(compact)return `<p class="chapter-dates-compact"><span>Twitch · ${esc(twitchDateLabel(t))}</span><span>${y.fecha?'YouTube':y.fecha_aviso?'Aviso YouTube':'YouTube'} · ${esc(civilDate(youtubeDate))}</span></p>`;
    const evidence=(entry.evidencias||[]).map(e=>`<li><a href="${esc(e.url_discord)}" target="_blank" rel="noopener noreferrer">${e.plataforma==='twitch'?'Twitch':'YouTube'} · ${esc(e.titulo)}</a><small>Aviso de Discord: ${esc(announcementTime(e.aviso_utc))}.${e.timestamp_tarjeta_utc?` Fecha de la tarjeta: ${esc(announcementTime(e.timestamp_tarjeta_utc))}.`:''}</small></li>`).join('');
    const youtubeNote=y.fecha?(y.origen_fecha==='metadatos_youtube'?'Publicación documentada en los metadatos de YouTube.':'Fecha de publicación indicada por la tarjeta del aviso de YouTube.'):y.fecha_aviso?'El aviso acredita que el vídeo estaba disponible; su fecha de publicación exacta sigue por confirmar.':'No se ha localizado un aviso de este vídeo en el historial conservado.';
    const inference=estimate?`<p><strong>${t.estado==='asumida'?'Fecha asumida para la cronología. Estimación de origen':'Fecha estimada'} · confianza ${esc(estimate.confianza)}.</strong> Intervalo ${esc(civilDate(estimate.desde))}–${esc(civilDate(estimate.hasta))}. ${esc(estimate.fundamento)} Esta estimación no fija un corte exacto para situar escenas de rol escrito.</p>`:'';
    const programming=(t.programacion||[]).map(p=>`<li><a href="${esc(p.url_discord)}" target="_blank" rel="noopener noreferrer">${esc(civilDate(p.fecha))} a las ${esc(p.hora)} · calendario semanal</a><small>Calendario publicado: ${esc(announcementTime(p.aviso_utc))}.${p.editado_utc?` Mensaje editado: ${esc(announcementTime(p.editado_utc))}.`:''}</small></li>`).join('');
    const plans=programming?`<div class="date-programming"><p><strong>Programación prevista en Twitch.</strong> El calendario no acredita la realización ni la hora real de inicio. Zona de Madrid asumida por el contexto del canal.</p><ul>${programming}</ul></div>`:'';
    const warning=t.advertencia_programacion?`<p class="date-discrepancy"><strong>Discrepancia entre fuentes.</strong> ${esc(t.advertencia_programacion)}</p>`:'';
    return `<dl class="chapter-dates" aria-label="Fechas de emisión y publicación"><div><dt>Directo en Twitch</dt><dd data-date-status="${t.estado==='asumida'?'asumida':t.fecha?'documentada':estimate?'estimada':'pendiente'}">${t.fecha?`<time datetime="${esc(t.fecha)}">${esc(civilDate(t.fecha))}</time>`:esc(twitchDateLabel(t))}</dd></div><div><dt>${youtubeLabel}</dt><dd>${youtubeDate?`<time datetime="${esc(youtubeDate)}">${esc(civilDate(youtubeDate))}</time>`:'Fecha por confirmar'}</dd></div></dl><details class="context-details date-sources"><summary>Fuentes de las fechas</summary><div class="document">${inference}${plans}${warning}<p>${esc(t.nota)}${t.fechas_candidatas?.length>1?' Fechas de los avisos: '+t.fechas_candidatas.map(civilDate).join(' · ')+'.':''}</p>${t.variantes?`<p>${esc(t.variantes)}</p>`:''}<p>${esc(youtubeNote)}</p><p>Las horas de las fuentes se muestran en horario de Madrid. El inicio del directo no fija la hora exacta de comienzo del rol.</p>${evidence?`<ul>${evidence}</ul>`:''}</div></details>`;
  }
  function roleScenes() {
    return (data.writtenRole?.scenes||[]).filter(scene=>!scene.campana||scene.campana===campaignId).slice().sort((a,b)=>String(a.inicio_utc).localeCompare(String(b.inicio_utc))||String(a.id).localeCompare(String(b.id)));
  }
  const roleLoads=new Map(),roleErrors=new Set();
  function loadRoleSources(scene) {
    if(!scene.sourceFile||scene.fuentes||roleLoads.has(scene.id)||roleErrors.has(scene.id))return;
    if(scene.sourceFile!==`rol_escrito/${campaignId}/${scene.id}.js`||! /^[xk]-\d+(?:-\d+)?$/.test(scene.id)){roleErrors.add(scene.id);return;}
    const script=document.createElement('script');roleLoads.set(scene.id,script);
    script.src=new URL(scene.sourceFile,location.href).href;
    const finish=ok=>{
      const sources=globalThis.arghastWrittenRoleSources?.[campaignId+'/'+scene.id];
      if(ok&&Array.isArray(sources)&&sources.length===scene.mensajes)scene.fuentes=sources;
      else roleErrors.add(scene.id);
      roleLoads.delete(scene.id);script.remove();
      const [route,arg]=current();if(route==='rol'&&arg.split('/')[0]===scene.id)render();
    };
    script.onload=()=>finish(true);script.onerror=()=>finish(false);document.head.append(script);
  }
  function roleSourcesLoading(scene) {
    loadRoleSources(scene);
    return roleErrors.has(scene.id)?`<div class="empty"><p>No se pudieron abrir los mensajes originales. Comprueba que la carpeta rol_escrito acompañe al HTML.</p><button class="secondary-button" data-role-retry="${esc(scene.id)}">Volver a intentar</button></div>`:'<p class="notice" role="status">Abriendo los mensajes originales…</p>';
  }
  function roleRoute(scene) {return '#rol/'+encodeURIComponent(scene.id);}
  function discordURL(value) {return /^https:\/\/(?:discord\.com|discordapp\.com)\/channels\/\d+\/\d+\/\d+(?:\?.*)?$/.test(value||'')?value:null;}
  function roleDate(scene) {
    const first=scene.fecha_local||String(scene.inicio_utc||'').slice(0,10);
    const last=scene.fin_utc?new Intl.DateTimeFormat('sv-SE',{timeZone:'Europe/Madrid'}).format(new Date(scene.fin_utc)):first;
    return civilDate(first)+(last&&last!==first?'–'+civilDate(last):'');
  }
  function roleInterval(scene,links=false) {
    const interval=scene.intervalo||{},chapter=n=>{
      const label=chapters.has(n)?chapterName(n):'Directo '+n+' · sin vídeo incorporado';
      const source=discordURL(n===interval.anterior?interval.anterior_fuente:interval.siguiente_fuente);
      return links&&chapters.has(n)?`<a href="#capitulo/${n}">${chapterName(n)}</a>`:links&&source?`<a href="${esc(source)}" target="_blank" rel="noopener noreferrer">${esc(label)}</a>`:esc(label);
    };
    if(interval.ambito==='antes_del_primero')return interval.siguiente!=null?'Antes del '+chapter(interval.siguiente):'Antes del primer capítulo';
    if(interval.anterior!=null&&interval.siguiente!=null)return 'Entre '+chapter(interval.anterior)+' y '+chapter(interval.siguiente);
    if(interval.ambito==='despues_del_catalogo')return 'Posterior al catálogo de vídeos disponible';
    if(interval.siguiente!=null)return 'Antes del '+chapter(interval.siguiente);
    if(interval.anterior!=null)return 'Después del '+chapter(interval.anterior);
    return 'Situación entre capítulos pendiente de revisión';
  }
  function roleCard(scene) {
    const status={cerrada:'Escena cerrada',abierta:'Escena abierta',continuacion:'Continuación'}[scene.estado]||'Escena escrita';
    const participants=(scene.participantes||[]).join(' · ');
    return `<a class="card role-card" data-role-id="${esc(scene.id)}" href="${roleRoute(scene)}"><span class="card-tag">Rol escrito · ${esc(roleDate(scene))}</span><h3 class="card-title">${esc(scene.titulo||'Interacción escrita')}</h3>${scene.resumen?`<p class="card-copy">${esc(short(scene.resumen,250))}</p>`:''}${participants?`<p class="role-participants">${esc(participants)}</p>`:''}<div class="card-meta"><span>${esc(status)} · ${scene.mensajes??scene.fuentes?.length??0} mensajes</span><span>${scene.revisada?'Revisada':'Lectura editorial pendiente'} ${icons.arrow}</span></div></a>`;
  }
  function readingHref(kind,id) {return '#lectura/'+kind+'/'+encodeURIComponent(id);}
  function chronicleViews(active,reading='#lectura') {
    return `<nav class="chronicle-views" aria-label="Vistas de las crónicas">${[['lectura','Leer historia',reading],['capitulos','Capítulos','#capitulos'],['rol','Escenas','#rol']].map(([key,label,href])=>`<a href="${href}"${key===active?' aria-current="page"':''}>${label}${key==='lectura'?'':`<span class="chronicle-view-count">${key==='capitulos'?data.chapters.length:roleScenes().length}</span>`}</a>`).join('')}</nav>`;
  }
  function readingItems() {
    const ordered=data.chapters.slice().sort((a,b)=>a.capitulo-b.capitulo);
    const positions=new Map(ordered.map((chapter,index)=>[chapter.capitulo,index]));
    const items=ordered.map((chapter,index)=>({kind:'capitulo',id:String(chapter.capitulo),title:chapter.titulo,chapter,slot:index*2+1}));
    for(const scene of roleScenes()) {
      const interval=scene.intervalo||{};
      const slot=positions.has(interval.siguiente)?positions.get(interval.siguiente)*2:positions.has(interval.anterior)?positions.get(interval.anterior)*2+2:interval.ambito==='antes_del_primero'?0:ordered.length*2;
      items.push({kind:'rol',id:scene.id,title:scene.titulo,scene,slot});
    }
    return items.sort((a,b)=>a.slot-b.slot||String(a.scene?.inicio_utc||'').localeCompare(String(b.scene?.inicio_utc||''))||a.id.localeCompare(b.id));
  }
  function readingArticle(item,index) {
    const chapter=item.chapter,scene=item.scene;
    const paragraphs=text=>String(text||'').split(/\n\s*\n/).filter(Boolean).map(p=>`<p>${esc(p)}</p>`).join('');
    const label=chapter?chapterName(chapter.capitulo):'Escena · '+roleDate(scene);
    const date=chapter?.emision?.twitch?`<p class="reading-date">Directo en Twitch · ${esc(twitchDateLabel(chapter.emision.twitch))}${chapter.emision.twitch.estado==='asumida'?' · fecha asumida':''}</p>`:'';
    const prose=chapter?(chapter.history?.etapas?.length?chapter.history.etapas.map(stage=>`<section class="reading-stage"><h3>${esc(stage.titulo)}</h3>${paragraphs(stage.texto)}</section>`).join(''):paragraphs(chapter.resumen||'El relato de esta sesión está pendiente de revisión.')):paragraphs(scene.relato||scene.resumen);
    const position=scene?`<p class="reading-date">${roleInterval(scene)}</p>`:'';
    const future=scene?.intervalo?.ambito==='despues_del_catalogo'?'<p class="role-placement-note">Posterior al último vídeo incorporado. Pueden faltar capítulos intermedios en la biblioteca.</p>':'';
    const references=chapter?[...new Set((chapter.history?.etapas||[]).flatMap(stage=>stage.referencias||[]))].map(id=>`<a href="#registro/${esc(id)}">${esc(id)}</a>`).join(' · '):'';
    const notes=scene?.notas?.length?`<ul>${scene.notas.map(note=>`<li>${esc(note)}</li>`).join('')}</ul>`:'';
    const context=chapter?`${chapterDates(chapter)}${references?`<p class="reading-references">${references}</p>`:''}<a href="#capitulo/${chapter.capitulo}">Ver ficha del capítulo</a>`:`<p>${esc(scene.intervalo?.nota||'')}</p>${notes}<a href="${roleRoute(scene)}">Ver escena y mensajes</a>`;
    const titleId='reading-title-'+item.kind+'-'+item.id;
    return `<article class="reading-entry" data-reading-kind="${item.kind}" data-reading-id="${esc(item.id)}" data-reading-index="${index}" aria-labelledby="${esc(titleId)}"><header class="reading-heading"><p class="eyebrow">${esc(label)}</p><h2 class="reading-title" id="${esc(titleId)}" tabindex="-1">${esc(item.title)}</h2>${date}${position}</header>${future}<div class="reading-prose">${prose}</div><section class="reading-context" aria-label="Fuentes y contexto"><h3>Fuentes y contexto</h3>${context}</section></article>`;
  }
  let readingStream=null;
  function readingJump() {
    return `<aside class="reading-jump" aria-label="Navegación por la historia"><section class="reading-jump-panel" id="reading-jump-panel" aria-labelledby="reading-jump-title" hidden><header><h2 id="reading-jump-title">Índice de la historia</h2><button class="reading-jump-close" data-reading-jump-close aria-label="Cerrar índice">×</button></header><label for="reading-jump-search">Buscar en la historia</label><input id="reading-jump-search" type="search" placeholder="Capítulo, escena o personaje…" autocomplete="off"><nav class="reading-jump-results" aria-label="Capítulos y escenas"></nav><p class="reading-jump-count" role="status" aria-live="polite"></p></section><button class="secondary-button reading-jump-toggle" data-reading-jump-toggle aria-expanded="false" aria-controls="reading-jump-panel">Saltar a</button></aside>`;
  }
  function readingJumpResults(query='') {
    if(!readingStream)return;
    const terms=fold(query).trim().split(/\s+/).filter(Boolean);
    const items=readingStream.items.filter(item=>terms.every(term=>fold([item.chapter?'Capítulo '+item.id:'Escena',item.title,...(item.scene?.participantes||[])].join(' ')).includes(term)));
    const results=content.querySelector('.reading-jump-results');
    results.innerHTML=items.map(item=>`<a href="${readingHref(item.kind,item.id)}"><span>${esc(item.chapter?chapterName(item.chapter.capitulo):'Escena · '+roleDate(item.scene))}</span>${esc(item.title)}</a>`).join('');
    results.scrollTop=0;
    content.querySelector('.reading-jump-count').textContent=items.length?items.length+' relatos':'No hay coincidencias.';
  }
  function closeReadingJump(restoreFocus=false) {
    const panel=content.querySelector('.reading-jump-panel'),button=content.querySelector('[data-reading-jump-toggle]');
    if(!panel||panel.hidden)return;
    panel.hidden=true;button.setAttribute('aria-expanded','false');
    if(restoreFocus)button.focus({preventScroll:true});
  }
  function toggleReadingJump() {
    const panel=content.querySelector('.reading-jump-panel'),button=content.querySelector('[data-reading-jump-toggle]');
    if(!panel)return;
    if(!panel.hidden)return closeReadingJump(true);
    panel.hidden=false;button.setAttribute('aria-expanded','true');
    const input=content.querySelector('#reading-jump-search');
    readingJumpResults(input.value);applyCampaignLettering();input.focus({preventScroll:true});
  }
  function stopReadingStream() {
    if(!readingStream)return;
    readingStream.observer?.disconnect();
    if(readingStream.frame)cancelAnimationFrame(readingStream.frame);
    readingStream=null;
  }
  function appendReadingChunk() {
    const stream=readingStream;
    if(!stream||!stream.container.isConnected||stream.cursor>=stream.items.length)return;
    stream.container.setAttribute('aria-busy','true');
    const end=Math.min(stream.cursor+6,stream.items.length);
    stream.container.insertAdjacentHTML('beforeend',stream.items.slice(stream.cursor,end).map((item,i)=>readingArticle(item,stream.cursor+i)).join(''));
    stream.cursor=end;
    stream.container.setAttribute('aria-busy','false');
    const finished=end===stream.items.length;
    stream.sentinel.textContent=finished?'Fin del contenido disponible.':'';
    stream.sentinel.dataset.finished=String(finished);
    if(finished)stream.observer?.disconnect();
    applyCampaignLettering();
    scheduleReadingLoad();
  }
  function scheduleReadingLoad() {
    const stream=readingStream;
    if(!stream||stream.frame||stream.cursor>=stream.items.length)return;
    stream.frame=requestAnimationFrame(()=>{
      stream.frame=0;
      if(readingStream===stream&&stream.container.isConnected&&stream.sentinel.getBoundingClientRect().top<=innerHeight+1000)appendReadingChunk();
    });
  }
  function readingView(rawId) {
    const items=readingItems();if(!items.length)return pendingSection(sections.capitulos);
    const index=rawId?items.findIndex(item=>item.kind+'/'+item.id===rawId):0;
    if(index<0)return missing();
    heading('Leer historia',sections.capitulos+' · Lectura');
    content.innerHTML=chronicleViews('lectura')+`<h1 class="sr-only">Historia de ${esc(campaign.name)}</h1><div class="reading-stream" aria-label="Historia de ${esc(campaign.name)}" data-reading-total="${items.length}"></div><p class="reading-status" role="status" aria-live="polite"></p>`+readingJump();
    readingStream={items,cursor:index,container:content.querySelector('.reading-stream'),sentinel:content.querySelector('.reading-status'),frame:0};
    appendReadingChunk();
    if(readingStream.cursor<items.length&&typeof IntersectionObserver==='function') {
      readingStream.observer=new IntersectionObserver(entries=>{if(entries.some(entry=>entry.isIntersecting))scheduleReadingLoad();},{rootMargin:'1000px 0px'});
      readingStream.observer.observe(readingStream.sentinel);
    }
  }
  function roleBlock(scenes,title,{afterCatalogue=false,id=''}={}) {
    if(!scenes.length)return '';
    const description=afterCatalogue?'Estas interacciones son posteriores al último vídeo incorporado. Pueden corresponder a capítulos todavía ausentes del catálogo; no se atribuyen automáticamente a la continuación inmediata de ese vídeo.':'';
    const body=`${description?`<p class="role-placement-note">${description}</p>`:''}<div class="role-cards">${scenes.map(roleCard).join('')}</div>`;
    return `<section class="role-block${afterCatalogue?' role-after-catalogue':''}" data-role-count="${scenes.length}" aria-label="${esc(title)}"><h2 class="role-block-title"${id?` id="${esc(id)}" tabindex="-1"`:''}>${esc(title)}</h2><p class="role-block-count">${scenes.length} ${scenes.length===1?'escena':'escenas'} · ${esc(roleDate(scenes[0]))}${scenes.length>1?' / '+esc(roleDate(scenes.at(-1))):''}</p>${body}</section>`;
  }
  function chapterRole(n,before) {
    const scenes=roleScenes().filter(scene=>before?scene.intervalo?.siguiente===n:scene.intervalo?.anterior===n||(n===Math.max(...chapters.keys())&&scene.intervalo?.ambito==='despues_del_catalogo'));
    const regular=scenes.filter(scene=>scene.intervalo?.ambito!=='despues_del_catalogo');
    const later=scenes.filter(scene=>scene.intervalo?.ambito==='despues_del_catalogo');
    return roleBlock(regular,before?'Antes del capítulo':'Después del capítulo',{id:before?'chapter-role-before-title':'chapter-role-after-title'})+roleBlock(later,'Rol posterior al catálogo',{afterCatalogue:true,id:'chapter-role-later-title'});
  }
  function roleInline(text) {
    const safe=esc(text);
    return safe.replace(/\*\*([^*]+)\*\*|\*([^*]+)\*/g,(_,action,thought)=>action?`<strong class="role-action">${action}</strong>`:`<em class="role-thought">${thought}</em>`);
  }
  function roleSource(source) {
    const url=discordURL(source.url_discord);
    const segments=Array.isArray(source.segmentos)&&source.segmentos.length?source.segmentos.map(segment=>segment.tipo==='accion'?`<strong class="role-action">${esc(segment.texto)}</strong>`:segment.tipo==='pensamiento'?`<em class="role-thought">${esc(segment.texto)}</em>`:esc(segment.texto)).join(''):roleInline(source.texto||'');
    const attachments=(source.adjuntos||[]).map(attachment=>{
      const value=attachment.url||'',valid=/^https:\/\/(?:cdn\.discordapp\.com|media\.discordapp\.net)\/attachments\/\d+\/\d+\//.test(value)||/^(?!\/)(?!.*(?:^|\/)\.\.(?:\/|$))[a-zA-Z0-9_./ -]+$/.test(value);
      return valid?`<li><a href="${esc(value)}" target="_blank" rel="noopener noreferrer">${esc(attachment.nombre||'Archivo adjunto')} ↗</a></li>`:'';
    }).join('');
    const audio=(source.transcripciones_audio||[]).map(note=>`<section class="role-audio-transcript" aria-label="Nota de voz"><h3>Nota de voz <small>Transcripción automática</small></h3><p>Puede contener errores, especialmente en los nombres. El audio original se conserva en los adjuntos.</p><div class="role-message-text">${esc(note.texto)}</div></section>`).join('');
    const forwarded=(source.reenviados||[]).map(item=>`<div class="role-forwarded"><p>Contenido reenviado${item.fecha_original_utc?' · '+esc(announcementTime(item.fecha_original_utc)):''}</p><div class="role-message-text">${roleInline(item.texto)}</div></div>`).join('');
    return `<article class="role-message" id="mensaje-${esc(source.id)}"><header>${source.personaje?`<strong>${esc(source.personaje)}</strong>`:source.no_narrativo?'<span>Contexto del hilo</span>':'<span>Mensaje original</span>'}${source.fecha_utc?`<time datetime="${esc(source.fecha_utc)}">${esc(announcementTime(source.fecha_utc))}</time>`:''}${url?`<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">Ver en Discord ↗</a>`:''}</header>${source.nota_editorial?`<p class="role-source-note">${esc(source.nota_editorial)}</p>`:''}<div class="role-message-text">${segments||'<span class="role-empty-message">Mensaje sin texto.</span>'}</div>${forwarded}${attachments?`<ul class="role-attachments" aria-label="Archivos adjuntos">${attachments}</ul>`:''}${audio}</article>`;
  }
  function roleList() {
    heading('Rol escrito',sections.capitulos+' · '+campaign.name);
    const all=roleScenes(),terms=fold(state.roleQuery).trim().split(/\s+/).filter(Boolean);
    const scenes=all.filter(scene=>terms.every(term=>roleSearchText(scene).includes(term)));
    const groups=new Map();for(const scene of scenes){const interval=scene.intervalo||{},key=[interval.ambito,interval.anterior,interval.siguiente].join('/');if(!groups.has(key))groups.set(key,[]);groups.get(key).push(scene);}
    content.innerHTML=chronicleViews('rol')+`<div class="section-head"><div><p class="eyebrow">${esc(campaign.name)} · Crónicas</p><h1>Rol escrito</h1><p>${all.length} escenas conservadas · fechas de los mensajes en horario de Madrid.</p></div></div><p class="archive-note">Interacciones escritas de Discord, situadas por su fecha respecto a los directos originales en Twitch. Las escenas abiertas conservan ese estado y los pensamientos pertenecen al personaje que los expresa.</p><div class="filters"><label>Buscar en el rol escrito<input type="search" id="role-search" value="${esc(state.roleQuery)}" placeholder="Personaje, escena o texto…"></label></div>${scenes.length?[...groups.values()].map(group=>roleBlock(group,roleInterval(group[0]),{afterCatalogue:group[0].intervalo?.ambito==='despues_del_catalogo'})).join(''):'<div class="empty"><p>No hay escenas que coincidan con esta búsqueda.</p></div>'}`;
  }
  function roleView(rawId) {
    const [id,messageId]=rawId.split('/');
    const scene=roleScenes().find(item=>item.id===id);if(!scene)return missing();
    heading(scene.titulo||'Interacción escrita',sections.capitulos+' · Rol escrito');
    const interval=scene.intervalo||{},sources=scene.fuentes||[];
    const status={cerrada:'Escena cerrada',abierta:'Escena abierta; no consta un cierre en los mensajes conservados.',continuacion:'Continuación de una escena escrita.'}[scene.estado]||'Escena escrita';
    const participants=(scene.participantes||[]).map(name=>entities.has(name)?chip(name):`<span class="role-participant">${esc(name)}</span>`).join('');
    const prose=scene.relato||scene.resumen||'';
    const evidence=(scene.evidencias||[]).map(item=>`<li>${esc(item.afirmacion)} ${sources.some(source=>String(source.id)===String(item.mensaje_id))?`<a href="#mensaje-${esc(item.mensaje_id)}" data-role-message="${esc(item.mensaje_id)}">Mensaje original</a>`:''}${item.tipo==='pensamiento'?' <em>Pensamiento del personaje.</em>':''}</li>`).join('');
    const notes=(scene.notas||[]).map(note=>`<li>${esc(note)}</li>`).join('');
    const referenceLabels={tarjeta_twitch:'aviso de Twitch',aviso_de_contraste:'aviso de contraste',programacion:'calendario previsto',tarjeta_twitch_sin_video:'directo sin vídeo'};
    const timings=(interval.referencias||[]).map(ref=>`<li>${esc(ref.catalogado?chapterName(ref.capitulo):'Directo '+ref.capitulo)} · ${esc(civilDate(ref.fecha))}${ref.inicio_referencia_utc?' · hora de referencia ('+esc(referenceLabels[ref.tipo_referencia]||'fecha')+'): '+esc(announcementTime(ref.inicio_referencia_utc)):''}${ref.fin_estimado_utc?' · final estimado: '+esc(announcementTime(ref.fin_estimado_utc)):''}${discordURL(ref.fuente)?` <a href="${esc(ref.fuente)}" target="_blank" rel="noopener noreferrer">Fuente en Discord ↗</a>`:''}</li>`).join('');
    const timingDetails=interval.nota?`<details class="context-details"><summary>Fuentes de las fechas</summary><p>${esc(interval.nota)}</p>${timings?`<ul>${timings}</ul>`:''}</details>`:'';
    const original=scene.fuentes?sources.map(roleSource).join(''):scene.sourceFile?roleSourcesLoading(scene):'';
    content.innerHTML=chronicleViews('rol',readingHref('rol',scene.id))+`<div class="section-head"><div><p class="eyebrow">Rol escrito · ${esc(roleDate(scene))}</p><h1 id="role-scene-title" tabindex="-1">${esc(scene.titulo||'Interacción escrita')}</h1><p>${esc(status)}</p></div></div>`+sectionNavigation([['role-scene-title','Rol escrito'],...(evidence?[['role-evidence-title','Evidencias del rol escrito']]:[]),['role-original-title','Interacción original']])+`<div class="document role-scene-context"><p class="role-interval">${roleInterval(scene,true)}</p>${interval.ambito==='despues_del_catalogo'?'<p class="role-placement-note">Posterior al último vídeo incorporado. Pueden faltar capítulos intermedios en la biblioteca.</p>':''}${timingDetails}${participants?`<div class="chips" aria-label="Personajes participantes">${participants}</div>`:''}${prose?`<div class="role-prose">${String(prose).split(/\n\s*\n/).map(paragraph=>`<p>${esc(paragraph)}</p>`).join('')}</div>`:''}${!scene.revisada?'<p class="limitations">La lectura editorial de esta escena está pendiente. Los mensajes originales se conservan a continuación.</p>':''}${notes?`<ul class="role-editorial-notes">${notes}</ul>`:''}${evidence?documentSection('role-evidence-title','Evidencias del rol escrito',`<ul>${evidence}</ul>`,'role-evidence'):''}</div><div class="section-head role-original-heading"><div><p class="eyebrow">Discord · ${scene.mensajes??sources.length} mensajes</p><h2 id="role-original-title" tabindex="-1">Interacción original</h2><p>Formato habitual: acciones en negrita y pensamientos en cursiva; las notas aclaran las excepciones. Un pensamiento no implica que los demás personajes lo conozcan.</p></div></div><div class="role-transcript" aria-label="Mensajes originales de la escena">${original}</div><nav class="chapter-nav">${interval.anterior!=null&&chapters.has(interval.anterior)?`<a href="#capitulo/${interval.anterior}">← ${chapterName(interval.anterior)}</a>`:'<span></span>'}<a href="#capitulos">Volver a las crónicas</a>${interval.siguiente!=null&&chapters.has(interval.siguiente)?`<a href="#capitulo/${interval.siguiente}">${chapterName(interval.siguiente)} →</a>`:'<span></span>'}</nav>`;
    if(/^\d+$/.test(messageId||''))requestAnimationFrame(()=>document.getElementById('mensaje-'+messageId)?.scrollIntoView({block:'center',behavior:'instant'}));
  }
  function roleFollowup(kind) {
    const category={misiones:'arcos',misterios:'pendientes',relaciones:'relaciones',nombres:'identidades'}[kind];
    if(!category)return '';
    const terms=kind==='misterios'?fold(state.questionQuery).trim().split(/\s+/).filter(Boolean):[];
    if(kind==='misterios'&&state.questionStatus)return '';
    const groups=(data.writtenRole?.integration||[]).map(report=>({report,items:(report[category]||[]).filter(item=>terms.every(term=>fold(JSON.stringify(item)).includes(term)))})).filter(group=>group.items.length);
    if(!groups.length)return '';
    const bodies=groups.map(({report,items})=>`<section class="role-followup-group"><h3>${esc(report.hilo)}</h3><p>${esc(report.nota_seguimiento)}</p>${items.map(item=>{
      const name=item.nombre||item.pregunta||(item.personas||[]).join(' · '),text=item.avance||item.desarrollo||item.nota||'';
      const sources=(item.fuentes_rol||[]).map(source=>`<a href="#rol/${encodeURIComponent(source.escena)}/${esc(source.mensaje_id)}">Mensaje ${esc(source.mensaje_id)}</a>`).join(' · ');
      const comparison=item.cotejo_posterior,answer=comparison?`<p><strong>${comparison.orden_temporal==='posterior'?'Respuesta posterior en el rol':'Cotejo entre escenas'} · ${esc(comparison.estado)}.</strong> ${esc(comparison.respuesta)}</p>${comparison.pendiente?`<p>${esc(comparison.pendiente)}</p>`:''}<p class="role-followup-sources">${(comparison.fuentes_rol||[]).map(source=>`<a href="#rol/${encodeURIComponent(source.escena)}/${esc(source.mensaje_id)}">Mensaje ${esc(source.mensaje_id)}</a>`).join(' · ')}</p>`:'';
      return `<article class="role-followup-entry"><h4>${esc(name)}</h4>${text?`<p>${esc(text)}</p>`:''}${item.alias?.length?`<p>Alias o formas: ${item.alias.map(esc).join(' · ')}.</p>`:''}<p class="role-followup-sources">${sources}</p>${answer}</article>`;
    }).join('')}</section>`).join('');
    return documentSection('role-followup-title','Rol escrito',`<p class="section-count">${groups.reduce((total,group)=>total+group.items.length,0)} entradas con sus mensajes originales</p><div class="document">${bodies}</div>`,'role-followup');
  }
  function chapterList() {
    heading(sections.capitulos,campaign.name+' · Sesión a sesión');
    const terms=fold(state.chapterQuery).trim().split(/\s+/).filter(Boolean);
    const list=data.chapters.filter(c=>terms.every(term=>fold(c.capitulo+' '+c.titulo).includes(term)));
    const gap=data.catalog?.capitulos_ausentes||[];
    const scenes=roleScenes();
    const cards=list.map(c=>`<a class="card chapter-card" href="#capitulo/${c.capitulo}"><span class="card-crest" aria-hidden="true">${String(c.capitulo).padStart(2,'0')}</span><span class="card-tag">${chapterName(c.capitulo)}${c.duracion?' · '+clock(c.duracion):''}</span><h2 class="card-title">${esc(c.titulo)}</h2>${chapterDates(c,true)}<p class="card-copy">${esc(c.resumen?short(c.resumen,190):c.transcripcion_disponible?'Transcripción incorporada. Lectura y relato pendientes.':'Vídeo localizado. Transcripción y relato pendientes.')}</p><div class="card-meta"><span>${c.registros.length} registros</span><span>${c.estado==='revisado'?'Revisado':'Pendiente de revisión'} ${icons.arrow}</span></div></a>`).join('');
    content.innerHTML=chronicleViews('capitulos')+`<div class="section-head"><div><p class="eyebrow">${esc(campaign.name)} · Sesión a sesión</p><h1>${sections.capitulos}</h1><p>${data.chapters.length} vídeos catalogados · ${reviewedCount} capítulos revisados.${scenes.length?' '+scenes.length+' escenas de rol escrito en Escenas y Leer historia.':''}</p></div></div>${gap.length?`<p class="notice">El capítulo ${gap.join(', ')} no figura en la lista consultada. Conservamos la numeración original, sin rellenar ese hueco.</p>`:''}<div class="filters"><label>Buscar un capítulo<input id="chapter-search" type="search" value="${esc(state.chapterQuery)}" placeholder="Número o título…"></label></div><div class="grid chapter-grid">${cards||'<div class="empty">No hay capítulos que coincidan con esta búsqueda.</div>'}</div>`;
  }
  function chapterView(n) {
    const c=chapters.get(n); if(!c)return missing();
    heading(c.titulo,chapterName(n));
    const tabs={relato:'Relato de la sesión',hechos:'Acontecimientos',misiones:'Misiones',preguntas:'Preguntas de la sesión',transcripcion:'Transcripción'};
    let body;
    if(state.tab==='relato')body=chapterRole(n,true)+(c.history?narrativeHistory(c.history,{kind:'capitulo',title:'Relato de la sesión',kicker:chapterName(n)+' · De principio a fin'}):`<p class="chapter-summary">${esc(c.resumen||'Revisión editorial pendiente.')}</p>`)+chapterRole(n,false);
    else if(state.tab==='hechos')body='<div class="list">'+(c.registros.map(id=>event(facts.get(id),true)).join('') || '<div class="empty">Aún no hay ficha revisada de este episodio.</div>')+'</div>';
    else if(state.tab==='transcripcion')body=transcriptView(n);
    else if(state.tab==='preguntas')body=`<p class="archive-note">Preguntas planteadas en esta sesión, cotejadas con los capítulos posteriores. El estado corresponde al último capítulo revisado en cada entrada.</p><div class="list">${(c.seguimiento||[]).map(questionCard).join('')}</div>`;
    else body=`<div class="document"><p class="limitations">${state.tab==='preguntas'?'Estas preguntas describen lo desconocido en este capítulo. Consulta los misterios actuales para ver respuestas posteriores.':'Información y cautelas conservadas en la revisión del capítulo.'}</p><ul>${(c[state.tab] || []).map(line=>`<li>${inline(line)}</li>`).join('') || '<li>Sin entradas en esta sección.</li>'}</ul></div>`;
    const sourceNotes=[...(c.nombres||[]),...(c.contradicciones||[])];
    const notes=sourceNotes.length?documentSection('chapter-source-title','Notas sobre las fuentes de este capítulo',`<div class="document"><ul>${sourceNotes.map(text=>`<li>${inline(text)}</li>`).join('')}</ul></div>`,'chapter-source-notes'):'';
    content.innerHTML=chronicleViews('capitulos',readingHref('capitulo',n))+`<div class="section-head"><div><p class="eyebrow">${chapterName(n)} · ${c.registros.length} registros</p><h1>${esc(c.titulo)}</h1></div><a class="secondary-button" href="${esc(c.url)}" target="_blank" rel="noopener noreferrer">Ver en YouTube ↗</a></div>${chapterDates(c)}<nav class="detail-tabs" aria-label="Secciones del capítulo">${Object.entries(tabs).map(([key,label])=>`<button data-tab="${key}" class="${state.tab===key?'active':''}" aria-pressed="${state.tab===key}">${label}</button>`).join('')}</nav>${body}${notes}<nav class="chapter-nav">${chapters.has(n-1)?`<a href="#capitulo/${n-1}">← ${chapterName(n-1)}</a>`:'<span></span>'}<a href="#capitulos">Volver a las crónicas</a>${chapters.has(n+1)?`<a href="#capitulo/${n+1}">${chapterName(n+1)} →</a>`:'<span></span>'}</nav>`;
  }
  function transcriptView(n) {
    const all=data.transcripts[String(n)] || [];
    if(!all.length&&data.transcriptFiles?.[String(n)])return transcriptLoading(n);
    if(!all.length&&chapters.get(n).comprobacion_subtitulos?.resultado==='sin_subtitulos')return `<div class="empty"><h2>Este vídeo no ofrece subtítulos</h2><p>La consulta del ${esc(chapters.get(n).comprobacion_subtitulos.fecha)} no encontró subtítulos manuales ni automáticos en YouTube. La transcripción de esta sesión sigue pendiente.</p><a class="secondary-button" href="${esc(chapters.get(n).url)}" target="_blank" rel="noopener noreferrer">Abrir el episodio ↗</a></div>`;
    if(!all.length)return '<div class="empty"><h2>Transcripción pendiente</h2><p>El vídeo está localizado, pero su transcripción todavía no se ha incorporado. Puedes abrir el episodio desde su ficha.</p></div>';
    const terms=fold(state.transcriptQuery).trim().split(/\s+/).filter(Boolean);
    const rows=all.filter(row=>terms.every(term=>fold(row[1]).includes(term)));
    const provenance=chapters.get(n).fuente_transcripcion;
    const note=provenance?'Transcripción automática generada localmente del audio con Whisper '+provenance.modelo+'. YouTube no ofrece una pista de subtítulos para este vídeo.':'Lectura derivada de los subtítulos automáticos de YouTube, con texto original de cada segmento.';
    return `<p class="limitations">${esc(note)} El reconocimiento puede contener errores; no se identifican hablantes automáticamente.</p><div class="filters"><label class="transcript-search">Buscar en esta transcripción<input type="search" id="transcript-search" value="${esc(state.transcriptQuery)}" placeholder="Una palabra o un nombre…"></label></div><div class="toolbar"><span>${rows.length} segmentos · se muestran ${Math.min(rows.length,state.transcriptLimit)}</span></div><div class="transcript">${rows.slice(0,state.transcriptLimit).map(([t,s])=>`<div class="transcript-row"><a href="${esc(chapters.get(n).url)}&t=${Math.floor(secs(t))}s" target="_blank" rel="noopener noreferrer">${clock(t)}</a><p>${esc(s)}</p></div>`).join('') || '<div class="empty">No hay coincidencias en esta transcripción.</div>'}</div>${rows.length>state.transcriptLimit?'<button class="secondary-button" data-transcript-more>Mostrar más segmentos</button>':''}`;
  }
  function recordView(id) {
    const f=facts.get(id); if(!f)return missing();
    heading(f.titulo,`${chapterName(f.capitulo)} · ${f.id}`);
    const around=(data.transcripts[String(f.capitulo)] || []).filter(([t])=>secs(t)>=Math.max(0,secs(f.evidencia_cue?.inicio || f.inicio)-25)&&secs(t)<=secs(f.evidencia_cue?.inicio || f.inicio)+40);
    const context=around.length?`<div class="transcript">${around.map(([t,s])=>`<div class="transcript-row"><a href="${esc(chapters.get(f.capitulo).url)}&t=${Math.floor(secs(t))}s" target="_blank" rel="noopener noreferrer">${clock(t)}</a><p>${esc(s)}</p></div>`).join('')}</div>`:data.transcriptFiles?.[String(f.capitulo)]?transcriptLoading(f.capitulo):'<p>Contexto no disponible.</p>';
    content.innerHTML=`<div class="section-head"><a class="secondary-button" href="#capitulo/${f.capitulo}">← ${chapterName(f.capitulo)}</a><button class="secondary-button" data-copy="${esc(f.id)}">Copiar referencia</button></div>${event(f,true)}${documentSection('record-context-title','Leer contexto de la transcripción',context,'context-details transcript-context')}<p class="archive-note">Fuente automática · ${esc(f.ambito || 'Ámbito sin determinar')} · Intervalo de contexto ${clock(f.inicio)}–${clock(f.fin)}. La cita se localiza en ${clock(f.evidencia_cue?.inicio || f.inicio)}; comprobar su interpretación en el contexto.</p>`;
  }
  function questionCard(q) {
    const color={resuelta:'confirmed',parcial:'statement',pendiente:'speculation',sin_revisar:'speculation'}[q.estado];
    const refs=q.referencias.map(id=>{const f=facts.get(id);return `<a href="#registro/${id}">${id} · ${clock(f.evidencia_cue?.inicio||f.inicio)}</a>`;}).join(' · ');
    return `<article class="event question-card" data-question="${q.id}" data-status="${q.estado}"><div class="event-time"><strong>${String(q.capitulo).padStart(2,'0')}</strong><small>${esc(q.id)}</small></div><div class="event-body"><div class="card-meta"><span class="badge ${color}">${questionStates[q.estado]}</span><span>Revisada hasta el cap. ${q.revisado_hasta}</span></div><h3><a href="#pregunta/${q.id}">${esc(q.pregunta)}</a></h3><p>${esc(q.respuesta)}</p>${refs?`<p class="source-link">Evidencia posterior: ${refs}</p>`:''}${q.pendiente?`<p class="limitations"><strong>Sigue pendiente.</strong> ${esc(q.pendiente)}</p>`:''}${q.requiere_actualizacion?'<p class="limitations">Hay capítulos posteriores que todavía deben cotejarse con esta respuesta.</p>':''}</div></article>`;
  }
  function questionView(id) {
    const q=questions.get(id);if(!q)return missing();
    heading(q.id,sections.misterios+' · '+chapterName(q.capitulo));
    const evidence=q.referencias.map(id=>event(facts.get(id),true)).join('');
    content.innerHTML=`<div class="section-head"><a href="#misterios" class="secondary-button">← ${sections.misterios}</a><a href="#capitulo/${q.capitulo}">${chapterName(q.capitulo)} · Origen</a></div>${questionCard(q)}${evidence?`<h2>Evidencias de la respuesta</h2><div class="list">${evidence}</div>`:'<p class="archive-note">No se ha localizado una respuesta posterior en los capítulos cotejados. Esto no demuestra que el asunto carezca de solución en el mundo de la campaña.</p>'}`;
  }
  function questionList() {
    if(!reviewedCount)return pendingSection(sections.misterios,'Las preguntas y sus respuestas se documentarán después de leer las sesiones de '+campaign.name+'. No se consideran resueltas por no tener todavía entradas.');
    heading(sections.misterios,'Seguimiento de la campaña');
    const all=[...questions.values()],terms=fold(state.questionQuery).trim().split(/\s+/).filter(Boolean);
    const list=all.filter(q=>(!state.questionStatus||q.estado===state.questionStatus)&&terms.every(t=>fold(q.pregunta+' '+q.respuesta+' '+q.pendiente+' '+q.id+' '+q.referencias.join(' ')).includes(t)));
    const counts=data.seguimiento.estados;
    const followup=roleFollowup('misterios');
    content.innerHTML=`<div class="section-head"><div><p class="eyebrow">Del planteamiento a la última evidencia</p><h1 id="question-list-title" tabindex="-1">${sections.misterios}</h1><p>${all.length} preguntas históricas · ${counts.resuelta||0} resueltas · ${counts.parcial||0} parciales · ${counts.pendiente||0} pendientes${counts.sin_revisar?` · ${counts.sin_revisar} sin revisar`:''}</p></div></div><p class="section-description">Cada pregunta conserva su contexto original y se enlaza con respuestas posteriores. Una nueva pista no cierra por sí sola un misterio. ${data.seguimiento.por_actualizar?`${data.seguimiento.por_actualizar} entradas necesitan cotejar los capítulos nuevos.`:`Cotejo completo hasta el capítulo ${data.seguimiento.ultimo_capitulo}.`}</p>`+sectionNavigation([['question-list-title',sections.misterios],...(followup?[['role-followup-title','Rol escrito']]:[]),['mystery-synthesis-title','Síntesis de las tramas principales']])+`<div class="filters"><label>Buscar una pregunta o respuesta<input id="question-search" type="search" value="${esc(state.questionQuery)}" placeholder="Nombre, asunto o referencia…"></label><label>Estado<select class="filter-select" data-filter="questionStatus"><option value="">Todos los estados</option>${Object.entries(questionStates).map(([key,label])=>`<option value="${key}" ${state.questionStatus===key?'selected':''}>${label}</option>`).join('')}</select></label></div>${paginated(list,questionCard,20)}${followup}${documentSection('mystery-synthesis-title','Síntesis de las tramas principales',`<article class="document">${markdown(documentText(data.documents.misterios,sections.misterios))}</article>`,'mystery-synthesis')}`;
  }
  function entityList(type) {
    const category=categories[type];
    if(!reviewedCount)return pendingSection(category.title,'Las fichas de '+category.title.toLowerCase()+' de '+campaign.name+' se redactarán con sus historias y evidencias tras revisar las transcripciones.');
    heading(category.title,'Enciclopedia · '+category.title);
    const terms=fold(state.entityQuery).trim().split(/\s+/).filter(Boolean);
    const list=data.entities.filter(e=>e.type===type&&terms.every(t=>fold(e.name+' '+e.aliases.join(' ')).includes(t)));
    content.innerHTML=catalogueViews(type)+`<div class="section-head"><div><p class="eyebrow">${esc(campaign.name)} · Enciclopedia</p><h1>${category.title}</h1><p>${category.copy}</p></div></div><div class="filters"><label>${category.search}<input id="entity-search" type="search" value="${esc(state.entityQuery)}" placeholder="Nombre o variante…"></label></div>${paginated(list,entityCard,36)}`;
  }
  function entityView(name) {
    const e=entities.get(name)||entityAliases.get(name); if(!e)return missing();
    const category=categories[e.type];
    heading(e.name,'Enciclopedia · '+category.title);
    const refs=(e.references||[]).map(id=>facts.has(id)?`<a href="#registro/${id}">${id}</a>`:`<a href="#capitulo/${Number(id)}">${chapterName(Number(id))}</a>`).join(' · ');
    const written=roleScenes().filter(scene=>(scene.participantes||[]).some(label=>label===e.name||entityAliases.get(label)===e));
    const navigation=[...(e.history?[['narrative-story-title','Historia']]:[]),...(written.length?[['entity-role-title','Rol escrito']]:[]),['entity-evidence-title','Registros y evidencias'],...(e.note?[['entity-identification-title','Identificación y referencias']]:[])];
    content.innerHTML=`<a class="source-link" href="#${category.route}">← Volver a ${category.title.toLowerCase()}</a><div class="section-head"><div><p class="eyebrow">${entityType(e.name)} · ${e.facts.length} registros${written.length?' · '+written.length+' escenas de rol escrito':''}</p><h1>${esc(e.name)}</h1></div></div>${e.description?`<p class="${e.history?'entity-intro':'chapter-summary'}">${esc(e.description)}</p>`:''}`+sectionNavigation(navigation)+`${e.history?entityHistory(e):''}${roleBlock(written,'Rol escrito',{id:'entity-role-title'})}<div class="section-head"><div><h2 id="entity-evidence-title" tabindex="-1">Registros y evidencias</h2></div></div>${paginated(e.facts.map(id=>facts.get(id)),f=>event(f,true),25)}${e.note?documentSection('entity-identification-title','Identificación y referencias',`<div class="document"><p>${esc(e.note)}</p><p>${refs}</p></div>`,'entity-identification'):''}`;
  }
  function entityHistory(e) {
    const titles={personaje:'Historia',lugar:'Historia y acontecimientos',faccion:'Intereses y evolución',objeto:'Origen y recorrido'};
    return narrativeHistory(e.history,{kind:e.type,title:titles[e.type],kicker:'Hasta el capítulo '+e.history.revisado_hasta});
  }
  function narrativeHistory(history,{kind,title,kicker}) {
    return `<section class="character-story narrative-story" data-story-kind="${esc(kind)}" aria-labelledby="narrative-story-title"><header class="story-heading"><div class="story-emblem" aria-hidden="true">${crest(kind==='capitulo'?'objeto':kind)}</div><div><p class="eyebrow">${esc(kicker)}</p><h2 id="narrative-story-title" tabindex="-1">${esc(title)}</h2></div></header><div class="story-stages">${history.etapas.map((stage,index)=>`<article class="story-stage"><div class="story-step" aria-hidden="true">${String(index+1).padStart(2,'0')}</div><div class="story-prose"><h3>${esc(stage.titulo)}</h3><p>${esc(stage.texto)}</p><nav class="story-sources" aria-label="Fuentes de ${esc(stage.titulo)}"><span>Fuentes</span>${stage.referencias.map(id=>{const f=facts.get(id);return `<a href="#registro/${id}" title="${esc(f.titulo)}">${id} <span>· ${clock(f.evidencia_cue?.inicio||f.inicio)}</span></a>`;}).join('')}</nav></div></article>`).join('')}</div></section>`;
  }
  function listing(query='') {
    if(!reviewedCount)return pendingSection(query?'Buscar en '+campaign.name:sections.cronologia,'Todavía no hay acontecimientos revisados de '+campaign.name+'. Puedes buscar por número o título en su catálogo de capítulos.');
    const results=matched(query,state.chapter,state.kind);
    heading(query?'Resultados de búsqueda':sections.cronologia,query?'Búsqueda · '+query:'Campaña · Capítulo y minuto');
    document.getElementById('search-status').textContent=query?`${results.length} resultados para ${query}`:'';
    content.innerHTML=`<div class="section-head"><div><p class="eyebrow">El archivo, con sus evidencias</p><h1>${query?`Resultados para «${esc(query)}»`:sections.cronologia}</h1><p>${query?'Se buscan todos los términos, ignorando acentos, en registros y equivalencias documentadas.':'Orden de capítulos y minutos del vídeo. No equivale a un calendario interno entre los grupos de la campaña.'}</p></div></div>${filters()}${paginated(results)}`;
  }
  function campaignSearch(query) {
    const terms=fold(query).trim().split(/\s+/).filter(Boolean);
    const results=campaignEntries().filter(item=>(!state.searchType||item.type===state.searchType)&&(!state.chapter||item.chapters.includes(Number(state.chapter)))&&(!state.kind||item.fact?.tipo===state.kind)&&terms.every(term=>item.text.includes(term)));
    const rank=item=>item.titleText===fold(query).trim()?0:terms.every(term=>item.titleText.includes(term))?1:2;
    results.sort((a,b)=>rank(a)-rank(b));
    const resultCard=item=>{
      if(item.fact)return event(item.fact);
      const body=item.type==='documento'?item.body.replace(/\[([^\]]+)\]\([^)]+\)/g,'$1').replace(/[#*`|>]/g,''):item.body;
      const at=terms.map(term=>fold(body).indexOf(term)).find(at=>at>=0)??0;
      const start=at>110?Math.max(0,body.lastIndexOf(' ',at-70)+1):0;
      const preview=(start?'…':'')+short(body.slice(start),300);
      return `<a class="card search-result" data-search-type="${esc(item.type)}" href="${esc(item.href)}"><span class="card-tag">${esc(searchTypes[item.type])}</span><h3 class="card-title">${esc(item.title)}</h3>${preview?`<p class="card-copy">${esc(preview)}</p>`:''}<div class="card-meta"><span>${esc(item.meta)}</span><span>Consultar ${icons.arrow}</span></div></a>`;
    };
    heading('Resultados de búsqueda','Búsqueda · '+campaign.name+' · '+query);
    document.getElementById('search-status').textContent=`${results.length} resultados para ${query}`;
    content.innerHTML=`<div class="section-head"><div><p class="eyebrow">${esc(campaign.name)}</p><h1>Resultados para «${esc(query)}»</h1><p>Crónicas, acontecimientos, fichas, misterios, documentos y rol escrito, incluidos sus mensajes originales. Se buscan todos los términos, ignorando mayúsculas y acentos.</p></div></div>${filters(true)}${paginated(results,resultCard)}`;
  }
  function targetLink(raw,label) {
    if(/^https:\/\//i.test(raw))return `<a href="${esc(raw)}" target="_blank" rel="noopener noreferrer">${label}</a>`;
    const match=raw.match(/(?:^|\/)capitulos\/(\d+)\.(?:md|json)/);
    if(match){ const ids=(label.match(/\b\d{2}-\d{3}\b/g)||[]).filter(id=>facts.has(id)); return `<a href="${ids.length===1?'#registro/'+ids[0]:'#capitulo/'+Number(match[1])}">${label}</a>`; }
    const doc=Object.entries(data.documents).find(([key])=>key!=='metodo'&&raw.toUpperCase().includes(({atlas:'ATLAS',facciones:'FACCIONES',misterios:'MISTERIOS',misiones:'MISIONES',contradicciones:'CONTRADICCIONES',relaciones:'RELACIONES',nombres:'NOMBRES'}[key])+'.MD'));
    return doc?`<a href="#${['atlas','facciones'].includes(doc[0])?'documento/':''}${doc[0]}">${label}</a>`:label;
  }
  function inline(text) {
    const protectedParts=[];
    const protect=html=>{protectedParts.push(html);return '\uE000'+(protectedParts.length-1)+'\uE001';};
    let s=String(text).replace(/\[([^\]]+)\]\(([^)]+)\)/g,(_,label,url)=>protect(targetLink(url,esc(label))));
    s=esc(s).replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
    s=s.replace(/\b\d{2}-\d{3}\b/g,id=>facts.has(id)?`<a href="#registro/${id}">${id}</a>`:id);
    return s.replace(/\uE000(\d+)\uE001/g,(_,i)=>protectedParts[Number(i)]);
  }
  function markdown(text) {
    const lines=text.split(/\r?\n/),out=[];let i=0;
    while(i<lines.length){ const line=lines[i];
      if(!line.trim()){i++;continue;}
      if(/^```/.test(line)){let block=[];i++;while(i<lines.length&&!/^```/.test(lines[i]))block.push(lines[i++]);i++;out.push('<pre><code>'+esc(block.join('\n'))+'</code></pre>');continue;}
      if(/^\|/.test(line)&&i+1<lines.length&&/^\|[\s:|-]+\|\s*$/.test(lines[i+1])){const cells=row=>row.trim().replace(/^\||\|$/g,'').split('|');const headers=cells(line);i+=2;let rows=[];while(i<lines.length&&/^\|/.test(lines[i]))rows.push(cells(lines[i++]));out.push('<div class="table-wrap"><table><thead><tr>'+headers.map(c=>'<th>'+inline(c.trim())+'</th>').join('')+'</tr></thead><tbody>'+rows.map(row=>'<tr>'+row.map(c=>'<td>'+inline(c.trim())+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>');continue;}
      const heading=line.match(/^(#{1,4})\s+(.*)/);if(heading){const level=Math.min(4,heading[1].length);out.push(`<h${level}>${inline(heading[2])}</h${level}>`);i++;continue;}
      if(/^[-*]\s+/.test(line)){let items=[];while(i<lines.length&&/^[-*]\s+/.test(lines[i]))items.push('<li>'+inline(lines[i++].replace(/^[-*]\s+/,''))+'</li>');out.push('<ul>'+items.join('')+'</ul>');continue;}
      if(/^>\s*/.test(line)){out.push('<blockquote>'+inline(line.replace(/^>\s*/,''))+'</blockquote>');i++;continue;}
      let p=[line];i++;while(i<lines.length&&lines[i].trim()&&!/^(?:#{1,4} |[-*] |\||```|>)/.test(lines[i]))p.push(lines[i++]);out.push('<p>'+inline(p.join(' '))+'</p>');
    }
    return out.join('');
  }
  function documentText(doc,title) {
    return (doc?.text||'').replace(/^# [^\r\n]+/,'# '+title);
  }
  function documentView(key) {
    const doc=data.documents[key];if(!doc||key==='metodo')return missing();
    const category=Object.entries(categories).find(([,category])=>category.document===key);
    const title=category?category[1].overview:sections[key]||doc.title;
    heading(title,'Enciclopedia · '+title);
    const followup=roleFollowup(key);
    content.innerHTML=(category?catalogueViews(category[0],true):'')+(followup?sectionNavigation([['campaign-document',title],['role-followup-title','Rol escrito']]):'')+'<article class="document" id="campaign-document" tabindex="-1">'+markdown(documentText(doc,title))+'</article>'+followup;
  }
  function missing(){heading('No se encontró la entrada');content.innerHTML='<div class="empty"><h1>Esta entrada no está en el archivo.</h1><p>Vuelve al índice o busca otra grafía.</p><a class="primary-button" href="#inicio">Ir al inicio</a></div>';}
  function current(){const parts=location.hash.slice(1).split('/');let value='';try{value=decodeURIComponent(parts.slice(1).join('/'));}catch{}return [parts[0]||(archive.world&&!Object.hasOwn(campaignMetadata,requestedCampaign)?'campanas':'inicio'),value];}
  function render(reset=false) {
    if(editor?.isEditing())return;
    stopReadingStream();
    const [route,arg]=current();
    const worldView=route==='campanas';
    document.body.dataset.campaign=campaignId;
    document.body.dataset.view=worldView?'world':'campaign';
    document.getElementById('campaign-selector').value=worldView?'':campaignId;
    document.getElementById('campaign-context').textContent=worldView?'El mundo de Arghast':'Arghast / '+campaign.name;
    document.querySelector('.search-box').hidden=worldView;
    document.querySelectorAll('#sidebar .nav-label,#sidebar .nav-links').forEach(node=>node.hidden=worldView);
    document.getElementById('app-stats').textContent=worldView?Object.keys(campaignMetadata).length+' campañas independientes':`${data.chapters.length} crónicas · ${data.facts.length} acontecimientos`;
    if(route==='entidades'){history.replaceState(null,'','#personajes');return render(true);}
    if(route==='metodo'){history.replaceState(null,'','#inicio');return render(true);}
    if(route!=='busqueda'){document.getElementById('search-status').textContent='';if(reset)searchInput.value='';}
    if(reset){state.page=1;state.tab='relato';state.chapterQuery='';state.entityQuery='';state.questionQuery='';state.questionStatus='';state.roleQuery='';state.transcriptQuery='';state.transcriptLimit=120;}
    const selectedEntity=route==='entidad'?(entities.get(arg)||entityAliases.get(arg)):null;
    const selectedDocumentCategory=route==='documento'?Object.values(categories).find(category=>category.document===arg):null;
    document.querySelectorAll('#sidebar a[href^="#"]').forEach(a=>{const active=a.hash==='#'+route || ((route==='capitulo'||route==='rol'||route==='lectura')&&a.hash==='#capitulos')||(route==='pregunta'&&a.hash==='#misterios')||(selectedEntity&&a.hash==='#'+categories[selectedEntity.type].route)||(selectedDocumentCategory&&a.hash==='#'+selectedDocumentCategory.route);a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
    document.getElementById('sidebar').classList.remove('open');document.getElementById('menu-toggle')?.setAttribute('aria-expanded','false');
    const category=Object.entries(categories).find(([,value])=>value.route===route);
    if(route==='campanas')worldHome();else if(route==='inicio')home();else if(route==='capitulos')chapterList();else if(route==='lectura')readingView(arg);else if(route==='rol')arg?roleView(arg):roleList();else if(route==='capitulo')chapterView(Number(arg));else if(route==='registro')recordView(arg);else if(route==='pregunta')questionView(arg);else if(route==='misterios')questionList();else if(category)entityList(category[0]);else if(route==='entidad')entityView(arg);else if(route==='documento')documentView(arg);else if(route==='cronologia')listing();else if(route==='busqueda'){searchInput.value=arg;campaignSearch(arg);}else documentView(route);
    document.getElementById('search-clear').hidden=!searchInput.value;
    editor?.decorate(current());
    applyCampaignLettering();
  }
  content.addEventListener('click',async eventObject=>{
    const roleMessage=eventObject.target.closest('[data-role-message]');if(roleMessage){eventObject.preventDefault();const target=document.getElementById('mensaje-'+roleMessage.dataset.roleMessage);target?.scrollIntoView({block:'center',behavior:'instant'});return;}
    const button=eventObject.target.closest('button');if(!button)return;
    if(button.dataset.sectionTarget){const target=document.getElementById(button.dataset.sectionTarget);target?.scrollIntoView({block:'start',behavior:'instant'});target?.focus({preventScroll:true});return;}
    if(button.hasAttribute('data-reading-jump-toggle')){toggleReadingJump();return;}
    if(button.hasAttribute('data-reading-jump-close')){closeReadingJump(true);return;}
    if(button.dataset.page){state.page=Number(button.dataset.page);render();content.scrollIntoView({block:'start'});}
    if(button.dataset.tab){state.tab=button.dataset.tab;state.transcriptLimit=120;render();}
    if(button.hasAttribute('data-reset')){state.chapter='';state.kind='';state.searchType='';state.page=1;render();}
    if(button.hasAttribute('data-transcript-more')){state.transcriptLimit+=200;const scrollY=window.scrollY;render();window.scrollTo(0,scrollY);}
    if(button.dataset.transcriptRetry){transcriptErrors.delete(button.dataset.transcriptRetry);render();}
    if(button.dataset.roleRetry){roleErrors.delete(button.dataset.roleRetry);render();}
    if(button.dataset.copy){const f=facts.get(button.dataset.copy);const text=`Arghast · ${campaign.name} · ${f.titulo} · ${chapterName(f.capitulo)} · ${clock(f.evidencia_cue?.inicio || f.inicio)} · ${f.id}\n${f.afirmacion}\nCita: ${f.cita}\n${sourceURL(f)}`;try{if(navigator.clipboard?.writeText)await navigator.clipboard.writeText(text);else{const area=document.createElement('textarea');area.value=text;document.body.append(area);area.select();document.execCommand('copy');area.remove();}button.textContent='Referencia copiada';}catch{button.textContent='Selecciona y copia la cita';} }
    applyCampaignLettering();
  });
  content.addEventListener('change',eventObject=>{const key=eventObject.target.dataset.filter;if(key){state[key]=eventObject.target.value;state.page=1;render();}});
  content.addEventListener('input',eventObject=>{const input=eventObject.target;if(input.id==='reading-jump-search'){readingJumpResults(input.value);return;}const field={'chapter-search':'chapterQuery','entity-search':'entityQuery','transcript-search':'transcriptQuery','question-search':'questionQuery','role-search':'roleQuery'}[input.id];if(field){const selection=input.selectionStart,scroll=window.scrollY;state[field]=input.value;state.page=1;state.transcriptLimit=120;render();const restored=document.getElementById(input.id);restored.focus();restored.setSelectionRange(selection,selection);window.scrollTo(0,scroll);}});
  searchInput.addEventListener('input',()=>{clearTimeout(searchTimer);searchTimer=setTimeout(()=>{state.page=1;state.chapter='';state.kind='';state.searchType='';const q=searchInput.value.trim();history.replaceState(null,'',q?'#busqueda/'+encodeURIComponent(q):'#inicio');render();},180);});
  document.getElementById('search-clear').addEventListener('click',()=>{clearTimeout(searchTimer);searchInput.value='';location.hash='#inicio';render();searchInput.focus();});
  document.getElementById('menu-toggle')?.addEventListener('click',eventObject=>{const open=document.getElementById('sidebar').classList.toggle('open');eventObject.currentTarget.setAttribute('aria-expanded',String(open));});
  document.getElementById('campaign-selector').addEventListener('change',eventObject=>{const id=eventObject.target.value;if(Object.hasOwn(campaignMetadata,id))location.assign(campaignURL(id));else location.hash='campanas';});
  window.addEventListener('scroll',scheduleReadingLoad,{passive:true});
  window.addEventListener('resize',scheduleReadingLoad,{passive:true});
  document.addEventListener('click',eventObject=>{const jump=content.querySelector('.reading-jump');if(jump&&!jump.contains(eventObject.target))closeReadingJump();});
  document.addEventListener('keydown',eventObject=>{if(eventObject.key==='Escape')closeReadingJump(true);});
  document.addEventListener('keydown',eventObject=>{if((eventObject.ctrlKey||eventObject.metaKey)&&eventObject.key.toLowerCase()==='k'){eventObject.preventDefault();searchInput.focus();searchInput.select();}if(eventObject.key==='Escape'){document.getElementById('sidebar').classList.remove('open');document.getElementById('menu-toggle')?.setAttribute('aria-expanded','false');}});
  window.addEventListener('hashchange',()=>{render(true);if(current()[0]==='lectura'){window.scrollTo({top:0,behavior:'instant'});document.querySelector('.reading-title')?.focus({preventScroll:true});}else window.scrollTo(0,0);});
  document.getElementById('app-stats').textContent=`${data.chapters.length} crónicas · ${data.facts.length} acontecimientos`;
  for(const [id,value] of [['count-chapters',data.chapters.length],['count-facts',data.facts.length],['count-entities',data.entities.length]])if(document.getElementById(id))document.getElementById(id).textContent=value;
  const editor=window.createArchiveEditor({data,campaignId,content,lettering:applyCampaignLettering,refresh:()=>{
    facts.clear();data.facts.forEach(f=>facts.set(f.id,f));
    chapters.clear();data.chapters.forEach(c=>chapters.set(c.capitulo,c));
    entities.clear();data.entities.forEach(e=>entities.set(e.name,e));
    entityAliases.clear();data.entities.forEach(e=>e.aliases.forEach(a=>entityAliases.set(a,e)));
    questions.clear();(data.seguimiento?.preguntas||[]).forEach(q=>questions.set(q.id,q));
    reviewedCount=data.chapters.filter(c=>c.estado==='revisado').length;
    searchIndex.length=0;
    for(const f of data.facts)searchIndex.push({fact:f,text:fold([f.titulo,f.afirmacion,f.cita,f.ambito,f.limitacion,...(f.etiquetas_originales||[]),...f.entidades,...f.entidades.flatMap(name=>entities.get(name)?.aliases||[])].join(' '))});
    campaignSearchIndex=undefined;
    render();
  }});
  render();
})();
