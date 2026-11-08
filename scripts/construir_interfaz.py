"""Genera una enciclopedia HTML autónoma, sin servidor ni dependencias externas."""
import json
import base64
from collections import defaultdict
from construir import ROOT, KB, BUILD, read_json, write, seconds
from catalogo import load_catalog, canonical_labels
from seguimiento import build_tracking
from historias import load_entity_histories, load_chapter_histories
from rutas import episodios


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
    episodes = episodios()
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
    from fechas_emision import attach_dates
    attach_dates('xoltacan', chapters)
    from rol_escrito import load_written_role
    data['writtenRole'] = load_written_role('xoltacan', chapters)
    return data


def main():
    from campanas import build_world
    from vistas_kuroto import refresh
    from exportar_kuroto import export
    from compilar_web import compile_world
    world = build_world(build_data())
    refresh(world['campaigns']['kuroto'])
    export(world['campaigns']['kuroto'])
    compile_world(world)


if __name__ == '__main__':
    main()
