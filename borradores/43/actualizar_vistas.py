"""Actualiza las vistas de consulta y la procedencia del capítulo 43, solo en local."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import read_json
from catalogo import load_catalog, canonical_labels
from preparar import save

FOLDER = ROOT / 'borradores/43'
MAPPING = read_json(FOLDER / 'integracion.json')['mapa_referencias']


def refs(text):
    return re.sub(r'\b43-\d{3}\b', lambda m: MAPPING[m[0]], text)


def write(path, text):
    newline = '\r\n' if path.exists() and b'\r\n' in path.read_bytes() else '\n'
    path.write_bytes(text.replace('\n', newline).encode('utf-8'))


def appendix(filename, title, body):
    path = ROOT / 'conocimiento' / filename
    content = path.read_text(encoding='utf-8')
    marker = '\n\n## ' + title
    content = content.split(marker)[0].rstrip() + marker + '\n\n' + refs(body).strip() + '\n'
    write(path, content)


def main():
    catalog = read_json(ROOT / 'config/entidades.json')
    for group in catalog['grupos']:
        if group['nombre'] == 'Nox':
            group['etiquetas'] = list(dict.fromkeys(group['etiquetas'] + ['Amaru', 'Amaru (reconocido por Citlali)']))
            note = 'En el capítulo 43, Citlali reconoce en Nox al hijo que llama Amaru; la escena no reconstruye el rescate del cofre ni su crianza.'
            if note not in group['nota']:
                group['nota'] += ' ' + note
        if group['nombre'] == 'Caja de música de Citlali':
            group['etiquetas'] = list(dict.fromkeys(group['etiquetas'] + ['Caja musical de Citlali']))
    save(ROOT / 'config/entidades.json', catalog)
    # La nueva perspectiva confirma la activación previa, no una devolución a una dueña anterior.
    for filename, collection in [('historias_personajes_complementarias.json', 'personajes'), ('historias_objetos.json', 'entidades')]:
        path = ROOT / 'config' / filename
        doc = read_json(path)
        for entries in doc[collection].values():
            for stage in entries:
                stage['titulo'] = stage['titulo'].replace('La moneda devuelta y el disparo de Taylor', 'La entrega de la moneda y el disparo de Taylor').replace('El poder vuelve a manos de Ione', 'El poder pasa a manos de Ione')
        save(path, doc)
    editorial = read_json(FOLDER / 'edicion_integrada.json')
    appendix('MISIONES.md', 'Actualización del capítulo 43', '\n\n'.join('- ' + m + ' ([ficha](capitulos/43.md)).' for m in editorial['misiones']))
    appendix('RELACIONES.md', 'El frente terrestre y el reconocimiento de Amaru', '''
Molly organiza la defensa terrestre mientras Bonnie dirige la naval. Eleanor ayuda por el trato dado a Erandy y le entrega un broche a Molly. Erandy protege a su señora; Eleanor deja su escudo para cubrirla e intenta mantenerla en retaguardia, pero el trance de la escudera la empuja a seguir avanzando ([43-002, 43-005, 43-009–43-010, 43-014–43-016, 43-107, 43-113 y 43-116](capitulos/43.md)).

Lunaria lleva a Citlali y a Etley por la jungla, lucha junto a ellas y las protege del fuego. Eleanor monta al oso y combina su energía con el impacto de la caída. La cooperación no equivale a compartir el conocimiento de las visiones privadas de Citlali ([43-011–43-013, 43-108, 43-114, 43-117–43-120, 43-206 y 43-212](capitulos/43.md)).

Citlali reconoce en Nox al hijo que llama Amaru, llora su pérdida y trata de alcanzar el Zampaolas. Molly comprende su mirada y queda conmocionada. La historia del niño en el cofre y sus años hasta la vida adulta aún no se reconstruyen ([43-203, 43-209, 43-217 y 43-219](capitulos/43.md)).

El ser serpentino incita a Citlali a matar y quitar juventud. La escena final enlaza sus símbolos con un altar, sin dar un nombre a la entidad o equipararla automáticamente con otras presencias de la campaña ([43-203–43-204, 43-208 y 43-220](capitulos/43.md)).
''')
    appendix('ATLAS.md', 'La jungla del Garfio en el capítulo 43', '''
El frente terrestre forma parte de la misma defensa que el arrecife del capítulo 42. Molly conduce a los piratas hasta un embudo con trampas y tiradores ocultos para impedir el avance sobre Shiaru. Liz permanece en el poblado tras barricadas. El punto no se identifica con las ruinas del lago del capítulo 36 ([43-001, 43-005, 43-008, 43-010 y 43-014–43-018](capitulos/43.md)).

Citlali y Lunaria llegan desde la jungla; los personajes ven la explosión naval desde tierra y al final distinguen el Zampaolas detenido o varado en la costa oriental. No se representa aún el encuentro con sus tripulantes ([43-011–43-013, 43-102, 43-202 y 43-219](capitulos/43.md)).

El altar del epílogo carece de localización. La imagen no da coordenadas ni prueba que esté en el campo de batalla o en un templo ya explorado ([43-220](capitulos/43.md)).
''')
    appendix('FACCIONES.md', 'Resultado terrestre del capítulo 43', '''
La alianza defensiva de Molly y Bonnie se contempla desde la jungla. Molly sigue sin su antiguo cargo de capitana de la Marina y dirige piratas cuya preparación juzga inferior. Erandy, Eleanor, Citlali y Lunaria rompen a los pelotones con fuego, golpes y ataques masivos. La caída de los mandos fuerza la huida de los supervivientes; no se elimina toda la organización ([43-005, 43-010, 43-014, 43-101, 43-105, 43-109, 43-213 y 43-216](capitulos/43.md)).

La victoria de Molly en tierra no demuestra una restitución en la Marina ni un nuevo gobierno de Shiaru después del disparo de Taylor contra Bonnie. Los dos capítulos cubren frentes y momentos parcialmente simultáneos ([43-001, 43-202, 43-216–43-217](capitulos/43.md)).
''')
    path = ROOT / 'conocimiento/MISTERIOS.md'
    text = path.read_text(encoding='utf-8').replace('estado al cierre del capítulo 42', 'estado al cierre del capítulo 43')
    replacements = {
        'Citlali: daño, drenaje y rejuvenecimiento': '| Citlali: absorción vital observada; origen abierto | El toque cierra heridas, las víctimas envejecen y Citlali rejuvenece. Un ser le ordena quitar juventud y activa un altar de símbolos idénticos a sus tatuajes. | [43-115, 43-203–43-204, 43-208, 43-215 y 43-220](capitulos/43.md) | No se explican el origen, las reglas completas, la edad final o la duración de los cambios. |',
        'Nox como el bebé perdido': '| Nox y Amaru — reconocimiento materno; historia intermedia abierta | Citlali ve a Nox durante la explosión, lo llora como a un hijo y lo recuerda como Amaru, contraponiendo al niño del cofre con el adulto. | [43-003, 43-203, 43-217 y 43-219](capitulos/43.md) | Falta reconstruir el rescate y la crianza; la identificación emocional no proporciona una cronología completa. |',
        'Molly, Bonnie y Tórtola': '| Molly, Bonnie y Tórtola — dos frentes de la misma batalla | La defensa terrestre comienza junto a la partida de la flota. Molly combate y termina herida, mientras la explosión naval se contempla desde la jungla. | [43-001, 43-005, 43-202 y 43-213–43-217](capitulos/43.md), [42-060–42-072](capitulos/42.md) | La presencia inicial de Bonnie no demuestra una vuelta después del disparo. No se reconstruyen nuevos destinos de Pinky y Tórtola o un gobierno posterior de Shiaru. |',
    }
    lines = text.splitlines()
    for i, line in enumerate(lines):
        for beginning, replacement in replacements.items():
            if line.startswith('| ' + beginning):
                lines[i] = refs(replacement)
    write(path, '\n'.join(lines) + '\n')
    appendix('MISTERIOS.md', 'El altar y las consecuencias del capítulo 43', '''
La entidad serpentina ordena a Citlali matar y quitar juventud. En el epílogo enciende símbolos exactamente iguales a los de su cuerpo y anuncia que ya es la hora, sin nombre, localización o consecuencia posterior mostrados ([43-203–43-204 y 43-220](capitulos/43.md)).

Citlali intenta alcanzar el Zampaolas y Erandy queda agotada después del trance. La leyenda ligada al ofrecimiento del broche y la procedencia de la caja de música siguen abiertas. Las ocho preguntas de esta sesión se conservan en [el capítulo 43](capitulos/43.md) y en [el seguimiento individual](SEGUIMIENTO.md).
''')
    path = ROOT / 'conocimiento/TRAMAS.md'
    text = path.read_text(encoding='utf-8')
    if '[Continuidad del capítulo 43]' not in text:
        text = text.replace('- [Continuidad del capítulo 42](continuidad_42.md).', '- [Continuidad del capítulo 42](continuidad_42.md).\n- [Continuidad del capítulo 43](continuidad_43.md).')
    write(path, text)
    continuity = '''# Continuidad del capítulo 43

Batalla en la Jungla del Garfio se incorpora tras leer completos los 2.763 segmentos de la transcripción en tres bloques sin solapamiento: 00:00:01.280–00:41:56.510, 00:41:56.520–01:22:34.550 y 01:22:34.560–02:06:16.559. Contiene 62 evidencias, once etapas y seis fichas nuevas. La [procedencia y los cinco hashes](../config/fuente_xoltacan_43.json), el [reparto](../borradores/43/reparto.json) y la [integración](../borradores/43/integracion.json) conservan su trazabilidad. No se ha cotejado el audio.

## Dos frentes, un mismo ataque

La apertura sitúa la acción al mismo tiempo que el inicio de la partida naval. La plaza, el discurso y la activación de la moneda de Bonnie son el mismo acontecimiento visto desde el grupo terrestre. Las historias de Bonnie, Gobs, Armin y la moneda incorporan nuevas referencias dentro de su etapa anterior, sin repetir una partida de la flota después del disparo de Taylor. La explosión marítima enlaza después ambos frentes ([43-001, 43-006–43-007, 43-103 y 43-202](capitulos/43.md)).

La emisión real de Twitch está documentada el 10 de julio de 2026; YouTube publicó el vídeo el 27 de octubre. Esas fechas civiles y el orden de los capítulos no sustituyen el orden ficticio de las acciones simultáneas.

## La defensa de tierra

Molly conduce unos veinte piratas a un embudo con trampas y tiradores. Acepta que Eleanor y Erandy huyan si es necesario, recibe el broche de la caballera y continúa luchando pese a las heridas. La leyenda evocada al entregarlo no se ejecuta como una resurrección. Los pelotones, cañones, perros y oficiales de la Marina representan más combatientes que sus fichas de juego; no se deduce de ellas un censo de bajas ([43-010, 43-014–43-018, 43-020, 43-104–43-106 y 43-216](capitulos/43.md)).

Erandy encadena fuego y rayos durante un trance que vive como entrega al Sol. Eleanor protege a su escudera con el escudo y marca la retaguardia con el estandarte, pero ella no escucha la orden. La interpretación religiosa de la explosión pertenece a Erandy; el espacio de conjuro final se atribuye al chat. Al terminar apenas sigue en pie y su recuperación no se representa ([43-101, 43-105, 43-107, 43-111, 43-113, 43-116, 43-205, 43-210 y 43-218](capitulos/43.md)).

Lunaria es la otra kender, que transporta a Citlali y a Etley como oso. Arroja a la cría, que agita las alas sin volar, y usa un cañón como garrote y propulsor. Eleanor monta al oso, se transforma y añade su energía al impacto de la caída. La protección final de alas espectrales mantiene a Citlali y a la cría al margen de la explosión representada ([43-012, 43-108, 43-112, 43-114, 43-117–43-120, 43-206 y 43-212](capitulos/43.md)).

Los vocativos Bonnie o Erandy que aparecen aisladamente durante acciones continuas no crean otra llegada de Bonnie a la jungla ni cambian a Eleanor por la escudera como jinete. Al final los mandos caen y los marines supervivientes huyen: la victoria no elimina a toda la Marina ([43-119, 43-206, 43-213 y 43-216](capitulos/43.md)).

## Citlali, Nox y Amaru

La primera visión muestra al pirata de espaldas y una batalla vista bajo el agua; la siguiente identifica a Nox cayendo durante la explosión. Citlali afirma que se ha ido y Molly entiende una mirada de pérdida de un hijo. Cuando ve el Zampaolas, lo llama Amaru y recuerda al niño del cofre frente al adulto de trenzas, ron y malos chistes. El capítulo sostiene ese reconocimiento materno, sin reconstruir el rescate o los años de crianza ([43-003, 43-013, 43-203, 43-217 y 43-219](capitulos/43.md)).

P39-002 y P11-001 pasan a parcial: la identificación adquiere una representación narrativa sostenida, pero la historia del cofre y sus años intermedios sigue incompleta. P42-001 también pasa a parcial por el desarrollo de la pérdida de Nox; Pinky y Tórtola no reciben una nueva escena después del estallido. No se inventa una recuperación de cuerpos.

La caja de música acompaña los recuerdos iniciales y el duelo final. Las escenas escritas ya conservan un objeto cuadrado que Nox dejó a Citlali y el hallazgo posterior de una caja; esta revisión no identifica ambos objetos solo por su forma ni convierte la música en la causa probada del dolor. Las fuentes escritas siguen disponibles en sus escenas originales.

## La vida absorbida y los símbolos

El toque de Citlali cierra sus heridas y tensa la piel. Tras el dolor de los tatuajes y la incitación del ser, el drenaje se vuelve violento; ella rejuvenece mientras sus víctimas envejecen. Mata al general y consume al marine que Eleanor retiene. P19-002 pasa a parcial por esta relación funcional observada, conservando lo que falta sobre el origen del poder y el episodio anterior de curación fallida ([43-115, 43-202–43-204, 43-208–43-209 y 43-214–43-215](capitulos/43.md)).

El epílogo muestra al interlocutor serpentino activando un altar de símbolos exactamente iguales a los de Citlali. P39-001 pasa a parcial por ese vínculo concreto; no se identifica al Señor de los yuan-ti ni la función completa de la piel como clave. El altar se cataloga como objeto, sin localización inventada. Tampoco se equiparan el ser con Set, otras visiones o el ojo de Nox, ni las marcas de Citlali con las de él ([43-203–43-204 y 43-220](capitulos/43.md)).

Los personajes no acceden automáticamente al epílogo. El desliz Kuroto en la despedida se corrige en la mesa y no traslada evidencias entre campañas.

## La costa y el rol escrito

Citlali y sus compañeros ven las velas y la bandera del Zampaolas detenerse como varadas en la costa oriental. Su intento de alcanzarlo no llega a un encuentro representado; P42-006 pasa a parcial por la posición posterior del barco, sin un nuevo uso de la moneda por Ione ([43-219](capitulos/43.md)).

La duración conservada del vídeo orienta un corte a las 20:41:48 UTC del 10 de julio, sin certificar la hora real de juego. El único aviso que cruza ese corte contiene exclusivamente menciones de usuarios. Se marca como no narrativo y se conserva con «El Zampaolas amanece después de la batalla», evitando inventar una escena vacía. Sus tres mensajes, textos, fechas, adjunto y hashes originales se conservan; el archivo sigue con 304 escenas y 6.241 mensajes. El [registro del ajuste](../borradores/43/ajuste_rol.json) guarda el estado anterior.

Las 253 preguntas anteriores están cotejadas y se añaden ocho: 261 en total. Las tramas sin novedades conservan su estado. Esta nueva versión permanece en local para revisión, sin publicación autorizada.
'''
    write(ROOT / 'conocimiento/continuidad_43.md', refs(continuity))
    all_chapters = [read_json(p) for p in (ROOT / 'conocimiento/capitulos').glob('*.json')]
    aliases, notes, excluded = load_catalog()
    mentioned = {name for c in all_chapters for f in c['afirmaciones'] for name in canonical_labels(f['entidades'], aliases)}
    visible = [g for name, g in notes.items() if name in mentioned and g.get('tipo') and g.get('visible', True) and name not in excluded]
    counts = {kind: sum(g['tipo'] == kind for g in visible) for kind in ('personaje', 'lugar', 'faccion', 'objeto')}
    total_facts = sum(len(c['afirmaciones']) for c in all_chapters)
    path = ROOT / 'README.md'
    text = path.read_text(encoding='utf-8')
    for old, new in [
        ('sus 42 capítulos revisados, 1115 registros, 161 fichas', f'sus 43 capítulos revisados, {total_facts} registros, {len(visible)} fichas'),
        ('los 42 capítulos, 1115 registros', f'los 43 capítulos, {total_facts} registros'),
        ('Los 94 personajes incluyen', f'Los {counts["personaje"]} personajes incluyen'),
        ('hasta el capítulo 42.', 'hasta el capítulo 43.'),
        ('seguimiento actualizado al capítulo 42.', 'seguimiento actualizado al capítulo 43.'),
        ('Los **42 capítulos**', 'Los **43 capítulos**'),
        ('las 253 preguntas históricas de Xoltacan', 'las 261 preguntas históricas de Xoltacan'),
        ('**sus 42 capítulos: 38 documentadas y 4 asumidas**', '**sus 43 capítulos: 39 documentadas y 4 asumidas**'),
        ('Hay 42 capítulos catalogados, 84 VTT y 84 TXT', 'Hay 43 capítulos catalogados, 86 VTT y 86 TXT'),
        ('01/ … 42/', '01/ … 43/'),
        ('Los 42 capítulos disponibles se han leído completos y cuentan con fichas estructuradas: 1115 registros', f'Los 43 capítulos disponibles se han leído completos y cuentan con fichas estructuradas: {total_facts} registros'),
        ('Los **28 lugares**, las **8 facciones** y los **27 objetos**', f'Los **{counts["lugar"]} lugares**, las **{counts["faccion"]} facciones** y los **{counts["objeto"]} objetos**'),
        ('--capitulo 42 --url "https://www.youtube.com/watch?v=ID_DE_VIDEO"', '--capitulo 44 --url "https://www.youtube.com/watch?v=ID_DE_VIDEO"'),
    ]:
        text = text.replace(old, new)
    marker = '\n\nEl **capítulo 43, Batalla en la Jungla del Garfio**'
    text = text.split(marker)[0].rstrip() + marker + ' (directo del 10/07/2026; publicado en YouTube el 27/10/2026), está incorporado tras leer completos tres bloques sin solapamiento: 62 evidencias, once etapas y seis fichas nuevas. Las 253 preguntas anteriores están cotejadas y se añaden ocho: 261 en total. Se integran los dos frentes simultáneos, el reconocimiento materno de Amaru en Nox y el vínculo de los símbolos de Citlali con el altar, sin inventar los episodios que siguen abiertos. Véanse [la continuidad](conocimiento/continuidad_43.md) y [la procedencia con hashes](config/fuente_xoltacan_43.json). Versión local para revisión, sin publicación autorizada.\n'
    write(path, text)
    print(json.dumps(dict(capitulos=len(all_chapters), evidencias=total_facts, fichas=len(visible), tipos=counts), ensure_ascii=False))


if __name__ == '__main__':
    main()
