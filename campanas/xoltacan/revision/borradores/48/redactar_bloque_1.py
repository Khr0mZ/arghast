"""Entrega editorial local de la lectura completa del primer tercio del capítulo 48."""
import hashlib
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import validate_fact

SEG = json.loads((BASE / 'bloque_1_segmentos.json').read_text(encoding='utf-8'))
PREG = json.loads((BASE / 'preguntas_bloque_1.json').read_text(encoding='utf-8'))
CAT = json.loads((BASE / 'identidades_contexto.json').read_text(encoding='utf-8'))
SOURCE = ROOT / 'campanas/xoltacan/fuentes/48 - FYarBX28XfI.es-orig.vtt'
EXPECTED = '1fe4de4381f91a2e084979a969a5ac43d91a6c000b0d4379ed3755907844383d'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED

F = []
def fact(n, title, a, b, cue, text, entities, kind='hecho_confirmado', limit=''):
    s = SEG[cue - 1]
    assert a <= cue <= b
    F.append(dict(id=f'48-{n}', titulo=title, tipo=kind, afirmacion=text,
        inicio=SEG[a-1]['inicio'], fin=SEG[b-1]['fin'], cita=s['texto_original'],
        evidencia_cue=dict(inicio=s['inicio'], fin=s['fin'], texto=s['texto_original']),
        entidades=entities, ambito='preparativos en Iktan y expedición a la cueva envenenada',
        conocedores=[], conocimiento_personaje='desconocido',
        nota_conocimiento='No se establece el acceso de Madame Oghma a estos sucesos. Los interlocutores y participantes se identifican en la afirmación sin extender su conocimiento a ausentes.',
        confianza='lectura íntegra de subtítulos automáticos; audio no cotejado', limitacion=limit))

fact(101, 'Naór recuerda el colegio y sus nuevos encuentros', 5, 26, 14,
    'En el repaso inicial, la jugadora de Naór recuerda que conoció a Citlali al salir del colegio de Leo y Eztli: hubo un desencuentro, pero comprobaron que los pequeños jugaban juntos. También recuerda haber ido a entrenar con el interlocutor transcrito como Ilicar y Lilicar; dice que lo dejó inconsciente y que después ella acabó inconsciente en un combate con Tortas.',
    ['Naór', 'Citlali', 'Leo', 'Eztli', 'Tortas', 'Colegio de Iktan'], 'declaracion_personaje',
    'Recapitulación de acontecimientos anteriores, sin volver a representar los encuentros. La identificación del nombre Ilicar/Lilicar con Ilikar es compatible con el catálogo, pero no se utiliza este repaso para fijar una nueva identidad ni las circunstancias de cada pérdida de conocimiento.')
fact(102, 'Eldrath recuerda por qué teme por su hermana', 28, 48, 39,
    'El jugador de Eldrath recuerda sus conversaciones personales con Tesara y explica que ella le contó la amenaza del dragón verde. La posibilidad de que invada la aldea con no muertos preocupa al elfo tanto por sí mismo como por su hermana.',
    ['Eldrath', 'Tryel', 'Tesara Queen', 'Clolgedranx', 'Iktan'], 'declaracion_personaje',
    'Repaso del jugador y temor del personaje; no hay invasión ejecutada ni ataque nuevo durante este recuerdo.')
fact(103, 'Tesara dedica su tiempo a los archivos de Walulu', 54, 84, 71,
    'Tesara recuerda que, tras el encuentro con el dragón y después de informar a Eldrath, trató de organizar a la gente para prevenir el peligro. Ha pasado tiempo en el templo con Walulu leyendo libros, documentos y profecías de su biblioteca en busca de información sobre el dragón, los rituales y los no muertos.',
    ['Tesara Queen', 'Eldrath', 'Walulu', 'Clolgedranx', 'Iktan'], 'declaracion_personaje',
    'Se relata la actividad de investigación entre escenas; no se identifica individualmente cada documento ni se acredita un descubrimiento concreto hasta la explicación posterior del director.')
fact(104, 'Coyote presenta su descanso en la taberna', 85, 95, 94,
    'Coyote dice haberse dedicado a estar tranquilo. Recuerda ver juntos a un elfo y una mujer de pelo azul, observar conversaciones de otros compañeros y marcharse a beber.',
    ['Coyote'], 'declaracion_personaje',
    'Su interpretación de la cercanía de los otros no demuestra una relación amorosa; el descanso es un repaso, no una misión completada.')
fact(105, 'Tesara llega cargada de libros a El Huevo Emplumado', 137, 173, 155,
    'La escena vuelve a Iktan y sigue a Tesara cargada de libros, informes y pergaminos después de estudiar en el templo. Busca primero a los hermanos elfos en la taberna y entra torpemente con las manos ocupadas. Allí están Eldrath, Tryel y Coyote, que toma cerveza y mira a la encargada felina.',
    ['Tesara Queen', 'Eldrath', 'Tryel', 'Coyote', 'Angelique', 'El Huevo Emplumado', 'Iktan'],
    limit='Tesara estima que pudo pasar un día o día y medio estudiando, sin fijar una duración exacta. La identidad del establecimiento y de su encargada se conserva por la continuidad de Iktan; no es la Sirena Borracha de Shiaru.')
fact(106, 'Eldrath sospecha de los clientes y Tryel mira a Molly', 174, 205, 178,
    'Eldrath vigila de reojo a una mesa de clientes que le parecen piratas de Shiaru y llama la atención de Tryel sobre ellos. Su hermana está distraída, tocándose el pelo y mirando a Molly. Tryel la considera amigable y propone acercarse; Eldrath le advierte que parece juntarse con los hombres de aquella mesa.',
    ['Eldrath', 'Tryel', 'Molly', 'Shiaru', 'El Huevo Emplumado'],
    limit='La procedencia, afiliación y participación de estos clientes en la ocupación de Shiaru son sospechas de Eldrath. La escena no identifica a la mesa con los ocupantes referidos por Patata ni convierte a Molly en miembro de esa facción.')
fact(107, 'Tesara pide adelantarse al golpe del dragón', 207, 247, 238,
    'Tesara deja su documentación en la barra e interrumpe a los presentes. Tras un intercambio sobre los saludos y la bebida de primera hora, explica que ha revisado lo que Walulu conserva sobre el dragón verde y quiere encontrarlo para golpear antes de que él actúe.',
    ['Tesara Queen', 'Walulu', 'Clolgedranx', 'Eldrath', 'Tryel', 'Coyote', 'El Huevo Emplumado'], 'declaracion_personaje',
    'Es la valoración urgente de Tesara y una propuesta de actuación; no se ha preparado todavía una trampa ni se ha descubierto una debilidad.')
fact(108, 'Los archivos sitúan al dragón joven antes de la fundación de Iktan', 260, 273, 266,
    'El director explica lo que Tesara ha podido averiguar en los archivos: el dragón verde llegó a la zona joven, incluso antes de que se fundara Iktan. Creció durante los años alimentándose de la jungla de Xoltacan y creando no muertos que le ayudaban a sobrevivir.',
    ['Tesara Queen', 'Clolgedranx', 'Iktan', 'Xoltacan'], 'explicacion_director',
    'Información histórica obtenida por Tesara, sin escena retrospectiva, fecha absoluta, edad exacta o mecanismo completo de creación de los no muertos. El nombre canónico enlaza con el dragón del que se habla, no con Zarynth.')
fact(109, 'El dragón dejó crecer los poblados como fuente de presas', 274, 282, 281,
    'Según la explicación histórica del director, el dragón no se interesaba en atacar las pequeñas ciudades que iban construyéndose. Las dejaba crecer, y quien se perdía en la jungla podía convertirse en alimento para él.',
    ['Clolgedranx', 'Iktan', 'Xoltacan', 'Tesara Queen'], 'explicacion_director',
    'No se identifica a víctimas concretas ni se afirma que nunca hubiera atacado una población en toda su existencia; se describe el comportamiento recogido en la información consultada.')
fact(110, 'Un ataque dracónico anterior motivó el ritual protector', 283, 290, 285,
    'El director relata que, unos cien o doscientos años antes según su estimación oral, un dragón destruyó parte de la ciudad. Sacerdotes y personas religiosas realizaron después un ritual para protegerla. Al explicar sus hallazgos a los compañeros, Tesara se refiere al ataque de otro dragón que destruyó media ciudad.',
    ['Tesara Queen', 'Iktan', 'Clolgedranx', 'Walulu'], 'explicacion_director',
    'El atacante histórico carece de nombre y color en este pasaje. La expresión posterior de Tesara «otro dragón» debe conservarse junto a la atribución y los ciento veinte años del relato de Walulu en 47-082; no se resuelve la tensión identificando o separando individuos por cuenta del editor.')
fact(111, 'Tesara conoce la función del rito, pero no comprende cómo se realiza', 290, 304, 294,
    'La investigación permite a Tesara saber que el ritual protege Iktan de la entrada de grandes dragones, pero el director aclara que no tiene suficiente capacidad mágica para comprender todo su funcionamiento. Sobre los no muertos movidos por plantas no revela en ese momento un secreto adicional: sigue tratándolos como muertos que se mueven.',
    ['Tesara Queen', 'Iktan', 'Clolgedranx'], 'explicacion_director',
    'No se entrega una fórmula reproducible ni ingredientes, duración, puntos de fallo o protección universal. La explicación no demuestra que el rito detenga a los no muertos; 47-083 había distinguido ambas amenazas.')
fact(112, 'Tesara transmite los hallazgos y habla de otro dragón al mando', 305, 347, 314,
    'Tesara cuenta a Eldrath, Tryel y Coyote la historia recuperada. Le preocupa que el dragón haya pasado de tolerar a los poblados a amenazar uno entero y afirma que parece trabajar para otro dragón. Recuerda después el ataque histórico de otro dragón, el ritual y la protección que ofrece. Los documentos disponibles le han aportado sobre todo cuentos, leyendas e historias de comportamiento, sin una debilidad explotable.',
    ['Tesara Queen', 'Eldrath', 'Tryel', 'Coyote', 'Clolgedranx', 'Iktan'], 'declaracion_personaje',
    'La identidad y naturaleza del empleador no se verifican. En 47-072 la criatura dijo que alguien pagaba por los elfos; esta afirmación de Tesara no demuestra por sí sola que ese alguien sea otro dragón. El atacante del pasado y el empleador actual tampoco quedan identificados entre sí.')
