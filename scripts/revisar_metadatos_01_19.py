"""Revisión literal de metadatos; no modifica evidencia ni afirmaciones."""
import json
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIELDS=('resumen','misiones','preguntas','contradicciones','nombres_dudosos')
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    rules=read(ROOT/'derivados/revision_estilo_01_19/metadatos.json')
    for n,pairs in rules.items():
        path=ROOT/'conocimiento/capitulos'/f'{n}.json'
        d=read(path); old=deepcopy(d)
        for field in FIELDS:
            if field not in d:continue
            values=d[field] if isinstance(d[field],list) else [d[field]]
            values=[v for v in values if not (n=='01' and field=='preguntas' and 'Madame Oghma' in v)]
            for a,b in pairs: values=[v.replace(a,b) for v in values]
            d[field]=values if isinstance(d[field],list) else values[0]
        assert {k:v for k,v in old.items() if k not in FIELDS}=={k:v for k,v in d.items() if k not in FIELDS}
        write(path,d)
        draftpath=ROOT/'borradores'/f'{n}.json'
        if draftpath.exists():
            draft=read(draftpath)
            for f in FIELDS:
                if f in draft:draft[f]=d[f]
            write(draftpath,draft)
        print(n,sum(old.get(k)!=d.get(k) for k in FIELDS))
if __name__=='__main__':main()
