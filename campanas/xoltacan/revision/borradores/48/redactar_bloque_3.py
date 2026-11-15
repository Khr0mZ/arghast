import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import validate_fact, parse_vtt

SOURCE = ROOT / 'campanas/xoltacan/fuentes/48 - FYarBX28XfI.es-orig.vtt'
EXPECTED = '1fe4de4381f91a2e084979a969a5ac43d91a6c000b0d4379ed3755907844383d'
segments = json.loads((BASE / 'bloque_3_segmentos.json').read_text(encoding='utf-8'))
assigned = json.loads((BASE / 'preguntas_bloque_3.json').read_text(encoding='utf-8'))
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
assert len(segments) == 1566
facts = []

def fact(title, start, end, evidence, text, entities, kind='hecho_confirmado', limitation='La lectura corresponde a los subtítulos automáticos; audio no cotejado.', witnesses=None):
    cue = segments[evidence - 1]
    item = {
        'id': f'48-{301 + len(facts):03d}',
        'titulo': title, 'tipo': kind, 'afirmacion': text,
        'inicio': segments[start - 1]['inicio'], 'fin': segments[end - 1]['fin'],
        'cita': cue['texto_original'],
        'evidencia_cue': {'inicio': cue['inicio'], 'fin': cue['fin'], 'texto': cue['texto_original']},
        'entidades': entities,
        'ambito': 'exploración de la cueva envenenada y espera de Leo en Iktan',
        'conocedores': witnesses or [], 'conocimiento_personaje': 'desconocido',
        'nota_conocimiento': 'Acceso de Madame Oghma sin establecer en este pasaje.',
        'confianza': 'lectura íntegra de subtítulos; audio no cotejado', 'limitacion': limitation,
    }
    validate_fact(item, SOURCE)
    facts.append(item)
    return item['id']

CAVE = 'Cueva envenenada explorada por el grupo'
DEAD = 'No muertos de la cueva envenenada'
SNAKE = 'Serpiente esquelética de la cueva envenenada'
POISON = 'Muestras de veneno de la cueva envenenada'
FANG = 'Colmillo de la serpiente guardado por Naór'
TREASURE = 'Tesoro de la cueva envenenada'

fact('Un gran esqueleto junto al tesoro', 1, 13, 10,
     'La cámara contiene montones de objetos apenas visibles en la oscuridad, entre ellos lo que parece un escudo, y un enorme esqueleto en el centro. Tesara examina el entorno de huesos y raíces antes de aproximarse al tesoro.',
     ['Tesara Queen', CAVE, TREASURE, SNAKE], 'explicacion_director',
     'El escudo se percibe con poca luz. La descripción inicial no identifica todavía la criatura por su nombre ni prueba poderes de los objetos.')
fact('Tesara exige no pisar raíces ni huesos', 14, 45, 16,
     'Tesara pide avanzar despacio, sin tocar nada que no sea suelo: prohíbe pisar raíces, plantas y huesos o patear calaveras, y deja atrás a quien no pueda cumplirlo. Repite el aviso a Tryel y a los demás antes de acercarse a los objetos.',
     ['Tesara Queen', 'Tryel', CAVE], 'declaracion_personaje',
     'Es una precaución propuesta por Tesara, no una regla que demuestre qué activa a los enemigos.')
fact('Un destello ciega a Coyote', 61, 76, 74,
     'Coyote duda si tocar la pared y juega con esa posibilidad. Al mirar ve un destello muy intenso que le impide ver; el director confirma la ceguera temporal que condicionará sus primeras intervenciones.',
     ['Coyote', CAVE], 'explicacion_director',
     'El lenguaje del destello es jocoso y no fija criatura, conjuro o responsable; no se establece que Coyote haya tocado la pared.')
fact('Los vapores dejan a Tesara sin oír', 77, 90, 82,
     'Tesara se separa del grupo para registrar el tesoro. Las salidas de vapor de las charcas de veneno producen un sonido tan fuerte que el director la deja sorda durante un rato, mientras sus compañeros permanecen atrás y Coyote sigue ciego.',
     ['Tesara Queen', 'Coyote', CAVE], 'explicacion_director',
     'La sordera se adjudica al ruido de las salidas de las charcas; no equivale a una lesión permanente.')
fact('No hay huellas identificadas en el suelo de roca', 100, 129, 127,
     'Un compañero intenta averiguar si los esqueletos dejaron huellas. El director aclara que desde esa posición solo se ven huesos sobre roca y corrige la interpretación de que exista un rastro de pisadas que seguir.',
     [CAVE, DEAD], 'explicacion_director',
     'El hablante no se identifica con seguridad en este intercambio; no se inventa un recorrido ni se niega que pueda investigarse otra zona.')
fact('Tesara busca pistas entre un botín corroído', 146, 183, 173,
     'Tesara busca algo relacionado con el dragón que destaque sobre el oro. Remueve los objetos con el mango del látigo procurando hacer poco ruido. Encuentra que parte del tesoro está corroída y destrozada, aunque algunos objetos siguen sorprendentemente bien conservados.',
     ['Tesara Queen', CAVE, TREASURE, 'Clolgedranx'], 'explicacion_director',
     'La intención de buscar una pista no demuestra que la encuentre, y la corrosión no recibe un análisis de causa.')
fact('Naór intenta recorrer la pared con las garras', 231, 250, 249,
     'Naór intenta evitar el suelo escalando la pared con las garras de manos y pies. Solo alcanza unos pocos pies de altura; el director la sitúa a cinco pies del suelo.',
     ['Naór', CAVE], 'hecho_confirmado',
     'La comparación del suelo con lava es una broma del grupo, no una propiedad de la cámara.')
fact('La serpiente sorprende al grupo', 260, 275, 269,
     'Mientras Tesara registra los objetos y los demás se distraen, el director pide iniciativa y declara al grupo sorprendido. Naór puede responder al entrar en furia; el resto pierde su primera oportunidad de actuar.',
     ['Naór', 'Tesara Queen', 'Eldrath', 'Tryel', 'Coyote', SNAKE, CAVE], 'explicacion_director',
     'Se conserva la adjudicación mecánica de sorpresa; no se identifica una trampa concreta ni el gesto exacto que inició el ataque.')
fact('La furia de Naór permite lanzar su arma', 276, 305, 294,
     'La furia de Naór infunde su arma con magia: brilla, su daño pasa a fuerza y obtiene la posibilidad de lanzarla y recuperarla en la mano. Naór la utiliza para iniciar el ataque contra la serpiente.',
     ['Naór', SNAKE], 'explicacion_director',
     'Son efectos temporales adjudicados a esa furia, no una transformación permanente del hacha. La broma de lanzar aliados no se ejecuta.')
fact('La serpiente muerde y enrosca a Naór', 326, 372, 366,
     'La serpiente aprovecha la sorpresa para morder a Naór. Después la golpea con la cola, la derriba y vuelve a pasarla para enroscarla, dejándola apresada y restringida. El grupo todavía no puede intervenir en esa primera ronda.',
     ['Naór', SNAKE], 'hecho_confirmado',
     'Los nombres grapple y restrained pertenecen a la adjudicación del combate; no se añade una especie de bestiario o anatomía no descrita.')
fact('Tesara guarda un collar antes de advertir el combate', 379, 412, 396,
     'Todavía sorda, Tesara sigue buscando una pista en el tesoro y guarda un collar. Al terminar se incorpora y se vuelve para anunciar que solo encontró un par de baratijas; entonces descubre la escena del ataque. Al pasar su turno recupera la audición.',
     ['Tesara Queen', TREASURE, CAVE, SNAKE], 'hecho_confirmado',
     'La aparición del collar no acredita valor, poderes, inscripción o destino para Angelique; tampoco agota todo el tesoro disponible.')
fact('Naór contraataca a pesar del abrazo de la serpiente', 413, 468, 453,
     'Naór se levanta y responde estando aún restringida. Encadena varios impactos críticos y nuevos ataques mediante recursos de combate y una carta, aunque los últimos golpes fallan. Mantiene la lucha pese al veneno y la presión de la cola.',
     ['Naór', SNAKE], 'hecho_confirmado',
     'La carta forma parte de la intervención externa del chat y de la mesa; no se la convierte en objeto o aliado del mundo. No se reconstruye daño acumulado a partir de tiradas parciales.')
fact('La primera oleada de veneno se resiste', 470, 492, 491,
     'La serpiente usa una acción legendaria que obliga a quienes están en la sala a resistir veneno. El director permite ventaja a quienes habían bebido antitoxina. En la conversación se aclara que se repartieron tres dosis a los compañeros considerados más vulnerables y ninguna a Naór; las salvaciones de esa oleada se superan.',
     ['Naór', 'Tesara Queen', 'Coyote', 'Tryel', 'Eldrath', SNAKE, CAVE], 'explicacion_director',
     'La antitoxina concede una ventaja mecánica en esa tirada, sin demostrar inmunidad ni resistencia permanente. La distribución exacta debe cotejarse con el tramo anterior.')