fact(113, 'El grupo dispone de seis días para responder al ultimátum', 348, 374, 361,
    'Los compañeros quieren descubrir más sobre el dragón antes de intentar matarlo o tenderle una trampa. Tesara concreta que dio una semana para que se entregaran los elfos, que ha pasado un día y que quedan seis. Reprocha a Coyote no haberlo escuchado y recuerda que ya había informado a Eldrath.',
    ['Tesara Queen', 'Eldrath', 'Tryel', 'Coyote', 'Clolgedranx', 'Iktan'], 'declaracion_personaje',
    'Es el plazo expresado por Tesara y el tiempo transcurrido que ella calcula. No se da una fecha de calendario ni se representa aún el cumplimiento o incumplimiento del ultimátum.')
fact(114, 'Tryel recuerda una gran cueva donde se envenenó', 375, 401, 389,
    'Eldrath pregunta a Tryel por el lugar donde se envenenó. Ella recuerda una gran cueva en la jungla que parecía la gruta del dragón. Eldrath propone prepararse e investigarla en busca de información con la que diseñar un plan o una trampa, pues considera que un enfrentamiento inmediato los mataría.',
    ['Eldrath', 'Tryel', 'Clolgedranx'], 'declaracion_personaje',
    'El recuerdo de Tryel enlaza con la cueva de la emboscada que ya relató en 40-030. Es una identificación aportada por ella, sin confirmar la propiedad del dragón; la visita sigue siendo un plan.')
fact(115, 'La falta de tiempo descarta buscar una gran biblioteca', 402, 441, 404,
    'Los compañeros recuerdan que el dragón tiene varias guaridas. Eldrath prefiere investigar la que encontró su hermana porque localizar otras llevaría más de una semana. Tesara propone obtener información en una gran ciudad con una biblioteca competente, pero no saben dónde hallarla y temen exponerse a una emboscada durante la búsqueda. Deciden hacer los preparativos y partir hacia la cueva recordada.',
    ['Eldrath', 'Tryel', 'Tesara Queen', 'Coyote', 'Clolgedranx', 'Iktan'], 'declaracion_personaje',
    'Las varias guaridas son un dato discutido por los personajes, coherente con el aviso de Walulu; no se localizan aquí varias a la vez. La existencia de una biblioteca adecuada permanece sin verificar.')
fact(116, 'Coyote carece de dinero para las pociones', 442, 459, 446,
    'Mientras se organizan las compras, Coyote calcula si puede pagar una poción y lamenta disponer de veinticinco monedas. Se propone acudir al alquimista, en lugar de pedir pociones a la encargada de la taberna.',
    ['Coyote', 'Iktan'], 'declaracion_personaje',
    'No se representa una compra de Coyote en este intercambio ni se identifica por nombre al alquimista; no se importa automáticamente a Froger a una escena donde no aparece nombrado.')
fact(117, 'Tryel reclama prioridad ante el interés de Coyote por Molly', 464, 489, 472,
    'Coyote se acerca a Tryel y comenta el atractivo de Molly. Tryel se le planta delante, le dice que ella la vio primero e intenta intimidarlo. Coyote responde con bromas, y la elfa le gruñe antes de moverse.',
    ['Coyote', 'Tryel', 'Molly', 'El Huevo Emplumado'],
    limit='Es interés y rivalidad expresados por Tryel y Coyote. Molly no responde ni consiente una relación en esta escena.')
fact(118, 'Naór recibe una clase de calma de una tortuga con gafas', 525, 553, 533,
    'El director sitúa a Naór en el templo junto a Walulu y una tortuga pequeña con gafas, sentada en una silla. La tortuga pregunta cómo se sintió al insultar a la señora Miaussy en el colegio y la reprende por hablar así a otras madres. Naór responde que estuvo mal y que debe comportarse como una madre.',
    ['Naór', 'Walulu', 'Miaussy', 'Colegio de Iktan', 'Tortuga terapeuta del templo de Iktan', 'Iktan'],
    limit='La introducción nombra a Naór y la continuidad de Leo identifica a la interlocutora aunque el ASR use después Leona. No se añade a Leona como participante. La tortuga no da nombre ni se identifica con Tortas. Se conserva Miaussy, grafía confirmada del catálogo, sin fusionar a Miausi, profesora registrada por separado.')
fact(119, 'Walulu insiste en los motivos para que Naór se calme', 554, 580, 562,
    'En la clase se recuerda a Naór que una madre no debe dejar a su hijo varios días con una desconocida sin pagarle. Walulu considera necesario que se calme y menciona sus saltos por las palmeras y al goliat que llevaron con la cabeza muy herida y tuvieron que arrastrar. Naór admite que fue culpa suya, aunque no era su intención.',
    ['Naór', 'Walulu', 'Leo', 'Tesara Queen', 'Tortuga terapeuta del templo de Iktan'], 'declaracion_personaje',
    'Los reproches sobre los cuidados y las heridas son relato de los interlocutores, sin reconstruir el incidente del goliat ni nombrarlo aquí. El contexto apunta a los cuidados de Tesara, que los confirma después; no fija una remuneración ya acordada o pagada.')
fact(120, 'La tortuga enseña a respirar y Walulu paga la donación', 581, 614, 586,
    'La tortuga hace callar a Walulu y guía las últimas respiraciones de Naór: inspirar, espirar y repetir que no tiene rabia ni se enfada. La llama una leona sin uñas. Al concluir acerca un recipiente y pide una donación para seguir dando las clases; Walulu deposita monedas y dice que irá pagando. Naór agradece la sesión y sale.',
    ['Naór', 'Walulu', 'Tortuga terapeuta del templo de Iktan'],
    limit='No se fija importe ni se acredita una curación definitiva, una pérdida física de uñas o un cambio mágico. La práctica respiratoria reaparece cuando Naór intenta dominar el enfado.')
fact(121, 'Tryel invita a Naór a pelear y recibe una respuesta pacífica', 615, 632, 631,
    'Al salir, Naór proyecta dar una vuelta y comprar la merienda. Encuentra a Tryel, que la invita a acompañarlos para golpear criaturas, despertar la rabia y pegar a todo el mundo. Naór responde que puede acompañarla si lo desea, pero sin violencia.',
    ['Naór', 'Tryel'], 'declaracion_personaje',
    'La declaración pacífica sigue a la clase; no garantiza que Naór no vuelva a usar violencia. La invitación no acredita enemigos nuevos encontrados o golpeados.')
fact(122, 'Tesara reclama a Naór por los tres días al cuidado de Leo', 633, 680, 661,
    'Tesara saluda con sarcasmo a Naór como madre del año y pregunta por Leo. Naór dice que el niño está en el colegio y que hablará con él si se comporta mal. Tesara le reprocha sus malas palabras con ella, la camarera y otros vecinos y afirma que lo ha cuidado tres días. Naór le pone la mano en el hombro y aprieta hasta que le piden que afloje, mientras conserva un trato exageradamente amable.',
    ['Tesara Queen', 'Naór', 'Leo', 'Angelique', 'Colegio de Iktan'],
    limit='Los tres días son declaración expresa de Tesara. Sus preguntas sobre fugas, puñaladas o arrancar pelo son provocaciones, no nuevos incidentes escolares comprobados. La caída de palmeras narrada durante el intercambio no identifica expresamente a su causante.')
fact(123, 'Naór acepta la expedición, condicionada a recoger a Leo', 686, 740, 735,
    'Tesara pide las manos fuertes de Naór para investigar una guarida del dragón en busca de pistas y acuerda reunirse con Eldrath a la entrada de Iktan. Naór pregunta por la hora de vuelta: tiene que estar de regreso a las cinco y media para recoger a Leo y avisa que se marchará si la salida se alarga. Tesara le asegura con ironía que volverán a las cinco. Llamar líder a Eldrath provoca a Tryel, que se va a buscarlo para disputarle el puesto.',
    ['Naór', 'Tesara Queen', 'Tryel', 'Eldrath', 'Leo', 'Iktan', 'Clolgedranx'], 'declaracion_personaje',
    'No hay una garantía real de regreso ni un mando formal aceptado. La hora de las cinco y media es el compromiso de Naór, sin que se represente todavía la recogida.')
fact(124, 'Eldrath vende un jade por cincuenta y cinco monedas', 741, 789, 782,
    'Eldrath acude a armarse y a hacer negocios. Ofrece un jade al comerciante, que lo mira, lo huele y lo chupa antes de ofrecer cincuenta monedas. El elfo pide cincuenta y cinco y la venta se cierra por esa cantidad.',
    ['Eldrath', 'Comerciante minotauro de Iktan', 'Iktan'],
    limit='El minotauro se identifica por la continuidad del negocio y el tatuaje posterior, no por un nombre propio confirmado. El jade no se enlaza con otras gemas o collares de la campaña.')
fact(125, 'Eldrath compra armadura y prepara antitoxinas', 790, 819, 805,
    'Eldrath solicita una armadura mejorada y antitoxina. Tras confundir los términos de cuero y cuero tachonado, corrigen que se trata de la segunda y acuerdan noventa monedas, que el elfo paga. Hablan de comprar dos antitoxinas, aclarando que otra persona asumirá una, y Eldrath da por concluidas esas compras antes de recordar el tatuaje.',
    ['Eldrath', 'Comerciante minotauro de Iktan'],
    limit='La solicitud se formula con «más uno», pero no se describe aquí la propiedad exacta ni se añade una estadística permanente por el precio. La conversación sobre quién paga cada antitoxina no permite asignar automáticamente todas las unidades a Eldrath o identificar al segundo pagador.')
fact(126, 'El tatuaje retrasa una hora a Eldrath', 811, 849, 841,
    'Eldrath añade a sus preparativos un tatuaje y tarda mientras los compañeros esperan a la entrada de la ciudad. Tesara pregunta por él y Tryel explica que se está tatuando. Los presentes hablan de una hora de espera; Tryel muestra además su propio hombro tatuado, sin describir en palabras el dibujo.',
    ['Eldrath', 'Tryel', 'Tesara Queen', 'Naór', 'Comerciante minotauro de Iktan', 'Tatuaje incompleto de Eldrath', 'Iktan'],
    limit='La duración es la queja de los personajes y el comentario de la mesa, sin cronómetro diegético. No se reconstruye el diseño visto en pantalla ni se equiparan el tatuaje de Tryel y el de Eldrath.')
