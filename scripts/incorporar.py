"""Añade episodios al catálogo local y descarga únicamente subtítulos, sin sobrescribir originales."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capitulo', type=int)
    parser.add_argument('--url')
    parser.add_argument('--titulo')
    parser.add_argument('--descargar', action='store_true', help='Recupera los episodios sin VTT válido')
    args = parser.parse_args()
    source = ROOT / 'xoltacan_subtitulos'
    extra = ROOT / 'config/episodios_nuevos.json'
    new = json.loads(extra.read_text(encoding='utf-8')) if extra.exists() else []
    episodes = json.loads((source / 'episodios.json').read_text(encoding='utf-8')) + new
    if any(x is not None for x in (args.capitulo, args.url, args.titulo)):
        if not all((args.capitulo, args.url, args.titulo)) or args.capitulo < 1:
            parser.error('Indica juntos --capitulo, --url y --titulo; capítulo positivo')
        match = re.fullmatch(r'https://(?:www\.)?youtube\.com/watch\?v=([\w-]{11})|https://youtu\.be/([\w-]{11})', args.url)
        if not match:
            parser.error('Usa una URL de vídeo YouTube sin parámetros adicionales')
        video_id = match[1] or match[2]
        ep = dict(capitulo=args.capitulo, id=video_id, titulo=args.titulo,
                  url='https://www.youtube.com/watch?v=' + video_id)
        conflict = [e for e in episodes if e['capitulo'] == ep['capitulo'] or e['id'] == video_id]
        if conflict and conflict != [ep]:
            parser.error('Número o vídeo ya registrado con otros datos; revisa el catálogo')
        if not conflict:
            new.append(ep)
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text(json.dumps(sorted(new, key=lambda e: e['capitulo']), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            episodes.append(ep)
    errors = []
    if args.descargar:
        sys.path.insert(0, str(ROOT / 'scripts'))
        from construir import parse_vtt
        out = source / 'subtitulos'
        out.mkdir(exist_ok=True)
        for ep in sorted(episodes, key=lambda e: e['capitulo']):
            stem = f'{ep["capitulo"]:02d} - {ep["id"]}'
            candidates = list(out.glob(stem + '*.vtt'))
            valid = False
            for file in candidates:
                try:
                    parse_vtt(file)
                    valid = True
                except ValueError:
                    pass
            if valid:
                continue
            print(f'Descargando subtítulos: {ep["capitulo"]:02d}', flush=True)
            # Los archivos existentes, incluso defectuosos, se conservan para investigar.
            result = subprocess.run([sys.executable, '-m', 'yt_dlp', '--skip-download',
                '--no-playlist', '--write-subs', '--write-auto-subs', '--sub-langs', 'es-orig,es',
                '--sub-format', 'vtt', '--no-overwrites', '--socket-timeout', '20', '--retries', '2',
                '-o', str(out / (stem + '.%(ext)s')), ep['url']], check=False)
            if result.returncode:
                errors.append(ep['capitulo'])
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/construir.py')], check=False)
    if errors:
        print('Descargas con error (no implica ausencia de subtítulos):', errors)
    return result.returncode or bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
