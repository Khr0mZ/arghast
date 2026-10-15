"""Preparar el Worker de Sites sin fuentes privadas ni transcripciones."""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def prepare(destination):
    world = json.loads(re.search(r'<script id="xoltacan-data" type="application/json">(.*?)</script>',
                               (ROOT / 'arghast.html').read_text(encoding='utf-8'), re.S)[1])
    sources = {campaign: [str(c['capitulo']) for c in data['chapters']]
               for campaign, data in [('xoltacan', world), ('kuroto', world['campaigns']['kuroto'])]}
    source = 'const sources=' + json.dumps(sources) + ';\n'
    source += (ROOT / 'online/modelo.mjs').read_text(encoding='utf-8').replace('export function validate', 'function validate')
    worker = (ROOT / 'online/worker.mjs').read_text(encoding='utf-8')
    source += '\n' + re.sub(r'^import .*?;\n', '', worker, flags=re.M)
    target = destination / 'worker/index.js'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source, encoding='utf-8')
    manifest_path = destination / '.openai/hosting.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest.update(d1=None, r2='BUCKET')
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print('Worker preparado; solo se incluyen los números de las transcripciones, no su contenido.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    prepare(parser.parse_args().destination.resolve())
