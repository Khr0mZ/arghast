"""Entrega editorial del bloque 2, basada en su lectura completa y sin audio cotejado."""
from pathlib import Path
import hashlib
import json
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import parse_vtt, validate_fact

SEG = json.loads((BASE / 'bloque_2_segmentos.json').read_text(encoding='utf-8'))
ASIGNADAS = json.loads((BASE / 'preguntas_bloque_2.json').read_text(encoding='utf-8'))
FUENTE = ROOT / 'campanas/xoltacan/fuentes/47 - yvqhR20m7Zg.es-orig.vtt'
SHA = 'af82762727aa32ebc82b92459bdc4b039b6b17839c0f994d26f0a5aaf88e983e'
assert hashlib.sha256(FUENTE.read_bytes()).hexdigest() == SHA
assert len(SEG) == 1028
assert SEG[0]['id'] == 'c002057' and SEG[-1]['id'] == 'c004113'
assert all(x['texto_original'] == x['texto_normalizado'] for x in SEG)
assert (BASE / 'bloque_2.md').read_text(encoding='utf-8') == '\n\n'.join(
    f'[{x["inicio"]}–{x["fin"]}] {x["texto_original"]}' for x in SEG) + '\n'

TESA = 'Tesara Queen'
FELINO = 'Mictlan'
MUERTOS = 'Cadáveres movidos por raíces de las ruinas del lago'
DRAGON = 'Dragón verde del bosque de Iktan'
LUGAR = 'Ruinas de la orilla del lago de Iktan'
GRUPO = [TESA, FELINO, 'Tentacol', 'Chopito', 'Patata']
FACTS = []


def fact(numero, a, b, cita_indice, titulo, afirmacion, entidades, limitacion='', tipo='hecho_confirmado', conocedores=None):
    cue = SEG[cita_indice]
    FACTS.append({
        'id': f'47-{numero}', 'titulo': titulo, 'tipo': tipo,
        'afirmacion': afirmacion,
        'inicio': SEG[a]['inicio'], 'fin': SEG[b]['fin'],
        'cita': cue['texto_original'],
        'evidencia_cue': {'id': cue['id'], 'inicio': cue['inicio'], 'fin': cue['fin'], 'texto': cue['texto_original']},
        'entidades': entidades, 'ambito': 'combate e intrusión mental en el camino de Iktan',
        'conocedores': GRUPO if conocedores is None else conocedores,
        'conocimiento_personaje': 'desconocido',
        'nota_conocimiento': 'El acceso de Madame Oghma a este pasaje no está establecido. Los conocedores indican testigos de la escena o destinatarios del efecto; no incluyen a los elfos mostrados en las imágenes.',
        'confianza': 'lectura íntegra de subtítulos; audio no cotejado',
        'limitacion': limitacion or 'Se conserva la adjudicación de esta escena, sin añadir capacidades generales de bestiario ni resultados posteriores al intervalo.',
    })


fact(201, 0, 38, 21, 'Los expulsados se apartan de Patata',
     'Varios muertos animados emplean su movimiento en alejarse de Patata. La mesa aclara que la expulsión limita sus acciones a correr o destrabarse y que recibir daño permite volver a actuar. No todos ven a Patata; algunos se apartan sin localizarlo. La reducción de movimiento aplicada antes continúa afectando a uno de ellos.',
     ['Patata', MUERTOS],
     'El director distingue la expulsión de la condición de miedo. El bloque empieza con el efecto en curso; su lanzamiento pertenece al bloque anterior.')

fact(202, 39, 78, 72, 'Mictlan golpea y sufre el veneno de proximidad',
     'Mictlan se acerca y golpea con Booming Blade, aprovechando la ventaja contra un adversario que todavía no había actuado. Se le exige una salvación de Constitución por comenzar a menos de diez pies de una criatura. Tras fallarla queda envenenado hasta su siguiente turno y no puede recuperar puntos de vida durante ese efecto.',
     [FELINO, MUERTOS],
     'Los subtítulos dicen MD y otras variantes; el coordinador confirma Mictlan mediante la escena escrita posterior x-1531013198478708756, sin trasladar sus hechos a este bloque. La adjudicación no identifica una enfermedad permanente ni permite una ficha completa del enemigo.')

fact(203, 79, 119, 106, 'Tesara dispara para aliviar la presión sobre el felino',
     'Tesara ve al compañero felino en dificultades, sale de su escondite y dispara con ventaja. El impacto incorpora ataque furtivo y la marca de Favored Foe. Después se desplaza y vuelve a esconderse; el director advierte que su sigilo no garantiza por sí solo que el enemigo no la encuentre.',
     [TESA, FELINO, MUERTOS],
     'La conversación sobre concentración y Zephyr Strike pertenece a las reglas. No se añade daño de fuego: el director indica expresamente que el daño anunciado va sin fuego.')

fact(204, 120, 159, 147, 'Tentacol controla la distancia con el tentáculo y los rayos',
     'Tentacol coloca su tentáculo para atacar con la acción adicional y después lanza dos rayos. Los impactos desplazan a sus objetivos diez pies; aplica además una reducción de movimiento a uno. Se precisa que esa reducción no se aplica a todos por golpear dos veces. El grupo recuerda que dañar a un expulsado termina la limitación que lo hacía huir.',
     ['Tentacol', 'Chopito', MUERTOS],
     'Los nombres ingleses de conjuros aparecen deformados. El tentáculo invocado, Chopito y Tentacol no se convierten en una única criatura ni en tres nombres del mismo efecto.')

fact(205, 160, 216, 173, 'Mictlan esquiva y Patata sostiene la ofensiva',
     'Un muerto animado se coloca delante de Mictlan e intenta golpearlo dos veces; ambos ataques fallan. Patata responde con un impacto y mueve su espada espiritual, cuyo desplazamiento se corrige a veinte pies. Otros muertos siguen alejándose de él, mientras un adversario ya herido recupera la capacidad de avanzar y correr hacia el combate.',
     [FELINO, 'Patata', MUERTOS],
     'La comparación con el poder ilimitado y los comentarios sobre clérigos son bromas y reglas, sin revelación de un poder ilimitado de Patata.')

fact(206, 217, 270, 256, 'Una voz implanta la necesidad de atraer a dos elfos',
     'Durante la lucha el ambiente se vuelve pesado y todos realizan una salvación de Sabiduría contra una influencia de encantamiento. El director aplica el resultado a todos, incluida Tesara: sienten una presencia invasiva dentro de la cabeza, ven imágenes de dos elfos de piel pálida y reciben la orden de atraerlos al bosque. Saben que la idea es ajena, pero sienten la necesidad de cumplirla.',
     GRUPO + [DRAGON],
     'Las imágenes no certifican la situación real de los elfos en ese instante. La broma sobre los ruidos de la cocina no forma parte de la visión. La identidad de la voz se confirma dentro de este mismo bloque en 47-218.')

fact(207, 271, 300, 278, 'El tentáculo amortigua un golpe junto a Mictlan',
     'Un enemigo previamente herido puede volver a atacar al felino. Se aplica Guardian Coil para restar un dado de ocho al daño de uno de sus golpes. El director confirma un impacto y describe una respuesta de veneno que salta alrededor del atacante antes del siguiente golpe. Al comenzar su turno, Mictlan supera la salvación de Constitución exigida por los dos enemigos próximos.',
     [FELINO, 'Tentacol', MUERTOS],
     'La respuesta venenosa no recibe un nombre inequívoco de habilidad ni una explicación de origen. La corrección de la interfaz y las tiradas no permiten fijar una cifra total de daño no verbalizada.')

