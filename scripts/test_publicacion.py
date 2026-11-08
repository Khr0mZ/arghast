"""El paquete público conserva ambos lectores y excluye los originales."""
from pathlib import Path
import tempfile
import unittest

from preparar_publicacion import prepare


class PublicationTests(unittest.TestCase):
    def test_only_public_readers_are_staged_and_can_be_rebuilt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('arghast', 'xoltacan', 'kuroto'):
                (root / (name + '.html')).write_text(name, encoding='utf-8')
            for campaign in ('xoltacan', 'kuroto'):
                folder = root / 'campanas' / campaign
                (folder / 'publico/transcripciones').mkdir(parents=True)
                (folder / 'publico/rol_escrito/adjuntos').mkdir(parents=True)
                (folder / 'publico/index.html').write_text(campaign, encoding='utf-8')
                (folder / 'publico/datos.js').write_text(campaign, encoding='utf-8')
                (folder / 'publico/transcripciones/001.js').write_text('transcript', encoding='utf-8')
                (folder / 'publico/rol_escrito/adjuntos/1.png').write_bytes(b'image')
                (folder / 'config').mkdir()
                (folder / 'config/privado.json').write_text('{}', encoding='utf-8')
            target = prepare(root=root)
            self.assertEqual((target / 'index.html').read_text(encoding='utf-8'), 'arghast')
            for campaign in ('xoltacan', 'kuroto'):
                folder = target / 'campanas' / campaign
                self.assertEqual((folder / 'publico/index.html').read_text(encoding='utf-8'), campaign)
                self.assertTrue((folder / 'publico/rol_escrito/adjuntos/1.png').is_file())
                self.assertFalse((folder / 'config').exists())
            (target / 'obsolete.txt').write_text('old', encoding='utf-8')
            prepare(root=root)
            self.assertFalse((target / 'obsolete.txt').exists())

    def test_campaign_sources_and_arbitrary_folders_cannot_be_destinations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for target in (root, root / 'campanas/xoltacan/publico', root / 'web', root / '.pruebas', root.parent):
                with self.subTest(target=target), self.assertRaises(ValueError):
                    prepare(target, root=root)
            target = root / '.pruebas/important'
            target.mkdir(parents=True)
            marker = target / 'existing.txt'
            marker.write_text('keep', encoding='utf-8')
            with self.assertRaises(ValueError):
                prepare(target, root=root)
            self.assertEqual(marker.read_text(encoding='utf-8'), 'keep')


if __name__ == '__main__':
    unittest.main()