fact(127, 'Coyote provoca a Tesara sobre una supuesta relación con Eldrath', 850, 886, 864,
    'Coyote afirma haber visto muy juntos a Tesara y Eldrath y bromea con que se quedará sin novio. Tesara niega haberlo abrazado: recuerda que, cuando sintió pánico, fue el elfo quien le puso la mano encima. Defiende que puede elegir seguir soltera y devuelve la provocación a Coyote.',
    ['Coyote', 'Tesara Queen', 'Eldrath', 'Tryel'], 'declaracion_personaje',
    'Las bromas y lecturas de Coyote no confirman un noviazgo. Se conserva la explicación de Tesara sin sustituirla por la insinuación del compañero.')
fact(128, 'Naór intimida al tatuador y saca a Eldrath con el dibujo a medias', 887, 936, 926,
    'Naór va a la tienda, saluda a Eldrath y presiona al minotauro que lo está tatuando. Le pone la mano en el hombro, clava las uñas y muestra los colmillos mientras insiste en que el trabajo está acabado aunque solo hay medio dibujo. La intimidación surte efecto: el comerciante lo da por terminado y Naór levanta a Eldrath para marcharse.',
    ['Naór', 'Eldrath', 'Comerciante minotauro de Iktan', 'Tatuaje incompleto de Eldrath'],
    limit='«Reotra» es una grafía aislada del saludo en el ASR, no un nombre fijado. La presión para salir no termina la otra mitad del tatuaje ni prueba qué propiedades mágicas tendrá.')
fact(129, 'Las cartas del chat modifican el dinero de Eldrath y Tesara', 937, 998, 984,
    'El director adjudica por cartas del chat una pérdida de veinte monedas a Eldrath, corregida a nueve después de repetir la tirada; le devuelve once para conciliar el ajuste. A Tesara le adjudica nueve monedas y después otras treinta y tres. Los participantes discuten las tiradas y la aplicación de las cartas antes de retomar el viaje.',
    ['Eldrath', 'Tesara Queen'], 'explicacion_director',
    'Ajustes de mesa: no se representa un ladrón, donante o mecanismo del mundo que cause esos cambios. No se mezclan con el precio de la armadura, el jade o una misión de tesoro.')
fact(130, 'Los cinco salen de Iktan con Tryel como guía', 999, 1042, 1000,
    'Se reúnen Eldrath, Tryel, Tesara, Coyote y Naór. Eldrath lleva armadura nueva y medio tatuaje. Mientras discute con Tesara por la espera, Naór pregunta a Tryel si conoce la guarida, la sube encima de ella y sale de la ciudad. Los otros los siguen; Tryel va indicando el camino desde arriba.',
    ['Eldrath', 'Tryel', 'Tesara Queen', 'Coyote', 'Naór', 'Tatuaje incompleto de Eldrath', 'Iktan'],
    limit='Son cinco viajeros; no se añade a Tortas, Ilikar o Leona a la expedición. Las palabras «guarida» pertenecen al destino esperado por el grupo y no identifican por sí solas la propiedad de la cueva que encontrarán.')
fact(131, 'La orientación de Tryel los hace dar vueltas', 1043, 1064, 1049,
    'La marcha por la jungla hace que reconozcan árboles y una misma roca repetidas veces. Eldrath cuestiona a Tryel; ella insiste en que la roca es diferente y dice que sigue el rumbo hacia el que apunta. Naór mantiene su intención de regresar a tiempo para recoger al niño, incluso si los demás continúan dando vueltas.',
    ['Tryel', 'Eldrath', 'Naór', 'Leo'],
    limit='La desorientación no demuestra un engaño deliberado de Tryel. La decisión de Naór de irse a una hora no constituye una salida ya efectuada.')
fact(132, 'Tesara y Eldrath rechazan las bromas sobre noviazgo y jefatura', 1065, 1104, 1081,
    'Las provocaciones de Coyote vuelven a presentar a Tesara como novia de Eldrath y al elfo como jefe. Ambos niegan el noviazgo; Eldrath añade que no es jefe, sino quien propuso una idea. Discute con Tesara sobre el valor de las aportaciones de los otros, y decide dejar el asunto para salir de la jungla cuanto antes.',
    ['Tesara Queen', 'Eldrath', 'Coyote', 'Tryel'], 'declaracion_personaje',
    'La escena no crea un cargo ni una relación amorosa. La discusión tampoco demuestra que los demás carezcan de capacidades o información.')
fact(133, 'Naór intenta seguir el olor del dragón sin lograr orientarse', 1105, 1140, 1124,
    'Mientras varios comen fruta, Naór intenta respirar y olfatear el rastro del olor que percibió antes junto al dragón. El director explica que las quejas de Tesara, las risas de Coyote, el enfado de Eldrath y los toques de Tryel la distraen y le devuelven la irritación. No consigue con ese intento dar con el camino.',
    ['Naór', 'Clolgedranx', 'Tesara Queen', 'Coyote', 'Eldrath', 'Tryel'],
    limit='El recuerdo de sus rondas contra los no muertos es lo que declara la jugadora; no se representa otra patrulla completa. Fallar el rastreo no elimina permanentemente su olfato.')
fact(134, 'Naór asusta a Tesara y la coloca al frente para rastrear', 1141, 1176, 1159,
    'Tras pedir que alguien aporte una manera de seguir el rastro, Naór ruge con fuerza en la cara de Tesara. La resolución de la salvación establece que la historiadora queda aterrada por ella. Naór le pregunta si sabe explorar, la toma por los hombros y la pone delante para que busque. Tryel observa mientras comparte fruta de Coyote.',
    ['Naór', 'Tesara Queen', 'Tryel', 'Coyote'],
    limit='El miedo procede del rugido de Naór, no de una aparición del dragón. La condición se adjudica en ese momento, sin fijar aquí una duración nueva.')
fact(135, 'Las frutas aportan efectos que se comentan durante la búsqueda', 1177, 1208, 1199,
    'Durante la pausa, un participante representa que una serpiente enroscada en su fruta lo muerde mientras come. La mesa también comenta que Naór puede respirar bajo el agua. Los efectos de fruta acompañan la exploración; más adelante Tesara identifica expresamente el suyo como la capacidad de producir fuego sin herramientas.',
    ['Naór', 'Tesara Queen'], 'explicacion_director',
    'No se fija el nombre del mordido por falta de identificación inequívoca de voz. El comentario sobre respirar bajo el agua se conserva como adjudicación de mesa y no se confunde con los besos sirénidos del viaje a Perlasal. La duración de estos efectos no se precisa.')
fact(136, 'Tesara encuentra marcas del dragón y pisadas desacompasadas', 1227, 1280, 1269,
    'Tesara busca huellas de no muertos y señales que recuerden el paso del dragón. Bajo la presión de Naór fracasa primero y después encuentra ramas rotas en los árboles por donde pasó el dragón, además de pisadas de humanoides y criaturas de cuatro patas que avanzan de forma irregular, como a trompicones. Los rastros se internan en la jungla.',
    ['Tesara Queen', 'Naór', 'Clolgedranx'],
    limit='Las pisadas no identifican nombres, número exacto o cuerpos individuales. Las señales indican una dirección, no que el dragón esté presente ni que la cueva haya sido ya localizada en este instante.')
fact(137, 'Eldrath reconoce el terreno rocoso hacia el que apuntan los rastros', 1281, 1325, 1308,
    'Eldrath quiere estudiar la inclinación, las plantas y el suelo para inferir si hay una cueva cerca. El director resuelve la búsqueda con Naturaleza: ve aumentar la roca y disminuir los árboles en la dirección de Tesara. Ella comparte los rastros encontrados y él señala que las características del terreno parecen conducir hacia una cueva por aquel lado.',
    ['Eldrath', 'Tesara Queen', 'Naór'],
    limit='Es una inferencia sobre el terreno corroborada después al encontrar la entrada, no un mapa, una coordenada o el hallazgo instantáneo de todas las guaridas.')
fact(138, 'Eldrath enlaza las mentes de cuatro compañeros durante seis horas', 1362, 1403, 1391,
    'Para comunicarse sin hablar si el dragón está cerca, Eldrath emplea Susurro psiónico y establece un enlace con Tryel, Tesara y Coyote. Declara una duración de seis horas y prueba la conexión hablándoles directamente en la cabeza. Excluye a Naór y bromea con que no quiere conocer lo que pasa por su mente.',
    ['Eldrath', 'Tryel', 'Tesara Queen', 'Coyote', 'Naór'],
    limit='No se acredita lectura pasiva de pensamientos, una conexión con Naór o un poder del dragón. La duración se declara al activar la capacidad y no se extiende a otras sesiones.')
fact(139, 'El director precisa que Eldrath debe retransmitir los mensajes', 1404, 1418, 1407,
    'El director aclara que Tesara y Coyote escuchan a Eldrath, y que la comunicación no los conecta directamente entre sí. Eldrath acepta hacer de antena y retransmitir lo que los demás digan por el enlace para que puedan coordinarse.',
    ['Eldrath', 'Tesara Queen', 'Coyote', 'Tryel'], 'explicacion_director',
    'La frase automática «os podéis comunicar entre vosotros» aparece dentro de una corrección contradictoria; la explicación inmediata de que Eldrath retransmitirá impide presentarlo como una red de conversación libre entre todos.')
fact(140, 'Las huellas terminan ante una pared cubierta de raíces', 1419, 1437, 1436,
    'Siguiendo a Tesara, el grupo avanza por lugares que Tryel vuelve a reconocer y alcanza un montículo o pared rocosa cubierta de raíces. Las huellas llegan hasta esa vegetación, que oculta el acceso.',
    ['Tesara Queen', 'Tryel', 'Eldrath', 'Coyote', 'Naór', 'Cueva envenenada explorada por el grupo'],
    limit='El director corrige su primera palabra montaña y no fija altura, topónimo o coordenadas. Tryel reconoce el recorrido de la cueva que había recordado (40-030, 48-114); se conserva esa identificación atribuida a ella, sin confirmar la propiedad del dragón.')
