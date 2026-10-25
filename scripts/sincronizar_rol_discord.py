"""Sincronización privada e incremental de rol; solo realiza GET contra Discord.

Inicializar desde el archivo conservado no necesita token ni conexión. Cada éxito
guarda un cursor por hilo; una descarga fallida conserva el estado anterior.
"""
import argparse
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request


APPLICATION_ID = '1561698096491008081'
GUILD = '946724148628041748'
KNOWN = {'1440275050493378681': 'xoltacan', '1362069716792901843': 'kuroto'}
BASE = 'https://discord.com/api/v10'
ROOT = Path(__file__).resolve().parents[1] / '.local/discord'
STATE = 'sincronizacion_rol.json'
VIEW, HISTORY, ADMIN = 1 << 10, 1 << 16, 1 << 3


def now():
    return datetime.now(timezone.utc).isoformat()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    """Reemplazo atómico en el mismo volumen, incluido el checkpoint final."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
        stream.flush()
        os.fsync(stream.fileno())
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def inside(root, relative):
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError('Referencia fuera del archivo privado')
    return target


def reference(root, path):
    payload = path.read_bytes()
    return dict(archivo=path.resolve().relative_to(root.resolve()).as_posix(),
                sha256=hashlib.sha256(payload).hexdigest(), bytes=len(payload))


def verified(root, record):
    payload = inside(root, record['archivo']).read_bytes()
    if hashlib.sha256(payload).hexdigest() != record['sha256']:
        raise ValueError('Hash del original incorrecto')
    if 'bytes' in record and len(payload) != record['bytes']:
        raise ValueError('Tamaño del original incorrecto')
    return payload


@contextmanager
def locked(root):
    root.mkdir(parents=True, exist_ok=True)
    lock = root / 'sincronizacion_rol.lock'
    with lock.open('x', encoding='utf-8') as stream:
        stream.write(str(os.getpid()))
    try:
        yield
    finally:
        lock.unlink()


def attachments(message):
    return message.get('attachments', []) + [a for s in message.get('message_snapshots', [])
                                             for a in s['message'].get('attachments', [])]


def validate_messages(messages, channel):
    if not isinstance(messages, list) or any(m.get('channel_id') != channel for m in messages):
        raise ValueError('Mensajes fuera de canal')
    ids = [int(m['id']) for m in messages]
    if len(set(ids)) != len(ids) or any(i <= 0 for i in ids):
        raise ValueError('Identificadores duplicados o inválidos')


def thread_record(root, campaign, parent, meta, messages, path, meta_path, at):
    return dict(campana=campaign, padre=parent, nombre=meta['name'], mensajes=len(messages),
                ultimo_mensaje_id=messages[-1]['id'] if messages else None,
                ultima_fecha_mensaje_utc=messages[-1]['timestamp'] if messages else None,
                ultima_sincronizacion_utc=at, fuente_mensajes=reference(root, path),
                fuente_metadatos=reference(root, meta_path))


def bootstrap(root, folder):
    """Valida e indexa el archivo previo sin modificarlo ni consultar Discord."""
    root, folder = root.resolve(), folder.resolve()
    folder.relative_to(root)
    with locked(root):
        if (root / STATE).exists():
            raise FileExistsError('Ya existe un checkpoint; no se reinicia')
        manifest = read(folder / 'manifest.json')
        if not manifest['completo'] or manifest['servidor_id'] != GUILD:
            raise ValueError('Exportación incompleta o de otro servidor')
        at = manifest['finalizado_utc']
        requests = read(folder / manifest['respuestas_archivo'])
        for record in requests.values():
            verified(folder, record)
        initial = reference(root, folder / 'manifest.json')
        state = dict(version=1, servidor_id=GUILD, ultima_sincronizacion_utc=at,
                     origen_inicial=initial, campanas={}, hilos={}, adjuntos={},
                     historial=[], pendientes_revision=[])
        media = {a['adjunto_id']: a for a in manifest['adjuntos']}
        for name in ('adjuntos_verificados.json', 'reenviados_verificados.json'):
            if (folder / name).exists():
                companion = read(folder / name)
                if companion['manifest_original_sha256'] != initial['sha256']:
                    raise ValueError('Adjuntos de otra exportación')
                media.update({a['adjunto_id']: a for a in companion['adjuntos']})
        for campaign, data in manifest['campanas'].items():
            if campaign not in KNOWN.values():
                raise ValueError('Campaña desconocida')
            state['campanas'][campaign] = dict(canales=data['canales'])
            for thread in data['hilos']:
                tid = thread['id']
                path = inside(folder, thread['archivo_mensajes'])
                messages = json.loads(verified(folder, dict(archivo=thread['archivo_mensajes'],
                                                          sha256=thread['sha256_mensajes'])))
                validate_messages(messages, tid)
                originals = []
                for page in thread['paginas']:
                    if requests[page['ruta_api']] != {k: v for k, v in page.items() if k != 'ruta_api'}:
                        raise ValueError('Índice de respuestas incoherente')
                    originals.extend(json.loads(verified(folder, page)))
                if sorted(originals, key=lambda m: int(m['id'])) != messages or len(messages) != thread['mensajes']:
                    raise ValueError('Mensajes derivados distintos del original')
                meta_path = inside(folder, thread['archivo_metadatos'])
                meta = read(meta_path)
                if tid in state['hilos'] or meta['id'] != tid or meta.get('parent_id') != thread['padre']:
                    raise ValueError('Identidad de hilo incoherente')
                for message in messages:
                    for attachment in attachments(message):
                        record = media[attachment['id']]
                        if record['campana'] != campaign:
                            raise ValueError('Adjunto de otra campaña')
                        verified(folder, record)
                        state['adjuntos'][attachment['id']] = dict(record, **reference(root, inside(folder, record['archivo'])))
                state['hilos'][tid] = thread_record(root, campaign, thread['padre'], meta,
                                                  messages, path, meta_path, at)
        if sum(t['mensajes'] for t in state['hilos'].values()) != manifest['mensajes']:
            raise ValueError('Recuento incompleto')
        if not set(KNOWN) <= {c['id'] for v in state['campanas'].values() for c in v['canales']}:
            raise ValueError('Falta una campaña')
        save(root / STATE, state)
        return state


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Discord:
    def __init__(self, token):
        self.token = token
        self.opener = urllib.request.build_opener(NoRedirect())

    def get(self, path):
        if not path.startswith('/') or '://' in path:
            raise ValueError('Ruta API no permitida')
        for attempt in range(6):
            request = urllib.request.Request(BASE + path, method='GET', headers={
                'Authorization': 'Bot ' + self.token, 'Accept': 'application/json',
                'User-Agent': 'DiscordBot (https://github.com/Khr0mZ/arghast, 1.0)'})
            try:
                with self.opener.open(request, timeout=30) as response:
                    payload = response.read()
                time.sleep(.2)
                return payload
            except urllib.error.HTTPError as error:
                try:
                    detail = json.loads(error.read())
                except ValueError:
                    detail = {}
                delay = float(detail.get('retry_after', min(2 ** attempt, 8)))
                if error.code in (429, 500, 502, 503, 504) and attempt < 5 and 0 <= delay <= 30:
                    time.sleep(delay + .3)
                    continue
                raise RuntimeError(f'Discord HTTP {error.code}; checkpoint sin avanzar') from None

    def attachment(self, attachment):
        url = urllib.parse.urlparse(attachment['url'])
        if url.scheme != 'https' or url.hostname not in ('cdn.discordapp.com', 'media.discordapp.net'):
            raise ValueError('Adjunto fuera de Discord CDN')
        request = urllib.request.Request(attachment['url'], method='GET', headers={'User-Agent': 'ArghastArchive/1.0'})
        # La credencial del bot nunca se envía al CDN ni se sigue una redirección.
        with self.opener.open(request, timeout=45) as response:
            return response.read()


class Archive:
    def __init__(self, transport, folder):
        self.transport, self.folder, self.index = transport, folder, {}

    def get(self, path):
        if path in self.index:
            return json.loads(verified(self.folder, self.index[path]))
        payload = self.transport.get(path)
        data = json.loads(payload)
        target = self.folder / f'respuestas/{len(self.index) + 1:05d}.json'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        self.index[path] = dict(reference(self.folder, target), recuperado_utc=now())
        save(self.folder / 'respuestas.json', self.index)
        return data


def permissions(base, roles, channel):
    if base & ADMIN:
        return VIEW | HISTORY
    overwrites = channel.get('permission_overwrites', [])
    everyone = next((o for o in overwrites if o['id'] == GUILD and o['type'] == 0), None)
    value = (base & ~int(everyone['deny'])) | int(everyone['allow']) if everyone else base
    allow, deny = 0, 0
    for entry in overwrites:
        if entry['type'] == 0 and entry['id'] in roles:
            allow |= int(entry['allow'])
            deny |= int(entry['deny'])
    value = (value & ~deny) | allow
    own = next((o for o in overwrites if o['id'] == APPLICATION_ID and o['type'] == 1), None)
    return (value & ~int(own['deny'])) | int(own['allow']) if own else value


def archived(api, channel, private=False):
    result, before = {}, None
    suffix = 'users/@me/threads/archived/private' if private else 'threads/archived/public'
    while True:
        path = f'/channels/{channel}/{suffix}?limit=100'
        if before:
            path += '&before=' + urllib.parse.quote(before, safe='')
        data = api.get(path)
        for thread in data['threads']:
            if thread['parent_id'] != channel or thread['id'] in result:
                raise ValueError('Paginación de hilos incoherente')
            result[thread['id']] = thread
        if not data['has_more']:
            return result
        if not data['threads']:
            raise ValueError('Paginación de hilos incompleta')
        cursor = str(min(int(t['id']) for t in data['threads'])) if private else min(
            t['thread_metadata']['archive_timestamp'] for t in data['threads'])
        if before and (int(cursor) >= int(before) if private else cursor >= before):
            raise ValueError('La paginación de hilos no avanza')
        before = cursor


def discover(api, state):
    member = api.get(f'/guilds/{GUILD}/members/{APPLICATION_ID}')
    roles = api.get(f'/guilds/{GUILD}/roles')
    base = 0
    for role in roles:
        if role['id'] == GUILD or role['id'] in member['roles']:
            base |= int(role['permissions'])
    channels = api.get(f'/guilds/{GUILD}/channels')
    active = api.get(f'/guilds/{GUILD}/threads/active')['threads']
    selected, found = {}, {}
    prior = {c['id']: campaign for campaign, data in state['campanas'].items() for c in data['canales']}
    for channel in channels:
        name = ''.join(c for c in unicodedata.normalize('NFD', channel.get('name', '').lower())
                       if unicodedata.category(c) != 'Mn')
        campaign = KNOWN.get(channel['id']) or prior.get(channel['id'])
        if not campaign and 'rol' in name:
            campaign = next((c for c in KNOWN.values() if c in name), None)
        if not campaign or channel['type'] not in (0, 5, 15, 16):
            continue
        if permissions(base, set(member['roles']), channel) & (VIEW | HISTORY) != VIEW | HISTORY:
            raise ValueError('Un canal de rol no permite leer su historial')
        selected[channel['id']] = (campaign, channel)
        threads = archived(api, channel['id'])
        threads.update({t['id']: t for t in active if t['parent_id'] == channel['id']})
        if channel['type'] in (0, 5):
            threads.update(archived(api, channel['id'], private=True))
            threads[channel['id']] = channel
        for tid, thread in threads.items():
            if thread.get('guild_id', GUILD) != GUILD or tid in found:
                raise ValueError('Hilo de otro servidor o campaña')
            found[tid] = (campaign, channel['id'], thread)
    if not (set(prior) | set(KNOWN)) <= set(selected):
        raise ValueError('Faltan canales previamente sincronizados')
    for tid, record in state['hilos'].items():
        if tid not in found:
            # Un hilo privado/inaccesible no puede convertirse en un éxito vacío.
            meta = api.get(f'/channels/{tid}')
            if meta.get('guild_id', GUILD) != GUILD or meta.get('parent_id') != record['padre']:
                raise ValueError('Hilo ausente o trasladado')
            found[tid] = (record['campana'], record['padre'], meta)
    return selected, found


def fetch_messages(api, tid, old, overlap=100):
    """Recorre hacia atrás hasta el cursor y una ventana acotada de ediciones.

    Discord devuelve del más nuevo al más antiguo. Usar before evita saltarse
    páginas cuando se han escrito más de cien mensajes desde la última descarga.
    """
    lower = int(old[-min(overlap, len(old))]['id']) if old else 0
    found, before = {}, None
    while True:
        path = f'/channels/{tid}/messages?limit=100' + (f'&before={before}' if before else '')
        batch = api.get(path)
        validate_messages(batch, tid)
        if not batch:
            break
        ids = [int(m['id']) for m in batch]
        if before and max(ids) >= before:
            raise ValueError('La paginación de mensajes no avanza')
        for message in batch:
            if int(message['id']) >= lower:
                found[message['id']] = message
        if min(ids) <= lower:
            break
        before = min(ids)
    return found, lower


def editorial_value(message):
    """Ignora contadores y URLs CDN firmadas que cambian sin editar el texto."""
    def stable(value):
        if isinstance(value, dict):
            return {k: stable(v) for k, v in value.items()}
        if isinstance(value, list):
            return [stable(v) for v in value]
        if isinstance(value, str) and value.startswith('https://'):
            url = urllib.parse.urlsplit(value)
            if url.hostname in ('cdn.discordapp.com', 'media.discordapp.net'):
                return urllib.parse.urlunsplit((url.scheme, url.netloc, url.path, '', ''))
        return value

    value = {k: message.get(k) for k in ('id', 'channel_id', 'content', 'timestamp',
                                        'edited_timestamp', 'type', 'message_reference', 'message_snapshots', 'embeds')}
    value['attachments'] = [{k: v for k, v in a.items() if k not in ('url', 'proxy_url')}
                            for a in message.get('attachments', [])]
    return stable(value)


def sync(root, transport, overlap=100):
    if not 1 <= overlap <= 1000:
        raise ValueError('Ventana de comprobación entre 1 y 1000 mensajes')
    root = root.resolve()
    with locked(root):
        state = read(root / STATE)
        if state['version'] != 1 or state['servidor_id'] != GUILD:
            raise ValueError('Checkpoint de otro servidor o versión')
        application = json.loads(transport.get('/oauth2/applications/@me'))
        if application['id'] != APPLICATION_ID:
            raise ValueError('Otra aplicación; no se consulta el servidor')
        if not int(application.get('flags', 0)) & ((1 << 18) | (1 << 19)):
            raise ValueError('Message Content Intent no está habilitado')
        folder = root / 'fuentes/rol_incremental' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        folder.mkdir(parents=True, exist_ok=False)
        (folder / 'estado_anterior.json').write_bytes((root / STATE).read_bytes())
        receipt = dict(version=1, servidor_id=GUILD, completo=False, iniciado_utc=now(), solo_lectura=True,
                       estado_anterior=reference(root, folder / 'estado_anterior.json'), ventana_mensajes=overlap,
                       cambios=[], revision_editorial='pendiente si hay cambios', publicado=False)
        save(folder / 'manifest.json', receipt)
        api = Archive(transport, folder)
        updated = deepcopy(state)
        selected, threads = discover(api, state)
        for campaign in KNOWN.values():
            updated['campanas'][campaign] = dict(canales=[dict(id=c['id'], nombre=c['name'], tipo=c['type'])
                for ca, c in selected.values() if ca == campaign])
        for tid, (campaign, parent, meta) in sorted(threads.items()):
            previous = state['hilos'].get(tid)
            if previous and (previous['campana'], previous['padre']) != (campaign, parent):
                raise ValueError('Identidad de campaña alterada')
            old = json.loads(verified(root, previous['fuente_mensajes'])) if previous else []
            validate_messages(old, tid)
            old = sorted(old, key=lambda m: int(m['id']))
            if previous and previous['ultimo_mensaje_id'] != (old[-1]['id'] if old else None):
                raise ValueError('Cursor distinto del archivo verificado')
            fetched, lower = fetch_messages(api, tid, old, overlap)
            merged = {m['id']: m for m in old}
            absent = set(previous.get('ausentes_en_comprobacion', [])) if previous else set()
            for mid, message in fetched.items():
                kind = 'nuevo' if mid not in merged else ('editado' if editorial_value(message) != editorial_value(merged[mid]) else None)
                if mid in absent:
                    kind = kind or 'reaparecido'
                    absent.remove(mid)
                if kind:
                    receipt['cambios'].append(dict(campana=campaign, hilo_id=tid, mensaje_id=mid, tipo=kind))
                merged[mid] = message
                for attachment in attachments(message):
                    aid = attachment['id']
                    if aid in updated['adjuntos']:
                        if updated['adjuntos'][aid]['campana'] != campaign:
                            raise ValueError('Adjunto compartido entre campañas')
                        verified(root, updated['adjuntos'][aid])
                        continue
                    payload = transport.attachment(attachment)
                    target = folder / 'adjuntos' / aid
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(payload)
                    if len(payload) != attachment['size']:
                        save(folder / 'adjuntos_pendientes.json', dict(adjunto_id=aid, nombre=attachment['filename'],
                            bytes_declarados=attachment['size'], **reference(root, target)))
                        raise ValueError('Tamaño del adjunto diferente al declarado; requiere revisión')
                    updated['adjuntos'][aid] = dict(adjunto_id=aid, campana=campaign, canal_id=tid,
                        mensaje_id=mid, nombre=attachment['filename'], tipo=attachment.get('content_type'),
                        **reference(root, target))
            for message in old:
                if int(message['id']) >= lower and message['id'] not in fetched:
                    if message['id'] not in absent:
                        receipt['cambios'].append(dict(campana=campaign, hilo_id=tid, mensaje_id=message['id'],
                            tipo='ausente_en_comprobacion', nota='Se conserva el original; requiere revisión.'))
                    absent.add(message['id'])
            messages = sorted(merged.values(), key=lambda m: int(m['id']))
            path, meta_path = folder / f'mensajes/{campaign}/{tid}.json', folder / f'canales/{campaign}/{tid}.json'
            save(path, messages)
            save(meta_path, meta)
            updated['hilos'][tid] = thread_record(root, campaign, parent, meta, messages, path, meta_path, now())
            updated['hilos'][tid]['ausentes_en_comprobacion'] = sorted(absent, key=int)
        at = now()
        receipt.update(completo=True, finalizado_utc=at,
                       hilos=len(updated['hilos']), mensajes=sum(t['mensajes'] for t in updated['hilos'].values()),
                       nuevos=sum(c['tipo'] == 'nuevo' for c in receipt['cambios']),
                       editados=sum(c['tipo'] == 'editado' for c in receipt['cambios']))
        save(folder / 'manifest.json', receipt)
        receipt_ref = reference(root, folder / 'manifest.json')
        updated['historial'].append(receipt_ref)
        if receipt['cambios']:
            updated['pendientes_revision'].append(receipt_ref)
        updated['ultima_sincronizacion_utc'] = at
        save(root / STATE, updated)  # Único avance; todos los mensajes y adjuntos ya están verificados.
        return updated


def summary(state):
    return dict(ultima_sincronizacion_utc=state['ultima_sincronizacion_utc'],
                hilos=len(state['hilos']), mensajes=sum(t['mensajes'] for t in state['hilos'].values()),
                adjuntos=len(state['adjuntos']), importaciones_pendientes_revision=len(state['pendientes_revision']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('accion', choices=('inicializar', 'estado', 'sincronizar'))
    parser.add_argument('--archivo', type=Path, help='Carpeta de la exportación completa existente')
    parser.add_argument('--ventana', type=int, default=100, help='Mensajes previos por hilo que se vuelven a comprobar')
    args = parser.parse_args()
    if args.accion == 'inicializar':
        folder = args.archivo or Path(read(ROOT / 'rol_archivo_actual.json')['carpeta'])
        state = bootstrap(ROOT, folder)
    elif args.accion == 'estado':
        state = read(ROOT / STATE)
    else:
        token = sys.stdin.read().strip()
        if not re.fullmatch(r'[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', token):
            raise ValueError('Token local incompleto')
        state = sync(ROOT, Discord(token), args.ventana)
    print(json.dumps(summary(state), ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps(dict(resultado='sin_completar', tipo=type(error).__name__, checkpoint_sin_avanzar=True)))
        raise SystemExit(1)
