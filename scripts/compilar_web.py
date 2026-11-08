"""Compila lectores autónomos por campaña y un visor común sin datos duplicados."""
from copy import deepcopy
import json
from rutas import ROOT, CAMPAIGNS, XOLTACAN
from construir import write
from recursos import inline_assets
from estilos import expand_styles


def compile_world(world):
    template = (ROOT / 'web/plantilla.html').read_text(encoding='utf-8')
    script = (ROOT / 'web/edicion.js').read_text(encoding='utf-8') + '\n' + (ROOT / 'web/app.js').read_text(encoding='utf-8')
    lettering = (XOLTACAN.web / 'assets/rotulos-xoltacan/indice.json').read_text(encoding='utf-8')
    script = script.replace('/* ROTULOS_XOLTACAN */{}', lettering)
    sheets = [ROOT / 'web' / name for name in ('selva.css', 'codice.css', 'arghast.css', 'paletas.css', 'fuentes.css', 'tipografia.css')]
    sheets += [XOLTACAN.web / 'rotulos.css', ROOT / 'web/edicion.css']
    theme = inline_assets('\n'.join(expand_styles(path.read_text(encoding='utf-8')) for path in sheets))
    template = inline_assets(template)
    metadata = world['campaignMetadata']
    loading_css = (ROOT / 'web/carga.css').read_text(encoding='utf-8')
    loading_js = (ROOT / 'web/carga.js').read_text(encoding='utf-8')
    lettering_index = json.loads(lettering)
    loading_letters = {label: lettering_index[label] for label in ('Cargando Xoltacan…', 'Volver a intentar')}
    datasets = {'xoltacan': {key: deepcopy(value) for key, value in world.items() if key not in ('world', 'campaignMetadata', 'campaigns')},
                **{key: deepcopy(value) for key, value in world['campaigns'].items()}}

    def html(payload):
        names = {key: value['name'] for key, value in payload['campaignMetadata'].items()}
        loading_config = json.dumps({'names': names, 'defaultCampaign': payload.get('defaultCampaign'), 'lettering': loading_letters if 'xoltacan' in names else {}}, ensure_ascii=False).replace('<', '\\u003c')
        loading_theme = loading_css + '\n' + '\n'.join((CAMPAIGNS[name].web / 'estilos/carga.css').read_text(encoding='utf-8') for name in names)
        loading = '<style>' + loading_theme + '</style><script>' + loading_js.replace('/* LOADING_CONFIG */{}', loading_config) + '</script>'
        data = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
        return template.replace('<!-- LOADING -->', loading).replace('<!-- THEME -->', '<style>' + theme + '</style>').replace(
            '<!-- DATA -->', '<script id="xoltacan-data" type="application/json">' + data + '</script>').replace(
            '<!-- APP -->', '<script>' + script.replace('</script', '<\\/script') + '</script>')

    files = {}
    for campaign, dataset in datasets.items():
        paths = CAMPAIGNS[campaign]
        dataset['transcriptFiles'] = {}
        for number, rows in dataset['transcripts'].items():
            if not rows:
                continue
            relative = f'transcripciones/{int(number):03d}.js'
            key = json.dumps(f'{campaign}/{number}')
            content = json.dumps(rows, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
            write(paths.publico / relative, f'globalThis.arghastTranscripts ??= Object.create(null);\nglobalThis.arghastTranscripts[{key}] = {content};\n')
            dataset['transcriptFiles'][number] = relative
            dataset['transcripts'][number] = []
        payload = json.dumps(dataset, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
        write(paths.publico / 'datos.js', 'globalThis.arghastCampaigns ??= Object.create(null);\nglobalThis.arghastCampaigns[' + json.dumps(campaign) + ']=' + payload + ';\n')
        standalone = {'world': 'Arghast', 'rootCampaignId': campaign, 'defaultCampaign': campaign,
                      'campaignMetadata': {campaign: metadata[campaign]}, 'campaignFiles': {campaign: 'datos.js'}}
        write(paths.publico / 'index.html', html(standalone))
        files[campaign] = (paths.publico / 'datos.js').relative_to(ROOT).as_posix()
    manifest = {'world': 'Arghast', 'rootCampaignId': 'xoltacan', 'campaignMetadata': metadata, 'campaignFiles': files}
    write(ROOT / 'arghast.html', html(manifest))
    for campaign in CAMPAIGNS:
        redirect = '<!doctype html><html lang="es"><meta charset="utf-8"><title>Arghast</title><body><a href="arghast.html?campana=' + campaign + '">Abrir ' + metadata[campaign]['name'] + '</a><script>const u=new URL("arghast.html",location.href);u.search=location.search;u.searchParams.set("campana",u.searchParams.get("campana")||"' + campaign + '");u.hash=location.hash;location.replace(u.href);</script></body></html>\n'
        write(ROOT / (campaign + '.html'), redirect)
    print('Lectores autónomos, transcripciones y rol generados dentro de cada campaña; visor común actualizado.')
