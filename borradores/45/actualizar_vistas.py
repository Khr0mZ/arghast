"""Actualiza continuidad y procedencia antes de la construcción final del capítulo 45."""
import re
from preparar import ROOT, FOLDER, read_json

MAPPING = read_json(FOLDER / 'integracion.json')['mapa_referencias']


def refs(text):
    return re.sub(r'\b45-\d{3}\b',lambda m:MAPPING[m[0]],text)


def write(path,text):
    newline = '\r\n' if path.exists() and b'\r\n' in path.read_bytes() else '\n'
    path.write_bytes(text.replace('\n',newline).encode('utf-8'))


def appendix(filename,title,body):
    path = ROOT / 'conocimiento' / filename
    marker = '\n\n## ' + title
    text = path.read_text(encoding='utf-8')
    write(path,text.split(marker)[0].rstrip()+marker+'\n\n'+refs(body).strip()+'\n')


def main():
    appendix('RELACIONES.md','El rescate y la audiencia del capítulo 45','''
Naór, Tortas, Coyote, Triel, Tentacol y Chopito comparten la expedición. El temor de Naór al agua no desaparece por recibir respiración acuática; se apoya en Tortas y más tarde lo impulsa para huir de los tiburones. Las pretensiones de Chopito no hacen que Tortas acepte su culto ni que los oficiantes lo reconozcan ([45-005–45-006, 45-016–45-019, 45-025–45-027, 45-121](capitulos/45.md)).

Coyote vuelve a contactar con Maris y ayuda a una cautiva herida, que no es la sirena con quien mantiene el contacto. Maris se identifica como hija de Ivet y consigue la audiencia para Naór. Las bromas sobre la suegra no formalizan un matrimonio. Ivet y la princesa presentan posiciones distintas sobre las promesas del padre de Naór, sin lograr todavía una alianza ([45-012–45-015, 45-217, 45-222–45-226](capitulos/45.md)).

El cuidado de Leo continúa fuera del vídeo: una escena escrita muestra su [espera bajo la lluvia](https://discord.com/channels/946724148628041748/1482149664131383316/1527444416187596951) y otra la [llegada de Tessa](https://discord.com/channels/946724148628041748/1482149664131383316/1527455379028574428), que se presenta como Tesara, amiga de Naór. No se identifica a la chica autorizada del diálogo escolar solo por el color del pelo.
''')
    appendix('ATLAS.md','Del lago Tachan al escondite y Perlasal','''
El director sitúa Iktan junto al lago de nombre provisional Tachan. Una guía sirénida conduce al grupo por una gruta lateral cuyas corrientes llegan al mar. Las ruinas del ataque al escuadrón ofrecen coral roto, cortes y un rastro de magia residual de armas hacia el norte. No son todavía Perlasal ni el escondite del altar ([45-002, 45-019–45-023](capitulos/45.md)).

Un muro submarino oculta el túnel al refugio. Dentro hay una cámara de aire, tierra y zonas inundadas; la oscuridad se salva con la guía de Chopito y las luces de Triel. Más allá de los primeros defensores, un islote contiene la cautiva y el altar. La detección posterior muestra magia intensa en el altar y el agua, sin desactivación o identificación del consagrante ([45-101–45-104, 45-117–45-120, 45-220–45-221](capitulos/45.md)).

El grupo sale con la rescatada, vuelve a reunirse con la guía y entra en Perlasal. Maris los lleva al templo donde Ivet oficia y recibe a Naór. Ese templo y su altar son distintos del islote de los Profundos y del altar de los símbolos de Citlali ([45-222–45-227](capitulos/45.md)).
''')
    appendix('FACCIONES.md','Los Profundos y la invitación a Perlasal','''
Maris informa de nuevos secuestros y del cierre de Perlasal. La investigación localiza defensores y un rito con una sirena atada. Los interlocutores reclaman sacrificios y algo que poseen las sirenas para resucitar a su dios. No lo identifican con Chopito o el kraken. Se rescata a una cautiva y se vence a los presentes, pero el sacerdote muere sin interrogatorio y la instalación conserva magia ([45-013, 45-020, 45-118–45-121, 45-206, 45-217–45-222](capitulos/45.md)).

Naór obtiene una audiencia con Ivet, que es madre de Maris, y la convoca a Tutucan. La oficiante recuerda una antigua promesa de unión incumplida; Naór defiende a Atlan. Ivet solo promete meditarlo y no confirma asistencia o tropas. Sus advertencias sobre los yuan-ti no hacen que estos y los Profundos sean la misma organización ([45-223–45-226](capitulos/45.md)).

El [debate escrito posterior](https://discord.com/channels/946724148628041748/1482149664131383316/1527449224642433127) añade el relato de Naór sobre reliquias, la Llave del Sol y la Cámara de los Clanes Elementales. Sigue siendo su explicación de la convocatoria; no representa la reunión, la unión de los objetos o una guerra decidida por todos.
''')
    path = ROOT / 'conocimiento/MISTERIOS.md'
    text = path.read_text(encoding='utf-8').replace('estado al cierre del capítulo 44','estado al cierre del capítulo 45')
    replacements = {
        '| Maris, perla y concha': refs('| Maris, perla y concha — visita y rescate; red abierta | La perla vuelve a contactar con Maris. El grupo inspecciona unas ruinas y un escondite, libera a una cautiva y llega a Perlasal. Oye reclamar sacrificios para resucitar a un dios y detecta magia en altar y agua. | [24-012–24-015](capitulos/24.md), [29-019–29-025](capitulos/29.md), [45-012–45-025, 45-118–45-121 y 45-217–45-222](capitulos/45.md) | No se identifica el dios, se localiza el kraken o se determina el destino de todos los desaparecidos. El altar no se desactiva y la concha rota no se repara. |'),
        '| Concilio de Tutucan': refs('| Concilio de Tutucan — nueva audiencia; Perlasal sin decidir | Tras los contactos anteriores, Naór convoca a Ivet. La oficiante recuerda una promesa de unión del padre de la princesa y solo dice que meditará asistir. El rol posterior recoge la explicación de Naór sobre las reliquias y la Llave del Sol. | [31-019 y 31-027](capitulos/31.md), [45-223–45-226](capitulos/45.md), [explicación escrita](https://discord.com/channels/946724148628041748/1482149664131383316/1527449224642433127) | No se celebra el concilio, se confirma la asistencia de Ivet o se abre la Cámara de los Clanes Elementales. La amenaza de guerra expresada por Naór no es una decisión común. |'),
    }
    lines = text.splitlines()
    for i,line in enumerate(lines):
        for beginning,replacement in replacements.items():
            if line.startswith(beginning):lines[i]=replacement
    write(path,'\n'.join(lines)+'\n')
    appendix('MISTERIOS.md','Las preguntas del escondite','''
La visita submarina de Naór y su medio de respiración se cumplen: P41-010 queda resuelta. P29-001 pasa a parcial por la instalación inspeccionada y el rescate, sin resolver toda la red, el kraken o el dios. La duración y condiciones de los besos sirénidos y la religión de Ivet siguen sin explicación suficiente ([45-016–45-019, 45-118–45-121, 45-217–45-227](capitulos/45.md)).

Las nueve preguntas nuevas conservan los destinos del escuadrón, el dios y sus requisitos, la magia del altar, la red restante, la decisión de Ivet, el pacto antiguo, la perla, la recuperación de la cautiva y el destello de Tortas. La monta del hipocampo y la recogida de Leo ya están documentadas en el rol posterior y no se fabrican misterios sobre si llegan a ocurrir. Véanse [el capítulo 45](capitulos/45.md), el [seguimiento individual](SEGUIMIENTO.md) y el [cotejo de continuidad](continuidad_45.md).
''')
    path = ROOT / 'conocimiento/TRAMAS.md'
    text = path.read_text(encoding='utf-8')
    if '[Continuidad del capítulo 45]' not in text:
        text = text.replace('- [Continuidad del capítulo 44](continuidad_44.md).','- [Continuidad del capítulo 44](continuidad_44.md).\n- [Continuidad del capítulo 45](continuidad_45.md).')
    write(path,text)
    appendix('METODO.md','Incorporación del capítulo 45','''
«El escondite de los Profundos» se incorpora después de leer completos los 4.311 segmentos en tres bloques sin solapamiento. El [reparto](../borradores/45/reparto.json), las tres entregas y la [integración](../borradores/45/integracion.json) conservan su cobertura. La [procedencia](../config/fuente_xoltacan_45.json) registra las dos variantes VTT, sus TXT y el metadato original con cinco hashes. No se ha cotejado el audio.

Se releen además cuatro escenas escritas completas, con 45 mensajes, para separar el monólogo previo de Tortas de los desenlaces posteriores: el concilio y la Llave del Sol, la monta del hipocampo y el cuidado de Leo. El [cotejo](../borradores/45/cotejo_rol.json) conserva identificadores y hashes sin alterar los originales. El directo está documentado el 16 de julio de 2026 y YouTube publicó el vídeo el 3 de noviembre.
''')
    write(ROOT / 'conocimiento/continuidad_45.md',refs('''# Continuidad del capítulo 45

«El escondite de los Profundos» se ha leído íntegro: 4.311 segmentos en tres bloques sin solapamiento, desde 00:00:00.640 hasta 03:16:30.680. Contiene 78 evidencias, quince etapas, diecinueve entidades nuevas y nueve preguntas nuevas. Se conservan el [reparto](../borradores/45/reparto.json), las [tres entregas y su integración](../borradores/45/integracion.json) y la [procedencia con cinco hashes](../config/fuente_xoltacan_45.json). El audio no se ha cotejado.

## La visita de Naór y el rescate

P41-010 se resuelve con el medio de respirar y la llegada efectiva al templo de Perlasal. La burbuja de una hora de Walulu solo se propone; la respiración procede de los besos de la guía enviada por Maris. P29-002 conserva abiertas duración y condiciones generales, sin cambiar de estado solo por añadir otro caso ([45-008–45-019, 45-222–45-224](capitulos/45.md)).

La guía corrige su primera versión de única superviviente: vio caer a dos y huyó cuando aún quedaban otros. Alfira, Zamuria, Jariora y María Antonieta son grafías provisionales de los nombres que da. La cautiva rescatada no se identifica con una de esas personas, ni se confunde con Maris o la guía. Las tres sombras no son desaparecidos reconocidos ([45-020, 45-024–45-025, 45-104, 45-217, 45-222–45-223](capitulos/45.md)).

## Un rito sin deidad identificada

Las ruinas del ataque, el refugio y Perlasal permanecen separados. El escondite tiene una cámara de aire y zonas inundadas. La discusión se corrige de Auran a Aquan. Los enemigos reclaman más sacrificios y algo que las sirenas tienen para resucitar a su dios, sin nombre o eficacia demostrados ([45-019–45-023, 45-101–45-102, 45-117–45-121](capitulos/45.md)).

El sacerdote, el hechicero acuático y la criatura que grita no son una persona. El segundo grito se retira antes de ejecutarse. El sacerdote queda inconsciente a petición de Tentacol, pero Chopito lo mata después y no se obtiene una confesión. Sus proclamas, el humo y la sombra son parte de la escena, sin probar divinidad. Las leyendas del kraken tampoco identifican a Chopito o al dios del rito ([45-204–45-218, 45-221](capitulos/45.md)).

P29-001 pasa a parcial: se inspecciona una instalación y se libera a una cautiva, pero quedan la organización, los otros desaparecidos y el kraken. El altar y el agua conservan magia; nadie los desactiva. El altar no es el del templo de Ivet ni el de los símbolos de Citlali. La mano y el fragmento facial de Tortas proceden de cuerpos diferentes; la perla de Tentacol no es la de comunicación ([45-116, 45-216–45-222, 45-224](capitulos/45.md)).

## Ivet, Maris y la convocatoria

Maris se identifica como hija de Ivet y facilita la audiencia. Ivet permite hablar a la princesa y que permanezcan, sin mostrar confianza plena o nombrar su deidad; P29-003 sigue pendiente. Recuerda una promesa del padre de Naór y la princesa defiende la ayuda de Atlan. La respuesta al concilio es meditarlo y de momento poco favorable: no hay aceptación, envío de tropas o alianza firmada ([45-223–45-227](capitulos/45.md)).

Las preguntas P16-004, P17-003 y P22-004 incorporan esta invitación sin cerrar la reunión. El rol escrito posterior añade el [relato de la tregua](https://discord.com/channels/946724148628041748/1482149664131383316/1527443109590466710) y la [explicación de Naór sobre la Llave del Sol](https://discord.com/channels/946724148628041748/1482149664131383316/1527449224642433127). Coyote y Tortas proponen resolver los problemas de Perlasal; la amenaza de guerra de Naór no significa que los demás la acuerden.

## Desenlaces escritos y fuentes preservadas

Se han releído completas cuatro escenas, con 45 mensajes, registradas en el [cotejo de rol](../borradores/45/cotejo_rol.json). El monólogo de Tortas precede al viaje. Después del vídeo, Triel [monta el hipocampo](https://discord.com/channels/946724148628041748/1482149664131383316/1527442489018159298) y Naór acaba bajándola. El vídeo solo representa su pregunta. Leo [espera bajo la lluvia](https://discord.com/channels/946724148628041748/1482149664131383316/1527444416187596951) y [Tessa lo recoge](https://discord.com/channels/946724148628041748/1482149664131383316/1527455379028574428) tras un aviso tardío. Ese resultado no demuestra que la chica autorizada por Naór pueda identificarse solo por el pelo.

P21-004 recoge esos cuidados y mantiene abierta la custodia formal. P40-005 conserva las cifras de edad incompatibles: el destello no las explica y el rol añade una afirmación de unos setecientos años. No se convierten el año ficticio 1496 o las 10:43 en fechas de emisión.

El directo está documentado el 16 de julio de 2026 y la publicación de YouTube el 3 de noviembre. Sus 11.791 segundos orientan un corte a las 21:18:51 UTC, sin certificar la hora real de juego. Ninguna escena cruza el nuevo corte; se conservan 325 escenas y 6.723 mensajes de Xoltacan, incluidos los añadidos anteriores de Oghma y Jivirix. Los originales y datos de Kuroto se mantienen intactos. Se cotejan las 267 preguntas anteriores y se añaden nueve: 276 en total, sin revisiones pendientes de actualizar. Esta versión permanece en local para revisión y no se publica sin aprobación expresa.
'''))
    path = ROOT / 'README.md'
    text = path.read_text(encoding='utf-8')
    changes = {'44 capítulos':'45 capítulos','1233 registros':'1311 registros','173 fichas de entidades':'192 fichas de entidades',
        '88 VTT y 88 TXT':'90 VTT y 90 TXT','al capítulo 44':'al capítulo 45','01/ … 44/':'01/ … 45/',
        '--capitulo 45 --url':'--capitulo 46 --url','45 capítulos: 40 documentadas y 4 asumidas':'45 capítulos: 41 documentadas y 4 asumidas'}
    for old,new in changes.items():text=text.replace(old,new)
    write(path,text)
    print('Vistas actualizadas; Misiones, Preguntas y notas se regeneran exclusivamente desde la ficha.')


if __name__ == '__main__':
    main()
