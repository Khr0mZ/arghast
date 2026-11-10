"""Conserva en el catálogo las identidades corregidas por jugadores en el editor."""
from copy import deepcopy
import json
from preparar import ROOT, FOLDER, read_json, save


def main():
    source = read_json(ROOT / '.local/capitulo47/editor_antes.json')
    mapping = read_json(FOLDER / 'identidades_contexto.json')['cambios']
    remote = {e['name']: e for e in source['content']['entities']}
    path = ROOT / 'campanas/xoltacan/config/entidades.json'
    document = read_json(path)
    for group in document['grupos']:
        before = group['nombre']
        if before not in mapping:
            continue
        after = mapping[before]
        group['nombre'] = after
        group['etiquetas'] = list(dict.fromkeys([*group['etiquetas'], before, *remote[after]['aliases']]))
        correction = f'Nombre confirmado por corrección de jugadores en el editor compartido (revisión {source["revision"]}): {after}.'
        if correction not in group['nota']:
            group['nota'] += ' ' + correction
        if before == 'Dragón de Erendriel':
            group['nota'] = f'El pequeño dragón que acompaña a Aerendriel conserva su identidad histórica. {correction}'
    tesara = next(g for g in document['grupos'] if g['nombre'] == 'Tesara Queen')
    tesara['etiquetas'] = list(dict.fromkeys([*tesara['etiquetas'], 'Tesa', 'Tessa', 'Tessara Quinn']))
    save(path, document)
    for filename, collection in [('historias_personajes.json', 'personajes'), ('historias_personajes_complementarias.json', 'personajes'),
                                  ('historias_lugares.json', 'entidades'), ('historias_facciones.json', 'entidades'), ('historias_objetos.json', 'entidades')]:
        path = ROOT / 'campanas/xoltacan/config' / filename
        document = read_json(path)
        document[collection] = {mapping.get(name, name): stages for name, stages in document[collection].items()}
        save(path, document)
    save(ROOT / 'campanas/xoltacan/revision/identidades_confirmadas_editor_20261110.json', dict(
        campana='xoltacan', origen='editor_compartido', revision=source['revision'],
        fuente=f'https://arghast-editor.ivan-osorio440384.chatgpt.site/api/editor/document/xoltacan?revision={source["revision"]}',
        nombres=mapping,
        criterio='Se conservan las identidades y etiquetas históricas, las citas literales y los originales; solo se adopta la grafía corregida por los jugadores.'))
    print(f'{len(mapping)} nombres corregidos conservados, con sus alias y relatos históricos.')


if __name__ == '__main__':
    main()
