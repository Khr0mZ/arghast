"""Integridad de las historias: cobertura canónica, referencias y revisión."""
import json
import tempfile
import unittest
from pathlib import Path

from historias import load_histories, load_chapter_histories
from construir_interfaz import build_data


class HistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = build_data()

    def document(self, *, name='Persona', reference='01-001', until=39):
        return {'revisado_hasta': until, 'personajes': {name: [
            {'titulo': 'Un comienzo', 'texto': 'Una historia documentada.', 'referencias': [reference]}
        ]}}

    def load(self, *documents):
        with tempfile.TemporaryDirectory() as folder:
            paths = []
            for i, document in enumerate(documents):
                path = Path(folder) / f'{i}.json'
                path.write_text(json.dumps(document), encoding='utf-8')
                paths.append(path)
            return load_histories(['Persona'], {'01-001': {'capitulo': 1}}, paths)

    def test_all_entities_have_cited_histories(self):
        data = self.data
        self.assertTrue(all(entity['history']['etapas'] for entity in data['entities']))
        self.assertEqual({entity['type'] for entity in data['entities']}, {'personaje', 'lugar', 'faccion', 'objeto'})

    def test_chapter_stages_preserve_the_complete_summary_and_session_scope(self):
        data = self.data
        facts = {fact['id']: fact for fact in data['facts']}
        for chapter in data['chapters']:
            with self.subTest(chapter=chapter['capitulo']):
                stages = chapter['history']['etapas']
                self.assertEqual(' '.join(stage['texto'] for stage in stages), chapter['resumen'])
                self.assertTrue(all(facts[key]['capitulo'] == chapter['capitulo']
                                    for stage in stages for key in stage['referencias']))

    def test_chapter_rejects_future_or_external_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'relato.json'
            path.write_text(json.dumps({'capitulos': {'1': [['Comienzo', '', ['02-001']]]}}), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Fuente ajena'):
                load_chapter_histories([{'capitulo': 1, 'resumen': 'Una historia.', 'estado': 'revisado'}],
                                       {'02-001': {'capitulo': 2}}, path)

    def test_chapter_rejects_a_cut_that_no_longer_matches_the_summary(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'relato.json'
            path.write_text(json.dumps({'capitulos': {'1': [
                ['Comienzo', '', ['01-001']], ['Final', 'Texto retirado', ['01-001']]
            ]}}), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Corte editorial ausente'):
                load_chapter_histories([{'capitulo': 1, 'resumen': 'Una historia.', 'estado': 'revisado'}],
                                       {'01-001': {'capitulo': 1}}, path)

    def test_unknown_reference_fails(self):
        with self.assertRaisesRegex(ValueError, 'Referencia inexistente'):
            self.load(self.document(reference='99-999'))

    def test_duplicate_identity_fails(self):
        with self.assertRaisesRegex(ValueError, 'duplicada'):
            self.load(self.document(), self.document())

    def test_noncanonical_name_fails(self):
        with self.assertRaisesRegex(ValueError, 'canónica'):
            self.load(self.document(name='Alias sin revisar'))

    def test_missing_character_fails(self):
        with self.assertRaisesRegex(ValueError, 'Faltan historias'):
            self.load({'revisado_hasta': 39, 'personajes': {}})

    def test_reference_after_review_fails(self):
        document = self.document()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'historia.json'
            path.write_text(json.dumps(document), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'posterior'):
                load_histories(['Persona'], {'01-001': {'capitulo': 40}}, [path])

    def test_uncited_stage_fails(self):
        document = self.document()
        document['personajes']['Persona'][0]['referencias'] = []
        with self.assertRaisesRegex(ValueError, 'sin referencias'):
            self.load(document)


if __name__ == '__main__':
    unittest.main()