fact('Coyote inspira a Tryel mientras sigue sin ver', 493, 537, 503,
     'Coyote permanece tumbado y ciego junto a Tryel. Al enterarse de que están siendo atacados le concede inspiración bárdica por el contacto próximo, pero su falta de visión limita las otras acciones que considera. Eldrath le exige que deje de manosear a su hermana y ayude contra la serpiente.',
     ['Coyote', 'Tryel', 'Eldrath', SNAKE], 'hecho_confirmado',
     'La identificación de Tryel se apoya en la queja explícita del hermano y la continuidad del diálogo; las bromas no crean un nuevo vínculo sentimental.')
fact('La constricción continúa dañando a Naór', 538, 589, 582,
     'La serpiente vuelve a morder a Naór y la sigue apretando con la cola. El director aclara que quitar el icono de restricción fue un error y que continúa apresada; la constricción causa daño cada turno y ocupa la cola del enemigo.',
     ['Naór', SNAKE], 'explicacion_director',
     'Se distingue la corrección de la interfaz del estado narrativo: no hubo una liberación en el momento de quitar el icono. La curación de una carta externa no se atribuye a otro personaje.')
fact('Eldrath dispara con sus dagas y se reposiciona', 590, 609, 604,
     'Eldrath apunta con una daga y dispara. Falla un primer intento y acierta con la otra mano para ayudar a Naór; después cambia de posición.',
     ['Eldrath', 'Naór', SNAKE], 'hecho_confirmado',
     'El arma se mantiene dentro de la continuidad de las dagas de Eldrath, sin añadir poderes distintos a los observados.')
fact('Tryel crea duplicados antes de acercarse', 610, 619, 614,
     'Tryel se toca y aparecen varias imágenes de ella. Se acerca entonces a la serpiente para atacarla con la espada, utilizando los duplicados como defensa para dificultar que la alcancen.',
     ['Tryel', SNAKE], 'hecho_confirmado',
     'Son imágenes mágicas, no personas nuevas. El pasaje no detalla la duración total del efecto.')
fact('El grito de la serpiente despierta esqueletos menores', 620, 629, 628,
     'Al terminar la ronda, la serpiente que tiene apresada a Naór empieza a chillar y gruñir. A su alrededor despiertan pequeños esqueletos que se incorporan al combate.',
     ['Naór', SNAKE, DEAD, CAVE], 'explicacion_director',
     'Se narra una secuencia de grito y despertar; no se establece un ritual, creador último o equivalencia con los muertos de otros lugares.')
fact('Tesara flanquea para intentar liberar a Naór', 630, 674, 633,
     'Tesara considera prioritario rescatar a Naór. Activa sus recursos, corre hacia el lado opuesto al de Tryel y dispara a la serpiente para dividir su atención y conseguir que suelte a la leonina.',
     ['Tesara Queen', 'Naór', 'Tryel', SNAKE], 'declaracion_personaje',
     'El efecto de distraerla es el propósito declarado, sin una liberación confirmada en ese turno; las cartas de ayuda se mantienen como recursos de mesa.')
fact('Tesara y Tryel quedan envenenadas', 702, 718, 713,
     'Una nueva oleada de veneno exige salvaciones de Constitución. Esta vez Tesara y Tryel quedan envenenadas y el director añade que no pueden recuperar puntos de vida mientras mantengan ese efecto.',
     ['Tesara Queen', 'Tryel', SNAKE], 'explicacion_director',
     'La prohibición de curación corresponde al efecto concreto adjudicado; no se formula como una regla universal de todo veneno.')
fact('Coyote recupera la vista y se acerca a ayudar', 728, 755, 730,
     'Coyote se frota los ojos y recupera la vista. Al contemplar lo ocurrido se aproxima a Naór y le presta ayuda; también concede inspiración a Tesara antes de que vuelva a actuar la serpiente.',
     ['Coyote', 'Naór', 'Tesara Queen', SNAKE], 'hecho_confirmado',
     'La transcripción no permite fijar con suficiente claridad el nombre de toda la primera ayuda usada sobre Naór. La inspiración a Tesara se confirma cuando ella gasta después el dado.')
fact('Naór cae y la serpiente deja de retenerla', 756, 785, 770,
     'La serpiente mantiene su presión y sus ataques hasta que Naór cae al suelo. La restricción termina y el enemigo puede volver su atención hacia otros compañeros. Una intervención de Silvery Barbs acompaña la respuesta del grupo.',
     ['Naór', SNAKE, 'Coyote', 'Eldrath'], 'hecho_confirmado',
     'La caída aparece reconocida en el diálogo y en el turno posterior de Tryel; no se interpreta como muerte. No se fija el destinatario de cada reacción a partir de palabras incompletas.')
fact('Eldrath se separa de un esqueleto y ataca a la serpiente', 786, 837, 808,
     'Eldrath emplea su acción adicional para destrabarse de un esqueleto y alejarse sin recibir su ataque. A continuación dispara con ventaja a la serpiente y aplica ataque furtivo, intentando acabar con ella antes de que hiera a más compañeros.',
     ['Eldrath', SNAKE, DEAD], 'hecho_confirmado',
     'Al haber gastado su acción adicional no realiza el segundo ataque que había considerado. No se adjudica todavía la muerte de la serpiente.')
fact('Tryel levanta a Naór', 839, 856, 848,
     'En su turno Tryel llama a Naór para que se levante y emplea ayuda para reincorporarla a la lucha. Después intenta golpear a un enemigo, todavía con la desventaja del envenenamiento.',
     ['Tryel', 'Naór', SNAKE, DEAD], 'hecho_confirmado',
     'El diálogo identifica al objetivo como el gatito caído y la continuación muestra a Naór levantarse; no se inventa el nombre del recurso o una recuperación completa.')
fact('Tesara cruza una poza colgada del látigo', 858, 908, 905,
     'Tesara propone enganchar el látigo a una estalactita para saltar la poza y disparar desde detrás de la serpiente. Suelta la antorcha y usa la inspiración de Coyote para completar la maniobra. Consigue balancearse hasta el otro lado y saca la pistola mientras cuelga.',
     ['Tesara Queen', 'Coyote', SNAKE, CAVE], 'hecho_confirmado',
     'El salto se resuelve con las tiradas que pide el director; no se identifica por nombre la pistola en este pasaje.')
fact('El disparo derriba a la serpiente, pero resiste', 909, 954, 946,
     'El disparo de Tesara impacta a pesar de la desventaja y el director anuncia primero que cae la serpiente. Después aclara que sigue en pie con un punto de vida: ha resistido el golpe de forma semejante a los zombis, por lo que el combate aún no termina.',
     ['Tesara Queen', SNAKE], 'explicacion_director',
     'El primer anuncio de caída se corrige explícitamente. No se atribuye a Tesara un remate definitivo ni se importa un rasgo de bestiario externo.')
fact('Naór remata a la serpiente y disimula el golpe', 955, 979, 973,
     'Naór se levanta, ve que la serpiente todavía se mueve y la golpea cuando intenta incorporarse. Procura que el remate parezca accidental y felicita a Tesara como si ella hubiera acabado con la criatura.',
     ['Naór', 'Tesara Queen', SNAKE], 'hecho_confirmado',
     'La felicitación de Naór es parte del disimulo: la secuencia representa a Naór completando la derrota después del disparo de Tesara.')
fact('Naór encadena ataques contra los esqueletos', 980, 1014, 1009,
     'Tras el remate Naór arroja el hacha y encadena nuevos impactos críticos contra los esqueletos próximos. Acaba ayudando a Tesara a incorporarse y continúa atribuyéndole con humor el mérito de la victoria.',
     ['Naór', 'Tesara Queen', DEAD], 'hecho_confirmado',
     'El blanco de cada tirada no se nombra con suficiente claridad para dar identidades individuales a los esqueletos o contar bajas por separado.')
fact('Eldrath arrebata a Tryel el último remate', 1030, 1063, 1058,
     'Eldrath se acerca a su hermana y prepara una maniobra conjunta. Tryel le advierte que no toque al enemigo, pero él le responde que nunca le hace caso y mata con un golpe crítico al esqueleto que ella tenía enfrente. El cuerpo se deshace delante de Tryel.',
     ['Eldrath', 'Tryel', DEAD], 'hecho_confirmado',
     'Se documenta la disputa entre hermanos sin convertir el esqueleto anónimo en un personaje diferente por cada intervención.')
fact('Tryel paraliza y golpea a Eldrath', 1064, 1116, 1103,
     'Tryel ordena a Eldrath que se quede quieto y lo paraliza. Guarda las espadas, se acerca con los puños y le da una paliza de cachetes y puñetazos, expresamente sin matarlo. Después lo suelta y él cae sentado, dolorido y enfadado. Los demás observan la represalia.',
     ['Tryel', 'Eldrath', 'Naór', 'Tesara Queen', 'Coyote'], 'hecho_confirmado',
     'La amenaza de matarlo y los críticos se usan en broma; el director precisa que no lo mata. El intento de hablar mentalmente con Naór se corrige porque no estaban conectados.')
