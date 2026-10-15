/* Validación del mismo documento editorial que admite el servicio local. */
export function validate(content, sources) {
  const object = v => v !== null && typeof v === 'object' && !Array.isArray(v);
  const require = (ok, message) => { if (!ok) throw new Error(message); };
  const types = {text:v=>typeof v==='string',number:Number.isSafeInteger,list:Array.isArray};
  const collections = ['chapters','facts','entities','seguimiento','documents'];
  require(object(content) && Object.keys(content).length===collections.length && collections.every(k=>Object.hasOwn(content,k)), 'Solo se puede guardar el contenido editorial; la transcripción está protegida.');
  for (const key of ['chapters','facts','entities']) require(Array.isArray(content[key]), `${key}: se espera una lista.`);
  require(object(content.seguimiento) && Array.isArray(content.seguimiento.preguntas), 'Falta la lista de misterios.');
  require(object(content.documents), 'Los documentos deben ser un objeto.');
  const required = {
    chapters:{capitulo:'number',id:'text',titulo:'text',url:'text',resumen:'text',estado:'text',registros:'list',misiones:'list',preguntas:'list',contradicciones:'list',nombres:'list',duracion:'text'},
    facts:{id:'text',titulo:'text',tipo:'text',afirmacion:'text',inicio:'text',fin:'text',cita:'text',entidades:'list',capitulo:'number'},
    entities:{name:'text',facts:'list',aliases:'list',type:'text'},
    questions:{id:'text',capitulo:'number',pregunta:'text',estado:'text',respuesta:'text',referencias:'list',pendiente:'text',revisado_hasta:'number'}
  };
  const groups={chapters:content.chapters,facts:content.facts,entities:content.entities,questions:content.seguimiento.preguntas};
  for(const [key,rows] of Object.entries(groups)) for(const row of rows){
    require(object(row), `${key}: entrada no válida.`);
    for(const [field,type] of Object.entries(required[key])) require(types[type](row[field]),`${key}: ${field} no es válido.`);
  }
  const numbers=content.chapters.map(c=>c.capitulo), ids=content.facts.map(f=>f.id), names=content.entities.map(e=>e.name), qids=groups.questions.map(q=>q.id);
  for(const values of [numbers,ids,names,qids]) require(values.length===new Set(values).size,'Hay entradas duplicadas.');
  require(numbers.every(n=>n>0),'La numeración de capítulos debe ser positiva.');
  require([...ids,...qids].every(id=>/^[\w.:-]+$/.test(id)),'Identificador no válido.');
  require(names.every(n=>n.trim()),'Los nombres no pueden estar vacíos.');
  const assigned=content.chapters.filter(c=>c._source!=null).map(c=>c._source);
  require(assigned.every(s=>typeof s==='string' && sources.includes(s)) && new Set(assigned).size===assigned.length,'La asociación con las transcripciones originales está protegida.');
  const facts=new Set(ids), chapters=new Set(numbers);
  const references=(rows,label)=>require(Array.isArray(rows) && rows.every(r=>typeof r==='string' && facts.has(r)),`${label}: hay referencias a registros que no existen.`);
  for(const row of [...content.facts,...groups.questions]) require(chapters.has(row.capitulo),`${row.id}: el capítulo no existe.`);
  for(const fact of content.facts) for(const field of ['entidades','etiquetas_originales']) require(Array.isArray(fact[field]??[]) && (fact[field]??[]).every(v=>typeof v==='string'),`${field}: se espera una lista de nombres.`);
  for(const entity of content.entities){
    require(['personaje','lugar','faccion','objeto'].includes(entity.type),'Tipo de ficha desconocido.');
    require(entity.aliases.every(a=>typeof a==='string'),'Los alias deben ser textos.');
    references(entity.facts,entity.name); references(entity.references??[],entity.name);
  }
  for(const chapter of content.chapters){
    references(chapter.registros,chapter.titulo);
    require((!chapter.url || /^https?:\/\//.test(chapter.url)) && !/[<>"'\s]/.test(chapter.url),'El enlace del episodio debe ser HTTP o HTTPS y no contener espacios ni comillas.');
  }
  for(const row of [...content.chapters,...content.entities]) if(row.history!=null){
    const history=row.history;
    require(object(history) && Array.isArray(history.etapas),'El relato debe contener una lista de etapas.');
    require(Number.isSafeInteger(history.revisado_hasta??0),'El horizonte del relato debe ser un número de capítulo.');
    history.revisado_hasta??=0;
    for(const stage of history.etapas){
      require(object(stage) && typeof stage.titulo==='string' && typeof stage.texto==='string','Cada etapa necesita título y texto.');
      references(stage.referencias??[],'Etapa'); stage.referencias??=[];
    }
  }
  for(const question of groups.questions){
    require(['resuelta','parcial','pendiente','sin_revisar'].includes(question.estado),'Estado de misterio desconocido.');
    references(question.referencias,question.id); references(question.referencias_origen??[],question.id);
  }
  for(const [identity,doc] of Object.entries(content.documents)){
    require(/^[\w.:-]+$/.test(identity),'Identificador del documento no válido.');
    require(object(doc) && typeof doc.title==='string' && typeof doc.text==='string','Cada documento necesita título y contenido.');
  }
  const byChapter=new Map(numbers.map(n=>[n,[]])), questionsByChapter=new Map(numbers.map(n=>[n,[]]));
  for(const fact of content.facts) byChapter.get(fact.capitulo).push(fact.id);
  for(const question of groups.questions) questionsByChapter.get(question.capitulo).push(question);
  for(const chapter of content.chapters){chapter.registros=byChapter.get(chapter.capitulo);chapter.seguimiento=questionsByChapter.get(chapter.capitulo);}
  content.seguimiento.estados=Object.fromEntries(['resuelta','parcial','pendiente','sin_revisar'].map(s=>[s,groups.questions.filter(q=>q.estado===s).length]));
  content.seguimiento.por_actualizar=groups.questions.filter(q=>q.requiere_actualizacion).length;
  return content;
}
