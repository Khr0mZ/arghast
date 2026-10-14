"""Localiza anclas editoriales fuera de intervalo antes de compilar una ficha."""
import argparse
import html
import re
from construir import ROOT, TIMING, read_json, seconds

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('ficha')
args = parser.parse_args()
d = read_json(ROOT / args.ficha)
n = d['capitulo']
meta = read_json(ROOT / 'derivados' / f'{n:02d}' / 'meta.json')
cues = []
for block in re.split(r'\n{2,}', (ROOT / meta['fuente']).read_text(encoding='utf-8-sig').replace('\r\n', '\n')):
    match = TIMING.search(block)
    if match:
        payload = block.splitlines()[next(i for i, line in enumerate(block.splitlines()) if TIMING.search(line)) + 1:]
        text = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]*>', '', ' '.join(payload)))).strip()
        cues.append((match[1], text))
bad = 0
for idx, r in enumerate(d['registros'], 1):
    matches = [(t, x) for t, x in cues if r[6] in x]
    if not any(seconds(r[0]) <= seconds(t) <= seconds(r[1]) for t, x in matches):
        bad += 1
        print(idx, r[6], matches[:4])
        if not matches:
            tokens = r[6].split()
            candidates = [(t, x) for t, x in cues if seconds(r[0]) <= seconds(t) <= seconds(r[1])
                          and any(word in x for word in tokens if len(word) > 4)]
            print('Candidatos:', candidates[:6])
print('Anclas pendientes:', bad)
