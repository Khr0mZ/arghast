"""Actualiza las vistas de continuidad con la integración revisada del capítulo 46."""
from preparar import ROOT, FOLDER, read_json


def write(path, text):
    newline = '\r\n' if path.exists() and b'\r\n' in path.read_bytes() else '\n'
    path.write_bytes(text.replace('\n', newline).encode('utf-8'))


def appendix(filename, title, body):
    path = ROOT / 'campanas/xoltacan/conocimiento' / filename
    marker = '\n\n## ' + title
    text = path.read_text(encoding='utf-8')
    write(path, text.split(marker)[0].rstrip() + marker + '\n\n' + body.strip() + '\n')


def main():
    chapter = read_json(ROOT / 'campanas/xoltacan/conocimiento/capitulos/46.json')
    integration = read_json(FOLDER / 'integracion.json')
    role = read_json(FOLDER / 'cotejo_rol.json')
    facts = chapter['afirmaciones']
    chapter_link = '[capítulo 46](capitulos/46.md)'
    appendix('RELACIONES.md', 'El regreso de Ione, Eleanor y Citlali', f'''
La estampida y el río separan a Ione, Eleanor y Citlali del resto de la comitiva que viaja hacia Iktan. Etley queda con el otro grupo; no se convierte esa separación en un abandono en la ciudad. Las tres liberan a Zoltan de un soporte de madera y lo incorporan al viaje. La sospecha de Eleanor sobre los cadáveres de la cueva no demuestra que él los matara. El combate contra los dos tiranosaurios muestra tanto su ayuda como los riesgos de su electricidad ({chapter_link}).

En Iktan, Ione vuelve a encontrar a sus tripulantes y plantea reunir dinero y combatientes para recuperar Shiaru. La ausencia del novato recordado como Jacki no se confunde con una captura nueva del exmarine Jack ni resuelve la identidad del cautivo mencionado por Taylor. Citlali recoge a Etley en el colegio y discute con Leo; Miausi es la profesora que interviene, sin identificarla automáticamente con la directora del capítulo 45.

El [reencuentro escrito de Eleanor y Erandi](https://discord.com/channels/946724148628041748/1504602363728756846/1529957197948260414) queda después del capítulo 46. Eleanor la abraza y comprueba cómo está; Erandi despierta mareada. El afecto no establece por sí solo parentesco o una relación romántica, y el mareo no aporta un diagnóstico de su trance anterior.
''')
    appendix('ATLAS.md', 'El camino perdido y la aldea de la cascada', f'''
La estampida y el río desorientan a las tres viajeras. Los intentos de elegir rumbo y seguir huellas las llevan de nuevo hacia la costa y después hasta una aldea con lago y cascada. Las monedas utilizadas para orientarse no se identifican como la moneda pirata de Bonnie ni prueban que Ione haya activado su poder ({chapter_link}).

La aldea conserva pieles humanas y una cueva con cuerpos ennegrecidos, además de la choza donde Eleanor encuentra una copa. Se mantienen como lugares de este viaje: no se equiparan a otras aldeas caníbales, al templo de los nawals o a las ruinas de Citlali. Los dos tiranosaurios que combaten allí tampoco se identifican con el ejemplar cañoneado del capítulo 37. Las descargas de Zoltan queman después restos y prenden construcciones, sin demostrar que él causara las muertes anteriores.

Citlali reconoce finalmente el camino y conduce al grupo a Iktan. La taberna y el colegio reúnen de nuevo a los viajeros con sus conocidos. La secuencia improvisada de templos, dioses y otras aventuras que la mesa reconoce como broma no se convierte en una expedición o cartografía de la campaña.
''')
    appendix('FACCIONES.md', 'La tripulación reunida en Iktan', f'''
Los tripulantes que Ione encuentra en la taberna refieren que llevan cuatro días en Iktan. La capitana propone conseguir dinero, reclutar gente y recuperar Shiaru, pero no ejecuta en este capítulo una reconquista ni se establece quién gobierna ahora el puerto. Los nombres de los presentes y la ausencia del novato se conservan con el alcance de sus declaraciones ({chapter_link}).

La aldea de la cascada no se adscribe a los Profundos, los yuan-ti o la tribu de la Hoja Caída. Las pieles y los cadáveres no bastan para reconstruir su organización, autoría de las muertes o relación con los poderes de Zoltan.
''')
    appendix('MISTERIOS.md', 'Zoltan, los cadáveres y la vuelta a Iktan', f'''
El {chapter_link} incorpora a Zoltan con una marca oscura, lagunas sobre su situación y una reacción borrosa al nombre o aspecto de Ione. Sus descargas posteriores son observables; la responsabilidad por los cuerpos ya ennegrecidos permanece sin demostrar. Tampoco se deduce una relación entre su electricidad y la moneda de Bonnie.

La recapitulación aclara parcialmente el reencuentro de Citlali con los demás en la playa: recuerda una discusión y un disparo, sin reconstruir su autor y objetivo exactos. P43-005 pasa a parcial. Las nuevas absorciones vitales de Citlali y el plan de consultar a Walulu amplían la continuidad de P43-004, sin resolver la duración de su rejuvenecimiento ni representar una cura. P43-006 conserva el seguimiento de Erandy con los dos mensajes escritos posteriores, sin dar por terminada su recuperación.

La vuelta de Ione aporta una comitiva y un proyecto para recuperar Shiaru; no recupera a Nox o su cuerpo ni establece el desenlace de Pinky y Tórtola. El novato ausente queda sin identidad histórica confirmada y no se mezcla con el Jackie citado por Taylor. Las preguntas nuevas y el cotejo de las 276 anteriores figuran en [Seguimiento](SEGUIMIENTO.md).
''')
    path = ROOT / 'campanas/xoltacan/conocimiento/MISTERIOS.md'
    write(path, path.read_text(encoding='utf-8').replace('estado al cierre del capítulo 45', 'estado al cierre del capítulo 46'))
    path = ROOT / 'campanas/xoltacan/conocimiento/TRAMAS.md'
    text = path.read_text(encoding='utf-8')
    if '[Continuidad del capítulo 46]' not in text:
        text = text.replace('- [Continuidad del capítulo 45](continuidad_45.md).', '- [Continuidad del capítulo 45](continuidad_45.md).\n- [Continuidad del capítulo 46](continuidad_46.md).')
    write(path, text)
    appendix('METODO.md', 'Incorporación del capítulo 46', f'''
«Camino perdido a Iktan» se incorpora tras leer completos los 3.437 segmentos en tres bloques sin solapamiento. El [reparto](../revision/borradores/46/reparto.json), las tres entregas y la [integración](../revision/borradores/46/integracion.json) conservan su cobertura. La [procedencia](../revision/fuente_xoltacan_46.json) registra los dos VTT, sus TXT derivados y los metadatos originales con cinco hashes. No se ha cotejado el audio.

El capítulo reúne {len(facts)} evidencias y {integration['etapas']} etapas narrativas. Se cotejan las 276 preguntas anteriores y se añaden {len(chapter['preguntas'])}. Las bromas de la mesa, las hipótesis sobre las muertes y los objetos sin identificación no se convierten en hechos confirmados.

Se leen completos los dos mensajes de la escena de Eleanor y Erandi. El [cotejo del rol](../revision/borradores/46/cotejo_rol.json) comprueba todas las escenas contra el nuevo corte estimado: 23 de julio a las 20:50:37 UTC, calculado desde la tarjeta de Twitch y los 8.661 segundos del vídeo. Solo cambia de intervalo ese reencuentro, que queda entre los capítulos 46 y 47. Ninguna escena necesita dividirse y se conservan los originales de las 325 escenas y sus 6.723 mensajes. La publicación de YouTube corresponde al 8 de noviembre de 2026.
''')
    write(ROOT / 'campanas/xoltacan/conocimiento/continuidad_46.md', f'''# Continuidad del capítulo 46

«Camino perdido a Iktan» se ha leído íntegro: 3.437 segmentos, desde 00:00:00.000 hasta 02:24:20.520, en tres bloques sin solapamiento. Contiene {len(facts)} evidencias y {integration['etapas']} etapas. Se conservan el [reparto](../revision/borradores/46/reparto.json), las entregas, la [integración](../revision/borradores/46/integracion.json) y la [procedencia](../revision/fuente_xoltacan_46.json). El audio no está cotejado.

## Identidades, lugares y causalidad

Zoltan queda incorporado por presentación, con esa grafía. Su reacción al nombre de Ione y a su gorro no explica el cartel que recuerda ni demuestra una relación anterior concreta. Las descargas del combate y del intento de extraer un diente no prueban que matara a los habitantes antes de ser rescatado.

La aldea caníbal de la cascada y su cueva no se fusionan con asentamientos anteriores. La copa de Eleanor y el collar que Ione vende a Froger son botín de esta aldea; no son objetos de otros altares o collares mágicos ya catalogados. Los dos tiranosaurios quedan separados del ejemplar del capítulo 37. Las monedas usadas para elegir camino no se identifican como la moneda de Bonnie.

Etley queda con la otra comitiva al separarse el grupo y vuelve a aparecer en el colegio de Iktan. Miausi es la profesora de la escena, sin equipararla solo por el aspecto felino con la directora anterior. Angelique conserva la continuidad editorial del cortejo de Coyote y la taberna, con grafía provisional. El novato ausente llamado Jacki sigue sin identificarse con el exmarine Jack o con el cautivo referido por Taylor.

## Preguntas anteriores y desenlaces

Las recapitulaciones permiten avanzar P43-005 a parcial por la reunión en la playa, sin atribuir el disparo. Citlali vuelve a absorber vida y se cura, pero las reglas, edad final y duración del rejuvenecimiento continúan pendientes en P43-004. Se propone buscar ayuda de Walulu; no se representa todavía esa consulta o una cura. Ione quiere recuperar Shiaru sin haber ejecutado el plan o localizado a Nox.

El reencuentro de Eleanor y Erandy amplía P43-006 mediante [sus fuentes escritas completas](https://discord.com/channels/946724148628041748/1504602363728756846/1529957197948260414). La escudera está viva y despierta mareada; no recibe un diagnóstico o una recuperación completa. Los recuerdos mentales de Nox no equivalen a una aparición o resurrección suya. El montaje que la mesa reconoce como improvisación humorística tampoco incorpora aventuras, templos o dioses nuevos como hechos de campaña.

Se cotejan las 276 preguntas anteriores y se incorporan {len(chapter['preguntas'])} nuevas. Las respuestas y sus evidencias están en el [seguimiento](SEGUIMIENTO.md) y la ficha del [capítulo 46](capitulos/46.md).

## Rol escrito y fuentes conservadas

El directo está documentado el 23 de julio de 2026 a través del anuncio 1529917702439698493. El vídeo fue publicado en YouTube el 8 de noviembre. La suma de su duración a la hora de referencia de Twitch orienta el final a las 20:50:37 UTC; no certifica la hora real de juego.

La escena de Eleanor y Erandi, escrita desde las 21:03:41 UTC, pasa del intervalo 45–46 al 46–47. Es el único cambio de posición. Ninguna escena atraviesa el corte nuevo: las 325 escenas, los 6.723 mensajes y todos los originales permanecen completos. El [cotejo](../revision/borradores/46/cotejo_rol.json) conserva los dos identificadores leídos y el hash de la escena. Los datos de Kuroto permanecen separados e intactos.

La versión se verifica en local antes de solicitar la aprobación de publicación.
''')
    total_facts = sum(len(read_json(p)['afirmaciones']) for p in (ROOT / 'campanas/xoltacan/conocimiento/capitulos').glob('*.json'))
    visible = sum(g.get('visible', True) for g in read_json(ROOT / 'campanas/xoltacan/config/entidades.json')['grupos'])
    path = ROOT / 'README.md'
    text = path.read_text(encoding='utf-8')
    replacements = {'45 capítulos': '46 capítulos', '1311 registros': f'{total_facts} registros',
        '192 fichas de entidades': f'{visible} fichas de entidades', '90 VTT y 90 TXT': '92 VTT y 92 TXT',
        'al capítulo 45': 'al capítulo 46', '01/ … 45/': '01/ … 46/', '--capitulo 46 --url': '--capitulo 47 --url',
        '46 capítulos: 41 documentadas y 4 asumidas': '46 capítulos: 42 documentadas y 4 asumidas'}
    for before, after in replacements.items():
        text = text.replace(before, after)
    write(path, text)
    print('Vistas y continuidad actualizadas; las misiones se generan desde la ficha del capítulo.')


if __name__ == '__main__':
    main()