fact('Tesara no encuentra marcas en la serpiente derrotada', 1117, 1153, 1134,
     'Tesara investiga el esqueleto de la serpiente buscando marcas, residuos o una pista del método con que cree que el dragón la controla. Su examen arcano no revela nada extraño y tampoco encuentra una marca física; el director la describe simplemente como un esqueleto de serpiente. Tesara amplía después la búsqueda al resto de la sala.',
     ['Tesara Queen', SNAKE, CAVE, 'Clolgedranx'], 'explicacion_director',
     'El control por el dragón es una intuición de Tesara. El resultado negativo de esa tirada no demuestra ausencia absoluta de magia ni un mecanismo de animación conocido.')
fact('Naór conserva un colmillo para Leo', 1155, 1164, 1162,
     'Naór quiere llevarle a Leo un recuerdo y arranca un colmillo de la serpiente derrotada para guardarlo. Más tarde Coyote recuerda que ella tomó solo uno, dejando otro en la criatura.',
     ['Naór', 'Leo', SNAKE, FANG], 'hecho_confirmado',
     'No se representa la entrega a Leo ni se demuestra que el colmillo tenga un poder propio.')
fact('Naór percibe una magia antigua que se apaga', 1165, 1185, 1182,
     'Al buscar con su detección, Naór percibe en esta sala una magia antigua y muy tenue, distinta de la ausencia de señal en las otras cámaras. El director la compara con la que pudo notar al ver al dragón y describe que se está apagando y desapareciendo.',
     ['Naór', CAVE, 'Clolgedranx'], 'explicacion_director',
     'La comparación no identifica una runa, objeto o foco concreto ni demuestra un vínculo causal con las pozas.')
fact('Naór deja la investigación para recoger a Leo', 1186, 1208, 1191,
     'Naór avisa a Eldrath de que hay una pista oculta en la sala y emprende el regreso por el camino de entrada. Se marcha porque debe atender la recogida de Leo; el diálogo alude a las cinco y cuarto y anticipa que llegará tarde.',
     ['Naór', 'Eldrath', 'Leo', CAVE, 'Colegio de Iktan'], 'declaracion_personaje',
     'El aviso expresa la interpretación de Naór; no prueba que exista un objeto escondido. Todavía no se representa su llegada al colegio.')
fact('Tryel y Coyote continúan buscando en el tesoro', 1209, 1236, 1223,
     'Eldrath se disculpa ante Tryel por haber rematado al enemigo, mientras ella sigue registrando el tesoro. Coyote se ofrece a ayudarla y excava entre los objetos. El hallazgo previo de un collar por Tesara no significaba que no quedase nada: el director aclara que solo describía su búsqueda de seis segundos.',
     ['Eldrath', 'Tryel', 'Coyote', 'Tesara Queen', TREASURE, CAVE], 'hecho_confirmado',
     'La mención a una copa está entrecortada y no fija material, valor, propiedades o una identificación con copas anteriores.')
fact('La sala no contiene las inscripciones que buscan', 1237, 1272, 1271,
     'Eldrath busca objetos o superficies con inscripciones dracónicas intentando explicar la señal que detectó Naór. Tesara recuerda que también está buscando grabados o un pasadizo. El director descarta esa vía: es una cueva y no hay inscripciones en ningún lado.',
     ['Eldrath', 'Tesara Queen', CAVE, TREASURE], 'explicacion_director',
     'La búsqueda de runas es una hipótesis, sin texto dracónico encontrado. No se generaliza el descarte de inscripciones a toda otra cueva de la campaña.')
fact('Tesara detecta el mismo rastro en toda la cámara', 1273, 1321, 1315,
     'Eldrath comunica a Tesara que Naór solo describió una presencia mágica tenue antes de salir corriendo. Coyote explica que no dispone de una habilidad que le sirva para rastrearla y la consulta a Mirien tampoco ofrece solución. Tesara realiza su propio examen arcano y percibe una magia tenue que desaparece por toda la sala, sin una dirección o foco localizado.',
     ['Eldrath', 'Tesara Queen', 'Coyote', 'Naór', CAVE], 'explicacion_director',
     'Mirien se conserva como nombre dudoso del interlocutor y no se abre una entidad nueva sin contexto suficiente. Coyote no declara carecer de toda magia, solo de la habilidad útil para este rastreo.')
fact('El director separa el rastro mágico de las pozas', 1322, 1443, 1415,
     'El director orienta al grupo mediante preguntas: los dragones desprenden magia y la señal que se disipa apunta a que el dragón se ha ido. También aclara que esa magia no tiene relación con las pozas. Al margen del rastro, propone pensar en el veneno como material para futuros antídotos; las teorías de un ojo vigilante o una planta protectora no se confirman.',
     [CAVE, 'Clolgedranx', POISON], 'explicacion_director',
     'Son pistas dadas a la mesa, no una aparición del dragón ni un hallazgo plenamente deducido por los personajes. La palabra que responde a la habilidad del dragón verde no es inequívoca en el subtítulo; no se completa con lore externo.')
fact('Eldrath llena su cantimplora de veneno', 1444, 1465, 1453,
     'Eldrath vacía su cantimplora de agua y la llena con veneno de una de las pozas. La guarda para que pueda servir en la preparación de pociones contra el dragón verde; la cantidad de la cantimplora se maneja como equivalente a cuatro sorbos.',
     ['Eldrath', CAVE, POISON, 'Clolgedranx'], 'hecho_confirmado',
     'Recolectar el líquido no es fabricar un antídoto; los cuatro sorbos no garantizan cuatro pociones o cuatro protecciones eficaces.')
fact('Tesara recoge una segunda muestra de las pozas', 1469, 1493, 1483,
     'Tesara pregunta por la utilidad del veneno. Eldrath explica que quiere disponer del propio veneno del dragón para preparar pociones con las que combatirlo. Ella considera buena la idea, vacía su propia cantimplora y recoge más, prefiriendo que sobre material al enfrentarse a un dragón.',
     ['Tesara Queen', 'Eldrath', CAVE, POISON, 'Clolgedranx'], 'hecho_confirmado',
     'La atribución del líquido al dragón y su utilidad futura se expresan como explicación del personaje; no existe análisis, receta o ensayo de eficacia en este tramo.')
fact('Coyote obtiene veneno del colmillo restante', 1494, 1519, 1501,
     'Coyote también vacía su recipiente de agua, pero elige obtener la muestra de la serpiente en vez de acudir a la poza. Utiliza el colmillo que queda después de la extracción de Naór y guarda el veneno en una botellita.',
     ['Coyote', 'Naór', SNAKE, POISON], 'hecho_confirmado',
     'No se equipara químicamente esta muestra a la de las pozas, al veneno del claro o a los viales de los sacerdotes; tampoco se identifica el procedimiento como suficiente para fabricar un remedio.')
fact('Los compañeros abandonan la cueva heridos', 1520, 1538, 1536,
     'Después de recoger las muestras los compañeros acuerdan marcharse cuanto antes: reconocen que están debilitados y alguno se encuentra mal. Inician el camino de vuelta mientras la narración regresa a Iktan.',
     ['Tesara Queen', 'Eldrath', 'Tryel', 'Coyote', CAVE, POISON, 'Iktan'], 'hecho_confirmado',
     'Emprender el regreso no demuestra que todo el grupo haya llegado ya a la ciudad, descansado o neutralizado el veneno.')
fact('Leo espera y Naór sigue corriendo por la jungla', 1539, 1566, 1551,
     'En la puerta del colegio de Iktan una mujer felina espera impaciente con libros y carpetas, acompañada por Leo. Dice que su madre volverá a llegar tarde. Al mismo tiempo Naór corre a toda prisa por la jungla, apartando ramas de su cara e insistiendo en que ya llega. La sesión termina antes del encuentro.',
     ['Naór', 'Leo', 'Colegio de Iktan', 'Iktan'], 'explicacion_director',
     'La mujer no recibe nombre en este epílogo; no se la identifica automáticamente con Miaussy o Miausi. No se representa la entrega del colmillo, la recogida de Leo o una reunión de madres.')

def refs(*nums):
    return [f'48-{n:03d}' for n in nums]

