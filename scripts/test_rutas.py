"""Contrato de ubicación común y catálogo activo tras separar las campañas."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import rutas


class CampaignPathTests(unittest.TestCase):
    def test_campaigns_have_the_same_categories_in_separate_roots(self):
        categories = ('config', 'fuentes', 'revision', 'conocimiento', 'derivados', 'web', 'publico')
        for name, campaign in rutas.CAMPAIGNS.items():
            self.assertEqual(campaign.raiz, rutas.ROOT / 'campanas' / name)
            self.assertTrue(campaign.catalogo.is_file())
            for category in categories:
                self.assertEqual(getattr(campaign, category), campaign.raiz / category)
                self.assertTrue(getattr(campaign, category).is_dir())
        self.assertNotEqual(rutas.XOLTACAN.conocimiento, rutas.KUROTO.conocimiento)

    def test_episode_loader_reads_the_active_catalog_of_the_selected_campaign(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(rutas, 'ROOT', Path(directory)):
            for name, campaign in rutas.CAMPAIGNS.items():
                campaign.raiz.mkdir(parents=True)
                campaign.catalogo.write_text(json.dumps({'episodios': [{'id': name}]}), encoding='utf-8')
            self.assertEqual(rutas.episodios('xoltacan'), [{'id': 'xoltacan'}])
            self.assertEqual(rutas.episodios('kuroto'), [{'id': 'kuroto'}])


if __name__ == '__main__':
    unittest.main()
