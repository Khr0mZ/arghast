"""Aplica únicamente cambios editoriales revisados y comprueba la evidencia."""
import json
from pathlib import Path
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'derivados/revision_estilo_01_19'
FOLDER.mkdir(parents=True, exist_ok=True)
EDITABLE = {'resumen', 'titulo', 'afirmacion', 'ambito', 'limitacion', 'nota_conocimiento',
            'misiones', 'preguntas', 'contradicciones', 'nombres_dudosos'}

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def write(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def apply():
    changes = read(FOLDER / 'cambios.json')
    baseline_path = FOLDER / 'antes.json'
    if baseline_path.exists():
        baseline = read(baseline_path)
    else:
        baseline = {}
        for n in range(1, 20):
            for directory in ('conocimiento/capitulos', 'borradores'):
                p = ROOT / directory / f'{n:02d}.json'
                if p.exists():
                    baseline[str(p.relative_to(ROOT)).replace('\\', '/')] = read(p)
        write(baseline_path, baseline)
    counts = {}
    for n in range(1, 20):
        key = f'conocimiento/capitulos/{n:02d}.json'
        old = baseline[key]
        result = deepcopy(old)
        section = changes.get(f'{n:02d}', {})
        literal_path = FOLDER / 'sustituciones.json'
        literal_rules = read(literal_path).get(f'{n:02d}', []) if literal_path.exists() else []
        for identifier, replacements in literal_rules:
            original = next(r for r in old['afirmaciones'] if r['id'] == identifier)
            value = original['afirmacion']
            for before, after in replacements:
                if before not in value:
                    raise ValueError(f'Sustitución editorial no localizada: {identifier} {before}')
                value = value.replace(before, after)
            section.setdefault('afirmaciones', {}).setdefault(identifier, {})['afirmacion'] = value
        for field, value in section.get('capitulo', {}).items():
            assert field in EDITABLE
            result[field] = value
        changed = 0
        for row in result['afirmaciones']:
            updates = section.get('afirmaciones', {}).get(row['id'], {})
            for field, value in updates.items():
                assert field in EDITABLE
                row[field] = value
            if updates:
                changed += 1
        for a, b in zip(old['afirmaciones'], result['afirmaciones']):
            assert {k:v for k,v in a.items() if k not in EDITABLE} == {k:v for k,v in b.items() if k not in EDITABLE}
        write(ROOT / key, result)
        draft_key = f'borradores/{n:02d}.json'
        if draft_key in baseline:
            draft = deepcopy(baseline[draft_key])
            for field, value in section.get('capitulo', {}).items():
                if field in draft:
                    draft[field] = value
            for source, edited in zip(old['afirmaciones'], result['afirmaciones']):
                for row in draft.get('registros', []):
                    if row[4] != source['afirmacion']:
                        continue
                    for index, field in ((2, 'titulo'), (4, 'afirmacion'), (7, 'ambito'), (10, 'limitacion')):
                        if field in edited and field in source and source[field] != edited[field]:
                            assert index < len(row)
                            row[index] = edited[field]
            for a,b in zip(baseline[draft_key]['registros'], draft['registros']):
                assert [v for i,v in enumerate(a) if i not in (2,4,7,10)] == [v for i,v in enumerate(b) if i not in (2,4,7,10)]
            write(ROOT / draft_key, draft)
        counts[f'{n:02d}'] = changed
    write(FOLDER / 'resultado.json', counts)
    print(counts)

if __name__ == '__main__':
    raise SystemExit('Helper histórico deshabilitado: restauraría una instantánea anterior a la revisión final. Use scripts/aplicar_estilo.py con config/revision_estilo_01_19_final.json.')
