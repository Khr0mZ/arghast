"""División editorial local de una unidad al incorporar el vídeo del capítulo 42."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from rol_escrito import (digest, load_written_role, read, scene_interval,
                         session_anchors, temporal_groups, validate_scene)

folder = ROOT / 'conocimiento/rol_escrito'
original_id = 'x-1524356880258961458'
original_path = folder / f'escenas/{original_id}.json'
manifest_path = folder / 'manifest.json'
backup = ROOT / 'borradores/42/rol_antes'
backup.mkdir(parents=True, exist_ok=True)
for path in (original_path, original_path.with_suffix('.md'), manifest_path):
    target = backup / path.name
    if not target.exists():
        shutil.copyfile(path, target)

before = read(backup / original_path.name)
manifest_before = read(backup / 'manifest.json')
catalog = read(ROOT / 'xoltacan_subtitulos/episodios.json') + read(ROOT / 'config/episodios_nuevos.json')
anchors = session_anchors('xoltacan', catalog)
groups = temporal_groups(before['fuentes'], anchors)
assert [len(g['fuentes_ids']) for g in groups] == [1, 5]
assert groups[0]['fuentes_ids'] == ['1524356880258961458']
assert groups[1]['fuentes_ids'][0] == '1524890107604369578'

# Cotejo de los seis originales completos con el archivo privado inalterado.
private_folder = ROOT / '.local/discord/fuentes/rol/20261020T152108Z'
private_manifest = read(private_folder / 'manifest.json')
assert digest(private_folder / 'manifest.json') == manifest_before['manifest_original_sha256']
thread = next(t for t in private_manifest['campanas']['xoltacan']['hilos'] if t['id'] == before['hilo_id'])
private_path = private_folder / thread['archivo_mensajes']
assert digest(private_path) == thread['sha256_mensajes']
original_messages = {m['id']: m for m in read(private_path)}
for source in before['fuentes']:
    message = original_messages[source['id']]
    assert source['texto'] == message['content']
    assert source['fecha_utc'] == message['timestamp']
    expected = hashlib.sha256(json.dumps(message, ensure_ascii=False, sort_keys=True,
                                         separators=(',', ':')).encode('utf-8')).hexdigest()
    assert source['mensaje_sha256'] == expected

scenes = []
for group in groups:
    scene = copy.deepcopy(before)
    scene['fuentes'] = [s for s in scene['fuentes'] if s['id'] in group['fuentes_ids']]
    scene['id'] = 'x-' + scene['fuentes'][0]['id']
    scene['inicio_utc'] = scene['fuentes'][0]['fecha_utc']
    scene['fin_utc'] = scene['fuentes'][-1]['fecha_utc']
    scene['fecha_local'] = scene['fuentes'][0]['fecha_local']
    scene['intervalo'] = scene_interval(group['frame'], anchors)
    scene['evidencias'] = [e for e in scene['evidencias'] if e['mensaje_id'] in group['fuentes_ids']]
    scenes.append(scene)

first, second = scenes
first.update(
    titulo='El insomnio de Citlali',
    resumen='En el templo de Iktan, Citlali recuerda a Amaru y descubre algo extraño en su bolsillo.',
    relato='Citlali no consigue dormir en el templo de Iktan. Los siseos de las serpientes y unos recuerdos cargados de culpa le impiden descansar. Mira a Eztli dormir en paz y oye las voces de Walulu y una elfa en otra habitación, sin intervenir en su conversación.\n\nVuelve a pronunciar el nombre de Amaru entre amargura y añoranza. Mientras busca un trozo de chocolate en su falda, nota algo extraño dentro del bolsillo y se pregunta qué es. Este mensaje no identifica todavía el objeto ni muestra la melodía, el dolor o la marca que se narrarán después.',
    evidencias=[
        dict(mensaje_id='1524356880258961458', afirmacion='Citlali permanece despierta en el templo de Iktan mientras Eztli duerme; recuerda a Amaru y nota algo extraño en el bolsillo al buscar chocolate.', tipo='accion')
    ],
    notas=[
        'Amaru aparece en el recuerdo de Citlali; no se describe su estado actual.',
        'El objeto del bolsillo no se identifica en este mensaje. Su descubrimiento continúa en la subescena posterior al corte estimado del capítulo 42.',
        'La división conserva la fecha de publicación de los mensajes; no atribuye una pausa ficticia o un cambio de lugar a Citlali.'
    ])
second['relato'] = ('La búsqueda de Citlali da lugar al hallazgo de una pequeña caja de música con manivela, madera gastada y delicados grabados en la tapa. Al hacerla sonar, la melodía le recuerda a sus niños y enlaza la imagen de Amaru y de un bebé en un cofre con otra de Nox sonriendo junto a una hoguera.\n\n'
    'La quietud se vuelve extraña: viento y hojas parecen detenerse. Citlali siente un ardor bajo la piel que crece hasta quitarle el aire y apenas puede pedir ayuda a Walulu. Después llega el silencio y el dolor cesa. Se levanta de golpe, despierta a Eztli y se dispone a salir con urgencia.\n\n'
    'La narración le impone la certeza de que debe correr hacia un lugar, sin que comprenda cómo sabe hacerlo. Al mirar el brazo no distingue una quemadura evidente, pero sí un trazo oscuro diminuto que empieza a formarse y crecer bajo la piel. El vínculo con lo ocurrido casi cuarenta años antes aparece como una advertencia evocada por el narrador; no se revela todavía la causa de la marca, su mecanismo ni el estado actual de Amaru. La carrera continúa en la unidad siguiente.')
second['notas'].append('Esta subescena reúne los cinco mensajes publicados después del final estimado del capítulo 42; la apertura de Citlali permanece en la subescena anterior sin duplicar su mensaje.')

def markdown_scene(scene):
    interval = scene['intervalo']
    position = ('Antes del capítulo ' + str(interval['siguiente']) if interval['anterior'] is None else
                'Después del capítulo ' + str(interval['anterior']) if interval['siguiente'] is None else
                f'Entre los directos {interval["anterior"]} y {interval["siguiente"]}')
    lines = ['# ' + scene['titulo'], '', position + '.', '', scene['relato'], '', '## Evidencias', '']
    for evidence in scene['evidencias']:
        source = next(s for s in scene['fuentes'] if s['id'] == evidence['mensaje_id'])
        lines.append(f'- {evidence["afirmacion"]} [Mensaje original]({source["url_discord"]}).')
    lines.extend(['', '## Notas de lectura', '', *('- ' + n for n in scene['notas']),
                  '', '## Interacción original completa', ''])
    for source in scene['fuentes']:
        lines.extend([f'### {source["fecha_utc"]} · {source["id"]}', '', source['texto'], '',
                      f'[Ver en Discord]({source["url_discord"]})', ''])
    return '\n'.join(lines).rstrip() + '\n'

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

new_records = []
for scene in scenes:
    validate_scene(scene, 'xoltacan')
    assert len(temporal_groups(scene['fuentes'], anchors)) == 1
    path = folder / f'escenas/{scene["id"]}.json'
    write_json(path, scene)
    path.with_suffix('.md').write_text(markdown_scene(scene), encoding='utf-8')
    new_records.append(dict(id=scene['id'], archivo=path.relative_to(folder).as_posix(), sha256=digest(path)))

assert [s for scene in scenes for s in scene['fuentes']] == before['fuentes']
assert len({s['id'] for scene in scenes for s in scene['fuentes']}) == 6
manifest = read(manifest_path)
new_id = second['id']
manifest['escenas'] = [r for r in manifest['escenas'] if r['id'] != new_id]
position = next(i for i, r in enumerate(manifest['escenas']) if r['id'] == original_id)
manifest['escenas'][position:position+1] = new_records
manifest['estadisticas']['escenas'] = len(manifest['escenas'])
for key, value in manifest_before['estadisticas'].items():
    if key != 'escenas':
        assert manifest['estadisticas'][key] == value
write_json(manifest_path, manifest)

decision = dict(
    campana='xoltacan', unidad_revision=original_id,
    motivo='La duración conservada del vídeo 42 introduce un corte operativo entre el primer mensaje y los cinco siguientes de esta unidad. Se releen los seis mensajes y se divide editorialmente sin perder ni duplicar fuentes.',
    corte_estimado_utc=next(a['corte_ordenacion_utc'] for a in anchors if a['capitulo'] == 42),
    limitacion='El corte ordena por publicación y duración del vídeo; no certifica la hora real de la partida ni un salto temporal dentro de la ficción.',
    original_editorial=dict(archivo=(backup / original_path.name).relative_to(ROOT).as_posix(), sha256=digest(backup / original_path.name)),
    fuentes_privadas_verificadas=dict(manifest_sha256=digest(private_folder / 'manifest.json'), archivo_hilo_sha256=digest(private_path), mensajes=6),
    escenas=[dict(id=s['id'], titulo=s['titulo'], mensajes=len(s['fuentes']), fuentes_ids=[m['id'] for m in s['fuentes']],
                  anterior=s['intervalo']['anterior'], siguiente=s['intervalo']['siguiente'], relato=s['relato']) for s in scenes],
    estadisticas_antes=manifest_before['estadisticas'], estadisticas_despues=manifest['estadisticas'],
    fuentes_conservadas_integras_una_vez=True,
    informes_hilo='Sin cambios: no contienen vínculos de escena a los mensajes trasladados; sus evidencias por mensaje siguen existiendo.',
    verificacion={})
write_json(ROOT / 'borradores/42/division_rol.json', decision)
result = load_written_role('xoltacan', catalog, output=ROOT / '.pruebas/cap42_rol/rol_escrito')
decision['verificacion'] = dict(load_written_role='correcto', escenas=len(result['scenes']), mensajes=result['stats']['mensajes_en_escenas'],
                                fuentes_sha256='cotejadas con los mensajes originales y el manifest privado')
write_json(ROOT / 'borradores/42/division_rol.json', decision)
print(json.dumps(dict(escenas=[dict(id=s['id'],mensajes=len(s['fuentes']),anterior=s['intervalo']['anterior'],siguiente=s['intervalo']['siguiente']) for s in scenes],
                      verificacion=decision['verificacion']),ensure_ascii=False))
