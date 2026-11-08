"""Ubicaciones comunes de las campañas; la raíz contiene solo recursos compartidos."""
from dataclasses import dataclass
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class CampaignPaths:
    id: str

    @property
    def raiz(self):
        return ROOT / 'campanas' / self.id

    @property
    def catalogo(self):
        return self.raiz / 'catalogo.json'

    @property
    def config(self):
        return self.raiz / 'config'

    @property
    def fuentes(self):
        return self.raiz / 'fuentes'

    @property
    def revision(self):
        return self.raiz / 'revision'

    @property
    def conocimiento(self):
        return self.raiz / 'conocimiento'

    @property
    def derivados(self):
        return self.raiz / 'derivados'

    @property
    def web(self):
        return self.raiz / 'web'

    @property
    def publico(self):
        return self.raiz / 'publico'


CAMPAIGNS = {name: CampaignPaths(name) for name in ('xoltacan', 'kuroto')}
XOLTACAN = CAMPAIGNS['xoltacan']
KUROTO = CAMPAIGNS['kuroto']


def episodios(campaign='xoltacan'):
    return json.loads(CAMPAIGNS[campaign].catalogo.read_text(encoding='utf-8'))['episodios']