fact(141, 'Eldrath aparta parte de las raíces y percibe el hedor del interior', 1438, 1457, 1454,
    'Eldrath intenta apartar las raíces con una daga para ver qué hay detrás. Consigue abrir un poco la vegetación, suficiente para notar un aire de olor muy fuerte y distinguir que parece haber una cueva al otro lado. Las raíces siguen bien adheridas y aún tapan el paso.',
    ['Eldrath', 'Cueva envenenada explorada por el grupo'],
    limit='El primer intento no despeja completamente el acceso ni revela un dragón. El olor, por sí solo, no demuestra la propiedad o identidad histórica del refugio.')
fact(142, 'Tesara quema las raíces con el fuego recibido de una fruta', 1458, 1474, 1462,
    'Tesara pide sitio y aprovecha el efecto de una fruta que le permite crear fuego sin herramientas. Pone las manos sobre las raíces y las quema. La vegetación se agita violentamente, cae todavía en movimiento y en llamas y deja una cueva abierta ante el grupo; el hedor del interior aumenta.',
    ['Tesara Queen', 'Cueva envenenada explorada por el grupo'],
    limit='La facultad se atribuye expresamente a la fruta, no a Escupefuego ni a un aprendizaje permanente. El movimiento de las raíces es observable, sin nombrar a quien las controla o acreditar que el fuego afecte al dragón.')
fact(143, 'Eldrath comparte una botella con Tryel antes de entrar', 1475, 1491, 1477,
    'Eldrath bebe aproximadamente media botella y entrega el resto a Tryel para que también beba. El jugador aclara que representa su preocupación por su hermana y que el reparto no aplica un efecto mecánico parcial. Después pide al grupo que esté listo y alerta.',
    ['Eldrath', 'Tryel', 'Cueva envenenada explorada por el grupo'],
    limit='La botella no se nombra en este momento; no se le asigna por anticipación una protección de media dosis o una curación. La intención protectora no equivale a inmunidad.')
fact(144, 'La expedición busca información antes de enfrentarse al dragón', 1492, 1513, 1500,
    'Ante la pregunta de qué esperan encontrar, Eldrath explica que necesitan alguna pista que los lleve al dragón o revele un punto débil, porque actúan con poca información. Considera la cueva una de las guaridas del dragón verde y entra para comprobar qué hay.',
    ['Eldrath', 'Clolgedranx', 'Cueva envenenada explorada por el grupo'], 'declaracion_personaje',
    'La propiedad del lugar es la hipótesis que guía al personaje, no una aparición o confirmación independiente del dragón. No se ha obtenido aún la pista que buscan.')
fact(145, 'Cubrirse del hedor y proponer tropas de Atlan', 1514, 1521, 1518,
    'Antes de internarse, Tesara se cubre la boca con un pañuelo por el hedor. Se plantea enviar un emisario a Atlan para que venga un ejército y acabe con el dragón, mientras continúa la entrada en la cueva.',
    ['Tesara Queen', 'Atlan', 'Clolgedranx', 'Cueva envenenada explorada por el grupo'], 'declaracion_personaje',
    'No se identifica con certeza la voz que propone el emisario ni se representa que alguien lo envíe. No llegan tropas ni se activa una alianza militar por esta sugerencia.')
fact(146, 'La entrada obliga a resistir veneno y hiere a Tesara', 1522, 1541, 1536,
    'Los cinco entran en la cueva y el director pide salvaciones de Constitución. Tesara recibe cuatro puntos de daño de veneno. La adjudicación se vincula expresamente a una trampa introducida mediante una carta del chat.',
    ['Tesara Queen', 'Eldrath', 'Tryel', 'Coyote', 'Naór', 'Cueva envenenada explorada por el grupo'], 'explicacion_director',
    'La herida de veneno se aplica en la escena; el chat es su origen de mesa, sin autor material, dispositivo concreto o intención de un personaje demostrados. No se atribuyen esos cuatro puntos a todos los viajeros.')
fact(147, 'La cueva huele a podredumbre y veneno y pierde la luz de la entrada', 1542, 1565, 1546,
    'El grupo avanza entre un olor pesado que mezcla podredumbre y veneno. La luz de la entrada queda atrás y se apaga. Los hermanos elfos y Naór pueden ver en la oscuridad, mientras Tesara y Coyote distinguen poco. Tesara se sorprende de no llevar antorchas a pesar de ser exploradora.',
    ['Tesara Queen', 'Coyote', 'Eldrath', 'Tryel', 'Naór', 'Cueva envenenada explorada por el grupo'],
    limit='La falta de luz no significa ceguera permanente. La cueva no contiene un dragón visible en lo leído hasta 01:06:36.549; los sucesos posteriores requieren el cotejo de los otros tramos.')

def stage(title, text, refs): return dict(titulo=title, texto=text, referencias=[f'48-{n}' for n in refs])

