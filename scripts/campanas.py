"""Archivos independientes de Arghast; nunca infiere canon desde títulos."""
import hashlib
from collections import defaultdict
from pathlib import Path

from construir import ROOT, read_json, parse_vtt, validate_fact, seconds

KUROTO = ROOT / 'campanas/kuroto'


def mission_text(mission):
    """Conserva la redacción y las fuentes de entregas editoriales estructuradas."""
    if isinstance(mission, str):
        return mission
    if not isinstance(mission, dict) or any(not isinstance(mission.get(key), str) or not mission[key].strip()
                                          for key in ('titulo', 'estado', 'descripcion')):
        raise ValueError('Misión sin título, estado o descripción editorial')
    references = mission.get('referencias', [])
    if not isinstance(references, list) or any(not isinstance(reference, str) for reference in references):
        raise ValueError('Referencias de misión incorrectas')
    text = f'{mission["titulo"]}: {mission["descripcion"]} Estado: {mission["estado"]}.'
    if references:
        text += ' Fuentes: ' + ', '.join(references) + '.'
    return text


def validate_story(history, facts, label, chapter=None):
    if not history or type(history.get('revisado_hasta')) is not int or history['revisado_hasta'] < 1:
        raise ValueError('Historia sin horizonte de revisión: ' + label)
    if chapter is not None and history['revisado_hasta'] != chapter:
        raise ValueError('Horizonte de relato distinto de su sesión: ' + label)
    if not isinstance(history.get('etapas'), list) or not history['etapas']:
        raise ValueError('Historia sin etapas: ' + label)
    for stage in history['etapas']:
        if any(not isinstance(stage.get(key), str) or not stage[key].strip() for key in ('titulo', 'texto')):
            raise ValueError('Etapa sin título o texto: ' + label)
        references = stage.get('referencias')
        if not isinstance(references, list) or not references:
            raise ValueError('Etapa sin referencias: ' + label)
        for reference in references:
            if reference not in facts:
                raise ValueError('Historia con evidencia inexistente: ' + label)
            number = facts[reference]['capitulo']
            if number > history['revisado_hasta']:
                raise ValueError('Historia con evidencia posterior a su revisión: ' + label)
            if chapter is not None and number != chapter:
                raise ValueError('Relato con evidencia de otra sesión: ' + label)


