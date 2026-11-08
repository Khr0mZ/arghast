#!/usr/bin/env python3
"""Descarga subtitulos (manuales o automaticos) en español de 39 capitulos.
No descarga video/audio. Requiere 'pip install yt-dlp'. Ejecutar en una red
con acceso normal a YouTube. Los .vtt incluyen las marcas de tiempo.
"""
import csv
import html
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'subtitulos'
OUT.mkdir(exist_ok=True)


def texto_desde_vtt(path: Path) -> str:
    """Versión legible con tiempos. El .vtt original es la fuente principal."""
    lines = path.read_text(encoding='utf-8-sig', errors='replace').splitlines()
    parts = []
    last = ''
    t = ''
    for line in lines:
        line = line.strip()
        if '-->' in line:
            t = line.split('-->')[0].strip()
            continue
        if not line or line.startswith(('WEBVTT', 'Kind:', 'Language:', 'NOTE', 'STYLE', 'REGION')):
            continue
        if re.fullmatch(r'\d+', line):
            continue
        line = html.unescape(re.sub(r'<[^>]*>', '', line))
        line = re.sub(r'\s+', ' ', line).strip()
        if line and line != last:
            parts.append(f'[{t}] {line}' if t else line)
            last = line
    return '\n'.join(parts) + '\n'


def main():
    if importlib.util.find_spec('yt_dlp') is None:
        print('Falta yt-dlp. Instala con: python -m pip install -U yt-dlp')
        return 1
    eps = json.loads((ROOT/'episodios.json').read_text(encoding='utf-8'))
    log = []
    for idx, ep in enumerate(eps, start=1):
        stem = f'{ep["capitulo"]:02d} - {ep["id"]}'
        existing = sorted(OUT.glob(stem + '*.vtt'))
        if not existing:
            print(f'[{idx}/{len(eps)}] Capitulo {ep["capitulo"]:02d}: {ep["titulo"]}', flush=True)
            cmd = [sys.executable, '-m', 'yt_dlp',
                   '--skip-download', '--write-subs', '--write-auto-subs',
                   '--sub-langs', 'es.*', '--sub-format', 'vtt/best',
                   '--no-overwrites', '--ignore-errors',
                   '-o', str(OUT / (stem + '.%(ext)s')),
                   ep['url']]
            try:
                proc = subprocess.run(cmd, check=False)
                if proc.returncode != 0:
                    print('  Advertencia: YouTube o yt-dlp no devolvio subtitulos.')
            except KeyboardInterrupt:
                print('Interrumpido; los archivos ya descargados se conservan.')
                return 130
            existing = sorted(OUT.glob(stem + '*.vtt'))
        if existing:
            for subfile in existing:
                txtfile = subfile.with_suffix('.txt')
                if not txtfile.exists():
                    txtfile.write_text(texto_desde_vtt(subfile),encoding='utf-8')
            state = 'descargado'
            print('  OK: ' + ', '.join(p.name for p in existing))
        else:
            state = 'sin_subtitulos_o_error'
            print('  SIN SUBTITULOS. Puede requerir transcripcion de audio con Whisper.')
        log.append({**ep,'estado':state})
        (ROOT/'estado.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (ROOT/'estado.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=['capitulo','titulo','url','id','estado'])
        w.writeheader(); w.writerows(log)
    print(f'\nCompletado: {sum(e["estado"]=="descargado" for e in log)} de {len(log)} capitulos con subtitulos.')
    print(f'Archivos en: {OUT}')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
