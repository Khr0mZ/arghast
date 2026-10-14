"""Rasteriza rótulos sin redistribuir Ambystoma. Requiere Pillow y --fuente local.

El constructor normal usa los PNG guardados y no necesita la fuente original.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
LABELS = [
    'Portada', 'Crónicas', 'Acontecimientos', 'Personajes', 'Lugares',
    'Facciones', 'Vestigios', 'Misiones', 'Misterios y desenlaces',
    'Relaciones', 'Fuentes y método', 'Nombres y equivalencias',
    'Archivo', 'Campaña', 'Estás explorando', 'Ver las campañas',
    'Arghast / Xoltacan', 'Abrir las crónicas', 'Seguir los misterios',
    'Leer el relato', 'Elegir campaña', 'Explorar los capítulos',
    'Restablecer', 'Anterior', 'Siguiente', 'Abrir episodio',
    'Abrir el episodio', 'Copiar referencia', 'Referencia copiada',
    'Volver a intentar', 'Mostrar más segmentos', 'Ir al inicio',
    'Relato de la sesión', 'Preguntas de la sesión', 'Transcripción',
    'Historia', 'Historia y acontecimientos', 'Intereses y evolución',
    'Origen y recorrido', 'Registros y evidencias',
    'Contexto geográfico y rutas', 'Contexto político y conflictos',
    'Identificación y referencias', 'Síntesis de las tramas principales',
    'Leer contexto de la transcripción', 'Volver a las crónicas',
    'Buscar un capítulo', 'Buscar un personaje', 'Buscar un lugar',
    'Buscar una facción', 'Buscar un vestigio', 'Estado', 'Capítulo',
    'Evidencia', 'Resultados de búsqueda', 'Buscar en esta transcripción',
    'Buscar una pregunta o respuesta',
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fuente', type=Path, required=True)
    args = parser.parse_args()
    font = ImageFont.truetype(str(args.fuente), 96)
    target = ROOT / 'web/assets/rotulos-xoltacan'
    target.mkdir(parents=True, exist_ok=True)
    title_font = ImageFont.truetype(str(args.fuente), 240)
    title_box = title_font.getbbox('Xoltacan')
    title_image = Image.new('RGBA', (title_box[2]-title_box[0]+16, title_box[3]-title_box[1]+16))
    ImageDraw.Draw(title_image).text((8-title_box[0],8-title_box[1]), 'Xoltacan', font=title_font, fill='#F7EAC8')
    title_image.save(ROOT/'web/assets/xoltacan-titulo.png', optimize=True)
    entries = {}
    styles = ['/* Rótulos de Ambystoma Mexicanum; no contiene software de fuente. */']
    for label in LABELS + ['Misterios y desenlaces|sidebar']:
        lines = ['Misterios y', 'desenlaces'] if label.endswith('|sidebar') else [label]
        boxes = [font.getbbox(line) for line in lines]
        width = max(box[2]-box[0] for box in boxes) + 8
        height = max(box[3]-box[1] for box in boxes) + 8 + (len(lines)-1)*100
        image = Image.new('RGBA', (width, height))
        draw = ImageDraw.Draw(image)
        for index, (line, box) in enumerate(zip(lines, boxes)):
            draw.text((4-box[0], 4-box[1]+index*100), line, font=font, fill='white')
        key = 'r' + hashlib.sha256(label.encode()).hexdigest()[:12]
        image.save(target / (key+'.png'), optimize=True)
        entries[label] = key
        styles.append(f'[data-lettering="{key}"] {{ --lettering-src:url(assets/rotulos-xoltacan/{key}.png); --lettering-width:{width/96:.5f}em; --lettering-height:{height/96:.5f}em; }}')
    (ROOT/'web/rotulos.css').write_text('\n'.join(styles)+'\n',encoding='utf-8')
    (target/'indice.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    provenance = {
        'family': 'Ambystoma Mexicanum', 'author': 'Chequered Ink',
        'source': 'https://www.dafont.com/ambystoma-mexicanum.font',
        'license': 'Personal, Non-Commercial; only rendered graphics, no font software redistributed',
        'license_file': 'web/assets/xoltacan-titulo.licencia.html',
        'font_sha256': hashlib.sha256(args.fuente.read_bytes()).hexdigest(),
        'generator': 'scripts/generar_rotulos.py',
        'files': [{'label': label, 'file': f'web/assets/rotulos-xoltacan/{key}.png',
                   'sha256': hashlib.sha256((target/(key+'.png')).read_bytes()).hexdigest()}
                  for label, key in entries.items()],
    }
    (ROOT/'web/assets/rotulos-xoltacan.procedencia.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(entries)} rótulos de interfaz preparados.')


if __name__ == '__main__':
    main()