stages = [
    {'titulo': 'Precauciones ante el tesoro', 'texto': 'La última cámara reúne raíces, huesos y objetos apenas visibles en la oscuridad. Entre el botín parece haber un escudo y en el centro destaca un enorme esqueleto. Tesara insiste en que nadie pise raíces, plantas o huesos, ni toque nada que no sea suelo. Su intención es llegar hasta los objetos sin provocar otra amenaza y encontrar una pista sobre el dragón. La disciplina dura poco. Coyote se entretiene dudando si tocar la pared y un destello lo deja ciego; Tesara, que se ha separado para registrar los montones, queda temporalmente sorda por el ruido de las salidas de vapor de las charcas. La roca no ofrece el rastro de pisadas que otro compañero espera ver: el director aclara que solo se distinguen huesos. Tesara remueve con el mango del látigo un tesoro en parte corroído, aunque todavía contiene algunas piezas bien conservadas. Naór intenta evitar el suelo trepando con las garras, pero apenas consigue elevarse unos pies.', 'referencias': refs(301,302,303,304,305,306,307)},
    {'titulo': 'La serpiente aprisiona a Naór', 'texto': 'La serpiente sorprende al grupo mientras sus integrantes miran el tesoro o se distraen. Naór logra reaccionar al entrar en furia: su arma brilla y puede lanzarla para que regrese a su mano. El enemigo concentra en ella el ataque, la muerde, la derriba con la cola y la enrosca hasta dejarla restringida. Tesara continúa buscando sin escuchar lo que sucede y guarda un collar; cuando se vuelve para anunciar que solo encontró baratijas se descubre por fin ante la pelea. Naór responde desde el abrazo de la criatura con una sucesión de golpes, varios de ellos críticos, y agota recursos para sostenerse. La serpiente fuerza al grupo a resistir otra oleada de veneno. Las antitoxinas ayudan a los que las bebieron, aunque Naór se quedó sin una de las tres dosis repartidas. Coyote, todavía ciego y tumbado junto a Tryel, consigue inspirarla, pero apenas puede orientar el resto de su ayuda.', 'referencias': refs(308,309,310,311,312,313,314)},
    {'titulo': 'Esqueletos y veneno en la cámara', 'texto': 'La serpiente mantiene a Naór atrapada y le inflige daño con cada nueva presión de la cola. Eldrath le dispara con las dagas y se reposiciona; Tryel crea imágenes de sí misma antes de acercarse con la espada. Al acabar la ronda el grito de la serpiente acompaña el despertar de pequeños esqueletos, que se suman a la lucha y dispersan la atención de los viajeros. Tesara decide que liberar a Naór es lo más urgente y corre al lado opuesto de Tryel para disparar y dividir la atención del enemigo. Una nueva oleada de veneno alcanza a ambas mujeres y, mientras dure el efecto, les impide recuperar vida. Coyote vuelve a ver, se acerca a ayudar y deja una inspiración en manos de Tesara. Naór termina cayendo bajo el castigo de la serpiente. Eldrath abandona el alcance de uno de los esqueletos y vuelve a atacar al enemigo mayor; Tryel ayuda a la leonina a reincorporarse.', 'referencias': refs(315,316,317,318,319,320,321,322,323,324)},
    {'titulo': 'Un disparo en pleno balanceo y el golpe que lo completa', 'texto': 'Tesara decide cruzar una poza colgada del látigo. Suelta la antorcha, engancha el arma a una estalactita y utiliza la inspiración de Coyote para completar el balanceo. Desde allí saca la pistola con la otra mano y dispara por detrás a la serpiente. El impacto parece derribarla, pero el anuncio se corrige: la criatura aún resiste con un punto de vida y trata de levantarse. Naór, ya reincorporada, detecta el movimiento y la remata con un golpe que procura disimular. Felicita a Tesara como si ella hubiera concluido la faena y continúa de inmediato lanzando el hacha contra los esqueletos. Tras nuevos impactos ayuda a la historiadora a levantarse y sigue atribuyéndole con humor el mérito de la victoria.', 'referencias': refs(325,326,327,328)},
    {'titulo': 'La revancha entre los hermanos', 'texto': 'El combate desemboca en una disputa entre Eldrath y Tryel. Ella quiere acabar con el enemigo que tiene delante y le advierte que no intervenga; él sonríe, recuerda que nunca le hace caso y destruye al esqueleto con un golpe crítico. Tryel lo mira, le ordena que se quede quieto y lo paraliza. Guarda las espadas, se acerca crujiéndose los nudillos y le descarga cachetes y puñetazos mientras los demás contemplan la represalia. El director deja claro que no lo mata. Cuando lo suelta, Eldrath cae sentado, se sujeta el estómago y se aparta enfadado. Más tarde intenta disculparse: asegura que no esperaba ser quien rematase al adversario y que normalmente es ella quien lo hace. Tryel prosigue entretanto con la búsqueda del tesoro.', 'referencias': refs(329,330,335)},
    {'titulo': 'Una huella mágica que se desvanece', 'texto': 'Tesara examina a la serpiente derrotada buscando una marca o un residuo que revele cómo podría controlarla el dragón, pero no encuentra nada extraño. Amplía el registro a las paredes y al resto de la sala. Naór arranca un colmillo como recuerdo para Leo y percibe después una magia antigua, muy tenue, semejante a la que pudo notar ante el dragón. La señal está desapareciendo. Antes de que puedan concretarla, Naór avisa a Eldrath y emprende el regreso: tiene que recoger al niño y teme llegar tarde. Los que permanecen buscan inscripciones dracónicas o un foco escondido entre los objetos, sin resultado. Coyote no dispone de una habilidad que permita seguir ese rastro. Tesara lo examina por sí misma y confirma que impregna toda la cámara, sin dirección definida. Las pistas del director separan esta señal del veneno de las pozas y la relacionan con la magia que desprenden los dragones y su ausencia reciente; las teorías sobre ojos vigilantes, runas o plantas protectoras no llegan a confirmarse.', 'referencias': refs(331,332,333,334,336,337,338)},
    {'titulo': 'Veneno para una preparación futura', 'texto': 'El tesoro todavía ofrece objetos y Coyote ayuda a Tryel a removerlo, pero la exploración encuentra una utilidad más concreta en el líquido de las pozas. Eldrath vacía su cantimplora y recoge veneno para una futura preparación contra el dragón verde. Explica a Tesara que disponer de su propio veneno podría servir para elaborar pociones con las que combatirlo. Ella imita la recogida y prefiere llevar material de sobra. Coyote utiliza otro recipiente, aunque obtiene su muestra del colmillo que queda en la serpiente, después de que Naór arrancase el otro. Ninguna de estas recogidas produce todavía un remedio ni prueba que los líquidos sean equivalentes. Los viajeros, heridos y debilitados, acuerdan dejar la cueva y emprenden el camino de regreso.', 'referencias': refs(335,339,340,341,342)},
    {'titulo': 'Leo espera a la salida del colegio', 'texto': 'En Iktan, una mujer felina espera con libros y carpetas en la puerta del colegio, marcando con el pie su impaciencia. Leo está a su lado y escucha que su madre volverá a llegar tarde. Naór todavía corre por la jungla a toda prisa, con las ramas golpeándole la cara y repitiendo que ya llega. La aventura termina antes de que pueda alcanzar al niño, entregar su recuerdo o explicar el retraso.', 'referencias': refs(343)},
]

def entity(name, typ, description, note, new, entries):
    return {'nombre': name, 'tipo': typ, 'descripcion': description, 'nota': note, 'nueva': new,
            'etapas': [{'titulo': title, 'texto': text, 'referencias': refs(*numbers)} for title, text, numbers in entries]}

