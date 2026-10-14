"""Pruebas de limpieza temporal y localización de evidencia; sin tocar originales."""
import tempfile
import unittest
from pathlib import Path
from construir import normalize, parse_vtt, validate_fact


class TranscriptTests(unittest.TestCase):
    def source(self, text):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name) / 'source.vtt'
        path.write_text(text, encoding='utf-8')
        return path

    def test_blank_display_line_and_rolling_caption(self):
        p = self.source('WEBVTT\n\n00:00:00.160 --> 00:00:01.000\n \nHola\n\n'
                        '00:00:01.000 --> 00:00:02.000\nHola\nmundo<00:00:01.500><c> feliz</c>\n')
        result = parse_vtt(p)
        self.assertEqual(result[0]['inicio'], '00:00:00.160')
        self.assertEqual([s['texto_original'] for s in result], ['Hola', 'mundo feliz'])

    def test_spoken_repetition_with_new_word_timing_survives(self):
        p = self.source('WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nNo\n\n'
                        '00:00:01.000 --> 00:00:02.000\n<00:00:01.200><c>No</c>\n')
        self.assertEqual([s['texto_original'] for s in parse_vtt(p)], ['No', 'No'])

    def test_identical_line_after_gap_survives(self):
        p = self.source('WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nSí\n\n'
                        '00:00:05.000 --> 00:00:06.000\nSí\n')
        self.assertEqual(len(parse_vtt(p)), 2)

    def test_normalization_only_known_whole_names(self):
        original = 'Choltacán y preCholtacán; Ione.'
        self.assertEqual(normalize(original, {'Choltacán': 'Xoltacan'}), 'Xoltacan y preCholtacán; Ione.')
        self.assertEqual(original, 'Choltacán y preCholtacán; Ione.')

    def test_evidence_rejected_outside_interval(self):
        p = self.source('WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nSecreto\n\n'
                        '00:01:00.000 --> 00:01:01.000\nPúblico\n')
        fact = dict(id='prueba', tipo='hecho_confirmado', conocimiento_personaje='desconocido',
                    inicio='00:00:00.000', fin='00:00:02.000', cita='Secreto')
        validate_fact(fact, p)
        fact['inicio'], fact['fin'] = '00:01:00.000', '00:01:02.000'
        with self.assertRaises(ValueError):
            validate_fact(fact, p)

    def test_invalid_vtt_not_accepted(self):
        p = self.source('<html>access denied</html>')
        with self.assertRaises(ValueError):
            parse_vtt(p)


if __name__ == '__main__':
    unittest.main()