ETAPAS = [
stage('Lo que Tesara trae del templo',
    'La amenaza del dragón verde pesa de forma distinta sobre cada uno. Eldrath sabe por Tesara que su hermana y él están en el centro del peligro; ella ha intentado prevenir lo que pueda pasar y ha pasado tiempo con Walulu, entre documentos, libros y profecías. Coyote ha preferido la tranquilidad de la taberna. Naór recuerda por su parte el encuentro con Citlali a la salida del colegio y unos entrenamientos que acabaron con combatientes inconscientes. Esos recuerdos dan paso a la mañana en Iktan.\n\nTesara sale del templo cargada de informes, pergaminos y libros y busca a los dos elfos en El Huevo Emplumado. Entra empujando como puede la puerta con el cuerpo y deja lo que lleva en la barra. Eldrath estaba pendiente de unos clientes: parecen piratas de Shiaru y su presencia le inspira desconfianza. Tryel, en cambio, está distraída con Molly, se toca el pelo y la encuentra lo bastante amigable como para querer hablar con ella. Coyote toma cerveza y mira a la encargada felina. Tesara interrumpe a todos. Los reproches por la bebida de primera hora y por su falta de saludo duran poco: trae un asunto más urgente y quiere que encuentren al dragón para dar el primer golpe.',
    [101,102,103,104,105,106,107]),
stage('Una historia antigua y seis días de plazo',
    'La investigación no ofrece la debilidad que esperaban, pero sí una historia. El dragón llegó joven a la jungla antes de la fundación de Iktan. Creció alimentándose allí y creando no muertos que lo ayudaban a sobrevivir. Dejaba que las pequeñas poblaciones prosperaran: las personas que se perdían entre los árboles podían convertirse en su comida. Después, un ataque dracónico de hace cien o doscientos años según la estimación del director llevó a sacerdotes y gente religiosa a proteger la ciudad con un ritual. Tesara puede saber que impide entrar a grandes dragones, aunque carece de la capacidad mágica necesaria para comprenderlo por entero. Tampoco descubre un secreto nuevo detrás de los cuerpos movidos por plantas.\n\nTesara expone lo que ha podido recuperar de aquellos cuentos, leyendas e historias. Se refiere al desastre antiguo como obra de otro dragón y ve una anomalía preocupante en el interés actual del verde por invadir la ciudad. Además, afirma que parece trabajar para otro dragón: esa es la conclusión que transmite, sin que puedan identificar al supuesto patrón. El grupo quiere información para tender una trampa o explotar alguna debilidad. El tiempo es escaso. El enemigo dio una semana para que se entregaran los elfos y, según recuerda Tesara, ya ha transcurrido un día. Quedan seis.',
    [108,109,110,111,112,113]),
stage('Una cueva recordada y unos preparativos desiguales',
    'Eldrath vuelve sobre el envenenamiento de Tryel y le pregunta dónde ocurrió. Su hermana recuerda una gran cueva de la jungla que parecía la gruta del dragón. El elfo propone prepararse e investigarla: entrar directamente en una pelea sin información les parece mortal. Saben que hay varias guaridas, pero buscar todas consumiría el plazo. Tesara preferiría una ciudad con una biblioteca mejor y compendios útiles; no saben dónde encontrarla ni pueden arriesgarse a vagar por la jungla para sufrir otra emboscada. La cueva recordada es lo que tienen.\n\nLas compras quedan condicionadas por el dinero. Coyote solo cuenta veinticinco monedas y no consigue cuadrar una poción. Mientras los demás se preparan, se acerca a Tryel y comenta el atractivo de Molly. La elfa se planta ante él: la ha visto primero y no quiere competencia. La amenaza, resuelta con una tirada de intimidación, provoca nuevas bromas del cambiaformas y un gruñido de Tryel. Molly no participa de ese acuerdo que los otros parecen disputarse.',
    [114,115,116,117]),
stage('La calma que Walulu intenta enseñarle a Naór',
    'En el templo, Naór está con Walulu y una tortuga pequeña que lleva gafas y dirige una clase para dominar su ira. Le pregunta por el insulto que dedicó a Miaussy en el colegio y la lleva a admitir que no debió decirlo. La conversación se extiende a lo que significa comportarse como una madre: hablar bien, respetar a los demás, no dejar al hijo durante días con una desconocida y pagar a quien lo cuida. Naór pregunta si todo aquello es necesario. Walulu responde que sí, al menos hasta que se calme, y le recuerda los saltos entre palmeras y el goliat que llevaron muy herido y tuvieron que arrastrar. La leonina asume la culpa, aunque dice que no lo pretendía.\n\nLa tortuga interrumpe a Walulu para guiar las últimas respiraciones. Naór inspira y espira, repite que no tiene rabia y que no se enfada. Ser una leona sin uñas le resulta una consigna menos fácil de aceptar. La sesión termina con un recipiente para donaciones: Walulu deposita unas monedas y promete ir pagando las clases. Naór agradece la ayuda y sale dispuesta a tener un día fabuloso, dar una vuelta y comprar la merienda. Tryel le ofrece un plan distinto: salir con ellos, despertar la rabia y golpear criaturas. Naór acepta acompañarla, pero responde que lo hará sin violencia.',
    [118,119,120,121]),
stage('La madre del año y la espera ante la puerta',
    'Tesara recibe a Naór con un sarcasmo que pone a prueba las respiraciones recién aprendidas. Pregunta por Leo, que según su madre está en el colegio, y le recuerda que ha pasado tres días cuidándolo mientras soportaba sus malas palabras. Naór promete hablar con el niño si hace falta; al posar la mano en el hombro de Tesara aprieta más de la cuenta y tiene que aflojar. La historiadora ofrece incluso una crema para una hinchazón que la otra atribuye al sol. Bajo la amabilidad forzada de la leonina sigue habiendo irritación.\n\nTesara le pide la fuerza de sus manos para buscar pistas en una guarida del dragón. Han quedado con Eldrath en la entrada de Iktan. Naór se suma con una condición: a las cinco y media tiene que estar de vuelta para recoger a Leo y se marchará si la expedición se alarga. Tesara asegura con ironía que estarán a las cinco. Otro sarcasmo, el de llamar gran líder a Eldrath, manda a Tryel a disputar el puesto a su hermano.\n\nEl elfo está ocupado con negocios. Vende un jade por cincuenta y cinco monedas, compra una armadura de cuero tachonado por noventa y prepara antitoxinas. Todavía añade un tatuaje a la lista. Los demás esperan en la puerta y se quejan de una hora de retraso; Tryel explica que sigue tatuándose. Coyote aprovecha la espera para atribuir a Tesara un noviazgo con Eldrath. Ella lo niega: cuando tuvo miedo, fue él quien le puso una mano encima. No piensa aceptar que esa ayuda decida sus relaciones.',
    [122,123,124,125,126,127]),
stage('Un tatuaje a medias y un camino que se repite',
    'Naór pierde la paciencia con el retraso y va a buscar a Eldrath a la tienda. El comerciante minotauro solo ha dibujado la mitad del tatuaje. La leonina lo saluda con dulzura, le clava las uñas en el hombro y muestra los colmillos mientras insiste en que el trabajo está terminado. El tatuador cede; Naór levanta al elfo y lo saca. Unos ajustes de dinero ligados a las cartas del chat se resuelven antes de que la marcha continúe: Eldrath pierde finalmente nueve monedas y Tesara recibe nueve y otras treinta y tres, sin que aparezca un responsable dentro de la historia.\n\nPor fin se reúnen los cinco. Eldrath lleva armadura nueva y el tatuaje a medias; Tesara sigue reprochándole el tiempo perdido. Naór pregunta a Tryel si conoce la guarida, la sube encima y sale con ella de la ciudad. La elfa indica giros desde arriba, pero los árboles y una roca se repiten demasiado. Eldrath desconfía de su orientación, mientras Naór recuerda que llegará una hora en la que se irá a recoger a Leo. Coyote vuelve a llamarlo jefe y a presentar a Tesara como su novia. Los dos niegan la relación; Eldrath también rechaza haberse proclamado líder. La discusión termina por agotarlos antes de resolver el camino.',
    [128,129,130,131,132]),
stage('Rastros entre las disputas y voces en la cabeza',
    'Algunos comen fruta mientras Naór intenta reconocer el olor que percibió junto al dragón. Sus respiraciones no bastan: las quejas, las risas y los toques de Tryel la distraen y le devuelven el enfado. Al pedir alguien capaz de seguir un rastro, acaba rugiendo en la cara de Tesara. La historiadora queda aterrada. Naór le pregunta si es una buena exploradora, la coge por los hombros y la coloca al frente para que demuestre cómo busca.\n\nTesara intenta encontrar huellas de los no muertos o señales del dragón. La presión la hace fallar al principio, pero después distingue ramas rotas a su paso y pisadas de humanoides y criaturas de cuatro patas que anduvieron a trompicones. Se dirigen hacia dentro de la jungla. Eldrath estudia por su parte la forma del suelo y la vegetación; ve que aumentan las rocas y disminuyen los árboles en aquella dirección. Al poner en común ambos hallazgos, reconoce una vía probable hacia la cueva. Tesara sigue demasiado pendiente de la respiración de Naór en su nuca y llega a pedir que le enseñe los ejercicios de calma.\n\nMientras avanzan, Eldrath prepara una manera de comunicarse sin alertar al dragón si está cerca. Usa Susurro psiónico para enlazarse con Tryel, Tesara y Coyote durante seis horas; deja a Naór fuera. Los compañeros oyen su voz dentro de la cabeza. El director precisa el alcance de la conexión: Tesara y Coyote escuchan al elfo, pero necesitan que él retransmita los mensajes para hablar entre sí. Eldrath acepta hacer de antena y pide que no le comuniquen pensamientos que no quiera conocer.',
    [133,134,135,136,137,138,139]),
stage('Las raíces arden y se abre la oscuridad',
    'Siguen a Tesara por rincones que Tryel vuelve a reconocer hasta llegar a una pared de un montículo rocoso. Las huellas se pierden en las raíces que la cubren. Eldrath intenta apartarlas con una daga y abre lo bastante para notar un aire de hedor intenso: parece haber una cueva detrás, pero la vegetación está bien pegada. Tesara pide paso y recurre al efecto de la fruta que ha comido, capaz de darle fuego sin herramientas. Al contacto de sus manos las raíces arden y se agitan violentamente. Caen aún en movimiento y dejan el acceso abierto.\n\nEldrath bebe parte de una botella y comparte el resto con Tryel, un gesto de preocupación por su hermana cuya media dosis no se aplica como un nuevo efecto mecánico. Pide que todos estén alerta. No espera una victoria inmediata: entran para buscar alguna pista, un punto débil o información que les permita dejar de actuar a ciegas. Tesara se tapa la boca con un pañuelo. Se propone pedir un ejército a Atlan, aunque nadie envía todavía al emisario.\n\nAl cruzar al interior deben resistir el veneno; Tesara recibe cuatro puntos de daño en una adjudicación vinculada a una carta del chat. El olor mezcla podredumbre y veneno. La entrada se aleja y su luz va desapareciendo: los hermanos elfos y Naór se orientan en la oscuridad, pero Tesara y Coyote apenas ven. La historiadora descubre que ni siquiera ha traído antorchas. La exploración acaba de empezar.',
    [140,141,142,143,144,145,146,147]),
]

H = []
def history(name, kind, desc, note, new, stages):
    H.append(dict(nombre=name, tipo=kind, descripcion=desc, nota=note, nueva=new, etapas=stages))

history('Tesara Queen','personaje','Historiadora humana de Puerto de Espadas; combina su investigación del dragón con los cuidados de Leo.',
    'Tesa es la abreviatura canónica. Separar los hallazgos archivísticos de su hipótesis sobre otro dragón como patrón; el fuego de esta salida procede de una fruta.',False,[
    stage('De la biblioteca a la urgencia del ultimátum','Tesara dedica su tiempo con Walulu a leer documentos, libros y profecías sobre el dragón verde, los rituales y los muertos movidos por plantas. Llega a la taberna con los brazos llenos de material y pide actuar antes que el enemigo. Lo que ha recuperado es sobre todo historia: la llegada de un dragón joven antes de la fundación de Iktan, su relación depredadora con la jungla y el ritual levantado tras un ataque dracónico antiguo. Comprende que impide la entrada de grandes dragones, pero no cómo se realiza. Al transmitirlo habla de otro dragón en el ataque histórico y de un supuesto patrón dracónico actual, sin poder identificar a ninguno. Recuerda a los compañeros que del plazo de una semana quedan seis días.',[103,105,107,108,109,110,111,112,113]),
    stage('El peso de Leo y la irritación con los elfos','La historia de los archivos no basta para diseñar la trampa que quisiera y Tesara preferiría consultar una gran biblioteca, pero no conocen una cercana y carecen de tiempo. Reclama a Naór por haber cuidado a Leo tres días y la invita a ayudar con su fuerza en la expedición. Después espera a Eldrath ante la puerta mientras él se tatúa y le reprocha el retraso. Coyote interpreta como romance la ayuda que el elfo le prestó durante su miedo; ella rechaza el noviazgo y afirma su decisión de estar soltera.',[115,122,123,126,127,132]),
    stage('La exploradora aterrada encuentra las señales','Naór la asusta con un rugido y la obliga a ponerse al frente. Pese a la presión, Tesara termina encontrando las ramas rotas por el dragón y las pisadas desacompasadas de otros seres que se internan en la jungla. Comparte el hallazgo con Eldrath, que lo relaciona con la zona rocosa. Acepta el enlace psiónico del elfo para comunicarse sin hablar y comprende que él debe retransmitir las respuestas.',[134,136,137,138,139]),
    stage('El fuego de una fruta abre una entrada envenenada','Ante las raíces que cubren la pared rocosa, Tesara usa el efecto de una fruta para producir fuego con sus manos. Las quema y despeja el acceso mientras la vegetación se retuerce. Se cubre la boca con un pañuelo y entra con los otros. Recibe cuatro puntos de daño de veneno al inicio de la exploración, en una adjudicación introducida por una carta del chat. Cuando la luz de la entrada queda atrás apenas ve y descubre que no ha llevado antorchas.',[140,142,145,146,147])])
history('Eldrath','personaje','Elfo hermano de Tryel que busca información para enfrentarse al dragón y protege a su hermana.',
    'Distinto de Aerendriel. La jefatura y el noviazgo con Tesara son bromas rechazadas por los personajes. El enlace psiónico necesita su retransmisión.',False,[
    stage('Buscar primero la manera de vencer','La amenaza transmitida por Tesara le preocupa por su hermana y por sí mismo. Escucha la historia recuperada de los archivos y asume que solo quedan seis días. Pregunta a Tryel por la cueva donde se envenenó y propone investigarla para encontrar información, pues considera suicida acudir a un combate directo. Reconoce que el dragón tiene varios refugios y que buscarlos todos consumiría el plazo.',[102,107,112,113,114,115]),
    stage('Prepararse hasta que Naór lo saca de la tienda','En el negocio de un minotauro vende un jade por cincuenta y cinco monedas y compra una armadura de cuero tachonado por noventa. Prepara antitoxinas y añade un tatuaje que retrasa al grupo. Naór intimida al tatuador y lo saca con medio dibujo todavía pendiente. Las cartas del chat le adjudican una pérdida final de nueve monedas. Se reúne con los otros y sale con la armadura nueva y el trabajo incompleto, todavía discutiendo con Tesara por la espera.',[124,125,126,128,129,130]),
    stage('Terreno, telepatía y una botella para Tryel','Cuestiona la orientación de Tryel cuando el grupo repite árboles y rocas, pero niega haberse proclamado jefe. Ayuda a rastrear estudiando el suelo y la vegetación, e identifica una dirección más rocosa que coincide con las marcas halladas por Tesara. Enlaza su mente con Tryel, Tesara y Coyote durante seis horas y se ofrece a retransmitir sus mensajes. Aparta parte de las raíces con una daga antes de que Tesara despeje el acceso con fuego. Comparte una botella con su hermana por preocupación y entra en busca de pistas, sin ver aún al dragón.',[131,132,137,138,139,141,143,144])])