def build_kuroto(folder=KUROTO):
    catalog = read_json(folder / 'catalogo.json')
    numbers = [episode['capitulo'] for episode in catalog['episodios']]
    ids = [episode['id'] for episode in catalog['episodios']]
    if len(numbers) != len(set(numbers)) or len(ids) != len(set(ids)):
        raise ValueError('Catálogo de Kuroto con capítulos o vídeos duplicados')
    chapters, facts, transcripts = [], [], {}
    checked_path = folder / 'fuentes/verificaciones_subtitulos.json'
    checked = read_json(checked_path) if checked_path.exists() else {}
    local_path = folder / 'fuentes/transcripciones_locales.json'
    local_sources = read_json(local_path) if local_path.exists() else {}
    integration_path = folder / 'revision/integracion.json'
    integrated = set(read_json(integration_path)['capitulos_integrados']) if integration_path.exists() else None
    aliases_path = folder / 'revision/identidades_confirmadas.json'
    aliases = read_json(aliases_path) if aliases_path.exists() else {}

    def canonical(name):
        seen = set()
        while name in aliases:
            if name in seen:
                raise ValueError('Ciclo de identidades de Kuroto: ' + name)
            seen.add(name)
            name = aliases[name]
        return name
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
        dossier = read_json(path) if path.exists() and (integrated is None or number in integrated) else {}
        if dossier and (not source or dossier.get('fuente_sha256') != hashlib.sha256(source.read_bytes()).hexdigest()):
            raise ValueError(f'Ficha de Kuroto sin fuente original validada: {number}')
        chapter = {**episode, 'estado': dossier.get('estado_revision', 'pendiente'),
                   'resumen': dossier.get('resumen', ''), 'registros': [],
                   'misiones': [mission_text(mission) for mission in dossier.get('misiones', [])],
                   'misiones_editoriales': dossier.get('misiones', []), 'preguntas': dossier.get('preguntas', []),
                   'contradicciones': dossier.get('contradicciones', []),
                   'nombres': dossier.get('nombres_dudosos', []), 'seguimiento': [],
                   'history': dossier.get('historia'), 'transcripcion_disponible': bool(segments),
                   'comprobacion_subtitulos': checked.get(str(number)),
                   'fuente_transcripcion': local_sources.get(str(number)) if source and '.es-local.' in source.name else None,
                   'duracion': segments[-1]['fin'] if segments else ''}
        for original in sorted(dossier.get('afirmaciones', []), key=lambda item: seconds(item['inicio'])):
            validate_fact(original, source)
            fact = {**original, 'capitulo': number,
                    'etiquetas_originales': original.get('entidades', []),
                    'entidades': list(dict.fromkeys(canonical(name) for name in original.get('entidades', [])))}
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
                                  ('nombres', 'Nombres y cautelas de Kuroto', 'NOMBRES.md'),
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
        for mission in chapter['misiones_editoriales']:
            if isinstance(mission, dict) and any(reference not in by_id or by_id[reference]['capitulo'] != chapter['capitulo']
                                                for reference in mission.get('referencias', [])):
                raise ValueError('Misión con referencia ajena a su sesión: ' + str(chapter['capitulo']))
        chapter['seguimiento'] = [question for question in tracking['preguntas'] if question['capitulo'] == chapter['capitulo']]
        if chapter['estado'] == 'revisado' or chapter.get('history'):
            validate_story(chapter.get('history'), by_id, str(chapter['capitulo']), chapter=chapter['capitulo'])
            if ' '.join(stage['texto'] for stage in chapter['history']['etapas']) != chapter['resumen']:
                raise ValueError('El relato no conserva el resumen de Kuroto: ' + str(chapter['capitulo']))
    for entity in entities:
        for reference in entity['references']:
            if reference not in by_id:
                raise ValueError('Entidad de Kuroto con referencia ajena')
        validate_story(entity.get('history'), by_id, entity['name'])
    if folder.resolve() == KUROTO.resolve():
        from fechas_emision import attach_dates
        attach_dates('kuroto', chapters)
    from rol_escrito import load_written_role
    written_role = load_written_role('kuroto', chapters) if folder.resolve() == KUROTO.resolve() else {'scenes': [], 'stats': {}}
    return {'chapters': chapters, 'facts': facts, 'entities': entities, 'writtenRole': written_role,
            'transcripts': transcripts, 'documents': documents, 'seguimiento': tracking,
            'revision': read_json(integration_path) if integration_path.exists() else None,
            'catalog': {key: value for key, value in catalog.items() if key != 'episodios'}}


def build_world(xoltacan):
    metadata = {
        'xoltacan': {'id': 'xoltacan', 'name': 'Xoltacan', 'tagline': 'Entre la selva y el mar',
                     'setting': 'Isla selvática', 'description': 'Piratas, pueblos ocultos y ruinas entre la selva y el mar.'},
        'kuroto': {'id': 'kuroto', 'name': 'Kuroto', 'tagline': 'Tras el velo de los yokai',
                   'setting': 'Fantasía de inspiración japonesa',
                   'description': 'Cazadores, yokais y antiguos guardianes. Una isla entre pactos, sombras y la esperanza de convivir.',
                   'setting_source': 'https://lichpol.es/?p=57'}
    }
    # La raíz conserva el formato de Xoltacan para herramientas y enlaces anteriores.
    return {**xoltacan, 'world': 'Arghast', 'campaignMetadata': metadata,
            'campaigns': {'kuroto': build_kuroto()}}
