"""Entrega local tras lectura humana íntegra de los 1566 segmentos asignados."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import validate_fact

SOURCE = ROOT / 'campanas/xoltacan/fuentes/48 - FYarBX28XfI.es-orig.vtt'
EXPECTED = '1fe4de4381f91a2e084979a969a5ac43d91a6c000b0d4379ed3755907844383d'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
S = json.loads((HERE / 'bloque_2_segmentos.json').read_text(encoding='utf-8'))
Q = json.loads((HERE / 'preguntas_bloque_2.json').read_text(encoding='utf-8'))
CAVE = 'Cueva envenenada explorada por el grupo'
DEAD = 'No muertos de la cueva envenenada'
BOTTLES = 'Botellas antitoxina de la cueva'
TESA = 'Tesara Queen'
NAOR = 'Naór'
ELD = 'Eldrath'
TRY = 'Tryel'
COY = 'Coyote'
DRAGON = 'Clolgedranx'
F = []


def fact(number, title, kind, text, first, last, evidence, entities, limitation):
    cue = S[evidence]
    record = {
        'id': f'48-{number}', 'titulo': title, 'tipo': kind, 'afirmacion': text,
        'inicio': S[first]['inicio'], 'fin': S[last]['fin'],
        'cita': cue['texto_original'],
        'evidencia_cue': {'id': cue['id'], 'inicio': cue['inicio'], 'fin': cue['fin'], 'texto': cue['texto_original']},
        'entidades': entities,
        'ambito': 'exploración de la cueva envenenada y combate contra sus no muertos',
        'conocedores': [], 'conocimiento_personaje': 'desconocido',
        'nota_conocimiento': 'No se determina aquí el acceso de Madame Oghma. Las presencias y acciones narradas no se convierten en conocimiento compartido fuera de escena.',
        'confianza': 'lectura íntegra de subtítulos; audio no cotejado',
        'limitacion': limitation,
    }
    validate_fact(record, SOURCE)
    F.append(record)


fact(201, 'Antorchas para entrar en una cueva cubierta de raíces', 'hecho_confirmado',
     'Los viajeros comprueban que llevan antorchas. Tesara mantiene pistola y antorcha en las manos, lo que impide utilizar al mismo tiempo el látigo. La cueva tiene raíces por suelo y paredes, incluso atravesando la roca, musgo y pequeños estanques de veneno. Se advierten unos a otros que eviten las charcas.',
     0, 50, 31, [TESA, CAVE],
     'La consulta de inventario y los botones de mochila son procedimiento de mesa. No se identifica un topónimo propio, no se determina el constructor de la cueva ni se confirma que cada elemento verde posea idénticas propiedades.')
fact(202, 'Eldrath reconoce cápsulas que expulsan una nube tóxica', 'explicacion_director',
     'Al examinar unas plantas extrañas con una tirada de Naturaleza, Eldrath descubre capullos que rezuman veneno y se abren para soltar una nube tóxica. Advierte al grupo que procure no tocarlos.',
     51, 67, 62, [ELD, CAVE],
     'Se describen las plantas presentes; no se ofrece nombre botánico, especie de bestiario ni una explicación del origen de su veneno.')
fact(203, 'La capa de Eldrath contiene una primera descarga', 'hecho_confirmado',
     'Eldrath se acerca cuidadosamente y cubre una de las cápsulas con la capa, intentando formar una bolsa que retenga el gas. La planta se abre y vuelve a cerrarse; el director confirma que esa descarga no lo afecta. Un nuevo acercamiento de Eldrath con la capa vuelve a evitar el efecto por el momento.',
     68, 129, 102, [ELD, CAVE],
     'Las salvaciones resuelven estos acercamientos. No se adjudica inmunidad permanente ni se demuestra que la capa neutralice por sí sola todo el gas de una sala.')
fact(204, 'Los acercamientos descuidados terminan en envenenamiento', 'hecho_confirmado',
     'Otro intento de cubrir la planta, seguido de la propuesta de echarse encima, hace que una cápsula expulse veneno directamente a la cara de quien se acerca. Se adjudica la condición de envenenado. Después del fracaso, los viajeros discuten y piden probar otro método.',
     105, 162, 120, [CAVE],
     'El turno no permite asignar con seguridad todas esas frases a una sola voz. Se conserva el envenenamiento sin inventar el nombre de su primera víctima; las bromas sobre la falda no establecen una identidad nueva.')
fact(205, 'Tesara propone cruzar colgados de las raíces', 'hecho_confirmado',
     'Tesara guarda la pistola y usa el látigo para descolgar raíces o enredaderas del techo. Propone pasar agarrándose a ellas por encima de las plantas. El director exige salvaciones de Constitución: el alcance del látigo deja a los viajeros a menos de diez pies de las cápsulas y la nube también alcanza esa altura.',
     163, 213, 192, [TESA, CAVE],
     'La maniobra no evita las salvaciones. No se da por establecido que todos fallen ni se deduce inmunidad por no pisar el suelo.')
fact(206, 'La kusarigama abre camino donde fallan las dagas psíquicas', 'hecho_confirmado',
     'Eldrath prueba una daga psíquica contra las cápsulas: impacta, pero la planta no se inmuta. Cambia a la parte cortante de su kusarigama, ataca desde más lejos y corta una cápsula, que descarga el gas y queda muerta. Decide continuar podándolas para despejar también el regreso.',
     214, 249, 242, [ELD, CAVE],
     'La adjudicación de daño psíquico corresponde a esta planta; no se universaliza a toda vegetación o criatura. Cortar una cápsula libera gas en lugar de hacerlo desaparecer de inmediato.')
fact(207, 'Una sala de huesos despierta las sospechas de Tesara', 'hecho_confirmado',
     'La siguiente sala presenta un ambiente verdoso que se nota en la nariz, pozas de veneno, musgo y montones de huesos y cadáveres. Tesara pide no acercarse a los cuerpos que puedan levantarse y recuerda al grupo el peligro de los no muertos.',
     250, 285, 271, [TESA, CAVE],
     'El examen inicial no determina aún qué cadáveres son enemigos, sus identidades o cuánto tiempo llevan allí.')
fact(208, 'El poder atribuido al dragón sigue siendo un aviso del grupo', 'declaracion_personaje',
     'En la discusión sobre buscar pistas entre los cuerpos, se advierte que el dragón puede resucitarlos. La afirmación sirve para insistir en que no se acerquen a los cadáveres.',
     273, 298, 289, [DRAGON, TESA, CAVE],
     'Es la explicación que los viajeros manejan. En este instante no se muestra al dragón animando los cuerpos ni se demuestra qué controla cada adversario de la cueva.')
fact(209, 'Naór patea una calavera antes de oír los primeros ruidos', 'hecho_confirmado',
     'Naór lanza de una patada una calavera hacia el fondo de la caverna. Al principio no ocurre nada visible. Cuando siguen avanzando y distinguen otra sala al sur, oyen ruidos detrás; Tesara le recuerda que le había pedido no tocar cadáveres y ella responde que solo ha chutado una calavera.',
     299, 329, 321, [NAOR, TESA, CAVE],
     'La secuencia temporal no prueba que la patada cause la animación ni identifica al responsable. No se convierte la calavera en un vestigio con poderes.')
fact(210, 'Un arquero no muerto ataca por la retaguardia', 'hecho_confirmado',
     'Tesara se desplaza sin dejar de mirar hacia los ruidos y mantiene la mano en la pistola. Tryel sigue al grupo sin haberse enterado inicialmente. Algo se levanta detrás de ellos y dispara; una flecha transmite veneno. Tesara saca la pistola y grita que tengan cuidado con el suelo.',
     330, 381, 379, [TESA, TRY, DEAD, CAVE],
     'El VTT no permite repartir con certeza la percepción entre todos los presentes ni identificar por nombre propio al arquero. Las referencias al móvil corresponden a la mesa.')
fact(211, 'Tesara dispara mientras Eldrath termina de podar', 'hecho_confirmado',
     'Tesara apunta y dispara con desventaja por el veneno y la distancia. Un segundo esqueleto dispara desde más allá del alcance que se estaba comprobando. Mientras tanto, Eldrath rompe la última planta que tenía delante y se aproxima al combate.',
     382, 430, 428, [TESA, ELD, DEAD, CAVE],
     'Se despeja ese paso de plantas, sin acreditar la eliminación de toda vegetación tóxica de la cueva. No se fija un número total de flechas o enemigos.')
fact(212, 'Naór lanza a Tryel hacia los enemigos', 'hecho_confirmado',
     'Tryel señala a un enemigo y pide que la lancen. Naór activa su furia, obtiene puntos temporales y la arroja unos treinta y cinco pies. Tryel intenta golpear al llegar, pero el ataque falla por la desventaja del veneno; Naór se acerca corriendo después.',
     431, 471, 460, [NAOR, TRY, DEAD],
     'Los puntos temporales y el lanzamiento se resuelven mecánicamente. No se asigna la furia a Tryel ni se presenta el lanzamiento fallido como una baja enemiga.')
fact(213, 'Zombis y esqueletos se levantan alrededor del grupo', 'hecho_confirmado',
     'Más zombis y esqueletos se incorporan desde distintos puntos de la sala. Los zombis avanzan contra Coyote y Tryel y otros rivales disparan. Coyote combate con dos dagas y Tryel devuelve golpes mientras recibe presión desde varios lados.',
     472, 542, 480, [COY, TRY, DEAD, CAVE],
     'Los señalamientos sobre el tablero no aportan coordenadas absolutas. El colectivo de esta cueva se mantiene separado de los cadáveres de las ruinas del lago del capítulo anterior.')
fact(214, 'Las flechas y la vegetación prolongan el veneno', 'hecho_confirmado',
     'Un esqueleto alcanza a Coyote con una flecha envenenada. Tesara sigue buscando una posición útil para disparar y se oculta detrás de una seta; el director exige otra salvación de Constitución y confirma que continúa envenenada.',
     543, 620, 616, [COY, TESA, DEAD, CAVE],
     'Las discusiones sobre el final del turno no fijan una duración universal del veneno. Las bromas de frustración no representan una muerte de Tesara.')
fact(215, 'Eldrath se suma a los ataques de la sala', 'hecho_confirmado',
     'Después de terminar la poda, Eldrath avanza y ataca dos veces al enemigo que elige. El director y el jugador completan su turno, con impactos adjudicados, mientras el resto del grupo continúa rodeado.',
     621, 641, 637, [ELD, DEAD],
     'No se adjudica una baja concreta si el texto solo confirma el impacto. El cambio de quién maneja el turno no implica ausencia del personaje de la escena.')
fact(216, 'La furia de Naór abate a varios adversarios', 'hecho_confirmado',
     'Naór ruge y aplica el efecto necrótico de su furia a los enemigos cercanos, excluyendo a Tryel. Algunos superan la salvación y no reciben daño. Encadena después golpes: cae un esqueleto y otros adversarios terminan en el suelo, uno de ellos sin piernas.',
     642, 709, 685, [NAOR, TRY, DEAD],
     'Se conservan las adjudicaciones de salvación, sin atribuir todo el daño a un poder desconocido o a la intervención del chat. Los caídos no permiten reconstruir un censo completo de la sala.')
fact(217, 'Coyote bebe un frasco durante el combate', 'hecho_confirmado',
     'Mientras Tryel sigue recibiendo ataques, Coyote hiere a un adversario y bebe el contenido de un frasco que dice haber comprado. Continúa usando sus recursos para alterar ataques enemigos y conceder ventaja; la elección de aliado depende de a quién puede ver.',
     710, 778, 740, [COY, TRY, DEAD],
     'En este intercambio no se describe con claridad el contenido del frasco ni su efecto final. No se identifica automáticamente con las antitoxinas que Eldrath menciona más adelante.')
fact(218, 'Tryel derriba un esqueleto y Tesara vuelve a exponerse al gas', 'hecho_confirmado',
     'Tryel se deshace de un esqueleto y se vuelve hacia el zombi. Coyote recibe otra flecha. Tesara intenta esconderse bajo otra planta y, aunque su aspecto le parecía menos peligroso, debe superar de nuevo una salvación; continúa envenenada.',
     779, 837, 794, [TRY, COY, TESA, DEAD, CAVE],
     'Los chistes sobre dispararse y dejar de sufrir no se ejecutan. Que una planta parezca una palmera no establece que sea inocua.')
fact(219, 'Coyote prepara un dinosaurio espiritual que aún no invoca', 'declaracion_personaje',
     'Coyote sigue atacando con sus cuchillos. Pregunta por una capacidad guardada en su fruta que produciría un dinosaurio espiritual, comparada en la mesa con un arma espiritual. Al aclararse que requiere la acción adicional ya gastada, aplaza su uso para un turno posterior.',
     838, 938, 937, [COY, ELD, NAOR, DEAD],
     'Es una consulta y una intención. No se materializa aquí el dinosaurio ni se crea una nueva entidad a partir de la capacidad anunciada. La ayuda y las cartas mencionadas pertenecen al chat y al procedimiento de juego.')
fact(220, 'Tryel remata a otro rival y Tesara consigue disparar', 'hecho_confirmado',
     'Tras el ataque de un zombi, se corrige el daño pendiente de Tryel y el director confirma que ha acabado con su adversario. Tesara sale del escondite, corre hasta obtener alcance y dispara. Se aclara que la carga de fuego ya se ha consumido y que la desventaja le impide añadir ataque furtivo.',
     939, 1017, 969, [TRY, TESA, 'Escupefuego', DEAD],
     'No se narran cargas nuevas recuperadas ni una vulnerabilidad al fuego de los enemigos. La corrección de daño no concede una baja adicional distinta del adversario que se estaba resolviendo.')
fact(221, 'Los ataques de Eldrath y Naór reducen los últimos enemigos', 'hecho_confirmado',
     'Eldrath apunta al enemigo que combate con Coyote para terminar con él y lanza otro ataque hacia el que está cerca de Tryel, antes de ponerse junto a Tesara. Naór alcanza a dos rivales con el efecto de su furia, aunque uno resiste, y continúa intentando golpearlos. Un esqueleto que la tiene enfrente saca la espada y consigue herirla.',
     1018, 1060, 1058, [ELD, NAOR, COY, TRY, TESA, DEAD],
     'La intención de terminar con un enemigo no sustituye una confirmación independiente de su muerte. Se conserva el progreso del combate sin inventar totales de bajas o puntos de vida.')
fact(222, 'La inspiración de Coyote provoca a Naór', 'hecho_confirmado',
     'Coyote ataca e intenta inspirar a Naór diciéndole que hará de Leo un descarado que toque a los otros escolares. El director adjudica el resultado como un bono de cinco para las acciones de Naór contra el propio Coyote. Tryel le muestra su manera de espantar a un enemigo con un insulto, pero falla el siguiente intento de apuñalar al esqueleto.',
     1061, 1110, 1092, [COY, NAOR, 'Leo', 'Colegio de Iktan', TRY, DEAD],
     'La amenaza de Coyote es una provocación, sin una escena de Leo cometiendo esos actos ni un programa de crianza que se ejecute. El efecto de la inspiración se presenta como adjudicación de mesa.')
fact(223, 'El combate cede y los viajeros se reagrupan', 'hecho_confirmado',
     'Después de otro turno de Tesara, deja de ver enemigos y el director dice que parece que han acabado con ellos. Una voz recuerda que falta uno, pero la escena pasa al reagrupamiento: Eldrath pregunta si todos están bien y vuelven las discusiones entre compañeros.',
     1111, 1129, 1118, [TESA, ELD, NAOR, COY, TRY, DEAD],
     'Se respeta la discrepancia sobre un posible enemigo restante. No se declara limpia toda la cueva ni destruida la totalidad de la hueste del dragón. Las cartas de emboscada que comenta el director no son fuerzas del mundo.')
fact(224, 'Las calaveras pasan de los enemigos a las disputas del grupo', 'hecho_confirmado',
     'Naór recoge restos del esqueleto y se los arroja a Coyote, usando el bono que había recibido contra él. Coyote interviene para forzar una nueva tirada y el lanzamiento falla. Tryel se divierte, pide a su hermano que no se acerque y le tira una calavera que lo golpea en la cara; Eldrath protesta por la nariz mientras ella bromea con que se trata de una pista.',
     1130, 1181, 1172, [NAOR, COY, TRY, ELD, DEAD],
     'La primera posibilidad de impacto queda corregida por la repetición de la tirada. No se establece una lesión permanente de Eldrath ni se atribuye la agresión de Tryel al control mental del dragón.')
fact(225, 'La supuesta despensa sigue siendo una interpretación', 'declaracion_personaje',
     'Eldrath observa la acumulación de huesos, cadáveres, pozas venenosas y musgo y propone que esa parte de la cueva sea la despensa del dragón. Si todos pueden continuar, quiere seguir avanzando.',
     1182, 1195, 1193, [ELD, DRAGON, CAVE],
     'La función de despensa es la hipótesis expresada por el personaje. No identifica a las víctimas ni confirma que el dragón viva o guarde su tesoro en esa sala.')
fact(226, 'Tesara atiende las heridas de Coyote antes de continuar', 'hecho_confirmado',
     'Tesara pregunta a Coyote si necesita atención. Se lo describe herido y con flechas; ella se detiene para darle primeros auxilios, aunque le advierte que no se emocione. Después le pide que se levante porque los compañeros los están dejando atrás.',
     1196, 1220, 1203, [TESA, COY],
     'La asistencia se narra sin un total final de puntos de vida ni una curación completa demostrada. La conversación sobre la hora anticipa la obligación de recoger a Leo.')
fact(227, 'Naór detecta un brillo mágico entre las rocas', 'hecho_confirmado',
     'En una sala repleta de hongos y plantas de colores, Tesara grita que no se acerquen. Naór usa su detección de magia: las plantas no aparecen mágicas, pero distingue un brillo especial entre una roca. Se aclara que solo ella ve ese brillo; los demás ven la piedra.',
     1221, 1280, 1242, [NAOR, TESA, CAVE],
     'La detección no identifica escuela, contenido, fabricante u origen de la magia. No se presenta el brillo como una señal visible para todo el grupo ni como poder mágico de las plantas.')
fact(228, 'Eldrath cae entre las plantas pero resiste el veneno', 'hecho_confirmado',
     'Eldrath intenta llegar a la roca balanceándose con la cadena de la kusarigama para no tocar las plantas. Falla las acrobacias y cae de culo entre ellas. Recuerda la antitoxina que había tomado y realiza con ventaja la salvación contra veneno, que supera. Consigue acercarse a la roca y pregunta a Naór dónde está el brillo.',
     1281, 1310, 1295, [ELD, NAOR, CAVE],
     'La ventaja y la resistencia corresponden a esta exposición; no se demuestra que la antitoxina cure toda condición anterior ni que conceda inmunidad.')
fact(229, 'Naór levanta la roca con Eldrath encima', 'hecho_confirmado',
     'Naór entra también entre las plantas, resiste el veneno y levanta la roca con Eldrath todavía encima. Él conserva el equilibrio mientras aparecen las botellas que estaban ocultas debajo y trata de recogerlas sin que ella suelte la piedra.',
     1311, 1343, 1330, [NAOR, ELD, CAVE, BOTTLES],
     'La pérdida de vida señalada en la interfaz se corrige como un problema de configuración; no se convierte en una herida narrativa por levantar la roca.')
fact(230, 'El hallazgo son tres botellas identificadas como antitoxinas', 'hecho_confirmado',
     'La investigación y las tiradas de botín resuelven el hallazgo de tres botellitas. Eldrath las reconoce como antitoxinas y dice que resultarán útiles contra el veneno de la cueva.',
     1344, 1357, 1355, [ELD, NAOR, BOTTLES, CAVE],
     'El reconocimiento automático pasa de «toxina» a la aclaración «antitoxinas» del personaje; no se inventa una cuarta botella ni una composición, fabricante o duración que no se describe.')
fact(231, 'Volver sobre los hombros de Naór tampoco evita el gas', 'hecho_confirmado',
     'Eldrath pide a Naór subir a sus hombros para regresar con las botellas. Ella acepta y camina hacia los demás; Tryel rechaza subirse también. El director recuerda que el peligro es gas y exige salvaciones a Naór y Eldrath, que ambos superan.',
     1358, 1390, 1389, [ELD, NAOR, TRY, BOTTLES, CAVE],
     'La altura no evita respirar la nube. No se adjudica a Tryel una caída en esta maniobra ni se deduce que haya bebido ya una de las botellas.')
fact(232, 'Eldrath reparte las antitoxinas a sus compañeros', 'hecho_confirmado',
     'Eldrath vuelve con los demás y reparte las tres pociones, comparándolas con la que él tomó antes. Recomienda tomarlas en ese momento porque le están ayudando a resistir los venenos. Tesara y Coyote habían esperado sentados a que acabara la búsqueda.',
     1391, 1448, 1441, [ELD, TESA, COY, NAOR, TRY, BOTTLES],
     'Se documenta el reparto sin una asignación nominal inequívoca de cada botella ni una confirmación individual de que todos las beban. Esperar sentados no equivale a un descanso corto reglado.')
fact(233, 'La recogida de Leo impide hacer un descanso corto', 'explicacion_director',
     'Coyote intenta recuperar un recurso mientras espera, pero el director recuerda que requiere un descanso corto. Eso consumiría una hora. Se descarta porque la persona encargada de recoger al niño no llegaría a tiempo; el grupo opta por continuar.',
     1422, 1440, 1434, [COY, NAOR, TESA, 'Leo', 'Colegio de Iktan'],
     'No se realiza el descanso, no se recuperan sus recursos y todavía no se representa la recogida de Leo. La conversación no formaliza una custodia ni acredita qué personaje acabará cumpliendo la obligación.')
fact(234, 'Un puente roto atraviesa el barrizal de veneno', 'explicacion_director',
     'Naór alcanza una zona con un enorme barrizal venenoso cruzado por un puente de piedra parcialmente destruido. El director muestra conexiones derrumbadas: antes habría varios caminos entre los tramos, pero solo queda uno disponible.',
     1449, 1475, 1453, [NAOR, CAVE],
     'La disposición procede de los señalamientos del tablero. No se adjudica una antigüedad, autoría o causa al derrumbe ni se considera agua potable el barrizal.')
fact(235, 'Naór avanza saltando de roca en roca', 'hecho_confirmado',
     'Naór se lanza a saltar antes de que termine el aviso sobre el veneno. Supera las tiradas y pasa por tres piedras sucesivas. Tesara llega dando la vuelta mientras Eldrath llama a Tryel y Coyote para que se acerquen.',
     1476, 1499, 1493, [NAOR, TESA, ELD, TRY, COY, CAVE],
     'Los saltos narrados no prueban que todos usen exactamente la misma ruta ni reconstruyen toda la geometría del puente.')
fact(236, 'Tryel cae al veneno y Naór se mete para ayudarla', 'hecho_confirmado',
     'Tryel intenta alcanzar el siguiente tramo corriendo, no llega y cae al líquido venenoso. Nada hasta una piedra y queda envenenada. Naór se arroja al verla caer, la pone encima de sí como una balsa y la ayuda a subir; también recibe el veneno.',
     1500, 1519, 1515, [TRY, NAOR, CAVE],
     'La escena no da por ahogada a Tryel ni muestra una salvación fallada de todas las personas presentes. El que los subtítulos alternen géneros no altera que Tryel y Naór sean mujeres.')
fact(237, 'Tryel escupe el veneno y responde que está bien', 'hecho_confirmado',
     'Tras alcanzar la roca, preguntan a Tryel si está bien y le dan golpecitos para que escupa. Tose sobre quien la ayuda y responde que sí; se queja del agua y los compañeros le recuerdan que es veneno. La discusión vuelve al riesgo de tocar plantas durante la persecución de un esqueleto.',
     1520, 1537, 1528, [TRY, NAOR, TESA, CAVE],
     'La respuesta de Tryel no elimina automáticamente la condición de envenenada ni acredita recuperación completa. «Mirien/Mirien» se trata como una variante de transcripción en una interpelación a Tryel, sin crear otro personaje.')
fact(238, 'Tesara pide prudencia mientras se acaba el tiempo', 'declaracion_personaje',
     'Tesara pide que se comporten como adultos y no toquen nada verde ni que huela mal. Anuncia que se irá en veinte minutos. Eldrath suspira y expresa sus dudas sobre que el grupo salga bien de allí.',
     1538, 1549, 1546, [TESA, ELD, NAOR, COY, TRY, CAVE],
     'El límite es lo que anuncia Tesara; no se representa todavía su partida. El pesimismo de Eldrath no es un desenlace ni un augurio confirmado.')
fact(239, 'Eldrath intenta prevenir otra emboscada en la siguiente sala', 'hecho_confirmado',
     'Antes de que crucen a la siguiente sala, Eldrath detiene al grupo con una mano y pide examinarla, recordando trampas y emboscadas anteriores. El director vuelve a describir pozas, raíces que cubren el suelo y montones de huesos.',
     1550, 1565, 1557, [ELD, CAVE],
     'La descripción termina con los huesos y no resuelve por sí misma si la sala contiene una trampa o nuevos enemigos. No se extrapola una limpieza de la cueva o el encuentro con el dragón.')


def refs(*numbers):
    return [f'48-{n}' for n in numbers]


stages = [
    {'titulo': 'El gas también alcanza el techo',
     'texto': 'Con las antorchas encendidas, los viajeros se internan en una cueva donde las raíces atraviesan hasta la roca y el musgo rodea pequeñas pozas venenosas. Tesara lleva pistola y luz, pendiente de no acercarse al líquido. Eldrath estudia unos capullos que rezuman veneno y comprende que pueden abrirse para expulsarlo en forma de nube. Prueba a contener una descarga bajo su capa y sale indemne de ese primer acercamiento, pero los intentos siguientes acaban exponiendo a los compañeros al gas. Las pullas sobre quién debe dar las ideas tensan la marcha. Tesara propone descolgar las raíces con el látigo y cruzar agarrados por arriba; el director aclara que siguen demasiado cerca de las plantas y deben resistir el veneno. Eldrath encuentra por fin un procedimiento útil: la daga psíquica no altera la cápsula, pero el filo de la kusarigama la corta, libera su nube y la deja muerta. Continúa podando para no repetir el peligro a la vuelta.',
     'referencias': refs(201,202,203,204,205,206)},
    {'titulo': 'La calavera y las flechas de la retaguardia',
     'texto': 'El paso desemboca en una sala de ambiente verdoso, con más pozas, musgo y restos humanos. Tesara teme que los cadáveres se alcen como los enemigos que ya conocen; el grupo recuerda el poder de resucitarlos que atribuye al dragón. Naór insiste en buscar pistas y termina enviando una calavera de una patada hacia el fondo. No sucede nada visible al principio. Después, cuando distinguen otra sala al sur, llegan ruidos desde atrás. Tesara le reprocha haber tocado los muertos y mantiene la mirada en esa dirección mientras se desplaza con la mano en la pistola. Tryel sigue a los demás sin comprender de inmediato el peligro. Una figura se incorpora y dispara una flecha venenosa. Tesara desenfunda y grita que vigilen el suelo. No ven al dragón animar los restos: deben ocuparse de los atacantes que ya tienen encima.',
     'referencias': refs(207,208,209,210,211)},
    {'titulo': 'Pelear rodeados y envenenados',
     'texto': 'Eldrath rompe la última cápsula del paso mientras Tesara intenta disparar lastrada por el veneno y la distancia. Tryel señala un enemigo y pide a Naór que la lance: la leonina activa su furia y la arroja hacia él, aunque la elfa falla el golpe al llegar. Se levantan más esqueletos y zombis por distintos flancos. Tryel soporta golpes y flechas; Coyote pelea con sus cuchillos y recibe proyectiles envenenados. Tesara se aparta en busca de cobertura, pero ocultarse entre setas y plantas solo la expone a nuevas nubes. Eldrath se suma a los ataques. Naór ruge, descarga el efecto necrótico de su furia y encadena golpes que derriban a varios rivales, aunque algunos resisten sus salvaciones. Coyote bebe un frasco comprado antes y usa recursos que dificultan los ataques enemigos; también consulta la capacidad de producir un dinosaurio espiritual desde su fruta, pero aplaza la invocación. Tryel remata a un esqueleto y luego a otro adversario. Tesara consigue avanzar hasta tener alcance y disparar; la carga de fuego ya está consumida y el veneno impide añadir el ataque furtivo. Eldrath cambia de objetivos para ayudar a Coyote y a su hermana, y después se aproxima a Tesara. La pelea va cediendo, sin que puedan considerar segura toda la cueva.',
     'referencias': refs(211,212,213,214,215,216,217,218,219,220,221,223)},
    {'titulo': 'Las bromas sobreviven al combate',
     'texto': 'La tentativa de Coyote de inspirar a Naór toma una dirección peligrosa: la provoca prometiendo malcriar a Leo y el resultado le da a ella un bono contra el propio Coyote. Cuando los ataques aflojan y Eldrath pregunta si siguen enteros, Naór le arroja restos de un esqueleto al provocador. Coyote consigue forzar otra tirada y el proyectil falla. Tryel se ríe de la escena y golpea en la cara a su hermano con una calavera, presentándola como otra pista. Eldrath protesta por la nariz, observa la acumulación de huesos y propone que se trate de la despensa del dragón. Es una conjetura que no identifica a las víctimas ni prueba dónde se encuentra el dueño. Tesara se detiene con Coyote, que sigue herido y con flechas, para darle primeros auxilios; después le pide que se ponga en pie porque el resto ya avanza.',
     'referencias': refs(222,223,224,225,226)},
    {'titulo': 'Tres botellas bajo una roca',
     'texto': 'La siguiente cámara está llena de hongos y plantas de colores. Tesara vuelve a advertir que no se acerquen, pero Naór detecta un brillo mágico entre una roca. Las plantas no aparecen mágicas y los demás no ven el resplandor que ella distingue. Eldrath intenta llegar balanceándose con la cadena de la kusarigama, cae entre la vegetación y tiene que resistir el veneno. La antitoxina que había tomado le permite tirar con ventaja y supera la exposición. Naór entra también, aguanta la nube y levanta la roca con el elfo todavía haciendo equilibrio encima. Debajo hay tres botellitas. Eldrath las recoge e identifica como antitoxinas. Para volver pide subir a los hombros de Naór; ni esa altura los libra de otra salvación, aunque ambos resisten. Ya con sus compañeros, reparte las pociones y recomienda usarlas porque a él le están ayudando.',
     'referencias': refs(227,228,229,230,231,232)},
    {'titulo': 'No queda una hora para descansar',
     'texto': 'Tesara y Coyote han esperado sentados mientras se recuperaban las botellas, pero esa pausa no cuenta como descanso corto. Coyote intenta recuperar un recurso y el director recuerda que necesitaría una hora entera. La conversación vuelve a Leo: si se detienen tanto, no llegarán a recoger al niño. Descartan el descanso y conservan sus recursos tal como están. Las tres antitoxinas ofrecen una ayuda inmediata para seguir, sin que se detalle quién bebe cada una.',
     'referencias': refs(232,233)},
    {'titulo': 'El puente sobre el barrizal',
     'texto': 'Naór encuentra un barrizal enorme de veneno y los restos de varios puentes de piedra. Las conexiones están rotas y solo parece quedar un camino. Salta antes de que termine el aviso y consigue enlazar varias piedras. Tesara alcanza la zona dando la vuelta y llaman a Tryel y Coyote. La elfa trata de cruzar corriendo, no llega y cae al líquido. Nada hacia una roca, envenenada. Naór se arroja tras ella, la sostiene encima de sí como una balsa y la ayuda a salir, pero recibe también el veneno. Tryel tose sobre quien la auxilia y contesta que está bien; cuando se queja del agua, le recuerdan que no era agua. Tesara reclama por fin que se comporten como adultos y dejen de tocar lo verde o maloliente: anuncia que en veinte minutos se irá. Eldrath teme que ninguno salga bien de allí y detiene al grupo antes de otra sala para examinar posibles trampas o emboscadas. Por delante vuelven a ver pozas, raíces y montones de huesos.',
     'referencias': refs(234,235,236,237,238,239)},
]

histories = []


def history(name, kind, description, note, new, entries):
    histories.append({'nombre': name, 'tipo': kind, 'descripcion': description, 'nota': note,
                      'nueva': new, 'etapas': [{'titulo': t, 'texto': text, 'referencias': refs(*r)} for t,text,r in entries]})


history(ELD,'personaje','Elfo hermano de Tryel que combate con dagas psíquicas y una kusarigama.',
        'Eldrath no es Aerendriel. La grafía canónica se conserva frente a Eldrat/Eldra del VTT.',False,[
        ('Podar el camino y volver con ayuda','Eldrath intenta contener las plantas venenosas bajo la capa y discute con los demás sobre cómo cruzar. La daga psíquica no sirve contra las cápsulas; cambia al filo de la kusarigama y las va cortando para despejar el regreso. Cuando termina, se incorpora a la lucha y alterna objetivos para ayudar a Coyote y a Tryel. Tras el combate se preocupa por los compañeros y recibe de su hermana una calavera en la cara entre bromas.',[202,203,206,211,215,221,223,224]),
        ('La roca, las botellas y la siguiente sala','Sigue la indicación mágica de Naór e intenta balancearse hasta una roca. Cae entre las plantas, pero resiste gracias a la antitoxina. Mientras Naór sostiene la roca recoge tres frascos y los identifica como nuevas antitoxinas; vuelve a hombros de ella y los reparte al grupo. El gas obliga a otra salvación incluso a esa altura. Después de las caídas del puente, intenta detener a los compañeros antes de otra sala para prevenir una emboscada.',[227,228,229,230,231,232,239])])
history(TRY,'personaje','Elfa hermana de Eldrath, compañera de la exploración de la cueva.',
        'Mantener Tryel; las interpelaciones transcritas como Mirien/Mirien no crean otra identidad.',False,[
        ('Lanzada entre los no muertos','Tryel sigue al grupo y tarda en advertir el ataque desde atrás. Cuando empieza la lucha pide a Naór que la lance contra los enemigos. El golpe al llegar falla, pero permanece en primera línea pese al veneno y los disparos. Acaba con un esqueleto y con otro rival al corregirse el daño pendiente. Recuperada la calma, lanza una calavera a Eldrath y se ríe de su queja por la nariz.',[210,212,213,218,220,224]),
        ('El salto que termina en el veneno','Rechaza subir también a los hombros de Naór durante la recuperación de las botellas. Más adelante intenta cruzar el barrizal corriendo, se queda corta y cae al veneno. Llega nadando a una piedra y Naór entra para ayudarla a subir. Tryel tose y dice que está bien, sin que eso quite por sí solo el envenenamiento.',[231,236,237])])
history(NAOR,'personaje','Princesa leonina de Atlan y madre adoptiva de Leo.',
        'Naór y Tryel son mujeres. No se añade una nueva hazaña de Leo a partir de las provocaciones de Coyote.',False,[
        ('Furia entre los esqueletos','Naór insiste en buscar pistas y patea una calavera, sin que la secuencia pruebe que eso anime a los muertos. Durante la pelea lanza a Tryel al frente, ruge y golpea a los enemigos con el efecto necrótico de su furia y sus ataques. La inspiración provocadora de Coyote termina volviéndose contra él: Naór le arroja unos restos, aunque la repetición de la tirada hace que fallen.',[209,212,216,221,222,224]),
        ('Detectar, cargar y rescatar','La detección de Naór localiza un brillo que los demás no ven debajo de una roca. Aguanta el gas, levanta la piedra con Eldrath encima y lo transporta de regreso después de que recupere tres antitoxinas. Ante el barrizal salta varias piedras, pero cuando Tryel cae entra tras ella, la sostiene y la ayuda a subir; también queda expuesta al veneno.',[227,229,230,231,234,235,236,237])])
history(TESA,'personaje','Historiadora humana que explora la cueva con los elfos, Naór y Coyote.',
        'El plazo de veinte minutos y la recogida de Leo son compromisos expresados, todavía sin escena de cumplimiento.',False,[
        ('La cautela también necesita un sitio donde esconderse','Tesara entra con antorcha y pistola y propone cruzar el paso de plantas colgados de las raíces que baja con el látigo. El gas llega hasta esa altura. Desconfía de los montones de cadáveres y vigila los ruidos por la retaguardia, donde empieza el ataque. Lucha con la pistola y busca coberturas, pero las setas y plantas que escoge la exponen a nuevas salvaciones de veneno. Cuando consigue un disparo útil, la carga de fuego ya se ha gastado y la desventaja limita su ataque furtivo.',[201,205,207,210,211,214,218,220]),
        ('Auxilio y tiempo para el regreso','Se ocupa de las heridas de Coyote y le pide levantarse para seguir al grupo. Espera mientras Naór y Eldrath recuperan las antitoxinas. El descanso corto queda descartado por la recogida de Leo. Tras alcanzar el puente por otra ruta y presenciar otra exposición al veneno, pide a los compañeros que no toquen nada sospechoso y anuncia que se irá en veinte minutos.',[226,232,233,235,237,238])])
history(COY,'personaje','Cambiaformas de Iktan que acompaña la exploración y combate con cuchillos y recursos de bardo.',
        'No es Citlali ni Ione. La identidad anterior y las razones de sus suplantaciones no se explican.',False,[
        ('Flechas, cuchillos y una inspiración inoportuna','Coyote combate con sus dagas y recibe flechas envenenadas. Bebe un frasco comprado antes, cuyo contenido no queda inequívocamente explicado, y usa recursos para alterar ataques y ayudar a sus compañeros. Consulta una capacidad que podría invocar un dinosaurio espiritual, pero no la materializa. Su intento de inspirar a Naór mediante una burla sobre Leo le da a ella un bono contra él; evita que lo alcance el esqueleto que le arroja forzando otra tirada. Tesara le da primeros auxilios antes de avanzar.',[213,214,217,218,219,222,224,226]),
        ('Una pausa que no recupera los recursos','Espera sentado mientras Eldrath y Naór buscan las botellas. Al intentar recuperar un recurso, el director explica que necesita una hora de descanso corto. El grupo descarta esa demora para no fallar a la recogida de Leo.',[232,233])])
history(CAVE,'lugar','Caverna de raíces, musgo, pozas venenosas, hongos y pasos de piedra deteriorados.',
        'Nombre editorial acordado con coordinación. No se identifica por parecido con el claro envenenado, las ruinas del lago, la cueva de Cuicapalli o una guarida anterior de Clolgedranx.',True,[
        ('Cápsulas que cierran el paso','Las raíces atraviesan suelo y paredes de roca, alrededor de charcas de veneno. Unas plantas con capullos expelen nubes tóxicas que alcanzan incluso a quienes intentan cruzar por encima. La capa de Eldrath ayuda en algunos acercamientos; el filo de su kusarigama permite cortar las cápsulas y abrir camino.',[201,202,203,204,205,206]),
        ('La cámara de los muertos','Un ambiente verdoso rodea los montones de huesos y cadáveres. Tras los primeros ruidos se levantan arqueros esqueléticos y zombis, que rodean a los exploradores. El combate remite y Eldrath propone que sea la despensa del dragón, una interpretación que no identifica al dueño ni a las víctimas.',[207,209,210,213,223,225]),
        ('Ayuda bajo la piedra y peligro en los puentes','En otra cámara, Naór detecta un brillo mágico bajo una roca, mientras las plantas no aparecen mágicas. El grupo recupera tres botellas identificadas como antitoxinas. Más adelante encuentran un enorme barrizal de veneno y puentes derrumbados; Tryel cae durante el cruce y Naór se sumerge para ayudarla. Al otro lado siguen las raíces, pozas y huesos.',[227,228,229,230,231,234,235,236,237,239])])
history(DEAD,'personaje','Colectivo de esqueletos arqueros y zombis que se levantan en la cueva envenenada.',
        'Entidad descriptiva de los adversarios observados; no es una facción ni se fusiona con cadáveres de otros lugares. El controlador y las identidades en vida no se acreditan aquí.',True,[
        ('Se levantan por la retaguardia y los flancos','Un ruido avisa del movimiento de los restos. Un arquero se levanta y lanza una flecha venenosa; otros esqueletos y zombis aparecen por distintos lados y atacan a la expedición. Tryel y Coyote reciben especial presión, mientras Tesara trata de mantenerse a distancia. Eldrath acaba de podar el paso y se une a los golpes de Naór y los demás.',[210,211,212,213,214,215,216,217,218]),
        ('Los restos quedan para las bromas','Tryel y Naór abaten adversarios y los compañeros reducen a quienes siguen atacando. El director habla de que parecen haber terminado, aunque otra voz recuerda uno restante. La narración pasa al reagrupamiento: Naór arroja unos restos a Coyote y Tryel golpea a Eldrath con una calavera. Eso no confirma la eliminación de todos los muertos de la cueva.',[216,220,221,223,224])])
history(BOTTLES,'objeto','Tres botellitas recuperadas bajo una roca e identificadas como antitoxinas.',
        'Lote descriptivo de este hallazgo, separado de las pociones compradas previamente, el remedio de Eromov y los viales de otros lugares. No se identifican fabricante o duración.',True,[
        ('El brillo y las manos que las recuperan','La detección de Naór revela magia bajo una roca. Tras resistir el gas, ella la levanta con Eldrath encima y él recoge las tres botellas. Las reconoce como antitoxinas, vuelve a hombros de Naór y las reparte a sus compañeros, recomendando usarlas por la ayuda que a él le está dando una poción anterior. No queda un reparto nominal inequívoco de cada frasco.',[227,229,230,231,232])])
history('Escupefuego','objeto','Pistola de Tesara con una carga de fuego utilizada en sus combates.',
        'La continuidad corresponde a la pistola de Tesara; no se fijan cargas máximas ni propiedades nuevas.',False,[
        ('Un disparo limitado por el veneno','Tesara se mueve hasta obtener alcance y dispara durante la pelea de la cueva. Se aclara que ya ha gastado la carga de fuego y que el envenenamiento impide añadir ataque furtivo. El comentario no acredita una nueva recarga o una debilidad general de los no muertos al fuego.',[211,220])])

questions = [
    {'pregunta':'¿Quién anima y controla a los no muertos de esta cueva?', 'respuesta':'Se levantan y atacan esqueletos y zombis. Los viajeros relacionan el peligro con el dragón, pero aquí no se muestra la animación ejecutada por él ni se identifica otro controlador.', 'referencias':refs(208,209,210,213),'pendiente':'Identificar al controlador y el mecanismo; no deducirlo de la patada de Naór.'},
    {'pregunta':'¿Es esta cueva la guarida de Clolgedranx o su despensa?', 'respuesta':'Eldrath propone que la sala de cadáveres sea su despensa. Se trata de una hipótesis; no aparece el dragón ni se establece aquí la función completa del lugar.', 'referencias':refs(225,239),'pendiente':'Confirmar la identidad y el uso del lugar al integrar el resto de la exploración.'},
    {'pregunta':'¿Qué hacen las tres botellas halladas y quién las toma?', 'respuesta':'Eldrath las identifica como antitoxinas y las reparte, comparándolas con la que ya le ayuda a superar salvaciones. No se describe inequívocamente a cada destinatario bebiendo una.', 'referencias':refs(228,230,231,232),'pendiente':'Precisar el reparto y los usos individuales si aparecen después.'},
    {'pregunta':'¿Podrán completar la exploración y volver a recoger a Leo?', 'respuesta':'Rechazan un descanso corto para no perder una hora y Tesara anuncia que se irá en veinte minutos. El regreso y la recogida todavía no se representan.', 'referencias':refs(226,233,238),'pendiente':'Comprobar el regreso y la recogida del niño.'},
    {'pregunta':'¿Ha terminado el peligro al acabar el combate de la sala de huesos?', 'respuesta':'El director dice que parecen haber terminado y una voz recuerda un rival restante. La escena pasa a las curas y las siguientes salas conservan veneno, raíces y huesos.', 'referencias':refs(223,226,234,236,239),'pendiente':'Verificar los nuevos riesgos y la salida de la cueva.'},
]

observations = {
 'P14-005': ('Eldrath actúa, combate y resiste venenos, sin atribuirle una marca o maldición nueva causada por la moneda negra del mercante.', [], 'sin_cambio'),
 'P14-007': ('Eldrath y Tryel exploran y se ayudan entre hermanos, sin relatar su lugar de origen o el episodio de las dríadas.', [], 'sin_cambio'),
 'P15-006': ('El dragón mencionado como posible dueño de la cueva no se identifica con Zarynth. No se reconstruye la antigua pronunciación Tarin/Zari.', [], 'sin_cambio'),
 'P16-008': ('Las plantas tóxicas de la cueva y las tres antitoxinas no se identifican con las plantas fucsias del encargo del kenku o los tubos de Lunaria.', refs(202,230), 'sin_cambio'),
 'P21-004': ('La urgencia de recoger a Leo y la burla de Coyote muestran que sigue siendo una obligación del grupo; no hay decisión de Eromov, custodia formal o evaluación de secuelas.', refs(222,233,238), 'sin_cambio'),
 'P24-004': ('Coyote combate y conversa como persona distinta, sin relatar una identidad anterior ni equipararse a Citlali.', [], 'sin_cambio'),
 'P26-004': ('Las acciones presentes de Coyote no explican por qué suplantó a Ione ni revelan el informe de Poncelot.', [], 'sin_cambio'),
 'P29-004': ('La provocación de Coyote sobre Leo es una amenaza de broma actual; no identifica a la familia ni al sacrificio que Maris mencionó antes.', refs(222), 'sin_cambio'),
 'P30-001': ('Las tres antitoxinas se recuperan en otra cueva y se reparten entre la expedición; no se administran a Eromov ni informan de su recuperación.', refs(230,232), 'sin_cambio'),
 'P30-005': ('Los no muertos de esta cueva no se identifican con hombres serpiente ni demuestran alianzas o jerarquías de esos grupos.', refs(210,213), 'sin_cambio'),
 'P31-001': ('Se conserva Clolgedranx como identidad canónica por los antecedentes; esta exploración no altera la respuesta sobre su nombre y las ruinas de Iktan.', [], 'sin_cambio'),
 'P31-002': ('Se observan nuevos cadáveres que se levantan y atacan, y los viajeros recuerdan que el dragón puede resucitarlos. No se muestra al controlador actuando, una intrusión mental nueva o una neutralización permanente de su influencia.', refs(208,210,213,223), 'sin_cambio'),
 'P31-006': ('Tryel recibe daño y actúa en combate, sin una explicación del efecto de su tatuaje.', [], 'sin_cambio'),
}
cotejo = []
for q in Q:
    observation, references, result = observations.get(q['id'], (
        'La lectura completa de 01:06:36.559–02:16:45.990 no retoma el asunto concreto de esta pregunta. No se extrapola una respuesta desde semejanzas de personas, lugares, venenos u objetos.', [], 'sin_cambio'))
    cotejo.append({
        'id':q['id'],'sha256_pregunta':q['sha256_pregunta'],'pregunta':q['pregunta'],
        'estado_previo':q['estado'],'resultado':result,'observacion':observation,
        'referencias':references,'estado_propuesto':q['estado'],'pendiente':q.get('pendiente',''),
    })

output = {
    'bloque':2,'capitulo':48,'lectura_completa':True,'segmentos_leidos':1566,
    'primer_segmento':'c003131','ultimo_segmento':'c006263','fuente_sha256':EXPECTED,
    'cobertura_lectura':list(range(len(S))),
    'tandas_lectura':[{'desde':a,'hasta':b,'segmentos':b-a+1} for a,b in [(0,199),(200,399),(400,599),(600,799),(800,999),(1000,1199),(1200,1399),(1400,1565)]],
    'criterio':'Lectura completa secuencial del tramo, sin búsquedas como sustituto de lectura. Cotejo íntegro de 98 preguntas asignadas y del catálogo de 209 identidades. Ausencia de respuesta limitada a este tramo; el coordinador integra la sesión completa.',
    'etapas':stages,'afirmaciones':F,'historias_entidades':histories,
    'misiones':[
        'Abrir paso por las plantas venenosas: Eldrath poda las cápsulas con la kusarigama tras comprobar que las dagas psíquicas no las alteran (48-202–48-206).',
        'Sobrevivir a la emboscada de esqueletos y zombis: el combate cede y el grupo se reagrupa, sin acreditar la eliminación de todos los no muertos de la cueva (48-210–48-224).',
        'Recuperar la ayuda detectada bajo una roca: Naór y Eldrath consiguen tres botellas identificadas como antitoxinas y las reparten (48-227–48-232).',
        'Cruzar el barrizal venenoso: Naór supera los primeros saltos y ayuda a Tryel después de que caiga; ambas quedan expuestas al veneno (48-234–48-237).',
        'Regresar para recoger a Leo: se descarta una hora de descanso corto y Tesara anuncia que se irá en veinte minutos; el cumplimiento sigue pendiente en este tramo (48-233,48-238).',
        'Explorar la posible relación de la cueva con el dragón: Eldrath interpreta una sala como su despensa, sin encontrarlo ni confirmar aquí esa función (48-225,48-239).',
    ],
    'preguntas':questions,
    'contradicciones':[
        'En torno a 01:58 el director considera que parecen haber acabado con los enemigos y otra voz recuerda uno restante. Se narra el reagrupamiento sin declarar eliminada toda la cueva (48-223).',
        'La primera resolución del lanzamiento de Naór contra Coyote se repite y falla; no conservar el impacto previsto antes de esa corrección (48-224).',
        'El botín se reconoce primero como «toxina» en los subtítulos y se aclara de inmediato como antitoxinas. Se conserva el hallazgo de tres botellas, sin fijar una composición externa (48-230).',
        'Subirse a los hombros, colgarse de raíces o usar una capa no produce inmunidad universal al gas; cada exposición se resuelve mediante las salvaciones descritas (48-203–48-205,48-228–48-231).',
        'Cartas de ayuda y emboscada, tiradas, alcance, errores de configuración y chistes sobre suicidarse se mantienen separados de los hechos del mundo.',
    ],
    'nombres_dudosos':[
        '«Eldrat», «Eldra», «el drat» se normalizan como Eldrath según el catálogo vigente; nunca Aerendriel.',
        '«Triel», «Trier», «Triet» y la interpelación «Mirien» junto al rescate se mantienen dentro de la continuidad de Tryel, sin introducir otro personaje.',
        '«Naor», «Nahor» y variantes se normalizan como Naór. Su género femenino y su condición de madre adoptiva de Leo no cambian por la alternancia automática de los subtítulos.',
        '«Tesa» y «Tesa/Tesa» se normalizan como Tesara Queen; no se introduce otra historiadora.',
        'La cueva carece de topónimo pronunciado en este tramo. Las etiquetas descriptivas se coordinan con el resto de la sesión antes de integrar el catálogo.',
    ],
    'cotejo_preguntas_asignadas':cotejo,
    'verificacion':{'afirmaciones_validadas':len(F),'validate_fact':'scripts/construir.py:validate_fact','preguntas_cotejadas':len(cotejo),'hash_original_intacto':True},
}
assert len(S) == 1566 and len(Q) == len(cotejo) == 98
assert all(hashlib.sha256(q['pregunta'].encode('utf-8')).hexdigest() == q['sha256_pregunta'] for q in Q)
ids = {f['id'] for f in F}
for stage in stages:
    assert set(stage['referencias']) <= ids
tagged = {n for f in F for n in f['entidades']}
for h in histories:
    assert h['nombre'] in tagged
    for stage in h['etapas']:
        assert set(stage['referencias']) <= ids
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
(HERE / 'entrega_2.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines = ['# Lectura íntegra del capítulo 48: bloque 2','',
         'Fuente original: `48 - FYarBX28XfI.es-orig.vtt`.',
         f'SHA-256 verificado antes y después: `{EXPECTED}`.','',
         'Leídos completos los 1566 segmentos, 01:06:36.559–02:16:45.990, desde c003131 hasta c006263. Índices locales de base cero.','',
         '| Tanda | Índices completos | Primer cue | Último cue |',
         '| --- | --- | --- | --- |']
for i,(a,b) in enumerate([(0,199),(200,399),(400,599),(600,799),(800,999),(1000,1199),(1200,1399),(1400,1565)],1):
    lines.append(f'| {i} | {a}–{b} | {S[a]["id"]} | {S[b]["id"]} |')
lines += ['', 'Se leyeron además las 98 preguntas completas asignadas, sus respuestas previas, estados y referencias; los 209 grupos de identidades del contexto; y las historias vigentes pertinentes de Eldrath, Tryel, Naór, Coyote, Tesara Queen, Clolgedranx, Colegio de Iktan y Escupefuego.', '',
          'Entrega: 39 afirmaciones con evidencia literal validada, siete etapas narrativas, nueve historias de entidad y 98 resultados de cotejo. No se altera ningún estado previo solo por ausencia de novedades en este tramo.', '',
          'La etiqueta de la cueva y la de sus no muertos se han acordado con el coordinador. Las antitoxinas son un lote nuevo del hallazgo, separado de todas las pociones anteriores. La declaración sobre la despensa conserva atribución a Eldrath; las cartas del chat y las bromas no se convierten en lore.', '',
          'La exploración continúa después de los montones de huesos de la siguiente sala. No se afirma una victoria sobre el dragón, una recogida de Leo realizada ni una limpieza total de la cueva.']
(HERE / 'lectura_bloque_2.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f'{len(F)} afirmaciones validadas; {len(histories)} historias; {len(stages)} etapas; {len(cotejo)} preguntas. SHA-256 intacto.')
