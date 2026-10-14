"""Construcción local, incremental y sin dependencias de la biblioteca de Xoltacan."""
import argparse
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'xoltacan_subtitulos'
BUILD = ROOT / 'derivados'
KB = ROOT / 'conocimiento'
VERSION = 1
TIMING = re.compile(r'(\d+:\d{2}:\d{2}\.\d{3})\s+-->\s+(\d+:\d{2}:\d{2}\.\d{3})')


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding='utf-8') != text:
        path.write_text(text, encoding='utf-8')


def write_json(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seconds(t):
    h, m, s = t.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def parse_vtt(path):
    """Quita únicamente líneas de arrastre de cues contiguos; no deduplica diálogo."""
    raw = path.read_text(encoding='utf-8-sig')
    if not raw.startswith('WEBVTT'):
        raise ValueError(f'Cabecera VTT inválida: {path}')
    segments = []
    previous_lines, previous_end = [], -1
    cue_number = 0
    for block in re.split(r'\n{2,}', raw.replace('\r\n', '\n')):
        lines = block.splitlines()
        timing_index = next((i for i, line in enumerate(lines) if TIMING.search(line)), None)
        if timing_index is None:
            continue
        start, end = TIMING.search(lines[timing_index]).groups()
        if seconds(end) < seconds(start):
            raise ValueError(f'Cue invertido: {path}: {start}')
        cue_number += 1
        payload = []
        tagged = []
        for line in lines[timing_index + 1:]:
            clean = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]*>', '', line))).strip()
            if clean:
                payload.append(clean)
                tagged.append(bool(re.search(r'<\d+:\d{2}:\d{2}\.\d{3}>', line)))
        contiguous = 0 <= seconds(start) - previous_end <= 0.021
        fresh = [line for line, has_new_timing in zip(payload, tagged)
                 if has_new_timing or not (contiguous and line in previous_lines)]
        if fresh:
            segments.append({'id': f'c{cue_number:06d}', 'inicio': start, 'fin': end,
                             'texto_original': ' '.join(fresh)})
        previous_lines, previous_end = payload, seconds(end)
    if not segments:
        raise ValueError(f'VTT sin texto: {path}')
    return segments


