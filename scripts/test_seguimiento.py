"""Cobertura y protección de la revisión incremental de preguntas."""
import json
import tempfile
import unittest
from pathlib import Path
from seguimiento import build_tracking


class FollowupTests(unittest.TestCase):
    def setUp(self):
        self.chapters = [
            {'capitulo':1,'preguntas':['¿Se recupera el objeto?'],
             'afirmaciones':[{'id':'01-001'}]},
            {'capitulo':2,'preguntas':[], 'afirmaciones':[{'id':'02-001'}]}]
        self.review = {'revisado_hasta':2,'preguntas':[
            {'id':'P01-001','capitulo':1,'indice':1,'pregunta':'¿Se recupera el objeto?',
             'estado':'resuelta','respuesta':'Se recupera en la siguiente expedición.',
             'referencias':['02-001'],'pendiente':'','revisado_hasta':2}]}
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'review.json'

    def build(self):
        self.path.write_text(json.dumps(self.review), encoding='utf-8')
        return build_tracking(self.chapters, [self.path])

    def test_new_episode_flags_prior_reviews_and_new_questions(self):
        self.chapters.append({'capitulo':3,'preguntas':['¿Qué pasa después?'],'afirmaciones':[]})
        result = self.build()
        self.assertTrue(result['preguntas'][0]['requiere_actualizacion'])
        self.assertEqual(result['preguntas'][1]['estado'], 'sin_revisar')
        self.assertEqual(result['estados'], {'resuelta':1,'sin_revisar':1})

    def test_edited_question_invalidates_its_old_review(self):
        self.chapters[0]['preguntas'][0] = '¿Se destruye el objeto?'
        with self.assertRaisesRegex(ValueError, 'pregunta cambió'):
            self.build()

    def test_closure_needs_valid_later_evidence(self):
        for refs in ([], ['01-001'], ['02-999']):
            with self.subTest(refs=refs):
                self.review['preguntas'][0]['referencias'] = refs
                with self.assertRaises(ValueError):
                    self.build()

    def test_partial_answer_must_preserve_unknown_part(self):
        self.review['preguntas'][0]['estado'] = 'parcial'
        with self.assertRaisesRegex(ValueError, 'pendiente'):
            self.build()
        self.review['preguntas'][0]['pendiente'] = 'No se sabe quién lo robó.'
        self.assertEqual(self.build()['estados'], {'parcial':1})

    def test_real_campaign_has_individual_complete_coverage(self):
        result = build_tracking()
        self.assertEqual(len(result['preguntas']), 228)
        self.assertEqual(result['estados'].get('sin_revisar',0), 0)
        self.assertEqual(result['por_actualizar'], 0)
        self.assertEqual(len({q['id'] for q in result['preguntas']}), 228)


if __name__ == '__main__':
    unittest.main()
