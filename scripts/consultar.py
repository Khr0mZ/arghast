"""Búsqueda en la enciclopedia completa, con referencias y tipos de evidencia."""
import argparse
import json
import unicodedata
from construir import ROOT, KB, read_json, seconds


def folded(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text.casefold())
                   if unicodedata.category(c) != 'Mn')


def search(query='', character=None, chapter=None, kind=None):
    terms = folded(query).split()
    aliases = {}
    for group in read_json(ROOT / 'config/entidades.json')['grupos']:
        for label in group['etiquetas']:
            aliases[label] = ' '.join([group['nombre'], *group['etiquetas']])
    results = []
    for path in sorted((KB / 'capitulos').glob('*.json')):
        n = int(path.stem)
        if chapter is not None and n != chapter:
            continue
        for fact in read_json(path).get('afirmaciones', []):
            if kind and fact['tipo'] != kind:
                continue
            if character and not any(folded(character) in folded(name) for name in fact.get('conocedores', [])):
                continue
            haystack = folded(' '.join([fact['titulo'], fact['afirmacion'], fact.get('limitacion', ''),
                                        *[aliases.get(label, label) for label in fact.get('entidades', [])]]))
            if all(term in haystack for term in terms):
                results.append({'capitulo': n, **fact})
    return sorted(results, key=lambda fact: (fact['capitulo'], seconds(fact['inicio'])))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('consulta', nargs='?', default='', help='Todos los términos deben aparecer en el mismo registro; ignora acentos.')
    parser.add_argument('--personaje', help='Filtra destinatarios/testigos explícitos; listas vacías no prueban ignorancia.')
    parser.add_argument('--capitulo', type=int)
    parser.add_argument('--tipo', choices=['hecho_confirmado', 'declaracion_personaje', 'explicacion_director', 'especulacion_jugadores', 'desconocido'])
    parser.add_argument('--limite', type=int, default=20)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if args.limite <= 0:
        parser.error('--limite debe ser mayor que cero')
    results = search(args.consulta, args.personaje, args.capitulo, args.tipo)
    shown = results[:args.limite]
    if args.json:
        print(json.dumps({'total': len(results), 'mostrados': len(shown), 'resultados': shown}, ensure_ascii=False, indent=2))
        return
    print(f'{len(results)} registros encontrados; se muestran {len(shown)}. Enciclopedia completa.')
    if args.personaje:
        print('Filtro de testigos explícitos; ausencia de resultados no prueba ignorancia.')
    for fact in shown:
        print(f'\n{fact["id"]} | {fact["inicio"]} | {fact["tipo"]} | {fact["titulo"]}')
        print(fact['afirmacion'])
        print('Ficha: conocimiento/capitulos/' + f'{fact["capitulo"]:02d}.md')
        if fact.get('limitacion'):
            print('Límite: ' + fact['limitacion'])


if __name__ == '__main__':
    main()
