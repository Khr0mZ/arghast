"""Fechas documentadas de Twitch y YouTube, separadas del canon narrativo."""
from datetime import date, datetime, time
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'config/fuentes_anuncios_discord.json'
ESTIMATES = ROOT / 'config/estimaciones_emisiones.json'
PROGRAMMING = ROOT / 'config/programacion_twitch.json'
CAMPAIGNS = {
    'xoltacan': ROOT / 'config/emisiones_xoltacan.json',
    'kuroto': ROOT / 'campanas/kuroto/revision/emisiones.json',
}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def validate_estimate(estimate, campaign, evidence):
    start, end = date.fromisoformat(estimate['desde']), date.fromisoformat(estimate['hasta'])
    if start > end:
        raise ValueError('Intervalo estimado invertido')
    probable = estimate.get('fecha_probable')
    if probable and not start <= date.fromisoformat(probable) <= end:
        raise ValueError('Día probable fuera del intervalo estimado')
    if estimate.get('confianza') not in ('media', 'baja') or not estimate.get('fundamento'):
        raise ValueError('Estimación sin grado de confianza o fundamento')
    if estimate.get('sirve_como_corte_exacto') is not False:
        raise ValueError('Una estimación no fija un corte exacto entre escenas')
    refs = estimate.get('fuentes', [])
    if not refs:
        raise ValueError('Estimación sin anuncios de referencia')
    for ref in refs:
        source = evidence[ref]
        if source['campana'] != campaign or source['plataforma'] != 'twitch':
            raise ValueError('Estimación con fuente de otra campaña o plataforma')
    for ref in estimate.get('fuentes_contraste', []):
        if evidence[ref]['plataforma'] != 'twitch':
            raise ValueError('El contraste de un directo debe conservar un aviso de Twitch')
    known_dates = [date.fromisoformat(evidence[ref]['fecha_tarjeta_local']) for ref in refs]
    if start < min(known_dates) or end > max(known_dates):
        raise ValueError('Intervalo estimado fuera de los anuncios de referencia')


def load_programming(path=None):
    path = Path(path) if path else PROGRAMMING
    if not path.exists():
        return {'fuentes': {}, 'advertencias': {}}
    document = read(path)
    if document['zona_horaria'] != 'Europe/Madrid':
        raise ValueError('Zona horaria incorrecta en la programación')
    for ref, source in document['fuentes'].items():
        if source['tipo'] != 'programacion_twitch' or not source['url_discord'].endswith('/' + ref):
            raise ValueError('Fuente de programación incorrecta')
        datetime.fromisoformat(source['aviso_utc'])
        if source.get('editado_utc'):
            datetime.fromisoformat(source['editado_utc'])
        for row in source['sesiones']:
            date.fromisoformat(row['fecha'])
            time.fromisoformat(row['hora'])
            if row['campana'] not in CAMPAIGNS or not isinstance(row['capitulo'], int) or row['capitulo'] < 1:
                raise ValueError('Campaña o capítulo incorrectos en la programación')
    return document


def programming_for(document, campaign, number):
    return [dict(fecha=row['fecha'], hora=row['hora'], fuente=ref,
                 url_discord=source['url_discord'], aviso_utc=source['aviso_utc'],
                 editado_utc=source.get('editado_utc'))
            for ref, source in document['fuentes'].items() for row in source['sesiones']
            if row['campana'] == campaign and row['capitulo'] == number]


