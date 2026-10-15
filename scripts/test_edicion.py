"""Pruebas HTTP del código compartido, persistencia y conflictos entre jugadores."""
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from copy import deepcopy

from servidor_edicion import ArchiveServer, ROOT


class EditionTest(unittest.TestCase):
    def setUp(self):
        (ROOT / '.pruebas').mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / '.pruebas')
        self.database = Path(self.temp.name) / 'edits.sqlite3'
        self.public = Path(self.temp.name) / 'public'
        self.public.mkdir()
        (self.public / 'arghast.html').write_bytes((ROOT / 'arghast.html').read_bytes())
        # Verificar el servicio de archivos sin depender de derivados locales
        # que se generan después de las pruebas en el flujo de publicación.
        transcript = self.public / 'transcripciones/kuroto/001.js'
        transcript.parent.mkdir(parents=True)
        transcript.write_text('globalThis.arghastTranscripts = {};', encoding='utf-8')
        self.start()

    def start(self):
        self.server = ArchiveServer(('127.0.0.1', 0), self.public, self.database, 'showmethemoney')
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f'http://127.0.0.1:{self.server.server_port}'

    def stop(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()
        self.server.db.close()

    def tearDown(self):
        self.stop()
        self.temp.cleanup()

    def request(self, path, data=None, token='', origin=None):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
        if origin:
            headers['Origin'] = origin
        request = Request(self.url + path, data=json.dumps(data).encode() if data is not None else None, headers=headers)
        try:
            response = urlopen(request)
        except HTTPError as error:
            response = error
        with response:
            return response.status, json.load(response)

    def test_shared_edits(self):
        self.assertEqual(self.request('/api/editor/unlock', {'code': 'incorrecto'})[0], 403)
        status, result = self.request('/api/editor/unlock', {'code': 'showmethemoney'})
        self.assertEqual(status, 200)
        token = result['token']
        campaign, kind, identity, field = next(iter(self.server.fields))
        body = dict(campaign=campaign, kind=kind, identity=identity, field=field,
                    value='Corrección de un jugador', author='Jugador de prueba', reason='Estuve en esa sesión', revision=0)
        self.assertEqual(self.request('/api/editor/save', body)[0], 401)
        self.assertEqual(self.request('/api/editor/save', body, token, 'https://otra.example')[0], 403)
        self.assertEqual(self.request('/api/editor/save', {**body, 'field': 'cita'}, token)[0], 400)
        self.assertEqual(self.request('/api/editor/save', {**body, 'campaign': 'otra'}, token)[0], 400)
        status, result = self.request('/api/editor/save', body, token)
        self.assertEqual(status, 200)
        first = result['edits'][0]
        self.assertEqual(self.request('/api/editor/save', body, token)[0], 409)
        original = self.server.fields[(campaign, kind, identity, field)]
        status, result = self.request('/api/editor/save', {**body, 'value': original, 'revision': first['revision'], 'reason': 'Restaurar original'}, token)
        self.assertEqual(status, 200)
        self.assertEqual(len(result['edits']), 2)
        # Un lector sin código ve las mismas correcciones; reiniciar conserva el historial.
        self.stop()
        self.start()
        status, result = self.request('/api/editor')
        self.assertEqual(status, 200)
        self.assertEqual([e['value'] for e in result['edits']], [body['value'], original])
        self.assertEqual(self.request('/.local/edicion/correcciones.sqlite3')[0], 404)
        self.assertEqual(self.request('/AGENTS.md')[0], 404)
        self.assertEqual(self.request('/transcripciones/../../README.md')[0], 404)

    def test_session_revocation_and_attempt_limit(self):
        _, result = self.request('/api/editor/unlock', {'code': 'showmethemoney'})
        token = result['token']
        self.assertEqual(self.request('/api/editor/lock', {}, token)[0], 200)
        self.assertEqual(self.request('/api/editor/save', {}, token)[0], 401)
        for _ in range(9):
            self.assertEqual(self.request('/api/editor/unlock', {'code': 'incorrecto'})[0], 403)
        self.assertEqual(self.request('/api/editor/unlock', {'code': 'showmethemoney'})[0], 429)

    def test_full_document_editing_and_transcript_protection(self):
        _, result = self.request('/api/editor/unlock', {'code':'showmethemoney'})
        token = result['token']
        _, initial = self.request('/api/editor/document/xoltacan')
        content = deepcopy(initial['content'])
        content['facts'][0]['cita'] = 'Cita corregida por un participante'
        content['facts'][0]['inicio'] = '00:01:01'
        content['chapters'][0]['titulo'] = 'Título corregido'
        content['chapters'][0]['misiones'].append('Misión aportada por un jugador')
        content['chapters'][0]['history']['etapas'].append({'titulo':'Otra etapa','texto':'Relato nuevo','referencias':[]})
        content['entities'][0]['name'] = 'Nombre corregido'
        content['seguimiento']['preguntas'][0]['pregunta'] = 'Pregunta corregida'
        content['entities'].append({'name':'Nueva ficha','facts':[],'aliases':[],'type':'personaje','description':'Historia nueva','history':None})
        body = dict(campaign='xoltacan',content=content,revision=0,author='Jugador',reason='Estuve en la sesión')
        self.assertEqual(self.request('/api/editor/save-document', body)[0],401)
        self.assertEqual(self.request('/api/editor/save-document', {**body,'content':{**content,'transcripts':{}}},token)[0],400)
        invalid = deepcopy(content)
        invalid['entities'][0]['facts'] = ['no-existe']
        self.assertEqual(self.request('/api/editor/save-document',{**body,'content':invalid},token)[0],400)
        self.assertEqual(self.request('/api/editor/save-document',body,token)[0],200)
        self.assertEqual(self.request('/api/editor/save-document',body,token)[0],409)
        _, saved = self.request('/api/editor/document/xoltacan')
        self.assertEqual(saved['content']['facts'][0]['cita'],content['facts'][0]['cita'])
        self.assertEqual(saved['content']['entities'][-1]['name'],'Nueva ficha')
        self.assertNotIn('transcripts',saved['content'])
        self.assertEqual(self.request('/api/editor/document/xoltacan?since='+str(saved['revision']))[1],{'unchanged':True})
        _, prior = self.request('/api/editor/document/xoltacan?revision='+str(saved['revision']))
        self.assertEqual(prior['content'],saved['content'])
        _, kuroto = self.request('/api/editor/document/kuroto')
        self.assertNotEqual(kuroto['content']['chapters'][0]['titulo'],'Título corregido')
        self.assertEqual(self.request('/api/editor/save-document',{**body,'content':initial['content'],'revision':saved['revision']},token)[0],200)
        self.stop()
        self.start()
        _, restored = self.request('/api/editor/document/xoltacan')
        self.assertEqual(restored['content']['facts'][0]['cita'],initial['content']['facts'][0]['cita'])
        self.assertEqual(len(restored['history']),2)
        with urlopen(self.url+'/transcripciones/kuroto/001.js') as response:
            self.assertEqual(response.status,200)
            self.assertIn('javascript',response.headers['Content-Type'])


if __name__ == '__main__':
    (ROOT / '.pruebas').mkdir(exist_ok=True)
    unittest.main()
