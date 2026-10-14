"""Carga historias editoriales y valida cobertura, fechas y referencias."""
from construir import ROOT, read_json


def load_histories(character_names, facts, paths=None, collection='personajes'):
    paths = paths if paths is not None else [
        ROOT / 'config/historias_personajes.json',
        ROOT / 'config/historias_personajes_complementarias.json',
    ]
    names = set(character_names)
    result = {}
    for path in paths:
        document = read_json(path)
        until = document['revisado_hasta']
        if type(until) is not int or until < 1:
            raise ValueError(f'Horizonte de revisión inválido: {path}')
        for name, stages in document[collection].items():
            if name in result:
                raise ValueError('Historia duplicada: ' + name)
            if name not in names:
                raise ValueError('Entidad sin identidad canónica: ' + name)
            if not isinstance(stages, list) or not stages:
                raise ValueError('Historia sin etapas: ' + name)
            for stage in stages:
                if any(not isinstance(stage.get(key), str) or not stage[key].strip()
                       for key in ('titulo', 'texto')):
                    raise ValueError('Historia sin título o texto: ' + name)
                references = stage.get('referencias')
                if not isinstance(references, list) or not references or any(not isinstance(ref, str) for ref in references):
                    raise ValueError('Etapa sin referencias válidas: ' + name)
                for reference in references:
                    if reference not in facts:
                        raise ValueError(f'Referencia inexistente en {name}: {reference}')
                    if facts[reference]['capitulo'] > until:
                        raise ValueError(f'Referencia posterior a la revisión de {name}: {reference}')
            result[name] = {'revisado_hasta': until, 'etapas': stages}
    missing = names - result.keys()
    if missing:
        raise ValueError('Faltan historias para: ' + ', '.join(sorted(missing)))
    return result


def load_entity_histories(entities, facts):
    """Cada categoría tiene prosa editorial propia y cobertura independiente."""
    result = load_histories(
        [entity['name'] for entity in entities if entity['type'] == 'personaje'], facts)
    for kind, filename in [('lugar', 'lugares'), ('faccion', 'facciones'), ('objeto', 'objetos')]:
        result.update(load_histories(
            [entity['name'] for entity in entities if entity['type'] == kind], facts,
            [ROOT / f'config/historias_{filename}.json'], collection='entidades'))
    return result


def load_chapter_histories(chapters, facts, path=None):
    """Presenta los resúmenes íntegros según divisiones editoriales explícitas."""
    document = read_json(path or ROOT / 'config/relatos_capitulos.json')
    by_number = {chapter['capitulo']: chapter for chapter in chapters}
    result = {}
    for key, divisions in document['capitulos'].items():
        number = int(key)
        if number not in by_number:
            raise ValueError(f'Relato de capítulo inexistente: {number}')
        chapter = by_number[number]
        summary = chapter['resumen']
        if not divisions or divisions[0][1] != '':
            raise ValueError(f'El relato debe empezar al principio del capítulo {number}')
        positions = [0]
        for title, beginning, references in divisions[1:]:
            if not beginning or summary.count(beginning) != 1:
                raise ValueError(f'Corte editorial ausente o ambiguo en capítulo {number}: {beginning}')
            position = summary.index(beginning)
            if position <= positions[-1] or not summary[:position].rstrip().endswith(('.', '!', '?')):
                raise ValueError(f'Corte fuera de orden o dentro de una frase en capítulo {number}')
            positions.append(position)
        positions.append(len(summary))
        stages = []
        for index, (title, beginning, references) in enumerate(divisions):
            text = summary[positions[index]:positions[index+1]].strip()
            if not title.strip() or not text or not references:
                raise ValueError(f'Parte incompleta del capítulo {number}')
            for reference in references:
                if reference not in facts or facts[reference]['capitulo'] != number:
                    raise ValueError(f'Fuente ajena o inexistente en capítulo {number}: {reference}')
            stages.append({'titulo': title, 'texto': text, 'referencias': references})
        if ' '.join(stage['texto'] for stage in stages) != summary:
            raise ValueError(f'El relato altera el resumen del capítulo {number}')
        result[number] = {'revisado_hasta': number, 'etapas': stages}
    missing = [chapter['capitulo'] for chapter in chapters
               if chapter['estado'] == 'revisado' and chapter['capitulo'] not in result]
    if missing:
        raise ValueError(f'Faltan relatos para capítulos revisados: {missing}')
    return result
