"""Conserva fuentes y distribuye la lectura completa del capítulo 47."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import parse_vtt, normalize, sha, read_json
from datos_publicos import load_public_world
from subtitulos import texto_desde_vtt

FOLDER = Path(__file__).parent
INFO = ROOT / 'campanas/xoltacan/fuentes/47 - yvqhR20m7Zg.info.json'


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    newline = '\r\n' if path.exists() and b'\r\n' in path.read_bytes() else '\n'
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').replace('\n', newline).encode('utf-8'))


def main():
    proof = ROOT / '.local/capitulo47'
    proof.mkdir(parents=True, exist_ok=True)
    if not (proof / 'baseline.json').exists():
        world = load_public_world(ROOT)
        originals = {p.relative_to(ROOT).as_posix(): sha(p) for campaign in ('xoltacan', 'kuroto')
                     for category in ('fuentes', 'conocimiento/rol_escrito')
                     for p in (ROOT / 'campanas' / campaign / category).rglob('*')
                     if p.is_file() and not p.name.startswith('47 - yvqhR20m7Zg.')}
        save(proof / 'baseline.json', dict(originales=originals,
            kuroto_sha256=hashlib.sha256(json.dumps(world['campaigns']['kuroto'], ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
            escenas_antes=world['writtenRole']['scenes'], estadisticas_rol=world['writtenRole']['stats']))
        save(FOLDER / 'seguimiento_antes.json', world['seguimiento']['preguntas'])
    metadata = read_json(INFO)
    assert metadata['id'] == 'yvqhR20m7Zg' and metadata['channel_id'] == 'UCWJ11LdxIuDJpbknXpSPgeg'
    for source in sorted(INFO.parent.glob('47 - yvqhR20m7Zg.*.vtt')):
        if not source.with_suffix('.txt').exists():
            source.with_suffix('.txt').write_bytes(texto_desde_vtt(source).encode('utf-8'))
    catalog_path = ROOT / 'campanas/xoltacan/catalogo.json'
    catalog = read_json(catalog_path)
    episode = dict(capitulo=47, id=metadata['id'], titulo='Cadáveres', url=metadata['webpage_url'])
    existing = [e for e in catalog['episodios'] if e['capitulo'] == 47 or e['id'] == episode['id']]
    assert not existing or existing == [episode]
    if not existing:
        catalog['episodios'].append(episode)
        save(catalog_path, catalog)
    dates_path = ROOT / 'campanas/xoltacan/config/emisiones.json'
    dates = read_json(dates_path)
    dates['capitulos']['47'] = dict(video_id=episode['id'], twitch=dict(
        estado='documentada', fecha='2026-07-24', fuentes=['1530274670023278874'], criterio='campana_numero_y_titulo',
        nota='La tarjeta conservada identifica campaña, capítulo y título; no fija el comienzo exacto del rol.',
        variantes=None, fechas_candidatas=['2026-07-24']), youtube=dict(
        estado='publicacion_documentada', fecha='2026-11-10', fecha_aviso=None, fuentes=[], origen_fecha='metadatos_youtube',
        archivo_metadatos=INFO.relative_to(ROOT).as_posix(), sha256_metadatos=sha(INFO),
        publicacion_reportada_utc=datetime.fromtimestamp(metadata['timestamp'], timezone.utc).isoformat()))
    save(dates_path, dates)
    durations_path = ROOT / 'campanas/xoltacan/config/duraciones_rol.json'
    durations = read_json(durations_path)
    durations['fuentes']['xoltacan47'] = dict(archivo=INFO.relative_to(ROOT).as_posix(), sha256=sha(INFO))
    durations['campanas']['xoltacan']['47'] = dict(video_id=episode['id'], segundos=metadata['duration'], fuente='xoltacan47')
    save(durations_path, durations)
    source = INFO.parent / '47 - yvqhR20m7Zg.es-orig.vtt'
    segments = parse_vtt(source)
    aliases = read_json(ROOT / 'campanas/xoltacan/config/nombres.json')['alias_confirmados']
    for segment in segments:
        segment['texto_normalizado'] = normalize(segment['texto_original'], aliases)
    tracking = read_json(FOLDER / 'seguimiento_antes.json')
    split = dict(capitulo=47, fuente=source.relative_to(ROOT).as_posix(), sha256=sha(source), total_segmentos=len(segments), bloques=[])
    for i in range(3):
        rows = segments[len(segments)*i//3:len(segments)*(i+1)//3]
        save(FOLDER / f'bloque_{i+1}_segmentos.json', rows)
        (FOLDER / f'bloque_{i+1}.md').write_bytes(('\n\n'.join(f'[{r["inicio"]}–{r["fin"]}] {r["texto_normalizado"]}' for r in rows) + '\n').encode())
        questions = tracking[len(tracking)*i//3:len(tracking)*(i+1)//3]
        save(FOLDER / f'preguntas_bloque_{i+1}.json', questions)
        split['bloques'].append(dict(bloque=i+1, inicio=rows[0]['inicio'], fin=rows[-1]['fin'], segmentos=len(rows),
            palabras=sum(len(r['texto_original'].split()) for r in rows), primer_segmento=rows[0]['id'], ultimo_segmento=rows[-1]['id'],
            preguntas_asignadas=[q['id'] for q in questions]))
    save(FOLDER / 'reparto.json', split)
    names = read_json(proof / 'identidades_confirmadas.json')
    save(FOLDER / 'identidades_contexto.json', names)
    originals = {p.relative_to(ROOT).as_posix(): dict(sha256=sha(p), bytes=p.stat().st_size) for p in sorted(INFO.parent.glob('47 - yvqhR20m7Zg.*'))}
    save(ROOT / 'campanas/xoltacan/revision/fuente_xoltacan_47.json', dict(
        **{k:metadata[k] for k in ('id','title','duration','upload_date','channel','channel_id','webpage_url')},
        capitulo=47, recuperado_el='2026-11-10', herramienta='yt-dlp', version='2026.08.19',
        lectura='Pendiente de lectura completa e integración; las descargas no equivalen a una revisión editorial.',
        originales=originals, reparto='campanas/xoltacan/revision/borradores/47/reparto.json'))
    print(json.dumps(split, ensure_ascii=False))


if __name__ == '__main__':
    main()
