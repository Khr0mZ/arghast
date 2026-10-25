"""Comprueba continuación, integridad y fallos sin conexión ni credenciales."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
import urllib.parse

from sincronizar_rol_discord import (APPLICATION_ID, GUILD, HISTORY, KNOWN, STATE, VIEW,
    Archive, archived, bootstrap, editorial_value, read, reference, save, summary, sync, verified)


X, K = list(KNOWN)
AT = '2026-10-20T15:26:05+00:00'


def message(mid, channel='10', text='Ione: Hola.'):
    # Fechas idénticas intencionalmente: el cursor debe ser el ID, no la fecha.
    return dict(id=str(mid), channel_id=channel, timestamp=AT, edited_timestamp=None,
                content=text, attachments=[], type=0)


def metadata(tid, parent):
    return dict(id=tid, parent_id=parent, guild_id=GUILD, name='Sala ' + tid,
                type=11, thread_metadata=dict(archived=False, archive_timestamp=AT))


class FakeDiscord:
    def __init__(self, messages, extra_threads=()):
        self.messages = deepcopy(messages)
        self.threads = [metadata('10', X), metadata('20', K)] + list(extra_threads)
        self.calls, self.media_calls = [], []
        self.fail_channel = None
        self.fail_media = False
        self.payload = b'original attachment'
        self.application = APPLICATION_ID
        self.flags = 1 << 19

    def get(self, path):
        self.calls.append(path)
        if path == '/oauth2/applications/@me':
            data = dict(id=self.application, flags=self.flags)
        elif path.endswith('/members/' + APPLICATION_ID):
            data = dict(roles=[])
        elif path.endswith('/roles'):
            data = [dict(id=GUILD, permissions=str(VIEW | HISTORY))]
        elif path == f'/guilds/{GUILD}/channels':
            data = [dict(id=cid, name=campaign + '-rol', type=15) for cid, campaign in KNOWN.items()]
        elif path.endswith('/threads/active'):
            data = dict(threads=self.threads)
        elif '/threads/archived/' in path:
            data = dict(threads=[], has_more=False)
        elif '/messages?' in path:
            tid = path.split('/')[2]
            if tid == self.fail_channel:
                raise RuntimeError('Fallo de red simulado')
            query = urllib.parse.parse_qs(urllib.parse.urlsplit(path).query)
            before = int(query.get('before', ['9999999999999999999'])[0])
            data = sorted((m for m in self.messages[tid] if int(m['id']) < before),
                          key=lambda m: int(m['id']), reverse=True)[:100]
        elif path.startswith('/channels/'):
            data = next(t for t in self.threads if t['id'] == path.split('/')[2])
        else:
            raise AssertionError('Ruta inesperada: ' + path)
        return json.dumps(data, ensure_ascii=False).encode('utf-8')

    def attachment(self, item):
        self.media_calls.append(item['id'])
        if self.fail_media:
            raise RuntimeError('Fallo CDN simulado')
        return self.payload


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / 'fuentes/rol/base'
        self.messages = {'10': [message(i) for i in range(1000, 1250)], '20': [message(2000, '20')]}
        self.seed()

    def seed(self):
        api = FakeDiscord(self.messages)
        archive = Archive(api, self.folder)
        manifest = dict(completo=True, servidor_id=GUILD, finalizado_utc=AT,
                        respuestas_archivo='respuestas.json', campanas={}, adjuntos=[], mensajes=0)
        for cid, campaign in KNOWN.items():
            tid = '10' if cid == X else '20'
            pages, before = [], None
            while True:
                route = f'/channels/{tid}/messages?limit=100' + (f'&before={before}' if before else '')
                batch = archive.get(route)
                pages.append(dict(ruta_api=route, **archive.index[route]))
                if not batch:
                    break
                before = str(min(int(m['id']) for m in batch))
            path, meta = self.folder / f'mensajes/{tid}.json', self.folder / f'canales/{tid}.json'
            save(path, self.messages[tid])
            save(meta, metadata(tid, cid))
            thread = dict(id=tid, padre=cid, mensajes=len(self.messages[tid]),
                          archivo_mensajes=path.relative_to(self.folder).as_posix(),
                          archivo_metadatos=meta.relative_to(self.folder).as_posix(),
                          sha256_mensajes=reference(self.folder, path)['sha256'], paginas=pages)
            manifest['campanas'][campaign] = dict(canales=[dict(id=cid, nombre=campaign, tipo=15)], hilos=[thread])
            manifest['mensajes'] += len(self.messages[tid])
        save(self.folder / 'manifest.json', manifest)

    def initialize(self):
        return bootstrap(self.root, self.folder)

    def test_bootstrap_uses_original_date_and_does_not_change_originals(self):
        before = {p.relative_to(self.folder): p.read_bytes() for p in self.folder.rglob('*') if p.is_file()}
        state = self.initialize()
        self.assertEqual(state['ultima_sincronizacion_utc'], AT)
        self.assertEqual(state['hilos']['10']['ultimo_mensaje_id'], '1249')
        self.assertEqual(summary(state)['mensajes'], 251)
        self.assertEqual(before, {p.relative_to(self.folder): p.read_bytes() for p in self.folder.rglob('*') if p.is_file()})
        with self.assertRaises(FileExistsError):
            self.initialize()

    def test_bootstrap_refuses_tampered_source_and_writes_no_checkpoint(self):
        response = next((self.folder / 'respuestas').iterdir())
        response.write_bytes(b'[]')
        with self.assertRaises(ValueError):
            self.initialize()
        self.assertFalse((self.root / STATE).exists())

    def test_more_than_one_page_and_same_timestamp_are_not_skipped(self):
        self.initialize()
        api = FakeDiscord(self.messages)
        api.messages['10'] += [message(i) for i in range(1250, 1601)]
        updated = sync(self.root, api)
        self.assertEqual(updated['hilos']['10']['ultimo_mensaje_id'], '1600')
        self.assertEqual(summary(updated)['mensajes'], 602)
        receipt = read(self.root / updated['historial'][-1]['archivo'])
        self.assertEqual(receipt['nuevos'], 351)
        self.assertEqual(receipt['editados'], 0)
        self.assertEqual(receipt['revision_editorial'], 'pendiente si hay cambios')
        self.assertEqual(json.loads(verified(self.root, receipt['estado_anterior']))['hilos']['10']['ultimo_mensaje_id'], '1249')
        requests = [p for p in api.calls if p.startswith('/channels/10/messages')]
        self.assertEqual(len(requests), 5)  # 351 nuevos + 100 de comprobación, no todo el historial.
        again = FakeDiscord(api.messages)
        repeated = sync(self.root, again)
        self.assertEqual(len(repeated['pendientes_revision']), 1)
        self.assertEqual(len([p for p in again.calls if p.startswith('/channels/10/messages')]), 1)
        self.assertFalse(read(self.root / repeated['historial'][-1]['archivo'])['cambios'])

    def test_discovers_new_thread_without_refetching_existing_history(self):
        self.initialize()
        api = FakeDiscord(self.messages, [metadata('30', X)])
        api.messages['30'] = [message(i, '30') for i in range(3000, 3220)]
        state = sync(self.root, api)
        self.assertEqual(state['hilos']['30']['mensajes'], 220)
        self.assertEqual(state['hilos']['30']['campana'], 'xoltacan')
        self.assertEqual(len([p for p in api.calls if p.startswith('/channels/10/messages')]), 1)

    def test_recent_edit_and_absence_preserve_previous_snapshot(self):
        initial = self.initialize()
        original = (self.root / initial['hilos']['10']['fuente_mensajes']['archivo']).read_bytes()
        api = FakeDiscord(self.messages)
        api.messages['10'][-1]['content'] = 'Ione: Otra respuesta.'
        api.messages['10'][-1]['edited_timestamp'] = '2026-10-20T16:00:00+00:00'
        del api.messages['10'][-2]
        state = sync(self.root, api)
        changes = read(self.root / state['historial'][-1]['archivo'])['cambios']
        self.assertEqual({(c['mensaje_id'], c['tipo']) for c in changes},
                         {('1249', 'editado'), ('1248', 'ausente_en_comprobacion')})
        self.assertEqual(state['hilos']['10']['mensajes'], 250)
        self.assertEqual((self.root / initial['hilos']['10']['fuente_mensajes']['archivo']).read_bytes(), original)
        state = sync(self.root, api)
        self.assertFalse(read(self.root / state['historial'][-1]['archivo'])['cambios'])
        api.messages['10'].append(message(1248))
        state = sync(self.root, api)
        self.assertEqual(read(self.root / state['historial'][-1]['archivo'])['cambios'][0]['tipo'], 'reaparecido')

    def test_failure_in_later_thread_does_not_advance_any_cursor(self):
        self.initialize()
        before = (self.root / STATE).read_bytes()
        api = FakeDiscord(self.messages)
        api.messages['10'].append(message(1250))
        api.fail_channel = '20'
        with self.assertRaises(RuntimeError):
            sync(self.root, api)
        self.assertEqual((self.root / STATE).read_bytes(), before)
        self.assertFalse((self.root / 'sincronizacion_rol.lock').exists())
        manifest = next((self.root / 'fuentes/rol_incremental').glob('*/manifest.json'))
        self.assertFalse(read(manifest)['completo'])

    def test_attachment_failure_then_retry_and_cache_without_redownloading(self):
        self.initialize()
        before = (self.root / STATE).read_bytes()
        api = FakeDiscord(self.messages)
        new = message(1250)
        new['attachments'] = [dict(id='99', filename='voz.ogg', size=len(api.payload),
                                   url='https://cdn.discordapp.com/attachments/99/voz.ogg?ex=old')]
        api.messages['10'].append(new)
        api.fail_media = True
        with self.assertRaises(RuntimeError):
            sync(self.root, api)
        self.assertEqual((self.root / STATE).read_bytes(), before)
        api.fail_media = False
        state = sync(self.root, api)
        payload_path = self.root / state['adjuntos']['99']['archivo']
        self.assertEqual(payload_path.read_bytes(), api.payload)
        repeated = FakeDiscord(api.messages)
        repeated.messages['10'][-1]['attachments'][0]['url'] += '-renewed'
        state = sync(self.root, repeated)
        self.assertFalse(repeated.media_calls)
        self.assertFalse(read(self.root / state['historial'][-1]['archivo'])['cambios'])
        payload_path.write_bytes(b'altered')
        checkpoint = (self.root / STATE).read_bytes()
        with self.assertRaises(ValueError):
            sync(self.root, repeated)
        self.assertEqual((self.root / STATE).read_bytes(), checkpoint)

    def test_wrong_bot_does_not_access_server_or_advance(self):
        self.initialize()
        before = (self.root / STATE).read_bytes()
        api = FakeDiscord(self.messages)
        api.application = 'another-bot'
        with self.assertRaises(ValueError):
            sync(self.root, api)
        self.assertEqual(api.calls, ['/oauth2/applications/@me'])
        self.assertEqual((self.root / STATE).read_bytes(), before)

    def test_mismatched_attachment_is_preserved_without_advancing(self):
        self.initialize()
        api = FakeDiscord(self.messages)
        new = message(1250)
        new['attachments'] = [dict(id='99', filename='image.png', size=len(api.payload) + 1,
                                   url='https://cdn.discordapp.com/attachments/99/image.png')]
        api.messages['10'].append(new)
        before = (self.root / STATE).read_bytes()
        with self.assertRaises(ValueError):
            sync(self.root, api)
        self.assertEqual((self.root / STATE).read_bytes(), before)
        pending = read(next((self.root / 'fuentes/rol_incremental').glob('*/adjuntos_pendientes.json')))
        self.assertEqual(verified(self.root, pending), api.payload)

    def test_archived_threads_are_paginated_and_assigned_to_their_campaign(self):
        self.initialize()
        api = FakeDiscord(self.messages)
        original_get = api.get
        recent = metadata('30', X)
        recent['thread_metadata']['archive_timestamp'] = '2026-10-19T00:00:00+00:00'
        older = metadata('40', X)
        older['thread_metadata']['archive_timestamp'] = '2026-10-18T00:00:00+00:00'
        for thread in (recent, older):
            thread['thread_metadata']['archived'] = True
            api.messages[thread['id']] = [message(int(thread['id']) * 100, thread['id'])]
        def get(path):
            if path.startswith(f'/channels/{X}/threads/archived/public'):
                api.calls.append(path)
                return json.dumps(dict(threads=[older if '&before=' in path else recent],
                                       has_more='&before=' not in path)).encode()
            return original_get(path)
        api.get = get
        state = sync(self.root, api)
        self.assertEqual(state['hilos']['30']['campana'], 'xoltacan')
        self.assertEqual(state['hilos']['40']['campana'], 'xoltacan')
        self.assertEqual(state['hilos']['20']['campana'], 'kuroto')
        self.assertTrue(any('&before=' in path for path in api.calls if '/threads/archived/' in path))

    def test_archived_pagination_rejects_a_repeated_cursor(self):
        thread = metadata('30', X)
        class RepeatingAPI:
            def get(self, path):
                return dict(threads=[thread], has_more=True)
        with self.assertRaises(ValueError):
            archived(RepeatingAPI(), X)

    def test_thread_cannot_switch_campaign(self):
        self.initialize()
        api = FakeDiscord(self.messages)
        api.threads[0]['parent_id'] = K
        before = (self.root / STATE).read_bytes()
        with self.assertRaises(ValueError):
            sync(self.root, api)
        self.assertEqual((self.root / STATE).read_bytes(), before)

    def test_concurrent_run_cannot_replace_checkpoint(self):
        self.initialize()
        (self.root / 'sincronizacion_rol.lock').write_text('123')
        with self.assertRaises(FileExistsError):
            sync(self.root, FakeDiscord(self.messages))

    def test_missing_message_content_intent_does_not_consult_server(self):
        self.initialize()
        api = FakeDiscord(self.messages)
        api.flags = 0
        before = (self.root / STATE).read_bytes()
        with self.assertRaises(ValueError):
            sync(self.root, api)
        self.assertEqual(api.calls, ['/oauth2/applications/@me'])
        self.assertEqual((self.root / STATE).read_bytes(), before)

    def test_signed_forwarded_urls_do_not_create_false_edits(self):
        old = message(1)
        old['message_snapshots'] = [dict(message=dict(content='Foto', attachments=[dict(
            id='9', url='https://cdn.discordapp.com/attachments/9/a.png?ex=old')]))]
        new = deepcopy(old)
        new['message_snapshots'][0]['message']['attachments'][0]['url'] += '-renewed'
        self.assertEqual(editorial_value(old), editorial_value(new))
        new['message_snapshots'][0]['message']['content'] = 'Otra foto'
        self.assertNotEqual(editorial_value(old), editorial_value(new))


if __name__ == '__main__':
    unittest.main()
