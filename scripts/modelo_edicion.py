"""Modelo editable y validación de referencias, separado de las transcripciones."""
from copy import deepcopy
import re

COLLECTIONS = ('chapters', 'facts', 'entities', 'seguimiento', 'documents')


def editable(data):
    result = {k: deepcopy(data[k]) for k in COLLECTIONS}
    for chapter in result['chapters']:
        chapter['_source'] = str(chapter['capitulo'])
    return result


def validate(content, original):
    def require(ok, message):
        if not ok:
            raise ValueError(message)

    require(isinstance(content, dict) and set(content) == set(COLLECTIONS), 'Solo se puede guardar el contenido editorial; la transcripción está protegida.')
    for key in ('chapters', 'facts', 'entities'):
        require(isinstance(content[key], list), f'{key}: se espera una lista.')
    require(isinstance(content['seguimiento'], dict) and isinstance(content['seguimiento'].get('preguntas'), list), 'Falta la lista de misterios.')
    require(isinstance(content['documents'], dict), 'Los documentos deben ser un objeto.')
    # Validar los campos que utiliza el lector sin impedir añadir otros campos editoriales.
    required = {
        'chapters': {'capitulo':int,'id':str,'titulo':str,'url':str,'resumen':str,'estado':str,'registros':list,'misiones':list,'preguntas':list,'contradicciones':list,'nombres':list,'duracion':str},
        'facts': {'id':str,'titulo':str,'tipo':str,'afirmacion':str,'inicio':str,'fin':str,'cita':str,'entidades':list,'capitulo':int},
        'entities': {'name':str,'facts':list,'aliases':list,'type':str},
        'questions': {'id':str,'capitulo':int,'pregunta':str,'estado':str,'respuesta':str,'referencias':list,'pendiente':str,'revisado_hasta':int},
    }
    groups = {**{k:content[k] for k in ('chapters','facts','entities')}, 'questions':content['seguimiento']['preguntas']}
    for group, rows in groups.items():
        for row in rows:
            require(isinstance(row, dict), f'{group}: entrada no válida.')
            for field, kind in required[group].items():
                require(type(row.get(field)) is kind, f'{group}: {field} debe ser {kind.__name__}.')
    numbers = [c['capitulo'] for c in content['chapters']]
    ids = [f['id'] for f in content['facts']]
    names = [e['name'] for e in content['entities']]
    qids = [q['id'] for q in groups['questions']]
    for values, title in ((numbers,'capítulos'),(ids,'registros'),(names,'nombres'),(qids,'misterios')):
        require(len(values) == len(set(values)), f'Hay {title} duplicados.')
    require(all(n > 0 for n in numbers), 'La numeración de capítulos debe ser positiva.')
    require(all(re.fullmatch(r'[\w.:-]+', identity, flags=re.ASCII) for identity in ids + qids), 'Los identificadores solo admiten letras, números, puntos, guiones y dos puntos.')
    require(all(name.strip() for name in names), 'Los nombres no pueden estar vacíos.')
    source_keys = {c['_source'] for c in original['chapters']}
    assigned = [c.get('_source') for c in content['chapters'] if c.get('_source') is not None]
    require(all(isinstance(s,str) and s in source_keys for s in assigned) and len(assigned) == len(set(assigned)), 'La asociación con las transcripciones originales está protegida.')
    facts = set(ids)
    chapters = set(numbers)
    for row in content['facts'] + groups['questions']:
        require(row['capitulo'] in chapters, f'{row["id"]}: el capítulo no existe.')
    for fact in content['facts']:
        for field in ('entidades','etiquetas_originales'):
            require(isinstance(fact.get(field,[]),list) and all(isinstance(v,str) for v in fact.get(field,[])), f'{field}: se espera una lista de nombres.')
    def references(rows, label):
        require(isinstance(rows,list) and all(isinstance(r,str) and r in facts for r in rows), f'{label}: hay referencias a registros que no existen.')
    for entity in content['entities']:
        require(entity['type'] in ('personaje','lugar','faccion','objeto'), 'Tipo de ficha desconocido.')
        require(all(isinstance(a,str) for a in entity['aliases']), 'Los alias deben ser textos.')
        references(entity['facts'], entity['name'])
        references(entity.get('references', []), entity['name'])
    for chapter in content['chapters']:
        references(chapter['registros'], chapter['titulo'])
        url = chapter['url']
        require((not url or url.startswith(('https://','http://'))) and not re.search(r'[<>"\x27\s]', url), 'El enlace del episodio debe ser HTTP o HTTPS y no contener espacios ni comillas.')
    for row in content['chapters'] + content['entities']:
        history = row.get('history')
        if history is not None:
            require(isinstance(history,dict) and isinstance(history.get('etapas'),list), 'El relato debe contener una lista de etapas.')
            require(type(history.get('revisado_hasta',0)) is int, 'El horizonte del relato debe ser un número de capítulo.')
            history.setdefault('revisado_hasta',0)
            for stage in history['etapas']:
                require(isinstance(stage,dict) and isinstance(stage.get('titulo'),str) and isinstance(stage.get('texto'),str), 'Cada etapa necesita título y texto.')
                references(stage.get('referencias', []), 'Etapa')
                stage.setdefault('referencias',[])
    for question in groups['questions']:
        require(question['estado'] in ('resuelta','parcial','pendiente','sin_revisar'), 'Estado de misterio desconocido.')
        references(question['referencias'], question['id'])
        references(question.get('referencias_origen', []), question['id'])
    for identity,doc in content['documents'].items():
        require(re.fullmatch(r'[\w.:-]+', identity, flags=re.ASCII), 'El identificador del documento contiene caracteres no permitidos.')
        require(isinstance(doc,dict) and isinstance(doc.get('title'),str) and isinstance(doc.get('text'),str), 'Cada documento necesita título y contenido.')
    # Los índices y cifras se recalculan tras cambios de estructura.
    for chapter in content['chapters']:
        chapter['registros'] = [f['id'] for f in content['facts'] if f['capitulo'] == chapter['capitulo']]
        chapter['seguimiento'] = [q for q in groups['questions'] if q['capitulo'] == chapter['capitulo']]
    content['seguimiento']['estados'] = {s:sum(q['estado']==s for q in groups['questions']) for s in ('resuelta','parcial','pendiente','sin_revisar')}
    content['seguimiento']['por_actualizar'] = sum(bool(q.get('requiere_actualizacion')) for q in groups['questions'])
    return content
