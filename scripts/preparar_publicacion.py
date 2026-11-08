"""Prepara solo el visor común y los lectores públicos, sin fuentes o revisiones."""
import argparse
from pathlib import Path
import shutil
from rutas import ROOT


def prepare(destination=None, root=ROOT):
    root = Path(root).resolve()
    destination = Path(destination or root / '_site').resolve()
    if destination != root / '_site' and not destination.is_relative_to(root / '.pruebas'):
        raise ValueError('El destino debe ser _site o una carpeta dentro de .pruebas.')
    if destination == root / '.pruebas':
        raise ValueError('No se reemplaza la raíz de las pruebas.')
    if destination.exists():
        if destination != root / '_site' and not (destination / '.arghast-publicacion').is_file():
            raise ValueError('No se reemplaza una carpeta ajena al constructor.')
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    (destination / '.arghast-publicacion').write_text('Arghast\n', encoding='utf-8')
    shutil.copyfile(root / 'arghast.html', destination / 'index.html')
    shutil.copyfile(root / 'arghast.html', destination / 'arghast.html')
    for campaign in ('xoltacan', 'kuroto'):
        shutil.copyfile(root / (campaign + '.html'), destination / (campaign + '.html'))
        source = root / 'campanas' / campaign / 'publico'
        target = destination / 'campanas' / campaign / 'publico'
        shutil.copytree(source, target)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino', type=Path)
    args = parser.parse_args()
    print(prepare(args.destino))
