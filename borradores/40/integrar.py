"""Integra la revisión editorial del capítulo 40, leída en tres bloques completos.

Los textos son decisiones editoriales; este archivo no resume transcripciones.
Ejecutar desde la raíz antes de redactar.py y construir.py.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import read_json, write_json, write

blocks = [read_json(ROOT / f'borradores/40/bloque_{i}.json') for i in (1, 2, 3)]
records = [row for block in blocks for row in block['registros']]
assert len(records) == 42

paragraphs = [
    'Ilikar recuerda su revancha con la capitana y los entrenamientos en la playa de Shiaru. Tras hablar con Erandy, busca en la selva un trofeo para la maestra mencionada en esa conversación. Eldrat cuenta que su hermana Triel regresó envenenada por el dragón verde y que la cuidó por miedo a perderla; también entrenó con Coyote y Tesara. Leona explica que Eromov sigue envenenado y la envió a Iktan para advertir de un posible ataque de hombres serpiente durante el festival. Guayacán, su aprendiz, queda cuidando al dirigente. En la jungla, Ilikar ayuda a Cipo a sacar un fragmento de espada de debajo de una roca. Leona los encuentra y los guía a Iktan. Las frutas alteran sus cuerpos: la sombra de Leona se desprende, Ilikar se vuelve translúcido y Eldrat brilla de verde. El elfo pisa a Cipo, recibe un mordisco en el calzado y lo aleja de una patada que el goliat no ve. Ilikar se presenta ante Eldrat y Leona mediante su saludo de apretón y palmadas.',
    'Walulu recibe en el templo la advertencia de Leona, agradece que la avisen y promete informar a los guardias y enviar hombres con recetas y protecciones a Cuicapalli. No se muestra el envío ni la cura de Eromov. Dice a Eldrat que Triel ha salido al espectáculo para despejarse. Mientras Ilikar busca a Cipo, Eldrat encubre la patada diciendo que al elemental le salieron alas. El goliat y un guardia buscan un supuesto dragón de fuego y llegan a confundirlo con el sol. Un vecino explica que el festival celebra los movimientos infrecuentes del Gran Anciano, una tortuga pétrea cubierta de plantas a la que consideran protectora de Iktan y augurio de buenas cosechas. Eldrat impide que Triel trepe hasta ella. Durante la ceremonia, la tortuga gira lentamente la cabeza, una piedra lanzada por Triel se rompe antes de alcanzarla y Walulu le atribuye más de quinientos años. Ilikar interpreta la mirada como indicación del camino a Shiaru y supone que la lentitud se debe a falta de agua. Por sugerencia de Eldrat, lanza una bolsa llena del lago. La tortuga la atrapa y lanza hacia arriba con una rapidez que contradice su lentitud aparente.',
    'El anciano siente sufrir las plantas de su caparazón y percibe vegetación que se marchita y muere cerca del lago, al norte de Iktan. Se pone de pie, hace temblar la roca y deja caer plantas. La población y Walulu se inclinan. Leona lo carga en la dirección que observa, con el consentimiento de su conducta aunque sin respuesta verbal; Ilikar, Triel y Eldrat los siguen. La voz mental del elfo causa nuevos equívocos sobre la supuesta estatua. Encuentran huesos, carne parcialmente devorada y miembros de animales y dinosaurios unidos de forma imposible. Leona lanza al anciano recogido en su caparazón para que los examine. El líquido verde huele a veneno dracónico y los viajeros creen estar ante restos de comida del dragón. Triel sigue vendada y desoye la petición de Eldrat de que vuelva a descansar. La masa empieza a sacudirse y se levanta.',
    'Leona carga en furia con el hacha y los golpes desprenden zombis verdosos. Eldrat hace girar al anciano con la cadena de su kusarigama: la maniobra derriba a dos enemigos, pero la masa mayor recompone su posición. Ilikar lanza a Triel con sus espadas a través de los cuerpos y después crece y combate con hielo. La criatura hiere a la elfa e intenta envolverla, aunque no consigue atraparla. Eldrat dirige sus dagas contra quienes atacan a su hermana y Leona golpea a varios rivales. Los zombis vuelven a levantarse y expulsan nubes venenosas; Tortas evita inhalarlas aguantando la respiración. El anciano aturde a un enemigo, Triel imita sus patadas y utiliza su espada de escamas, e Ilikar mantiene la presión con la lanza. Tortas remata al último zombi y el director confirma el final del combate. La victoria no demuestra que el claro quede descontaminado ni que esa masa sea la misma de la expedición anterior.',
    'Eldrat revisa las heridas de Triel, la reprende por arriesgarse estando convaleciente y termina celebrando con ella e Ilikar el lanzamiento. Recogen una muestra de veneno muy denso, de verde más intenso y aparentemente más agresivo que el yuan-ti conocido. Tortas se cura y recibe una poción de Triel; explica que es una tortuga viva y que permanecía quieto por su aprecio a la paciencia. Los juegos de fuerza llevan a golpear y talar árboles. El anciano reprocha haber derribado un árbol al que aún le quedaban muchos años y enseña a distinguir un tronco próximo a morir. En la conversación sobre los orígenes aparece un bosque lejano y una isla de grafía provisional Brunami, sin hablante identificado con seguridad. Tortas dice que no ha salido de Xoltacan.',
    'Tortas se presenta por su nombre y expresa su preocupación por el veneno. Triel cuenta que, tras las burlas de sus compañeros, salió a buscar al dragón para demostrar su valor. Entró en una cueva y recibió veneno por la espalda durante una emboscada. No sabe si es su guarida. La mesa recuerda el título Serpiente del Bosque, pero los subtítulos no fijan su nombre propio. Ilikar lo desafía a gritos. Tortas declara tener 77 años, cifra que queda en tensión con los siglos que le atribuye Walulu. El director aclara que puede sentir zonas afectadas por el veneno, no localizar al dragón. Ilikar encuentra ramas dañadas, arañazos y copas deshojadas que orientan hacia el norte. Eldrat reconoce el rastro, pero insiste en que están heridos y deben recuperarse. Triel y Leona forcejean mientras los demás discuten. Leona ordena mágicamente descansar a Ilikar, que cae y ronca; después lo carga de vuelta a Iktan.',
    'La población se arrodilla al ver caminar a Tortas. Leona entrega la botella a Walulu y atribuye al veneno la conversión de los animales en no muertos; la chamana ve una muestra potente, sin concluir un análisis, y ruega que no provoquen al dragón porque la ciudad no podría detenerlo. Tortas manifiesta brazos astrales verdes y lleva a Ilikar a la taberna, despertando la admiración de Triel, que quiere aprender la técnica. Leona acepta descansar antes de volver a Cuicapalli. Eldrat e Ilikar pactan herir al dragón para interrogarlo y entregar después su cabeza al goliat. Leona se presenta en la taberna como futura líder de Cuicapalli, todavía sin nombramiento oficial, y recibe trato especial. Triel cura a su hermano y ambos buscan aliados. Ilikar declara proceder de Valle Blanco, en las tierras frías del norte. Debe volver a Shiaru y propone sumar a Ione y Sir Poncelot; las grandes hazañas que atribuye al caballero son su testimonio, no hechos comprobados en esta sesión.',
    'Los preparativos derivan en competiciones de habilidad y fuerza. Una cabra destinada a la cena acaba aplastada por los golpes. Leona e Ilikar lanzan dos veces a Tortas al lago, pese a sus intentos de resistirse. Eldrat le aconseja esconderse bajo el agua y el anciano se sumerge. Triel ocupa la piedra sagrada e intenta meditar para obtener brazos astrales; los vecinos la miran con disgusto y Eldrat la retira y se disculpa ante Walulu. No aparece ningún poder nuevo. La sesión termina con los hermanos retirándose y Leona e Ilikar decidiendo qué hacer con la otra cabra. El dragón no ha sido enfrentado ni interrogado, la ayuda a Eromov no ha llegado en escena y el veneno sigue pendiente de estudio.',
]

missions = [
    'Advertir del ataque al festival: Leona informa a Walulu en nombre de Eromov. La chamana prepara el aviso a los guardias; no se representa un ataque yuan-ti ni se prueba que haya sido cancelado (40-002, 40-006).',
    'Ayudar a Eromov: Walulu promete enviar hombres, recetas y protecciones a Cuicapalli. El envío, la elaboración de un antídoto y la recuperación del dirigente no se muestran (40-006).',
    'Investigar la vegetación marchita: Tortas guía al grupo hasta los restos contaminados. Derrotan a los zombis y regresan con una muestra; no comprueban la recuperación del entorno (40-013–40-024, 40-026, 40-035).',
    'Cazar e interrogar al dragón: Ilikar encuentra un rastro al norte. Eldrat exige descansar y pacta obtener respuestas antes de que el goliat se quede con la cabeza. El combate y el reclutamiento de Ione y Poncelot siguen proyectados (40-030–40-033, 40-037, 40-039).',
    'Cuidar a los heridos: Triel sigue convaleciente y vuelve a exponerse al veneno. Tras las curaciones y el regreso a Iktan no se acredita su recuperación completa (40-017, 40-025, 40-027, 40-034–40-038).',
    'Aprender de Tortas: Triel imita sus patadas y pide aprender los brazos astrales. Meditar en la piedra no produce poderes ni acredita un aprendizaje completado (40-023, 40-036, 40-042).',
]
questions = [
    '¿Quién anima los restos y qué relación causal tiene el veneno con los no muertos? La semejanza dracónica y la explicación de Leona no sustituyen un análisis de la muestra (40-016–40-017, 40-026, 40-035).',
    '¿Se recuperará la vegetación o continúa la contaminación del entorno del lago y del claro? La derrota de los zombis no se acompaña de una comprobación del entorno (40-013, 40-015, 40-024).',
    '¿Cuál es la grafía del nombre de la Serpiente del Bosque y es la cueva de la emboscada su guarida? El rastro orienta al norte, pero no fija su posición ni su relación con Clodidrax (40-030–40-033).',
    '¿Qué información necesita Eldrat del dragón y aceptarán Ione y Poncelot ayudar? El interrogatorio y el reclutamiento no se realizan (40-037, 40-039).',
    '¿Qué explica los 77 años que declara Tortas frente a los siglos de inmovilidad que recuerda Walulu? No se ofrece una explicación (40-011, 40-031, 40-035).',
    '¿Llegará la ayuda prometida a Eromov y se producirá el ataque al festival? No se muestran el envío, una cura ni el ataque anunciado (40-002, 40-006, 40-036).',
    '¿Dónde está Cipo tras la patada y de dónde procede el fragmento de espada recuperado? No se resuelven su búsqueda ni la historia del arma (40-003–40-009).',
]
notes = [
    'La amenaza yuan-ti se comunica como advertencia, y la autoría del envenenamiento de Eromov sigue atribuida al testimonio de Leona. La promesa de Walulu no acredita una cura (40-002, 40-006).',
    'Cipo continúa siendo un elemental de fuego. Las alas, el dragón y el sol proceden de una excusa de Eldrat y de los equívocos de los buscadores (40-003–40-009).',
    'Tortas es una tortuga viva de apariencia pétrea, no una estatua cuya petrificación se haya roto. Su edad declarada y la antigüedad atribuida por Walulu quedan conservadas por separado (40-011, 40-027, 40-031, 40-035).',
    'Triel y Eldrat se identifican como hermanos en la sesión. La enfermedad y los cuidados coinciden con la pareja anónima del capítulo 39, pero no se enlaza expresamente aquella habitación con sus nombres (40-002, 40-007, 40-017).',
    'Los restos se comparan con comida del dragón y la muestra con veneno dracónico. No se presencia la creación de los zombis ni se demuestra que sean la masa del capítulo 31. El claro tampoco queda certificado como descontaminado (40-015–40-024, 40-035).',
    'El director limita la percepción de Tortas a zonas afectadas por el veneno. No permite localizar al dragón ni confirma una segunda criatura por una frase posterior del anciano (40-032–40-033).',
    'Leona entrega la muestra a Walulu, lo que establece su custodia al regreso. El hablante que la recoge inicialmente no queda identificado en ese pasaje (40-026, 40-035).',
    'Valle Blanco es el origen declarado por Ilikar; Shiaru es su residencia y destino de regreso. La emboscada relatada por Triel no explica las heridas con las que él apareció en el capítulo 38 (40-030, 40-039).',
    'Leona todavía no es dirigente oficial. Las proezas de Poncelot proceden del relato de Ilikar. El intento de Triel de obtener brazos astrales no tiene resultado; los lanzamientos finales de Tortas se resuelven en el lago (40-038–40-042).',
]
names = [
    'Tortas/Torta es la tortuga conocida como Gran Anciano y protector de Iktan; la presentación establece el nombre, con grafía provisional (40-029).',
    'Serpiente del Bosque es el título inteligible del dragón verde. Clen Dranks/clungrax/Clogreg/Clogen/Clog son lecturas automáticas inciertas. Se conserva una ficha descriptiva separada de Clodidrax/Clotis, sin afirmar que sean dragones distintos ni la misma identidad (40-030–40-032).',
    'Ilicar/Ilcar/Ericar e Icar corresponden a Ilikar; Eldra/el Dr a Eldrat; Tri/Trial/Trier a Triel. Walulu/Waluro y las variantes de Iktan, Shiaru y Cuicapalli se agrupan con sus identidades existentes.',
    'Tunkaz aparece en la presentación inicial de Ilikar y Brunami en una conversación sobre una isla lejana. Sus grafías y la atribución del segundo hablante quedan pendientes. Valle Blanco sí es un origen declarado inteligible, sin coordenadas (40-005, 40-028, 40-039).',
    'La tabernera tabaxi no se presenta por nombre en este capítulo: no se fusiona por este pasaje con Angélica Thunder ni con Angelique. Gusiluz es una broma rechazada por Eldrat, no una identidad nueva (40-029, 40-038).',
]
draft = dict(capitulo=40, estado_revision='revisado', resumen=' '.join(paragraphs), registros=records,
             misiones=missions, preguntas=questions, contradicciones=notes, nombres_dudosos=names)
write_json(ROOT / 'borradores/40.json', draft)
divisions = [
    ('Los viajeros y el encargo de Eromov', [1, 2, 3, 4, 5]),
    ('El festival del protector', [6, 7, 8, 10, 11, 12]),
    ('El bosque que se marchita', [13, 14, 15, 16, 17]),
    ('La masa y los zombis envenenados', [18, 19, 20, 21, 22, 23, 24]),
    ('Curarse y conocer al anciano', [25, 26, 27, 28]),
    ('El rastro y la retirada', [29, 30, 31, 32, 33, 34]),
    ('El regreso a Iktan y el pacto', [35, 36, 37, 38, 39]),
    ('Juegos y la piedra sagrada', [40, 41, 42]),
]
relatos = read_json(ROOT / 'config/relatos_capitulos.json')
relatos['capitulos']['40'] = [[title, '' if i == 0 else paragraphs[i].split('.')[0] + '.',
                             [f'40-{number:03d}' for number in refs]]
                            for i, (title, refs) in enumerate(divisions)]
write_json(ROOT / 'config/relatos_capitulos.json', relatos)

# Etiquetas descriptivas cuya identidad se integra en una ficha única.
catalog = read_json(ROOT / 'config/entidades.json')
new_entities = [
    ('Tortas', 'personaje', ['Tortas (anciano tortuga, grafía provisional)'], [7, 11, 29, 35], 'Tortuga monje venerada como Gran Anciano y protectora de Iktan.', 'Su aspecto pétreo no es una petrificación. Se conservan en tensión la edad declarada de 77 años y los siglos atribuidos por Walulu.'),
    ('Dragón verde del bosque de Iktan', 'personaje', ['Dragón verde del bosque de Iktan'], [2, 30, 32], 'Adversario del bosque relacionado con el veneno, las heridas de Triel y la caza proyectada por Ilikar y Eldrat.', 'Nombre propio de reconocimiento incierto. No se fusiona con Clodidrax ni se afirma que sean necesariamente criaturas diferentes. La destrucción de las casas antiguas tampoco fija su autoría.'),
    ('Masa zombi del claro envenenado', 'personaje', ['Masa zombi del claro envenenado', 'Zombis desprendidos de la masa (capítulo 40)'], [16, 17, 18, 24], 'Amalgama de fauna muerta que desprende zombis venenosos durante el combate del capítulo 40.', 'Nombre editorial descriptivo. Los zombis menores se integran en su historia; no se identifica con la masa del capítulo 31 ni se fija creador o especie de bestiario.'),
    ('Claro de los restos envenenados', 'lugar', ['Claro de los restos envenenados (capítulo 40)'], [13, 15, 16], 'Foco de vegetación marchita y cadáveres en las inmediaciones del lago al norte de Iktan.', 'Etiqueta geográfica descriptiva; no fija coordenadas, no abarca toda la orilla ni acredita la descontaminación posterior.'),
    ('Valle Blanco', 'lugar', ['Valle Blanco (origen declarado de Ilikar)'], [39], 'Lugar de las tierras frías del norte del que Ilikar declara proceder.', 'Procedencia declarada sin coordenadas. No se equipara con Tunkaz ni se confunde con Shiaru, donde Ilikar se ha alojado.'),
    ('Muestra de veneno del claro', 'objeto', ['Muestra de veneno del claro (capítulo 40)', 'Muestra de veneno entregada a Walulu'], [26, 35], 'Botella de veneno recogida tras el combate y entregada por Leona a Walulu.', 'Una sola muestra con dos etiquetas: se desconoce el recolector inicial; la entrega sí identifica a Leona y la custodia de Walulu. El análisis queda pendiente.'),
    ('Fragmento de espada bajo la roca', 'objeto', ['Fragmento de espada bajo la roca (40)'], [3], 'Pieza de espada rota que Cipo extrae de debajo de una roca sostenida por Ilikar.', 'No se establecen propietario, antigüedad ni relación con otras espadas.'),
    ('Piedra sagrada de Iktan', 'objeto', ['Piedra sagrada de Iktan (asiento de Tortas)'], [8, 13, 42], 'Soporte venerado que ocupaba Tortas y donde Triel intenta meditar al final del festival.', 'Su valor sagrado está documentado. No se demuestra que otorgue brazos astrales ni otro poder propio.'),
]
for name, kind, labels, refs, description, note in new_entities:
    group = dict(nombre=name, tipo=kind, etiquetas=labels, referencias=[f'40-{n:03d}' for n in refs], descripcion=description, nota=note)
    if name == 'Dragón verde del bosque de Iktan':
        group['referencias'].insert(0, '31-015')
    catalog['grupos'] = [g for g in catalog['grupos'] if g['nombre'] != name] + [group]
write_json(ROOT / 'config/entidades.json', catalog)

def stage(title, text, *refs):
    return dict(titulo=title, texto=text, referencias=[f'40-{n:03d}' if isinstance(n, int) else n for n in refs])

updates = {
    'Tortas': [
        stage('El protector abandona la piedra', 'La comunidad de Iktan venera al Gran Anciano, una tortuga cubierta de musgo y plantas cuyo movimiento asocia a las cosechas. Parece una estatua, pero gira la cabeza y atrapa una bolsa de agua a enorme velocidad. Siente que la vegetación muere cerca del lago y se levanta ante los vecinos. Leona lo transporta hacia el foco. Tortas se presenta por su nombre y explica que permanecía inmóvil por su paciencia. Dice tener 77 años, mientras Walulu le atribuye siglos: esa diferencia queda sin explicación.', 7, 8, 11, 12, 13, 14, 27, 29, 31, 35),
        stage('Un monje entre nuevos compañeros', 'Sale del caparazón tras el lanzamiento, examina los restos y combate junto a los viajeros. Acepta la maniobra de Eldrat con la cadena, aturde enemigos y remata al último zombi; evita el gas conteniendo la respiración. Después se cura, recibe una poción de Triel y enseña a respetar los árboles que aún tienen vida. Puede percibir las zonas dañadas por el veneno, pero el director aclara que no localiza al dragón mediante ese sentido.', 16, 18, 21, 22, 24, 27, 28, 32),
        stage('Los brazos astrales y el lago', 'Al volver a Iktan manifiesta brazos astrales verdes y lleva al goliat ante los vecinos arrodillados. Triel le pide aprender. Las competiciones posteriores terminan con Leona e Ilikar lanzándolo al lago a pesar de su resistencia; acepta el consejo de Eldrat y se esconde bajo el agua. La piedra que deja atrás conserva su valor sagrado, pero no transmite sus poderes a Triel.', 36, 40, 41, 42),
    ],
    'Dragón verde del bosque de Iktan': [
        stage('El enemigo que permanece en el bosque', 'Eldrat identifica un enorme dragón verde camuflado durante el viaje a Iktan; el grupo huye sin derrotarlo. Después relata que Triel volvió envenenada por ese dragón y que la cuidó. En el festival, Tortas expresa preocupación por el daño del veneno y se recuerda el título Serpiente del Bosque. Las variantes automáticas no fijan su nombre propio ni demuestran una identidad con Clodidrax.', '31-015', '31-019', 2, 29, 30),
        stage('Una persecución aplazada', 'Triel cuenta una emboscada con veneno al entrar en una cueva, sin saber si era la guarida. Los restos del claro y la muestra se comparan con veneno dracónico, pero no se observa su producción. El goliat encuentra un rastro hacia el norte y Eldrat exige recuperarse antes de seguirlo. Walulu teme que provocar al dragón cause un ataque que Iktan no podría detener. Eldrat e Ilikar pactan obtener respuestas y después entregar la cabeza como trofeo; aún no se enfrentan al enemigo.', 16, 26, 30, 32, 33, 35, 37, 39),
    ],
    'Masa zombi del claro envenenado': [
        stage('Los restos se levantan', 'Lo que parece comida medio devorada de fauna y dinosaurios contiene miembros de especies distintas unidos de forma imposible y líquido verdoso. La masa se sacude y se alza. Los golpes desprenden zombis menores; la peonza de Tortas derriba a dos, pero el cuerpo principal recompone su posición. Triel lo atraviesa al ser lanzada y después evita que la envuelva, aunque resulta herida.', 15, 16, 17, 18, 19, 20),
        stage('Veneno y derrota local', 'Los zombis pueden levantarse tras caer y expulsan nubes venenosas. Tortas contiene la respiración y aturde a un rival; los demás combaten con hacha, dagas, espada y hielo. El anciano remata al último zombi y termina el combate. La explicación de Leona sobre el veneno que los convirtió en no muertos sigue siendo un testimonio; no se establece creador ni identidad con la masa anterior del bosque.', 21, 22, 23, 24, 35),
    ],
    'Ilikar': [
        stage('De Shiaru al festival de Iktan', 'Tras la revancha con la capitana, busca en la selva un trofeo a raíz de su conversación con Erandy. Acompaña a Cipo, ayuda a sacar un fragmento de espada y acepta que Leona lo guíe a Iktan. Eldrat le oculta la patada que aleja al elemental y el goliat lo busca bajo la falsa idea de un dragón de fuego. Se relaciona con los elfos mediante sus saludos de fuerza y sigue a Tortas al bosque.', 1, 3, 4, 5, 7, 9, 12, 14),
        stage('El trofeo y el trato con Eldrat', 'Lanza a Triel a través de la masa y combate con lanza y hielo. Encuentra un rastro del dragón al norte, pero el grupo necesita descansar. Eldrat le concede la futura cabeza a cambio de poder interrogar antes al dragón. Ilikar declara proceder de Valle Blanco, en las tierras frías del norte; debe volver a Shiaru y propone reclutar a Ione y Sir Poncelot. Todavía no obtiene el trofeo. Los juegos con Leona acaban con Tortas en el lago.', 19, 20, 23, 25, 30, 33, 34, 37, 39, 41),
    ],
    'Eldrat': [
        stage('Cuidar a Triel durante el festival', 'Cuenta que su hermana regresó envenenada por el dragón verde y que la cuidó por miedo a perderla. Entrena con Coyote y Tesara y vigila los riesgos que Triel toma ante el anciano sagrado. En el claro le pide que vuelva a la aldea, pero acaba luchando para protegerla. Utiliza la cadena de su kusarigama para lanzar a Tortas, comunica avisos mentalmente y sufre el gas venenoso. Tras la victoria reprende a su hermana y comparte su celebración con el goliat.', 2, 5, 7, 8, 10, 17, 18, 21, 24, 25),
        stage('Preguntas para el dragón', 'Reconoce el rastro encontrado por Ilikar, pero insiste en descansar antes de enfrentarse al dragón. Pacta con el goliat herir al enemigo para obligarlo a responder y cederle después la cabeza. Triel lo cura y los hermanos intentan reunir aliados; también considera visitar a Ione y Poncelot. Al terminar aconseja a Tortas esconderse en el lago y retira a Triel de la piedra sagrada, disculpándose ante Walulu. Las preguntas que quiere formular al dragón no se revelan.', 33, 34, 37, 38, 39, 41, 42),
    ],
    'Triel': [
        stage('La convalecencia no frena su curiosidad', 'Eldrat cuenta que la cuidó tras su regreso envenenada. Walulu le recomienda salir al festival. Triel intenta tocar al anciano y probar su movimiento con una piedra. Sigue al grupo todavía vendada, pide a Ilikar que la lance a través de la masa de cadáveres y vuelve a resultar herida. Continúa con su espada de escamas e imita las patadas de Tortas. Se cura un poco, celebra la maniobra y administra una poción al monje. Su entusiasmo no acredita una recuperación completa. Al conversar con Tortas explica que buscó al dragón para demostrar su valor y este la emboscó con veneno por la espalda en una cueva que no sabe si era su guarida.', 2, 7, 8, 10, 17, 19, 20, 23, 25, 27, 29, 30),
        stage('El deseo de aprender los brazos astrales', 'Admira los brazos verdes con los que Tortas lleva al goliat y le pide aprender. También cura a Eldrat y ayuda a buscar compañeros para la caza del dragón. Después ocupa la piedra sagrada e intenta meditar para conseguir el mismo poder. Los vecinos la miran con disgusto y su hermano la aparta. No obtiene brazos astrales ni se demuestra que el soporte tenga poderes.', 36, 38, 42),
    ],
    'Leona': [
        stage('Representar a Cuicapalli', 'Deja a Guayacán cuidando a Eromov y viaja a Iktan para advertir de un posible ataque al festival. Guía hasta allí a Ilikar y Cipo y consigue que Walulu prometa precauciones y ayuda. En la celebración carga a Tortas hacia el foco de vegetación muerta. Lucha en furia con el hacha, participa en maniobras con el monje y resiste parte del veneno. Su cometido diplomático y su acción en el bosque no equivalen todavía a una investidura como dirigente.', 2, 3, 6, 14, 16, 18, 20, 21, 24),
        stage('La muestra y el descanso aplazado', 'Obliga mágicamente a Ilikar a descansar y lo carga de vuelta. Entrega a Walulu la botella de veneno y cuenta que convirtió a las criaturas en no muertos, interpretación que no recibe aún un análisis concluyente. Acepta descansar antes de regresar a Cuicapalli. En la taberna afirma ser considerada futura líder, aunque no oficialmente, y recibe mejor alojamiento y comida. Después participa en los juegos de fuerza y en los lanzamientos de Tortas al lago.', 34, 35, 36, 38, 40, 41),
    ],
    'Walulu': [
        stage('Una advertencia durante el festival', 'Leona le informa del envenenamiento de Eromov y de un posible ataque yuan-ti. Walulu promete avisar a los guardias y enviar hombres con recetas y protecciones para su amigo de Cuicapalli. Ha recomendado a Triel salir para despejarse y conduce a Leona a la ceremonia del Gran Anciano. Atribuye a la tortuga más de quinientos años y se inclina cuando esta se levanta.', 6, 7, 10, 11, 13),
        stage('Proteger Iktan del dragón', 'Al regreso ve caminar a Tortas, a quien atribuye siglos de inmovilidad. Recibe de Leona una muestra de veneno que parece potente, pero no concluye una fórmula ni explica la creación de los no muertos. Advierte que la ciudad no podría detener al dragón si lo provocan. Permite descansar a Leona y presencia el disgusto de los vecinos cuando Triel ocupa la piedra sagrada. Su conversación pendiente con Citlali sobre las marcas no se representa.', 35, 36, 42),
    ],
    'Eromov': [stage('Un enviado y una promesa de ayuda', 'Leona lo describe todavía envenenado y cuenta que la envió a Iktan para prevenir un ataque durante el festival. Guayacán queda cuidándolo. Walulu lo llama amigo y promete enviar recetas y protecciones. Esto documenta un nuevo encargo referido por Leona y una oferta de apoyo, sin mostrar el envío ni la administración de un antídoto.', 2, 6)],
    'Guayacán': [stage('Cuidar al dirigente durante la misión', 'Leona lo llama su aprendiz y explica que lo deja en Cuicapalli cuidando al envenenado Eromov mientras ella advierte a Walulu. La recapitulación no fija una sucesión de Leona ni resuelve el secreto anterior de Guayacán.', 2)],
    'Cipo': [stage('El fragmento y la búsqueda fallida', 'Con sombrero de explorador, extrae una pieza de espada de debajo de la roca que sostiene Ilikar. Reconoce a Leona y los acompaña a Iktan. Eldrat lo pisa, recibe un mordisco y lo aleja de una patada que el goliat no presencia. El elfo encubre lo sucedido diciendo que al elemental le salieron alas. Ilikar y un guardia lo buscan bajo la idea de un dragón de fuego, sin recuperarlo en escena. Esa confusión no cambia su naturaleza de elemental.', 3, 4, 5, 7, 9)],
    'Sir Poncelot': [stage('Un aliado propuesto desde Iktan', 'Ilikar propone incorporarlo a la caza del dragón junto con Ione y le atribuye grandes hazañas contra dragones, dinosaurios y gigantes. Esas proezas pertenecen al relato del goliat, no se representan en esta sesión. Eldrat considera visitar a ambos; no hay invitación ni aceptación mostradas.', 39)],
    'Ione': [stage('Una capitana a la que se quiere reclutar', 'Al pactar con Eldrat contra el dragón, Ilikar propone sumar la fuerza de su capitana Ione y de Sir Poncelot, pero explica que debe regresar a Shiaru. No se muestra una invitación ni la respuesta de la capitana.', 39)],
    'Claro de los restos envenenados': [stage('La vegetación anuncia el peligro', 'Tortas siente que las plantas mueren en las inmediaciones del lago al norte de Iktan. El grupo encuentra animales y dinosaurios medio devorados cuyos restos dañan el entorno. El líquido verdoso se compara con veneno dracónico y los cuerpos se levantan como una masa. Allí se libra el combate y se recoge una muestra. La derrota del último zombi no va seguida de una comprobación de la recuperación del claro.', 13, 15, 16, 17, 24, 26)],
    'Valle Blanco': [stage('La tierra fría recordada por Ilikar', 'Ilikar declara que procede de Valle Blanco, en las tierras frías del norte, al comparar las costumbres de fuerza de su tierra con los juegos de sus nuevos compañeros. El lugar no se visita, no recibe coordenadas y no se identifica con Shiaru ni con la lectura incierta Tunkaz de su saludo inicial.', 5, 39)],
    'Muestra de veneno del claro': [stage('De los restos a manos de Walulu', 'Tras vencer a los zombis, un integrante recoge en una botella un veneno muy denso, más verde y aparentemente más agresivo que el de los yuan-ti conocidos. No se identifica al recolector en ese pasaje. Al regresar a Iktan, Leona entrega la muestra a Walulu y atribuye a ella la conversión de las criaturas en no muertos. La chamana ve que parece potente y advierte del riesgo de provocar al dragón. La custodia queda documentada, pero el análisis y la explicación causal siguen abiertos.', 16, 26, 35)],
    'Fragmento de espada bajo la roca': [stage('Un hallazgo de Cipo', 'Cipo busca debajo de una roca de la jungla y, con ayuda de Ilikar que la sostiene parcialmente, extrae un trozo de arma. Otro filo queda clavado debajo. La expedición no identifica dueño, antigüedad ni uso posterior del fragmento, y no lo relaciona con ninguna espada previa.', 3)],
    'Piedra sagrada de Iktan': [stage('El soporte del protector', 'La tortuga venerada permanece sobre una roca cubierta de vegetación hasta que siente el deterioro del bosque y se levanta, haciendo temblar el soporte. Al final Triel ocupa la piedra e intenta meditar para obtener brazos astrales. La población muestra disgusto y Eldrat la aparta y se disculpa ante Walulu. Su carácter sagrado es visible en el trato de los habitantes; no se demuestra un poder propio ni la transmisión de las capacidades de Tortas.', 8, 13, 42)],
    'Iktan': [stage('El festival y una amenaza que se extiende', 'La ciudad celebra los movimientos del Gran Anciano como augurio de cosechas. Leona llega para advertir de un ataque yuan-ti y Walulu promete precauciones y ayuda a Cuicapalli. Tortas se levanta al sentir plantas morir junto al lago al norte de Iktan; los visitantes investigan, vencen a los zombis y vuelven con una muestra. La dirigente teme un ataque del dragón que no podrían detener. La población reverencia al monje y protege el valor de su piedra, incluso frente a la curiosidad de Triel.', 6, 8, 11, 13, 15, 24, 35, 36, 42)],
    'Cuicapalli': [stage('La advertencia de Leona y el apoyo prometido', 'Con Eromov todavía envenenado según Leona, Guayacán queda cuidándolo y ella actúa como representante ante Walulu para advertir del posible ataque al festival de Iktan. La chamana promete enviar hombres, recetas y protecciones. Leona se presenta después como futura líder de Cuicapalli, pero admite que no es oficial. El regreso de la enviada, la ayuda y la cura no se muestran.', 2, 6, 36, 38)],
    'Yuan-ti': [stage('Una amenaza comunicada durante el festival', 'Leona atribuye a los hombres serpiente el envenenamiento de Eromov y transmite a Walulu la previsión de un ataque al festival de Iktan. Se adoptan precauciones, sin que el capítulo muestre ese ataque ni revele nuevos mandos. La muestra obtenida en el claro se describe como diferente del veneno yuan-ti conocido, por lo que los zombis no se les atribuyen por semejanza.', 2, 6, 26, 35)],
    'Espada azul de escamas de Triel': [stage('De nuevo en combate durante la convalecencia', 'Triel la emplea contra los zombis del claro mientras sigue herida. Cambia de postura y combina los golpes de la espada de escamas con patadas que imitan a Tortas. El capítulo no le adjudica nuevos poderes ni modifica su procedencia.', 23)],
}
paths = list((ROOT / 'config').glob('historias_*.json'))
documents = {p: read_json(p) for p in paths}
for name, stages in updates.items():
    targets = [(p, doc, 'personajes' if 'personajes' in doc else 'entidades') for p, doc in documents.items()
               if name in doc.get('personajes', doc.get('entidades', {}))]
    if not targets:
        kind = next(g['tipo'] for g in catalog['grupos'] if g['nombre'] == name)
        filename = {'personaje': 'historias_personajes_complementarias.json', 'lugar': 'historias_lugares.json', 'objeto': 'historias_objetos.json', 'faccion': 'historias_facciones.json'}[kind]
        p = ROOT / 'config' / filename
        doc = documents[p]
        key = 'personajes' if kind == 'personaje' else 'entidades'
        targets = [(p, doc, key)]
    assert len(targets) == 1, name
    p, doc, key = targets[0]
    # Idempotencia: conservar las etapas anteriores y sustituir solo las nuevas.
    old = [s for s in doc[key].get(name, []) if not any(ref.startswith('40-') for ref in s['referencias'])]
    doc[key][name] = old + stages
for p, doc in documents.items():
    doc['revisado_hasta'] = 40
    write_json(p, doc)

# Cotejo de todas las preguntas anteriores contra la sesión completa.
reviews = {p: read_json(p) for p in (ROOT / 'config').glob('seguimiento_preguntas_*.json') if p.name != 'seguimiento_preguntas_40.json'}
all_questions = {q['id']: q for doc in reviews.values() for q in doc['preguntas']}
def answer(qid, text, refs, pending=None, state=None):
    q = all_questions[qid]
    q['respuesta'] = text
    q['referencias'] = list(dict.fromkeys([*[r for r in q['referencias'] if not r.startswith('40-')], *[f'40-{n:03d}' for n in refs]]))
    if pending is not None:
        q['pendiente'] = pending
    if state is not None:
        q['estado'] = state

answer('P30-001', 'Leona relata que Eromov sigue envenenado, que la envió a Iktan para advertir de un ataque y que Guayacán quedó cuidándolo. Walulu promete enviar hombres, recetas y protecciones. Esto aporta un estado referido y un ofrecimiento de ayuda, pero no muestra un antídoto administrado ni la recuperación del líder.', [2, 6])
answer('P30-005', 'Además de la operación contra Citlali y Etley, Leona transmite una previsión de ataque yuan-ti al festival de Iktan. Walulu promete precauciones. La advertencia no se convierte en un ataque mostrado ni identifica jerarquía, aliados o vínculo organizativo preciso con Hoja Caída.', [2, 6])
answer('P31-001', 'El capítulo 40 recuerda al dragón verde como Serpiente del Bosque y proporciona un nombre con lecturas automáticas inciertas: Clen Dranks, clungrax, Clogreg y variantes. No fija una grafía inequívoca ni prueba quién destruyó las casas antiguas de Iktan. La similitud con Clodidrax/Clotis no permite fusionar las identidades.', [30, 32])
answer('P31-002', 'Los viajeros encuentran un nuevo foco de plantas muertas, restos fusionados y zombis que expulsan veneno. Derrotan a los enemigos de ese claro y recogen una muestra, pero no vencen al dragón ni demuestran que sean los mismos cadáveres de la expedición anterior. La percepción de Tortas detecta zonas afectadas, no al dragón. No se explica el mecanismo de las voces ni una neutralización permanente.', [15, 16, 21, 24, 32, 35])
answer('P34-002', 'Nox reaparece en Shiaru, prepara la infiltración de Aurora, regresa con Molly y después parte hacia el fuerte con el ojo. El capítulo 40 sí nombra a Triel y Eldrat en Iktan: ella sale al festival y participa vendada en la expedición al claro. Queda establecido un paradero posterior de Triel tras su ausencia, sin atribuir retrospectivamente esos nombres a los elfos anónimos de la habitación del 39.', [2, 7, 17], '', 'resuelta')
answer('P38-001', 'Ilikar reaparece en el capítulo 40 y participa en la expedición de Iktan, pero no se muestra una transformación ni se diagnostica el efecto de la mordedura de Ione. El crecimiento en furia y el daño de hielo no se atribuyen a ella. Tampoco su reaparición acredita inmunidad.', [1, 20, 39])
answer('P38-002', 'Ilikar declara proceder de Valle Blanco, en las tierras frías del norte. No explica quién le causó las heridas de su llegada a la playa ni desarrolla toda su historia tribal. La emboscada con veneno relatada en esta sesión corresponde a Triel, no al goliat.', [39], 'La causa de las heridas con que apareció en la playa y los detalles de sus antecedentes tribales.', 'parcial')
answer('P39-001', 'Los yuan-ti reclaman la piel de Citlali como clave y su maldición cura a una abominación. El capítulo 40 no retoma la explicación de las marcas ni identifica al Señor; el nuevo veneno del bosque no demuestra una relación causal con ellas.', [])
answer('P39-002', 'Citlali expresa una duda sobre el bebé y la influencia del alcohol. El capítulo 40 no aporta una identificación ni confirma parentesco entre Citlali y Nox.', [])
answer('P39-003', 'La continuación nombra a Eldrat y a su hermana Triel en Iktan. Eldrat relata que ella volvió envenenada por el dragón verde y que la cuidó; sale del templo al festival y sigue vendada. Es una continuidad compatible con la pareja anónima, pero no hay un enlace expreso a aquella habitación. No se explica por qué Clodidrax no podía acercarse ni se acredita un diagnóstico de la elfa de esa escena.', [2, 7, 17])
answer('P39-004', 'La conversación de Walulu con Citlali sobre las marcas no se representa. En cambio se amplían los problemas de Iktan: Leona advierte de un posible ataque yuan-ti; Tortas detecta vegetación marchita y el grupo encuentra restos animados y veneno. Walulu recibe la muestra y teme un ataque del dragón que la ciudad no podría detener.', [6, 13, 16, 35], 'El resultado de la conversación con Citlali sobre las marcas y las causas de la amenaza del bosque.', 'parcial')
for p, doc in reviews.items():
    doc['revisado_hasta'] = 40
    doc['cotejo_capitulo_40'] = 'Preguntas cotejadas individualmente con los tres bloques completos. Las respuestas sin novedad conservan su evidencia y estado; se actualizan únicamente las continuidades aportadas por esta sesión.'
    for q in doc['preguntas']:
        q['revisado_hasta'] = 40
    write_json(p, doc)
tracking_new = []
new_answers = [
    ('Los restos fusionados se levantan y desprenden zombis que expulsan gas. Leona atribuye su condición al veneno al entregar la muestra; Walulu solo observa que parece potente. No se identifica a un creador ni se concluye un análisis.', 'El origen de la animación de los restos y la función causal del veneno.'),
    ('El grupo mata al último zombi y abandona el claro. La recogida de una muestra y el regreso a Iktan no incluyen una inspección de las plantas ni una descontaminación.', 'La extensión restante del daño y la recuperación de la vegetación.'),
    ('La mesa recuerda el título Serpiente del Bosque y varias lecturas inciertas del nombre. Triel cuenta la emboscada de la cueva sin saber si era una guarida. El rastro hallado por Ilikar orienta al norte, pero la persecución se aplaza.', 'La grafía, la ubicación de la guarida y la relación de identidad con Clodidrax.'),
    ('Eldrat obtiene de Ilikar el compromiso de preguntar antes de entregarle la cabeza del dragón. No revela el contenido de sus preguntas. Ilikar propone a Ione y Poncelot como aliados, sin invitación ni aceptación mostradas.', 'Las preguntas de Eldrat, el reclutamiento y el cumplimiento del pacto.'),
    ('Tortas dice tener 77 años. Walulu le atribuye más de quinientos y recuerda siglos de inmovilidad anteriores a su bisabuela. La fuente no explica cómo conciliar esas declaraciones.', 'La edad de Tortas y la historia de su inmovilidad.'),
    ('Walulu promete enviar ayuda y avisar a los guardias. Leona descansa en la taberna antes del regreso previsto. No se muestra un ataque, la salida de los emisarios ni una cura administrada a Eromov.', 'El envío y resultado de la ayuda, la recuperación de Eromov y el destino del ataque anunciado.'),
    ('Cipo extrae la pieza y más tarde Eldrat lo aleja de una patada. Ilikar y el guardia lo buscan a partir de un equívoco, sin recuperarlo en escena. No se identifica al dueño ni la procedencia del arma.', 'El paradero de Cipo y el origen y destino del fragmento de espada.'),
]
for i, question in enumerate(questions, 1):
    import re
    refs = list(dict.fromkeys(re.findall(r'\b40-\d{3}\b', question)))
    tracking_new.append(dict(id=f'P40-{i:03d}', capitulo=40, indice=i, pregunta=question,
                             estado='pendiente', respuesta=new_answers[i-1][0],
                             referencias=refs, pendiente=new_answers[i-1][1], revisado_hasta=40))
write_json(ROOT / 'config/seguimiento_preguntas_40.json', dict(version=1, revisado_hasta=40, preguntas=tracking_new))
print('Integración editorial preparada: 42 registros, 8 etapas y 8 identidades nuevas.')
