"""Comprueba cortes temporales, integridad y separación de las escenas de rol."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from rol_escrito import (digest, instant, load_video_durations, load_written_role, madrid_instants, message_frame,
                        scene_interval, session_anchors, temporal_groups, validate_scene)


def anchor(number=1, end='2026-01-28T22:00:00+00:00', catalog=True):
    return dict(capitulo=number, fecha=end[:10], estado='documentada', catalogado=catalog,
        fuente='https://discord.com/channels/1/2/3', inicio_referencia_utc='2026-01-28T19:00:00+00:00',
        fin_estimado_utc=end, corte_ordenacion_utc=end, duracion_video_segundos=10800,
        tipo_referencia='tarjeta_twitch')


def source(mid='123', at='2026-01-28T19:30:00+00:00', text='Ione: **Abre la puerta.** *¿Quién vendrá?* Hola. <script>bad()</script>'):
    return dict(id=mid, fecha_utc=at, fecha_local=at[:10], editado_utc=None, texto=text,
        texto_sha256=hashlib.sha256(text.encode()).hexdigest(), mensaje_sha256='a' * 64,
        tipo_discord=0, referencia=None, url_discord='https://discord.com/channels/1/2/' + mid,
        adjuntos=[])


def scene():
    return dict(id='x-123', campana='xoltacan', titulo='La visita', resumen='Ione recibe una visita.',
        relato='Ione abre la puerta y saluda sin reconocer todavía a la persona que llega.',
        participantes=['Ione'], revisada=True, estado='abierta', fuentes=[source()],
        evidencias=[dict(mensaje_id='123', afirmacion='Ione abre la puerta.', tipo='accion')],
        inicio_utc='2026-01-28T19:30:00+00:00', fin_utc='2026-01-28T19:30:00+00:00', fecha_local='2026-01-28')


class RoleChronologyTests(unittest.TestCase):
    def test_late_start_and_after_estimated_end(self):
        anchors = [anchor(), anchor(2, '2026-02-01T22:00:00+00:00')]
        self.assertEqual(message_frame(source(at='2026-01-28T19:30:00+00:00'), anchors), 0)
        self.assertEqual(message_frame(source(at='2026-01-28T22:00:01+00:00'), anchors), 1)
        self.assertEqual(scene_interval(1, anchors)['anterior'], 1)
        self.assertEqual(scene_interval(1, anchors)['siguiente'], 2)

    def test_end_after_midnight_keeps_early_message_before_session(self):
        anchors = [anchor(end='2026-01-29T00:30:00+00:00')]
        self.assertEqual(message_frame(source(at='2026-01-29T00:10:00+00:00'), anchors), 0)
        self.assertEqual(message_frame(source(at='2026-01-29T00:31:00+00:00'), anchors), 1)

    def test_late_closing_marker_does_not_move_conversation(self):
        sources = [source(), source('124', '2026-01-29T00:30:00+00:00', '🔴 **Fin de la escena** 🔴')]
        self.assertEqual(temporal_groups(sources, [anchor()]), [{'frame': 0, 'fuentes_ids': ['123', '124']}])
        sources[-1]['texto'] = 'Nox: Ha llegado alguien. Fin de la escena.'
        self.assertEqual(len(temporal_groups(sources, [anchor()])), 2)

    def test_missing_video_is_not_a_catalog_chapter(self):
        anchors = [anchor(), anchor(2, '2026-02-01T23:59:59+00:00', catalog=False)]
        anchors[-1]['fin_estimado_utc'] = None
        interval = scene_interval(1, anchors)
        self.assertEqual(interval['ambito'], 'despues_del_catalogo')
        self.assertFalse(interval['siguiente_catalogado'])
        self.assertIn('sin hora o duración', interval['nota'])

    def test_opening_context_does_not_relocate_later_conversation(self):
        context = source('120', '2026-01-27T19:00:00+00:00', 'Mapa de la ciudad.')
        context['no_narrativo'] = True
        dialogue = source('124', '2026-01-29T12:00:00+00:00')
        self.assertEqual(temporal_groups([context, dialogue], [anchor()]),
                         [{'frame': 1, 'fuentes_ids': ['120', '124']}])

    def test_assumed_date_remains_visible_in_placement(self):
        anchors = [anchor()]
        anchors[0]['estado'] = 'asumida'
        interval = scene_interval(0, anchors)
        self.assertEqual(interval['confianza'], 'fecha_de_sesion_asumida')
        self.assertIn('fecha de sesión asumida', interval['nota'])

    def test_madrid_winter_and_summer_hours(self):
        times = madrid_instants(['2026-01-28T20:30:00', '2026-07-02T20:30:00'])
        self.assertEqual(times['2026-01-28T20:30:00'], instant('2026-01-28T19:30:00Z'))
        self.assertEqual(times['2026-07-02T20:30:00'], instant('2026-07-02T18:30:00Z'))

    def test_start_reference_uses_accepted_day_and_preserves_contrast(self):
        notice = dict(campana='otra', plataforma='twitch', episodio_anunciado=7,
            fecha_tarjeta_local='2026-07-02', timestamp_tarjeta_utc='2026-07-02T18:31:00+00:00',
            aviso_utc='2026-07-02T18:32:00+00:00', url_discord='https://discord.com/channels/1/2/3')
        dates = {40: dict(twitch=dict(fecha='2026-07-02', estado='asumida', fuentes=[],
            estimacion=dict(fuentes=[], fuentes_contraste=['3']), programacion=[]))}
        result = session_anchors('xoltacan', [dict(capitulo=40, duracion='02:00:00')], dates, {'3': notice})
        self.assertEqual(result[0]['tipo_referencia'], 'aviso_de_contraste')
        self.assertEqual(result[0]['fin_estimado_utc'], '2026-07-02T20:31:00+00:00')
        self.assertEqual(result[0]['estado'], 'asumida')


class RoleIntegrityTests(unittest.TestCase):
    def test_duration_is_checked_against_original_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'config').mkdir()
            metadata = root / 'metadata.utf16.json'
            metadata.write_bytes(json.dumps({'entries': [{'id': 'video', 'duration': 120}]}).encode('utf-16'))
            document = dict(fuentes={'source': dict(archivo=metadata.name, sha256=digest(metadata))},
                            campanas={'xoltacan': {'1': dict(video_id='video', segundos=120, fuente='source')}})
            (root / 'config/duraciones_rol.json').write_text(json.dumps(document), encoding='utf-8')
            with patch('rol_escrito.ROOT', root):
                self.assertEqual(load_video_durations('xoltacan', [dict(capitulo=1, id='video', duracion='00:01:59')]), {1: 120})
                with self.assertRaisesRegex(ValueError, 'otro vídeo'):
                    load_video_durations('xoltacan', [dict(capitulo=1, id='other')])

    def test_original_text_and_campaign_are_checked(self):
        original = scene()
        validate_scene(original, 'xoltacan')
        changed = copy.deepcopy(original)
        changed['fuentes'][0]['texto'] += ' alterado'
        with self.assertRaisesRegex(ValueError, 'Texto original modificado'):
            validate_scene(changed, 'xoltacan')
        with self.assertRaisesRegex(ValueError, 'campaña'):
            validate_scene(original, 'kuroto')

    def test_no_review_or_foreign_evidence_is_rejected(self):
        original = scene()
        original['revisada'] = False
        with self.assertRaisesRegex(ValueError, 'lectura'):
            validate_scene(original, 'xoltacan')
        original['revisada'] = True
        original['evidencias'][0]['mensaje_id'] = '999'
        with self.assertRaisesRegex(ValueError, 'evidencias'):
            validate_scene(original, 'xoltacan')

    def test_public_index_is_light_and_sources_are_local_and_escaped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / 'corpus'
            folder.mkdir()
            path = folder / 'scene.json'
            path.write_text(json.dumps(scene()), encoding='utf-8')
            manifest = dict(campana='xoltacan', revision_completa=True,
                escenas=[dict(archivo='scene.json', sha256=digest(path))],
                estadisticas=dict(mensajes_en_escenas=1))
            (folder / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
            with patch('rol_escrito.session_anchors', return_value=[anchor()]):
                result = load_written_role('xoltacan', [], folder, root / 'rol_escrito')
            self.assertNotIn('fuentes', result['scenes'][0])
            self.assertEqual(result['scenes'][0]['mensajes'], 1)
            self.assertIn('puerta', result['scenes'][0]['busqueda'])
            file = root / result['scenes'][0]['sourceFile']
            text = file.read_text(encoding='utf-8')
            self.assertIn('xoltacan/x-123', text)
            self.assertNotIn('<script>', text)
            self.assertIn('\\u003cscript>', text)
            path.write_text('{}', encoding='utf-8')
            with patch('rol_escrito.session_anchors', return_value=[anchor()]), self.assertRaisesRegex(ValueError, 'modificada'):
                load_written_role('xoltacan', [], folder, root / 'rol_escrito')


if __name__ == '__main__':
    unittest.main()
