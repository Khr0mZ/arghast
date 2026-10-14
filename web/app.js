(() => {
  'use strict';
  const archive = JSON.parse(document.getElementById('xoltacan-data').textContent);
  const campaignMetadata=archive.campaignMetadata||{xoltacan:{id:'xoltacan',name:'Xoltacan',tagline:'Entre la selva y el mar'}};
  const requestedCampaign=new URLSearchParams(location.search).get('campana')||(location.pathname.endsWith('/kuroto.html')?'kuroto':null);
  const campaignId=Object.hasOwn(campaignMetadata,requestedCampaign)?requestedCampaign:'xoltacan';
  const campaign=campaignMetadata[campaignId];
  const data = campaignId==='xoltacan'?archive:archive.campaigns[campaignId];
  const reviewedCount=data.chapters.filter(chapter=>chapter.estado==='revisado').length;
  const content = document.getElementById('content');
  const searchInput = document.getElementById('global-search');
  const facts = new Map(data.facts.map(f => [f.id, f]));
  const questions = new Map((data.seguimiento?.preguntas || []).map(q=>[q.id,q]));
  const questionStates = {resuelta:'Resuelta',parcial:'Parcialmente resuelta',pendiente:'Pendiente',sin_revisar:'Sin revisar'};
  const chapters = new Map(data.chapters.map(c => [c.capitulo, c]));
  const entities = new Map(data.entities.map(e => [e.name, e]));
  const entityAliases = new Map(data.entities.flatMap(e=>e.aliases.map(label=>[label,e])));
  const sections={inicio:'Portada',capitulos:'Crónicas',cronologia:'Acontecimientos',personajes:'Personajes',atlas:'Lugares',facciones:'Facciones',objetos:'Vestigios',misiones:'Misiones',misterios:'Misterios y desenlaces',relaciones:'Relaciones',metodo:'Fuentes y método',nombres:'Nombres y equivalencias'};
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
  let state={page:1,chapter:'',kind:'',chapterQuery:'',entityQuery:'',questionQuery:'',questionStatus:'',tab:'relato',transcriptQuery:'',transcriptLimit:120};
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
      const rows=globalThis.arghastTranscripts?.[campaignId+'/'+number];
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
  function heading(title,trail='Enciclopedia') {
    document.getElementById('page-title').textContent=title;
    document.getElementById('breadcrumbs').textContent=trail;
    document.title=title+' · '+campaign.name+' · Arghast';
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
    const preview=e.history?.etapas[0]?.texto || e.description || facts.get(e.facts[0]).titulo;
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
  function filters() {
    return `<div class="filters"><label>Capítulo<select class="filter-select" data-filter="chapter"><option value="">Todos los capítulos</option>${data.chapters.map(c=>`<option value="${c.capitulo}" ${String(c.capitulo)===state.chapter?'selected':''}>${String(c.capitulo).padStart(2,'0')} · ${esc(short(c.titulo,45))}</option>`).join('')}</select></label><label>Evidencia<select class="filter-select" data-filter="kind"><option value="">Todos los tipos</option>${Object.entries(labels).map(([key,label])=>`<option value="${key}" ${state.kind===key?'selected':''}>${label}</option>`).join('')}</select></label><button class="secondary-button" data-reset>Restablecer</button></div>`;
  }
  function paginated(list,render=event,size=35) {
    const count=Math.ceil(list.length/size);
    state.page=Math.min(Math.max(1,state.page),Math.max(1,count));
    const start=(state.page-1)*size;
    const empty='<div class="empty"><h3>No hay resultados</h3><p>Prueba otra grafía del nombre o quita algún filtro. Una búsqueda vacía no prueba que el dato falte en la campaña.</p></div>';
    return `<div class="toolbar"><span class="count">${list.length} ${list.length===1?'resultado':'resultados'}</span>${list.length?`<span>Mostrando ${start+1}–${Math.min(start+size,list.length)}</span>`:''}</div><div class="${render===entityCard?'grid':'list'}">${list.length?list.slice(start,start+size).map(f=>render(f)).join(''):empty}</div>${count>1?`<nav class="pagination" aria-label="Paginación"><button class="secondary-button" data-page="${state.page-1}" ${state.page===1?'disabled':''}>← Anterior</button><span>Página ${state.page} de ${count}</span><button class="secondary-button" data-page="${state.page+1}" ${state.page===count?'disabled':''}>Siguiente →</button></nav>`:''}`;
  }
  function homeActions() {
    return `<div class="hero-actions"><a class="primary-button" href="#capitulos">Abrir las crónicas <span aria-hidden="true">→</span></a><a class="secondary-button" href="#misterios">Seguir los misterios</a></div>`;
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
    content.innerHTML=campaignHero()+homeStats()+progress+homeShortcuts()+latestStory+`<nav class="hero-actions archive-actions" aria-label="Consultar el archivo"><a class="secondary-button" href="#metodo">${sections.metodo}</a><a class="secondary-button" href="#campanas">Elegir campaña</a></nav>`;
  }
  function chapterList() {
    heading(sections.capitulos,campaign.name+' · Sesión a sesión');
    const terms=fold(state.chapterQuery).trim().split(/\s+/).filter(Boolean);
    const list=data.chapters.filter(c=>terms.every(term=>fold(c.capitulo+' '+c.titulo).includes(term)));
    const gap=data.catalog?.capitulos_ausentes||[];
    content.innerHTML=`<div class="section-head"><div><p class="eyebrow">${esc(campaign.name)} · Sesión a sesión</p><h1>${sections.capitulos}</h1><p>${data.chapters.length} vídeos catalogados · ${reviewedCount} capítulos revisados.</p></div></div>${gap.length?`<p class="notice">El capítulo ${gap.join(', ')} no figura en la lista consultada. Conservamos la numeración original, sin rellenar ese hueco.</p>`:''}<div class="filters"><label>Buscar un capítulo<input id="chapter-search" type="search" value="${esc(state.chapterQuery)}" placeholder="Número o título…"></label></div><div class="grid chapter-grid">${list.map(c=>`<a class="card chapter-card" href="#capitulo/${c.capitulo}"><span class="card-crest" aria-hidden="true">${String(c.capitulo).padStart(2,'0')}</span><span class="card-tag">${chapterName(c.capitulo)}${c.duracion?' · '+clock(c.duracion):''}</span><h2 class="card-title">${esc(c.titulo)}</h2><p class="card-copy">${esc(c.resumen?short(c.resumen,190):c.transcripcion_disponible?'Transcripción incorporada. Lectura y relato pendientes.':'Vídeo localizado. Transcripción y relato pendientes.')}</p><div class="card-meta"><span>${c.registros.length} registros</span><span>${c.estado==='revisado'?'Revisado':'Pendiente de revisión'} ${icons.arrow}</span></div></a>`).join('')||'<div class="empty">No hay capítulos que coincidan con esta búsqueda.</div>'}</div>`;
  }
  function chapterView(n) {
    const c=chapters.get(n); if(!c)return missing();
    heading(c.titulo,chapterName(n));
    const tabs={relato:'Relato de la sesión',hechos:'Acontecimientos',misiones:'Misiones',preguntas:'Preguntas de la sesión',transcripcion:'Transcripción'};
    let body;
    if(state.tab==='relato')body=c.history?narrativeHistory(c.history,{kind:'capitulo',title:'Relato de la sesión',kicker:chapterName(n)+' · De principio a fin'}):`<p class="chapter-summary">${esc(c.resumen||'Revisión editorial pendiente.')}</p>`;
    else if(state.tab==='hechos')body='<div class="list">'+(c.registros.map(id=>event(facts.get(id),true)).join('') || '<div class="empty">Aún no hay ficha revisada de este episodio.</div>')+'</div>';
    else if(state.tab==='transcripcion')body=transcriptView(n);
    else if(state.tab==='preguntas')body=`<p class="archive-note">Preguntas planteadas en esta sesión, cotejadas con los capítulos posteriores. El estado corresponde al último capítulo revisado en cada entrada.</p><div class="list">${(c.seguimiento||[]).map(questionCard).join('')}</div>`;
    else body=`<div class="document"><p class="limitations">${state.tab==='preguntas'?'Estas preguntas describen lo desconocido en este capítulo. Consulta los misterios actuales para ver respuestas posteriores.':'Información y cautelas conservadas en la revisión del capítulo.'}</p><ul>${(c[state.tab] || []).map(line=>`<li>${inline(line)}</li>`).join('') || '<li>Sin entradas en esta sección.</li>'}</ul></div>`;
    const sourceNotes=[...(c.nombres||[]),...(c.contradicciones||[])];
    const notes=sourceNotes.length?`<details class="context-details"><summary>Notas sobre las fuentes de este capítulo</summary><div class="document"><ul>${sourceNotes.map(text=>`<li>${inline(text)}</li>`).join('')}</ul></div></details>`:'';
    content.innerHTML=`<div class="section-head"><div><p class="eyebrow">${chapterName(n)} · ${c.registros.length} registros</p><h1>${esc(c.titulo)}</h1></div><a class="secondary-button" href="${esc(c.url)}" target="_blank" rel="noopener noreferrer">Abrir episodio ↗</a></div><nav class="detail-tabs" aria-label="Secciones del capítulo">${Object.entries(tabs).map(([key,label])=>`<button data-tab="${key}" class="${state.tab===key?'active':''}" aria-pressed="${state.tab===key}">${label}</button>`).join('')}</nav>${body}${notes}<nav class="chapter-nav">${chapters.has(n-1)?`<a href="#capitulo/${n-1}">← ${chapterName(n-1)}</a>`:'<span></span>'}<a href="#capitulos">Volver a las crónicas</a>${chapters.has(n+1)?`<a href="#capitulo/${n+1}">${chapterName(n+1)} →</a>`:'<span></span>'}</nav>`;
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
    content.innerHTML=`<div class="section-head"><a class="secondary-button" href="#capitulo/${f.capitulo}">← ${chapterName(f.capitulo)}</a><button class="secondary-button" data-copy="${esc(f.id)}">Copiar referencia</button></div>${event(f,true)}<details class="context-details"><summary>Leer contexto de la transcripción</summary>${context}</details><p class="archive-note">Fuente automática · ${esc(f.ambito || 'Ámbito sin determinar')} · Intervalo de contexto ${clock(f.inicio)}–${clock(f.fin)}. La cita se localiza en ${clock(f.evidencia_cue?.inicio || f.inicio)}; comprobar su interpretación en el contexto.</p>`;
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
    content.innerHTML=`<div class="section-head"><div><p class="eyebrow">Del planteamiento a la última evidencia</p><h1>${sections.misterios}</h1><p>${all.length} preguntas históricas · ${counts.resuelta||0} resueltas · ${counts.parcial||0} parciales · ${counts.pendiente||0} pendientes${counts.sin_revisar?` · ${counts.sin_revisar} sin revisar`:''}</p></div></div><p class="section-description">Cada pregunta conserva su contexto original y se enlaza con respuestas posteriores. Una nueva pista no cierra por sí sola un misterio. ${data.seguimiento.por_actualizar?`${data.seguimiento.por_actualizar} entradas necesitan cotejar los capítulos nuevos.`:`Cotejo completo hasta el capítulo ${data.seguimiento.ultimo_capitulo}.`}</p><div class="filters"><label>Buscar una pregunta o respuesta<input id="question-search" type="search" value="${esc(state.questionQuery)}" placeholder="Nombre, asunto o referencia…"></label><label>Estado<select class="filter-select" data-filter="questionStatus"><option value="">Todos los estados</option>${Object.entries(questionStates).map(([key,label])=>`<option value="${key}" ${state.questionStatus===key?'selected':''}>${label}</option>`).join('')}</select></label></div>${paginated(list,questionCard,20)}<details class="context-details"><summary>Síntesis de las tramas principales</summary><article class="document">${markdown(documentText(data.documents.misterios,sections.misterios))}</article></details>`;
  }
  function entityList(type) {
    const category=categories[type];
    if(!reviewedCount)return pendingSection(category.title,'Las fichas de '+category.title.toLowerCase()+' de '+campaign.name+' se redactarán con sus historias y evidencias tras revisar las transcripciones.');
    heading(category.title,'Enciclopedia · '+category.title);
    const terms=fold(state.entityQuery).trim().split(/\s+/).filter(Boolean);
    const list=data.entities.filter(e=>e.type===type&&terms.every(t=>fold(e.name+' '+e.aliases.join(' ')).includes(t)));
    const doc=data.documents[category.document];
    const overview=doc?`<details class="context-details"><summary>${esc(category.overview)}</summary><article class="document">${markdown(documentText(doc,category.title))}</article></details>`:'';
    content.innerHTML=`<div class="section-head"><div><p class="eyebrow">${esc(campaign.name)} · Enciclopedia</p><h1>${category.title}</h1><p>${category.copy}</p></div></div><div class="filters"><label>${category.search}<input id="entity-search" type="search" value="${esc(state.entityQuery)}" placeholder="Nombre o variante…"></label></div>${paginated(list,entityCard,36)}${overview}`;
  }
  function entityView(name) {
    const e=entities.get(name)||entityAliases.get(name); if(!e)return missing();
    const category=categories[e.type];
    heading(e.name,'Enciclopedia · '+category.title);
    const refs=e.references.map(id=>facts.has(id)?`<a href="#registro/${id}">${id}</a>`:`<a href="#capitulo/${Number(id)}">${chapterName(Number(id))}</a>`).join(' · ');
    content.innerHTML=`<a class="source-link" href="#${category.route}">← Volver a ${category.title.toLowerCase()}</a><div class="section-head"><div><p class="eyebrow">${entityType(e.name)} · ${e.facts.length} registros</p><h1>${esc(e.name)}</h1></div></div>${e.description?`<p class="${e.history?'entity-intro':'chapter-summary'}">${esc(e.description)}</p>`:''}${e.history?entityHistory(e):''}${e.note?`<details class="context-details"><summary>Identificación y referencias</summary><div class="document"><p>${esc(e.note)}</p><p>${refs}</p></div></details>`:''}${e.history?'<div class="section-head"><div><p class="eyebrow">Los acontecimientos que sostienen el relato</p><h2>Registros y evidencias</h2></div></div>':''}${paginated(e.facts.map(id=>facts.get(id)),f=>event(f,true),25)}`;
  }
  function entityHistory(e) {
    const titles={personaje:'Historia',lugar:'Historia y acontecimientos',faccion:'Intereses y evolución',objeto:'Origen y recorrido'};
    return narrativeHistory(e.history,{kind:e.type,title:titles[e.type],kicker:'Hasta el capítulo '+e.history.revisado_hasta});
  }
  function narrativeHistory(history,{kind,title,kicker}) {
    return `<section class="character-story narrative-story" data-story-kind="${esc(kind)}" aria-labelledby="narrative-story-title"><header class="story-heading"><div class="story-emblem" aria-hidden="true">${crest(kind==='capitulo'?'objeto':kind)}</div><div><p class="eyebrow">${esc(kicker)}</p><h2 id="narrative-story-title">${esc(title)}</h2></div></header><div class="story-stages">${history.etapas.map((stage,index)=>`<article class="story-stage"><div class="story-step" aria-hidden="true">${String(index+1).padStart(2,'0')}</div><div class="story-prose"><h3>${esc(stage.titulo)}</h3><p>${esc(stage.texto)}</p><nav class="story-sources" aria-label="Fuentes de ${esc(stage.titulo)}"><span>Fuentes</span>${stage.referencias.map(id=>{const f=facts.get(id);return `<a href="#registro/${id}" title="${esc(f.titulo)}">${id} <span>· ${clock(f.evidencia_cue?.inicio||f.inicio)}</span></a>`;}).join('')}</nav></div></article>`).join('')}</div></section>`;
  }
  function listing(query='') {
    if(!reviewedCount)return pendingSection(query?'Buscar en '+campaign.name:sections.cronologia,'Todavía no hay acontecimientos revisados de '+campaign.name+'. Puedes buscar por número o título en su catálogo de capítulos.');
    const results=matched(query,state.chapter,state.kind);
    heading(query?'Resultados de búsqueda':sections.cronologia,query?'Búsqueda · '+query:'Campaña · Capítulo y minuto');
    document.getElementById('search-status').textContent=query?`${results.length} resultados para ${query}`:'';
    content.innerHTML=`<div class="section-head"><div><p class="eyebrow">El archivo, con sus evidencias</p><h1>${query?`Resultados para «${esc(query)}»`:sections.cronologia}</h1><p>${query?'Se buscan todos los términos, ignorando acentos, en registros y equivalencias documentadas.':'Orden de capítulos y minutos del vídeo. No equivale a un calendario interno entre los grupos de la campaña.'}</p></div></div>${filters()}${paginated(results)}`;
  }
  function targetLink(raw,label) {
    if(/^https:\/\//i.test(raw))return `<a href="${esc(raw)}" target="_blank" rel="noopener noreferrer">${label}</a>`;
    const match=raw.match(/(?:^|\/)capitulos\/(\d+)\.(?:md|json)/);
    if(match){ const ids=(label.match(/\b\d{2}-\d{3}\b/g)||[]).filter(id=>facts.has(id)); return `<a href="${ids.length===1?'#registro/'+ids[0]:'#capitulo/'+Number(match[1])}">${label}</a>`; }
    const doc=Object.entries(data.documents).find(([key])=>raw.toUpperCase().includes(({atlas:'ATLAS',facciones:'FACCIONES',misterios:'MISTERIOS',misiones:'MISIONES',contradicciones:'CONTRADICCIONES',relaciones:'RELACIONES',nombres:'NOMBRES',metodo:'METODO'}[key])+'.MD'));
    return doc?`<a href="#${doc[0]}">${label}</a>`:label;
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
    const doc=data.documents[key];if(!doc)return !reviewedCount?pendingSection({misiones:'Misiones',relaciones:'Relaciones',metodo:'Fuentes y método'}[key]||'Archivo de '+campaign.name):missing();
    const title=sections[key]||doc.title;
    heading(title,'Enciclopedia · '+title);
    content.innerHTML='<article class="document">'+markdown(documentText(doc,title))+'</article>';
  }
  function missing(){heading('No se encontró la entrada');content.innerHTML='<div class="empty"><h1>Esta entrada no está en el archivo.</h1><p>Vuelve al índice o busca otra grafía.</p><a class="primary-button" href="#inicio">Ir al inicio</a></div>';}
  function current(){const parts=location.hash.slice(1).split('/');let value='';try{value=decodeURIComponent(parts.slice(1).join('/'));}catch{}return [parts[0]||(archive.world&&!Object.hasOwn(campaignMetadata,requestedCampaign)?'campanas':'inicio'),value];}
  function render(reset=false) {
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
    if(route!=='busqueda'){document.getElementById('search-status').textContent='';if(reset)searchInput.value='';}
    if(reset){state.page=1;state.tab='relato';state.chapterQuery='';state.entityQuery='';state.questionQuery='';state.questionStatus='';state.transcriptQuery='';state.transcriptLimit=120;}
    const selectedEntity=route==='entidad'?(entities.get(arg)||entityAliases.get(arg)):null;
    document.querySelectorAll('#sidebar a[href^="#"]').forEach(a=>{const active=a.hash==='#'+route || (route==='capitulo'&&a.hash==='#capitulos')||(route==='pregunta'&&a.hash==='#misterios')||(selectedEntity&&a.hash==='#'+categories[selectedEntity.type].route);a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
    document.getElementById('sidebar').classList.remove('open');document.getElementById('menu-toggle')?.setAttribute('aria-expanded','false');
    const category=Object.entries(categories).find(([,value])=>value.route===route);
    if(route==='campanas')worldHome();else if(route==='inicio')home();else if(route==='capitulos')chapterList();else if(route==='capitulo')chapterView(Number(arg));else if(route==='registro')recordView(arg);else if(route==='pregunta')questionView(arg);else if(route==='misterios')questionList();else if(category)entityList(category[0]);else if(route==='entidad')entityView(arg);else if(route==='cronologia')listing();else if(route==='busqueda'){searchInput.value=arg;listing(arg);}else documentView(route);
    document.getElementById('search-clear').hidden=!searchInput.value;
  }
  content.addEventListener('click',async eventObject=>{
    const button=eventObject.target.closest('button');if(!button)return;
    if(button.dataset.page){state.page=Number(button.dataset.page);render();content.scrollIntoView({block:'start'});}
    if(button.dataset.tab){state.tab=button.dataset.tab;state.transcriptLimit=120;render();}
    if(button.hasAttribute('data-reset')){state.chapter='';state.kind='';state.page=1;render();}
    if(button.hasAttribute('data-transcript-more')){state.transcriptLimit+=200;const scrollY=window.scrollY;render();window.scrollTo(0,scrollY);}
    if(button.dataset.transcriptRetry){transcriptErrors.delete(button.dataset.transcriptRetry);render();}
    if(button.dataset.copy){const f=facts.get(button.dataset.copy);const text=`Arghast · ${campaign.name} · ${f.titulo} · ${chapterName(f.capitulo)} · ${clock(f.evidencia_cue?.inicio || f.inicio)} · ${f.id}\n${f.afirmacion}\nCita: ${f.cita}\n${sourceURL(f)}`;try{if(navigator.clipboard?.writeText)await navigator.clipboard.writeText(text);else{const area=document.createElement('textarea');area.value=text;document.body.append(area);area.select();document.execCommand('copy');area.remove();}button.textContent='Referencia copiada';}catch{button.textContent='Selecciona y copia la cita';} }
  });
  content.addEventListener('change',eventObject=>{const key=eventObject.target.dataset.filter;if(key){state[key]=eventObject.target.value;state.page=1;render();}});
  content.addEventListener('input',eventObject=>{const input=eventObject.target;const field={'chapter-search':'chapterQuery','entity-search':'entityQuery','transcript-search':'transcriptQuery','question-search':'questionQuery'}[input.id];if(field){const selection=input.selectionStart,scroll=window.scrollY;state[field]=input.value;state.page=1;state.transcriptLimit=120;render();const restored=document.getElementById(input.id);restored.focus();restored.setSelectionRange(selection,selection);window.scrollTo(0,scroll);}});
  searchInput.addEventListener('input',()=>{clearTimeout(searchTimer);searchTimer=setTimeout(()=>{state.page=1;state.chapter='';state.kind='';const q=searchInput.value.trim();history.replaceState(null,'',q?'#busqueda/'+encodeURIComponent(q):'#inicio');render();},180);});
  document.getElementById('search-clear').addEventListener('click',()=>{clearTimeout(searchTimer);searchInput.value='';location.hash='#inicio';render();searchInput.focus();});
  document.getElementById('menu-toggle')?.addEventListener('click',eventObject=>{const open=document.getElementById('sidebar').classList.toggle('open');eventObject.currentTarget.setAttribute('aria-expanded',String(open));});
  document.getElementById('campaign-selector').addEventListener('change',eventObject=>{const id=eventObject.target.value;if(Object.hasOwn(campaignMetadata,id))location.assign(campaignURL(id));else location.hash='campanas';});
  document.addEventListener('keydown',eventObject=>{if((eventObject.ctrlKey||eventObject.metaKey)&&eventObject.key.toLowerCase()==='k'){eventObject.preventDefault();searchInput.focus();searchInput.select();}if(eventObject.key==='Escape'){document.getElementById('sidebar').classList.remove('open');document.getElementById('menu-toggle')?.setAttribute('aria-expanded','false');}});
  window.addEventListener('hashchange',()=>{render(true);window.scrollTo(0,0);});
  document.getElementById('app-stats').textContent=`${data.chapters.length} crónicas · ${data.facts.length} acontecimientos`;
  for(const [id,value] of [['count-chapters',data.chapters.length],['count-facts',data.facts.length],['count-entities',data.entities.length]])if(document.getElementById(id))document.getElementById(id).textContent=value;
  render();
})();
