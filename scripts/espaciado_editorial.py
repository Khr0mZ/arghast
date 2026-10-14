"""Separa palabras y cifras pegadas en prosa editorial, sin tocar evidencias."""
import re
from construir import KB, ROOT, read_json, write_json
from aplicar_estilo import FIELDS, LISTS


def separate(text):
    # Minúsculas: conserva abreviaturas como D100 y CD65 e IDs como 31-027.
    return re.sub(r'(?<=[a-záéíóúñ])(?=\d)', ' ', text)


def main():
    recipe = {}
    for path in sorted((KB / 'capitulos').glob('*.json')):
        dossier = read_json(path)
        edits = {}
        for field in LISTS:
            value = dossier.get(field)
            if isinstance(value, str):
                revised = separate(value)
            elif isinstance(value, list):
                revised = [separate(item) for item in value]
            else:
                continue
            if revised != value:
                edits[field] = revised
        records = {}
        for fact in dossier['afirmaciones']:
            changed = {field: separate(fact[field]) for field in FIELDS
                       if isinstance(fact.get(field), str)
                       and separate(fact[field]) != fact[field]}
            if changed:
                records[fact['id']] = changed
        if records:
            edits['registros'] = records
        if edits:
            recipe[str(dossier['capitulo'])] = edits
    target = ROOT / 'config/revision_espaciado_editorial.json'
    write_json(target, recipe)
    print(f'Receta de espaciado: {len(recipe)} capítulos. Aplicar mediante aplicar_estilo.py.')


if __name__ == '__main__':
    main()
