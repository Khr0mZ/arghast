"""Conserva procedencia y reparte la transcripción; no marca el capítulo revisado."""
import hashlib
import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import read_json, sha, parse_vtt, normalize

FOLDER = ROOT / 'campanas/xoltacan/revision/borradores/45'
INFO = ROOT / 'campanas/xoltacan/fuentes/45 - 30qLJWABsPE.info.json'


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    newline = '\r\n' if path.exists() and b'\r\n' in path.read_bytes() else '\n'
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').replace('\n', newline).encode('utf-8'))


def main():
    report = ROOT / '.pruebas/capitulo45'
    report.mkdir(parents=True, exist_ok=True)
    baseline = report / 'baseline.json'
    if not baseline.exists():
        html = (ROOT / 'arghast.html').read_text(encoding='utf-8')
        world = json.loads(re.search(r'<script id="xoltacan-data" type="application/json">(.*?)</script>', html, re.S)[1])
        kuroto = json.dumps(world['campaigns']['kuroto'], ensure_ascii=False, sort_keys=True).encode('utf-8')
        role = world['writtenRole']
        original_scenes = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted((ROOT / 'campanas/xoltacan/conocimiento/rol_escrito/escenas').glob('*.json'))}
        save(baseline, dict(kuroto_sha256=hashlib.sha256(kuroto).hexdigest(), originales=read_json(ROOT / 'campanas/xoltacan/derivados/originales_sha256.json'),
            rol_escrito=dict(estadisticas=role['stats'], escenas=len(role['scenes']), originales=original_scenes)))
    spec = importlib.util.spec_from_file_location('descargador', ROOT / 'scripts/subtitulos.py')
    downloader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(downloader)
    for vtt in sorted(INFO.parent.glob('45 - 30qLJWABsPE.*.vtt')):
        if not vtt.with_suffix('.txt').exists():
            vtt.with_suffix('.txt').write_text(downloader.texto_desde_vtt(vtt), encoding='utf-8')
    metadata = read_json(INFO)
    assert metadata['id'] == '30qLJWABsPE' and metadata['channel_id'] == 'UCWJ11LdxIuDJpbknXpSPgeg'
    item = dict(capitulo=45, id=metadata['id'], titulo='El escondite de los Profundos', url=metadata['webpage_url'])
    path = ROOT / 'campanas/xoltacan/catalogo.json'
    catalog = read_json(path)
    episodes = catalog['episodios']
    previous = [e for e in episodes if e['capitulo'] == 45 or e['id'] == item['id']]
    assert not previous or previous == [item]
    if not previous:
        save(path, dict(catalog, episodios=episodes + [item]))
    path = ROOT / 'campanas/xoltacan/config/emisiones.json'
    dates = read_json(path)
    dates['capitulos']['45'] = dict(video_id=item['id'], twitch=dict(
        estado='documentada', fecha='2026-07-16', fuentes=['1527375684333338644'], criterio='campana_numero_y_titulo',
        nota='La tarjeta conservada identifica campaña, capítulo y título; el aviso no fija el comienzo exacto de la partida.',
        variantes=None, fechas_candidatas=['2026-07-16']), youtube=dict(
        estado='publicacion_documentada', fecha='2026-11-03', fecha_aviso=None, fuentes=[],
        origen_fecha='metadatos_youtube', archivo_metadatos=INFO.relative_to(ROOT).as_posix(), sha256_metadatos=sha(INFO),
        publicacion_reportada_utc=datetime.fromtimestamp(metadata['timestamp'], timezone.utc).isoformat()))
    save(path, dates)
    path = ROOT / 'campanas/xoltacan/config/duraciones_rol.json'
    durations = read_json(path)
    durations['fuentes']['xoltacan45'] = dict(archivo=INFO.relative_to(ROOT).as_posix(), sha256=sha(INFO))
    durations['campanas']['xoltacan']['45'] = dict(video_id=item['id'], segundos=metadata['duration'], fuente='xoltacan45')
    save(path, durations)
    source = INFO.parent / '45 - 30qLJWABsPE.es-orig.vtt'
    segments = parse_vtt(source)
    aliases = read_json(ROOT / 'campanas/xoltacan/config/nombres.json')['alias_confirmados']
    for segment in segments:
        segment['texto_normalizado'] = normalize(segment['texto_original'], aliases)
    split = dict(capitulo=45, fuente=source.relative_to(ROOT).as_posix(), sha256=sha(source), total_segmentos=len(segments), bloques=[])
    for index in range(3):
        rows = segments[len(segments)*index//3:len(segments)*(index+1)//3]
        save(FOLDER / f'bloque_{index+1}_segmentos.json', rows)
        (FOLDER / f'bloque_{index+1}.md').write_text('\n\n'.join(f'[{r["inicio"]}–{r["fin"]}] {r["texto_normalizado"]}' for r in rows) + '\n', encoding='utf-8')
        split['bloques'].append(dict(bloque=index+1, inicio=rows[0]['inicio'], fin=rows[-1]['fin'], segmentos=len(rows),
            palabras=sum(len(r['texto_normalizado'].split()) for r in rows), primer_segmento=rows[0]['id'], ultimo_segmento=rows[-1]['id']))
    save(FOLDER / 'reparto.json', split)
    originals = {p.relative_to(ROOT).as_posix(): dict(sha256=sha(p), bytes=p.stat().st_size) for p in sorted(INFO.parent.glob('45 - 30qLJWABsPE.*'))}
    save(ROOT / 'campanas/xoltacan/revision/fuente_xoltacan_45.json', dict(
        **{k:metadata[k] for k in ('id','title','duration','upload_date','channel','channel_id','webpage_url')},
        capitulo=45, recuperado_el='2026-11-03', herramienta='yt-dlp', version='2026.08.19',
        lectura='Pendiente de integrar las tres lecturas completas; descargar fuentes no equivale a revisión editorial.',
        txt='Representaciones legibles generadas desde los VTT con el descargador del proyecto; los VTT son la fuente principal.',
        originales=originals, reparto='borradores/45/reparto.json'))
    print(json.dumps(split, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