histories = [
    entity('Tesara Queen','personaje','Historiadora humana de Puerto de Espadas que investiga al dragón y explora con sus compañeros.',
           'Tesa y las variantes de la transcripción mantienen la identidad editorial Tesara Queen. La pistola utilizada aquí no se renombra por conjetura.',False,[
        ('La cautela se rompe ante el tesoro','Tesara intenta imponer una entrada cuidadosa en la cámara y se adelanta para buscar algo que explique al dragón. Encuentra objetos corroídos y algunas piezas conservadas, pero los vapores la dejan sorda. Guarda un collar sin enterarse al principio de que la serpiente ha apresado a Naór. Al girarse descubre la urgencia y abandona la búsqueda para ayudar.',[302,304,306,311]),
        ('Del rescate a la investigación del rastro','Trata de dividir la atención de la serpiente junto a Tryel, resulta envenenada y después cruza una poza balanceándose del látigo. El disparo que hace colgada derriba al enemigo, aunque todavía necesita el remate de Naór. Al terminar investiga el esqueleto y la cámara sin hallar marcas o inscripciones. Confirma una magia tenue que se apaga por toda la sala, y recoge veneno de una poza al aceptar la idea de preparar futuras pociones contra el dragón. Sale debilitada con los demás.',[319,320,325,326,327,331,336,337,340,342]),
    ]),
    entity('Naór','personaje','Princesa leonina de Atlan y madre adoptiva de Leo.',
           'Se conserva Naór, distinta de Leona y de Nox. La recogida de Leo no llega a representarse.',False,[
        ('Sostener el ataque de la serpiente','Naór intenta primero recorrer la pared con las garras. Al comenzar la emboscada entra en furia, infunde su arma y responde a la serpiente mientras sus compañeros están sorprendidos. Recibe mordiscos, queda atrapada por la cola y combate desde la restricción. Después de caer y recibir la ayuda de Tryel se levanta y remata al enemigo que había resistido el disparo de Tesara. Disimula el golpe para darle el mérito a su compañera y continúa atacando a los esqueletos.',[307,308,309,310,312,315,322,324,327,328]),
        ('Un recuerdo y una carrera para llegar al colegio','Guarda un colmillo de la serpiente para Leo. Su detección revela una magia antigua que se desvanece en la cámara, pero debe dejar la investigación a Eldrath y los demás para volver junto al niño. La narración la sigue corriendo por la jungla, todavía sin alcanzar el colegio, donde Leo y una mujer felina la esperan.',[332,333,334,343]),
    ]),
    entity('Eldrath','personaje','Elfo hermano de Tryel, combatiente con dagas y capacidades psíquicas.',
           'Eldrat y otras variantes de los subtítulos se conservan solo en las citas; el nombre confirmado es Eldrath, distinto de Aerendriel.',False,[
        ('Apoyar a Naór y provocar a Tryel','Dispara a la serpiente con sus dagas y se mueve para evitar quedar atrapado por los esqueletos. Después de gastar su acción adicional en separarse de uno de ellos, vuelve a atacar con ventaja al enemigo mayor. Al final arrebata a Tryel el remate de otro esqueleto, pese a su advertencia. Su hermana lo paraliza y lo golpea sin matarlo; él queda dolorido y termina intentando disculparse.',[316,323,329,330,335]),
        ('Un material para el próximo enfrentamiento','Recibe el aviso de Naór sobre la magia tenue e intenta encontrar inscripciones dracónicas, sin éxito. No logra explicar por completo el rastro que desaparece. Sí recoge veneno de una poza en su cantimplora y propone usarlo para futuras pociones contra el dragón verde. Comparte la idea con Tesara y sale de la cueva con los compañeros, sin haber fabricado o probado todavía un remedio.',[334,336,337,338,339,340,342]),
    ]),
    entity('Tryel','personaje','Elfa hermana de Eldrath que combate con espada y utiliza magia.',
           'El nombre confirmado es Tryel; las citas conservan Triel y otras variantes. Las imágenes mágicas no son personajes nuevos.',False,[
        ('Imágenes defensivas y ayuda para Naór','Tryel recibe la inspiración de Coyote, crea duplicados de sí misma y se aproxima a la serpiente con la espada. Los esqueletos que despiertan añaden nuevos frentes; la oleada de veneno la alcanza junto a Tesara e impide que recupere vida mientras dure el efecto. Cuando Naór cae, interviene para levantarla y mantener al grupo en combate.',[314,317,318,320,324]),
        ('El remate que exige a su hermano','Eldrath ignora su advertencia y mata al esqueleto que ella tenía delante. Tryel lo paraliza y le da una paliza sin matarlo mientras los demás miran; después lo deja caer sentado. Más tarde sigue buscando entre los objetos, recibe la oferta de ayuda de Coyote y escucha las disculpas del hermano. El grupo deja la cueva sin una curación completa representada.',[329,330,335,342]),
    ]),
    entity('Coyote','personaje','Cambiaformas de Iktan que acompaña al grupo y utiliza inspiración y magia.',
           'Se mantiene separado de Citlali, Ione y el animal de Nox. La ceguera es temporal.',False,[
        ('Ayudar aun sin ver','Un destello lo deja ciego cuando juega con la posibilidad de tocar la pared. La falta de visión lo mantiene confundido durante el inicio de la emboscada, pero logra inspirar a Tryel al estar junto a ella. Cuando vuelve a ver, se aproxima para ayudar a Naór y concede a Tesara la inspiración que ella gastará al cruzar la poza con el látigo.',[303,314,321,325]),
        ('Una búsqueda que acaba en recogida de veneno','Ayuda a Tryel a remover el tesoro y explica que no puede seguir la magia tenue con una habilidad adecuada. Antes de salir, vacía un recipiente y extrae veneno del colmillo que queda en la serpiente. Su muestra procede de la criatura y se conserva diferenciada de las recogidas directamente en las pozas.',[335,337,341,342]),
    ]),
    entity(CAVE,'lugar','Cueva con charcas de veneno, raíces, huesos y una cámara final con un gran esqueleto y tesoro.',
           'Nombre descriptivo común para la exploración del capítulo 48. Las alusiones al dragón no prueban identidad con la cueva de la emboscada de Tryel o las ruinas del lago.',True,[
        ('La sala de los huesos y el tesoro','Su cámara final conserva objetos en la oscuridad, un gran esqueleto y numerosos huesos. Tesara descubre que parte del botín está corroída. Los vapores y el veneno dificultan la exploración: la historiadora pierde temporalmente el oído y una serpiente esquelética sorprende al grupo. El despertar posterior de esqueletos menores transforma el registro en un combate prolongado.',[301,304,306,308,310,313,318,320]),
        ('Lo que queda después de la lucha','La serpiente y los esqueletos son vencidos. El examen de las paredes no revela inscripciones, pero Naór y Tesara perciben una magia antigua que se apaga por toda la cámara. El director distingue ese rastro de las pozas y lo utiliza para orientar la deducción sobre la ausencia del dragón. Eldrath y Tesara recogen veneno mientras Coyote obtiene otra muestra de la serpiente; los viajeros salen debilitados sin descontaminar el lugar o documentar una ocupación posterior.',[326,327,328,329,331,333,336,337,338,339,340,341,342]),
    ]),
    entity(SNAKE,'personaje','Enorme esqueleto de serpiente que muerde, constriñe y participa en el envenenamiento de la cámara.',
           'Etiqueta descriptiva del adversario del capítulo 48; no se identifica con Clolgedranx ni con abominaciones o serpientes anteriores. No se asigna bestiario externo.',True,[
        ('El abrazo que casi vence a Naór','La serpiente sorprende al grupo, muerde a Naór y la atrapa con la cola tras derribarla. La presión continúa dañándola mientras los compañeros intentan ayudar. Sus oleadas obligan a resistir veneno y su grito acompaña el despertar de esqueletos menores. Tryel y Tesara quedan envenenadas y Naór termina cayendo.',[308,310,313,315,318,320,322]),
        ('La caída y los restos aprovechados','Un disparo de Tesara durante su balanceo la derriba, pero el director aclara que aún resiste con un punto de vida. Naór la golpea al verla incorporarse y completa su derrota. Tesara no encuentra marcas físicas o arcanas que expliquen su animación. Naór conserva un colmillo y Coyote obtiene veneno del que queda, sin que esas extracciones revelen su origen o creador.',[325,326,327,331,332,341]),
    ]),
    entity(DEAD,'personaje','Conjunto descriptivo de los esqueletos que se incorporan a la lucha en la cueva envenenada.',
           'Colectivo del capítulo 48; mantener separado de los cadáveres de las ruinas del lago y del claro. La serpiente recibe además su propia historia por su actuación diferenciada.',True,[
        ('Los huesos se incorporan a la pelea','Los huesos esparcidos por el suelo no ofrecen huellas claras sobre la roca. Durante la pelea con la gran serpiente, su grito acompaña el despertar de esqueletos pequeños, que atacan con golpes y flechas y obligan a los viajeros a repartir su atención. Eldrath se aleja de uno para seguir disparando al enemigo mayor. Después de que caiga la serpiente, Naór encadena ataques y Eldrath destruye al que Tryel tenía enfrente. No se identifican las víctimas originales ni quién las animó.',[305,318,323,328,329]),
    ]),
    entity(POISON,'objeto','Líquidos recogidos por Eldrath, Tesara y Coyote después del combate en la cueva.',
           'Ficha conjunta de la recogida con procedencias separadas: dos cantimploras de pozas y una muestra de serpiente. No afirmar igualdad química ni identificar con muestras de otros capítulos.',True,[
        ('Una preparación todavía pendiente','Las pozas sugieren una utilidad después de la lucha. Eldrath vacía su cantimplora y recoge veneno para preparar futuras pociones contra el dragón verde; Tesara acepta la idea y hace lo mismo. Coyote utiliza un recipiente de agua para guardar veneno del colmillo restante de la serpiente. Los compañeros se llevan el material al salir, pero no se representa análisis, entrega a un alquimista, receta, fabricación o prueba que confirme una defensa eficaz.',[338,339,340,341,342]),
    ]),
    entity(FANG,'objeto','Colmillo arrancado de la serpiente derrotada por Naór como recuerdo para Leo.',
           'Nombre descriptivo. No se fusiona con el colmillo que Coyote utiliza para extraer veneno ni con trofeos anteriores.',True,[
        ('El recuerdo que debe esperar','Naór quiere llevarle algo a Leo después de la lucha y arranca un colmillo de la serpiente. Lo guarda antes de detectar la magia tenue y salir apresuradamente de la cueva. El epílogo todavía la sitúa corriendo por la jungla mientras Leo espera en el colegio, de modo que la entrega del recuerdo queda pendiente.',[332,334,341,343]),
    ]),
    entity(TREASURE,'objeto','Conjunto de objetos y riquezas de la cámara final, parte de ellos corroídos.',
           'Etiqueta colectiva descriptiva. Tesara y Eldrath lo vinculan al dragón, sin inventario completo, análisis de propiedad o valoración de poderes.',True,[
        ('Un collar entre piezas deterioradas','La oscuridad permite distinguir montones de objetos y lo que parece un escudo. Tesara intenta encontrar una pieza relacionada con el dragón, remueve el botín con su látigo y encuentra materiales corroídos junto a otros mejor conservados. Guarda un collar durante sus primeros segundos de búsqueda. Después del combate Tryel y Coyote continúan registrando: la falta de otros hallazgos de Tesara no agotaba la cámara. La investigación de inscripciones dracónicas no revela ninguna y no se establece un valor o poder de las piezas.',[301,306,311,335,336]),
    ]),
    entity('Leo','personaje','Niño harengon acogido por Naór y alumno del colegio de Iktan.',
           'La escena final no identifica por nombre a la profesora que lo acompaña.',False,[
        ('Esperar mientras su madre corre','Naór decide guardar para él un colmillo de la serpiente y deja la exploración para recogerlo. Leo permanece en la puerta del colegio junto a una mujer felina con libros y carpetas, que espera con impaciencia y anuncia otro retraso de su madre. La narración no muestra todavía el reencuentro ni la recepción del regalo.',[332,334,343]),
    ]),
    entity('Colegio de Iktan','lugar','Colegio al que acude Leo en Iktan.',
           'El epílogo mantiene a la mujer felina sin nombre; no resolver por semejanza la distinción Miaussy/Miausi.',False,[
        ('Una espera a la salida','La sesión vuelve a su puerta después de la expedición de la cueva. Una mujer felina espera con libros y carpetas junto a Leo y se impacienta por la tardanza de Naór. La madre todavía corre por la jungla. No llegan a representarse la recogida, la conversación sobre el retraso o una reunión de madres.',[334,343]),
    ]),
    entity('Clolgedranx','personaje','Dragón verde del bosque de Iktan que exige la entrega de Eldrath y Tryel.',
           'Nombre confirmado; distinto de Zarynth. En este tramo solo se lo investiga y menciona: el rastro no equivale a una aparición o ubicación actual.',False,[
        ('Preparativos entre sospechas y una huella tenue','Tesara busca en el tesoro y en el esqueleto una pista sobre el dragón, sin encontrar marcas que prueben su método de control. Naór y después Tesara detectan una magia antigua que desaparece en toda la cámara. El director orienta a la mesa relacionando el fenómeno con la magia que desprenden los dragones y la ausencia del ocupante, sin mostrar a Clolgedranx. Eldrath y Tesara deciden recoger veneno de las pozas para intentar elaborar futuras pociones contra él; no lo localizan, interrogan o derrotan, y la eficacia de esa preparación queda pendiente.',[306,331,333,337,338,339,340]),
    ]),
    entity('Iktan','lugar','Ciudad oculta protegida frente a los dragones y lugar de residencia temporal de los viajeros.',
           'Ictán en los subtítulos conserva la identidad editorial Iktan. La narración final solo representa la espera en el colegio.',False,[
        ('La ciudad espera a quienes vuelven de la cueva','Naór emprende el regreso antes que sus compañeros para recoger a Leo, mientras los otros viajeros terminan de tomar muestras y acuerdan salir de la cueva. La narración vuelve al colegio de Iktan, donde una mujer felina y el niño esperan impacientes. Naór todavía corre por la jungla al acabar la sesión; no se representa una llegada general, una nueva audiencia con Walulu o el desenlace del ultimátum.',[334,342,343]),
    ]),
]

