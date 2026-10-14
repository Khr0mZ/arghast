"""Aplica redacciones editoriales revisadas, sin modificar la evidencia."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITABLE = {'titulo', 'afirmacion', 'ambito', 'limitacion', 'nota_conocimiento'}
TOP = {'resumen', 'misiones', 'preguntas', 'contradicciones', 'nombres_dudosos'}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def protected(fact):
    return {k: v for k, v in fact.items() if k not in EDITABLE}


def main():
    patches = {}
    for path in sorted((ROOT / 'borradores').glob('revision_estilo_*.json')):
        for key, value in read(path).items():
            if 20 <= int(key) <= 29:
                patches[key] = value
    counts = []
    for key, patch in sorted(patches.items()):
        n = int(key)
        path = ROOT / f'conocimiento/capitulos/{n:02}.json'
        draft_path = ROOT / f'borradores/{n:02}.json'
        chapter, draft = read(path), read(draft_path)
        before = read(path)
        for field in TOP:
            if field in patch:
                chapter[field] = patch[field]
                draft[field] = patch[field]
        assert len(chapter['afirmaciones']) == len(draft['registros'])
        for fact, row in zip(chapter['afirmaciones'], draft['registros']):
            if fact['id'] not in patch['afirmaciones']:
                continue
            statement, limit = patch['afirmaciones'][fact['id']]
            fact['afirmacion'], fact['limitacion'] = statement, limit
            row[4] = statement
            if len(row) > 10:
                row[10] = limit
            elif limit:
                row.append(limit)
        assert chapter['fuente_sha256'] == before['fuente_sha256']
        assert [protected(a) for a in chapter['afirmaciones']] == [protected(a) for a in before['afirmaciones']]
        assert set(patch['afirmaciones']) == {a['id'] for a in chapter['afirmaciones']}
        write(path, chapter)
        write(draft_path, draft)
        counts.append((n, len(chapter['afirmaciones'])))
        print(f'{n:02}: {len(chapter["afirmaciones"])} afirmaciones; evidencia intacta')
    text = '# Revisión del estilo editorial: capítulos 20–29\n\n'
    text += 'Se revisaron íntegramente los campos editoriales de los capítulos indicados. Las redacciones se conservan también en los borradores para reproducir la generación.\n\n'
    text += '| Capítulo | Afirmaciones revisadas |\n|---|---:|\n'
    text += ''.join(f'| {n:02} | {count} |\n' for n, count in counts)
    text += f'\nTotal: {sum(c for _, c in counts)} afirmaciones.\n\n'
    text += 'Validación: los IDs, tipos, citas, evidencias VTT, tiempos, entidades, conocedores, estados de conocimiento, confianza y SHA de fuente son idénticos antes y después de aplicar cada revisión. No se altera la certeza ni se añaden hechos.\n\n'
    text += 'Ejemplos: «Naór saca Axi por tobillo hacia cubierto» pasa a «Naór saca a Axi por el tobillo y lo pone a cubierto». «Mosca no dragón» se expresa como «La montura es una mosca, no un dragón». Las citas conservan su texto literal.\n'
    (ROOT / 'conocimiento/revision_estilo_20_29.md').write_text(text, encoding='utf-8')


if __name__ == '__main__':
    main()