def load_dates(campaign, chapters, path=None, source_path=None, estimate_path=None, programming_path=None):
    """Rechaza fechas sin evidencia, asociaciones entre campañas y vídeos ajenos."""
    path = Path(path) if path else CAMPAIGNS[campaign]
    if not path.exists():
        return {}
    document = read(path)
    sources = read(Path(source_path) if source_path else SOURCES)
    evidence = sources['anuncios']
    estimates_file = Path(estimate_path) if estimate_path else ESTIMATES
    estimates = read(estimates_file)['campanas'].get(campaign, {}) if estimates_file.exists() else {}
    programming = load_programming(programming_path)
    if document['campana'] != campaign or document['zona_horaria'] != 'Europe/Madrid':
        raise ValueError('Campaña o zona horaria incorrecta en las emisiones')
    catalog = {c['capitulo']: c for c in chapters}
    if set(document['capitulos']) != {str(n) for n in catalog}:
        raise ValueError('La cronología no cubre exactamente los capítulos del catálogo')
    result = {}
    for key, entry in document['capitulos'].items():
        chapter = catalog[int(key)]
        if entry['video_id'] != chapter['id']:
            raise ValueError('Fecha asociada a otro vídeo de YouTube')
        for platform in ('twitch', 'youtube'):
            item = entry[platform]
            refs = item['fuentes']
            for ref in refs:
                source = evidence[ref]
                if source['campana'] != campaign or source['plataforma'] != platform:
                    raise ValueError('Fuente de otra campaña o plataforma en las emisiones')
                datetime.fromisoformat(source['aviso_utc'])
                if source.get('timestamp_tarjeta_utc'):
                    datetime.fromisoformat(source['timestamp_tarjeta_utc'])
                if platform == 'youtube' and source['video_id'] != chapter['id']:
                    raise ValueError('Aviso de YouTube correspondiente a otro vídeo')
                if platform == 'twitch' and item['estado'] == 'documentada' and source['episodio_anunciado'] != int(key):
                    raise ValueError('Número del directo distinto del capítulo asociado')
            if item.get('fecha'):
                date.fromisoformat(item['fecha'])
                if platform == 'twitch':
                    if item['estado'] == 'asumida':
                        pass  # Se valida abajo contra la estimación y su aceptación explícita.
                    elif item['estado'] != 'documentada' or not refs:
                        raise ValueError('Fecha de Twitch sin asociación documentada')
                    elif {evidence[ref]['fecha_tarjeta_local'] for ref in refs} != {item['fecha']}:
                        raise ValueError('Los avisos de Twitch no acreditan una fecha única')
                elif item.get('origen_fecha') == 'timestamp_tarjeta_youtube':
                    if not refs or item['fecha'] not in {evidence[r].get('fecha_tarjeta_local') for r in refs}:
                        raise ValueError('Fecha de YouTube sin timestamp de tarjeta')
                elif item.get('origen_fecha') == 'metadatos_youtube':
                    source_file = (ROOT / item['archivo_metadatos']).resolve()
                    if not source_file.is_relative_to(ROOT) or hashlib.sha256(source_file.read_bytes()).hexdigest() != item['sha256_metadatos']:
                        raise ValueError('Metadatos originales de YouTube modificados')
                    metadata = read(source_file)
                    if metadata['id'] != chapter['id'] or metadata['upload_date'] != item['fecha'].replace('-', ''):
                        raise ValueError('Fecha de publicación distinta de los metadatos de YouTube')
                else:
                    raise ValueError('El aviso no acredita por sí solo la fecha de publicación en YouTube')
            if platform == 'twitch' and item['estado'] not in ('documentada', 'asumida') and item.get('fecha') is not None:
                raise ValueError('Una fecha pendiente no puede mostrarse como confirmada')
        youtube = entry['youtube']
        if youtube.get('fecha_aviso') and youtube['fecha_aviso'] != min(evidence[r]['fecha_aviso_local'] for r in youtube['fuentes']):
            raise ValueError('Fecha del aviso de YouTube distinta de su fuente')
        estimate = estimates.get(key)
        plans = programming_for(programming, campaign, int(key))
        if estimate:
            if entry['twitch'].get('fecha') and entry['twitch']['estado'] != 'asumida':
                raise ValueError('No se superpone una estimación a una fecha documentada')
            validate_estimate(estimate, campaign, evidence)
            if not set(estimate.get('fuentes_programacion', [])) <= {p['fuente'] for p in plans}:
                raise ValueError('Programación de otra campaña o capítulo en la estimación')
            entry = {**entry, 'twitch': {**entry['twitch'], 'estimacion': estimate}}
        if entry['twitch']['estado'] == 'asumida':
            assumed = entry['twitch'].get('asuncion', {})
            if not estimate or not estimate.get('fecha_probable') or entry['twitch'].get('fecha') != estimate['fecha_probable']:
                raise ValueError('La fecha asumida debe coincidir con el día probable elegido')
            correction = assumed.get('criterio') == 'corregir_correspondencia_por_calendario'
            if assumed.get('autorizada_por_usuario') is not True or assumed.get('criterio') not in ('aceptar_dia_probable', 'corregir_correspondencia_por_calendario'):
                raise ValueError('Fecha asumida sin aceptación explícita del día probable')
            if correction:
                previous = assumed.get('fecha_anterior')
                original_dates = {evidence[r]['fecha_tarjeta_local'] for r in entry['twitch']['fuentes']}
                if (assumed.get('estado_anterior') != 'documentada' or not previous or original_dates != {previous}
                        or not assumed.get('motivo') or previous == entry['twitch']['fecha']
                        or entry['twitch']['fecha'] not in {p['fecha'] for p in plans}):
                    raise ValueError('Corrección sin correspondencia anterior conservada y calendario coincidente')
            elif assumed.get('fecha_anterior') is not None or assumed.get('estado_anterior') in (None, 'documentada', 'asumida'):
                raise ValueError('La aceptación no sustituye una fecha documentada')
        if plans:
            entry = {**entry, 'twitch': {**entry['twitch'], 'programacion': plans}}
        warning = programming.get('advertencias', {}).get(campaign, {}).get(key)
        if warning:
            entry = {**entry, 'twitch': {**entry['twitch'], 'advertencia_programacion': warning}}
        ids = list(dict.fromkeys([r for platform in ('twitch', 'youtube') for r in entry[platform]['fuentes']] + (estimate['fuentes'] + estimate.get('fuentes_contraste', []) if estimate else [])))
        result[int(key)] = {**entry, 'evidencias': [dict(id=r, **evidence[r]) for r in ids]}
    return result


