"""Catálogo revisado de identidades; las etiquetas de extracción no crean fichas."""
import unicodedata
from construir import ROOT, read_json


TYPES = {'personaje', 'lugar', 'faccion', 'objeto'}


def key(text):
    return ' '.join(''.join(c for c in unicodedata.normalize('NFD', text.casefold())
                           if unicodedata.category(c) != 'Mn').split())


def load_catalog():
    configuration = read_json(ROOT / 'config/entidades.json')
    groups = configuration['grupos']
    aliases, notes, names = {}, {}, set()
    for group in groups:
        name = group['nombre']
        if key(name) in names:
            raise ValueError('Nombre canónico duplicado: ' + name)
        names.add(key(name))
        notes[name] = group
        for label in [name, *group['etiquetas']]:
            if label in aliases and aliases[label] != name:
                raise ValueError('Etiqueta asignada a identidades distintas: ' + label)
            aliases[label] = name
        if 'tipo' in group and group['tipo'] not in TYPES:
            raise ValueError('Tipo inválido en catálogo: ' + name)
    excluded = {item['etiqueta']: item.get('razon', '') for item in configuration.get('exclusiones', [])}
    return aliases, notes, excluded


def canonical_labels(labels, aliases):
    return sorted({aliases.get(label, label) for label in labels}, key=key)


def source_links(group, prefix=''):
    links = []
    for reference in group.get('referencias', []):
        chapter = reference.split('-')[0]
        label = reference if '-' in reference else 'cap. ' + chapter
        links.append(f'[{label}]({prefix}capitulos/{int(chapter):02d}.md)')
    return ', '.join(links)