history('Tryel','personaje','Elfa hermana de Eldrath que recuerda una cueva donde se envenenó y guía la expedición con dificultades.',
    'Triel, Trier y Mirien se tratan por la continuidad de la hermana presente, sin inventar personas nuevas. El recuerdo no prueba la propiedad de la cueva visitada.',False,[
    stage('Molly, Coyote y el recuerdo de la gruta','En la taberna presta más atención a Molly que a las sospechas de su hermano sobre unos clientes con aspecto de piratas de Shiaru. Propone acercarse a ella y después reclama ante Coyote que la vio primero. A petición de Eldrath recuerda que se envenenó en una gran cueva que parecía la gruta del dragón, y ofrece ese punto de partida para buscar información.',[106,114,117]),
    stage('Una guía llevada a hombros','Invita a Naór a despertar su rabia y a pelear durante la expedición, pero recibe una respuesta pacífica. El sarcasmo de Tesara sobre Eldrath como líder la impulsa a disputarle el título. Mientras el hermano se tatúa, espera con los otros y explica la demora. Al salir, Naór la lleva encima para que señale el camino; repiten árboles y rocas, aunque Tryel insiste en su orientación. Más adelante reconoce lugares ya recorridos cuando siguen los rastros de Tesara.',[121,123,126,130,131,140]),
    stage('Compañera en la entrada de raíces','Observa las discusiones y comparte fruta con Coyote, participa en el enlace psiónico de Eldrath y llega con los otros a la pared cubierta de raíces. Su hermano comparte con ella una botella antes de entrar. Al perder la luz exterior puede seguir viendo en la oscuridad, a diferencia de Tesara y Coyote.',[134,138,140,143,147])])
history('Naór','personaje','Princesa leonina de Atlan, madre adoptiva de Leo, que intenta controlar su ira y se suma a la búsqueda de pistas.',
    'No se confunde con Leona, harengon que no participa en esta salida. La tortuga de las clases carece de nombre y se conserva separada de Tortas.',False,[
    stage('Aprender a respirar ante Walulu','Después de recordar los encuentros escolares y los entrenamientos, Naór recibe una clase de calma en el templo con Walulu y una pequeña tortuga de gafas. La reprenden por el insulto a Miaussy y por ausentarse varios días de los cuidados de Leo; Walulu añade el incidente del goliat herido. Naór acepta parte de la culpa y practica inspiraciones y espiraciones, repitiendo que no tiene rabia. Walulu paga la donación de las clases. Sale agradecida y responde a la invitación combativa de Tryel que puede acompañarla, pero sin violencia.',[101,118,119,120,121]),
    stage('La responsabilidad de volver por Leo','Tesara le reclama los tres días al cuidado del pequeño y las malas palabras que ha soportado. Naór mantiene un tono amable, aunque aprieta demasiado su hombro, y promete hablar con Leo sobre su conducta. Acepta ayudar a investigar la cueva, con la condición de regresar para recoger al niño a las cinco y media. Cuando Eldrath retrasa a todos con su tatuaje, va al negocio, intimida al minotauro y se lo lleva con medio dibujo hecho. Después sube a Tryel y parte con ella desde Iktan.',[122,123,126,128,130]),
    stage('La calma se rompe durante el rastreo','Intenta seguir por el olfato el recuerdo del dragón, pero las discusiones la distraen. Su rugido aterra a Tesara, a la que toma por los hombros y coloca delante para que encuentre huellas. La presión incomoda a la historiadora, aunque acaba dando resultado. Eldrath la deja fuera del enlace psiónico que prepara para los otros. Naór continúa con la expedición y puede orientarse en la oscuridad de la cueva, mientras Tesara y Coyote ven poco.',[131,133,134,136,138,147])])
history('Coyote','personaje','Cambiaformas de Iktan que acompaña la expedición después de descansar en la taberna.',
    'Sus insinuaciones no crean relaciones amorosas. La falta de dinero no se corrige atribuyéndole una compra no representada.',False,[
    stage('Descanso, curiosidad y provocaciones','Dice haberse mantenido tranquilo y dedicado a beber. En El Huevo Emplumado escucha a Tesara pedir que se adelanten al dragón y recibe la información de que solo quedan seis días. No puede cuadrar una poción con sus veinticinco monedas. Comparte con Tryel su interés por Molly y recibe una respuesta territorial: la elfa quiere prioridad y trata de intimidarlo. Más tarde provoca a Tesara con un supuesto noviazgo con Eldrath, que ella niega.',[104,105,107,112,113,116,117,127]),
    stage('La marcha hasta una oscuridad incómoda','Sale de Iktan con los otros cuatro y sigue bromeando sobre el liderazgo del elfo y su relación con Tesara. Mientras las discusiones y la búsqueda se prolongan, come fruta que Tryel comparte. Acepta el enlace psiónico de Eldrath y la necesidad de que el elfo retransmita sus mensajes. Llega a la cueva de raíces con los demás; al avanzar y perder la luz exterior, tanto él como Tesara ven poco.',[130,131,132,133,134,138,139,140,147])])
history('Walulu','personaje','Dirigente y chamana de Iktan que facilita archivos a Tesara y ayuda a Naór con su conducta.',
    'La asistencia de la tortuga no implica identidad con Tortas. La clase no resuelve la convocatoria de los clanes ni confirma que se celebrara la reunión propuesta en 47-087.',False,[
    stage('Libros y clases para dos urgencias','Tesara ha pasado tiempo con Walulu consultando los libros, documentos y profecías de su biblioteca para comprender al dragón y la protección de Iktan. En el templo, Walulu acompaña a Naór durante una clase dirigida por una tortuga pequeña con gafas. Defiende que necesita calmarse y le recuerda las palmeras y el goliat llevado con graves heridas. Cuando la profesora de calma pide una donación, la dirigente entrega monedas y dice que irá pagando las clases.',[103,105,118,119,120])])
history('Clolgedranx','personaje','Dragón verde cuya amenaza contra Iktan impulsa la búsqueda de información y de un refugio en la jungla.',
    'Distinto de Zarynth. La historia archivística y las conclusiones de Tesara conservan su atribución; no identifican al supuesto empleador ni al atacante antiguo.',False,[
    stage('Lo que cuentan los archivos de Iktan','La investigación de Tesara lo sitúa joven en la región antes de que se fundara Iktan. Creció alimentándose en la jungla y creando no muertos para ayudarse a sobrevivir. No solía interesarse por las pequeñas ciudades: dejar que crecieran le daba posibles presas cuando alguien se perdía en el bosque. Tras un ataque dracónico antiguo, sacerdotes y otros religiosos levantaron un ritual que impide entrar a grandes dragones. El director estima cien o doscientos años; Tesara habla del ataque de otro dragón. La atribución debe cotejarse con el relato de Walulu del capítulo anterior, que había hablado del ataque del dragón y de ciento veinte años.',[108,109,110,111,112]),
    stage('Un plazo que empuja a buscar sus refugios','Tesara informa al grupo de que queda un plazo de seis días antes de la respuesta exigida por el ultimátum. Sostiene que el dragón parece trabajar para otro dragón, sin una identidad verificada. Eldrath decide investigar la cueva recordada por Tryel, consciente de que se han mencionado varias guaridas y de que no dispone de tiempo para localizarlas todas. Las ramas rotas halladas por Tesara orientan la marcha hacia una cueva tapada de raíces y hedor, que el elfo considera uno de sus refugios. La criatura no se muestra durante la llegada y entrada; la propiedad sigue siendo una hipótesis de los viajeros.',[113,114,115,136,140,141,142,144])])
history('Iktan','lugar','Población protegida frente a la entrada de grandes dragones, donde se prepara la expedición.',
    'La función del rito no se extiende a amenazas distintas por inferencia. No se fija la identidad del dragón del ataque histórico con un nombre no pronunciado.',False,[
    stage('Los archivos y la amenaza que obliga a salir','La biblioteca de Walulu permite a Tesara recuperar una historia anterior a la ciudad: el dragón verde llegó joven y toleró después las pequeñas poblaciones de la región. Un ataque dracónico antiguo condujo a sacerdotes y religiosos a realizar un ritual protector. Tesara sabe su función general, impedir entrar a grandes dragones, pero no comprende la ejecución del rito. La amenaza de no muertos y la exigencia de entregar a los hermanos siguen haciendo necesario actuar: según Tesara quedan seis días.',[103,105,108,109,110,111,112,113]),
    stage('Una mañana de cuidados, compras y partida','El Huevo Emplumado reúne a los viajeros mientras Tesara les transmite sus hallazgos. En el templo, Walulu acompaña a Naór a una clase de calma; Leo permanece según su madre en el colegio, y Tesara reclama por tres días a su cuidado. Eldrath vende un jade y compra equipo antes de retrasarse con un tatuaje. Naór lo saca de la tienda y los cinco terminan saliendo de la ciudad hacia la jungla, con el compromiso de ella de regresar por Leo.',[105,106,107,118,119,120,122,123,124,125,126,128,130])])
history('El Huevo Emplumado','lugar','Taberna de Iktan donde Tesara comparte la información del dragón con Eldrath, Tryel y Coyote.',
    'La sospecha de que unos clientes son piratas de Shiaru no demuestra su vinculación con la ocupación del poblado.',False,[
    stage('Punto de reunión antes de buscar al dragón','Tesara llega desde el templo cargada de libros y pergaminos y encuentra a Eldrath, Tryel y Coyote. El elfo vigila a una mesa de clientes que le recuerdan piratas de Shiaru, mientras Tryel presta atención a Molly y Coyote toma cerveza mirando a la encargada felina. La historiadora deja el material en la barra y reclama una respuesta urgente al dragón. Allí comparte la historia de los archivos y recuerda los seis días de plazo. La salida se organiza entre la propuesta de visitar una cueva y los preparativos; antes de marcharse, Coyote y Tryel rivalizan de palabra por el interés en Molly.',[105,106,107,112,113,114,115,117])])