def attach_dates(campaign, chapters):
    dates = load_dates(campaign, chapters)
    for chapter in chapters:
        if chapter['capitulo'] in dates:
            chapter['emision'] = dates[chapter['capitulo']]


def calendar_date(value):
    return date.fromisoformat(value).strftime('%d/%m/%Y')


def estimate_label(estimate):
    if estimate.get('fecha_probable'):
        return 'aprox. ' + calendar_date(estimate['fecha_probable'])
    return calendar_date(estimate['desde']) + '–' + calendar_date(estimate['hasta']) + ' (estimado)'


def markdown_dates(entry):
    if not entry:
        return []
    twitch, youtube = entry['twitch'], entry['youtube']
    estimate = twitch.get('estimacion')
    twitch_label = calendar_date(twitch['fecha']) if twitch.get('fecha') else estimate_label(estimate) if estimate else 'fecha por confirmar'
    lines = [f'- **Directo en Twitch:** {twitch_label}. {twitch["nota"]}']
    if twitch['estado'] == 'asumida':
        lines.append('- **Procedencia de la fecha:** día probable adoptado para la cronología. No se asume una hora real de inicio.')
        if twitch['asuncion']['criterio'] == 'corregir_correspondencia_por_calendario':
            lines.append(f'- **Corrección de correspondencia:** se conservó el aviso del {calendar_date(twitch["asuncion"]["fecha_anterior"])}; se adopta el día del calendario porque se asume una rotulación anterior. El timestamp del aviso original no cambia.')
    for plan in twitch.get('programacion', []):
        lines.append(f'- **Programación prevista en Twitch:** {calendar_date(plan["fecha"])} a las {plan["hora"]}. '
                     f'[Calendario semanal]({plan["url_discord"]}). No acredita la realización ni la hora real de inicio.')
    if twitch.get('advertencia_programacion'):
        lines.append('- **Discrepancia entre fuentes:** ' + twitch['advertencia_programacion'])
    if estimate:
        label = 'Estimación de origen' if twitch['estado'] == 'asumida' else 'Estimación'
        lines.append(f'- **{label}:** intervalo {calendar_date(estimate["desde"])}–{calendar_date(estimate["hasta"])}; confianza {estimate["confianza"]}. {estimate["fundamento"]} No fija la hora de la sesión ni un corte exacto para el rol escrito.')
    if youtube.get('fecha'):
        lines.append(f'- **Publicación en YouTube:** {calendar_date(youtube["fecha"])}.')
    elif youtube.get('fecha_aviso'):
        lines.append(f'- **Aviso de publicación en YouTube:** {calendar_date(youtube["fecha_aviso"])}. No fija la fecha exacta de publicación.')
    else:
        lines.append('- **YouTube:** fecha de publicación sin documentar en los anuncios conservados.')
    sources = read(SOURCES)['anuncios']
    ids = list(dict.fromkeys([ref for platform in ('twitch', 'youtube') for ref in entry[platform]['fuentes']] + (estimate['fuentes'] + estimate.get('fuentes_contraste', []) if estimate else [])))
    links = [f'[{"Twitch" if sources[ref]["plataforma"] == "twitch" else "YouTube"} · anuncio {ref}]({sources[ref]["url_discord"]})' for ref in ids]
    if links:
        lines.append('- **Fuentes:** ' + ' · '.join(links) + '.')
    return lines + ['']


