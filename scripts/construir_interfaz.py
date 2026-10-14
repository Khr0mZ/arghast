"""Genera una enciclopedia HTML autónoma, sin servidor ni dependencias externas."""
import json
import base64
from collections import defaultdict
from construir import ROOT, KB, BUILD, read_json, write, seconds
from catalogo import load_catalog, canonical_labels
from seguimiento import build_tracking
from historias import load_entity_histories, load_chapter_histories


DOCUMENTS = {
    'atlas': ('Atlas de Xoltacan', 'ATLAS.md'),
    'facciones': ('Facciones y organizaciones', 'FACCIONES.md'),
    'misterios': ('Misterios y tramas', 'MISTERIOS.md'),
    'misiones': ('Misiones y consecuencias', 'MISIONES.md'),
    'relaciones': ('Relaciones entre personajes', 'RELACIONES.md'),
    'nombres': ('Nombres y equivalencias', 'NOMBRES.md'),
    'metodo': ('Fuentes y método', 'METODO.md'),
}


def build_data():
    episodes = read_json(ROOT / 'xoltacan_subtitulos/episodios.json')
    extras = ROOT / 'config/episodios_nuevos.json'
    if extras.exists():
        episodes += read_json(extras)
    aliases, notes, excluded = load_catalog()
    chapters, facts, entities, transcripts = [], [], defaultdict(list), {}
    for episode in sorted(episodes, key=lambda ep: ep['capitulo']):
        n = episode['capitulo']
        path = KB / 'capitulos' / f'{n:02d}.json'
        dossier = read_json(path) if path.exists() else {}
        chapter = {**episode, 'resumen': dossier.get('resumen', ''),
                   'estado': dossier.get('estado_revision', 'pendiente'),
                   'registros': [], 'misiones': dossier.get('misiones', []),
                   'preguntas': dossier.get('preguntas', []),
                   'contradicciones': dossier.get('contradicciones', []),
                   'nombres': dossier.get('nombres_dudosos', [])}
        meta_path = BUILD / f'{n:02d}/meta.json'
        chapter['duracion'] = read_json(meta_path).get('fin', '') if meta_path.exists() else ''
        for original in sorted(dossier.get('afirmaciones', []), key=lambda fact: seconds(fact['inicio'])):
            fact = {key: value for key, value in original.items()
                    if key not in ('conocedores', 'conocimiento_personaje', 'nota_conocimiento')}
            fact['capitulo'] = n
            fact['etiquetas_originales'] = fact.get('entidades', [])
            fact['entidades'] = canonical_labels(fact['etiquetas_originales'], aliases)
            facts.append(fact)
            chapter['registros'].append(fact['id'])
            for name in fact['entidades']:
                entities[name].append(fact['id'])
        segments_path = BUILD / f'{n:02d}/segmentos.jsonl'
        transcripts[str(n)] = []
        if segments_path.exists():
            for line in segments_path.read_text(encoding='utf-8').splitlines():
                segment = json.loads(line)
                transcripts[str(n)].append([segment['inicio'], segment['texto_original']])
        chapters.append(chapter)
    tracking = build_tracking()
    for chapter in chapters:
        chapter['seguimiento'] = [q for q in tracking['preguntas'] if q['capitulo'] == chapter['capitulo']]
    data = {'chapters': chapters, 'facts': facts, 'seguimiento': tracking, 'entities': [
        {'name': name, 'facts': list(dict.fromkeys(ids)), 'aliases': notes[name].get('etiquetas', [name]),
         'note': notes[name].get('nota', ''), 'type': notes[name]['tipo'],
         'description': notes[name].get('descripcion', ''),
         'references': notes[name].get('referencias', [])}
        for name, ids in sorted(entities.items(), key=lambda item: item[0].casefold())
        if name in notes and notes[name].get('tipo') and notes[name].get('visible', True) and name not in excluded],
        'transcripts': transcripts, 'documents': {
            key: {'title': title, 'text': (KB / filename).read_text(encoding='utf-8')}
            for key, (title, filename) in DOCUMENTS.items() if (KB / filename).exists()}}
    fact_index = {fact['id']: fact for fact in facts}
    histories = load_entity_histories(data['entities'], fact_index)
    for entity in data['entities']:
        entity['history'] = histories[entity['name']]
    chapter_histories = load_chapter_histories(chapters, fact_index)
    for chapter in chapters:
        chapter['history'] = chapter_histories.get(chapter['capitulo'])
    return data


def main():
    from campanas import build_world
    template = (ROOT / 'web/plantilla.html').read_text(encoding='utf-8')
    script = (ROOT / 'web/app.js').read_text(encoding='utf-8')
    theme = (ROOT / 'web/selva.css').read_text(encoding='utf-8')
    theme += '\n' + (ROOT / 'web/codice.css').read_text(encoding='utf-8')
    theme += '\n' + (ROOT / 'web/arghast.css').read_text(encoding='utf-8')
    landscape = base64.b64encode((ROOT / 'web/assets/xoltacan-selva.webp').read_bytes()).decode('ascii')
    theme = theme.replace('assets/xoltacan-selva.webp', 'data:image/webp;base64,' + landscape)
    if template.count('<!-- DATA -->') != 1 or template.count('<!-- APP -->') != 1:
        raise ValueError('La plantilla necesita un marcador DATA y un marcador APP')
    payload = json.dumps(build_world(build_data()), ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    output = template.replace('<!-- THEME -->', '<style>' + theme + '</style>')
    output = output.replace('<!-- DATA -->', '<script id="xoltacan-data" type="application/json">' + payload + '</script>')
    output = output.replace('<!-- APP -->', '<script>' + script.replace('</script', '<\\/script') + '</script>')
    write(ROOT / 'xoltacan.html', output)
    write(ROOT / 'arghast.html', output)
    print(f'arghast.html y xoltacan.html: {len(output.encode("utf-8")):,} bytes; archivo de campañas integrado.')


if __name__ == '__main__':
    main()
