"""Convierte una ficha editorial compacta en el esquema de evidencia validable.

Uso: python scripts/redactar.py borradores/02.json
Cada registro editorial: [inicio, fin, titulo, tipo, afirmacion, entidades,
fragmento_literal, ambito, conocedores, conocimiento_oghma, nota_opcional].
Los tiempos se expresan HH:MM:SS. La cita se toma de un cue literal que contenga
el fragmento dentro del intervalo; no se sintetiza ni normaliza.
"""
import argparse
import html
import json
import re
from construir import ROOT, TIMING, read_json, seconds, sha, write_json, validate_fact


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ficha')
    args = parser.parse_args()
    draft = read_json(ROOT / args.ficha)
    n = draft['capitulo']
    meta = read_json(ROOT / 'derivados' / f'{n:02d}' / 'meta.json')
    source = ROOT / meta['fuente']
    cues = []
    for block in re.split(r'\n{2,}', source.read_text(encoding='utf-8-sig').replace('\r\n', '\n')):
        match = TIMING.search(block)
        if match:
            payload = block.splitlines()[next(i for i, line in enumerate(block.splitlines()) if TIMING.search(line)) + 1:]
            text = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]*>', '', ' '.join(payload)))).strip()
            cues.append((match[1], match[2], text))
    facts = []
    for idx, row in enumerate(draft.pop('registros'), 1):
        start, end, title, kind, statement, entities, anchor, scope, knowers, oghma, *notes = row
        start += '.000' if '.' not in start else ''
        end += '.000' if '.' not in end else ''
        matches = [c for c in cues if seconds(start) <= seconds(c[0]) <= seconds(end) and anchor in c[2]]
        if not matches:
            raise ValueError(f'Capítulo {n:02d}, registro {idx}: ancla no localizada: {anchor}')
        quote = matches[0][2]
        # Usamos fragmento literal explícito; el cue se conserva en evidencia_cue.
        fact = dict(id=f'{n:02d}-{idx:03d}', titulo=title, tipo=kind,
                    afirmacion=statement, inicio=start, fin=end, cita=anchor,
                    evidencia_cue=dict(inicio=matches[0][0], fin=matches[0][1], texto=quote),
                    entidades=entities, ambito=scope, conocedores=knowers,
                    conocimiento_personaje=oghma,
                    nota_conocimiento=('Acceso de Madame Oghma sin establecer en este pasaje.' if oghma == 'desconocido'
                                       else 'Ver justificación y límites en la afirmación y su evidencia.'),
                    confianza='lectura de subtítulos; audio no cotejado',
                    limitacion=notes[0] if notes else '')
        validate_fact(fact, source)
        facts.append(fact)
    draft.update(fuente_sha256=sha(source), afirmaciones=facts)
    write_json(ROOT / 'conocimiento/capitulos' / f'{n:02d}.json', draft)
    print(f'Capítulo {n:02d}: {len(facts)} registros con citas localizadas.')


if __name__ == '__main__':
    main()
