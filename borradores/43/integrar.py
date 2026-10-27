"""Integra las tres lecturas completas del capítulo 43 y su continuidad editorial."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import read_json, sha, validate_fact, seconds
from preparar import save

FOLDER = ROOT / 'borradores/43'
SOURCE = ROOT / 'xoltacan_subtitulos/subtitulos/43 - tSdmoZCWEZQ.es-orig.vtt'
ALIASES = {
    'Caja musical de Citlali': 'Caja de música de Citlali',
    'Altar de los s?mbolos de Citlali': 'Altar de los símbolos de Citlali',
}
SHARED = {'Bonnie': '42-012', 'Gobs': '42-006', 'Armin': '42-006', 'Moneda pirata de Bonnie': '42-012'}


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
    mapping = {fact['id']: f'43-{i:03d}' for i, fact in enumerate(originals, 1)}
    assert len(mapping) == len(originals)

    def remap(value, context=''):
        if isinstance(value, dict):
            return {key: remap(child, key) for key, child in value.items()}
        if isinstance(value, list):
            return [remap(child, context) for child in value]
        if isinstance(value, str):
            if context in ('nombre', 'entidades'):
                value = ALIASES.get(value, value)
            return re.sub(r'\b43-\d{3}\b', lambda m: mapping[m[0]], value)
        return value

    deliveries = remap(deliveries)
    def polish(value):
        if isinstance(value, list):
            return [polish(v) for v in value]
        if isinstance(value, dict):
            return {k: v if k in ('cita', 'evidencia_cue') else polish(v) for k, v in value.items()}
        if isinstance(value, str):
            for before, after in [
                ('el impacto de su respuesta comienza en el tramo posterior.', 'prepara su respuesta de fuego.'),
                ('La escudera prepara una respuesta de fuego que aún no se resuelve en este primer tramo.', 'La escudera prepara una respuesta de fuego.'),
                ('La resistencia continúa y el bloque no muestra todavía el desenlace del frente.', 'La resistencia aún continúa.'),
                ('El bloque termina cuando el director le pide representar el lanzamiento.', 'El director le pide representar el lanzamiento.'),
                ('el bloque había seguido a Molly', 'la escena venía siguiendo a Molly'),
                ('este tramo no narra', 'este viaje no narra'),
                ('sin explicar en este repaso.', 'sin explicar.'),
            ]:
                value = value.replace(before, after)
        return value
    deliveries = polish(deliveries)
    editorial = remap(read_json(FOLDER / 'edicion_integrada.json'))
    stages = [stage for d in deliveries for stage in d['etapas']]
    stages[0]['titulo'] = 'Los dos frentes de la defensa de Shiaru'
    stages[0]['texto'] = stages[0]['texto'].replace(
        'La protección explicada en la mesa durará ocho horas y puede evitar que caiga a cero.',
        'La protección durará ocho horas y puede mantenerla en pie cuando sus fuerzas se agoten.')
    stages[2]['texto'] = stages[2]['texto'].replace(
        'La kender confirma el alcance de su bola de fuego y elige el lugar del lanzamiento; su resultado queda en el tramo siguiente.',
        'La kender confirma el alcance de su bola de fuego y elige el lugar del lanzamiento.')
    stages[6]['texto'] = stages[6]['texto'].replace('El impacto todavía no se muestra en este tramo.', 'Ambas quedan preparadas para el descenso.')
    facts = sorted([f for d in deliveries for f in d['afirmaciones']], key=lambda f: f['id'])
    by_id = {f['id']: f for f in facts}
    by_id['43-019']['limitacion'] = 'La plegaria prepara el lanzamiento; el impacto de la bola de fuego se narra en 43-023. No se reconstruye un discurso completo de las escrituras de Eleanor.'
    by_id['43-022']['limitacion'] = 'El impacto de esa bola de fuego se documenta en 43-023. No se calcula un censo de bajas a partir de los tokens.'
    by_id['43-042']['limitacion'] = 'La propuesta se resuelve durante el descenso y el impacto de 43-043 y 43-048. Es una resolución particular de la mesa, sin establecer reglas generales.'
    by_id['43-061']['limitacion'] = 'El duelo por Nox y la memoria de Amaru se enlazan expresamente mediante sus trenzas, ron, chistes y el contraste entre niño y hombre: Citlali reconoce al hijo perdido en Nox. No se cuenta cómo salió del cofre ni se reconstruye su crianza. Varado es la descripción visual desde la jungla, sin una inspección del casco o prueba de otro naufragio. La corrección de Kuroto a Xoltacan al cerrar no traslada la escena a otra campaña.'
    dossier = dict(capitulo=43, estado_revision='revisado', fuente_sha256=sha(SOURCE),
                   resumen=' '.join(s['texto'] for s in stages), afirmaciones=facts,
                   **{key: editorial[key] for key in ('misiones', 'preguntas', 'contradicciones', 'nombres_dudosos')})
    for fact in facts:
        validate_fact(fact, SOURCE)
    save(ROOT / 'conocimiento/capitulos/43.json', dossier)
    chapter_stages = read_json(ROOT / 'config/relatos_capitulos.json')
    chapter_stages['capitulos']['43'] = [[s['titulo'], '' if i == 0 else s['texto'].split('. ')[0] + '. ', s['referencias']]
                                       for i, s in enumerate(stages)]
    save(ROOT / 'config/relatos_capitulos.json', chapter_stages)

    catalog = read_json(ROOT / 'config/entidades.json')
    groups = {g['nombre']: g for g in catalog['grupos']}
    history_files = [('historias_personajes.json', 'personajes'), ('historias_personajes_complementarias.json', 'personajes'),
                     ('historias_lugares.json', 'entidades'), ('historias_facciones.json', 'entidades'), ('historias_objetos.json', 'entidades')]
    histories, history_for = {}, {}
    for filename, collection in history_files:
        doc = read_json(ROOT / 'config' / filename)
        doc['revisado_hasta'] = 43
        for name, entries in doc[collection].items():
            # La repetición de la plaza se cita dentro de su etapa previa, no como otra partida de la flota.
            for stage in entries:
                stage['referencias'] = [r for r in stage['referencias'] if not r.startswith('43-')]
            doc[collection][name] = [s for s in entries if s['referencias']]
            history_for[name] = filename
        histories[filename] = (doc, collection)
    default_files = {'personaje': 'historias_personajes_complementarias.json', 'lugar': 'historias_lugares.json',
                     'faccion': 'historias_facciones.json', 'objeto': 'historias_objetos.json'}
    proposals = [e for d in deliveries for e in d['historias_entidades']]
    for proposal in proposals:
        name, kind, new_stages = proposal['nombre'], proposal['tipo'], proposal['etapas']
        if name not in groups:
            group = dict(nombre=name, tipo=kind, etiquetas=[name], descripcion=proposal['descripcion'],
                         nota=proposal['nota'], referencias=[])
            catalog['grupos'].append(group)
            groups[name] = group
        group = groups[name]
        group['referencias'] = list(dict.fromkeys(group.get('referencias', []) + [r for s in new_stages for r in s['referencias']]))
        filename = history_for.setdefault(name, default_files[kind])
        doc, collection = histories[filename]
        target = doc[collection].setdefault(name, [])
        if name in SHARED:
            stage = next(s for s in target if SHARED[name] in s['referencias'])
            stage['referencias'] = list(dict.fromkeys(stage['referencias'] + [r for s in new_stages for r in s['referencias']]))
        else:
            for stage in new_stages:
                if stage not in target:
                    if name in ('Shiaru', 'Marina', 'El Garfio') and not stage['texto'].lower().startswith('en paralelo'):
                        stage = {**stage, 'texto': 'En paralelo al frente naval de la misma batalla, ' + stage['texto'][0].lower() + stage['texto'][1:]}
                    target.append(stage)
    for group in editorial.get('catalogo', []):
        groups[group['nombre']].update(group)
    save(ROOT / 'config/entidades.json', catalog)
    for filename, (doc, _) in histories.items():
        save(ROOT / 'config' / filename, doc)

    reviewed_ids = []
    for path in sorted((ROOT / 'config').glob('seguimiento_preguntas_*.json')):
        if path.name == 'seguimiento_preguntas_43.json':
            continue
        doc = read_json(path)
        doc['revisado_hasta'] = 43
        for question in doc['preguntas']:
            question.update(editorial['seguimiento_anterior'].get(question['id'], {}))
            question['revisado_hasta'] = 43
            reviewed_ids.append(question['id'])
        save(path, doc)
    assert len(reviewed_ids) == 253 and len(set(reviewed_ids)) == 253
    tracking = [dict(id=f'P43-{i:03d}', capitulo=43, indice=i, pregunta=q, estado='pendiente', revisado_hasta=43,
                     **editorial['seguimiento_nuevo'][i-1]) for i, q in enumerate(dossier['preguntas'], 1)]
    save(ROOT / 'config/seguimiento_preguntas_43.json', dict(version=1, revisado_hasta=43, preguntas=tracking))
    save(FOLDER / 'integracion.json', dict(mapa_referencias=mapping, preguntas_anteriores_cotejadas=reviewed_ids,
         preguntas_con_evidencia_nueva=list(editorial['seguimiento_anterior']), registros=len(facts), etapas=len(stages),
         palabras_relato=len(dossier['resumen'].split()), etapas_compartidas_actualizadas=SHARED))
    source_record = read_json(ROOT / 'config/fuente_xoltacan_43.json')
    source_record.update(lectura=f'Tres bloques completos sin solapamiento; {len(facts)} evidencias, {len(stages)} etapas y cotejo de las 253 preguntas anteriores. Audio no cotejado.',
                         integracion='borradores/43/integracion.json')
    save(ROOT / 'config/fuente_xoltacan_43.json', source_record)
    print(f'Capítulo 43: {len(facts)} evidencias, {len(stages)} etapas y {len(tracking)} preguntas nuevas.')


if __name__ == '__main__':
    main()
