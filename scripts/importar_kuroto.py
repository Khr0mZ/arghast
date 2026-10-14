"""Descarga subtítulos de Kuroto conservando originales; no genera resúmenes ni canon."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from construir import ROOT, parse_vtt, read_json, write_json
from campanas import KUROTO


def prepare():
    path = KUROTO / 'fuentes/originales_sha256.json'
    previous = read_json(path) if path.exists() else {}
    current = {source.relative_to(KUROTO).as_posix(): hashlib.sha256(source.read_bytes()).hexdigest()
               for source in sorted((KUROTO / 'fuentes').glob('*.vtt'))}
    if any(current.get(name) != digest for name, digest in previous.items()):
        raise ValueError('Se ha modificado o eliminado un original de Kuroto; investigar antes de continuar')
    for episode in read_json(KUROTO / 'catalogo.json')['episodios']:
        number = episode['capitulo']
        candidates = sorted((KUROTO / 'fuentes').glob(f'{number:03d} - {episode["id"]}*.vtt'))
        if not candidates:
            continue
        source = next((p for p in candidates if '.es-orig.' in p.name), candidates[0])
        segments = parse_vtt(source)
        folder = KUROTO / 'derivados' / f'{number:03d}'
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'segmentos.jsonl').write_text(''.join(json.dumps(segment, ensure_ascii=False)+'\n' for segment in segments), encoding='utf-8')
        (folder / 'lectura.md').write_text(f'# Kuroto · Capítulo {number}: {episode["titulo"]}\n\n'
            + '\n\n'.join(f'[{segment["inicio"]}] {segment["texto_original"]}' for segment in segments)+'\n', encoding='utf-8')
    write_json(path, current)
    print(f'{len(current)} originales de subtítulos conservados y verificados.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--descargar', action='store_true')
    parser.add_argument('--preparar', action='store_true')
    parser.add_argument('--capitulo', type=int)
    parser.add_argument('--cookies', type=Path, help='Archivo de cookies aportado explícitamente para YouTube; nunca se copia al proyecto')
    args = parser.parse_args()
    if args.cookies and not args.descargar:
        parser.error('--cookies requiere --descargar')
    episodes = read_json(KUROTO / 'catalogo.json')['episodios']
    if args.capitulo is not None:
        episodes = [episode for episode in episodes if episode['capitulo'] == args.capitulo]
        if not episodes:
            parser.error('Ese capítulo no está localizado en el catálogo de Kuroto')
    if args.descargar:
        prepare()
        for episode in episodes:
            number = episode['capitulo']
            pattern = f'{number:03d} - {episode["id"]}*.vtt'
            if list((KUROTO / 'fuentes').glob(pattern)):
                continue
            command = [sys.executable, '-m', 'yt_dlp', '--js-runtimes', 'node', '--skip-download',
                '--no-playlist', '--write-subs', '--write-auto-subs', '--sub-langs', 'es-orig,es',
                '--sub-format', 'vtt', '--no-overwrites', '--socket-timeout', '20', '--retries', '0',
                '--extractor-retries', '0', '-o', str(KUROTO / 'fuentes' / f'{number:03d} - {episode["id"]}.%(ext)s'), episode['url']]
            if args.cookies:
                command[command.index('--skip-download'):command.index('--skip-download')] = ['--cookies', str(args.cookies.resolve())]
            result = subprocess.run(command, text=True, encoding='utf-8', errors='replace', capture_output=True)
            prepare()  # Registra también originales recuperados antes de un fallo parcial.
            if result.returncode:
                blocked = '429' in result.stderr or 'not a bot' in result.stderr
                status = {'capitulo': number, 'estado': 'bloqueado_youtube' if blocked else 'error_descarga',
                          'detalle': 'YouTube requiere autenticación o limita las solicitudes.' if blocked else 'Revisar acceso y disponibilidad de subtítulos.',
                          'sin_subtitulos_confirmado': False}
                write_json(KUROTO / 'fuentes/estado_descarga.json', status)
                print(status['detalle'] + ' Se detiene la importación para no repetir peticiones fallidas.')
                return 1
    if args.preparar or not args.descargar:
        prepare()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
