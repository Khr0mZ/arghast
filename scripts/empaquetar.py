"""Empaqueta biblioteca reproducible y comprueba bytes de cada entrada ZIP."""
import argparse
import zipfile
from construir import ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solo-conocimiento', action='store_true', help='Enciclopedia y lecturas Markdown, sin originales VTT/TXT ni herramientas.')
    args = parser.parse_args()
    folders = ['conocimiento', 'campanas'] if args.solo_conocimiento else ['conocimiento', 'campanas', 'derivados', 'config', 'borradores', 'scripts', 'web', 'xoltacan_subtitulos', '.github']
    files = set()
    for folder in folders:
        for path in (ROOT / folder).rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts and path.suffix not in ('.pyc', '.zip'):
                files.add(path)
    if args.solo_conocimiento:
        files.update((ROOT / 'derivados').glob('*/lectura.md'))
    for name in ('README.md', 'requirements-descarga.txt', 'xoltacan.html', 'arghast.html', '.gitignore'):
        path = ROOT / name
        if path.exists():
            files.add(path)
    target = ROOT / ('xoltacan_enciclopedia.zip' if args.solo_conocimiento else 'xoltacan_biblioteca.zip')
    temporary = target.with_suffix('.zip.tmp')
    expected = {path.relative_to(ROOT).as_posix(): path for path in files}
    with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for relative, path in sorted(expected.items()):
            archive.write(path, relative)
    with zipfile.ZipFile(temporary) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(expected):
            raise ValueError('ZIP incompleto o con entrada dañada')
        for relative, path in expected.items():
            if archive.read(relative) != path.read_bytes():
                raise ValueError('Entrada ZIP no coincide con archivo local: ' + relative)
    temporary.replace(target)
    print(f'{target.name}: {len(expected)} archivos; {target.stat().st_size:,} bytes; todas las entradas verificadas.')


if __name__ == '__main__':
    main()
