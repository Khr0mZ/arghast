"""Mantiene con su escena un aviso administrativo posterior al corte del vídeo 43."""
import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from rol_escrito import read, digest, session_anchors, temporal_groups, scene_interval, validate_scene
from preparar import save


def main():
    folder = ROOT / 'conocimiento/rol_escrito'
    path = folder / 'escenas/x-1525042844560003125.json'
    manifest_path = folder / 'manifest.json'
    backup = ROOT / 'borradores/43/rol_antes'
    backup.mkdir(exist_ok=True)
    for original in (path, path.with_suffix('.md'), manifest_path):
        target = backup / original.name
        if not target.exists():
            shutil.copyfile(original, target)
    before = read(backup / path.name)
    scene = copy.deepcopy(before)
    notice = next(s for s in scene['fuentes'] if s['id'] == '1525248830570893413')
    assert notice['texto'] == '<@753394009153732689> <@220602485977382912> <@210947008716996609>'
    notice['no_narrativo'] = True
    notice['nota_editorial'] = 'Aviso por mención de usuarios, sin acción narrativa; conserva la posición de la escena que anuncia.'
    for a, b in zip(before['fuentes'], scene['fuentes']):
        assert all(a.get(k) == b.get(k) for k in ('id', 'texto', 'texto_sha256', 'mensaje_sha256', 'fecha_utc', 'adjuntos'))
    catalog = read(ROOT / 'xoltacan_subtitulos/episodios.json') + read(ROOT / 'config/episodios_nuevos.json')
    anchors = session_anchors('xoltacan', catalog)
    old_groups = temporal_groups(before['fuentes'], anchors)
    groups = temporal_groups(scene['fuentes'], anchors)
    assert len(old_groups) == 2 and len(groups) == 1
    scene['intervalo'] = scene_interval(groups[0]['frame'], anchors)
    validate_scene(scene, 'xoltacan')
    save(path, scene)
    manifest = read(manifest_path)
    record = next(r for r in manifest['escenas'] if r['id'] == scene['id'])
    record['sha256'] = digest(path)
    save(manifest_path, manifest)
    assert manifest['estadisticas'] == read(backup / 'manifest.json')['estadisticas']
    save(ROOT / 'borradores/43/ajuste_rol.json', dict(
        escena=scene['id'], mensajes=len(scene['fuentes']),
        fuente_aviso=notice['id'], texto_sha256=notice['texto_sha256'],
        original_editorial=dict(archivo=(backup / path.name).relative_to(ROOT).as_posix(), sha256=digest(backup / path.name)),
        motivo='La duración del capítulo 43 sitúa un aviso de usuarios después del corte estimado. El aviso carece de acción y se conserva con su escena, sin inventar otra ni duplicar mensajes.',
        corte_estimado_utc=next(a['corte_ordenacion_utc'] for a in anchors if a['capitulo'] == 43),
        antes=old_groups, despues=groups,
        estadisticas=manifest['estadisticas'], fuentes_originales_conservadas=True))
    for record in manifest['escenas']:
        item = read(folder / record['archivo'])
        assert len(temporal_groups(item['fuentes'], anchors)) == 1, item['id']
    print('304 escenas y 6241 mensajes conservados; aviso administrativo unido a su escena.')


if __name__ == '__main__':
    main()