fact(208, 301, 359, 328, 'Un muerto se levanta y Mictlan lo remata',
     'Mictlan decide usar el estoque contra los dos adversarios cercanos. Al golpear a uno, el director resuelve una salvación de Constitución y lo devuelve a un punto de vida. Un nuevo impacto lo mata; aclara que no vuelve a emplear ese recurso al caer desde un solo punto de vida. La duda sobre si la expulsión debía destruirlos se resuelve indicando que estas criaturas no son las de desafío tan bajo a las que se refería el jugador.',
     [FELINO, 'Patata', MUERTOS],
     'Hay confusión momentánea de selección en la interfaz. El director termina identificando como muerto al objetivo de arriba; no se convierten los dos ataques en dos bajas ni se fija el valor de desafío exacto.')

fact(209, 360, 392, 369, 'Tesara elimina al segundo perseguidor del felino',
     'Tesara sale del escondite para quitarle al compañero felino el otro enemigo próximo. Obtiene un crítico y el director establece que el muerto cae sin poder hacer la tirada para levantarse. Al revisar el terreno, ella se queja de la voz que no deja de hablarle de los gemelos, se lleva una mano a la cabeza, cambia de posición y vuelve a esconderse.',
     [TESA, FELINO, MUERTOS, DRAGON],
     'Tesara llama gemelos a los elfos de las imágenes, pero este tramo no pronuncia sus nombres personales. La vinculación con Eldrath y Tryel debe integrarse con las fuentes de identidad de los otros bloques.')

fact(210, 393, 401, 398, 'La exigencia consiste en sacar a los elfos de la ciudad',
     'Ante una pregunta de la mesa, el director precisa el contenido de la visión: muestra a los dos elfos pálidos y pide sacarlos de la ciudad para llevarlos a la jungla. Se trata de entregárselos a la presencia, no de una amenaza que los elfos hayan comunicado al grupo.',
     GRUPO + [DRAGON],
     'El pasaje no explica por qué la presencia los quiere ni por qué necesita intermediarios; tampoco nombra la ciudad dentro de esta aclaración.',
     tipo='explicacion_director')

fact(211, 402, 410, 406, 'Chopito convierte la orden en su propio plan de rescate',
     'Chopito le dice a Tentacol que acaba de tener una visión de dos orejas picudas en una ciudad del interior del bosque y que necesitan ser rescatadas y llevadas a la jungla. La interpretación se presenta como un plan que Chopito se apropia; anima a Tentacol a terminar deprisa con los muertos para cumplirlo.',
     ['Chopito', 'Tentacol', DRAGON],
     'La necesidad de rescate es una interpretación de Chopito bajo la influencia, no una cautividad demostrada de los dos elfos ni una visión independiente del pulpo.',
     tipo='declaracion_personaje', conocedores=['Chopito', 'Tentacol'])

fact(212, 411, 438, 423, 'Tentacol abate a uno y retrasa a otro',
     'Tentacol utiliza su acción adicional y vuelve a disparar. El primer rayo acompañado de Hex deja a su objetivo muerto después de resolver la salvación; el segundo hiere a otro, lo empuja diez pies y reduce su movimiento otros diez. La ofensiva mantiene lejos a parte de los adversarios mientras continúan las imágenes mentales.',
     ['Tentacol', 'Chopito', MUERTOS])

fact(213, 439, 484, 443, 'El grupo mantiene los ataques a distancia',
     'Patata invoca el poder de su dios para un ataque radiante; el adversario supera su salvación. Después presta atención al compañero felino, aunque los subtítulos no permiten certificar una cantidad de curación. Los muertos avanzan despacio o continúan huyendo de la expulsión, y el siguiente turno mantiene dos impactos desde fuera del cuerpo a cuerpo para evitar gastar más recursos.',
     ['Patata', FELINO, MUERTOS],
     'No se adjudica daño al ataque radiante resistido ni una curación concreta al fragmento «vamos a ponerlo poco». El turno a distancia se atribuye por secuencia de iniciativa, sin inventar el nombre del conjuro.')

fact(214, 485, 500, 490, 'Tesara derriba a otro muerto y cambia de escondite',
     'Tesara continúa reduciendo el número de adversarios. Impacta y mata a un muerto que ya tenía un solo punto de vida; por ese estado no se vuelve a levantar. Ella analiza de nuevo la situación, se mueve y repite su maniobra para esconderse.',
     [TESA, MUERTOS])

fact(215, 501, 545, 540, 'Los rayos y el daño radiante acorralan a los últimos',
     'Tras una pausa técnica de la mesa, Tentacol recoloca el tentáculo, ataca y vuelve a empujar y ralentizar a los muertos con sus rayos. Patata mata a otro mediante daño radiante. Todavía queda movimiento de un adversario en el turno siguiente, por lo que la impresión de que solo faltaba uno no da el combate por terminado.',
     ['Tentacol', 'Patata', MUERTOS],
     'La pausa y las bromas de hackeo de Foundry son incidencias de la herramienta. La frase «tengo que buscar al elfa» se conserva como intención, sin afirmar que se encuentre o entregue a nadie.')

fact(216, 546, 552, 550, 'La voz promete una recompensa por los elfos',
     'La presencia vuelve a mostrar a los dos elfos y repite que se los lleven. Promete recompensar al grupo si los saca de la ciudad y los entrega fuera, en la jungla.',
     GRUPO + [DRAGON],
     'La promesa no acredita una recompensa disponible, cobrada o definida. No se especifica la condición de los elfos ni el motivo del encargo.',
     tipo='declaracion_personaje')

fact(217, 553, 606, 591, 'Las raíces reúnen los cuerpos en una masa',
     'El grupo termina con los muertos que quedaban, pero la voz continúa presionándolo. Las raíces, ramas y flores que movían aquellos cuerpos los arrastran por el suelo y los concentran en un punto. La presencia amenaza con que el grupo sufrirá la misma suerte si no obedece. Los cuerpos se unen en una masa enorme de zombis de la que caen fragmentos de cráneos y brazos; la lucha se reanuda contra esa forma colectiva.',
     GRUPO + [MUERTOS, DRAGON],
     'La formación de la masa se ve; la amenaza es una declaración de la voz. No se identifica la biografía de los cadáveres ni se demuestra que la voz causara todas sus muertes. La tirada para recargar tinta se permite, pero aquí no se anuncia su resultado.')

fact(218, 607, 633, 624, 'Tesara reconoce la voz de la intrusión anterior',
     'Tesara pregunta si conoce esa voz y recuerda el episodio anterior a la entrada en Iktan: viajaba con los elfos, los atacaron zombis y un dragón entró en su cabeza. El director confirma que es la misma voz. Distingue el efecto actual como una repetición intrusiva de imágenes y órdenes, más molesta e insistente que la manipulación que ella recuerda.',
     [TESA, DRAGON],
     'El reconocimiento enlaza ambas experiencias de Tesara. En este tramo no se pronuncia Clolgedranx ni se establece automáticamente la identidad con todos los dragones verdes catalogados; la frase sobre el disparo anterior queda incompleta.',
     tipo='explicacion_director', conocedores=[TESA])

fact(219, 634, 679, 671, 'Tesara localiza señales de una criatura que no puede ver',
     'Tesara decide buscar al responsable de la voz mientras los compañeros retienen la masa. Imagina un gran dragón verde, pero admite que nunca lo ha visto. La percepción revela hojas y flores aplastadas y ramas apartadas bajo presión en una zona entre los árboles. El director confirma que algo ocupa ese lugar, aunque la criatura sigue sin verse.',
     [TESA, DRAGON, LUGAR],
     'Se localiza una posición por efectos sobre la vegetación; no se describe un cuerpo visible ni se revela la causa o el método de su ocultación.',
     conocedores=[TESA])

