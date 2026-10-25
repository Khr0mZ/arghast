"""Integra las tres lecturas editoriales del capítulo 42, conservando su procedencia."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import read_json, write_json, sha, validate_fact, seconds

FOLDER = ROOT / 'borradores/42'
SOURCE = ROOT / 'xoltacan_subtitulos/subtitulos/42 - 3IUV_YN_zxM.es-orig.vtt'
ALIASES = {
    'Prisionero encadenado del Invictus': 'Pinky',
    'Almirante del Invictus': 'Tórtola',
    'Almirante palomo del Invictus': 'Tórtola',
    'Arrecife del Garfio': 'El Garfio',
    'Banana': 'Elger Banana',
}


def main():
    split = read_json(FOLDER / 'reparto.json')
    assert sha(SOURCE) == split['sha256']
    deliveries = [read_json(FOLDER / f'entrega_{i}.json') for i in (1, 2, 3)]
    for block, delivery in zip(split['bloques'], deliveries):
        assert delivery['lectura_completa'] is True
        assert delivery['primer_segmento'] == block['primer_segmento']
        assert delivery['ultimo_segmento'] == block['ultimo_segmento']
        for fact in delivery['afirmaciones']:
            validate_fact(fact, SOURCE)
    originals = sorted([f for d in deliveries for f in d['afirmaciones']],
                       key=lambda f: (seconds(f['inicio']), f['id']))
    mapping = {fact['id']: f'42-{i:03d}' for i, fact in enumerate(originals, 1)}
    assert len(mapping) == len(originals)

    def remap(value, context=''):
        if isinstance(value, dict):
            return {k: remap(v, k) for k, v in value.items()}
        if isinstance(value, list):
            return [remap(v, context) for v in value]
        if isinstance(value, str):
            if context in ('nombre', 'entidades'):
                value = ALIASES.get(value, value)
            return re.sub(r'\b42-\d{3}\b', lambda m: mapping[m[0]], value)
        return value

    deliveries = remap(deliveries)
    def polish(value):
        if isinstance(value, list):
            return [polish(v) for v in value]
        if isinstance(value, dict):
            return {k: v if k in ('cita', 'evidencia_cue') else polish(v) for k, v in value.items()}
        if isinstance(value, str):
            for old, new in [
                ('se la devuelve a Ione', 'se la entrega a Ione'),
                ('le devuelve la moneda', 'le entrega la moneda'),
                ('devuelve la moneda a Ione', 'entrega la moneda a Ione'),
                ('devolver Bonnie la moneda a Ione', 'entregar Bonnie la moneda a Ione'),
                ('devolución de la moneda', 'entrega de la moneda'),
            ]:
                value = value.replace(old, new)
        return value
    deliveries = polish(deliveries)
    facts = sorted([f for d in deliveries for f in d['afirmaciones']], key=lambda f: f['id'])
    stages = [s for d in deliveries for s in d['etapas']]
    editorial = remap(read_json(FOLDER / 'edicion_integrada.json'))
    dossier = dict(capitulo=42, estado_revision='revisado',
                   resumen=' '.join(s['texto'] for s in stages),
                   fuente_sha256=sha(SOURCE), afirmaciones=facts,
                   **{k: editorial[k] for k in ('misiones', 'preguntas', 'contradicciones', 'nombres_dudosos')})
    write_json(ROOT / 'conocimiento/capitulos/42.json', dossier)
    chapter_stages = read_json(ROOT / 'config/relatos_capitulos.json')
    chapter_stages['capitulos']['42'] = [[s['titulo'], '' if i == 0 else s['texto'].split('. ')[0] + '. ',
                                       s['referencias']] for i, s in enumerate(stages)]
    write_json(ROOT / 'config/relatos_capitulos.json', chapter_stages)

    catalog = read_json(ROOT / 'config/entidades.json')
    groups = {g['nombre']: g for g in catalog['grupos']}
    histories = {}
    for filename, collection in [('historias_personajes.json', 'personajes'),
                                 ('historias_personajes_complementarias.json', 'personajes'),
                                 ('historias_lugares.json', 'entidades'),
                                 ('historias_facciones.json', 'entidades'),
                                 ('historias_objetos.json', 'entidades')]:
        path = ROOT / 'config' / filename
        doc = read_json(path)
        for name, entries in doc[collection].items():
            doc[collection][name] = [s for s in entries if not any(r.startswith('42-') for r in s['referencias'])]
        doc['revisado_hasta'] = 42
        histories[filename] = (path, doc, collection)
    history_for = {}
    for filename, (_, doc, collection) in histories.items():
        for name in doc[collection]:
            history_for[name] = filename
    filenames = {'personaje': 'historias_personajes_complementarias.json',
                 'lugar': 'historias_lugares.json', 'faccion': 'historias_facciones.json',
                 'objeto': 'historias_objetos.json'}
    proposals = [e for d in deliveries for e in d['historias_entidades']]
    proposals += editorial.get('historias_entidades', [])
    for proposal in proposals:
        name = proposal['nombre']
        if name in editorial.get('omitir_historias', []):
            continue
        kind = proposal['tipo']
        entries = proposal['etapas']
        if name not in groups:
            group = dict(nombre=name, tipo=kind, etiquetas=[name],
                         descripcion=proposal['descripcion'], nota=proposal['nota'],
                         referencias=list(dict.fromkeys(r for s in entries for r in s['referencias'])))
            catalog['grupos'].append(group)
            groups[name] = group
        groups[name]['referencias'] = list(dict.fromkeys(groups[name].get('referencias', [])
            + [r for s in entries for r in s['referencias']]))
        filename = history_for.get(name, filenames[kind])
        history_for[name] = filename
        _, doc, collection = histories[filename]
        target = doc[collection].setdefault(name, [])
        for stage in entries:
            if stage not in target:
                target.append(stage)
    for group in editorial.get('catalogo', []):
        name = group['nombre']
        if name in groups:
            groups[name].update(group)
        else:
            catalog['grupos'].append(group)
            groups[name] = group
    write_json(ROOT / 'config/entidades.json', catalog)
    for path, doc, _ in histories.values():
        write_json(path, doc)

    reviewed_ids = []
    changes = editorial['seguimiento_anterior']
    for path in sorted((ROOT / 'config').glob('seguimiento_preguntas_*.json')):
        if path.name == 'seguimiento_preguntas_42.json':
            continue
        doc = read_json(path)
        doc['revisado_hasta'] = 42
        for q in doc['preguntas']:
            q.update(changes.get(q['id'], {}))
            q['revisado_hasta'] = 42
            reviewed_ids.append(q['id'])
        write_json(path, doc)
    assert len(reviewed_ids) == 246 and len(set(reviewed_ids)) == 246
    tracking = []
    for i, question in enumerate(dossier['preguntas'], 1):
        entry = dict(id=f'P42-{i:03d}', capitulo=42, indice=i, pregunta=question,
                     estado='pendiente', revisado_hasta=42, **editorial['seguimiento_nuevo'][i-1])
        tracking.append(entry)
    write_json(ROOT / 'config/seguimiento_preguntas_42.json',
               dict(version=1, revisado_hasta=42, preguntas=tracking))
    write_json(FOLDER / 'integracion.json', dict(mapa_referencias=mapping,
               preguntas_anteriores_cotejadas=reviewed_ids,
               preguntas_con_evidencia_nueva=list(changes), registros=len(facts),
               etapas=len(stages), palabras_relato=len(dossier['resumen'].split())))
    print(f'Capítulo 42: {len(facts)} registros; {len(stages)} etapas; {len(tracking)} preguntas nuevas.')


if __name__ == '__main__':
    main()
