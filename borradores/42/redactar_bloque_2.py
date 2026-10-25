"""Entrega editorial del segundo bloque, leída íntegramente antes de redactar."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import validate_fact, write_json, seconds

rows = json.loads((ROOT / 'borradores/42/bloque_2_segmentos.json').read_text(encoding='utf-8'))
source = ROOT / 'xoltacan_subtitulos/subtitulos/42 - 3IUV_YN_zxM.es-orig.vtt'
facts = []


def fact(number, title, start, end, quote_time, text, entities, limitation='', kind='hecho_confirmado'):
    cue = next(s for s in rows if s['inicio'].startswith(quote_time))
    item = {'id':f'42-{number:03d}', 'titulo':title, 'tipo':kind, 'afirmacion':text,
            'inicio':start, 'fin':end, 'cita':cue['texto_original'],
            'evidencia_cue':{'inicio':cue['inicio'],'fin':cue['fin'],'texto':cue['texto_original']},
            'entidades':entities, 'ambito':'batalla naval del Arrecife del Garfio', 'conocedores':[],
            'conocimiento_personaje':'desconocido',
            'nota_conocimiento':'Acceso de Madame Oghma sin establecer en este pasaje.',
            'confianza':'lectura de subtítulos; audio no cotejado', 'limitacion':limitation}
    validate_fact(item, source)
    facts.append(item)


fact(101, 'La salva coordinada de la Marina alcanza al Zampaolas', '00:47:03.319','00:49:20.239','00:48:39.440',
     'La Marina responde a los disparos piratas con una salva sincronizada que rompe mástiles de varias naves. Un cañonazo alcanza el Zampaolas y hace saltar parte del casco. Merlucilla se refugia en los brazos de Sir Poncelot; se ordena reparar la abertura para impedir que entre más agua y los tripulantes corren con tablones.',
     ['Marina','Zampaolas','Tripulación del Zampaolas','Sir Poncelot','Merlucilla IV'],
     'El pasaje no identifica inequívocamente a quien da la orden inicial de reparación ni confirma que esta termine antes del siguiente ataque.')
fact(102, 'Sir Poncelot tranquiliza al tigre', '00:49:23.400','00:50:20.239','00:50:12.440',
     'Sir Poncelot baja de sus brazos al pesado Merlucilla e intenta tranquilizarlo. Declara que no sabe de barcos y se mantiene disponible para combatir o ayudar cuando se lo pidan. La tirada permite ir calmando al tigre, que todavía conserva algo de nerviosismo.',
     ['Sir Poncelot','Merlucilla IV','Zampaolas'],
     'La montura de esta escena es el tigre Merlucilla IV; no se convierte por el nombre compartido en el tiburón Merlucilla V.')
fact(103, 'Ilikar prepara sus pociones y el ancla', '00:50:20.240','00:51:44.734','00:51:25.640',
     'Ilikar pregunta por la distancia a los enemigos y por la posibilidad de saltar desde el barco al espigón y recorrerlo a pie. Guarda cuatro pociones de efectos todavía inciertos y sube a popa junto a la capitana con el ancla en la mano. Le ofrece utilizarla para corregir la maniobra si cruzan las piedras.',
     ['Ilikar','Ione','Zampaolas','El Garfio'],
     'La posibilidad de desembarcar en el espigón se acepta, pero Ilikar no desembarca aquí. No se identifica la procedencia de las pociones.')
fact(104, 'Ione ordena liberar la carga para aprovechar su peso', '00:51:44.735','00:53:18.598','00:52:27.280',
     'Ione ordena a Baps y Mugroso soltar la carga salvo los barriles y las municiones, dejando que su peso se distribuya al girar el barco, y manda preparar los cañones. Baps interpreta por un momento que debe arrojar carga y se acerca al gato; la capitana aclara que quiere aflojar la carga, no tirarla por la borda. Poncelot protege a su montura.',
     ['Ione','Baps','Tripulación del Zampaolas','Zampaolas','Sir Poncelot','Merlucilla IV'],
     'Mugroso aparece como destinatario de la orden, sin que este fragmento establezca una identidad personal adicional. No se arrojan aquí los barriles, la munición ni Merlucilla.')
fact(105, 'Ilikar inutiliza el mástil de un barco enemigo', '00:53:35.200','00:55:11.719','00:54:59.960',
     'Ilikar toma una bala unida a una cadena, aumenta de tamaño en popa y la hace girar para lanzarla con la mano en lugar de utilizar el cañón. El impacto rompe el mástil de una nave enemiga, que se balancea y queda sin poder moverse. Ilikar celebra el golpe aullando.',
     ['Ilikar','Zampaolas','Marina'],
     'Se confirma la inutilización del mástil y del movimiento, no un hundimiento inmediato.')
fact(106, 'Jack dispara a la orden de Poncelot', '00:55:11.720','00:56:31.239','00:56:21.760',
     'Sir Poncelot pasa junto a Jack, situado en un cañón, y le transmite la orden de disparar de la capitana. El gnomo se encarama al mascarón, se sujeta con una cuerda y anima a atacar con la lanza alzada. El disparo de Jack alcanza una nave enemiga y la deja muy dañada.',
     ['Sir Poncelot','Jack','Ione','Zampaolas','Marina'],
     'La idea de lanzar al propio Poncelot se plantea como comentario, pero él aclara que por ahora permanece agarrado al mascarón.')
fact(107, 'Bonnie descarga rayos sobre la flota', '00:56:31.240','00:57:21.919','00:56:56.599',
     'Bonnie avanza con su barco, alza la mano y cierra el puño. Empiezan a caer rayos que golpean los barcos de la Marina: uno rompe un mástil y prende la nave. Otros impactos destrozan barcos, mientras los marines saltan al agua aterrorizados.',
     ['Bonnie','Relámpago del Mar','Marina'],
     'La escena muestra varios impactos, pero no fija un recuento exhaustivo de naves hundidas o marines muertos.')
fact(108, 'Nox libera a Pinky de la celda del Invictus', '00:57:29.760','01:00:27.719','01:00:04.400',
     'Nox arroja un pedernal a la celda del Invictus. La cautiva resulta ser Pinky, que lo utiliza para volver a fumar y se queja de sus captores. Nox presenta su presencia como un cambio de bando por sus intereses. Pinky pide que le quite las ataduras para golpear a la paloma; Nox saca herramientas de sus trenzas y logra abrir las cadenas.',
     ['Nox','Pinky','Invictus','Marina','Tórtola'],
     'La explicación del cambio de bando pertenece a Nox. La liberación no identifica retrospectivamente el motivo ni la fecha de captura de Pinky.')
fact(109, 'Una fruta da a Pinky apariencia masculina', '01:00:27.720','01:01:35.679','01:00:39.960',
     'Pinky come un trozo de alimento que el director llama fruta. Le crece barba, le cambia la voz y pasa a presentar aspecto de hombre. Nox le pide discreción entre los chaquetas azules hasta que le dé la señal. Pinky busca el arma que, según dice, le dio una niña pequeña y que los marines le quitaron.',
     ['Pinky','Nox','Invictus','Marina'],
     'El diálogo menciona primero chocolate y después fruta; no se fija composición o nombre del alimento. Su apariencia masculina se conserva como transformación de Pinky, no como persona distinta.',
     'explicacion_director')
fact(110, 'Una ilusión de Nox hace encallar al primer escolta', '01:01:35.680','01:04:21.558','01:03:23.400',
     'Nox sale hacia proa y comprueba la ruta que había marcado entre los arrecifes: solo una grieta profunda permite circular. Con ilusión mayor hace parecer profundas unas aguas peligrosas y guía hacia ellas a un escolta pequeño. La nave sigue sus indicaciones y comienza a inclinarse al encallar. El mando, que había ordenado obedecerlo, culpa a sus hombres y manda subir al señor Hawkins como vigía.',
     ['Nox','Invictus','El Garfio','Marina','Tórtola'],
     'El engaño altera la apariencia del agua, no la profundidad real del arrecife. La continuidad de Hawkins con Nox se mantiene; no se crea otro piloto.')
fact(111, 'El segundo escolta queda atrapado y ordenan recuperar su munición', '01:04:21.559','01:06:15.719','01:05:13.119',
     'Desde su puesto elevado Nox repite ilusión mayor para dirigir el segundo barco pequeño contra las rocas. El casco choca, se rompe y queda inmovilizado. El almirante amenaza a Hawkins si se trata de una trampa. Nox acusa de incompetencia a los marines y propone trasladar hombres y munición al Invictus; el mando ordena recoger la carga y dejar a los hombres para no sobrecargar el buque.',
     ['Nox','Tórtola','Invictus','Marina','El Garfio'],
     'La orden final distingue carga y hombres: no se trasladan todos los marines al Invictus como proponía Nox. El pasaje alterna capitán y almirante para el mismo interlocutor.')
fact(112, 'Los refuerzos de Marina prolongan el fuego sobre los piratas', '01:06:18.720','01:08:34.879','01:08:15.480',
     'Ambas flotas siguen intercambiando cañonazos. Hay barcos destruidos, dañados y piratas que saltan al agua, mientras por el horizonte llegan nuevos buques de la Marina. Otro cañonazo revienta una pieza añadida al Zampaolas, descrita como un pegote que no pertenecía al casco original.',
     ['Marina','Zampaolas','Tripulación del Zampaolas'],
     'No se identifica qué reparación histórica corresponde a esa pieza ni se cuantifica toda la fuerza de refuerzo.')
fact(113, 'Poncelot dispara a Cipo y prende una nave enemiga', '01:08:34.880','01:11:57.919','01:11:43.400',
     'Ione ordena atarse con cuerdas, preparar el ancla y acudir a la ballesta. Sir Poncelot coloca a Cipo sobre un virote y lo dispara contra un barco enemigo. El elemental cae sobre la cubierta, saluda y hace arder la madera a su alrededor; los marines intentan buscar agua. La acción no dirige a Cipo al Invictus.',
     ['Ione','Sir Poncelot','Cipo','Zampaolas','Marina'],
     'Las bromas sobre fabricar más Cipos no acreditan que puedan duplicarlo. Se muestra el incendio del barco, sin seguimiento individual de todos sus ocupantes.')
fact(114, 'El ancla permite al Zampaolas cerrar el giro', '01:12:00.159','01:13:21.079','01:12:29.880',
     'Siguiendo el plan de Ione, Ilikar lanza el ancla contra las piedras del espigón, la engancha y se afirma con los pies sobre el barco. La distribución del peso y el tirón ayudan al Zampaolas a girar de forma cerrada. Ilikar señala el hueco abierto en la formación enemiga y propone aprovecharlo; la capitana responde que la romperán por detrás.',
     ['Ione','Ilikar','Zampaolas','El Garfio','Merlucilla IV'],
     'La maniobra es la resolución aceptada en mesa; no proporciona distancias o propiedades físicas verificadas fuera de la escena.')
fact(115, 'Ilikar bebe una poción para hablar con animales', '01:13:11.639','01:13:56.559','01:13:37.000',
     'Ilikar empieza a beber una de las pociones que había preparado y se concreta que es la de hablar con animales. También recuerda un producto llamado merluza recibido de Ione, al que en mesa atribuyen una ventaja relacionada con el encanto. No se muestra todavía una conversación entre Ilikar y Merlucilla.',
     ['Ilikar','Ione','Merlucilla IV'],
     'La transcripción dice «charro» en la explicación de la merluza; se conserva la lectura mecánica como incierta y no se convierte en un objeto o efecto plenamente identificado.')
fact(116, 'Los rayos alimentan el barco de Bonnie', '01:13:56.560','01:15:15.719','01:14:57.040',
     'El barco de Bonnie avanza sin retroceder y dispara una batería de cinco o seis cañones, destrozando o dañando varios buques enemigos. Los rayos de la tormenta empiezan entonces a caer sobre su propia nave: las velas se iluminan y la energía parece recorrer el barco hacia el timón donde está Bonnie, sin incendiarlo como a los barcos de la Marina.',
     ['Bonnie','Relámpago del Mar','Marina'],
     'La escena describe el recorrido visible de los rayos, sin explicar por completo el mecanismo del buque.')
fact(117, 'Nox contempla a Ione y decide iniciar la revuelta', '01:15:18.000','01:17:28.119','01:16:01.239',
     'Desde el puesto de vigía Nox observa el Zampaolas con su catalejo: ve a Ione coordinando a su gente, a Poncelot y al nuevo integrante que utiliza el ancla. Sonríe y dice «Esa es mi chica». Baja aprovechando que parte de los hombres transporta municiones y da la señal a Pinky para que salga y ataque. Con barba y chaqueta azul, Pinky pasa inicialmente por un miembro de la tripulación.',
     ['Nox','Ione','Sir Poncelot','Ilikar','Pinky','Zampaolas','Invictus','Marina'],
     'La mirada y la frase documentan el vínculo expresado por Nox; no acreditan que Ione pueda verlo ni que los marines conozcan la transformación de Pinky.')
fact(118, 'La carta de sueño permite capturar al almirante', '01:17:29.040','01:19:54.519','01:19:20.040',
     'Nox se acerca sonriente al almirante, que le exige trabajar y quitarse el sombrero. Le replica que debería aprender a no confiar en un pirata y le sopla polvo a la cara utilizando una carta que llevaba guardada. El mando cae dormido. Nox lo arrastra y lo ata con las cadenas de las balas de cañón.',
     ['Nox','Tórtola','Invictus'],
     'Se duerme y encadena al mismo palomo que da órdenes en el Invictus. El pasaje no establece que la captura sea definitiva ni explica origen o reutilización de la carta.')
fact(119, 'Pinky incendia la pólvora de los escoltas', '01:19:54.520','01:21:26.599','01:20:31.080',
     'Pinky observa a los hombres que suben pólvora desde las naves encalladas. Se acerca a uno, lo tira abajo de una patada y lanza manos ardientes sobre la pólvora. Las llamas provocan una explosión. Mientras Nox ajusta rumbo y velas para atravesar el arrecife, la pólvora sigue prendiendo y estallan las naves detenidas.',
     ['Pinky','Nox','Invictus','Marina','El Garfio'],
     'El pasaje enlaza el fuego de Pinky con las explosiones; no ofrece un recuento de víctimas ni muestra que toda la pólvora del Invictus haya detonado.')
fact(120, 'La presión de Marina obliga a varios piratas a virar', '01:21:29.120','01:22:46.000','01:22:34.040',
     'Los piratas siguen disparando y dañan cañones enemigos, pero varios barcos están muy deteriorados y algunos buscan otra dirección. La Marina hunde una nave pirata y sus hombres saltan al agua para salvarse. A pesar de las pérdidas infligidas por los piratas y Bonnie, siguen llegando refuerzos de la Marina.',
     ['Marina','Bonnie'],
     'Virar y buscar otra salida no equivale a una retirada completa de todos los piratas; el combate continúa.')
fact(121, 'Ione y Poncelot enlazan barcos enemigos con una cadena', '01:22:46.000','01:24:34.959','01:24:27.800',
     'Ione propone repetir una maniobra de giro para hacer chocar dos cascos enemigos entre sí. Ordena emplear un virote con cadena contra el barco de atrás y deja a sus compañeros margen para actuar de otra manera. Sir Poncelot dispara y confirma que uno de los barcos queda encadenado, pendiente del movimiento posterior.',
     ['Ione','Sir Poncelot','Zampaolas','Marina'],
     'El plan busca una colisión, pero este primer disparo solo confirma el enlace: el desenlace de la colisión no se adelanta.')
fact(122, 'Ilikar se impulsa hacia el barco en llamas y llama a Cipo', '01:24:34.960','01:27:39.000','01:26:56.800',
     'Ilikar prepara su ancla con un barril de aceite y la lanza contra el barco que Cipo ha incendiado. La clava, tira de la nave para acercarla y utiliza la tensión para impulsarse hacia ella. Los tirones del ancla y de la cadena de Poncelot desplazan los barcos. Cipo había comenzado a regresar al Zampaolas por la cadena, pero Ilikar lo llama y el elemental da la vuelta para saltar sobre él. Antes de lanzarse, Ilikar reta a Poncelot a no ser el último.',
     ['Ilikar','Cipo','Sir Poncelot','Ione','Zampaolas','Marina'],
     'El bloque termina esta acción con Ilikar desplazándose hacia los barcos; no se anticipa aquí el resultado del abordaje o del choque.')
fact(123, 'El Relámpago del Mar atraviesa y parte barcos de la Marina', '01:27:39.000','01:28:43.759','01:28:23.520',
     'El barco de Bonnie queda de un azul brillante, rodeado por una estela eléctrica. Sale disparado como un rayo, pasa delante de varios enemigos y aparece al otro lado. Los barcos atravesados por el Relámpago del Mar se parten por la mitad y quedan destrozados.',
     ['Bonnie','Relámpago del Mar','Marina'],
     'La comparación con la velocidad de Fly es una referencia descriptiva de mesa; no establece que Fly intervenga en la batalla.')
fact(124, 'Nox dirige el Invictus hacia la flota y prepara la pólvora', '01:28:43.760','01:32:26.999','01:31:18.960',
     'El Invictus atraviesa el arrecife y asoma a la batalla, descrito como un enorme buque blanco impecable, algo mayor e imponente que el de Bonnie. Nox fija rumbo hacia la flota, se lanza invisibilidad mayor y ayuda a Pinky a atacar marines, arrojando algunos por la borda y usando el estoque por detrás. Después toma un barril de pólvora y traza un reguero desde la zona de carga hasta la base del mástil mayor. Corta un cabo y sube a una red lateral del mástil, mirando al Zampaolas.',
     ['Nox','Pinky','Invictus','Zampaolas','Relámpago del Mar','Marina','El Garfio'],
     'Se prepara un reguero de pólvora, pero no se enciende en este intervalo. El rumbo hacia la flota no equivale todavía a una colisión.')
fact(125, 'El ataque de Bonnie anima a unos piratas mientras otros se marchan', '01:32:27.000','01:33:30.390','01:32:54.000',
     'Algunos barcos piratas desisten o se alejan, otros ya están destrozados y varios continúan combatiendo. La pasada de Bonnie anima a quienes siguen disparando, pero la Marina aumenta sus fuerzas: el director compara tres barcos destruidos por Bonnie con cinco nuevos que aparecen. El Zampaolas mantiene ante sí dos naves medio chamuscadas.',
     ['Bonnie','Marina','Zampaolas'],
     'La comparación de tres por cinco expresa el crecimiento de los refuerzos; no constituye un inventario definitivo de ambas flotas.')


def stage(title, text, *refs):
    return {'titulo':title,'texto':text,'referencias':list(refs)}


stages = [
    stage('Una capitana bajo los cañones',
          'La respuesta de la Marina llega en una salva sincronizada que rompe mástiles y alcanza el Zampaolas. Mientras los tripulantes corren con tablones para contener el agua, Poncelot baja de sus brazos al tigre Merlucilla y consigue calmarlo parcialmente. Ilikar prepara cuatro pociones y ofrece su ancla a Ione. La capitana manda aflojar la carga, conservando barriles y municiones, para aprovechar su desplazamiento al girar. Corrige la interpretación de Baps: no quiere arrojarla al mar. Ilikar crece en popa y lanza con la mano una bala encadenada que rompe un mástil enemigo. Poncelot transmite a Jack la orden de disparar; su cañonazo deja otra nave muy dañada. Bonnie, por su parte, hace caer rayos que prenden barcos y obligan a sus marines a saltar al agua.',
          '42-101','42-102','42-103','42-104','42-105','42-106','42-107'),
    stage('La prisionera y las aguas falsas',
          'Bajo la cubierta del Invictus, Nox arroja un pedernal a la cautiva y descubre a Pinky, deseosa de fumar y de vengarse de la paloma que la retiene. La libera con sus herramientas. Al comer un trozo de fruta, Pinky adquiere barba y apariencia masculina; Nox le pide discreción mientras busca su arma. De vuelta a la ruta del arrecife, el pirata aprovecha las instrucciones que había dado sobre el color de las aguas. Dos ilusiones mayores hacen parecer profundos pasos que esconden rocas. Los dos escoltas pequeños siguen la ruta y encallan. El mando amenaza a Hawkins, que culpa a los marines y propone recuperar sus hombres y munición. El almirante acepta trasladar la carga, pero ordena dejar a los hombres para no sobrecargar el Invictus.',
          '42-108','42-109','42-110','42-111'),
    stage('Cipo abre un hueco entre las naves',
          'El combate sigue dañando ambos bandos y llegan refuerzos de la Marina. Un segundo cañonazo arranca del Zampaolas una pieza añadida al casco. Ione ordena atarse y preparar una maniobra cerrada. Poncelot monta a Cipo sobre un virote y lo dispara contra una nave: el elemental prende la cubierta y fuerza a los marines a buscar agua. Ilikar engancha su ancla en las piedras y se afirma para ayudar al giro del Zampaolas. Propone aprovechar el hueco abierto en la formación, pero Ione quiere rodearla por detrás. El goliat bebe una poción para hablar con animales. A cierta distancia, el barco de Bonnie descarga sus cañones; después recibe los rayos de la tormenta sin arder y la luz recorre sus velas hasta el timón.',
          '42-112','42-113','42-114','42-115','42-116'),
    stage('El mando del Invictus cambia de manos',
          'Desde lo alto, Nox contempla con orgullo a Ione coordinando el Zampaolas y reconoce la actividad de sus compañeros. Aprovecha el traslado de munición para dar a Pinky la señal de atacar: con barba y chaqueta azul pasa inicialmente por otro marinero. Nox se acerca al almirante y, tras advertirle contra confiar en un pirata, utiliza una carta de sueño y le sopla polvo a la cara. El palomo cae dormido y termina atado con cadenas de balas de cañón. Pinky derriba a un hombre y lanza manos ardientes contra la pólvora que transportan desde los escoltas. Las explosiones destruyen las naves detenidas mientras Nox toma el timón, ajusta las velas y se dispone a cruzar el arrecife.',
          '42-117','42-118','42-119'),
    stage('Cadenas, rayos y una mecha preparada',
          'La Marina sigue llegando y varios piratas viran o abandonan, aunque otros continúan luchando. Ione propone hacer chocar dos barcos enemigos; Poncelot enlaza uno con un virote encadenado. Ilikar unta el ancla con aceite, la clava en el barco incendiado y se impulsa hacia él, retando al gnomo a seguirlo. Cipo, que regresaba por la cadena, cambia de dirección para subirse al goliat. El Relámpago del Mar, convertido en una estela azul eléctrica, atraviesa y parte varios barcos. El enorme Invictus blanco asoma a la batalla bajo el rumbo fijado por Nox. Invisible, el pirata apoya a Pinky contra los marines y prepara un reguero de pólvora hasta la base del mástil; después sube a una red lateral mirando al Zampaolas. La ofensiva de Bonnie anima a algunos aliados, pero siguen apareciendo más enemigos.',
          '42-120','42-121','42-122','42-123','42-124','42-125')
]

histories = []


def history(name, kind, title, text, refs, new=False, description='', note=''):
    histories.append({'nombre':name,'tipo':kind,'nueva':new,'descripcion':description,'nota':note,
                      'etapas':[stage(title,text,*refs)]})


history('Nox','personaje','El sabotaje del Invictus',
        'Con el nombre de Hawkins, Nox aprovecha la confianza del mando del Invictus para encallar sus dos escoltas mediante ilusiones. Libera a Pinky y coordina su ataque contra la pólvora, duerme al almirante con una carta y lo encadena. Desde el vigía contempla a Ione al frente del Zampaolas y expresa orgullo por ella. Toma el timón del buque enemigo, atraviesa el arrecife y prepara un reguero de pólvora antes de subir al mástil bajo invisibilidad mayor.',
        ['42-108','42-110','42-111','42-117','42-118','42-119','42-124'])
history('Ione','personaje','El Zampaolas atraviesa el fuego',
        'Ione coordina al Zampaolas bajo los cañones de Marina. Ordena aflojar la carga para aprovechar su peso al girar, conserva municiones y barriles y combina el ancla de Ilikar con el movimiento del casco. Prepara a Poncelot en la ballesta y después propone enlazar barcos enemigos para hacerlos chocar. Da instrucciones concretas y permite a sus compañeros resolver por su cuenta si encuentran otra oportunidad.',
        ['42-104','42-113','42-114','42-121'])
history('Sir Poncelot','personaje','La ballesta y el elemental',
        'Poncelot calma al tigre Merlucilla tras el primer impacto y anima a Jack a obedecer el fuego ordenado por Ione. Utiliza la ballesta del Zampaolas para lanzar a Cipo a una nave enemiga, donde el elemental incendia la cubierta. Más tarde dispara un virote con cadena para ejecutar el plan de colisión de la capitana, mientras Ilikar lo reta a seguirlo al abordaje.',
        ['42-102','42-106','42-113','42-121','42-122'])
history('Ilikar','personaje','El ancla como arma y como impulso',
        'Ilikar agranda su cuerpo para arrojar una bala encadenada y romper un mástil enemigo. Se ofrece a Ione para maniobrar con el ancla y la engancha al espigón durante el giro cerrado del Zampaolas. Después bebe una poción de hablar con animales, prepara el ancla con aceite y la clava en el barco incendiado por Cipo. Tira de ella y utiliza el impulso para lanzarse hacia la cubierta; llama al elemental que regresaba por la cadena para que se una a él.',
        ['42-103','42-105','42-114','42-115','42-122'])
history('Pinky','personaje','Liberada entre los marines',
        'Nox encuentra a Pinky encerrada en el Invictus, le permite volver a fumar y abre sus cadenas. Una fruta le da barba y apariencia de hombre. Disfrazada con chaqueta azul, aprovecha que los marines la toman por un compañero para moverse por cubierta. A la señal de Nox derriba a un hombre y prende con manos ardientes la pólvora que transportan desde los escoltas encallados. Continúa atacando marines mientras Nox conduce el buque.',
        ['42-108','42-109','42-117','42-119','42-124'])
history('Bonnie','personaje','La tormenta del Relámpago del Mar',
        'Bonnie combina las baterías de su barco con rayos que incendian los buques enemigos. Después atrae la tormenta sobre su propia nave: las velas se iluminan y la energía parece recorrerla hasta el timón. El Relámpago del Mar se vuelve azul brillante, deja una estela eléctrica y atraviesa varias naves, partiéndolas por la mitad. Su ataque anima a parte de los piratas, aunque la Marina sigue recibiendo refuerzos.',
        ['42-107','42-116','42-123','42-125'])
history('Cipo','personaje','Un incendio y una cadena de regreso',
        'Poncelot utiliza un virote para enviar a Cipo a un barco de la Marina. El elemental cae sobre la cubierta y hace arder la madera mientras los ocupantes buscan agua. Más tarde intenta regresar al Zampaolas por la cadena del ancla; al cruzarse con Ilikar, que vuela hacia el barco incendiado, escucha su llamada y da la vuelta para subirse al goliat.',
        ['42-113','42-122'])
history('Jack','personaje','Artillero del Zampaolas',
        'Apostado junto a un cañón del Zampaolas, Jack recibe de Poncelot la orden de abrir fuego de la capitana. Su disparo alcanza una nave de la Marina y la deja muy dañada, mientras el gnomo anima al ataque desde el mascarón.',
        ['42-106'])
history('Merlucilla IV','personaje','El tigre bajo los cañones',
        'Un cañonazo sobre el Zampaolas asusta al tigre Merlucilla, que se refugia en brazos de Poncelot. El gnomo lo baja y consigue tranquilizarlo parcialmente; después lo protege cuando Baps confunde la orden de aflojar la carga con arrojarla al mar. Durante el giro con el ancla el animal permanece agarrado al barco.',
        ['42-101','42-102','42-104','42-114'])
history('Tórtola','personaje','Un mando engañado por Hawkins',
        'El mando aviar del Invictus confía inicialmente en las indicaciones de Hawkins, que utiliza ilusiones para encallar sus dos escoltas. Lo amenaza al sospechar una trampa, pero acepta recuperar la carga y dejar a los hombres para no sobrecargar el buque. Nox se aproxima después, lo duerme con una carta y lo deja encadenado. El bloque alterna capitán, almirante y palomo sin introducir otro interlocutor.',
        ['42-110','42-111','42-118'],False,
        'Mando aviar del Invictus, engañado y capturado temporalmente por Nox durante la batalla.',
        'El nombre Tórtola requiere integración con los otros bloques; este tramo lo designa por almirante y palomo. La variación de rango no crea dos identidades.')
history('Invictus','objeto','De prisión a nave saboteada',
        'El Invictus contiene la celda donde Nox libera a Pinky y recibe la munición recuperada de sus escoltas encallados. El pirata duerme a su mando, toma el timón y cruza el arrecife hacia la batalla. El buque aparece como una nave blanca enorme e impecable, algo mayor e imponente que la de Bonnie. En su interior Nox prepara una línea de pólvora entre la zona de carga y el mástil, mientras Pinky combate a los marines.',
        ['42-108','42-111','42-118','42-119','42-124'],True,
        'Gran buque blanco de la Marina que Nox sabotea desde dentro durante la batalla del Garfio.',
        'Nave distinta del Zampaolas y del Relámpago del Mar; no se anticipa su destino al final de la batalla.')
history('Relámpago del Mar','objeto','El barco que recibe la tormenta',
        'La nave de Bonnie ataca con sus baterías mientras su capitana hace caer rayos sobre la Marina. Después los rayos golpean sus propias velas sin incendiarlas: la luz parece recorrer el casco hasta el timón. Transformado en una estela azul eléctrica, el Relámpago del Mar atraviesa la línea enemiga y parte varios barcos por la mitad.',
        ['42-107','42-116','42-123'],True,
        'Buque de Bonnie capaz de recibir rayos y atravesar naves enemigas envuelto en energía eléctrica.',
        'Nombre escuchado al describir su pasada; la escena no explica completamente su mecanismo mágico ni su construcción.')
history('Zampaolas','objeto','Cañonazos y giros en el arrecife',
        'El Zampaolas recibe impactos que abren el casco y arrancan una pieza añadida, por lo que su tripulación corre a reparar. Ione ordena redistribuir la carga y utiliza el ancla de Ilikar para cerrar un giro junto al espigón. La ballesta dispara primero a Cipo contra un barco y después un virote encadenado para enlazar naves enemigas. Mantiene la maniobra mientras el fuego cruzado y los refuerzos amenazan a la flota pirata.',
        ['42-101','42-104','42-112','42-113','42-114','42-121','42-122'])
history('Marina','faccion','Superioridad en el arrecife',
        'La Marina sostiene una línea de cañonazos coordinados y sigue recibiendo refuerzos pese a los barcos incendiados o partidos por Bonnie. En el Invictus, la confianza del mando en Hawkins facilita el sabotaje de dos escoltas y la recuperación de su pólvora provoca una vulnerabilidad que Pinky explota. La flota fuerza a varios piratas a virar o abandonar, aunque otros continúan luchando.',
        ['42-101','42-110','42-111','42-112','42-119','42-120','42-123','42-125'])
history('Tripulación del Zampaolas','faccion','Órdenes y soluciones durante la batalla',
        'Los tripulantes reparan el casco bajo el fuego y ejecutan las órdenes de Ione para preparar cañones y aflojar la carga. Poncelot, Jack e Ilikar combinan artillería, cadena y ancla para abrir huecos en la formación enemiga. La confusión inicial de Baps se corrige sin arrojar por la borda los suministros que la capitana necesita.',
        ['42-101','42-104','42-106','42-113','42-114','42-121'])
history('El Garfio','lugar','La batalla entre rocas y aguas estrechas',
        'El arrecife condiciona la batalla: solo un paso profundo permite a las grandes naves circular y sus aguas pueden engañarse mediante ilusiones. Nox hace encallar dos escoltas desviándolos hacia rocas ocultas; Ione utiliza el espigón y el ancla de Ilikar para cerrar la maniobra del Zampaolas. El Invictus termina atravesando el paso y asoma al combate bajo el rumbo fijado por Nox.',
        ['42-103','42-110','42-111','42-114','42-124'])

delivery = {'bloque':2,'lectura_completa':True,'primer_segmento':'c002157','ultimo_segmento':'c004311',
            'etapas':stages,'afirmaciones':facts,
            'misiones':[
                'Sobrevivir al fuego naval: el Zampaolas recibe daños y su gente comienza reparaciones; Ione combina carga, ancla y artillería para maniobrar sin que el bloque resuelva la batalla (42-101–42-106, 42-112–42-114, 42-121–42-125).',
                'Sabotear la Marina desde dentro: Nox encalla dos escoltas con ilusiones, libera a Pinky y duerme al mando del Invictus; ambos atacan a los marines y la pólvora mientras él conduce el buque hacia la batalla (42-108–42-111, 42-117–42-119, 42-124).',
                'Debilitar la formación enemiga: Ilikar rompe un mástil, Poncelot lanza a Cipo para incendiar otra nave y después enlaza barcos con una cadena; Bonnie destruye varios con rayos y una pasada eléctrica (42-105–42-107, 42-113, 42-116, 42-121–42-123).'
            ],
            'preguntas':[
                '¿Qué resultado tendrán la pólvora preparada por Nox y el rumbo del Invictus? En este tramo la mecha todavía no se enciende (42-124).',
                '¿Terminarán chocando los barcos enlazados y qué ocurrirá al abordaje de Ilikar y Cipo? El bloque deja al goliat impulsándose hacia las naves (42-121–42-122).',
                '¿Cómo resistirá la flota pirata los refuerzos continuos de la Marina? Los ataques de Bonnie animan a algunos, mientras otros abandonan (42-120, 42-123, 42-125).'
            ],
            'contradicciones':[
                'Ione aclara que quiere aflojar la carga, no tirarla al mar; la interpretación de Baps no se conserva como ejecución de esa orden (42-104).',
                'Nox propone trasladar hombres y munición, pero el mando decide recoger la carga y dejar a los hombres para no sobrecargar el Invictus (42-111).',
                'El mando del Invictus recibe tratamientos de capitán, almirante y palomo; la continuidad de órdenes y captura se conserva sin multiplicar personajes (42-110–42-111, 42-118).',
                'Cipo es el mismo elemental que incendia un barco y vuelve por la cadena; las bromas sobre producir más no prueban duplicación. La comparación de Bonnie con Fly tampoco introduce a Fly en el combate (42-113, 42-122–42-123).',
                'La presencia de Cipo aquí no explica por sí sola la procedencia del fragmento de espada de la escena anterior (42-113, 42-122).'
            ],
            'nombres_dudosos':[
                'Hawkin, Hawkins, señor Hin y variantes del vigía corresponden a Nox por continuidad; no se crea un piloto diferente (42-110–42-111, 42-117–42-118, 42-124).',
                'Pinky, Pinco y Pinko designan a la misma druida, cuya apariencia pasa a ser masculina al comer una fruta; no constituyen una nueva identidad (42-108–42-109, 42-117–42-119).',
                'Merlucilla es explícitamente un tigre en este tramo y se vincula a Merlucilla IV, conservando separado al tiburón Merlucilla V (42-101–42-102, 42-104).',
                'Ilicar e Ilikar corresponden al goliat; Jone, Yone y Jones, en las órdenes del Zampaolas, a Ione; Jacki y Yai a Jack por el disparo ordenado junto al cañón (42-103–42-106, 42-117).',
                'Invictus y Relámpago del Mar son barcos distintos del Zampaolas. El Arrecife del Garfio se conserva bajo El Garfio, sin establecer una región independiente a partir de este tramo (42-110–42-111, 42-123–42-124).',
                'El nombre Tórtola debe cotejarse con los otros bloques: aquí el mando es almirante, capitán o palomo y es la misma persona engañada y encadenada por Nox (42-110–42-111, 42-118).'
            ],'historias_entidades':histories}

assert len(facts) == 25
assert all(seconds(f['inicio']) <= seconds(f['evidencia_cue']['inicio']) <= seconds(f['fin']) for f in facts)
write_json(ROOT / 'borradores/42/entrega_2.json',delivery)
print(f'Entrega 2: {len(facts)} evidencias validadas, {len(stages)} etapas, {len(histories)} propuestas de historias.')