missions = [
    'Explorar la cámara final: el grupo derrota a la serpiente esquelética y a los esqueletos que despiertan; no descubre inscripciones o marcas que expliquen su animación.',
    'Preparar un enfrentamiento con el dragón verde: Eldrath y Tesara recogen veneno de las pozas y Coyote del colmillo restante de la serpiente, con la intención de obtener futuras pociones. No se fabrica ni prueba un antídoto.',
    'Investigar el rastro mágico: Naór y Tesara detectan una magia antigua que se disipa por toda la cámara. Las pistas del director la separan de las pozas y la relacionan con la ausencia del dragón, sin verlo o localizarlo.',
    'Recoger a Leo: Naór parte antes que sus compañeros y corre hacia Iktan; el niño sigue esperando a la salida del colegio al terminar la sesión.',
    'Regresar y recuperarse: los compañeros dejan la cueva debilitados tras la lucha; el regreso completo y la recuperación del envenenamiento no se representan en este tramo.',
]

questions = [
    {'pregunta':'¿Quién animó la serpiente y los esqueletos de la cueva, y cómo se relaciona ese proceso con el dragón?', 'respuesta':'Tesara sospecha del dragón, pero su examen no revela marcas o residuos concretos. El director describe un esqueleto de serpiente y una magia antigua que desaparece en toda la sala.', 'referencias':refs(318,331,333,337,338),'pendiente':'El creador, el mecanismo de animación y el vínculo probado con el dragón y el veneno.'},
    {'pregunta':'¿Podrán las muestras recogidas proporcionar una protección eficaz contra el dragón verde?', 'respuesta':'Eldrath y Tesara guardan veneno de las pozas y Coyote obtiene otra muestra del colmillo de la serpiente. La idea es emplearlo en futuras pociones.', 'referencias':refs(338,339,340,341),'pendiente':'El análisis de las muestras, la receta, su elaboración y una prueba de eficacia; no está demostrada la igualdad entre ambas procedencias.'},
    {'pregunta':'¿Qué indica exactamente la magia que se disipa en la cámara y dónde está ahora el dragón?', 'respuesta':'Naór y Tesara perciben una magia antigua tenue extendida por toda la sala. El director orienta la deducción con la magia que desprenden los dragones y su ausencia, diferenciándola de las pozas.', 'referencias':refs(333,337,338),'pendiente':'La localización y los movimientos del dragón, la antigüedad del rastro y el alcance del fenómeno.'},
    {'pregunta':'¿Qué valor, procedencia y destino tendrán los objetos recuperados del tesoro?', 'respuesta':'Tesara guarda un collar y Tryel y Coyote continúan buscando entre piezas corroídas y otras conservadas. La búsqueda de inscripciones no aporta ninguna.', 'referencias':refs(301,306,311,335,336),'pendiente':'Un inventario claro, la valoración y el destino del botín; no se demuestra que el collar vaya a entregarse a Angelique.'},
    {'pregunta':'¿Cómo se recuperarán Tesara y Tryel del veneno y el resto de los viajeros de las heridas?', 'respuesta':'Ambas resultan envenenadas y no pueden recuperar vida mientras permanezca el efecto. El grupo sale debilitado, sin un tratamiento final representado.', 'referencias':refs(320,330,342),'pendiente':'La curación, duración del efecto y posibles consecuencias posteriores.'},
    {'pregunta':'¿Alcanzará Naór a Leo y qué ocurrirá por el retraso en el colegio?', 'respuesta':'Naór guarda un colmillo para él y corre de regreso, pero el epílogo mantiene a Leo esperando junto a una mujer felina impaciente.', 'referencias':refs(332,334,343),'pendiente':'La recogida, la reacción de la profesora y la entrega del recuerdo.'},
]