fact(220, 680, 720, 695, 'Una rama rebota en la presencia oculta',
     'Tesara dispara contra la vegetación situada encima del hueco para hacer caer una rama o una maraña de lianas sobre lo que se oculta. La bala cruza cerca de Patata y del felino, rompe una rama y esta rebota sobre algo invisible. Se oye una risa y un comentario que reconoce su capacidad de observar. La rama no inmoviliza a la presencia y Tesara cambia de arbustos para esconderse otra vez.',
     [TESA, DRAGON, 'Patata', FELINO, LUGAR],
     'El resultado es una rama que golpea o rebota sobre algo oculto, sin daño cuantificado, red eficaz o revelación visual. El director comenta que se ha tirado una rama sobre un dragón.',
     conocedores=[TESA])

fact(221, 721, 751, 747, 'Tentacol maldice y desplaza la masa',
     'Tentacol aplica Hex a la masa, eligiendo desventaja en pruebas de Fuerza, y la hiere con sus rayos. Tras consultar si el tamaño impediría el empuje, el director permite desplazarla diez pies y reducir su movimiento. Durante ese turno se recuerda a Tesara que dispone de una bendición de un dado de cuatro.',
     ['Tentacol', MUERTOS, TESA],
     'La desventaja se precisa para pruebas de característica, no para toda salvación de Fuerza. Las bromas sobre disparar a una rama o lanzar una bola de fuego no adjudican un segundo ataque contra el dragón.')

fact(222, 752, 799, 794, 'Patata evita quedar envuelto en los cadáveres',
     'Al haber sido alejada la masa, Patata se queda donde estaba y no logra una ofensiva eficaz en ese turno. La criatura avanza y se arroja sobre él para envolverlo. Patata supera la salvación de Fuerza: recibe daño, pero no queda atrapado dentro y la masa cae a su lado.',
     ['Patata', MUERTOS],
     'Evitar el envolvimiento no equivale a ser inmune a posesiones. La frase «la patata no se puede poseer» es una broma posterior al éxito de la salvación.')

fact(223, 800, 827, 808, 'Mictlan maldice a la masa y dispara desde lejos',
     'Tras un turno oculto del adversario, Mictlan impone su propia maldición a la masa: explica que añade dos puntos de daño y amplía los críticos a diecinueve y veinte. Prefiere atacar desde su posición mientras Patata está junto a la criatura. El primer ataque falla y el segundo impacta.',
     [FELINO, 'Patata', MUERTOS],
     'La habilidad no se equipara a Hex solo por llamarse maldición. La broma sobre que la masa abraza a Patata no revoca la salvación superada ni establece que esté apresado.')

fact(224, 828, 870, 852, 'Tesara descubre que la presencia cambió de sitio',
     'Tesara vigila la zona donde detectó la presencia y usa su acción para examinarla. Las hojas y ramas están recuperando su posición: algo ha dejado de presionarlas y la criatura ya no está allí. No dispone de una segunda acción para localizarla de inmediato. Considera Zephyr Strike, lo descarta para conservar la posibilidad de esconderse y se desplaza a otros arbustos.',
     [TESA, DRAGON, LUGAR],
     'No se adjudica el lanzamiento de Zephyr Strike. El director describe un indicio de movimiento, sin revelar la nueva posición en este turno.',
     conocedores=[TESA])

fact(225, 871, 898, 884, 'Tentacol vuelve a apartar la masa de Patata',
     'Tentacol intenta acercar el tentáculo y el director señala un muro que impide atravesar la ruta elegida. Lo recoloca por un paso permitido y golpea a la masa, añadiendo Hex. Un rayo posterior la vuelve a empujar diez pies y los efectos del rayo y del tentáculo le reducen el movimiento.',
     ['Tentacol', 'Patata', MUERTOS, LUGAR],
     'La corrección de la tirada de daño no proporciona una estadística completa del enemigo. El muro es un obstáculo del escenario; no basta para fijar un edificio, templo o civilización.')

fact(226, 899, 947, 945, 'Patata deshace la masa y las raíces se retiran',
     'Patata golpea primero con el arma espiritual. La criatura supera una salvación y queda a un punto de vida. Su siguiente ofensiva acaba con ella: la masa se dispersa en cuerpos que caen por el suelo. El director confirma que todos esos cadáveres están totalmente inertes y que las raíces se retiran hacia la tierra. La presencia que Tesara sigue permanece oculta; un intento de localizarla a ella no tiene éxito.',
     ['Patata', MUERTOS, DRAGON, TESA],
     'La destrucción de la masa y la retirada de las raíces no prueban la muerte del dragón o el final de su influencia. No se certifica visión verdadera: el director rechaza que esa sea la explicación de la búsqueda de Tesara.')

fact(227, 948, 975, 971, 'Mictlan busca a los compañeros y no encuentra a Tesara',
     'Al no ver más enemigos, Mictlan empieza a comprobar cómo están los demás. Puede localizar a Patata y Tentacol, pero la búsqueda de Tesara no supera su escondite. El director conserva los turnos de combate y pide esperar al turno de cada cual para cualquier asistencia o curación.',
     [FELINO, 'Patata', 'Tentacol', TESA],
     'Tesara no ha desaparecido de la escena ni está secuestrada: permanece escondida. La intención de curar al felino no es todavía una curación resuelta.')

fact(228, 976, 1013, 989, 'Tesara encuentra el nuevo hueco y retrocede en sigilo',
     'Tesara utiliza la bendición disponible en una nueva percepción y encuentra otro hueco entre los árboles semejante al anterior. Comprende que la presencia está ahora enfrente de ella, pero ya ha gastado su acción en buscarla. Decide retroceder despacio y vuelve a tirar sigilo por haberse movido.',
     [TESA, DRAGON, LUGAR],
     'La posición se deduce otra vez por vegetación desplazada; no se obtiene visión directa. Su nueva tirada de sigilo no demuestra por sí sola que el perseguidor haya dejado de poder detectarla.',
     conocedores=[TESA])

fact(229, 1014, 1020, 1017, 'Tentacol se dirige a buscar a los elfos',
     'Una vez destruida la masa, Tentacol anuncia que deben buscar a los elfos y se pone en camino corriendo hacia el bosque. La acción sigue el propósito que Chopito había defendido después de recibir la intrusión.',
     ['Tentacol', 'Chopito', DRAGON],
     'No llega a encontrar, sacar de la ciudad o entregar a los elfos dentro del bloque. Se conserva el sentido de la declaración sin convertir la propuesta de rescate de Chopito en un secuestro ocurrido.')

fact(230, 1021, 1027, 1024, 'Patata ofrece ayuda y pregunta el nombre del felino',
     'Patata se acerca al compañero felino para echarle una mano y le pregunta cómo se llama. El otro responde con el nombre que los subtítulos escriben «mi clan»; Patata propone abreviarlo como Mic y la mesa repite la pronunciación.',
     ['Patata', FELINO],
     'La grafía Mictlan está confirmada por el coordinador con la escena escrita posterior x-1531013198478708756; se conserva mi clan en la cita. El corte se produce antes de resolver una curación o cualquier otra ayuda concreta.',
     conocedores=['Patata', FELINO])


def refs(*numbers):
    return [f'47-{n}' for n in numbers]


