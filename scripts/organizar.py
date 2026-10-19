"""Vistas de consulta derivadas de fichas; no infiere identidades ni relaciones."""
import hashlib
import re
from collections import defaultdict
from construir import ROOT, KB, BUILD, read_json, seconds, write, write_json
from catalogo import load_catalog, canonical_labels, source_links
from historias import load_entity_histories


def entity_filename(name):
    stem = re.sub(r'[^\w-]+', '-', name, flags=re.UNICODE).strip('-')[:65]
    return stem + '-' + hashlib.sha256(name.encode()).hexdigest()[:8] + '.md'


def collect():
    return [(int(path.stem), fact) for path in sorted((KB / 'capitulos').glob('*.json'))
            for fact in read_json(path).get('afirmaciones', [])]


def reference(n, fact, prefix=''):
    anchor = fact['id'] + ' · ' + fact['titulo']
    return f'[{anchor}]({prefix}capitulos/{n:02d}.md) · {fact["inicio"]}'


def render_views():
    facts = collect()
    aliases, notes, excluded = load_catalog()
    groups = list(notes.values())
    entities = defaultdict(list)
    for n, fact in facts:
        for name in canonical_labels(fact.get('entidades', []), aliases):
            if name in notes and notes[name].get('tipo') and notes[name].get('visible', True) and name not in excluded:
                entities[name].append((n, fact))
    fact_index = {fact['id']: {**fact, 'capitulo': n} for n, fact in facts}
    histories = load_entity_histories(
        [{'name': name, 'type': notes[name]['tipo']} for name in entities], fact_index)
    index = ['# Fichas de entidades', '',
             'Catálogo revisado de personajes, lugares, facciones y objetos. Las variantes acreditadas remiten a una sola ficha. Las etiquetas de acontecimientos, efectos y notas de revisión se conservan en las fuentes y no crean entradas del catálogo.', '',
             '| Entidad | Capítulos con menciones | Registros |', '|---|---|---|']
    generated = []
    for name, mentions in sorted(entities.items(), key=lambda item: item[0].casefold()):
        filename = entity_filename(name)
        generated.append(filename)
        chapters = ', '.join(f'{n:02d}' for n in sorted({n for n, _ in mentions}))
        index.append(f'| [{name}](entidades/{filename}) | {chapters} | {len(mentions)} |')
        lines = [f'# {name}', '',
                 'Menciones documentadas por capítulo y minuto. La etiqueta no garantiza grafía oficial; véanse limitaciones y nombres dudosos de cada episodio.', '']
        if name in notes:
            group = notes[name]
            links = source_links(group, '../')
            lines += [group.get('descripcion', ''), '']
            lines += [group['nota'], '', 'Etiquetas agrupadas: ' + '; '.join(group['etiquetas']) + '.', '',
                      'Base para revisar equivalencia: ' + links + '.', '']
        if name in histories:
            history = histories[name]
            story_title = {'personaje': 'Su historia en Xoltacan', 'lugar': 'Historia y acontecimientos',
                           'faccion': 'Intereses y evolución', 'objeto': 'Origen y recorrido'}[notes[name]['tipo']]
            lines += ['## ' + story_title, '',
                      f'Relato revisado hasta el capítulo {history["revisado_hasta"]}.', '']
            for stage in history['etapas']:
                lines += ['### ' + stage['titulo'], '', stage['texto'], '',
                          'Fuentes: ' + ' · '.join(
                              reference(fact_index[key]['capitulo'], fact_index[key], '../')
                              for key in stage['referencias']) + '.', '']
            lines += ['## Registros y evidencias', '']
        for n, fact in sorted(mentions, key=lambda item: (item[0], seconds(item[1]['inicio']))):
            lines += [f'## {reference(n, fact, "../")}', '',
                      f'Tipo: `{fact["tipo"]}`.', '',
                      fact['afirmacion'], '', fact.get('limitacion', ''), '']
        write(KB / 'entidades' / filename, '\n'.join(lines) + '\n')
    write(KB / 'FICHAS.md', '\n'.join(index) + '\n')
    folder = (KB / 'entidades').resolve()
    manifest_path = BUILD / 'entidades_generadas.json'
    previous = read_json(manifest_path) if manifest_path.exists() else []
    for filename in set(previous) - set(generated):
        path = (folder / filename).resolve()
        if path.parent != folder or path.suffix != '.md':
            raise ValueError('Ruta de ficha generada fuera de carpeta: ' + filename)
        if path.exists():
            path.unlink()
    write_json(manifest_path, sorted(generated))
    lines = ['# Nombres y equivalencias editoriales', '',
             'No se modifica ningún original. Estas equivalencias agrupan etiquetas de fichas; las candidatas siguen expresamente provisionales. Otras identidades dudosas se conservan separadas.', '',
             '| Etiqueta de consulta | Variantes agrupadas | Criterio y referencias |', '|---|---|---|']
    for group in groups:
        links = source_links(group)
        lines.append(f'| {group["nombre"]} | {"; ".join(group["etiquetas"])} | {group["nota"]} {links} |')
    lines += ['', '## Separaciones fundamentales', '',
              '- Naór y Nox son personas distintas.',
              '- Marina como organización y Marina como sirena son entidades diferentes.',
              '- Mamá/Citlali y Coyote no se fusionan por la pista del usuario; cada revelación necesita fuente.',
              '- Citlali y Coyote aparecen como personajes distintos en capítulo 39; compartir intérprete no los hace una identidad.',
              '- Tórtola, almirante aviar, no se fusiona con rey Jones ni con general anónimo por parecido de nombre o aspecto.',
              '- Los collares, mapas, copas y monedas de distintas expediciones no se consideran un mismo objeto por su material o nombre genérico.',
              '- Especie de una ilustración o token no prueba identidad ni resurrección. Las monturas numeradas de Poncelot son distintas.',
              '- Consultar los nombres dudosos de cada capítulo para variantes que aún no se pueden agrupar.', '']
    write(KB / 'NOMBRES.md', '\n'.join(lines))
    episodes = read_json(ROOT / 'xoltacan_subtitulos/episodios.json')
    extra = ROOT / 'config/episodios_nuevos.json'
    if extra.exists():
        episodes += read_json(extra)
    reviewed = []
    pending = []
    rows = []
    for episode in sorted(episodes, key=lambda ep: ep['capitulo']):
        n = episode['capitulo']
        dossier_path = KB / 'capitulos' / f'{n:02d}.json'
        dossier = read_json(dossier_path) if dossier_path.exists() else {}
        status = dossier.get('estado_revision', 'pendiente')
        (reviewed if status == 'revisado' else pending).append(n)
        count = len(dossier.get('afirmaciones', []))
        meta_path = BUILD / f'{n:02d}' / 'meta.json'
        duration = read_json(meta_path).get('fin', '') if meta_path.exists() else 'sin VTT preparado'
        rows.append(f'| [{n:02d}](capitulos/{n:02d}.md) | {status} | {count} | {duration} |' if dossier_path.exists()
                    else f'| {n:02d} | {status} | 0 | {duration} |')
    progress = ['# Progreso de la enciclopedia de Xoltacan', '',
                f'**{len(reviewed)}/{len(episodes)} capítulos revisados; {len(facts)} registros con evidencia temporal.**', '',
                'Consulta global, sin filtro de conocimiento de Oghma. Originales conservados; audio no cotejado. Revisado significa lectura completa y selección estructurada de acontecimientos, no transcripción perfecta o extracción de cada detalle.', '',
                '## Cobertura', '', '| Capítulo | Revisión | Registros | Último cue de fuente |',
                '|---|---|---|---|', *rows, '', '## Continuidad y mantenimiento', '',
                '[Índice](INDICE.md) · [Misterios actuales](MISTERIOS.md) · [Relaciones](RELACIONES.md) · [Tramas históricas](TRAMAS.md) · [Guía de consulta](GUIA_CONSULTA.md)', '',
                'La revisión paralela autorizada abarcó bloques 18–24, 25–31 y 32–39, con cruce posterior de revelaciones y referencias. Los anteriores se revisaron secuencialmente. El capítulo 40 se leyó en tres bloques sin solapamiento (00:00–00:58, 00:58–01:56 y 01:56–fin), integrados después con sus fichas y el seguimiento histórico.', '',
                'Siguiente capítulo pendiente: ' + (f'{min(pending):02d}.' if pending else 'ninguno en el catálogo actual.'), '',
                f'La campaña narrativa conserva asuntos abiertos al final del capítulo {max(reviewed, default=0)}. Incorporar publicaciones nuevas con `scripts/incorporar.py`, revisar fuentes completas y actualizar continuidades/alias/misterios antes de regenerar índices.', '',
                'Auditoría: `python -X utf8 scripts/auditar.py --exigir-completo --comparar-zip`. Pruebas: `scripts/test_construir.py` y `scripts/test_consultar.py`. Paquetes reproducibles: `scripts/empaquetar.py`.', '',
                'Notas de trabajo antiguas preservadas en [historial](historial/PROGRESO_01_16.md). No representan el estado actual.', '']
    write(KB / 'PROGRESO.md', '\n'.join(progress))


if __name__ == '__main__':
    render_views()
