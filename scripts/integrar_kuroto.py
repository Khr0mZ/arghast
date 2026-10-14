"""Integra entregas editoriales paralelas sin sobrescribir las fichas de los bloques.

La base conserva la revisión de 001–003. Los lotes aportan historias y seguimiento;
solo se aceptan capítulos con fuente, citas y relato validados. No publica nada.
"""
import argparse
import copy
from collections import Counter
import re

from construir import read_json, write_json, sha, validate_fact
from campanas import KUROTO, validate_story


def assemble(folder=KUROTO):
    revision = folder / 'revision'
    base_path = revision / 'base_003.json'
    if not base_path.exists():
        raise ValueError('Falta la instantánea editorial base_003.json; conservarla antes de integrar')
    base = read_json(base_path)
    entities = {}
    questions = {question['id']: copy.deepcopy(question) for question in base['preguntas']}
    reviewed = set(base['revisados'])
    alias_path = revision / 'identidades_confirmadas.json'
    aliases = read_json(alias_path) if alias_path.exists() else {}

    def canonical(name):
        seen = set()
        while name in aliases:
            if name in seen:
                raise ValueError('Ciclo de alias revisados: ' + name)
            seen.add(name)
            name = aliases[name]
        return name

    for original in base['entidades']:
        entity = copy.deepcopy(original)
        name = canonical(entity['nombre'])
        if name in entities:
            raise ValueError('Dos identidades base necesitan conciliación editorial: ' + name)
        entity['etiquetas'] = list(dict.fromkeys([name, entity['nombre'], *entity.get('etiquetas', [])]))
        entity['nombre'] = name
        entities[name] = entity

    lots = []
    for path in sorted(revision.glob('lote_*.json')):
        match = re.fullmatch(r'lote_(\d+)_(\d+)\.json', path.name)
        if not match:
            raise ValueError('Nombre de lote no reconocido: ' + path.name)
        lower, upper = map(int, match.groups())
        lot = read_json(path)
        numbers = lot['revisados']
        if len(numbers) != len(set(numbers)) or any(type(number) is not int or not lower <= number <= upper for number in numbers):
            raise ValueError('Capítulos duplicados o ajenos al bloque: ' + path.name)
        if reviewed.intersection(numbers):
            raise ValueError('Dos bloques reclaman la misma revisión: ' + path.name)
        reviewed.update(numbers)
        lots.append((path.name, lot))
        for incoming in lot.get('entidades', []):
            incoming = copy.deepcopy(incoming)
            original_name = incoming['nombre']
            name = canonical(original_name)
            incoming['nombre'] = name
            incoming['etiquetas'] = list(dict.fromkeys([name, original_name, *incoming.get('etiquetas', [])]))
            if name not in entities:
                entities[name] = incoming
                continue
            current = entities[name]
            if current['tipo'] != incoming['tipo']:
                raise ValueError('Identidad con dos tipos incompatibles: ' + name)
            current['etiquetas'] = list(dict.fromkeys([*current.get('etiquetas', [name]), *incoming['etiquetas']]))
            current['referencias'] = list(dict.fromkeys([*current.get('referencias', []), *incoming.get('referencias', [])]))
            for stage in incoming.get('historia', {}).get('etapas', []):
                if stage not in current['historia']['etapas']:
                    current['historia']['etapas'].append(stage)
            current['historia']['revisado_hasta'] = max(current['historia']['revisado_hasta'], incoming['historia']['revisado_hasta'])
            # Las descripciones y cautelas iniciales no se sustituyen tácitamente.
            note = incoming.get('nota', '').strip()
            if note and note not in current.get('nota', ''):
                current['nota'] = (current.get('nota', '')+' '+note).strip()
        for question in lot.get('preguntas', []):
            if question['id'] in questions:
                raise ValueError('Pregunta duplicada entre bloques: ' + question['id'])
            questions[question['id']] = copy.deepcopy(question)

    catalog = {episode['capitulo']: episode for episode in read_json(folder / 'catalogo.json')['episodios']}
    facts = {}
    for number in sorted(reviewed):
        if number not in catalog:
            raise ValueError('Se ha revisado un capítulo ajeno al catálogo: ' + str(number))
        episode = catalog[number]
        sources = sorted((folder / 'fuentes').glob(f'{number:03d} - {episode["id"]}*.vtt'))
        source = next((path for path in sources if '.es-orig.' in path.name), sources[0] if sources else None)
        if not source:
            raise ValueError('Capítulo revisado sin fuente: ' + str(number))
        dossier = read_json(folder / 'conocimiento/capitulos' / f'{number:03d}.json')
        if dossier.get('estado_revision') != 'revisado' or dossier.get('fuente_sha256') != sha(source):
            raise ValueError('Revisión o hash de fuente inválido: ' + str(number))
        if dossier.get('capitulo') != number or not dossier.get('afirmaciones'):
            raise ValueError('Ficha sin evidencias o con número incorrecto: ' + str(number))
        for original in dossier['afirmaciones']:
            validate_fact(original, source)
            fact = {**original, 'capitulo': number, 'entidades': [canonical(name) for name in original['entidades']]}
            if not fact['id'].startswith(f'{number:02d}-') or fact['id'] in facts:
                raise ValueError('Identificador de evidencia incorrecto: ' + fact['id'])
            facts[fact['id']] = fact
        validate_story(dossier.get('historia'), facts, str(number), chapter=number)
        if ' '.join(stage['texto'] for stage in dossier['historia']['etapas']) != dossier['resumen']:
            raise ValueError('El relato altera el resumen del capítulo ' + str(number))
    unknown = {name for fact in facts.values() for name in fact['entidades']} - entities.keys()
    if unknown:
        raise ValueError('Entidades etiquetadas sin ficha: '+', '.join(sorted(unknown)))
    for name, entity in entities.items():
        if entity['tipo'] not in ('personaje', 'lugar', 'faccion', 'objeto'):
            raise ValueError('Tipo sin clasificar: ' + name)
        validate_story(entity.get('historia'), facts, name)
        entity['historia']['etapas'].sort(key=lambda stage: min(
            (facts[reference]['capitulo'], facts[reference]['inicio']) for reference in stage['referencias']))
    # Cada lector conserva sus cotejos; gana la revisión de mayor alcance.
    # Los cotejos finales de bloque precisan los apuntes previos de coordinación.
    applied = {}
    for corrections_path in sorted(revision.glob('cotejos_*.json'),
                                   key=lambda path: (path.name != 'cotejos_coordinacion.json', path.name)):
        for update in read_json(corrections_path):
            identifier = update['id']
            if identifier not in questions:
                raise ValueError('Cotejo de una pregunta inexistente: ' + identifier)
            if identifier in applied and update['revisado_hasta'] < applied[identifier]:
                continue
            questions[identifier].update({key: value for key, value in update.items() if key != 'id'})
            applied[identifier] = update['revisado_hasta']
    for question in questions.values():
        if question['estado'] not in ('pendiente', 'parcial', 'resuelta', 'sin_revisar'):
            raise ValueError('Estado de pregunta desconocido: ' + question['id'])
        if question['capitulo'] not in reviewed or not question['referencias'] or any(reference not in facts for reference in question['referencias']):
            raise ValueError('Seguimiento sin evidencia revisada: ' + question['id'])
        if question['revisado_hasta'] not in reviewed or any(facts[reference]['capitulo'] > question['revisado_hasta'] for reference in question['referencias']):
            raise ValueError('Pregunta con evidencia posterior al cotejo: ' + question['id'])
    pending = sorted(catalog.keys() - reviewed)
    through = 0
    for number in sorted(catalog):
        if number not in reviewed:
            break
        through = number
    tracking = {'preguntas': sorted(questions.values(), key=lambda item: (item['capitulo'], item['id'])),
                'estados': dict(Counter(question['estado'] for question in questions.values())),
                'por_actualizar': sum(question.get('requiere_actualizacion', True) for question in questions.values()),
                'ultimo_capitulo': max(reviewed, default=None), 'revision_continua_hasta': through,
                'capitulos_revisados': sorted(reviewed), 'capitulos_pendientes': pending}
    manifest = {'capitulos_integrados': sorted(reviewed), 'revision_continua_hasta': through,
                'capitulos_pendientes': pending, 'lotes': [name for name, _ in lots],
                'entidades': len(entities), 'evidencias': len(facts), 'preguntas': len(questions)}
    return list(entities.values()), tracking, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrar', action='store_true', help='Guardar la integración validada; sin este indicador solo comprueba')
    args = parser.parse_args()
    entities, tracking, manifest = assemble()
    if args.integrar:
        write_json(KUROTO / 'conocimiento/entidades.json', entities)
        write_json(KUROTO / 'conocimiento/seguimiento.json', tracking)
        write_json(KUROTO / 'revision/integracion.json', manifest)
    print(f'{len(manifest["capitulos_integrados"])} capítulos, {manifest["evidencias"]} evidencias, '
          f'{len(entities)} entidades, {manifest["preguntas"]} preguntas; '
          f'revisión continua hasta {manifest["revision_continua_hasta"]}. '
          + ('Integrado en local.' if args.integrar else 'Comprobado sin escribir.'))


if __name__ == '__main__':
    main()
