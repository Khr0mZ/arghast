"""Recursos comunes y recursos propiedad de cada campaña para el compilador."""
import base64
from pathlib import Path
import re
from rutas import ROOT, CAMPAIGNS


def asset_files():
    result = {}
    for directory in [ROOT / 'web/assets', *(campaign.web / 'assets' for campaign in CAMPAIGNS.values())]:
        for path in directory.rglob('*'):
            if path.is_file() and path.suffix.lower() in ('.png', '.webp', '.jpg', '.svg', '.woff2', '.ttf'):
                key = 'assets/' + path.relative_to(directory).as_posix()
                if key in result:
                    raise ValueError('Recurso con dos propietarios: ' + key)
                result[key] = path
    return result


def inline_assets(text):
    assets = asset_files()
    def uri(name):
        path = assets[name]
        suffix = path.suffix.lower()
        mime = {'.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.ttf': 'font/ttf'}[suffix]
        return 'data:' + mime + ';base64,' + base64.b64encode(path.read_bytes()).decode('ascii')
    text = re.sub(r'url\(([\"\x27]?)(assets/[^)\"\x27]+)\1\)', lambda m: 'url(' + m[1] + uri(m[2]) + m[1] + ')', text)
    return re.sub(r'([\"\x27])(assets/[^\"\x27]+)\1', lambda m: m[1] + uri(m[2]) + m[1] if m[2] in assets and assets[m[2]].suffix in ('.png', '.webp', '.jpg', '.svg') else m[0], text)
