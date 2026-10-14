"""Regresiones de identidad, clasificación y conservación de etiquetas fuente."""
import unittest
from catalogo import load_catalog, canonical_labels, key
from construir_interfaz import build_data


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.aliases, cls.groups, cls.excluded = load_catalog()
        cls.data = build_data()
        cls.entities = {e['name']: e for e in cls.data['entities']}
        cls.facts = {f['id']: f for f in cls.data['facts']}

    def test_aliases_have_one_profile_and_unique_appearances(self):
        for name in ('Jack', 'Coyote', 'Winscore', 'Guayacán', 'Maris', 'Leona'):
            entity = self.entities[name]
            self.assertEqual(len(entity['facts']), len(set(entity['facts'])))
            for label in self.groups[name]['etiquetas']:
                self.assertEqual(self.aliases[label], name)
                self.assertTrue(any(label in f['etiquetas_originales']
                                    for f in self.data['facts']))
        self.assertEqual(canonical_labels(['Nox', 'Nox'], self.aliases), ['Nox'])

    def test_distinct_people_and_mounts_remain_distinct(self):
        for left, right in (('Nox', 'Naór'), ('Citlali', 'Coyote'),
                            ('Eldrat', 'Erendriel'), ('Leona', 'Leo'),
                            ('Marina', 'Marina, la sirena')):
            self.assertNotEqual(self.aliases[left], self.aliases[right])
            self.assertIn(left, self.entities)
            self.assertIn(right, self.entities)
        self.assertEqual(len({self.aliases[f'Merlucilla {i}']
                              for i in ('I','II','III','IV','V')}), 5)

    def test_object_names_do_not_create_people(self):
        self.assertEqual(self.entities['Patata']['type'], 'personaje')
        self.assertEqual(self.entities['Patata Hammer']['type'], 'objeto')
        self.assertEqual(self.entities['Diario Terran del nawal']['type'], 'objeto')
        self.assertEqual(self.entities['Marina']['type'], 'faccion')
        for label in self.excluded:
            self.assertNotIn(label, self.entities)

    def test_catalog_names_and_identity_references_are_valid(self):
        names = [key(e['name']) for e in self.data['entities']]
        self.assertEqual(len(names), len(set(names)))
        for entity in self.data['entities']:
            self.assertNotIn('grafía provisional', entity['name'])
            self.assertTrue(entity['description'])
            for fid in entity['references']:
                self.assertIn(fid, self.facts)
        self.assertNotIn('contradicciones', self.data['documents'])

    def test_original_tags_are_retained_and_mapped_without_duplicates(self):
        for fact in self.data['facts']:
            self.assertIn('etiquetas_originales', fact)
            self.assertEqual(fact['entidades'], canonical_labels(
                fact['etiquetas_originales'], self.aliases))


if __name__ == '__main__':
    unittest.main()
