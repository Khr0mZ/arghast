"""Comprueba consulta enciclopédica, atribución y búsquedas con acentos."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import consultar


class KnowledgeSearchTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        root = Path(self.folder.name)
        (root / 'capitulos').mkdir()
        rows = []
        for idx, (status, kind, witnesses) in enumerate([
            ('desconocido', 'hecho_confirmado', []),
            ('atestiguado', 'declaracion_personaje', ['Madame Oghma']),
            ('no_atestiguado', 'hecho_confirmado', ['Naór'])
        ], 1):
            rows.append(dict(id=f'01-{idx:03d}', titulo='Naór en Tutucan',
                             afirmacion='Declaración sobre concilio', entidades=['Naór'],
                             inicio=f'00:0{idx}:00', tipo=kind,
                             conocimiento_personaje=status, conocedores=witnesses))
        (root / 'capitulos/01.json').write_text(json.dumps({'afirmaciones': rows}), encoding='utf-8')
        context = patch.object(consultar, 'KB', root)
        context.start()
        self.addCleanup(context.stop)

    def test_encyclopedia_includes_all_knowledge_states(self):
        self.assertEqual(len(consultar.search()), 3)

    def test_heard_statement_not_promoted_to_fact(self):
        results = consultar.search(kind='declaracion_personaje')
        self.assertEqual([f['id'] for f in results], ['01-002'])
        self.assertEqual(len(consultar.search(kind='hecho_confirmado')), 2)

    def test_accents_and_explicit_witness_filter(self):
        self.assertEqual(len(consultar.search('naor declaracion')), 3)
        self.assertEqual([f['id'] for f in consultar.search(character='oghma')], ['01-002'])
        self.assertEqual(consultar.search(chapter=2), [])

    def test_documented_alias_does_not_merge_similar_names(self):
        path = consultar.KB / 'capitulos/01.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        data['afirmaciones'][0]['entidades'] = ['Nox']
        path.write_text(json.dumps(data), encoding='utf-8')
        self.assertEqual([f['id'] for f in consultar.search('Jim Hawkins')], ['01-001'])


if __name__ == '__main__':
    unittest.main()