def normalize(text, aliases):
    if not aliases:
        return text
    pattern = r'(?<!\w)(' + '|'.join(re.escape(x) for x in sorted(aliases, key=len, reverse=True)) + r')(?!\w)'
    return re.sub(pattern, lambda m: aliases[m.group()], text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reconstruir', action='store_true')
    args = parser.parse_args()
    names = read_json(ROOT / 'config/nombres.json')
    episodes = read_json(SOURCES / 'episodios.json')
    extra = ROOT / 'config/episodios_nuevos.json'
    if extra.exists():
        episodes += read_json(extra)
    nums = [e['capitulo'] for e in episodes]
    if len(nums) != len(set(nums)):
        raise ValueError('Capítulos duplicados en el catálogo')
    if len({e['id'] for e in episodes}) != len(episodes):
        raise ValueError('Un vídeo figura como varios capítulos')
    # Inventario de TODOS los originales, incluidos TXT y variantes no elegidas.
    inventory = {p.relative_to(ROOT).as_posix(): {'sha256': sha(p), 'bytes': p.stat().st_size}
                 for p in sorted((SOURCES / 'subtitulos').glob('*')) if p.suffix in ('.vtt', '.txt')}
    baseline = BUILD / 'originales_sha256.json'
    old = read_json(baseline) if baseline.exists() else {}
    changed = [p for p, metadata in old.items() if inventory.get(p) != metadata]
    if changed:
        raise ValueError('Originales modificados o desaparecidos; investigar antes de continuar: ' + ', '.join(changed))
    write_json(baseline, inventory)
    from seguimiento import build_tracking, render_tracking
    tracking = build_tracking()
    from historias import load_chapter_histories
    dossiers = [read_json(path) for path in sorted((KB / 'capitulos').glob('*.json'))]
    chapter_histories = load_chapter_histories(
        [{'capitulo': data['capitulo'], 'resumen': data['resumen'],
          'estado': data.get('estado_revision', 'pendiente')} for data in dossiers],
        {fact['id']: {**fact, 'capitulo': data['capitulo']}
         for data in dossiers for fact in data.get('afirmaciones', [])})
    manifest = []
    for ep in sorted(episodes, key=lambda e: e['capitulo']):
        n = ep['capitulo']
        stem = f'{n:02d} - {ep["id"]}'
        files = sorted((SOURCES / 'subtitulos').glob(stem + '*.vtt'))
        record = {**ep, 'variantes': [p.relative_to(ROOT).as_posix() for p in files]}
        folder = BUILD / f'{n:02d}'
        meta_file = folder / 'meta.json'
        if not files:
            record['estado_fuente'] = 'falta_vtt'
            manifest.append(record)
            continue
        source = next((p for p in files if '.es-orig.' in p.name), files[0])
        fingerprint = hashlib.sha256(json.dumps({'source': sha(source), 'names': names,
            'parser': sha(Path(__file__)), 'ep': ep, 'version': VERSION}, sort_keys=True).encode()).hexdigest()
        outputs = [folder / 'segmentos.jsonl', folder / 'lectura.md', folder / 'cambios.json']
        cached = meta_file.exists() and read_json(meta_file).get('fingerprint') == fingerprint and all(p.exists() for p in outputs)
        if not cached or args.reconstruir:
            segments = parse_vtt(source)
            changes = []
            for s in segments:
                s['texto_normalizado'] = normalize(s['texto_original'], names['alias_confirmados'])
                if s['texto_normalizado'] != s['texto_original']:
                    changes.append({k: s[k] for k in ('id', 'inicio', 'texto_original', 'texto_normalizado')})
            write(outputs[0], ''.join(json.dumps(s, ensure_ascii=False) + '\n' for s in segments))
            write(outputs[1], f'# Capítulo {n:02d}: {ep["titulo"]}\n\nTranscripción derivada, no resumen. Voz y hablante sin identificar automáticamente.\n\n' +
                  '\n\n'.join(f'[{s["inicio"]}] {s["texto_normalizado"]}' for s in segments) + '\n')
            write_json(outputs[2], changes)
            write_json(meta_file, {'fingerprint': fingerprint, 'fuente': source.relative_to(ROOT).as_posix(),
                'sha256': sha(source), 'segmentos': len(segments), 'inicio': segments[0]['inicio'],
                'fin': segments[-1]['fin'], 'cambios': len(changes)})
        meta = read_json(meta_file)
        dossier = KB / 'capitulos' / f'{n:02d}.json'
        review = 'pendiente'
        if dossier.exists():
            data = read_json(dossier)
            review = data.get('estado_revision', 'pendiente')
            if data.get('fuente_sha256') != sha(source):
                review = 'requiere_revision_fuente_cambiada'
            for fact in data.get('afirmaciones', []):
                validate_fact(fact, source)
            render_dossier(ep, data, tracking, chapter_histories.get(n))
        record.update(estado_fuente='disponible', revision=review, **meta)
        manifest.append(record)
    write_json(BUILD / 'inventario.json', manifest)
    render_indexes(manifest)
    render_tracking(tracking)
    from organizar import render_views
    render_views()
    if (ROOT / 'web/plantilla.html').exists():
        from construir_interfaz import main as build_interface
        build_interface()
    print(f'{sum(e["estado_fuente"] == "disponible" for e in manifest)}/{len(manifest)} capítulos con VTT; '
          f'{sum(e.get("revision") == "revisado" for e in manifest)} fichas revisadas.')


def validate_fact(fact, source):
    categories = {'hecho_confirmado', 'declaracion_personaje', 'especulacion_jugadores', 'desconocido', 'explicacion_director'}
    if fact['tipo'] not in categories:
        raise ValueError(f'Tipo inválido: {fact["id"]}')
    if fact['conocimiento_personaje'] not in ('atestiguado', 'no_atestiguado', 'desconocido'):
        raise ValueError(f'Conocimiento inválido: {fact["id"]}')
    if seconds(fact['fin']) < seconds(fact['inicio']):
        raise ValueError(f'Intervalo invertido: {fact["id"]}')
    # La cita debe existir literalmente en el intervalo del VTT original (sin etiquetas).
    raw = source.read_text(encoding='utf-8-sig')
    texts = []
    for block in re.split(r'\n{2,}', raw.replace('\r\n', '\n')):
        match = TIMING.search(block)
        if match and seconds(fact['inicio']) <= seconds(match[1]) <= seconds(fact['fin']):
            texts.append(html.unescape(re.sub(r'<[^>]*>', '', block[match.end():])))
    evidence = re.sub(r'\s+', ' ', ' '.join(texts)).strip()
    quote = re.sub(r'\s+', ' ', fact['cita']).strip()
    if quote not in evidence:
        raise ValueError(f'Cita no localizada en intervalo: {fact["id"]}: {quote}')


def render_dossier(ep, data, tracking=None, history=None):
    from catalogo import load_catalog, canonical_labels
    aliases, _, _ = load_catalog()
    lines = [f'# Capítulo {ep["capitulo"]:02d}: {ep["titulo"]}', '',
             f'Estado: **{data["estado_revision"]}**. Fuente: subtítulos automáticos, no audio verificado.', '',
             '## Relato de la sesión', '']
    if history:
        by_id = {fact['id']: fact for fact in data['afirmaciones']}
        for stage in history['etapas']:
            lines += ['### ' + stage['titulo'], '', stage['texto'], '',
                      'Fuentes: ' + ' · '.join(
                          f'[{key} · {by_id[key]["titulo"]}]({ep["url"]}&t={int(seconds(by_id[key].get("evidencia_cue", {}).get("inicio", by_id[key]["inicio"])))}s)'
                          for key in stage['referencias']) + '.', '']
    else:
        lines += [data['resumen'], '']
    lines += ['## Afirmaciones y evidencias', '']
    for fact in sorted(data.get('afirmaciones', []), key=lambda f: seconds(f['inicio'])):
        link = ep['url'] + '&t=' + str(int(seconds(fact['inicio']))) + 's'
        lines += [f'### {fact["id"]} · {fact["titulo"]}', '', fact['afirmacion'], '',
            f'- Tipo: `{fact["tipo"]}`. Confianza: {fact["confianza"]}.',
            f'- Fuente: [{fact["inicio"]}–{fact["fin"]}]({link}).',
            f'- Ámbito: {fact.get("ambito", "sin determinar")}. Conocimiento documentado de: {", ".join(fact.get("conocedores", [])) or "sin determinar"}.',
            f'- Entidades: {", ".join(canonical_labels(fact.get("entidades", []), aliases)) or "sin identificar"}.', '',
            'Cita literal de los subtítulos:', '', f'> {fact["cita"]}', '', fact.get('limitacion', ''), '']
        if fact.get('evidencia_cue'):
            cue = fact['evidencia_cue']
            cue_link = ep['url'] + '&t=' + str(int(seconds(cue['inicio']))) + 's'
            lines += [f'Cita localizada en [{cue["inicio"]}]({cue_link}); el intervalo anterior abarca el contexto de la afirmación.', '']
    for title, key in [('Misiones y resultados', 'misiones'), ('Preguntas de la sesión', 'preguntas'),
                       ('Notas de las fuentes', 'contradicciones'), ('Nombres pendientes de revisión', 'nombres_dudosos')]:
        lines += [f'## {title}', '']
        lines += [f'- {x}' for x in data.get(key, [])] or ['Sin registros en esta revisión; no implica ausencia en la campaña.']
        lines += ['']
    if tracking:
        lines += ['## Respuestas en capítulos posteriores', '']
        from seguimiento import STATES
        for question in tracking['preguntas']:
            if question['capitulo'] == ep['capitulo']:
                lines += [f'### {question["id"]} · {STATES[question["estado"]]}', '',
                          question['pregunta'], '', question['respuesta'], '']
                if question['referencias']:
                    lines += ['Evidencia posterior: ' + ', '.join(
                        f'[{fid}]({int(fid.split("-")[0]):02d}.md)' for fid in question['referencias']), '']
                if question['pendiente']:
                    lines += ['Sigue pendiente: ' + question['pendiente'], '']
                lines += [f'Revisada hasta el capítulo {question["revisado_hasta"]}. '
                          f'[Seguimiento completo](../SEGUIMIENTO.md#{question["id"].lower()}--{STATES[question["estado"]].lower().replace(" ", "-")}).', '']
    write(KB / 'capitulos' / f'{ep["capitulo"]:02d}.md', '\n'.join(lines))


def render_indexes(manifest):
    from catalogo import load_catalog, canonical_labels
    aliases, catalog, _ = load_catalog()
    rows = ['# Índice de la campaña', '',
        '[Cronología](CRONOLOGIA.md) · [Entidades](ENTIDADES.md) · [Fichas](FICHAS.md) · [Atlas](ATLAS.md) · [Facciones](FACCIONES.md) · [Relaciones](RELACIONES.md) · [Misiones](MISIONES.md) · [Tramas](TRAMAS.md) · [Preguntas y desenlaces](SEGUIMIENTO.md) · [Misterios](MISTERIOS.md) · [Progreso](PROGRESO.md) · [Guía](GUIA_CONSULTA.md)', '',
        'Las fichas reúnen acontecimientos seleccionados y citados. La tabla distingue disponibilidad de fuentes y revisión editorial; una transcripción preparada no equivale a una ficha revisada.', '',
        '| Cap. | Título | Fuente | Revisión | Lectura |', '|---|---|---|---|---|']
    facts, entities = [], {}
    for ep in manifest:
        n = ep['capitulo']
        dossier = KB / 'capitulos' / f'{n:02d}.json'
        title = f'[{ep["titulo"]}](capitulos/{n:02d}.md)' if dossier.exists() else ep['titulo']
        rows.append(f'| {n:02d} | {title} | {ep["estado_fuente"]} | {ep.get("revision", "pendiente")} | [texto](../derivados/{n:02d}/lectura.md) |')
        if dossier.exists():
            for f in read_json(dossier).get('afirmaciones', []):
                facts.append((n, f))
                for name in canonical_labels(f.get('entidades', []), aliases):
                    if name in catalog and catalog[name].get('tipo') and catalog[name].get('visible', True):
                        entities.setdefault(name, []).append((n, f))
    write(KB / 'INDICE.md', '\n'.join(rows) + '\n')
    chronology = ['# Cronología documentada', '', 'Orden de episodios y tiempos de vídeo; no equivale a calendario interno del mundo.', '']
    for n, f in sorted(facts, key=lambda item: (item[0], seconds(item[1]['inicio']))):
        chronology.append(f'- Cap. {n:02d}, {f["inicio"]}, **{f["tipo"]}**: {f["afirmacion"]} ([{f["id"]}](capitulos/{n:02d}.md)).')
    write(KB / 'CRONOLOGIA.md', '\n'.join(chronology) + '\n')
    entity_lines = ['# Entidades documentadas', '', 'Una entrada por identidad revisada, con sus variantes agrupadas. Las etiquetas de extracción sin identidad verificada no generan fichas automáticamente.', '']
    for name, mentions in sorted(entities.items()):
        entity_lines += [f'## {name}', '']
        entity_lines += [f'- Cap. {n:02d}, {f["inicio"]}: {f["titulo"]} ([{f["id"]}](capitulos/{n:02d}.md)).' for n, f in mentions]
        entity_lines += ['']
    write(KB / 'ENTIDADES.md', '\n'.join(entity_lines) + '\n')
    for filename, field in [('MISIONES', 'misiones'), ('PREGUNTAS', 'preguntas'), ('CONTRADICCIONES', 'contradicciones')]:
        items = [f'# {filename.title()}', '']
        if filename == 'PREGUNTAS':
            items += ['Historial de preguntas planteadas en cada episodio. Algunas reciben respuesta después; consultar [estado de misterios](MISTERIOS.md) y [tramas](TRAMAS.md) antes de considerarlas pendientes al cierre.', '']
        if filename == 'CONTRADICCIONES':
            items += ['Discrepancias, correcciones y cautelas editoriales fechadas por episodio. No todas son contradicciones activas: algunas son rectificaciones explícitas o límites de interpretación.', '']
        if filename == 'MISIONES':
            items += ['Historial de objetivos, resultados y consecuencias por episodio; las fichas posteriores y el seguimiento de tramas pueden actualizar su estado.', '']
        for ep in manifest:
            p = KB / 'capitulos' / f'{ep["capitulo"]:02d}.json'
            if p.exists():
                items += [f'- Cap. {ep["capitulo"]:02d}: {item} ([ficha](capitulos/{ep["capitulo"]:02d}.md)).' for item in read_json(p).get(field, [])]
        write(KB / f'{filename}.md', '\n'.join(items) + '\n')


if __name__ == '__main__':
    main()