ETAPAS = [
    {
        'titulo': 'La expulsión abre espacio en el combate',
        'texto': 'Los muertos continúan apartándose de Patata, aunque la expulsión solo los contiene mientras nadie los hiera. Mictlan se aproxima con su estoque y Booming Blade, pero la cercanía de las criaturas lo envenena e impide que recupere fuerzas durante el efecto. Tesara sale de su escondite para aliviar la presión sobre el felino, dispara con ventaja y ataque furtivo y vuelve a ocultarse. Tentacol combina el tentáculo y los rayos para empujar a los enemigos y hacer más lento su regreso. Los dos ataques de un muerto no alcanzan a Mictlan; Patata aprovecha el espacio y desplaza su espada espiritual. Algunos cuerpos siguen huyendo y otros, ya heridos, pueden volver a acercarse.',
        'referencias': refs(201, 202, 203, 204, 205),
    },
    {
        'titulo': 'Dos elfos en una orden que nadie ha elegido',
        'texto': 'En medio de la pelea cae una pesadez extraña sobre el grupo. La salvación no evita que una voz irrumpa en sus cabezas, les muestre dos elfos pálidos y les imponga la necesidad de atraerlos al bosque. Todos perciben la intrusión y saben que el impulso viene de fuera. La lucha continúa: el tentáculo reduce parte de un golpe junto a Mictlan y se produce una respuesta venenosa; después el felino resiste el efecto de proximidad, derriba a uno de sus adversarios y lo remata cuando este se levanta a un punto de vida. Tesara elimina al otro con un crítico que impide su retorno. Se queja de la voz y de los gemelos mientras cambia de escondite. El director precisa lo exigido: sacar a los elfos de la ciudad y entregarlos en la jungla. Chopito le cuenta a Tentacol que ha recibido una visión y transforma el encargo en un supuesto rescate, como si el plan fuese suyo. Tentacol lo escucha y continúa disparando. Patata invoca daño radiante y atiende a la situación del felino; los subtítulos no fijan aquí una curación concreta. Entre los ataques a distancia, los empujones y la lentitud impuesta a los adversarios, Tesara derriba a otro y Patata termina con uno mediante daño radiante.',
        'referencias': refs(206, 207, 208, 209, 210, 211, 212, 213, 214, 215),
    },
    {
        'titulo': 'La amenaza se construye con los muertos',
        'texto': 'La voz vuelve a enseñar a los elfos y ofrece una recompensa por llevarlos fuera. Al caer los últimos muertos, el peligro cambia de forma: las raíces y ramas que los movían arrastran los cuerpos hacia un punto y los reúnen en una masa enorme, de la que se desprenden brazos y trozos de cráneo. La presencia amenaza a los viajeros con acabar igual que ellos si no obedecen. Tesara distingue esa voz de la masa de cadáveres y pregunta por su familiaridad. Recuerda la experiencia anterior a Iktan, cuando viajaba con los elfos y un dragón penetró en su cabeza; el director confirma que oye la misma voz. Ahora la presión consiste en repetir las imágenes y el encargo de manera invasiva. Ella decide buscar al responsable mientras los demás contienen a la masa. Entre los árboles descubre flores aplastadas y una rama desviada por presión, aunque no consigue ver a la criatura. Dispara por encima del hueco para dejarle caer vegetación: una rama rebota sobre algo invisible, que se ríe y elogia su observación. El intento no lo inmoviliza. Tesara cambia de arbustos y vuelve al sigilo.',
        'referencias': refs(216, 217, 218, 219, 220),
    },
    {
        'titulo': 'La masa no logra envolver a Patata',
        'texto': 'Tentacol aplica Hex a la masa y la aleja con sus rayos. Patata renuncia a acercarse después del empujón y sus intentos de ese turno no prosperan. La criatura se arroja sobre él para envolverlo: la salvación de Fuerza le permite resistirse y quedar fuera, aunque recibe daño. Mictlan maldice al enemigo y mantiene la distancia; falla un disparo y acierta el siguiente. Tesara dedica otro turno a vigilar el lugar del ocupante oculto y ve las ramas recobrar su posición. La presencia se ha desplazado. Al gastar su acción en buscarla no puede localizarla otra vez en ese momento; descarta Zephyr Strike para conservar la maniobra de ocultarse. Tentacol sortea un muro para recolocar el tentáculo y vuelve a golpear, empujar y ralentizar la masa. Patata la alcanza con su arma espiritual; el enemigo aún resiste a un punto de vida, pero su siguiente ataque lo deshace. Los cuerpos quedan esparcidos e inertes y las raíces regresan a la tierra.',
        'referencias': refs(221, 222, 223, 224, 225, 226),
    },
    {
        'titulo': 'La presencia sigue cerca cuando el grupo empieza a dispersarse',
        'texto': 'El final de la masa no descubre al responsable. El director mantiene los turnos y un intento de detectar a Tesara falla. Mictlan comprueba cómo están Patata y Tentacol, pero tampoco encuentra a la historiadora, que continúa escondida. Ella emplea una bendición en otra búsqueda y reconoce un nuevo hueco entre los árboles: la presencia está ahora delante. Como ha gastado su acción en localizarla, opta por retirarse poco a poco y volver a probar su sigilo. Tentacol, entretanto, anuncia que ya pueden buscar a los elfos y corre hacia el bosque. Patata ofrece ayuda al compañero felino y le pregunta su nombre; recibe la respuesta transcrita «mi clan» y propone llamarlo Mic. El bloque termina antes de que se resuelva esa ayuda o de que Tentacol alcance a los elfos.',
        'referencias': refs(226, 227, 228, 229, 230),
    },
]


def historia(nombre, tipo, descripcion, nota, etapas, nueva=False):
    return {'nombre': nombre, 'tipo': tipo, 'nueva': nueva, 'descripcion': descripcion,
            'nota': nota, 'etapas': [{'titulo': t, 'texto': x, 'referencias': refs(*rr)} for t, x, rr in etapas]}