def verify_originals(folder):
    """Comprobación opcional local; el archivo privado no forma parte del sitio."""
    folder = Path(folder).resolve()
    public = read(SOURCES)
    manifest_path = folder / 'manifest.json'
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != public['archivo_original']['manifest_sha256']:
        raise ValueError('Manifiesto original distinto del revisado')
    manifest = read(manifest_path)
    seen = set()
    for page in manifest['paginas']:
        path = (folder / page['archivo']).resolve()
        if not path.is_relative_to(folder):
            raise ValueError('Página fuera del archivo original')
        payload = path.read_bytes()
        if hashlib.sha256(payload).hexdigest() != page['sha256']:
            raise ValueError('Respuesta original de Discord modificada')
        for message in json.loads(payload):
            if message['id'] in seen:
                raise ValueError('Mensaje duplicado entre páginas')
            seen.add(message['id'])
            if message['id'] in public['anuncios']:
                digest = hashlib.sha256(json.dumps(message, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
                entry = public['anuncios'][message['id']]
                if digest != entry['mensaje_sha256']:
                    raise ValueError('Evidencia derivada de otro mensaje original')
                if entry['aviso_utc'] != message['timestamp']:
                    raise ValueError('Hora del aviso distinta del original')
                embeds = [e for e in message.get('embeds', []) if e.get('title') == entry['titulo'] and e.get('url') == entry['url_plataforma']]
                if len(embeds) != 1 or embeds[0].get('timestamp') != entry.get('timestamp_tarjeta_utc'):
                    raise ValueError('Título, plataforma o timestamp distintos de la tarjeta original')
    if len(seen) != manifest['mensajes'] or not set(public['anuncios']) <= seen or not manifest['completo']:
        raise ValueError('Archivo de anuncios incompleto')
    return len(seen)


def render_estimates():
    estimates = read(ESTIMATES)
    evidence = read(SOURCES)['anuncios']
    programming = load_programming()
    adopted = adopted_days()
    lines = ['# Fechas asumidas y estimaciones de los directos de Twitch', '',
             'Se adoptan 22 fechas asumidas para la cronología por indicación del usuario. '
             'Incluyen los tres últimos casos de Kuroto y la corrección conjunta de los capítulos 55 y 56. '
             'Se conservan las estimaciones de origen; todos los capítulos catalogados tienen un día elegido. '
             'Los intervalos incluyen sus días extremos y suponen que los capítulos conservan el orden de emisión. '
             'Las fechas de publicación y los avisos de YouTube permanecen separados.', '',
             'Un día probable es una hipótesis de correspondencia. Un intervalo indica que no se elige un día. '
             'Ninguna estimación fija una hora ni un corte exacto para asignar escenas de rol escrito.', '']
    for campaign, entries in estimates['campanas'].items():
        lines += ['## ' + campaign.capitalize(), '',
                  '| Capítulo | Día asumido o intervalo | Intervalo de origen | Confianza de origen | Estado |', '|---|---|---|---|---|']
        for number, entry in entries.items():
            probable = calendar_date(entry['fecha_probable']) if entry.get('fecha_probable') else 'Solo intervalo'
            confidence = entry['confianza'] if entry.get('fecha_probable') else 'Sin día elegido'
            status = 'Fecha asumida' if number in adopted[campaign] else 'Solo intervalo'
            lines.append(f'| {number} | {probable} | {calendar_date(entry["desde"])}–{calendar_date(entry["hasta"])} | {confidence} | {status} |')
        lines += ['', '### Fundamentos y fuentes', '']
        for number, entry in entries.items():
            links = ' · '.join(f'[{evidence[ref]["titulo"]}]({evidence[ref]["url_discord"]})' for ref in entry['fuentes'])
            links += ''.join(f' · [Contraste: {evidence[ref]["titulo"]}]({evidence[ref]["url_discord"]})' for ref in entry.get('fuentes_contraste', []))
            links += ''.join(f' · [Calendario previsto]({programming["fuentes"][ref]["url_discord"]})' for ref in entry.get('fuentes_programacion', []))
            lines += [f'- **Capítulo {number}:** {entry["fundamento"]} Fuentes: {links}.']
        lines += ['']
    target = ROOT / 'conocimiento/ESTIMACIONES_EMISIONES.md'
    target.write_bytes(('\n'.join(lines) + '\n').encode('utf-8'))
    return sum(len(entries) for entries in estimates['campanas'].values())


def adopted_days():
    return {campaign: {n: entry['twitch']['fecha'] for n, entry in read(path)['capitulos'].items()
                      if entry['twitch']['estado'] == 'asumida'} for campaign, path in CAMPAIGNS.items()}


def render_date_report():
    sources = read(SOURCES)['anuncios']
    catalogs = {
        'xoltacan': read(ROOT / 'xoltacan_subtitulos/episodios.json') + read(ROOT / 'config/episodios_nuevos.json'),
        'kuroto': read(ROOT / 'campanas/kuroto/catalogo.json')['episodios'],
    }
    datasets = {campaign: load_dates(campaign, catalog) for campaign, catalog in catalogs.items()}
    documented = sum(entry['twitch']['estado'] == 'documentada' for entries in datasets.values() for entry in entries.values())
    assumed = sum(entry['twitch']['estado'] == 'asumida' for entries in datasets.values() for entry in entries.values())
    lines = ['# Fechas de emisión y publicación', '',
        f'La cronología utiliza {documented} fechas documentadas en los avisos y {assumed} fechas asumidas tras el cotejo editorial. '
        'Xoltacan tiene fecha para sus 41 capítulos y Kuroto para sus 181 capítulos catalogados. '
        'Las fechas asumidas se identifican en este informe y conservan sus [estimaciones y fuentes de origen](ESTIMACIONES_EMISIONES.md).', '',
        'Fechas civiles en Europe/Madrid. Twitch, publicación en YouTube, aviso de Discord y programación prevista se conservan separados. '
        'Aceptar el día no supone aceptar la hora programada como inicio real del rol. Véase el [cotejo de los calendarios](PROGRAMACION_TWITCH.md).', '']
    for campaign, catalog in catalogs.items():
        entries = datasets[campaign]
        lines += ['## ' + campaign.capitalize(), '',
                  '| Capítulo | Título | Directo Twitch | Publicación YouTube | Aviso YouTube |', '|---|---|---|---|---|']
        for chapter in catalog:
            number = chapter['capitulo']
            twitch, youtube = entries[number]['twitch'], entries[number]['youtube']

            def linked(value, refs):
                label = calendar_date(value) if value else 'Por confirmar'
                return f'[{label}]({sources[refs[0]]["url_discord"]})' if refs else label

            if twitch['estado'] == 'asumida':
                td = f'[{calendar_date(twitch["fecha"])}](ESTIMACIONES_EMISIONES.md) (asumida)'
            else:
                td = linked(twitch['fecha'], twitch['fuentes'])
            yd = linked(youtube.get('fecha'), youtube['fuentes'])
            ya = linked(youtube.get('fecha_aviso'), youtube['fuentes']) if youtube.get('fecha_aviso') else 'Sin aviso localizado'
            title = chapter['titulo'].replace('|', '\\|')
            lines.append(f'| {number} | {title} | {td} | {yd} | {ya} |')
        pending = [(n, entry['twitch']) for n, entry in entries.items() if not entry['twitch']['fecha']]
        if pending:
            lines += ['', '### Fechas de Twitch sin día elegido', '']
            for number, twitch in pending:
                lines += [f'- Capítulo {number}: {estimate_label(twitch["estimacion"])}. {twitch["estimacion"]["fundamento"]}']
        lines += ['']
    lines += ['## Límites de las fuentes', '',
        '- Kuroto 92 tiene un aviso de Twitch del 13/03/2025, pero sigue sin vídeo ni transcripción y no se crea una sesión revisada.',
        '- Kuroto 72–74 comparten directo con Diceland; la apertura de Twitch no fija el comienzo del rol.',
        '- Kuroto 55 adopta el 09/10/2024 y el 56 el 10/10/2024 como hipótesis conjunta basada en el calendario y en títulos arrastrados. El aviso original del 55 permanece fechado el día 10 y no se convierte en prueba del día 9.',
        '- Twitch 72 del 16/10/2026 no corresponde a YouTube 40 del 18/10/2026. La campaña, el número y las fuentes se cotejan por separado.', '']
    (ROOT / 'conocimiento/EMISIONES.md').write_bytes(('\n'.join(lines) + '\n').encode('utf-8'))
    return sum(map(len, catalogs.values()))


def verify_programming_originals(folder):
    """Verifica páginas originales y los 43 calendarios seleccionados; no exporta datos privados."""
    folder = Path(folder).resolve()
    public = load_programming()
    manifest_path = folder / 'manifest.json'
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != public['archivo_original']['manifest_sha256']:
        raise ValueError('Manifiesto de información distinto del revisado')
    manifest = read(manifest_path)
    messages = {}
    for page in manifest['paginas']:
        path = (folder / page['archivo']).resolve()
        if not path.is_relative_to(folder) or hashlib.sha256(path.read_bytes()).hexdigest() != page['sha256']:
            raise ValueError('Página original de información modificada')
        for message in read(path):
            if message['id'] in messages:
                raise ValueError('Mensaje duplicado en información')
            messages[message['id']] = message
    if len(messages) != manifest['mensajes'] or not manifest['completo']:
        raise ValueError('Archivo de información incompleto')
    for ref, source in {**public['fuentes'], **public.get('avisos', {})}.items():
        message = messages[ref]
        digest = hashlib.sha256(json.dumps(message, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
        if digest != source['mensaje_sha256'] or message['timestamp'] != source['aviso_utc'] or message.get('edited_timestamp') != source.get('editado_utc'):
            raise ValueError('Fuente de información distinta del mensaje original')
        if 'adjunto' in source:
            attachment = source['adjunto']
            original = next(a for a in message['attachments'] if a['id'] == attachment['id'])
            path = (folder / attachment['archivo']).resolve()
            if original['filename'] != attachment['nombre'] or not path.is_relative_to(folder) or hashlib.sha256(path.read_bytes()).hexdigest() != attachment['sha256']:
                raise ValueError('Calendario original modificado')
    return dict(mensajes=len(messages), calendarios=len(public['fuentes']))


def render_programming():
    document = load_programming()
    estimates = read(ESTIMATES)['campanas']
    adopted = adopted_days()
    lines = ['# Calendarios de Twitch contrastados con los avisos de directo', '',
        'Se ha leído el texto completo de los 193 mensajes disponibles del canal de información y se han revisado visualmente 43 de sus 149 adjuntos, seleccionados en las ventanas de los 21 capítulos pendientes. Los canales de información de Xoltacan y Kuroto también se han leído completos (3 y 1 mensajes). No contienen un registro de todas las emisiones realizadas.', '',
        'Los calendarios documentan programación prevista. La cronología conserva 200 fechas documentadas y adopta 22 fechas asumidas, por indicación del usuario. Los capítulos 49, 56 y 134 de Kuroto quedan fechados; también se corrige la correspondencia del 55 para conservar la secuencia prevista del 9 y 10 de octubre. No quedan capítulos catalogados sin día elegido. La zona Europe/Madrid se asume por el contexto; no está impresa en los calendarios. Las horas previstas no son horas reales de inicio ni cortes exactos para el rol escrito.', '',
        'El lateral de YouTube indica días de subida. Se mantiene separado de las filas y horas de los directos de Twitch.', '']
    for campaign, entries in estimates.items():
        lines += ['## ' + campaign.capitalize(), '', '| Capítulo | Programación prevista | Fecha adoptada o intervalo |', '|---|---|---|']
        for number, estimate in entries.items():
            plans = programming_for(document, campaign, int(number))
            labels = ' · '.join(f'[{calendar_date(p["fecha"])} {p["hora"]}]({p["url_discord"]})' for p in plans)
            label = calendar_date(adopted[campaign][number]) + ' (asumida)' if number in adopted[campaign] else estimate_label(estimate)
            lines.append(f'| {number} | {labels} | {label} |')
        lines += ['']
        for number, estimate in entries.items():
            lines += [f'- **Capítulo {number}:** {estimate["fundamento"]}']
        lines += ['']
    lines += ['## Discrepancias que impiden tratar un calendario como prueba de emisión', '',
        '- Kuroto 12 se programa primero para el 2 de mayo y luego para el 7; el aviso de directo es del 7. Se conservan ambos calendarios.',
        '- Kuroto 42 figura previsto para el 2 de septiembre, mientras su aviso de directo es del 3; además cambia el título frente al vídeo.',
        '- ' + document['advertencias']['kuroto']['55'],
        '- Kuroto 132 y 133 tampoco siguen exactamente la numeración prevista de la semana del 23 al 29 de junio de 2025. Los avisos de directo prevalecen como evidencia de emisión.', '',
        '## Cancelación de la semana del 22 al 28 de junio de 2026', '']
    for source in document.get('avisos', {}).values():
        lines += [source['lectura'] + f' [Aviso original]({source["url_discord"]}).', '']
    lines += ['## Conservación y verificación', '',
        '`config/programacion_twitch.json` conserva las lecturas, identificadores, fechas de publicación y edición de los mensajes, enlaces al canal y SHA-256 de cada mensaje y calendario. Los originales completos y los informes de lectura permanecen en local; no se incluyen autores, credenciales ni el historial privado en la biblioteca pública.', '',
        'La lectura visual es una transcripción editorial: el hash verifica el original conservado, no sustituye su cotejo humano. Las imágenes pueden editarse después de su publicación; se conserva el estado recuperado y la marca de edición de cada mensaje.', '']
    target = ROOT / 'conocimiento/PROGRAMACION_TWITCH.md'
    target.write_bytes(('\n'.join(lines) + '\n').encode('utf-8'))
    return len(document['fuentes'])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--originales', type=Path)
    parser.add_argument('--informe-estimaciones', action='store_true')
    parser.add_argument('--originales-informacion', type=Path)
    parser.add_argument('--informe-programacion', action='store_true')
    parser.add_argument('--informe-emisiones', action='store_true')
    args = parser.parse_args()
    if args.originales:
        print(f'Originales verificados: {verify_originals(args.originales)} mensajes.')
    if args.informe_estimaciones:
        print(f'Estimaciones presentadas con sus límites: {render_estimates()}.')
    if args.originales_informacion:
        print(f'Información original verificada: {verify_programming_originals(args.originales_informacion)}.')
    if args.informe_programacion:
        print(f'Calendarios presentados: {render_programming()}.')
    if args.informe_emisiones:
        print(f'Capítulos en el informe de fechas: {render_date_report()}.')
