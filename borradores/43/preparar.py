"""Registra el vídeo 43 y sus fechas sin convertir la descarga en revisión editorial."""
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import read_json, sha
import json

INFO = ROOT / 'xoltacan_subtitulos/subtitulos/43 - tSdmoZCWEZQ.info.json'


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    newline = '\r\n' if path.exists() and b'\r\n' in path.read_bytes() else '\n'
    text = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    path.write_bytes(text.replace('\n', newline).encode('utf-8'))


def main():
    metadata = read_json(INFO)
    assert metadata['id'] == 'tSdmoZCWEZQ'
    assert metadata['channel_id'] == 'UCWJ11LdxIuDJpbknXpSPgeg'
    path = ROOT / 'config/episodios_nuevos.json'
    episodes = read_json(path)
    item = dict(capitulo=43, id=metadata['id'], titulo='Batalla en la Jungla del Garfio', url=metadata['webpage_url'])
    previous = [e for e in episodes if e['capitulo'] == 43 or e['id'] == item['id']]
    assert not previous or previous == [item]
    if not previous:
        save(path, episodes + [item])
    path = ROOT / 'config/emisiones_xoltacan.json'
    dates = read_json(path)
    dates['capitulos']['43'] = dict(video_id=item['id'], twitch=dict(
        estado='documentada', fecha='2026-07-10', fuentes=['1525209204300841101'],
        criterio='campana_numero_y_titulo',
        nota='La tarjeta conservada identifica campaña, capítulo y título. La emisión se distingue del tiempo ficticio de la batalla y de la publicación posterior.',
        variantes=None, fechas_candidatas=['2026-07-10']), youtube=dict(
        estado='publicacion_documentada', fecha='2026-10-27', fecha_aviso=None, fuentes=[],
        origen_fecha='metadatos_youtube', archivo_metadatos=INFO.relative_to(ROOT).as_posix(),
        sha256_metadatos=sha(INFO),
        publicacion_reportada_utc=datetime.fromtimestamp(metadata['timestamp'], timezone.utc).isoformat()))
    save(path, dates)
    path = ROOT / 'config/duraciones_rol.json'
    durations = read_json(path)
    durations['fuentes']['xoltacan43'] = dict(archivo=INFO.relative_to(ROOT).as_posix(), sha256=sha(INFO))
    durations['campanas']['xoltacan']['43'] = dict(video_id=item['id'], segundos=metadata['duration'], fuente='xoltacan43')
    save(path, durations)
    originals = {p.relative_to(ROOT).as_posix(): dict(sha256=sha(p), bytes=p.stat().st_size)
                 for p in sorted(INFO.parent.glob('43 - tSdmoZCWEZQ.*'))}
    save(ROOT / 'config/fuente_xoltacan_43.json', dict(
        id=metadata['id'], title=metadata['title'], duration=metadata['duration'], upload_date=metadata['upload_date'],
        channel=metadata['channel'], channel_id=metadata['channel_id'], webpage_url=metadata['webpage_url'],
        capitulo=43, recuperado_el='2026-10-27', herramienta='yt-dlp', version='2026.08.19',
        lectura='Pendiente de integrar las tres lecturas completas; descargar fuentes no equivale a revisión editorial.',
        txt='Representaciones legibles generadas desde los VTT con el descargador del proyecto; los VTT son la fuente principal.',
        originales=originals, reparto='borradores/43/reparto.json'))
    print('Vídeo 43, emisión, publicación y duración registrados; cinco originales con hashes.')


if __name__ == '__main__':
    main()