HISTORIAS = [
    historia(TESA, 'personaje', 'Historiadora humana que combate con disparos y sigilo y rastrea a la presencia intrusiva.',
        'Tesa es Tesara Queen según el catálogo; se conserva su diferencia de conocimiento frente a los compañeros.', [
        ('Disparos para proteger al felino', 'Sale repetidamente de sus escondites, aplica ataque furtivo y acaba con los adversarios cercanos a Mictlan. Un crítico impide a uno de ellos levantarse. La voz que insiste en los gemelos la obliga a actuar mientras soporta una idea ajena.', [203, 209, 214]),
        ('La misma voz, un rastro invisible', 'Reconoce con ayuda del director la voz de la experiencia anterior con los elfos. En lugar de limitarse a atacar la masa busca al responsable, detecta vegetación aplastada y hace caer una rama que rebota sobre algo invisible. Al advertir que ese ocupante ha cambiado de lugar, lo rastrea otra vez con una bendición y retrocede al encontrarlo enfrente.', [206, 218, 219, 220, 224, 228]),
        ('Un escondite que también separa de los aliados', 'Los intentos de la presencia y de Mictlan no logran localizarla en ese momento. Mantiene el sigilo mientras Tentacol decide salir hacia los elfos.', [226, 227, 228, 229]),
    ]),
    historia('Patata', 'personaje', 'Agricultor y clérigo que contiene a los muertos y acaba con su masa colectiva.',
        'No se adjudica una deidad nueva ni se convierte la broma sobre la posesión en inmunidad.', [
        ('Expulsión y fuerza radiante', 'Mantiene a parte de los muertos apartados hasta que los golpes permiten su regreso. Los combate con magia, espada espiritual y daño radiante. Colabora en sostener al compañero felino sin que el fragmento permita fijar la curación inicial.', [201, 205, 213, 215]),
        ('Resistir el peso de los cadáveres', 'Soporta el intento de la masa de envolverlo: supera la salvación, recibe daño y queda fuera. Después la golpea hasta dispersarla y hacer cesar el movimiento de los cuerpos.', [222, 225, 226]),
        ('Tender una mano y conocer un nombre', 'Ofrece ayuda al compañero felino y pregunta su nombre. La respuesta se transcribe mi clan y Patata propone Mic; la resolución de la ayuda queda en el bloque siguiente.', [227, 230]),
    ]),
    historia(FELINO, 'personaje', 'Combatiente felino del camino de Iktan, llamado mi clan, Mlan o MD por el reconocimiento automático.',
        'Grafía Mictlan confirmada por el coordinador al leer completa la escena escrita posterior x-1531013198478708756; el bloque 1 recoge la presentación Mlan y este bloque mi clan/Mic. Esta confirmación solo fija la identidad; no se incorporan los hechos de la escena posterior. No se fija especie por el apodo gatito.', [
        ('Estoque, veneno y auxilio', 'Se acerca con Booming Blade y sufre el efecto venenoso que impide curarse. Esquiva dos ataques, recibe después otro parcialmente amortiguado por el tentáculo y vuelve a resistir la exposición de proximidad. Remata a un enemigo que acaba de levantarse con un punto de vida; Tesara elimina al otro de su lado.', [202, 203, 205, 207, 208, 209]),
        ('Distancia y preocupación por los demás', 'Contra la masa usa una maldición que mejora sus golpes y críticos y ataca desde lejos. Al ver los cuerpos inertes comprueba cómo están los compañeros. No encuentra a Tesara escondida. Patata le ofrece ayuda y pregunta cómo llamarlo.', [223, 226, 227, 230]),
    ], nueva=True),
    historia('Tentacol', 'personaje', 'Viajero acuático vinculado a Chopito que controla la distancia mediante un tentáculo y rayos.',
        'El tentáculo es un efecto de combate; se conserva separado de la identidad del pulpo y del viajero.', [
        ('Impedir que vuelvan los muertos', 'Empuja y ralentiza a los enemigos mientras su tentáculo golpea y reduce parte del daño de un ataque cercano al felino. El apoyo sostenido permite reducir su número sin que todos lleguen al cuerpo a cuerpo.', [204, 207, 212, 215]),
        ('Contra la forma colectiva', 'Aplica Hex y sigue golpeando a la masa, incluida una maniobra que debe rodear un muro del escenario. Los empujones la apartan y sus efectos reducen de nuevo la movilidad.', [221, 225]),
        ('Aceptar el supuesto rescate', 'Escucha la versión de Chopito sobre los elfos que necesitan ayuda. Después de dispersar la masa anuncia que deben buscarlos y corre hacia el bosque. La localización y entrega todavía no ocurren.', [206, 210, 211, 229]),
    ]),
    historia('Chopito', 'personaje', 'Pulpo telepático vinculado a Tentacol que interpreta la intrusión como un rescate.',
        'Su declaración de haber recibido la visión no prueba un mensaje independiente ni que conozca la situación real de los elfos.', [
        ('Un mandato presentado como idea propia', 'Cuenta a Tentacol que ha visto a dos orejas picudas en una ciudad del bosque y que deben rescatarlas y llevarlas a la jungla. Anima a terminar deprisa con los muertos y presenta el propósito como su propio plan.', [206, 210, 211, 229]),
    ]),
    historia(DRAGON, 'personaje', 'Presencia oculta cuya voz coincide con la intrusión sufrida antes por Tesara.',
        'En este bloque no se pronuncia un nombre personal. La coincidencia de voz se confirma; la fusión con Clolgedranx requiere la integración de identidades del coordinador.', [
        ('La exigencia sobre los dos elfos', 'Impone imágenes y el impulso de sacar a dos elfos pálidos de la ciudad para llevarlos a la jungla. Repite el mandato, ofrece una recompensa y amenaza con la suerte de los cadáveres. El fin que persigue y el motivo de recurrir a intermediarios siguen sin explicación.', [206, 210, 216, 217]),
        ('Seguido sin ser visto', 'Tesara conoce su posición por las ramas y flores aplastadas. Una rama rebota sobre algo invisible y recibe una respuesta burlona. La criatura se cambia de lugar durante la pelea; después Tesara detecta un nuevo hueco delante de ella. Ni la caída de la masa ni ese rastreo muestran su derrota.', [218, 219, 220, 224, 226, 228]),
    ]),
    historia(MUERTOS, 'personaje', 'Conjunto de cadáveres animados del camino que termina reunido por raíces en una sola masa.',
        'Nombre editorial descriptivo compartido con el bloque 1. La masa es una etapa del mismo conjunto de cuerpos. No se asigna especie de bestiario, origen o identidad individual a sus víctimas.', [
        ('Cuerpos que regresan a la lucha', 'Se apartan de Patata por la expulsión y pueden volver a actuar cuando reciben daño. La proximidad de algunos obliga a salvar contra veneno. Uno se levanta con un punto de vida; un nuevo golpe lo remata. El crítico y el daño radiante resuelven otras bajas sin nuevos levantamientos.', [201, 202, 205, 208, 209, 212, 214, 215]),
        ('La masa de cadáveres', 'Al terminar la primera lucha, raíces y ramas arrastran los cuerpos, los apilan y forman una criatura enorme de restos que se desprenden. La masa intenta envolver a Patata y fracasa, aunque lo hiere. Soporta maldiciones, impactos y empujones hasta que Patata la deshace; todos los cuerpos quedan inertes y las raíces se retiran.', [217, 221, 222, 223, 225, 226]),
    ], nueva=True),
    historia(LUGAR, 'lugar', 'Tramo del bosque en el trayecto de Iktan donde se combate entre árboles, raíces, flores y un muro.',
        'Denominación editorial compartida con el bloque 1. Este tramo mantiene el mismo escenario entre árboles y muros; no fija coordenadas, edificio o identidad con otros claros anteriores.', [
        ('Vegetación que actúa y deja huellas', 'Raíces y ramas mueven a los cadáveres y los reúnen en una masa. Esa misma vegetación permite a Tesara localizar por presión al ocupante invisible. Las ramas recobran su posición al moverse la criatura y después dejan un nuevo hueco; un muro limita el recorrido del tentáculo.', [217, 219, 220, 224, 225, 226, 228]),
    ], nueva=True),
]

MISIONES = [
    {'titulo': 'Superar a los muertos del camino', 'estado': 'cumplida en el bloque',
     'texto': 'Los muertos individuales y su masa final son destruidos. El director confirma cuerpos inertes y raíces que se retiran; la presencia invisible continúa sin ser derrotada.',
     'referencias': refs(201, 208, 209, 214, 215, 217, 226)},
    {'titulo': 'Encontrar al responsable de la voz', 'estado': 'en curso',
     'texto': 'Tesara reconoce la voz y localiza dos posiciones sucesivas por sus efectos sobre los árboles. No llega a ver directamente a la criatura, apresarla o terminar con la intrusión.',
     'referencias': refs(218, 219, 220, 224, 228)},
    {'titulo': 'Sacar a los dos elfos de la ciudad', 'estado': 'mandato de la presencia; ejecución iniciada por Tentacol',
     'texto': 'El encargo se implanta mentalmente y se acompaña de promesa de recompensa y amenaza. Chopito lo interpreta como un rescate y Tentacol corre a buscarlos. No se encuentran ni se entregan dentro del bloque.',
     'referencias': refs(206, 210, 211, 216, 217, 229)},
    {'titulo': 'Atender al compañero felino', 'estado': 'ayuda ofrecida; resolución por cotejar',
     'texto': 'El grupo alivia la presión sobre Mictlan y Patata ofrece echarle una mano al final. La curación concreta y el estado posterior requieren el bloque siguiente.',
     'referencias': refs(203, 207, 213, 227, 230)},
]

