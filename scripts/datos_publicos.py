"""Lectura del manifiesto común y de los datos públicos de cada campaña."""
import json
from pathlib import Path
import re


def script_data(path, campaign):
    text = Path(path).read_text(encoding='utf-8')
    prefix = 'globalThis.arghastCampaigns[' + json.dumps(campaign) + ']='
    value = text.split(prefix, 1)[1].strip().removesuffix(';')
    return json.loads(value)


def load_public_world(root):
    root = Path(root).resolve()
    html = (root / 'arghast.html').read_text(encoding='utf-8')
    data = json.loads(re.search(r'<script id="xoltacan-data" type="application/json">(.*?)</script>', html, re.S)[1])
    if not data.get('campaignFiles'):
        return data
    campaigns = {}
    for campaign, filename in data['campaignFiles'].items():
        path = (root / filename).resolve()
        public = (root / 'campanas' / campaign / 'publico').resolve()
        if not path.is_relative_to(public) or not public.is_relative_to(root):
            raise ValueError('Datos públicos fuera de su campaña.')
        campaigns[campaign] = script_data(path, campaign)
        campaigns[campaign]['resourceBase'] = public.relative_to(root).as_posix() + '/'
    primary = data.get('rootCampaignId', 'xoltacan')
    return {**campaigns[primary], **data, 'campaigns': {name: value for name, value in campaigns.items() if name != primary}}
