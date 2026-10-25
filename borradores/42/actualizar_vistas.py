"""Actualiza procedencia y vistas de consulta tras la integración editorial del 42."""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import read_json, write_json, write, sha

FOLDER = ROOT / 'borradores/42'
INFO = ROOT / 'xoltacan_subtitulos/subtitulos/42 - 3IUV_YN_zxM.info.json'
METADATA = read_json(INFO)
INTEGRATION = read_json(FOLDER / 'integracion.json')
MAP = INTEGRATION['mapa_referencias']


def refs(text):
    return re.sub(r'\b42-\d{3}\b', lambda m: MAP[m[0]], text)


def appendix(filename, title, body):
    path = ROOT / 'conocimiento' / filename
    content = path.read_text(encoding='utf-8')
    marker = '\n\n## ' + title
    content = content.split(marker)[0]
    write(path, content.rstrip() + marker + '\n\n' + refs(body).strip() + '\n')


def main():
    path = ROOT / 'config/emisiones_xoltacan.json'
    dates = read_json(path)
    dates['capitulos']['42']['twitch']['nota'] = 'Dos tarjetas del mismo día conservan campaña, capítulo y título. La hora del aviso no fija el inicio exacto de la partida.'
    write_json(path, dates)
    path = ROOT / 'config/duraciones_rol.json'
    durations = read_json(path)
    durations['fuentes']['xoltacan42'] = dict(archivo=INFO.relative_to(ROOT).as_posix(), sha256=sha(INFO))
    durations['campanas']['xoltacan']['42'] = dict(video_id=METADATA['id'], segundos=METADATA['duration'], fuente='xoltacan42')
    write_json(path, durations)
    originals = {p.relative_to(ROOT).as_posix(): dict(sha256=sha(p), bytes=p.stat().st_size)
                 for p in sorted(INFO.parent.glob('42 - 3IUV_YN_zxM.*'))}
    write_json(ROOT / 'config/fuente_xoltacan_42.json', dict(
        id=METADATA['id'], title=METADATA['title'], duration=METADATA['duration'],
        upload_date=METADATA['upload_date'], channel=METADATA['channel'],
        channel_id=METADATA['channel_id'], webpage_url=METADATA['webpage_url'],
        capitulo=42, recuperado_el='2026-10-25', herramienta='yt-dlp', version='2026.08.19',
        lectura='Tres bloques completos sin solapamiento; 72 registros, trece etapas de relato y cotejo de las 246 preguntas anteriores. Audio no cotejado.',
        txt='Representaciones legibles generadas desde los VTT con el descargador del proyecto; los VTT son la fuente principal.',
        originales=originals, reparto='borradores/42/reparto.json',
        integracion='borradores/42/integracion.json'))
    catalog = read_json(ROOT / 'config/entidades.json')
    for group in catalog['grupos']:
        if group['nombre'] == 'Taylor':
            group['etiquetas'] = list(dict.fromkeys(group['etiquetas'] + ['Tylor', 'Tayor']))
        if group['nombre'] == 'El Garfio':
            group['etiquetas'] = list(dict.fromkeys(group['etiquetas'] + ['Arrecife del Garfio']))
        if group['nombre'] == 'Elger Banana':
            group['etiquetas'] = list(dict.fromkeys(group['etiquetas'] + ['Banana']))
        if group['nombre'] == 'Invictus':
            group['descripcion'] = 'Buque de Tórtola saboteado por Nox y Pinky que explota contra la flota de la Marina en el Arrecife del Garfio.'
            group['nota'] = 'Su reputación de invicto no implica invulnerabilidad. La figura encadenada de los calabozos se identifica después como Pinky; no es otra identidad.'
    write_json(ROOT / 'config/entidades.json', catalog)
    dossier = read_json(ROOT / 'conocimiento/capitulos/42.json')
    appendix('MISIONES.md', 'Actualización del capítulo 42', '\n\n'.join(
        '- ' + line + ' ([ficha](capitulos/42.md)).' for line in read_json(FOLDER / 'edicion_integrada.json')['misiones']))
    appendix('RELACIONES.md', 'Vínculos al cierre de la batalla del Garfio', '''
Ione y Poncelot refuerzan su confianza: él le regala el fular y combate a su lado; Ilikar vuelve a Shiaru y ayuda a maniobrar, abordar y protegerla. Jack recibe la promesa de protección y el gorro de Ione ([42-003, 42-008–42-009, 42-106, 42-114 y 42-219](capitulos/42.md)).

Nox comienza en el Invictus buscando una patente de corso, pero sabotea a la Marina, libera a Pinky y acaba impidiendo que Tórtola desvíe el buque. Reconoce a Ione como capitana y pide volver a su tripulación. Ella busca su cuerpo sin encontrarlo; no se convierte su vínculo en una relación sentimental confirmada ([42-004, 42-108, 42-118–42-119 y 42-205–42-216](capitulos/42.md)).

Bonnie entrega la moneda a Ione y exige que retire el Zampaolas. Los otros reyes la rodean: Taylor le reprocha ocultar Xoltacan y le dispara ante Diente de Oro, Banana y Sonriente. El desenlace rompe la posición anterior de Bonnie sin mostrar una nueva autoridad de Shiaru ([42-217–42-224](capitulos/42.md)).
''')
    appendix('ATLAS.md', 'El arrecife y la costa en el capítulo 42', '''
La defensa de Shiaru se desplaza a los arrecifes del Garfio. El menor calado permite al Zampaolas maniobrar con el ancla de Ilikar; Nox altera la apariencia de las aguas para encallar a dos escoltas y conduce después el Invictus a la batalla. La explosión acerca al Zampaolas a la costa sin encallarlo. Su retirada no establece un nuevo asentamiento ni el abandono definitivo de Shiaru ([42-017, 42-110–42-114, 42-124 y 42-214–42-219](capitulos/42.md)).

Taylor refiere una captura de un barco rumbo a Puerto de Espadas. Es un destino del viaje relatado, sin ubicación exacta de la captura ni llegada mostrada ([42-222](capitulos/42.md)).
''')
    appendix('FACCIONES.md', 'Cambio de fuerzas en el capítulo 42', '''
La tripulación del Zampaolas combate con la pequeña flotilla de Shiaru contra la Marina. Nox rompe su colaboración con Tórtola mediante el sabotaje. Las embestidas de Bonnie y el estallido del Invictus destruyen buques; otros refuerzos llegan y son aniquilados por hielo y fuego cuando aparecen los cuatro reyes restantes ([42-004, 42-011–42-019, 42-118–42-125 y 42-214–42-217](capitulos/42.md)).

Los cinco reyes coinciden en el barco de Bonnie. Diente de Oro, Elger Banana, Sonriente y Taylor llegan a una isla cuyo secreto Taylor reprocha a Bonnie haber guardado. El disparo final no equivale a una deliberación sobre el gobierno de la isla; las cláusulas del pacto y los planes posteriores permanecen abiertos ([42-220–42-224](capitulos/42.md)).
''')
    path = ROOT / 'conocimiento/MISTERIOS.md'
    content = path.read_text(encoding='utf-8').replace('estado al cierre del capítulo 41', 'estado al cierre del capítulo 42')
    replacements = {
        'Ojo/orbe —': '| Ojo/orbe — con Nox antes del estallido; paradero posterior abierto | Nox lleva el ojo en su chaqueta y nota los tatuajes antes de renunciar a escapar del Invictus. | [42-213–42-214](capitulos/42.md) | No se explica la función de las señales, una protección o un escape, ni se recupera el objeto. |',
        'Zampaolas —': '| Zampaolas — vuelve a navegar y sale de la batalla | Ione relata la reparación y equipa la nave; navega, maniobra, recibe nuevos impactos y retira a la tripulación. | [42-002, 42-013, 42-101, 42-114 y 42-219](capitulos/42.md) | La reparación pendiente del capítulo 38 queda superada por la navegación mostrada. Sigue sin mostrarse una guarnición en las ruinas del lago. |',
        'Molly, Bonnie y Tórtola —': '| Molly, Bonnie y Tórtola — desenlace naval y cambio de fuerzas | Molly prepara la defensa junto a Bonnie. Nox libera a Pinky, sabotea el Invictus y lo hace estallar; Tórtola sigue a bordo antes del estallido. Taylor dispara a Bonnie después de la llegada de los cuatro reyes. | [42-006, 42-108, 42-212–42-214 y 42-220–42-224](capitulos/42.md) | El director despide a Bonnie, Nox y Pinky. No se muestran cuerpos recuperados, una restitución de Molly o el nuevo gobierno de Shiaru. |',
        'Cipo y el fragmento de espada —': '| Cipo y el fragmento de espada — reunión posterior; origen abierto | Cipo reaparece con Poncelot e Ilikar y participa en los abordajes. Pinky recuerda su búsqueda desde otro barco. | [41-008 y 41-014](capitulos/41.md), [42-113, 42-122, 42-202 y 42-209](capitulos/42.md) | No se explica cómo Ilikar supo del rescate ni se reúnen Pinky y Cipo en escena. El fragmento sigue sin dueño, origen o función. |',
    }
    lines = content.splitlines()
    for i, line in enumerate(lines):
        for beginning, replacement in replacements.items():
            if line.startswith('| ' + beginning):
                lines[i] = refs(replacement)
    write(path, '\n'.join(lines) + '\n')
    appendix('MISTERIOS.md', 'Preguntas nuevas de la batalla', '''
La búsqueda de Nox no recupera su cuerpo y el director lo despide junto a Pinky y Bonnie. El ojo-orbe queda sin paradero documentado después del estallido. La entrega de la moneda, el disparo de Taylor, el pacto de los reyes y el testimonio sobre Jackie abren el seguimiento siguiente. Los poderes de hielo y fuego no se atribuyen a cada rey por separado ([42-213–42-224](capitulos/42.md)).

Las siete preguntas nuevas y sus límites se conservan en [el capítulo 42](capitulos/42.md) y en [el seguimiento individual](SEGUIMIENTO.md). Las 246 anteriores se cotejan hasta este capítulo; una trama sin novedades no se cierra por falta de menciones.
''')
    path = ROOT / 'conocimiento/TRAMAS.md'
    content = path.read_text(encoding='utf-8')
    if '[Continuidad del capítulo 42]' not in content:
        content = content.replace('- [Continuidad del capítulo 41](continuidad_41.md).', '- [Continuidad del capítulo 41](continuidad_41.md).\n- [Continuidad del capítulo 42](continuidad_42.md).')
    write(path, content)
    total_facts = sum(len(read_json(p)['afirmaciones']) for p in (ROOT / 'conocimiento/capitulos').glob('*.json'))
    from catalogo import load_catalog, canonical_labels
    aliases, notes, excluded = load_catalog()
    mentioned = {name for p in (ROOT / 'conocimiento/capitulos').glob('*.json')
                 for fact in read_json(p)['afirmaciones']
                 for name in canonical_labels(fact.get('entidades', []), aliases)}
    visible = [g for name, g in notes.items() if name in mentioned and g.get('tipo')
               and g.get('visible', True) and name not in excluded]
    entity_count = len(visible)
    character_count = sum(g['tipo'] == 'personaje' for g in visible)
    path = ROOT / 'README.md'
    content = path.read_text(encoding='utf-8')
    for old, new in [
        ('1115 registros, 163 fichas', f'1115 registros, {entity_count} fichas'),
        ('Los 90 personajes incluyen', f'Los {character_count} personajes incluyen'),
        ('sus 41 capítulos revisados, 1043 registros, 153 fichas', f'sus 42 capítulos revisados, {total_facts} registros, {entity_count} fichas'),
        ('los 41 capítulos, 1043 registros', f'los 42 capítulos, {total_facts} registros'),
        ('Los **41 capítulos**', 'Los **42 capítulos**'),
        ('hasta el capítulo 41.', 'hasta el capítulo 42.'),
        ('las 246 preguntas históricas de Xoltacan', 'las 253 preguntas históricas de Xoltacan'),
        ('**sus 41 capítulos: 37 documentadas y 4 asumidas**', '**sus 42 capítulos: 38 documentadas y 4 asumidas**'),
        ('Hay 41 capítulos catalogados, 82 VTT y 82 TXT', 'Hay 42 capítulos catalogados, 84 VTT y 84 TXT'),
        ('01/ … 41/', '01/ … 42/'),
        ('Los 41 capítulos disponibles se han leído completos y cuentan con fichas estructuradas: 1043 registros', f'Los 42 capítulos disponibles se han leído completos y cuentan con fichas estructuradas: {total_facts} registros'),
        ('las tramas abiertas al capítulo 41 permanecen abiertas.', 'las tramas abiertas se mantienen con su seguimiento actualizado al capítulo 42.'),
    ]:
        content = content.replace(old, new)
    marker = '\n\nEl **capítulo 42, Batalla en el Arrecife del Garfio**'
    content = content.split(marker)[0].rstrip() + marker + ' (directo del 09/07/2026; publicado en YouTube el 25/10/2026), está incorporado con lectura íntegra en tres bloques sin solapamiento, 72 evidencias, trece etapas y ocho fichas nuevas. Las 246 preguntas anteriores están cotejadas y se añaden siete: 253 en total. El Zampaolas vuelve a navegar, Nox libera a Pinky y llegan los cuatro reyes restantes. Se conservan el desenlace del Invictus, la despedida del director y los límites de la búsqueda y del disparo final. Véanse [la continuidad](conocimiento/continuidad_42.md) y [la procedencia con hashes](config/fuente_xoltacan_42.json). Versión local para revisión, sin publicación autorizada.\n'
    write(path, content)
    print(f'Vistas y procedencia: {total_facts} evidencias; {entity_count} identidades.')


if __name__ == '__main__':
    main()
