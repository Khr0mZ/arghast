"""Encuadra el logo original en un favicon SVG circular, sin modificar sus píxeles."""
import base64
import hashlib
import json
from rutas import ROOT


def main():
    source = ROOT / 'web/assets/lichpol-logo.webp'
    raw = source.read_bytes()
    records = json.loads((ROOT / 'web/assets/imagenes-aportadas.procedencia.json').read_text(encoding='utf-8'))['assets']
    record = next(row for row in records if row['file'] == source.relative_to(ROOT).as_posix())
    assert hashlib.sha256(raw).hexdigest() == record['sha256'], 'El logo no coincide con el original registrado.'
    width, height = record['width'], record['height']
    assert width == height
    margin = round(width / 22)
    side = width - margin * 2
    image = 'data:image/webp;base64,' + base64.b64encode(raw).decode('ascii')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="{margin} {margin} {side} {side}">'
           '<title>Lichpol</title><defs><clipPath id="circle" clipPathUnits="userSpaceOnUse">'
           f'<circle cx="{width / 2:g}" cy="{height / 2:g}" r="{side / 2:g}"/></clipPath></defs>'
           f'<image width="{width}" height="{height}" href="{image}" clip-path="url(#circle)"/></svg>\n')
    target = ROOT / 'web/assets/lichpol-favicon.svg'
    target.write_bytes(svg.encode('utf-8'))
    provenance = dict(source=record['file'], source_sha256=record['sha256'],
                      file=target.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                      generator='scripts/generar_favicon.py', viewBox=[margin, margin, side, side],
                      processing='Circular SVG clipping and tighter framing; original embedded unchanged; transparent exterior.')
    (ROOT / 'web/assets/lichpol-favicon.procedencia.json').write_bytes((json.dumps(provenance, indent=2) + '\n').encode('utf-8'))
    print(target.relative_to(ROOT).as_posix())


if __name__ == '__main__':
    main()