PREGUNTAS = [
    {'pregunta': '¿Por qué la voz quiere que los viajeros saquen a los dos elfos de la ciudad y qué pretende hacer con ellos?',
     'estado': 'pendiente', 'respuesta': 'La presencia ordena llevarlos a la jungla y ofrece una recompensa, sin explicar el fin ni la necesidad de intermediarios.',
     'pendiente': 'Motivo del encargo, identidad integrada de los dos destinatarios y desenlace de la entrega.', 'referencias': refs(206, 210, 216, 217, 229)},
    {'pregunta': '¿Podrán resistir o terminar el impulso que la voz les ha implantado?',
     'estado': 'pendiente', 'respuesta': 'Todos reconocen que el impulso es ajeno, pero sienten necesidad de cumplirlo; Chopito lo presenta como un plan de rescate y Tentacol sale a buscar a los elfos.',
     'pendiente': 'Duración, condiciones de finalización y decisiones posteriores de todos los afectados.', 'referencias': refs(206, 211, 218, 229)},
    {'pregunta': '¿Logrará Tesara descubrir y enfrentar a la criatura que sigue entre los árboles?',
     'estado': 'parcial', 'respuesta': 'Confirma que la voz coincide con la experiencia anterior y encuentra dos posiciones sucesivas por vegetación desplazada; una rama rebota sobre algo invisible.',
     'pendiente': 'Ver directamente a la criatura, fijar su identidad completa y resolver la persecución.', 'referencias': refs(218, 219, 220, 224, 228)},
    {'pregunta': '¿De dónde proceden los cadáveres animados y cómo se relaciona su movimiento con la presencia oculta?',
     'estado': 'parcial', 'respuesta': 'Se observan raíces y ramas que reúnen los cuerpos en una masa mientras la voz amenaza con un destino semejante. Al ser destruida la masa las raíces vuelven a la tierra.',
     'pendiente': 'Identidades y causa de muerte de las víctimas, mecanismo de animación y responsabilidad concreta de la presencia.', 'referencias': refs(217, 226)},
    {'pregunta': '¿Qué hará Tentacol al encontrar a los elfos y qué papel tendrá Chopito en su decisión?',
     'estado': 'pendiente', 'respuesta': 'Chopito defiende un supuesto rescate y Tentacol inicia el desplazamiento para buscarlos. El bloque termina antes de localizar a nadie.',
     'pendiente': 'Encuentro, información que transmita al grupo y aceptación o rechazo del mandato.', 'referencias': refs(211, 229)},
]

