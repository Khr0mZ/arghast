import html
import re
from pathlib import Path


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
