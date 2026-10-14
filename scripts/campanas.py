"""Archivos independientes de Arghast; nunca infiere canon desde títulos."""
import hashlib
from collections import defaultdict
from pathlib import Path

from construir import ROOT, read_json, parse_vtt, validate_fact

KUROTO = ROOT / 'campanas/kuroto'


def build_kuroto(folder=KUROTO):
    catalog = read_json(folder / 'catalogo.json')
    numbers = [episode['capitulo'] for episode in catalog['episodios']]
    ids = [episode['id'] for episode in catalog['episodios']]
    if len(numbers) != len(set(numbers)) or len(ids) != len(set(ids)):
        raise ValueError('Catálogo de Kuroto con capítulos o vídeos duplicados')
    chapters, facts, transcripts = [], [], {}
    manifest_path = folder / 'fuentes/originales_sha256.json'
    inventory = read_json(manifest_path) if manifest_path.exists() else {}
    for relative, expected in inventory.items():
        source = (folder / relative).resolve()
        if not source.is_relative_to(folder.resolve()) or not source.is_file():
            raise ValueError('Fuente de Kuroto ausente o fuera de su archivo: ' + relative)
        if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
            raise ValueError('Fuente de Kuroto modificada: ' + relative)
    for episode in sorted(catalog['episodios'], key=lambda item: item['capitulo']):
        number = episode['capitulo']
        candidates = sorted((folder / 'fuentes').glob(f'{number:03d} - {episode["id"]}*.vtt'))
        source = next((path for path in candidates if '.es-orig.' in path.name), candidates[0] if candidates else None)
        if source and source.relative_to(folder).as_posix() not in inventory:
            raise ValueError('Ejecuta importar_kuroto.py --preparar para registrar el original: ' + str(source))
        segments = parse_vtt(source) if source else []
        transcripts[str(number)] = [[segment['inicio'], segment['texto_original']] for segment in segments]
        path = folder / 'conocimiento/capitulos' / f'{number:03d}.json'
        dossier = read_json(path) if path.exists() else {}
        if dossier and (not source or dossier.get('fuente_sha256') != hashlib.sha256(source.read_bytes()).hexdigest()):
            raise ValueError(f'Ficha de Kuroto sin fuente original validada: {number}')
        chapter = {**episode, 'estado': dossier.get('estado_revision', 'pendiente'),
                   'resumen': dossier.get('resumen', ''), 'registros': [],
                   'misiones': dossier.get('misiones', []), 'preguntas': dossier.get('preguntas', []),
                   'contradicciones': dossier.get('contradicciones', []),
                   'nombres': dossier.get('nombres_dudosos', []), 'seguimiento': [],
                   'history': dossier.get('historia'), 'transcripcion_disponible': bool(segments),
                   'duracion': segments[-1]['fin'] if segments else ''}
        for original in dossier.get('afirmaciones', []):
            validate_fact(original, source)
            fact = {**original, 'capitulo': number,
                    'etiquetas_originales': original.get('entidades', [])}
            if not fact['id'].startswith(f'{number:02d}-'):
                raise ValueError('Identificador de evidencia ajeno al capítulo de Kuroto')
            facts.append(fact)
            chapter['registros'].append(fact['id'])
        chapters.append(chapter)
    by_id = {fact['id']: fact for fact in facts}
    if len(by_id) != len(facts):
        raise ValueError('Identificadores de evidencia duplicados en Kuroto')
    entity_path = folder / 'conocimiento/entidades.json'
    entities, memberships = [], defaultdict(list)
    for fact in facts:
        for name in set(fact['entidades']):
            memberships[name].append(fact['id'])
    for entity in read_json(entity_path) if entity_path.exists() else []:
        if entity['tipo'] not in ('personaje', 'lugar', 'faccion', 'objeto'):
            raise ValueError('Tipo de entidad de Kuroto sin revisar')
        entities.append({'name': entity['nombre'], 'type': entity['tipo'],
                         'description': entity['descripcion'], 'aliases': entity.get('etiquetas', [entity['nombre']]),
                         'note': entity.get('nota', ''), 'references': entity.get('referencias', []),
                         'facts': memberships[entity['nombre']], 'history': entity.get('historia')})
    if len({entity['name'] for entity in entities}) != len(entities):
        raise ValueError('Identidad duplicada en el catálogo de Kuroto')
    unknown = set(memberships) - {entity['name'] for entity in entities}
    if unknown:
        raise ValueError('Entidades de Kuroto pendientes de clasificación: ' + ', '.join(sorted(unknown)))
    documents = {}
    for key, title, filename in [('metodo', 'Fuentes y método de Kuroto', 'METODO.md'),
                                  ('misiones', 'Misiones de Kuroto', 'MISIONES.md'),
                                  ('relaciones', 'Relaciones de Kuroto', 'RELACIONES.md'),
                                  ('atlas', 'Lugares de Kuroto', 'ATLAS.md'),
                                  ('facciones', 'Facciones de Kuroto', 'FACCIONES.md'),
                                  ('misterios', 'Misterios de Kuroto', 'MISTERIOS.md')]:
        path = folder / 'conocimiento' / filename
        if path.exists():
            documents[key] = {'title': title, 'text': path.read_text(encoding='utf-8')}
    tracking_path = folder / 'conocimiento/seguimiento.json'
    tracking = read_json(tracking_path) if tracking_path.exists() else {
        'preguntas': [], 'estados': {}, 'por_actualizar': 0, 'ultimo_capitulo': None}
    for question in tracking['preguntas']:
        for reference in question['referencias']:
            if reference not in by_id:
                raise ValueError('Seguimiento de Kuroto con referencia ajena: ' + reference)
    for chapter in chapters:
        chapter['seguimiento'] = [question for question in tracking['preguntas'] if question['capitulo'] == chapter['capitulo']]
        for stage in (chapter.get('history') or {}).get('etapas', []):
            if any(reference not in chapter['registros'] for reference in stage['referencias']):
                raise ValueError('Relato de Kuroto con evidencia de otra sesión')
    for entity in entities:
        for reference in entity['references']:
            if reference not in by_id:
                raise ValueError('Entidad de Kuroto con referencia ajena')
        for stage in (entity.get('history') or {}).get('etapas', []):
            if any(reference not in by_id for reference in stage['referencias']):
                raise ValueError('Historia de Kuroto con referencia ajena')
    return {'chapters': chapters, 'facts': facts, 'entities': entities,
            'transcripts': transcripts, 'documents': documents, 'seguimiento': tracking,
            'catalog': {key: value for key, value in catalog.items() if key != 'episodios'}}


def build_world(xoltacan):
    metadata = {
        'xoltacan': {'id': 'xoltacan', 'name': 'Xoltacan', 'tagline': 'Entre la selva y el mar',
                     'setting': 'Isla selvática', 'description': 'Piratas, pueblos ocultos y ruinas entre la selva y el mar.'},
        'kuroto': {'id': 'kuroto', 'name': 'Kuroto', 'tagline': 'Tras el velo de los yokai',
                   'setting': 'Fantasía de inspiración japonesa',
                   'description': 'Otra campaña de Arghast, con una ambientación de inspiración japonesa.',
                   'setting_source': 'https://lichpol.es/?p=57'}
    }
    # La raíz conserva el formato de Xoltacan para herramientas y enlaces anteriores.
    return {**xoltacan, 'world': 'Arghast', 'campaignMetadata': metadata,
            'campaigns': {'kuroto': build_kuroto()}}
