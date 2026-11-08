"""Inserta los estilos de cada campaña en el orden del diseño compartido."""
import re
from rutas import CAMPAIGNS


def expand_styles(text):
    cache = {}
    def replace(match):
        campaign, filename, block = match.groups()
        key = campaign, filename
        if key not in cache:
            source = (CAMPAIGNS[campaign].web / 'estilos' / filename).read_text(encoding='utf-8')
            parts = re.split(r'/\* ARGHAST-BLOQUE:(\d+) \*/', source)
            cache[key] = dict(zip(parts[1::2], parts[2::2]))
        return cache[key][block]
    return re.sub(r'/\* ARGHAST-ESTILO:(xoltacan|kuroto):([\w.-]+):(\d+) \*/', replace, text)
