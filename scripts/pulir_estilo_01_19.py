"""Segundo pase editorial literal; conserva todos los campos ajenos al cambio."""
from pathlib import Path
import json
from copy import deepcopy
ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'derivados/revision_estilo_01_19'
def read(path):
    return json.loads(path.read_text(encoding='utf-8'))
def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
def main():
    rules = read(FOLDER / 'segundo_pase.json')
    for chapter, pairs in rules.items():
        path = ROOT / 'conocimiento/capitulos' / f'{chapter}.json'
        data = read(path)
        old = deepcopy(data)
        draft_path = ROOT / 'borradores' / f'{chapter}.json'
        draft = read(draft_path) if draft_path.exists() else None
        for fact in data['afirmaciones']:
            before = fact['afirmacion']
            for source, target in pairs:
                fact['afirmacion'] = fact['afirmacion'].replace(source, target)
            if draft:
                for row in draft['registros']:
                    if row[4] == before:
                        row[4] = fact['afirmacion']
        assert [{k:v for k,v in r.items() if k!='afirmacion'} for r in old['afirmaciones']] == [{k:v for k,v in r.items() if k!='afirmacion'} for r in data['afirmaciones']]
        assert {k:v for k,v in old.items() if k!='afirmaciones'} == {k:v for k,v in data.items() if k!='afirmaciones'}
        write(path, data)
        if draft:
            write(draft_path, draft)
        print(chapter, sum(a['afirmacion']!=b['afirmacion'] for a,b in zip(old['afirmaciones'],data['afirmaciones'])))
if __name__=='__main__':
    main()