history('Molly','personaje','Antigua capitana de la Marina presente entre las miradas y comentarios de los viajeros en la taberna de Iktan.',
    'Su presencia no confirma afiliación a los clientes sospechosos ni consentimiento a las insinuaciones de Tryel y Coyote.',False,[
    stage('El interés de Tryel en la taberna','Tryel mira a Molly mientras se toca el pelo y la considera una persona amigable con la que acercarse a hablar. Eldrath le advierte que parece juntarse con una mesa de hombres que él toma por piratas de Shiaru. Coyote también comenta su atractivo y provoca que la elfa reclame haberla visto primero. Molly no interviene ni se define una relación entre ella y ninguno de los dos.',[106,117])])
history('Leo','personaje','Niño harengon acogido por Naór que motiva los reproches por los cuidados y el horario de regreso.',
    'No aparece actuando en estas escenas. Las preguntas acusatorias de Tesara no acreditan nuevas agresiones del niño.',False,[
    stage('El cuidado que los adultos discuten','La clase de Naór recuerda que no debe dejar a su hijo durante varios días con otra persona sin pagarle. Tesara precisa después que lo ha cuidado tres días y reprocha las malas palabras que dirige a ella, la camarera y otros vecinos. Naór afirma que Leo está en el colegio y promete hablar con él si lo necesita. Acepta la expedición con la condición de regresar a Iktan a las cinco y media para recogerlo y reitera que abandonará la salida si se alarga.',[119,122,123,131])])
history('Tortuga terapeuta del templo de Iktan','personaje','Tortuga pequeña con gafas que dirige una sesión para dominar la ira de Naór en el templo.',
    'Identidad descriptiva sin nombre propio o sexo confirmado; no se equipara con Tortas por pertenecer a la misma especie. No se la presenta como una profesión clínica moderna.',True,[
    stage('Respirar antes de salir','Sentada en una silla junto a Walulu y Naór, pregunta a la leonina por el insulto a Miaussy en el colegio y le hace reconocer que estuvo mal. La clase pasa por las obligaciones de una madre y por los episodios de violencia que preocupan a Walulu. La tortuga conduce las últimas inspiraciones y espiraciones y pide repetir que no hay rabia ni enfado; usa la imagen de una leona sin uñas. Al terminar acerca un recipiente y solicita donaciones para continuar dando clases. Walulu deposita monedas y promete ir pagando; Naór agradece la sesión.',[118,119,120])])
history('Comerciante minotauro de Iktan','personaje','Comerciante y tatuador que atiende los preparativos de Eldrath en Iktan.',
    'La única posible grafía de nombre es «Reotra» en el saludo de Naór. Mantener la etiqueta descriptiva y no fusionarlo con Armin, Froger o artesanos de Cuicapalli.',True,[
    stage('El jade y el equipo del elfo','Eldrath le ofrece un jade. Lo mira, lo huele y lo chupa antes de ofrecer cincuenta monedas; termina aceptando cincuenta y cinco. En el mismo intercambio se acuerda una armadura de cuero tachonado por noventa y se preparan antitoxinas antes de pasar al tatuaje.',[124,125]),
    stage('Un trabajo interrumpido por las uñas de Naór','Todavía está tatuando al elfo cuando Naór llega para terminar con la espera. Solo tiene medio dibujo hecho. La leonina le aprieta el hombro con las uñas y le muestra los colmillos mientras insiste en que está acabado. La intimidación lo hace dar por terminado el trabajo y Eldrath se marcha con el tatuaje incompleto. No se establece el precio o efecto del tatuaje ni una reparación posterior.',[126,128])])
history('Tatuaje incompleto de Eldrath','objeto','Tatuaje adquirido por Eldrath en Iktan y abandonado a medio dibujo cuando Naór exige partir.',
    'No se describe verbalmente el diseño ni una facultad mágica; se conserva separado de los tatuajes de Nox, Citlali y Tryel.',True,[
    stage('La mitad que se lleva a la expedición','Eldrath añade el tatuaje a sus compras y hace esperar a los compañeros ante la puerta de Iktan. Naór encuentra al minotauro trabajando en un dibujo solo terminado a medias y lo presiona para que dé por acabada la sesión. Se lleva al elfo y el propio grupo vuelve a señalar el tatuaje incompleto cuando se reúne para partir hacia la jungla. No se narra que durante la salida se complete o active.',[126,128,130])])
history('Cueva envenenada explorada por el grupo','lugar','Cueva abierta detrás de raíces en una pared rocosa de la jungla, con olor a podredumbre y veneno.',
    'Nombre editorial descriptivo. Tryel aporta el enlace con la cueva de su envenenamiento, ya relatada en 40-030, y reconoce el recorrido. La pertenencia a Clolgedranx sigue siendo una hipótesis del grupo, sin aparición del propietario.',True,[
    stage('Las pistas conducen a una entrada oculta','Tryel ha recordado una cueva donde se envenenó y los compañeros salen a buscar información que les sirva contra el dragón. Después de dar vueltas, Tesara encuentra ramas rotas y pisadas desacompasadas que se internan en la jungla. Eldrath observa una dirección más rocosa y con menos árboles. Al seguir esas señales, alcanzan una pared cubierta de raíces hasta la que llegan las huellas. Tryel reconoce elementos del recorrido, pero no se obtiene un nombre propio del lugar.',[114,115,136,137,140]),
    stage('El fuego y el primer veneno','Eldrath aparta parte de las raíces con una daga y nota un aire de hedor intenso. Tesara usa el fuego recibido de una fruta para quemar la vegetación, que se retuerce violentamente y deja paso a la cueva. Los viajeros entran para buscar pistas; una salvación de Constitución desemboca en cuatro puntos de daño de veneno para Tesara, mediante una adjudicación del chat. Conforme avanzan, el olor mezcla podredumbre y veneno y la luz exterior desaparece. Los elfos y Naór ven en la oscuridad; Tesara y Coyote apenas distinguen el interior.',[141,142,143,144,145,146,147])])

QUESTIONS = [
    dict(pregunta='¿Quién es el dragón al que Tesara atribuye el ataque antiguo y cómo se concilia su relato con el de Walulu?',
        respuesta='Los archivos proporcionan un ataque dracónico antiguo seguido de un ritual. El director estima cien o doscientos años, y Tesara habla expresamente del ataque de otro dragón que destruyó media ciudad. Walulu había referido ciento veinte años después del ataque del dragón en 47-082. No se da aquí nombre ni color del atacante.',
        referencias=['47-082','48-110','48-111','48-112'], pendiente='Identidad del atacante y conciliación de la atribución y la fecha sin convertir una estimación oral en un año exacto.'),
    dict(pregunta='¿Trabaja Clolgedranx para otro dragón y quién es ese supuesto patrón?',
        respuesta='Tesara dice que parece trabajar para otro dragón. La investigación no revela un nombre, y la afirmación no verifica la naturaleza del alguien que el dragón dijo que pagaba por los elfos.',
        referencias=['47-072','48-112'], pendiente='Identidad y naturaleza del empleador y motivo de su interés en Eldrath y Tryel.'),
    dict(pregunta='¿Cómo se realiza el ritual que impide la entrada de grandes dragones en Iktan?',
        respuesta='Tesara conoce su finalidad general después de leer los archivos, pero el director dice que no posee capacidad mágica suficiente para comprender todo el funcionamiento.',
        referencias=['48-110','48-111'], pendiente='Fórmula, ejecutantes identificados, ingredientes, duración y límites precisos del ritual.'),
    dict(pregunta='¿La cueva abierta tras las raíces es una guarida de Clolgedranx y coincide con la emboscada recordada por Tryel?',
        respuesta='El grupo sigue el recuerdo de Tryel, que enlaza con su testimonio de 40-030, y encuentra rastros hasta una cueva envenenada. Ella reconoce el recorrido y Eldrath la considera una de las guaridas del dragón; son identificaciones de los viajeros, sin aparición del propietario durante la llegada y primera entrada.',
        referencias=['40-030','48-114','48-136','48-140','48-141','48-144'], pendiente='Confirmación de propiedad y relación de sus habitantes o instalaciones con el dragón, conservando la identificación de Tryel con el lugar de su envenenamiento; cotejar con lo explorado después de 01:06:36.549.'),
    dict(pregunta='¿Quiénes son la tortuga que dirige las clases de calma y el minotauro que tatúa a Eldrath?',
        respuesta='La tortuga aparece pequeña y con gafas, sin nombre propio. El tatuador es identificado como minotauro, con una posible grafía Reotra en un saludo aislado.',
        referencias=['48-118','48-120','48-124','48-128'], pendiente='Nombres y confirmación de grafías sin identificarlos por especie u oficio con otros personajes.'),
    dict(pregunta='¿Se completará el tatuaje de Eldrath y qué efecto tiene?',
        respuesta='Naór lo saca de la tienda cuando el dibujo está a medias. Eldrath parte con él sin terminar.',
        referencias=['48-126','48-128','48-130'], pendiente='Diseño, coste, facultad y terminación o efectos de llevarlo incompleto; revisar continuación.'),
    dict(pregunta='¿Quiénes son los clientes que Eldrath toma por piratas de Shiaru y qué relación tienen con Molly?',
        respuesta='Eldrath sospecha por su aspecto y dice a Tryel que Molly parece juntarse con ellos. No se identifican nombres ni pertenencia a la ocupación de Shiaru.',
        referencias=['48-106','48-117'], pendiente='Identidades, procedencia efectiva, afiliación y relación concreta con Molly.'),
    dict(pregunta='¿Regresará Naór a tiempo para recoger a Leo?',
        respuesta='Naór fija las cinco y media como límite y avisa que se irá si la expedición se prolonga. Sale con el grupo y continúa presente al entrar en la cueva.',
        referencias=['48-123','48-131','48-147'], pendiente='Recogida efectiva, hora de regreso y continuidad de los cuidados del niño; cotejo con el resto de la sesión.'),
]

