"""Separación de campañas e integridad de fuentes pendientes."""
import json
import tempfile
import unittest
from pathlib import Path
from campanas import build_kuroto, build_world
from construir_interfaz import build_data


class CampaignTests(unittest.TestCase):
    def fixture(self, folder):
        (folder / 'fuentes').mkdir()
        (folder / 'catalogo.json').write_text(json.dumps({'episodios': [
            {'capitulo': 1, 'id': 'KkZZR81onIw', 'titulo': 'Un título que no prueba una aventura',
             'url': 'https://www.youtube.com/watch?v=KkZZR81onIw'}
        ]}), encoding='utf-8')

    def test_catalog_metadata_does_not_become_canon(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            self.fixture(folder)
            data = build_kuroto(folder)
            self.assertEqual(data['facts'], [])
            self.assertEqual(data['entities'], [])
            self.assertEqual(data['chapters'][0]['resumen'], '')
            self.assertEqual(data['chapters'][0]['estado'], 'pendiente')
            self.assertFalse(data['chapters'][0]['transcripcion_disponible'])

    def test_unregistered_original_is_not_silently_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            self.fixture(folder)
            (folder / 'fuentes/001 - KkZZR81onIw.es.vtt').write_text('WEBVTT\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'registrar el original'):
                build_kuroto(folder)

    def test_changed_original_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            self.fixture(folder)
            name = 'fuentes/001 - KkZZR81onIw.es.vtt'
            (folder / name).write_text('WEBVTT\n', encoding='utf-8')
            (folder / 'fuentes/originales_sha256.json').write_text(json.dumps({name: 'hash distinto'}), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'modificada'):
                build_kuroto(folder)

    def test_world_preserves_the_reviewed_xoltacan_archive(self):
        xoltacan = build_data()
        world = build_world(xoltacan)
        self.assertEqual(world['world'], 'Arghast')
        self.assertEqual(world['chapters'], xoltacan['chapters'])
        self.assertEqual(world['facts'], xoltacan['facts'])
        self.assertEqual(world['entities'], xoltacan['entities'])
        self.assertNotIn('kuroto', xoltacan)
        kuroto = world['campaigns']['kuroto']
        self.assertIsNot(kuroto['chapters'], xoltacan['chapters'])
        self.assertNotEqual(kuroto['chapters'][0]['id'], xoltacan['chapters'][0]['id'])

    def test_kuroto_keeps_the_published_numbers_and_gap(self):
        data = build_kuroto()
        numbers = [chapter['capitulo'] for chapter in data['chapters']]
        self.assertEqual(numbers, sorted(set(numbers)))
        self.assertNotIn(92, numbers)
        self.assertIn(182, numbers)
        self.assertEqual(data['catalog']['capitulos_ausentes'], [92])


if __name__ == '__main__':
    unittest.main()
