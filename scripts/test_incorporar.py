"""El registro usa el catálogo activo y conserva las descargas originales."""
from contextlib import redirect_stderr
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import incorporar


class EpisodeRegistrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.paths = SimpleNamespace(catalogo=root / 'catalogo.json', fuentes=root / 'fuentes')
        self.original = self.paths.fuentes / 'descarga_inicial/episodios.json'
        self.original.parent.mkdir(parents=True)
        self.original.write_bytes(b'[{"id":"descarga-original"}]\r\n')
        self.paths.catalogo.write_text(json.dumps({'campana': 'xoltacan', 'episodios': []}), encoding='utf-8')

    def register(self, video='abcdefghijk'):
        arguments = ['incorporar.py', '--capitulo', '47', '--url', 'https://www.youtube.com/watch?v=' + video, '--titulo', 'Otra aventura']
        with patch.object(incorporar, 'XOLTACAN', self.paths), patch.object(incorporar.sys, 'argv', arguments), \
                patch.object(incorporar.subprocess, 'run', return_value=SimpleNamespace(returncode=0)):
            return incorporar.main()

    def test_registration_writes_the_active_catalog_and_preserves_originals(self):
        self.assertEqual(self.register(), 0)
        catalog = json.loads(self.paths.catalogo.read_text(encoding='utf-8'))
        self.assertEqual(catalog['campana'], 'xoltacan')
        self.assertEqual(catalog['episodios'][0]['capitulo'], 47)
        self.assertEqual(catalog['episodios'][0]['id'], 'abcdefghijk')
        self.assertEqual(self.original.read_bytes(), b'[{"id":"descarga-original"}]\r\n')

    def test_same_episode_is_idempotent(self):
        self.register()
        before = self.paths.catalogo.read_bytes()
        self.register()
        self.assertEqual(self.paths.catalogo.read_bytes(), before)

    def test_conflicting_video_does_not_replace_an_episode(self):
        self.register()
        before = self.paths.catalogo.read_bytes()
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.register('zyxwvutsrqp')
        self.assertEqual(self.paths.catalogo.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
