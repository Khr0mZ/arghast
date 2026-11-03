"""Integra las tres lecturas completas y el cotejo de continuidad del capítulo 45."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import read_json, sha, validate_fact, seconds
from preparar import save

FOLDER = ROOT / 'borradores/45'
SOURCE = ROOT / 'xoltacan_subtitulos/subtitulos/45 - 30qLJWABsPE.es-orig.vtt'


def main():
    split = read_json(FOLDER / 'reparto.json')
    assert sha(SOURCE) == split['sha256']
    deliveries = [read_json(FOLDER / f'entrega_{i}.json') for i in (1, 2, 3)]
    for block, delivery in zip(split['bloques'], deliveries):
        assert delivery['lectura_completa'] is True
        for key in ('primer_segmento', 'ultimo_segmento'):
            assert delivery[key] == block[key]
        for fact in delivery['afirmaciones']:
            validate_fact(fact, SOURCE)
    originals = sorted([f for d in deliveries for f in d['afirmaciones']], key=lambda f: (seconds(f['inicio']), f['id']))
    mapping = {fact['id']: f'45-{i:03d}' for i, fact in enumerate(originals, 1)}
    assert len(mapping) == len(originals)
    editorial = read_json(FOLDER / 'edicion_integrada.json')
    aliases = editorial.get('alias_entidades', {})

    def remap(value, context=''):
        if isinstance(value, dict):
            return {mapping.get(key, key): remap(child, key) for key, child in value.items()}
        if isinstance(value, list):
            return [remap(child, context) for child in value]
        if isinstance(value, str):
            if context in ('nombre', 'entidades'):
                value = aliases.get(value, value)
            return re.sub(r'\b45-\d{3}\b', lambda m: mapping[m[0]], value)
        return value

    deliveries = remap(deliveries)
    editorial = remap(editorial)
    facts = sorted([f for d in deliveries for f in d['afirmaciones']], key=lambda f: f['id'])
    for fact in facts:
        fact.update(editorial.get('ajustes_afirmaciones', {}).get(fact['id'], {}))
        validate_fact(fact, SOURCE)
    stages = editorial.get('etapas') or [stage for d in deliveries for stage in d['etapas']]
    dossier = dict(capitulo=45, estado_revision='revisado', fuente_sha256=sha(SOURCE),
        resumen=' '.join(s['texto'] for s in stages), afirmaciones=facts,
        **{key:editorial[key] for key in ('misiones', 'preguntas', 'contradicciones', 'nombres_dudosos')})
    save(ROOT / 'conocimiento/capitulos/45.json', dossier)
    chapter_stages = read_json(ROOT / 'config/relatos_capitulos.json')
    chapter_stages['capitulos']['45'] = [[s['titulo'], '' if i == 0 else s['texto'].split('. ')[0] + '. ', s['referencias']]
        for i, s in enumerate(stages)]
    save(ROOT / 'config/relatos_capitulos.json', chapter_stages)
    catalog = read_json(ROOT / 'config/entidades.json')
    groups = {g['nombre']: g for g in catalog['grupos']}
    files = [('historias_personajes.json','personajes'), ('historias_personajes_complementarias.json','personajes'),
        ('historias_lugares.json','entidades'), ('historias_facciones.json','entidades'), ('historias_objetos.json','entidades')]
    histories, history_for = {}, {}
    for filename, collection in files:
        doc = read_json(ROOT / 'config' / filename)
        doc['revisado_hasta'] = 45
        for name, entries in doc[collection].items():
            for stage in entries:
                stage['referencias'] = [r for r in stage['referencias'] if not r.startswith('45-')]
            doc[collection][name] = [s for s in entries if s['referencias']]
            history_for[name] = filename
        histories[filename] = (doc, collection)
    defaults = {'personaje':'historias_personajes_complementarias.json','lugar':'historias_lugares.json',
        'faccion':'historias_facciones.json','objeto':'historias_objetos.json'}
    proposals = editorial.get('historias_entidades') or [e for d in deliveries for e in d['historias_entidades']]
    for proposal in proposals:
        name, kind, new_stages = proposal['nombre'], proposal['tipo'], proposal['etapas']
        if name not in groups:
            group = dict(nombre=name, tipo=kind, etiquetas=[name], descripcion=proposal['descripcion'],
                nota=proposal['nota'], referencias=[])
            catalog['grupos'].append(group)
            groups[name] = group
        group = groups[name]
        assert group['tipo'] == kind, (name,kind)
        group['referencias'] = list(dict.fromkeys(group.get('referencias',[]) + [r for s in new_stages for r in s['referencias']]))
        filename = history_for.setdefault(name, defaults[kind])
        doc, collection = histories[filename]
        target = doc[collection].setdefault(name, [])
        for stage in new_stages:
            if stage not in target:
                target.append(stage)
    for patch in editorial.get('catalogo', []):
        groups[patch['nombre']].update(patch)
    save(ROOT / 'config/entidades.json', catalog)
    for filename, (doc, _) in histories.items():
        save(ROOT / 'config' / filename, doc)
    reviewed_ids = []
    for path in sorted((ROOT / 'config').glob('seguimiento_preguntas_*.json')):
        if path.name == 'seguimiento_preguntas_45.json':
            continue
        doc = read_json(path)
        doc['revisado_hasta'] = 45
        for question in doc['preguntas']:
            question.update(editorial['seguimiento_anterior'].get(question['id'], {}))
            question['revisado_hasta'] = 45
            reviewed_ids.append(question['id'])
        save(path, doc)
    assert len(reviewed_ids) == 267 and len(set(reviewed_ids)) == 267
    tracking = [dict(id=f'P45-{i:03d}', capitulo=45, indice=i, pregunta=q, estado='pendiente', revisado_hasta=45,
        **editorial['seguimiento_nuevo'][i-1]) for i, q in enumerate(dossier['preguntas'], 1)]
    assert len(tracking) == len(editorial['seguimiento_nuevo'])
    save(ROOT / 'config/seguimiento_preguntas_45.json', dict(version=1, revisado_hasta=45, preguntas=tracking))
    save(FOLDER / 'integracion.json', dict(mapa_referencias=mapping, preguntas_anteriores_cotejadas=reviewed_ids,
        preguntas_con_evidencia_nueva=list(editorial['seguimiento_anterior']), registros=len(facts), etapas=len(stages),
        palabras_relato=len(dossier['resumen'].split())))
    source = read_json(ROOT / 'config/fuente_xoltacan_45.json')
    source.update(lectura=f'Tres bloques completos sin solapamiento; {len(facts)} evidencias, {len(stages)} etapas y cotejo de las 267 preguntas anteriores. Audio no cotejado.',
        integracion='borradores/45/integracion.json')
    if (FOLDER / 'cotejo_rol.json').exists():
        source['cotejo_rol'] = 'borradores/45/cotejo_rol.json'
    save(ROOT / 'config/fuente_xoltacan_45.json', source)
    print(f'Capítulo 45: {len(facts)} evidencias, {len(stages)} etapas y {len(tracking)} preguntas nuevas.')


if __name__ == '__main__':
    main()
