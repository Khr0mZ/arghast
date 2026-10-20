"""Escenas de Discord revisadas, originales y posición respecto a los directos.

El final calculado orienta la ordenación: no certifica cuándo empezó o acabó
realmente la partida. Las fechas asumidas conservan esa incertidumbre.
"""
from bisect import bisect_left
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import unicodedata

from fechas_emision import ROOT, SOURCES, load_dates, read

FOLDERS = {
    'xoltacan': ROOT / 'conocimiento/rol_escrito',
    'kuroto': ROOT / 'campanas/kuroto/conocimiento/rol_escrito',
}
UTC = timezone.utc
SCENE_ID = re.compile(r'[xk]-\d+(?:-\d+)?\Z')
MESSAGE_URL = re.compile(r'https://discord\.com/channels/\d+/\d+/\d+\Z')
CLOSE_ONLY = re.compile(r'\s*[*_~#.!\-\s]*(?:fin(?:\s+(?:de\s+)?(?:la\s+|el\s+)?(?:escena|rol))?|escena\s+(?:cerrada|finalizada))[*_~.!\-\s]*\Z', re.I)

ROLE_METHOD = '''## Rol escrito de Discord

Las [interacciones de rol escrito](rol_escrito/INDICE.md) conservan el texto original completo y un relato editorial redactado después de leer todas sus fuentes. Las lecturas se reparten por hilos o bloques sin solapamiento; sus subescenas conservan una cobertura comprobada de los mensajes, sin duplicarlos ni perder los marcadores y el contexto. Las imágenes se inspeccionan; las notas de voz conservan su audio y una transcripción automática local, identificada como tal y susceptible de errores de nombres.

Las escenas se ordenan respecto a los directos originales de Twitch. En horario de Madrid, el final se estima sumando la duración del vídeo de YouTube a la hora de referencia de la tarjeta o, en su ausencia, del calendario. El rol anterior al final estimado se coloca antes de la sesión, admitiendo retrasos; el posterior se coloca después. Ese corte operativo no certifica horas reales: la edición del vídeo, los retrasos y las fechas asumidas limitan su precisión. Sin hora o duración suficiente se conserva la orientación por día y se explica la incertidumbre. Un FIN publicado tarde permanece con la conversación que cierra.

Las retrospectivas explícitas, los sueños, los recuerdos y las visiones conservan su condición. Si no existe un ancla inequívoca para recolocar una retrospectiva, se mantiene su fecha de publicación y la nota de lectura. Las acciones suelen escribirse en negrita y los pensamientos en cursiva, pero el contexto también puede identificar cartas, telepatía o acciones en cursiva. Se conserva el formato literal y se señalan las excepciones; un pensamiento no pasa a ser conocimiento de otros personajes.

Los originales privados incluyen las respuestas JSON, los metadatos de los hilos y sus adjuntos, con SHA-256. La enciclopedia incorpora el texto de la escena, fechas, referencias y adjuntos conservados, sin los perfiles de autores ni las credenciales del bot. Los mensajes reenviados se identifican aparte. Las fuentes y las identidades de Xoltacan y Kuroto permanecen separadas, incluso cuando una escena recuerda otra isla o un mismo jugador escribe varios personajes.

Los informes por hilo enlazan identidades, arcos, relaciones y cuestiones pendientes con sus mensajes exactos. Cada cuestión conserva el contexto de sus fuentes y los cotejos enlazan las respuestas halladas en otras escenas; la ausencia de cotejo no demuestra que siga abierta después de otros capítulos. Las interacciones posteriores al último vídeo incorporado se presentan como posteriores al catálogo, con referencias a directos conocidos, sin inventar capítulos revisados.
'''


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def instant(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('Una marca temporal debe incluir zona horaria')
    return result.astimezone(UTC)


def madrid_instants(values):
    """Convierte horas civiles; Windows puede carecer de la base IANA de Python."""
    try:
        from zoneinfo import ZoneInfo
        zone = ZoneInfo('Europe/Madrid')
    except (ImportError, KeyError):
        # Intl incorpora los datos IANA del Node ya usado para probar la interfaz.
        script = r"""let s='';process.stdin.on('data',v=>s+=v);process.stdin.on('end',()=>{
          const f=new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Madrid',timeZoneName:'shortOffset'});
          process.stdout.write(JSON.stringify(Object.fromEntries(JSON.parse(s).map(v=>{
            const p=new Date(v+'Z'),z=f.formatToParts(p).find(x=>x.type==='timeZoneName').value;
            const m=z.match(/^GMT(?:([+-])(\d+)(?::(\d+))?)?$/);if(!m)throw Error(z);
            const offset=(m[1]==='-'?-1:1)*(Number(m[2]||0)*60+Number(m[3]||0));
            return [v,new Date(p.getTime()-offset*60000).toISOString()];
          }))));});"""
        result = subprocess.run(['node', '-e', script], input=json.dumps(values), text=True,
                                capture_output=True, check=True)
        return {key: instant(value) for key, value in json.loads(result.stdout).items()}
    return {v: datetime.fromisoformat(v).replace(tzinfo=zone).astimezone(UTC) for v in values}


def duration_seconds(value):
    if not value:
        return None
    parts = str(value).split(':')
    if len(parts) != 3:
        raise ValueError('Duración de vídeo incorrecta')
    seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    if seconds <= 0:
        raise ValueError('Duración de vídeo vacía')
    return seconds


def load_video_durations(campaign, chapters):
    document = read(ROOT / 'config/duraciones_rol.json')
    entries = document['campanas'][campaign]
    if set(entries) != {str(c['capitulo']) for c in chapters}:
        raise ValueError('Duraciones sin cobertura exacta del catálogo')
    sources = {}
    for ref in {e['fuente'] for e in entries.values()}:
        record = document['fuentes'][ref]
        path = safe_relative(ROOT, record['archivo'])
        if digest(path) != record['sha256']:
            raise ValueError('Metadatos originales de duración modificados')
        raw = path.read_bytes()
        metadata = json.loads(raw.decode('utf-16' if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8'))
        rows = metadata.get('entries', metadata.get('episodios', [metadata]))
        sources[ref] = {row['id']: row for row in rows}
    result = {}
    for chapter in chapters:
        entry = entries[str(chapter['capitulo'])]
        if chapter['id'] != entry['video_id']:
            raise ValueError('Duración correspondiente a otro vídeo')
        original = sources[entry['fuente']][entry['video_id']]
        seconds = original.get('duration', original.get('duracion_segundos'))
        if seconds != entry['segundos'] or not isinstance(seconds, (float, int)) or seconds <= 0:
            raise ValueError('Duración distinta de su metadato original')
        result[chapter['capitulo']] = seconds
    return result


def session_anchors(campaign, chapters, dates=None, announcements=None):
    """Conserva también directos anunciados cuyo vídeo aún no está en el catálogo."""
    durations = load_video_durations(campaign, chapters) if dates is None else {
        c['capitulo']: c.get('duracion_segundos') or duration_seconds(c.get('duracion')) for c in chapters}
    dates = load_dates(campaign, chapters) if dates is None else dates
    announcements = read(SOURCES)['anuncios'] if announcements is None else announcements
    catalog = {c['capitulo']: c for c in chapters}
    anchors = []
    for number, entry in dates.items():
        twitch = entry['twitch']
        day = twitch['fecha']
        estimate = twitch.get('estimacion', {})
        refs = list(dict.fromkeys(twitch['fuentes'] + estimate.get('fuentes', [])
                                  + estimate.get('fuentes_contraste', [])))
        notices = [dict(id=ref, **announcements[ref]) for ref in refs
                   if announcements[ref]['plataforma'] == 'twitch'
                   and announcements[ref].get('fecha_tarjeta_local') == day]
        direct = [s for s in notices if s['campana'] == campaign and s['episodio_anunciado'] == number]
        selected = min(direct or notices, key=lambda s: s.get('timestamp_tarjeta_utc') or s['aviso_utc']) if notices else None
        plans = [p for p in twitch.get('programacion', []) if p['fecha'] == day]
        start = (selected.get('timestamp_tarjeta_utc') or selected['aviso_utc']) if selected else None
        planned = min(plans, key=lambda p: p['hora']) if plans else None
        anchors.append(dict(capitulo=number, fecha=day, estado=twitch['estado'], catalogado=True,
            fuente=selected['url_discord'] if selected else planned['url_discord'] if planned else None,
            inicio_referencia_utc=start,
            hora_prevista=planned['hora'] if planned else None,
            tipo_referencia='tarjeta_twitch' if direct else 'aviso_de_contraste' if selected else 'programacion' if planned else 'solo_fecha',
            duracion_video_segundos=durations[number]))
    grouped = {}
    for ref, source in announcements.items():
        if source['campana'] == campaign and source['plataforma'] == 'twitch' and source['episodio_anunciado'] not in catalog:
            grouped.setdefault(source['episodio_anunciado'], []).append(dict(id=ref, **source))
    for number, rows in grouped.items():
        days = {s['fecha_tarjeta_local'] for s in rows}
        if len(days) != 1:
            continue
        selected = min(rows, key=lambda s: s.get('timestamp_tarjeta_utc') or s['aviso_utc'])
        anchors.append(dict(capitulo=number, fecha=next(iter(days)), estado='anunciada_sin_video',
            catalogado=False, fuente=selected['url_discord'],
            inicio_referencia_utc=selected.get('timestamp_tarjeta_utc') or selected['aviso_utc'],
            hora_prevista=None, tipo_referencia='tarjeta_twitch_sin_video', duracion_video_segundos=None))
    civil_times = [a['fecha'] + 'T' + a['hora_prevista'] + ':00' for a in anchors
                   if not a['inicio_referencia_utc'] and a['hora_prevista']]
    civil_times.extend(a['fecha'] + 'T23:59:59.999999' for a in anchors)
    converted = madrid_instants(civil_times)
    for anchor in anchors:
        if not anchor['inicio_referencia_utc'] and anchor['hora_prevista']:
            anchor['inicio_referencia_utc'] = converted[anchor['fecha'] + 'T' + anchor['hora_prevista'] + ':00'].isoformat()
        start, duration = anchor['inicio_referencia_utc'], anchor['duracion_video_segundos']
        end = instant(start) + timedelta(seconds=duration) if start and duration else None
        anchor['fin_estimado_utc'] = end.isoformat() if end else None
        # Sin duración conservamos la orientación por día y explicamos el límite.
        anchor['corte_ordenacion_utc'] = (end or converted[anchor['fecha'] + 'T23:59:59.999999']).isoformat()
    anchors.sort(key=lambda a: (a['corte_ordenacion_utc'], a['capitulo']))
    return anchors


def message_frame(source, anchors):
    return bisect_left([instant(a['corte_ordenacion_utc']) for a in anchors], instant(source['fecha_utc']))


def temporal_groups(sources, anchors):
    """Un FIN aislado conserva la posición del diálogo que cierra."""
    groups = []
    for index, source in enumerate(sources):
        frame = message_frame(source, anchors)
        marker = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in source.get('texto', ''))
        if source.get('no_narrativo') or CLOSE_ONLY.fullmatch(marker):
            if groups:
                frame = groups[-1]['frame']
            elif source.get('no_narrativo'):
                following = next((s for s in sources[index + 1:] if not s.get('no_narrativo')), None)
                if following:
                    frame = message_frame(following, anchors)
        if not groups or groups[-1]['frame'] != frame:
            groups.append({'frame': frame, 'fuentes_ids': []})
        groups[-1]['fuentes_ids'].append(source['id'])
    return groups


def scene_interval(frame, anchors):
    previous = anchors[frame - 1] if frame else None
    following = anchors[frame] if frame < len(anchors) else None
    catalog_indices = [i for i, a in enumerate(anchors) if a['catalogado']]
    scope = ('antes_del_primero' if frame <= min(catalog_indices) else
             'despues_del_catalogo' if frame > max(catalog_indices) else 'entre_capitulos')
    note = ('Ordenación por las fechas de los mensajes y los directos de Twitch. '
            'El final se estima sumando la duración del vídeo a la hora de referencia del aviso o calendario. '
            'El rol anterior a ese final estimado se sitúa antes de la sesión, admitiendo retrasos; '
            'el posterior, después. No acredita las horas reales de juego.')
    if any(a and a['estado'] == 'asumida' for a in (previous, following)):
        note += ' La posición depende de una fecha de sesión asumida.'
    if any(a and a['tipo_referencia'] == 'aviso_de_contraste' for a in (previous, following)):
        note += ' Una hora tomada de un aviso con título discrepante se utiliza solo como referencia aproximada de ese día.'
    if any(a and not a['fin_estimado_utc'] for a in (previous, following)):
        note += ' Un directo sin hora o duración suficiente solo permite orientar por el día; el rol de ese día se conserva antes.'
    return dict(anterior=previous['capitulo'] if previous else None,
                siguiente=following['capitulo'] if following else None,
                anterior_catalogado=bool(previous and previous['catalogado']),
                siguiente_catalogado=bool(following and following['catalogado']),
                anterior_fuente=previous['fuente'] if previous else None,
                siguiente_fuente=following['fuente'] if following else None,
                ambito=scope, criterio='horario_y_duracion_con_retrasos',
                confianza='fecha_de_sesion_asumida' if any(a and a['estado'] == 'asumida' for a in (previous, following)) else 'cronologica',
                referencias=[{k: a[k] for k in ('capitulo', 'fecha', 'inicio_referencia_utc', 'fin_estimado_utc',
                             'duracion_video_segundos', 'tipo_referencia', 'catalogado', 'fuente')}
                             for a in (previous, following) if a], nota=note)


def safe_relative(folder, value):
    path = (folder / value).resolve()
    if not path.is_relative_to(folder.resolve()):
        raise ValueError('Archivo de rol fuera de su campaña')
    return path


def validate_scene(scene, campaign):
    if scene['campana'] != campaign or not SCENE_ID.fullmatch(scene['id']):
        raise ValueError('Identidad de escena o campaña incorrecta')
    if not scene['id'].startswith('x-' if campaign == 'xoltacan' else 'k-'):
        raise ValueError('Escena de otra campaña')
    if scene.get('revisada') is not True or not scene.get('relato', '').strip():
        raise ValueError('Escena sin lectura y relato completos')
    sources = scene['fuentes']
    ids = [s['id'] for s in sources]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError('Escena sin fuentes o con mensajes repetidos')
    for source in sources:
        instant(source['fecha_utc'])
        if not MESSAGE_URL.fullmatch(source['url_discord']) or not source['url_discord'].endswith('/' + source['id']):
            raise ValueError('Enlace de evidencia incorrecto')
        if hashlib.sha256(source['texto'].encode('utf-8')).hexdigest() != source['texto_sha256']:
            raise ValueError('Texto original modificado')
        for forwarded in source.get('reenviados', []):
            if hashlib.sha256(forwarded['texto'].encode('utf-8')).hexdigest() != forwarded['texto_sha256']:
                raise ValueError('Texto reenviado modificado')
        for attachment in source.get('adjuntos', []):
            if not re.fullmatch(r'rol_escrito/adjuntos/\d+\.[a-z0-9]+', attachment['url']):
                raise ValueError('Adjunto fuera del archivo conservado')
    if not scene.get('evidencias') or any(e['mensaje_id'] not in ids for e in scene['evidencias']):
        raise ValueError('Relato sin evidencias de sus propios mensajes')
    if scene['estado'] not in ('cerrada', 'abierta', 'continuacion'):
        raise ValueError('Estado de escena incorrecto')


def search_words(scene):
    text = ' '.join([scene['titulo'], scene.get('resumen', ''), scene['relato'],
                     *scene.get('participantes', []), *(s['texto'] for s in scene['fuentes']),
                     *(f['texto'] for s in scene['fuentes'] for f in s.get('reenviados', [])),
                     *(a['texto'] for s in scene['fuentes'] for a in s.get('transcripciones_audio', []))])
    text = ''.join(c for c in unicodedata.normalize('NFD', text.lower()) if not unicodedata.combining(c))
    return ' '.join(sorted(set(re.findall(r'[\w]+', text))))


def load_written_role(campaign, chapters, folder=None, output=None):
    """Valida el corpus, escribe fuentes por escena y devuelve solo su índice ligero."""
    folder = Path(folder) if folder else FOLDERS[campaign]
    if not (folder / 'manifest.json').exists():
        return {'scenes': [], 'stats': {}}
    manifest = read(folder / 'manifest.json')
    if manifest['campana'] != campaign or not manifest['revision_completa']:
        raise ValueError('Archivo de rol sin revisión completa de la campaña')
    output = Path(output) if output else ROOT / 'rol_escrito'
    output.mkdir(parents=True, exist_ok=True)
    anchors = session_anchors(campaign, chapters)
    scenes, all_ids = [], set()
    for record in manifest['escenas']:
        path = safe_relative(folder, record['archivo'])
        if digest(path) != record['sha256']:
            raise ValueError('Ficha de rol modificada sin actualizar su manifest')
        scene = read(path)
        validate_scene(scene, campaign)
        ids = {s['id'] for s in scene['fuentes']}
        if ids & all_ids:
            raise ValueError('Un mensaje de rol aparece en varias escenas')
        all_ids.update(ids)
        groups = temporal_groups(scene['fuentes'], anchors)
        if len(groups) != 1:
            raise ValueError('Una escena atraviesa capítulos y necesita lectura editorial separada: ' + scene['id'])
        scene['intervalo'] = scene_interval(groups[0]['frame'], anchors)
        target = output / campaign / (scene['id'] + '.js')
        target.parent.mkdir(parents=True, exist_ok=True)
        sources_json = json.dumps(scene['fuentes'], ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
        target.write_text('globalThis.arghastWrittenRoleSources=globalThis.arghastWrittenRoleSources||{};\n'
                          + 'globalThis.arghastWrittenRoleSources[' + json.dumps(campaign + '/' + scene['id'])
                          + ']=' + sources_json + ';\n', encoding='utf-8')
        for source in scene['fuentes']:
            for attachment in source.get('adjuntos', []):
                original = safe_relative(folder, attachment['archivo'])
                if digest(original) != attachment['sha256']:
                    raise ValueError('Adjunto original de rol modificado')
                dest = output / 'adjuntos' / Path(attachment['url']).name
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists() or digest(dest) != attachment['sha256']:
                    shutil.copyfile(original, dest)
        scenes.append({**{k: v for k, v in scene.items() if k != 'fuentes'},
                       'mensajes': len(scene['fuentes']), 'busqueda': search_words(scene),
                       'notas_de_voz': sum(len(m.get('transcripciones_audio', [])) for m in scene['fuentes']),
                       'sourceFile': target.relative_to(output.parent).as_posix()})
    if len(all_ids) != manifest['estadisticas']['mensajes_en_escenas']:
        raise ValueError('Cobertura de mensajes distinta del archivo revisado')
    reports = []
    for record in manifest.get('integracion_hilos', []):
        path = safe_relative(folder, record['archivo'])
        if digest(path) != record['sha256']:
            raise ValueError('Informe de integración de rol modificado')
        report = read(path)
        if report['campana'] != campaign:
            raise ValueError('Informe de integración de otra campaña')
        for category in ('identidades', 'arcos', 'pendientes', 'relaciones'):
            if any(mid not in all_ids for item in report.get(category, []) for mid in item['pruebas']):
                raise ValueError('Informe con mensajes de otro archivo')
            if any(mid not in all_ids for item in report.get(category, [])
                   for mid in item.get('cotejo_posterior', {}).get('pruebas', [])):
                raise ValueError('Respuesta de rol con fuentes de otra campaña')
        reports.append(report)
    return {'scenes': sorted(scenes, key=lambda s: (s['inicio_utc'], s['id'])),
            'integration': reports, 'stats': manifest['estadisticas']}
