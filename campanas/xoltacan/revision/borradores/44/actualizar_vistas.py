"""Actualiza las vistas editoriales antes de reconstruir los documentos generados."""
import re
from preparar import ROOT, FOLDER, read_json

MAPPING = read_json(FOLDER / 'integracion.json')['mapa_referencias']


def refs(text):
    return re.sub(r'\b44-\d{3}\b', lambda m:MAPPING[m[0]], text)


def write(path, text):
    newline = '\r\n' if path.exists() and b'\r\n' in path.read_bytes() else '\n'
    path.write_bytes(text.replace('\n', newline).encode('utf-8'))


def appendix(filename, title, body):
    path = ROOT / 'campanas/xoltacan/conocimiento' / filename
    text = path.read_text(encoding='utf-8')
    marker = '\n\n## ' + title
    write(path, text.split(marker)[0].rstrip() + marker + '\n\n' + refs(body).strip() + '\n')


def main():
    appendix('RELACIONES.md', 'La búsqueda del antídoto de Eromov', '''
Leona, Guayacán, Ayoto y Tlachka se reúnen en Cuicapalli y cooperan en la búsqueda encargada por Parroter. Guayacán sigue llamando maestra a Leona y su angustia al verla dentro del moho afecta a sus acciones. Ayoto la saca de la masa ocupando su lugar; ante el devorafango, Guayacán lo inmoviliza y Tlachka abre sus mandíbulas para extraerla con las espinas ([44-001–44-013, 44-104, 44-109, 44-201–44-205](capitulos/44.md)).

El recuerdo de Eromov encontrando a Leona de pequeña impulsa a la harengon a arrancar la primera espina. Es un vínculo personal representado, sin una filiación biológica, adopción formal o sucesión política confirmadas ([44-117](capitulos/44.md)).

Parroter recibe el ingrediente obtenido en vida y administra el remedio, con una mejoría visible de Eromov. El herrero rechaza confiar su tienda a Baton y lo acusa de ladrón; Baton lo niega, sin que se pruebe el robo. Al terminar, Guayacán y Ayoto se apoyan para llevar el exoesqueleto hacia la tienda ([44-208, 44-210, 44-215–44-216](capitulos/44.md)).
''')
    appendix('ATLAS.md', 'La cueva del lago cercano a Cuicapalli', '''
Leona orienta la búsqueda del devorafango hacia una cueva húmeda junto a un lago donde jugaba de pequeña. El lugar recibe una etiqueta descriptiva, sin topónimo propio. No se identifica con la Hoja Caída, la cueva derrumbada de Citlali o la guarida del dragón ([44-013, 44-016–44-018](capitulos/44.md)).

La masa de moho consume huesos aparentemente humanoides y carece de boca definida. El devorafango llega después y llena de ácido la sala: ambos rivales tienen historias separadas. El grupo vuelve a Cuicapalli con las espinas y el cadáver del segundo, sin identificar a las víctimas de los huesos o comprobar el destino final del moho ([44-102–44-103, 44-109–44-112, 44-205–44-208](capitulos/44.md)).
''')
    appendix('FACCIONES.md', 'Cuicapalli durante el capítulo 44', '''
Leona y Guayacán mantienen la vigilancia mientras Eromov sigue enfermo. La escena escrita previa ya muestra a Leona entregando [viales y recetas de Iktan](https://discord.com/channels/946724148628041748/1482149664131383316/1525820723434618981) y a [Parroter empezando a trabajar](https://discord.com/channels/946724148628041748/1482149664131383316/1525825232810541056). La expedición por las espinas y el remedio del capítulo 44 amplían ese avance. Los expertos siguen esperados; tampoco se inviste a Leona como dirigente ([44-001, 44-003–44-004, 44-007–44-013, 44-208, 44-216](capitulos/44.md)).

Las alusiones a serpientes y materiales recibidos no identifican al autor que contaminó la comida de Eromov. Tampoco equiparan el ácido del devorafango, los pinchazos de sus espinas o el moho de la cueva con el veneno y los no muertos de otras expediciones ([44-009–44-011, 44-102, 44-111, 44-114](capitulos/44.md)).
''')
    path = ROOT / 'campanas/xoltacan/conocimiento/MISTERIOS.md'
    text = path.read_text(encoding='utf-8').replace('estado al cierre del capítulo 43', 'estado al cierre del capítulo 44')
    replacement = refs('| Eromov y Hoja Caída — remedio administrado; recuperación incompleta | Leona ya entregó viales y recetas de Iktan en el rol escrito. Parroter recibe después las espinas del devorafango vivo y administra el remedio; las venas negras menguan. | [Entrega escrita](https://discord.com/channels/946724148628041748/1482149664131383316/1525820723434618981), [44-008–44-013, 44-117, 44-205, 44-208 y 44-216](capitulos/44.md) | Faltan la recuperación completa y la llegada de los expertos. No se identifica al autor material del envenenamiento ni se demuestra la equivalencia de las distintas muestras. |')
    lines = [replacement if line.startswith('| Eromov y Hoja Caída') else line for line in text.splitlines()]
    write(path, '\n'.join(lines) + '\n')
    appendix('MISTERIOS.md', 'Las consecuencias del remedio y de la expedición', '''
La primera dosis muestra una mejoría de Eromov, no el final de la enfermedad. La historia de cómo encontró a Leona de pequeña aparece en un recuerdo sin quedar reconstruida. Los huesos del moho, el destino de la masa, las posibles consecuencias de comer la carne y la recuperación de los heridos siguen sin resolverse ([44-102, 44-110–44-111, 44-117, 44-208, 44-213–44-216](capitulos/44.md)).

Guayacán recupera exoesqueleto para Ayoto, pero todavía no hay un escudo fabricado. Las seis preguntas nuevas y el cotejo de las 261 anteriores están en [el capítulo 44](capitulos/44.md) y el [seguimiento individual](SEGUIMIENTO.md). La apertura de la boca y la salida de Leona sí se resuelven en esta sesión ([44-203, 44-205, 44-210, 44-212, 44-215](capitulos/44.md)).
''')
    path = ROOT / 'campanas/xoltacan/conocimiento/TRAMAS.md'
    text = path.read_text(encoding='utf-8')
    if '[Continuidad del capítulo 44]' not in text:
        text = text.replace('- [Continuidad del capítulo 43](continuidad_43.md).', '- [Continuidad del capítulo 43](continuidad_43.md).\n- [Continuidad del capítulo 44](continuidad_44.md).')
    write(path, text)
    appendix('METODO.md', 'Incorporación del capítulo 44', '''
«Una cura para Eromov» se incorpora después de leer completos los 2.516 segmentos en tres bloques sin solapamiento. El [reparto](../revision/borradores/44/reparto.json), las tres entregas y la [integración](../revision/borradores/44/integracion.json) conservan la cobertura. La [procedencia](../revision/fuente_xoltacan_44.json) registra las dos variantes VTT, sus dos representaciones TXT y el metadato original con sus cinco hashes. El audio no se ha cotejado.

El directo está documentado el 15 de julio de 2026 mediante el anuncio conservado; YouTube publicó el vídeo el 1 de noviembre. La duración de 6.934 segundos orienta la colocación del rol escrito, sin certificar el comienzo o el final reales de la partida. Las fuentes e identidades de Kuroto permanecen separadas.
''')
    continuity = refs('''# Continuidad del capítulo 44

«Una cura para Eromov» se ha leído completo: 2.516 segmentos repartidos sin solapamiento en tres bloques, desde 00:00:00.000 hasta 01:55:35.760. La revisión contiene 56 evidencias, once etapas narrativas, seis entidades nuevas y seis preguntas nuevas. El [reparto](../revision/borradores/44/reparto.json), la [integración](../revision/borradores/44/integracion.json) y la [procedencia con hashes](../revision/fuente_xoltacan_44.json) permiten comprobar la cobertura. El audio no se ha cotejado.

## El remedio de Eromov

La enfermedad sigue visible al inicio. Parroter ha avanzado con los materiales recibidos, pero no identifica todas sus procedencias. Pide espinas bucales del devorafango, extraídas mientras viva. Leona reúne al grupo y consigue dos: Parroter tritura una y administra la preparación. Las venas negras menguan y el alquimista anuncia más remedio. P30-001 pasa a parcial, sin dar por terminada la recuperación o la supervivencia posterior ([44-008–44-013, 44-117, 44-202, 44-205, 44-208, 44-216](capitulos/44.md)).

P40-006 continúa parcial con el cotejo del rol previo. Se ha releído completa la escena «Guayacán vigila y Leona vuelve con ayuda de Iktan», con sus 36 mensajes: Leona [entrega viales y recetas](https://discord.com/channels/946724148628041748/1482149664131383316/1525820723434618981) y [Parroter empieza a trabajar](https://discord.com/channels/946724148628041748/1482149664131383316/1525825232810541056). La llegada de los expertos queda anunciada. El vídeo añade la administración y la mejoría sin identificar toda la composición o dar por concluida la recuperación. La [trazabilidad del cotejo](../revision/borradores/44/cotejo_rol.json) conserva el hash de la escena y los identificadores leídos.

P41-006 mantiene abiertas la composición y equivalencia de las muestras: los viales traídos por Leona no se equiparan con los recuperados por Winscore de los atacantes del norte. P30-002 no recibe una identificación del autor material del envenenamiento. Las comidas de Tacha no se convierten en una confesión ([44-004, 44-009, 44-208, 44-216](capitulos/44.md)).

## Dos criaturas y dos rescates

La cueva del lago se conoce por un recuerdo infantil de Leona, sin identificarse con la Hoja Caída, el refugio de Citlali o una guarida del dragón. El moho carece de boca, consume huesos aparentemente humanoides y queda moribundo. El devorafango llega después, con ácido, espinas y exoesqueleto. No son dos nombres del mismo enemigo ([44-013, 44-018, 44-102, 44-110–44-112](capitulos/44.md)).

Ayoto saca a Leona del moho intercambiando posiciones. Ella entra después en la boca del devorafango. Guayacán aclara que intenta sujetar el cuello para facilitar el trabajo, frente a la primera interpretación de cerrar la boca. Tlachka abre las mandíbulas y la extrae con dos espinas: no queda una salida sin resolver. La muerte del animal es posterior a la extracción en vida ([44-109, 44-112, 44-117, 44-201–44-208](capitulos/44.md)).

El ácido, las heridas de las espinas y la ceguera por barro se conservan como efectos distintos. El director niega que los pinchazos dorsales envenenen a Ayoto. Leona resiste el picante, sin demostrar que la carne sea inocua; el aviso de Parroter tampoco demuestra una intoxicación ya sufrida ([44-111, 44-114, 44-204, 44-208, 44-213–44-214](capitulos/44.md)).

## Identidades y proyectos

Tlachka se mantiene separado de Tacha. Leona es la harengon, no Naór. El recuerdo de Eromov encontrándola de pequeña documenta un vínculo sin fijar adopción o filiación. La voz cambiante y el pico del traje de Guayacán amplían sus gestos sin resolver P22-003 o P27-002. Tlachka participa de nuevo en Cuicapalli sin un indulto explícito para P27-003 ([44-002, 44-005, 44-117, 44-203, 44-206, 44-213](capitulos/44.md)).

Guayacán extrae piezas imperfectas del exoesqueleto para Ayoto. El herrero del norte exige recibir el material en su tienda y no confía su vigilancia a Baton; su acusación de robo queda contestada. No se fija un nombre propio o especie del artesano ni se lo fusiona con Armin o el herrero tabaxi de un episodio anterior. El nuevo escudo sigue como proyecto, sin encargo aceptado, precio o pieza terminada ([44-209–44-210, 44-212, 44-215](capitulos/44.md)).

## Cobertura y rol escrito

El directo está documentado el 15 de julio de 2026 y la publicación de YouTube el 1 de noviembre. La duración del vídeo orienta los cortes operativos del rol escrito, que conserva 304 escenas y 6.241 mensajes en Xoltacan. No se modifican mensajes, adjuntos o fuentes de Kuroto. Las 261 preguntas anteriores se cotejan con las nuevas evidencias; se añaden seis para un total de 267. Esta versión se prepara en local para revisión, sin publicación autorizada.
''')
    write(ROOT / 'campanas/xoltacan/conocimiento/continuidad_44.md', continuity)
    path = ROOT / 'README.md'
    text = path.read_text(encoding='utf-8')
    replacements = {'43 capítulos':'44 capítulos','1177 registros':'1233 registros','167 fichas de entidades':'173 fichas de entidades',
        '86 VTT y 86 TXT':'88 VTT y 88 TXT','Los 43 capítulos':'Los 44 capítulos','al capítulo 43':'al capítulo 44',
        '01/ … 43/':'01/ … 44/', '--capitulo 44 --url':'--capitulo 45 --url',
        '44 capítulos: 39 documentadas y 4 asumidas':'44 capítulos: 40 documentadas y 4 asumidas'}
    for before, after in replacements.items():
        text = text.replace(before, after)
    write(path, text)
    print('Vistas de consulta y procedencia actualizadas; Misiones queda exclusivamente a cargo del constructor.')


if __name__ == '__main__':
    main()
