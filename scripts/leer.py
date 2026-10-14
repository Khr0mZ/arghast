"""Muestra toda la lectura de un intervalo, agrupada por dos minutos, sin resumirla."""
import argparse
import json
from collections import defaultdict
from pathlib import Path
from construir import ROOT, seconds

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('capitulo', type=int)
parser.add_argument('--desde', type=float, default=0, help='Minutos')
parser.add_argument('--hasta', type=float, default=10000, help='Minutos')
args = parser.parse_args()
path = ROOT / 'derivados' / f'{args.capitulo:02d}' / 'segmentos.jsonl'
groups = defaultdict(list)
for line in path.read_text(encoding='utf-8').splitlines():
    row = json.loads(line)
    time = seconds(row['inicio'])
    if args.desde * 60 <= time < args.hasta * 60:
        groups[int(time // 120)].append(row['texto_normalizado'])
for group, lines in groups.items():
    time = group * 120
    print(f'\n[{time // 3600:02d}:{time % 3600 // 60:02d}:00] ' + ' '.join(lines))