# Cada motivo se redactó tras leer el texto completo de su pregunta, respuesta,
# pendiente y referencias; no se convierte la mera ausencia en un desenlace.
COTEJO_RAZONES = {
    'P12-006': 'No se recibe ni se lee la carta del campamento destinada al capitán o a Molly.',
    'P12-007': 'No se revisa el mapa de los marines ni se relaciona el camino de Iktan con sus marcas de investigación.',
    'P12-008': 'No aparece el mondadientes de Bling; su recuperación ya resuelta no recibe novedades.',
    'P12-009': 'No aparece Pinky ni se narra la reversión de oveja o el final de aquellas alucinaciones.',
    'P13-001': 'Los muertos del camino no se identifican con el cuerpo del nawal y no se informa de quién lo retiró.',
    'P13-002': 'La vegetación y el muro del combate no se identifican con el templo de la danza ni explican a sus constructores.',
    'P13-003': 'No se plantan las semillas recogidas ni se modifica el escudo con esos materiales.',
    'P13-004': 'Patata combate, pero no recuerda cómo salió con el tesoro de aquella plataforma.',
    'P13-005': 'No se anuncian nuevas tiradas o resultados del botín de Kilzer en el sótano.',
    'P13-006': 'No intervienen Kilzer, Nox o Bonny para explicar el reparto y las cláusulas del casino.',
    'P13-007': 'No se trata el sombrero de Nox ni la recuperación de Jack; se conserva el desenlace anterior.',
    'P14-001': 'La voz del bosque se enlaza con la experiencia previa de Tesara, sin identificarla con la entidad del diario mercante.',
    'P14-002': 'No aparecen la mujer del bote ni la hija espectral y no se explica su coincidencia de rostro.',
    'P14-003': 'La amenaza de la voz no amplía la acusación del marinero de la lengua enjaulada.',
    'P14-004': 'Los cadáveres de este combate no proporcionan información del mercante, su hija o sus almas.',
    'P14-005': 'Las maldiciones usadas contra la masa son efectos de este combate; no se vinculan con la moneda negra de Eldrath.',
    'P14-006': 'La recompensa prometida por la voz se refiere a sacar a los elfos, sin aclarar la convocatoria o el pago de Bonny por el mercante.',
    'P14-007': 'Las imágenes de dos elfos y el reconocimiento de Tesara no explican el origen de Eldrath y Tryel ni el episodio de las dríadas.',
    'P14-008': 'No se trata el sombrero del nido del loro; no cambia su recuperación anterior.',
    'P15-001': 'No se trata la muerte de Aerendriel ni la detención por Bonny; no cambia el desenlace anterior.',
    'P15-002': 'No aparece Jack ni se habla de Puerto de Espadas, Lucy, cobros o del Jackie referido por Taylor.',
    'P15-003': 'No se identifica la aldea caníbal del capítulo 15 ni se explica aquel secuestro.',
    'P15-004': 'Que estos muertos vuelvan a levantarse no descifra ni vincula causalmente el tatuaje del combatiente del capítulo 15.',
    'P15-005': 'No se muestran ingresos, cosechas o apertura del casino. Las acciones de Patata aquí son de combate.',
    'P15-006': 'No se nombra el dragón compañero de Aerendriel. La voz corresponde al episodio de Tesara y no identifica a ese compañero. El contexto autorizado ya fija Zarynth; coordinar corrección con su fuente externa, sin atribuirla a este bloque.',
    'P15-007': 'No aparece Citlali ni se diagnostica su maldición. La exposición venenosa del felino es otra condición.',
    'P16-001': 'No se reconstruyen ejecutor, método o incumplimiento por la muerte de Aerendriel.',
    'P16-002': 'La presencia perseguida por Tesara no se identifica como Zarynth ni se trata el negocio de Bonny con Nox.',
    'P16-003': 'La animación de cadáveres y la voz no se vinculan a la prisión de la visión de Walulu ni identifican a lo despertado.',
    'P16-004': 'No se convoca o celebra el concilio ni se añaden asistentes a las promesas anteriores.',
    'P16-005': 'No se designa al campeón solar ni se relaciona con Ayoto. La magia radiante de Patata no satisface esa identificación.',
    'P16-006': 'No aparecen las visitantes alada y mediana de Eromov ni se conocen sus nombres.',
    'P16-007': 'No aparecen la mujer de Cuicapalli o Ayoto ni se añade un vínculo con la nawal.',
    'P16-008': 'Las flores del bosque sirven de indicio de presión y animación; no se identifican con las plantas fucsias del kenku o los tubos de Lunaria.',
    'P16-009': 'No se reconstruye la ruta de Lunaria ni se precisa el tatuaje festivo de Naór.',
    'P17-001': 'No se menciona Atlan ni se añaden coordenadas o grafía a su ubicación.',
    'P17-002': 'No aparecen los gobernantes de Ras Racor ni se dan términos de su alianza.',
    'P17-003': 'El mandato sobre los elfos no convoca el concilio de Tutucan; no se representa su celebración.',
    'P17-004': 'No se investigan los avistamientos de la patrulla ni se vinculan los muertos actuales con la crisis de Cuicapalli.',
    'P18-001': 'No se estudian las botas, la palabra tiempo o las heridas de Citlali. La intrusión no explica sus marcas.',
    'P18-002': 'No aparecen las víctimas marinas del templo ni su ritual de sangre; los cuerpos del camino siguen sin identidad.',
    'P18-003': 'La invocación radiante de Patata no nombra a Lares, Larcamas o Set ni establece equivalencias entre deidades.',
    'P18-004': 'La presencia actual se enlaza con una experiencia previa de Tesara, sin identificar la sombra del cierre del capítulo 18.',
    'P19-001': 'No aparece el collar ni se identifica su presencia con la voz del bosque. El movimiento actual de cadáveres por raíces no confirma control del dinosaurio de la charca.',
    'P19-002': 'No se produce drenaje de Citlali ni se explican rejuvenecimiento o daño durante su curación anterior.',
    'P19-003': 'No aparece Leona ni el collar de Bling, y no se ejecuta su entrenamiento o custodia.',
    'P20-001': 'No aparecen Arcan o Zarial ni una explicación de la búsqueda de fuerza.',
    'P20-002': 'No se estudia el mapa de Poncelot o la X junto a Slaz; el muro del combate no fija ese destino.',
    'P20-003': 'No se trata el campamento del gas ni la desaparición anterior de Eldrath. Las imágenes de elfos no explican aquel cometido.',
    'P20-004': 'La masa de cuerpos no se identifica con la criatura de tres cabezas de la tradición leonina.',
    'P21-001': 'Ninguno de los cadáveres se identifica como la tercera criatura arrastrada del antiguo campamento.',
    'P21-002': 'No aparecen el humano-lobo, las marcas lunares o el estanque ni se establece su relación con el culto.',
    'P21-003': 'La voz y las imágenes de elfos no nombran a la mujer pez de la visión del collar.',
    'P21-004': 'No aparece Leo ni se trata su custodia por Eromov o la evolución de sus secuelas.',
    'P22-001': 'No se reconstruye la infiltración del festival ni la demanda del collar a Citlali.',
    'P22-002': 'No aparece Bling ni se transmite el aviso de Eromov. La orden actual tiene otros destinatarios.',
    'P22-003': 'No aparece Guayacán ni se declara su especie o linaje; los apodos felinos de Mictlan corresponden a otra persona.',
    'P22-004': 'Buscar a los elfos no equivale a ejecutar la expedición al norte ni a celebrar el concilio.',
    'P23-001': 'La voz no se identifica con la serpiente del foso de Aurora ni explica a su diosa o su conocimiento de Hawkins.',
    'P23-002': 'La ciudad de los elfos no recibe una equivalencia con la ciudad no verbalizada de los documentos o con Slaz.',
    'P23-003': 'No se trata el símbolo de Nox o el alto cargo llamado palomo; no se confirma su equivalencia con Tórtola.',
    'P23-004': 'No se informa del galeón a la deriva, de los perros aliados o de los presos de Aurora.',
    'P24-001': 'No se trata el robo a Bonny o los impostores de la costa; la presencia del bosque no se vincula con ellos.',
    'P24-002': 'El tentáculo de Tentacol es un efecto de combate, sin uso de la perla, lectura de coordenadas o reparación de la concha.',
    'P24-003': 'No aparece Sam ni Ione ni se explica la reacción de ella a su nombre.',
    'P24-004': 'La comparación humorística del pulpo con Coyote no revela una identidad anterior de Coyote ni lo equipara con Citlali.',
    'P24-005': 'La recarga de tinta de Chopito se plantea como recurso del pulpo; no son las máquinas y la tinta del servicio de tatuajes de Gobs.',
    'P25-001': 'El mandato de la voz sobre los elfos no identifica al mandante del ataque a Shiaru o la necesidad del mapa y collar.',
    'P25-002': 'La localización actual junto a Iktan no recibe identificación con Ezlat o Slaz ni aclara su entidad del templo.',
    'P25-003': 'No aparece el collar de Bling ni se determina una relación con otros collares.',
    'P25-004': 'El arma espiritual de Patata y los recursos de combate de sus compañeros no identifican los pergaminos robados o los efectos de la espina-lanza.',
    'P26-001': 'No aparecen las marcas de Nox ni se explica su contenido o quién pretende obtenerlas.',
    'P26-002': 'Nadie se sienta en el trono de la pirámide ni se demuestra su efecto.',
    'P26-003': 'El reconocimiento de la voz por Tesara no la identifica como controlador del guardia de ojos rojos o como nuestro Señor.',
    'P26-004': 'No se reconstruye la suplantación de Ione por Coyote ni el uso del informe de Poncelot.',
    'P26-005': 'No aparecen los reyes piratas ni se conocen nuevos términos o decisiones de su pacto.',
    'P27-001': 'No aparecen los hombres de azul ni se explica el objetivo del ataque a Cuicapalli o sus supervivientes.',
    'P27-002': 'No aparece Guayacán ni se amplía quién conoce el secreto de su traje y pico.',
    'P27-003': 'No aparece Tlachka ni se otorga una revocación formal de su destierro.',
    'P27-004': 'No aparecen Zippo o Pinky ni se muestra un reencuentro entre ellos.',
    'P28-001': 'La masa actual está compuesta de los cadáveres del camino; no se identifica con la entidad de serpientes de la pirámide.',
    'P28-002': 'Las imágenes de dos elfos no identifican a la serpiente alada ni explican el rito de múltiples cabezas y Nox en el altar.',
    'P28-003': 'No se recupera ni utiliza el collar abandonado dentro de la fruta; la intrusión actual no se atribuye a ese objeto.',
    'P28-004': 'No aparece Citlali ni se explica lo que protegían Bonny y Molly. El deseo de sacar a los elfos no demuestra equivalencia con ese secreto.',
    'P28-005': 'No aparecen los superiores de Aurora ni se amplía el acuerdo de Molly y Bonny.',
    'P29-001': 'Chopito y Tentacol combaten, pero no aportan novedades sobre los Profundos, el dios del altar, el kraken o los desaparecidos.',
    'P29-002': 'No se conceden branquias ni se fija duración o capacidad de las sirenas para hacerlo.',
    'P29-003': 'No aparecen Ivet o su templo ni se identifica su deidad o la vía para obtener su confianza.',
    'P29-004': 'La mención comparativa de Coyote no amplía su historia familiar o el sacrificio aludido por Maris.',
    'P29-005': 'Los cuerpos usados por las raíces no se identifican como restos de Aerendriel ni explican su deterioro o destino.',
    'P30-001': 'El veneno del combate actual no informa del remedio de Parroter o de la evolución de Eromov.',
    'P30-002': 'No se identifica al envenenador de Eromov ni a sus visitantes. La animación del bosque no las vincula con la Hoja Caída.',
    'P30-003': 'No se visita la prisión ni se identifica ningún muerto como un cautivo de aquella reja.',
    'P30-004': 'No aparece Naór ni se reconstruye la formulación del encargo de Eromov.',
    'P30-005': 'Se confirma que Tesara oye la misma voz que antes y se observa movimiento de cadáveres por raíces, pero no se establece alianza o jerarquía entre el dragón, los sacerdotes o la Hoja Caída.',
}
assert len(COTEJO_RAZONES) == len(ASIGNADAS) == 95
assert set(COTEJO_RAZONES) == {x['id'] for x in ASIGNADAS}
COTEJO = []
for pregunta in ASIGNADAS:
    COTEJO.append({
        'pregunta_id': pregunta['id'], 'sha256_pregunta': pregunta['sha256_pregunta'],
        'pregunta': pregunta['pregunta'], 'lectura_completa': True,
        'estado_anterior': pregunta['estado'], 'estado_propuesto': pregunta['estado'],
        'resultado_bloque': 'sin_novedad_en_el_bloque',
        'respuesta_bloque': COTEJO_RAZONES[pregunta['id']],
        'referencias': refs(206, 217, 218, 226) if pregunta['id'] == 'P30-005' else [],
        'pendiente': pregunta['pendiente'],
        'limite': 'Cotejo limitado a 00:45:29.000–01:34:05.709. El coordinador integra otros bloques y las correcciones de identidad autorizadas.',
    })

