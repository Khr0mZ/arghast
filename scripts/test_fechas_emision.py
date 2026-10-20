"""Regresiones de procedencia: emisión original, publicación y aviso son distintos."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from fechas_emision import ROOT, SOURCES, CAMPAIGNS, ESTIMATES, PROGRAMMING, load_dates, read, validate_estimate, load_programming


class EmissionDatesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = read(ROOT / 'xoltacan_subtitulos/episodios.json') + read(ROOT / 'config/episodios_nuevos.json')
        cls.document = read(CAMPAIGNS['xoltacan'])
        cls.dates = load_dates('xoltacan', cls.catalog)

    def mutated(self, change, campaign='xoltacan'):
        document = copy.deepcopy(self.document if campaign == 'xoltacan' else read(CAMPAIGNS[campaign]))
        catalog = self.catalog if campaign == 'xoltacan' else read(ROOT / 'campanas/kuroto/catalogo.json')['episodios']
        change(document)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'emisiones.json'
            path.write_text(json.dumps(document), encoding='utf-8')
            return load_dates(campaign, catalog, path=path, source_path=SOURCES)

    def test_chapter_41_twitch_is_july_not_youtube_october(self):
        chapter = self.dates[41]
        self.assertEqual(chapter['twitch']['fecha'], '2026-07-03')
        self.assertEqual(chapter['youtube']['fecha'], '2026-10-20')
        self.assertEqual(chapter['twitch']['fuentes'], ['1522672340213694706'])

    def test_late_youtube_notice_does_not_replace_publication(self):
        chapter = self.dates[1]
        self.assertEqual(chapter['youtube']['fecha'], '2026-04-07')
        self.assertEqual(chapter['youtube']['fecha_aviso'], '2026-04-09')

    def test_adoption_preserves_repeated_announcements(self):
        self.assertEqual(self.dates[21]['twitch']['fecha'], '2026-04-01')
        self.assertEqual(self.dates[21]['twitch']['fechas_candidatas'], ['2026-04-01', '2026-04-02'])
        self.assertEqual(self.dates[22]['twitch']['fecha'], '2026-04-02')
        self.assertEqual(self.dates[40]['twitch']['fecha'], '2026-07-02')

    def test_no_publication_inferred_from_notice_without_video_timestamp(self):
        self.assertEqual(self.dates[39]['youtube']['estado'], 'solo_aviso')
        self.assertIsNone(self.dates[39]['youtube']['fecha'])
        with self.assertRaisesRegex(ValueError, 'aviso no acredita'):
            self.mutated(lambda d: d['capitulos']['39']['youtube'].update(fecha='2026-10-13'))

    def test_youtube_source_cannot_date_a_twitch_broadcast(self):
        with self.assertRaisesRegex(ValueError, 'otra campaña o plataforma'):
            self.mutated(lambda d: d['capitulos']['41']['twitch'].update(fuentes=['1562037763434610738']))

    def test_other_youtube_video_cannot_date_chapter(self):
        with self.assertRaisesRegex(ValueError, 'otro vídeo'):
            self.mutated(lambda d: d['capitulos']['41']['youtube'].update(fuentes=['1561312850138505226']))

    def test_distinct_twitch_dates_cannot_be_promoted_to_one_date(self):
        with self.assertRaisesRegex(ValueError, 'fecha única'):
            self.mutated(lambda d: d['capitulos']['21']['twitch'].update(estado='documentada', fecha='2026-04-01'))

    def test_twitch_source_from_another_chapter_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Número del directo'):
            self.mutated(lambda d: d['capitulos']['41']['twitch'].update(fuentes=self.dates[1]['twitch']['fuentes']))

    def test_campaigns_and_unavailable_chapters_stay_separate(self):
        catalog = read(ROOT / 'campanas/kuroto/catalogo.json')['episodios']
        ku = load_dates('kuroto', catalog)
        self.assertNotIn(92, ku)
        self.assertEqual(ku[131]['twitch']['fecha'], '2025-06-24')
        self.assertEqual(ku[143]['twitch']['fecha'], '2025-08-07')
        self.assertEqual(len(ku[143]['twitch']['fuentes']), 2)
        self.assertEqual(ku[46]['twitch']['fecha'], '2024-09-11')
        self.assertEqual(ku[47]['twitch']['fecha'], '2024-09-17')
        for number, day in ((49, '2024-09-24'), (56, '2024-10-10'), (134, '2025-07-02')):
            self.assertEqual(ku[number]['twitch']['fecha'], day)
            self.assertEqual(ku[number]['twitch']['estado'], 'asumida')
            self.assertEqual(ku[number]['twitch']['estimacion']['fecha_probable'], day)
        self.assertIn('Diceland', ku[72]['twitch']['nota'])

    def test_accepted_probable_days_preserve_their_estimation_provenance(self):
        for number in (21, 22, 38, 40):
            twitch = self.dates[number]['twitch']
            self.assertEqual(twitch['estado'], 'asumida')
            self.assertEqual(twitch['fecha'], twitch['estimacion']['fecha_probable'])
            self.assertTrue(twitch['asuncion']['autorizada_por_usuario'])
            self.assertIn('estimacion', twitch)
            self.assertFalse(twitch['estimacion']['sirve_como_corte_exacto'])
        self.assertEqual(self.dates[21]['twitch']['estimacion']['fecha_probable'], '2026-04-01')
        self.assertEqual(self.dates[38]['twitch']['estimacion']['fecha_probable'], '2026-06-15')
        self.assertEqual(self.dates[40]['twitch']['estimacion']['fecha_probable'], '2026-07-02')

    def test_accepting_a_day_does_not_accept_the_scheduled_start_time(self):
        for number, day in ((38, '2026-06-15'), (40, '2026-07-02')):
            twitch = self.dates[number]['twitch']
            self.assertEqual(twitch['fecha'], day)
            self.assertNotIn('hora', twitch)
            self.assertEqual(twitch['programacion'][0]['fecha'], day)
            self.assertEqual(twitch['programacion'][0]['hora'], '20:00')
        self.assertEqual(self.dates[41]['twitch']['fecha'], '2026-07-03')

    def test_assumed_day_requires_explicit_acceptance(self):
        with self.assertRaisesRegex(ValueError, 'aceptación explícita'):
            self.mutated(lambda d: d['capitulos']['38']['twitch']['asuncion'].update(autorizada_por_usuario=False))

    def test_adoption_cannot_choose_a_different_day(self):
        with self.assertRaisesRegex(ValueError, 'día probable elegido'):
            self.mutated(lambda d: d['capitulos']['38']['twitch'].update(fecha='2026-06-16'))

    def test_rescheduled_session_preserves_both_plans_and_actual_notice(self):
        catalog = read(ROOT / 'campanas/kuroto/catalogo.json')['episodios']
        ku = load_dates('kuroto', catalog)
        self.assertEqual([p['fecha'] for p in ku[12]['twitch']['programacion']], ['2024-05-02', '2024-05-07'])
        self.assertEqual(ku[12]['twitch']['fecha'], '2024-05-07')
        self.assertEqual(ku[42]['twitch']['programacion'][0]['fecha'], '2024-09-02')
        self.assertEqual(ku[42]['twitch']['estimacion']['fecha_probable'], '2024-09-03')
        self.assertIn('Discrepancia', ku[55]['twitch']['advertencia_programacion'])
        self.assertEqual(ku[55]['twitch']['fecha'], '2024-10-09')
        self.assertEqual(ku[55]['twitch']['asuncion']['fecha_anterior'], '2024-10-10')
        self.assertEqual(ku[55]['twitch']['fuentes'], ['1294002567352811644'])
        self.assertEqual(ku[56]['twitch']['fecha'], '2024-10-10')

    def test_correction_preserves_the_actual_date_of_its_original_notice(self):
        with self.assertRaisesRegex(ValueError, 'Corrección sin correspondencia'):
            self.mutated(lambda d: d['capitulos']['55']['twitch']['asuncion'].update(fecha_anterior='2024-10-09'), campaign='kuroto')

    def test_contradictory_other_campaign_notice_cannot_be_used_as_direct_proof(self):
        with self.assertRaisesRegex(ValueError, 'otra campaña o plataforma'):
            self.mutated(lambda d: d['capitulos']['49']['twitch'].update(fuentes=['1288206046950588457']), campaign='kuroto')
        evidence = read(SOURCES)['anuncios']
        self.assertEqual(evidence['1288206046950588457']['campana'], 'zaland')
        self.assertEqual(evidence['1390030497551487016']['campana'], 'campana_iii')

    def test_calendar_reference_cannot_cross_campaigns(self):
        document = copy.deepcopy(read(PROGRAMMING))
        ref = self.dates[38]['twitch']['estimacion']['fuentes_programacion'][0]
        document['fuentes'][ref]['sesiones'][0]['campana'] = 'kuroto'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'programacion.json'
            path.write_text(json.dumps(document), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'otra campaña o capítulo'):
                load_dates('xoltacan', self.catalog, programming_path=path)

    def test_all_pending_cases_have_reviewed_calendar_evidence(self):
        programming = load_programming()
        for campaign, entries in read(ESTIMATES)['campanas'].items():
            for number, estimate in entries.items():
                self.assertTrue(estimate['fuentes_programacion'])
                for ref in estimate['fuentes_programacion']:
                    self.assertTrue(any(r['campana'] == campaign and r['capitulo'] == int(number) for r in programming['fuentes'][ref]['sesiones']))

    def test_estimated_day_cannot_escape_the_interval(self):
        estimate = copy.deepcopy(read(ESTIMATES)['campanas']['xoltacan']['40'])
        estimate['fecha_probable'] = '2026-07-10'
        with self.assertRaisesRegex(ValueError, 'fuera del intervalo'):
            validate_estimate(estimate, 'xoltacan', read(SOURCES)['anuncios'])

    def test_estimation_cannot_use_other_campaign_or_a_youtube_notice(self):
        estimate = copy.deepcopy(read(ESTIMATES)['campanas']['xoltacan']['40'])
        estimate['fuentes'] = self.dates[41]['youtube']['fuentes']
        with self.assertRaisesRegex(ValueError, 'otra campaña o plataforma'):
            validate_estimate(estimate, 'xoltacan', read(SOURCES)['anuncios'])

    def test_estimated_day_is_not_an_exact_boundary_for_roleplay(self):
        estimate = copy.deepcopy(read(ESTIMATES)['campanas']['xoltacan']['21'])
        estimate['sirve_como_corte_exacto'] = True
        with self.assertRaisesRegex(ValueError, 'corte exacto'):
            validate_estimate(estimate, 'xoltacan', read(SOURCES)['anuncios'])


if __name__ == '__main__':
    unittest.main()
