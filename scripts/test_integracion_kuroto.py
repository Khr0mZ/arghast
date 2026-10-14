"""Pruebas de los límites de autoría y la conciliación de entregas paralelas."""
import tempfile
import unittest
from pathlib import Path

from construir import write_json, sha
from campanas import build_kuroto
from integrar_kuroto import assemble


class IntegrationTests(unittest.TestCase):
    def fixture(self, folder):
        episodes = []
        inventory = {}
        for number, text in [(1, 'El clérigo ayuda a sus compañeros.'), (2, 'Su enfermedad continúa después del ritual.')]:
            video = f'video{number}'
            episodes.append({'capitulo': number, 'id': video, 'titulo': f'Sesión {number}',
                             'url': f'https://www.youtube.com/watch?v={video}'})
            source = folder / 'fuentes' / f'{number:03d} - {video}.es-orig.vtt'
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text('WEBVTT\n\n00:00:01.000 --> 00:00:03.000\n'+text+'\n', encoding='utf-8')
            inventory[source.relative_to(folder).as_posix()] = sha(source)
            name = 'Sir' if number == 1 else 'Sirth'
            fact = {'id': f'{number:02d}-001', 'titulo': 'El clérigo', 'tipo': 'hecho_confirmado',
                    'afirmacion': text, 'inicio': '00:00:01.000', 'fin': '00:00:03.000',
                    'cita': text, 'entidades': [name], 'conocimiento_personaje': 'desconocido'}
            history = {'revisado_hasta': number, 'etapas': [{'titulo': f'Una etapa {number}',
                       'texto': text, 'referencias': [fact['id']]}]}
            write_json(folder / 'conocimiento/capitulos' / f'{number:03d}.json',
                       {'capitulo': number, 'estado_revision': 'revisado', 'fuente_sha256': sha(source),
                        'resumen': text, 'historia': history, 'afirmaciones': [fact]})
            entity = {'nombre': name, 'tipo': 'personaje', 'descripcion': 'Clérigo de la compañía.',
                      'etiquetas': [name], 'nota': '', 'referencias': [], 'historia': history}
            if number == 1:
                write_json(folder / 'revision/base_003.json', {'revisados': [1], 'entidades': [entity], 'preguntas': []})
            else:
                write_json(folder / 'revision/lote_002_002.json', {'revisados': [2], 'entidades': [entity], 'preguntas': []})
        write_json(folder / 'catalogo.json', {'episodios': episodes})
        write_json(folder / 'fuentes/originales_sha256.json', inventory)
        write_json(folder / 'revision/identidades_confirmadas.json', {'Sir': 'Sirth'})

    def test_confirmed_alias_preserves_both_authored_stories(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            self.fixture(folder)
            entities, tracking, manifest = assemble(folder)
            self.assertEqual(len(entities), 1)
            self.assertEqual(entities[0]['nombre'], 'Sirth')
            self.assertEqual(len(entities[0]['historia']['etapas']), 2)
            self.assertIn('Sir', entities[0]['etiquetas'])
            self.assertEqual(manifest['capitulos_integrados'], [1, 2])
            self.assertEqual(manifest['revision_continua_hasta'], 2)

    def test_same_alias_cannot_merge_a_person_and_a_place(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            self.fixture(folder)
            from construir import read_json
            path = folder / 'revision/lote_002_002.json'
            lot = read_json(path)
            lot['entidades'][0]['tipo'] = 'lugar'
            write_json(path, lot)
            with self.assertRaisesRegex(ValueError, 'tipos incompatibles'):
                assemble(folder)

    def test_unintegrated_dossier_does_not_leak_into_the_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            self.fixture(folder)
            from construir import read_json
            base = read_json(folder / 'revision/base_003.json')
            entity = base['entidades'][0]
            entity['nombre'] = 'Sirth'
            write_json(folder / 'conocimiento/entidades.json', [entity])
            write_json(folder / 'revision/integracion.json', {'capitulos_integrados': [1]})
            data = build_kuroto(folder)
            self.assertEqual([fact['id'] for fact in data['facts']], ['01-001'])
            self.assertEqual(data['facts'][0]['entidades'], ['Sirth'])
            self.assertEqual(data['chapters'][1]['estado'], 'pendiente')
            self.assertEqual(data['chapters'][1]['registros'], [])


if __name__ == '__main__':
    unittest.main()
