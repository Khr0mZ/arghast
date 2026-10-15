"""Separación de campañas e integridad de fuentes pendientes."""
import json
import tempfile
import unittest
from pathlib import Path
from campanas import build_kuroto, build_world, validate_story, mission_text
from construir_interfaz import build_data


class CampaignTests(unittest.TestCase):
    def test_structured_mission_keeps_authored_result_and_citations(self):
        text = mission_text({'titulo': 'Rescatar al joyero', 'estado': 'parcial',
                             'descripcion': 'Sale de la cueva, pero necesita atención.', 'referencias': ['57-011']})
        self.assertIn('Sale de la cueva, pero necesita atención.', text)
        self.assertIn('parcial', text)
        self.assertIn('57-011', text)
        self.assertEqual(mission_text('Entrega pendiente.'), 'Entrega pendiente.')

    def test_story_cannot_use_a_later_revelation_before_its_review(self):
        story = {'revisado_hasta': 1, 'etapas': [
            {'titulo': 'Un acuerdo', 'texto': 'El señor paga a los cazadores.', 'referencias': ['02-025']}]}
        with self.assertRaisesRegex(ValueError, 'posterior a su revisión'):
            validate_story(story, {'02-025': {'capitulo': 2}}, 'La casa')

    def test_chapter_story_cannot_borrow_evidence_from_another_session(self):
        story = {'revisado_hasta': 2, 'etapas': [
            {'titulo': 'El pago', 'texto': 'La venta queda pagada.', 'referencias': ['01-007']}]}
        with self.assertRaisesRegex(ValueError, 'otra sesión'):
            validate_story(story, {'01-007': {'capitulo': 1}}, 'Capítulo 2', chapter=2)

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


if __name__ == '__main__':
    unittest.main()