CONTRAS = [
    'Atribución histórica: 47-082 presenta el relato de Walulu sobre el ataque del dragón hace ciento veinte años; 48-110–48-112 ofrecen una estimación de cien o doscientos y la expresión de Tesara «otro dragón que destruyó media ciudad». Conservar ambas atribuciones sin identificar al atacante por inferencia.',
    'Empleador: 47-072 solo prueba que el dragón afirma que alguien paga por los elfos. En 48-112 Tesara dice que parece otro dragón. La naturaleza dracónica del patrón es una afirmación suya, no una identidad nueva comprobada.',
    'Telepatía: la frase ASR de 00:59:30.240–00:59:32.549 parece autorizar comunicación entre receptores después de decir que solo escuchan a Eldrath. La respuesta de que hará de antena establece la retransmisión como uso acordado; no ampliar a lectura libre de mentes.',
    'La actitud pacífica declarada por Naór al salir de las clases coexiste con los apretones, la intimidación al tatuador y el rugido posterior. Son intentos de control con recaídas en la misma mañana, no una curación estable o una segunda persona.'
]
NOMBRES = [
    'Naor/Naor Tarcan corresponde a Naór. Las referencias a Leona durante su clase se resuelven por la introducción explícita de Naór y su papel de madre de Leo; no incluir a Leona harengon en la expedición.',
    'Triel/Trier/Mirien son variantes o errores del diálogo referido a la hermana de Eldrath: se conserva Tryel en la redacción y la grafía original en las citas.',
    'Ilicar/Lilicar aparece en la recapitulación del entrenamiento de Naór. Es compatible con Ilikar por el nombre y la referencia posterior al goliat herido, pero no se crea una nueva identidad ni se usa como prueba nominal independiente.',
    'Miausi en el recuerdo del insulto se resuelve como Miaussy, la directora confirmada en el catálogo. Miausi, profesora registrada separadamente en el capítulo 46, no se fusiona por esta sola mención.',
    'Reotra es una posible grafía aislada para el minotauro tatuador. Se usa «Comerciante minotauro de Iktan» hasta cotejar audio o confirmación.',
    'La tortuga pequeña con gafas no se nombra. Se usa «Tortuga terapeuta del templo de Iktan» sin fusionarla con Tortas.',
    'Clolgedranx es el dragón verde del conflicto continuo; Zarynth sigue siendo el pequeño dragón de Aerendriel. Eldrath y Aerendriel tampoco se fusionan.',
    'Cueva envenenada explorada por el grupo es una etiqueta geográfica editorial; no se le adjudica el nombre de una cueva previa ni propiedad de Clolgedranx sin prueba adicional.'
]

# Cada una de estas preguntas se leyó completa, con su respuesta y su pendiente.
# El resultado es deliberadamente local a los minutos efectivamente leídos.
OBS = {
 'P05-001':'Molly está presente y es objeto de comentarios; no se lee el contrato con Bonny ni se mencionan copias o consecuencias jurídicas.',
 'P05-002':'La escena con Molly no presenta la nota de Nox ni noticias de su supervivencia al incendio.',
 'P05-003':'La presencia de Molly en Iktan añade un paradero, sin aportar un balance de supervivientes del buque incendiado.',
 'P05-007':'El interés de Tryel y Coyote por Molly no reconstruye el pasado entre ella y Nox.',
 'P04-008':'Hay efectos nuevos de frutas y Tesara quema raíces con uno de ellos. Ninguno fecha el fin de la segunda cola u otros efectos del capítulo 4.',
 'P07-007':'Las monedas modificadas por cartas del chat corresponden a Eldrath y Tesara, sin autor diegético. No explican las antiguas pérdidas de Patata y sus compañeros.',
 'P01-006':'El dragón estudiado y perseguido es el verde de Iktan; no se retoma la pronunciación de Zari o Tarin ni se identifica con Zarynth.',
 'P07-002':'Eztli se menciona en el repaso del encuentro escolar, sin precio, nuevo dato de especie o descubrimiento del pacto por Citlali.',
 'P12-006':'Las insinuaciones sobre Molly en la taberna no incluyen recepción o lectura de la carta de Nox.',
 'P12-002':'La presencia actual de Molly no modifica las evidencias anteriores sobre Aurora ni descifra los puntos del mapa.',
}

TRACK = []
for q in PREG:
    observation = OBS.get(q['id'])
    if observation is None:
        if q['estado'] == 'resuelta':
            observation = 'La lectura de 00:00:00.880 a 01:06:36.549 no vuelve a representar este desenlace ni aporta evidencia que lo contradiga; se conserva la resolución previa.'
        else:
            observation = 'La lectura de 00:00:00.880 a 01:06:36.549 no añade evidencia para resolver este extremo: ' + q['pendiente']
    TRACK.append(dict(id=q['id'], sha256_pregunta=q['sha256_pregunta'], pregunta=q['pregunta'],
        estado_previo=q['estado'], resultado='sin_novedad_en_lectura_asignada', observacion=observation,
        referencias=[], estado_propuesto=q['estado'], pendiente=q['pendiente']))

DELIVERY = dict(capitulo=48, bloque=1, lectura_completa=True, segmentos_leidos=len(SEG),
    primer_segmento=SEG[0]['id'], ultimo_segmento=SEG[-1]['id'], fuente_sha256=EXPECTED,
    inicio=SEG[0]['inicio'], fin=SEG[-1]['fin'],
    cobertura_lectura=dict(indices=list(range(1,len(SEG)+1)), segmentos=[s['id'] for s in SEG],
        tandas=[dict(desde=a,hasta=b) for a,b in [(1,180),(181,360),(361,540),(541,720),(721,900),(901,1080),(1081,1260),(1261,1420),(1421,1565)]]),
    identidades_contexto_leidas=len(CAT['grupos']), preguntas_asignadas_leidas=len(PREG),
    etapas=ETAPAS, afirmaciones=F, historias_entidades=H,
    misiones=[
        'Descubrir información y una debilidad de Clolgedranx para actuar antes de que expire el ultimátum: Tesara calcula que quedan seis días (48-107, 48-113).',
        'Investigar la cueva que recuerda Tryel, elegida por la urgencia frente a buscar otras guaridas o una gran biblioteca. Los cinco llegan a una cueva envenenada y empiezan a explorar, sin confirmar todavía propietario o identidad con la cueva antigua (48-114, 48-115, 48-140–48-147).',
        'Regresar a Iktan para recoger a Leo a las cinco y media, condición expresada por Naór. La recogida no ocurre antes de 01:06:36.549 y requiere cotejo con el resto de la sesión (48-123, 48-131).',
        'La posible petición de un ejército a Atlan permanece como propuesta verbal: no se envía un emisario en esta lectura (48-145).',
        'El aprendizaje de calma de Naór se practica con respiraciones y recibe apoyo económico de Walulu, pero sus reacciones posteriores muestran que aún no domina el enfado (48-118–48-123, 48-128, 48-133–48-134).'
    ], preguntas=QUESTIONS, contradicciones=CONTRAS, nombres_dudosos=NOMBRES,
    cotejo_preguntas_asignadas=TRACK,
    comprobaciones=dict(citas_validadas=0, evidencia_cue_literal=True, originales_sin_modificar=True,
        criterio_cobertura='Lectura secuencial completa de todos los segmentos de esta partición, incluidos recapitulación, bromas, cartas y reglas; no se infieren sucesos de los otros dos tramos.'))

for f in F:
    validate_fact(f, SOURCE)
    assert f['cita'] == f['evidencia_cue']['texto']
    assert any(f['evidencia_cue'] == dict(inicio=s['inicio'],fin=s['fin'],texto=s['texto_original']) for s in SEG)
assert len(TRACK) == 98 and len({x['id'] for x in TRACK}) == 98
assert len(SEG) == 1565 and SEG[-1]['id'] == 'c003129'
assert len(F) == len({x['id'] for x in F})
keys = {x['id'] for x in F}
for s in ETAPAS:
    assert set(s['referencias']) <= keys
for h in H:
    for s in h['etapas']: assert set(s['referencias']) <= keys
    if h['nueva']: assert any(h['nombre'] in f['entidades'] for f in F)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
DELIVERY['comprobaciones']['citas_validadas'] = len(F)
(BASE/'entrega_1.json').write_text(json.dumps(DELIVERY,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines = ['# Lectura completa del primer tramo del capítulo 48','',
    'Fuente original: `48 - FYarBX28XfI.es-orig.vtt`.', '',
    f'SHA-256 verificado antes y después: `{EXPECTED}`.', '',
    'Leídos completos 1.565 segmentos, 8.726 palabras, desde c000001 (00:00:00.880) hasta c003129 (01:06:36.549). La última tanda contiene los 145 segmentos restantes. También se han leído completas las 98 preguntas asignadas y las 209 entradas de identidades_contexto.json. Audio no cotejado.', '',
    'Tandas secuenciales sin omisiones: 1–180, 181–360, 361–540, 541–720, 721–900, 901–1080, 1081–1260, 1261–1420 y 1421–1565. La entrega incluye todos los índices e identificadores, 47 afirmaciones con evidencia literal, ocho etapas narrativas y quince historiales de entidad.', '',
    'Las 98 preguntas anteriores conservan su estado en esta lectura. El coordinador debe cotejar los otros tramos antes de adoptar el resultado de ausencia de evidencia como global. P31-001 no forma parte de la asignación de preguntas; requiere atención editorial por la atribución del ataque antiguo y la distinción entre el dragón presente, el atacante histórico y el supuesto empleador.', '',
    '## Relato propuesto','']
for s in ETAPAS:
    lines += ['### '+s['titulo'],'',s['texto'],'','Evidencias: '+', '.join(s['referencias'])+'.','']
lines += ['## Puntos para la integración','']
lines += ['- '+x for x in CONTRAS] + ['']
lines += ['- Nuevas etiquetas: Tortuga terapeuta del templo de Iktan; Comerciante minotauro de Iktan; Tatuaje incompleto de Eldrath; Cueva envenenada explorada por el grupo.',
    '- No se atribuye a los clientes de la taberna la ocupación de Shiaru. No se fusiona a la tortuga de gafas con Tortas ni al tatuador con otros comerciantes.',
    '- El fuego de Tesara procede de una fruta; la primera pérdida de vida por veneno se adjudica por una carta del chat. El enlace psiónico dura seis horas y requiere que Eldrath retransmita entre los receptores; Naór queda fuera.',
    '- Solo se han creado estos entregables locales; no se han modificado fuentes, catálogo o configuración y no se ha hecho commit, push o publicación.','']
(BASE/'lectura_bloque_1.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps(dict(afirmaciones=len(F),etapas=len(ETAPAS),historias=len(H),preguntas_cotejadas=len(TRACK),citas_validadas=len(F),sha256=EXPECTED),ensure_ascii=False))