ENTREGA = {
    'bloque': 2, 'lectura_completa': True,
    'primer_segmento': SEG[0]['id'], 'ultimo_segmento': SEG[-1]['id'],
    'inicio': SEG[0]['inicio'], 'fin': SEG[-1]['fin'], 'segmentos_leidos': len(SEG),
    'fuente': FUENTE.relative_to(ROOT).as_posix(), 'sha256_fuente': SHA,
    'cobertura_lectura': [
        {'formato': 'bloque_2.md', 'desde_indice': 0, 'hasta_indice': 260, 'lineas_desde': 1, 'lineas_hasta': 522},
        {'formato': 'bloque_2.md', 'desde_indice': 261, 'hasta_indice': 521, 'lineas_desde': 523, 'lineas_hasta': 1044},
        {'formato': 'bloque_2.md', 'desde_indice': 522, 'hasta_indice': 782, 'lineas_desde': 1045, 'lineas_hasta': 1566},
        {'formato': 'bloque_2.md', 'desde_indice': 783, 'hasta_indice': 1027, 'lineas_desde': 1567, 'lineas_hasta': 2055},
        {'formato': 'bloque_2_segmentos.json', 'desde_indice': 0, 'hasta_indice': 259},
        {'formato': 'bloque_2_segmentos.json', 'desde_indice': 260, 'hasta_indice': 519},
        {'formato': 'bloque_2_segmentos.json', 'desde_indice': 520, 'hasta_indice': 779},
        {'formato': 'bloque_2_segmentos.json', 'desde_indice': 780, 'hasta_indice': 1027},
    ],
    'cobertura_preguntas': [{'desde_indice': a, 'hasta_indice': b} for a, b in [(0,19),(20,39),(40,59),(60,79),(80,94)]],
    'etapas': ETAPAS, 'afirmaciones': FACTS, 'historias_entidades': HISTORIAS,
    'misiones': MISIONES, 'preguntas': PREGUNTAS,
    'relaciones': [
        {'origen': TESA, 'destino': FELINO, 'texto': 'Tesara dispara contra los dos adversarios próximos al felino para aliviar la presión sobre él y acaba con uno mediante un crítico.', 'referencias': refs(203, 209)},
        {'origen': 'Patata', 'destino': FELINO, 'texto': 'Patata presta atención al estado del felino durante la pelea y al final le ofrece ayuda y pregunta su nombre. No se certifica todavía una curación concreta.', 'referencias': refs(213, 227, 230)},
        {'origen': 'Chopito', 'destino': 'Tentacol', 'texto': 'El pulpo interpreta el mandato intrusivo como un rescate, lo presenta como plan propio y anima a Tentacol a ejecutarlo; este acaba corriendo a buscar a los elfos.', 'referencias': refs(211, 229)},
        {'origen': DRAGON, 'destino': TESA, 'texto': 'La voz coincide con la experiencia anterior de Tesara; ella reconoce la invasión, busca al responsable y logra seguir su posición por vegetación desplazada, sin verle el cuerpo.', 'referencias': refs(206, 218, 219, 220, 224, 228)},
    ],
    'seguimiento_nuevo': [
        {'tema': 'Mandato y resistencia mental', 'nota': 'Todos reciben una idea ajena y la necesidad de realizarla. Chopito la transforma en supuesto rescate y Tentacol sale a buscar a los elfos; el desenlace necesita bloque 3.', 'referencias': refs(206, 210, 211, 216, 229)},
        {'tema': 'La voz de la experiencia anterior de Tesara', 'nota': 'El director establece coincidencia de voz. Cotejar con las preguntas globales sobre influencia del dragón y el disparo anterior; el recuerdo de Tesara no termina la frase del objetivo de aquel disparo.', 'referencias': refs(218)},
        {'tema': 'Ninguna alianza serpiente demostrada', 'pregunta_id': 'P30-005', 'nota': 'La voz y la animación se producen juntas; no aparece identificación con sacerdotes, Hoja Caída o los superiores serpentinos.', 'referencias': refs(206, 217, 218, 226)},
        {'tema': 'Identidad externa del dragón de Aerendriel', 'pregunta_id': 'P15-006', 'nota': 'El contexto autorizado da Zarynth. Incorporar con su propia fuente externa en la integración; no usar al dragón de este bloque como prueba del compañero de Aerendriel.', 'referencias': []},
    ],
    'cotejo_preguntas_asignadas': COTEJO,
    'dudas_y_conexiones_para_coordinacion': [
        'Mictlan queda confirmado por el coordinador mediante la escena escrita posterior x-1531013198478708756. Este bloque ofrece MD, Mlan, mi clan y Mic; se conservan literalmente en citas y no se atribuyen al bloque los hechos posteriores.',
        'Denominaciones armonizadas con bloque 1: Ruinas de la orilla del lago de Iktan y Cadáveres movidos por raíces de las ruinas del lago. La masa está formada por los mismos cadáveres y se trata como etapa de la ficha colectiva.',
        'Los dos elfos son pálidos y Tesara los llama gemelos; el bloque no pronuncia Eldrath o Tryel en esa orden. Integrar identificación con bloque 1/3 y fuentes autorizadas.',
        'El reconocimiento de la voz por Tesara es explícito. No se pronuncia Clolgedranx; armonizar identidad sin fusionar todos los dragones por parecido.',
        'La frase de Tesara sobre el disparo anterior termina «le disparé al» y no nombra blanco en este bloque. No atribuir ese disparo desde esta sola cita.',
        'La ayuda de Patata al felino queda en intención al corte. Bloque 3 debe resolver curación, cuantía y estado final.',
        'Bloque 3 debe cotejar qué pasa con Tesara delante de la presencia, cuánto dura la intrusión y si Tentacol llega a encontrar o entregar a los elfos.',
    ],
    'exclusiones_editoriales': [
        'La broma de cocina no forma parte de las imágenes mentales.',
        'La broma sobre posesión de Patata no acredita inmunidad.',
        'No se adjudica bola de fuego a la rama ni red eficaz que apresa al dragón.',
        'La mención a visión verdadera no demuestra ese sentido: el director lo rechaza como explicación.',
        'Pausas de Foundry y bromas de hackeo no son hechos de campaña.',
        'Que Chopito los llame rescatables no demuestra que los elfos estén cautivos.',
        'No se fija el resultado de la tirada para recargar tinta, solo el permiso para tirarla.',
    ],
}

for item in FACTS:
    validate_fact(item, FUENTE)
    assert SEG[0]['inicio'] <= item['inicio'] <= item['fin'] <= SEG[-1]['fin']
    assert item['evidencia_cue']['texto'] == item['cita']
source_segments = {x['id']: x for x in parse_vtt(FUENTE)}
for segment in SEG:
    assert source_segments[segment['id']] == {k: segment[k] for k in ('id', 'inicio', 'fin', 'texto_original')}
for item in FACTS:
    cue = item['evidencia_cue']
    expected = source_segments[cue['id']]
    assert (cue['inicio'], cue['fin'], cue['texto']) == (expected['inicio'], expected['fin'], expected['texto_original'])
all_ids = {x['id'] for x in FACTS}
assert len(all_ids) == len(FACTS) == 30
for stage in ETAPAS:
    assert set(stage['referencias']) <= all_ids
for story in HISTORIAS:
    for stage in story['etapas']:
        assert set(stage['referencias']) <= all_ids

(BASE / 'entrega_2.json').write_text(json.dumps(ENTREGA, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Entrega 2 validada: {len(FACTS)} afirmaciones, {len(ETAPAS)} etapas, {len(HISTORIAS)} historias y {len(COTEJO)} cotejos; SHA verificado.')