observations = {
 'P32-002':'No aparece el general aviar ni se identifica a un atacante de la Marina en la cueva.',
 'P32-003':'No se lee el pacto de Bonny con la Marina ni aparece una decisión sobre Citlali.',
 'P32-004':'La cría y Citlali no intervienen en esta exploración; no cambia la respuesta ya resuelta.',
 'P33-001':'No se representa a Axi ni se explica su amnesia o los cadáveres de aquella noche.',
 'P33-002':'No aparece la piedra rota, su donante o una noticia del acantilado.',
 'P33-003':'El lugar explorado no se identifica como el escondite que ocultaba Nox ni aporta su motivo.',
 'P33-004':'No hay noticias de Morris ni de la comunicación de la muerte de Margaret.',
 'P34-001':'El destello que ciega temporalmente a Coyote no explica las lagunas de Bling.',
 'P34-002':'Tryel y Eldrath aparecen en la cueva, pero el paradero posterior planteado ya estaba resuelto; no se documenta aquella semana de ausencia.',
 'P34-003':'No aparece el campamento del huevo ni se explica la desaparición del marine Paco.',
 'P34-004':'Leo espera en el colegio sin Eztli; la serpiente esquelética no aporta especie o residencia de la cría.',
 'P35-001':'La serpiente derrotada es un adversario de la cueva y no se identifica con las criaturas de la visión o la pirámide.',
 'P35-002':'No se consultan informes de Molly ni se representa una charla con Nox.',
 'P35-003':'No llegan reyes piratas o marines; se conserva la resolución previa de aquella ofensiva.',
 'P35-004':'No aparecen Smith, Pinky o una persecución de la Marina.',
 'P36-001':'La ceguera de Coyote no es una aparición del licántropo de ojos ámbar ni lo identifica.',
 'P36-002':'No se interroga al marine entregado a Bonny ni se da noticia de su destino.',
 'P36-003':'No intervienen Bling o Eleanor y la exploración no explica los regresos o amnesia de la hada.',
 'P36-004':'La retirada de la cueva no representa una guarnición de las ruinas de la Marina ni una nueva reparación del Zampaolas.',
 'P37-001':'La hipótesis de un ojo vigilante se descarta como solución no confirmada y no identifica o recupera el ojo-orbe de Nox.',
 'P37-002':'No se representa la llegada de Nox a Aurora ni se informa de su ojo después de la explosión.',
 'P37-003':'El tesoro de la cueva no se destina a la alianza de Eleanor ni acredita contacto con Aragón.',
 'P37-004':'El esqueleto derrotado se identifica como serpiente; no es la inspección del tiranosaurio del cañonazo.',
 'P38-001':'No se examina a Ilikar; el veneno de Tesara y Tryel no explica la mordedura de Ione.',
 'P38-002':'Ilikar no relata en este tramo su llegada herido o su pasado tribal.',
 'P38-003':'El tesoro registrado es el de esta cueva y no se identifica con el cofre repartido de Bonny.',
 'P38-004':'No aparece el Zampaolas; la recogida de muestras no cambia la navegación previamente resuelta.',
 'P39-001':'La magia antigua de la cámara no se enlaza con la piel de Citlali, sus tatuajes o el Señor de los yuan-ti.',
 'P39-002':'No se reconstruye el rescate del niño Amaru ni su crianza hasta ser Nox.',
 'P39-003':'Tryel y Eldrath actúan expresamente como hermanos, pero no se enlaza la escena anónima del 39 ni se diagnostica a aquella elfa.',
 'P39-004':'Walulu y Citlali no mantienen la conversación pendiente sobre los tatuajes.',
 'P39-005':'No se identifica la presencia del epílogo del 39 ni se revisan los yuan-ti sepultados.',
 'P40-001':'Tesara sospecha que el dragón controla esta serpiente, pero no encuentra marcas. No se analiza la muestra del claro ni se demuestra el mismo proceso en sus cadáveres.',
 'P40-002':'El grupo se marcha de otra cueva sin inspeccionar la vegetación del claro o comprobar su descontaminación.',
 'P40-003':'La cueva contiene una señal que se disipa, comparada por el director con magia del dragón. No se la identifica con la cueva de la emboscada del 40 ni se fijan coordenadas de las guaridas.',
 'P40-004':'Eldrath prepara material contra el dragón con sus compañeros, pero no revela las preguntas del pacto con Ilikar ni obtiene la aceptación de Ione o Poncelot.',
 'P40-005':'La hora que precipita la vuelta de Naór no explica la edad o los siglos de Tortas.',
 'P40-006':'Las muestras recogidas no se envían a Eromov ni se documentan expertos o recuperación completa.',
 'P40-007':'No aparecen Zippo o el fragmento de espada; no se determina su origen.',
 'P41-001':'La carrera de Naór hacia Leo no proporciona un nombre, paradero o noticia del emisario de Atlan.',
 'P41-002':'No se revela quién era «ella» ni se atribuye ese anuncio a la serpiente o al rastro mágico.',
 'P41-003':'El veneno de la cámara es otro episodio y no explica la muerte o serpientes de la infiltrada.',
 'P41-004':'No se explica el plan de retirar al Anciano ni se prueba una segunda abominación.',
 'P41-005':'Los esqueletos anónimos no se identifican con el cautivo vivo que quedó tras el festival.',
 'P41-006':'Se recogen nuevas muestras de pozas y serpiente sin analizarlas o equipararlas a los viales del norte, el veneno de Eromov o la muestra del claro.',
 'P41-007':'Los hallazgos de la cámara no identifican un taller o proveedor de las cimitarras.',
 'P41-008':'La ceguera temporal de Coyote no explica la excepción de Tentacol a la compulsión.',
 'P41-009':'La señal de la cámara sugiere presencia dracónica anterior por las pistas del director, sin localizar la guarida que desconocía Tortas ni identificar esta cueva con la emboscada antigua.',
 'P41-010':'No hay una nueva visita submarina; se conserva la resolución de la visita de Naór a Perlasal.',
 'P41-011':'La magia detectada se extiende por esta cámara y no explica el brillo observado en Tortas.',
 'P42-001':'No se representa una escena posterior de Nox, Pinky o Tórtola tras la explosión.',
 'P42-002':'No se recupera el ojo-orbe ni se atribuye al rastro de la cueva una intervención en la decisión de Nox.',
 'P42-003':'No se visita Shiaru ni se identifican sus gobernantes o responsables de exponer a Bonny.',
 'P42-004':'No se lee el pacto de los reyes o sus planes posteriores.',
 'P42-005':'No aparece Jackie ni se confirma identidad o destino de los distintos Jack.',
 'P42-006':'La recogida de veneno no pertenece a una búsqueda de Ione o uso de su moneda.',
 'P42-007':'El veneno y la furia de Naór no atribuyen a los reyes el hielo o fuego de sus monedas.',
 'P43-001':'La serpiente de la cueva recibe una identidad descriptiva separada de la entidad de Citlali; no se revela su plan.',
 'P43-002':'No se encuentra el altar de los símbolos ni se explica su activación.',
 'P43-003':'No hay recuerdos o testimonios nuevos sobre el rescate y crianza de Amaru.',
 'P43-004':'Los envenenamientos de la cueva no documentan la evolución de los drenajes o rejuvenecimiento de Citlali.',
 'P43-005':'No se vuelve al Zampaolas o a la discusión de la playa.',
 'P43-006':'No se examina a Erandy ni se explica su trance o recuperación.',
 'P43-007':'Levantar a Naór durante el combate no es la resurrección condicional de la leyenda de Eleanor ni prueba del broche.',
 'P43-008':'Los objetos del tesoro no se identifican con la caja musical de Citlali ni explican su procedencia.',
 'P44-001':'No hay seguimiento clínico o nueva dosis del tratamiento de Eromov.',
 'P44-002':'El posible escudo del tesoro no es la fabricación del exoesqueleto encargado por Ayoto.',
 'P44-003':'La serpiente y los esqueletos de esta cueva no se identifican con el moho o sus restos humanoides.',
 'P44-004':'No aparecen Leona o un recuerdo nuevo de cómo Eromov la encontró.',
 'P44-005':'El veneno de este combate no se atribuye a comer devorafango ni demuestra inocuidad de aquella carne.',
 'P44-006':'Naór y sus compañeros son otros heridos; no se documenta la recuperación de Ayoto y Guayacán.',
 'P45-001':'No aparecen los nombres del escuadrón ni se identifica a la sirena cautiva.',
 'P45-002':'La serpiente animada no se identifica como el dios de los Profundos o parte de aquel rito.',
 'P45-003':'La magia que se disipa está en otra cámara y no desactiva o explica el agua del escondite de los Profundos.',
 'P45-004':'La derrota en esta cueva no acredita el final de la red submarina o sus cautivos.',
 'P45-005':'Naór se dirige al colegio sin recibir una nueva decisión de Ivet.',
 'P45-006':'No se reconstruyen términos del pacto tribal o nuevos incumplimientos.',
 'P45-007':'El collar y los objetos encontrados no son la perla de Tentacol ni prueban su utilidad.',
 'P45-008':'No hay tratamiento o escena posterior de la cola de la sirena rescatada.',
 'P45-009':'Las horas de recogida de Leo no explican el destello de Tortas.',
 'P46-001':'No se visita la cueva de Zoltan ni se identifica a quien mató a sus ocupantes.',
 'P46-002':'No aparece el cartel recordado por Zoltan o se explica su pinchazo.',
 'P46-003':'No se relatan el encierro o las marcas de Zoltan.',
 'P46-004':'La magia que infunde el arma de Naór no explica la electricidad o control de Zoltan.',
 'P46-005':'La mención entrecortada a una copa en este tesoro no la identifica con la copa inscrita de Eleanor ni lee su escritura.',
 'P46-006':'No se localiza al novato de Ione ni se fija identidad con otros Jack.',
 'P46-007':'Los materiales recogidos se proyectan contra el dragón, sin reclutamiento de Ione o reconquista de Shiaru.',
 'P46-008':'Leo aparece esperando con una mujer felina y Naór corre a recogerlo; no se celebra la reunión de madres ni se representa a Citlali y Eztli.',
 'P47-001':'La escena vuelve a Iktan sin identificar dirigentes u ocupantes de Shiaru.',
 'P47-002':'La cámara de la cueva carece de inscripciones halladas, pero no se identifica con las ruinas del lago ni resuelve su origen.',
 'P47-003':'Tesara guarda un collar y otros siguen buscando botín; no se entrega a Angelique o se declara que cumpla la promesa de la joya.',
 'P47-004':'Mictlan y sus vigilantes no aparecen o explican sus normas.',
 'P47-005':'Esta serpiente y sus esqueletos no se identifican con los cadáveres del lago y el examen de Tesara no prueba su método de animación.',
 'P47-006':'No se adjudica una nueva orden dracónica ni se prueba el fin de la compulsión antigua; la parálisis de Eldrath la causa explícitamente Tryel.',
 'P47-007':'El tesoro no identifica al contratante que quiere a los hermanos ni los términos de su recompensa.',
 'P47-008':'El grupo obtiene muestras para intentar preparar pociones contra el dragón, mantiene juntos a los hermanos y emprende el regreso. No se entrega a los elfos o se resuelve el ultimátum.',
 'P47-009':'La idea no confirmada de ojos vigilantes no explica cómo supo Clolgedranx de Oliver ni acredita una captura.',
 'P47-010':'La detección orientada por el director y la recogida de veneno aportan pasos de exploración y preparación, sin localizar al dragón, leer resultados nuevos de Walulu o fabricar una defensa probada.',
 'P47-011':'Naór sale para recoger a Leo y la profesora espera; no se realiza la reunión pedida por Walulu ni se identifica su propósito.',
}

