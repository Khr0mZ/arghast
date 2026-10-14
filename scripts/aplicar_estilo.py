"""Aplica redacción editorial por ID sin cambiar campos de evidencia."""
import argparse
from construir import ROOT, read_json, write_json


FIELDS = {'titulo','afirmacion','ambito','limitacion','nota_conocimiento'}
LISTS = {'resumen','misiones','preguntas','contradicciones','nombres_dudosos'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('revision')
    args=parser.parse_args()
    changes=read_json(ROOT / args.revision)
    for number, edit in changes.items():
        n=int(number)
        path=ROOT / 'conocimiento/capitulos' / f'{n:02d}.json'
        original=read_json(path)
        before={fact['id']:{key:value for key,value in fact.items() if key not in FIELDS}
                for fact in original['afirmaciones']}
        for field in LISTS:
            if field in edit: original[field]=edit[field]
        by_id={fact['id']:fact for fact in original['afirmaciones']}
        for fid, updates in edit.get('registros',{}).items():
            if not set(updates)<=FIELDS:raise ValueError('Intento de alterar campo protegido: '+fid)
            by_id[fid].update(updates)
        after={fact['id']:{key:value for key,value in fact.items() if key not in FIELDS}
               for fact in original['afirmaciones']}
        if before!=after:raise ValueError('Evidencia alterada en capítulo '+number)
        draft_path=ROOT / 'borradores' / f'{n:02d}.json'
        if draft_path.exists():
            draft=read_json(draft_path)
            for field in LISTS:
                if field in edit:draft[field]=edit[field]
            for idx,row in enumerate(draft['registros'],1):
                fact=by_id[f'{n:02d}-{idx:03d}']
                row[2],row[4],row[7]=fact['titulo'],fact['afirmacion'],fact['ambito']
                if len(row)>10:row[10]=fact.get('limitacion','')
                elif fact.get('limitacion'):row.append(fact['limitacion'])
            write_json(draft_path,draft)
        write_json(path,original)
        print(f'{n:02d}: {len(edit.get("registros",{}))} registros revisados; evidencia preservada.')


if __name__=='__main__':main()