updates = {
    'P40-003': ('avance_parcial', refs(333,337,338), 'parcial'),
    'P40-004': ('avance_parcial', refs(339,340), 'pendiente'),
    'P41-009': ('avance_parcial', refs(333,337,338), 'parcial'),
    'P47-008': ('avance_parcial', refs(339,340,341,342), 'parcial'),
    'P47-010': ('avance_parcial', refs(333,337,338,339,340,341), 'parcial'),
}
related_refs = {
    'P40-001': refs(331,333), 'P41-006': refs(339,340,341),
    'P46-008': refs(343), 'P47-003': refs(311,335), 'P47-005': refs(331),
    'P47-006': refs(330), 'P47-009': refs(338), 'P47-011': refs(334,343),
}
crosschecks = []
for question in assigned:
    qid = question['id']
    assert qid in observations
    assert hashlib.sha256(question['pregunta'].encode('utf-8')).hexdigest() == question['sha256_pregunta']
    outcome, references, state = updates.get(qid, ('sin_avance_en_tramo', related_refs.get(qid, []), question['estado']))
    crosschecks.append({
        'id': qid, 'sha256_pregunta': question['sha256_pregunta'],
        'pregunta': question['pregunta'], 'estado_previo': question['estado'],
        'resultado': outcome, 'observacion': observations[qid], 'referencias': references,
        'estado_propuesto': state, 'pendiente': question.get('pendiente', ''),
    })

delivery = {
    'bloque':3, 'capitulo':48, 'lectura_completa':True, 'segmentos_leidos':1566,
    'primer_segmento':'c006265', 'ultimo_segmento':'c009395', 'fuente_sha256':EXPECTED,
    'cobertura_lectura':list(range(1,1567)), 'ids_segmentos_leidos':[s['id'] for s in segments],
    'tandas_lectura':[{'primero':a,'ultimo':b,'primer_segmento':segments[a-1]['id'],'ultimo_segmento':segments[b-1]['id'],'completa':True} for a,b in [(1,200),(201,400),(401,600),(601,800),(801,1000),(1001,1200),(1201,1400),(1401,1566)]],
    'identidades_contexto_leidas_completas':209, 'preguntas_asignadas_leidas_completas':99,
    'historias_consultadas':['config/historias_personajes_complementarias.json: Tesara Queen, Naór, Eldrath, Tryel, Coyote, Clolgedranx, Leo, Miaussy','config/historias_lugares.json: Colegio de Iktan, Iktan','config/historias_objetos.json: Escupefuego'],
    'etapas':stages, 'afirmaciones':facts, 'historias_entidades':histories,
    'misiones':missions, 'preguntas':questions,
    'contradicciones':[
        'El director anuncia la caída de la serpiente tras el disparo de Tesara y después precisa que todavía resiste con un punto de vida; Naór completa el remate (48-326–48-327).',
        'La retirada del icono de restricción a Naór es corregida como error de interfaz: la serpiente seguía reteniéndola (48-315).',
        'Se corrige el intento de Eldrath de hablar mentalmente con Naór: no existía esa conexión y los interlocutores declarados eran Tesara y Coyote (48-330).',
        'Las cartas del chat, las tiradas extra y la curación externa permanecen como mecánicas de mesa, sin crear objetos o causantes diegéticos.',
        'El rastro mágico antiguo y las pozas de veneno se distinguen expresamente. Las teorías de runas, ojos vigilantes y plantas protectoras no reciben confirmación (48-336–48-338).',
        'La cueva y sus no muertos se mantienen separados de los cadáveres y lugares de capítulos anteriores; no hay coordenadas o enlace verbal con la cueva de la emboscada de Tryel.',
        'La mujer felina del epílogo no se nombra: la semejanza profesional no resuelve la separación vigente entre Miaussy y Miausi.',
    ],
    'nombres_dudosos':[
        'Mirien/Miriam: menciones en consultas de Tesara sin identificación suficiente dentro de este tramo; conservar grafía de la cita y coordinar con la lectura anterior antes de abrir entidad.',
        'Triel, triels, Tri: variantes originales del nombre confirmado Tryel; Eldra, Eldrat, Edrat y drat corresponden al Eldrath confirmado por continuidad.',
        'La mujer gato del epílogo permanece sin nombre: no convertirla automáticamente en Miaussy o Miausi.',
        'La respuesta a la habilidad del dragón verde en c009129 («La bicad.») es ilegible para una identificación inequívoca; no completar su sentido con reglas externas.',
    ],
    'cotejo_preguntas_asignadas':crosschecks,
    'nota_integracion':'Los resultados sin avance se limitan al intervalo 02:16:46.000–03:23:45.160. El coordinador debe integrar la lectura anterior antes de decidir estados globales. Los nombres comunes de cueva y no muertos se coordinan con los otros lectores.',
}

assert facts[0]['id'] == '48-301' and facts[-1]['id'] == '48-343'
assert len(crosschecks) == 99
assert {x['id'] for x in crosschecks} == {x['id'] for x in assigned}
valid_ids = {f['id'] for f in facts}
for entry in stages + questions:
    assert set(entry['referencias']) <= valid_ids
for ent in histories:
    assert any(ent['nombre'] in f['entidades'] for f in facts), ent['nombre']
    for stage in ent['etapas']:
        assert set(stage['referencias']) <= valid_ids
original = {s['id']:s for s in parse_vtt(SOURCE)}
for s in segments:
    assert s['id'] in original
    assert s['texto_original'] == original[s['id']]['texto_original']
for f in facts:
    validate_fact(f, SOURCE)
    ev = f['evidencia_cue']
    assert any(s['inicio'] == ev['inicio'] and s['fin'] == ev['fin'] and s['texto_original'] == ev['texto'] for s in segments)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
(BASE / 'entrega_3.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines = [
    '# Lectura completa del tercer tramo del capítulo 48', '',
    'Fuente original: `48 - FYarBX28XfI.es-orig.vtt`.',
    f'SHA-256 verificado antes y después: `{EXPECTED}`.',
    'Intervalo leído: **02:16:46.000–03:23:45.160**; **1566 segmentos**, de `c006265` a `c009395`.',
    'Lectura realizada sin omisiones en ocho tandas de 200, 200, 200, 200, 200, 200, 200 y 166 segmentos. La primera salida conjunta de contexto fue truncada; se volvieron a leer completas las 209 identidades y las 99 preguntas asignadas mediante tandas independientes sin truncar.',
    '', 'Tandas de fuente leídas:', '',
]
for batch in delivery['tandas_lectura']:
    lines.append(f"- {batch['primero']}–{batch['ultimo']}: {batch['primer_segmento']}–{batch['ultimo_segmento']}.")
lines += ['', 'Resultado editorial: **43 afirmaciones** (`48-301`–`48-343`), ocho etapas narrativas, quince historias de entidades, cinco misiones, seis preguntas y 99 cotejos individuales.',
          '', 'Todas las afirmaciones pasan `construir.validate_fact`; cada `evidencia_cue` coincide literalmente con un segmento original. La cobertura incluye los 1566 índices y sus identificadores. Se ha cotejado la fuente mediante `parse_vtt` y se conserva el SHA-256 original.',
          '', 'Límites que debe conservar la integración:', '',
          '- La serpiente sobrevive inicialmente al disparo de Tesara; Naór remata y disimula el golpe.',
          '- Tryel paraliza y golpea a Eldrath sin matarlo; no se convierte la amenaza jocosa en muerte.',
          '- El control por Clolgedranx es una sospecha de Tesara. Las pistas sobre magia que se disipa no muestran al dragón o localizan su guarida.',
          '- Las muestras de pozas y serpiente tienen procedencias separadas; recogida no equivale a antídoto elaborado o eficaz.',
          '- La mujer felina del epílogo no se nombra. Naór todavía corre hacia el colegio; no se representa recogida, reunión de madres o entrega del colmillo.',
          '- Los resultados de preguntas sin avance se refieren solo a este tramo. Los parciales deben integrarse con las fuentes anteriores.',
          '', 'Historias vigentes consultadas: Tesara Queen, Naór, Eldrath, Tryel, Coyote, Clolgedranx, Leo, Miaussy, Colegio de Iktan, Iktan y Escupefuego.',
          '', 'No se ha editado la fuente, ninguna configuración o borrador ajeno, ni se ha realizado commit, publicación o push.', '']
(BASE / 'lectura_bloque_3.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'afirmaciones':len(facts),'etapas':len(stages),'historias':len(histories),'cotejos':len(crosschecks),'sha256':EXPECTED},ensure_ascii=False))
