"""Fichas de lectura íntegra del bloque segundo del capítulo 43."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import validate_fact, write_json, seconds

rows = json.loads((ROOT/'borradores/43/bloque_2_segmentos.json').read_text(encoding='utf-8'))
source = ROOT/'xoltacan_subtitulos/subtitulos/43 - tSdmoZCWEZQ.es-orig.vtt'
facts = []


def fact(number, title, start, end, quote_time, text, entities, limitation='', kind='hecho_confirmado'):
    cue = next(s for s in rows if s['inicio'].startswith(quote_time))
    item = {'id':f'43-{number:03d}','titulo':title,'tipo':kind,'afirmacion':text,
            'inicio':start,'fin':end,'cita':cue['texto_original'],
            'evidencia_cue':{'inicio':cue['inicio'],'fin':cue['fin'],'texto':cue['texto_original']},
            'entidades':entities,'ambito':'batalla terrestre de la jungla del Garfio','conocedores':[],
            'conocimiento_personaje':'desconocido',
            'nota_conocimiento':'Acceso de Madame Oghma sin establecer en este pasaje.',
            'confianza':'lectura de subtítulos; audio no cotejado','limitacion':limitation}
    validate_fact(item,source)
    facts.append(item)


fact(101,'Erandy invoca al Sol y prende un batallón','00:41:56.520','00:45:38.479','00:43:51.559',
     'Erandy canaliza fuego por manos y brazos, con los ojos dorados, mientras invoca al Señor Sol y reclama castigo para quienes subyugan a los débiles. Su bola de fuego explota entre los marines: algunos salen despedidos y otros corren ardiendo. Los piratas, antes desmotivados, se animan y cargan; sus gritos a favor del saqueo y la esclavitud no reproducen la justificación de la escudera. Molly comenta a Eleanor que la pequeña esconde muchas cosas, carga su pistola y avanza.',
     ['Erandy','Eleanor','Molly','Marina'],
     'La invocación y el aspecto solar forman parte de la interpretación de Erandy; no demuestran por sí solos posesión divina. La reacción pirata no implica que compartan su defensa de los inocentes.')
fact(102,'Citlali y Lunaria ven formarse una tormenta sobre el mar','00:45:41.480','00:47:48.719','00:46:46.440',
     'Citlali y Lunaria avanzan hacia Shiaru por la jungla, tan deprisa como permite la forma de oso de Lunaria. Llevan a la cría atada y arrastrada detrás. Oyen ruidos atronadores y Citlali, situada más alta, distingue al este grandes nubes negras sobre el mar que empiezan a formar una tormenta. Anima a Lunaria a acelerar mientras esta da tirones a la cuerda de la cría.',
     ['Citlali','Lunaria','Etley','Shiaru'],
     'Los comentarios sobre enseñar a volar a la cría son bromas; no acreditan que vuele. La observación de Citlali no identifica por sí sola a quien provoca la tormenta.')
fact(103,'La tormenta de una reina pirata se ve desde la lucha terrestre','00:48:18.839','00:49:22.039','00:48:47.720',
     'Durante el combate terrestre cae una lluvia fina y se ven enormes nubes formándose sobre el mar. El director las atribuye al poder de una de las reinas piratas. Los mandos de la Marina insisten en no rendirse y ordenan disparar los cañones.',
     ['Marina','El Garfio'],
     'Este intervalo no nombra a la reina. La atribución a una reina pirata no convierte todos los sucesos del capítulo 42 en anteriores a esta escena.',
     'explicacion_director')
fact(104,'La artillería alcanza a Erandy, Molly y Eleanor','00:49:27.520','00:51:03.439','00:50:35.079',
     'Los cañones disparan sobre los piratas. Erandy recibe metralla, resuelta con quince puntos de daño; Molly también resulta alcanzada. Eleanor se protege detrás del escudo cuando una bala cae frente a ella, pero la fuerza la empuja hacia atrás y recibe treinta y tres puntos de daño.',
     ['Erandy','Molly','Eleanor','Marina','Escudo de Eleanor'],
     'El escudo reduce o contiene parte del impacto descrito, pero no evita el daño. No se especifica aquí la gravedad total de las heridas de Molly.')
fact(105,'Otra bola de fuego destroza tropas, caballos y artillería','00:51:32.559','00:53:59.439','00:53:17.799',
     'Erandy apunta una nueva bola de fuego hacia los batallones y sus cañones. La explosión lanza marines y rifles por los aires, arroja piezas de cañón a la jungla y quema caballos de los mandos, haciendo caer al menos a un general. El director aclara que las fichas de la escena representan pelotones y que las tropas siguen llegando.',
     ['Erandy','Marina','El Garfio'],
     'Los puntos de vida restaurados en las fichas representan el desarrollo de los pelotones y no resurrecciones literales. No se confirma la muerte de todos los generales o la destrucción de toda la artillería.')
fact(106,'Molly continúa el avance con los piratas','00:54:01.680','00:54:33.399','00:54:17.480',
     'Molly sigue avanzando, dispara y trata de proteger a quienes marchan con ella. Los piratas la acompañan y disparan contra los marines. Durante el avance muere algún perro de combate.',
     ['Molly','Marina'],
     'El reconocimiento dice primero que Molly dispara a piratas y después que combate con ellos contra marines; se conserva el avance y apoyo, sin convertir la frase contradictoria en un ataque deliberado contra sus aliados.')
fact(107,'Eleanor deja el escudo como cobertura para su escudera','00:54:33.400','00:55:37.719','00:55:13.240',
     'Eleanor clava su escudo delante de Erandy para proporcionarle cobertura y corre al frente sin él. Aclara que no se lleva a la escudera: deja el escudo vertical, como una torre. Molly la ve sin escudo, sonríe y continúa cargando a su lado.',
     ['Eleanor','Erandy','Molly','Escudo de Eleanor'],
     'Dejar el escudo en retaguardia es una decisión de combate; no se muestra aquí que Eleanor lo pierda definitivamente.')
fact(108,'Lunaria arroja a Etley contra los marines','00:55:42.480','00:58:59.118','00:58:15.880',
     'Las trampas de la jungla saltan al paso de quienes llegan: se disparan dardos y se activan mecanismos con ganchos. Lunaria, en forma de oso, lanza al grupo enemigo la cría que lleva atada. Citlali acompaña el lanzamiento con un silbido de ataque. Etley agita las alas, pero no consigue volar: cae sobre los marines y abre un hueco entre varios pelotones.',
     ['Lunaria','Citlali','Etley','Marina','El Garfio'],
     'La cría se identifica por el cuidado de Citlali y el nombre oído como Echil/Etil; una mención aislada parecida a Erandy al caer no cambia su identidad. No se demuestra vuelo autónomo ni se toma el pentakill como recuento exacto.')
fact(109,'Los golpes masivos hacen flaquear la formación','00:59:01.520','00:59:56.038','00:59:34.720',
     'Tras las bolas de fuego y la caída de la cría, varios fusileros abandonan su posición y retroceden. El director describe que la formación empieza a flaquear por la devastación de los ataques masivos, un cambio especialmente perceptible para Eleanor por su experiencia con ejércitos.',
     ['Eleanor','Erandy','Etley','Marina'],
     'La formación debilitada no equivale todavía a la rendición o derrota definitiva de toda la Marina.')
fact(110,'Citlali entra con el arco y después con sus chanclas','01:00:00.480','01:03:02.598','01:00:48.359',
     'Citlali aparece sobre el oso con el arco preparado y dispara una flecha que se clava en un marine y casi lo derriba. Harta y deseosa de ver a Nox, se dispone a bajar y lanzarse al cuerpo a cuerpo. Se describe más joven y rápida que al comienzo de sus aventuras y corre hacia la Marina para repartir golpes con sus chanclas.',
     ['Citlali','Lunaria','Marina','Nox'],
     'El deseo de ver a Nox no implica que conozca su situación durante la batalla naval. El rejuvenecimiento comparado no fija edad, duración o causa de ese estado.')
fact(111,'Erandy se entrega al trance solar y dispersa a más mandos','01:03:02.599','01:07:07.759','01:06:24.640',
     'La jugadora explica que Erandy, normalmente consciente y controlada, está ahora en un trance abrazado por el Sol: no ha advertido el escudo, el lanzamiento de la cría ni el resto de la escena. Con voz profunda reclama que ardan quienes quieren purgar la tierra y lanza otra bola de fuego. El director acepta la descripción: una pequeña esfera se forma junto a los generales y explota, los lanza heridos a la jungla y espanta los caballos. Los marines empiezan a separarse por los caminos mientras Citlali irrumpe entre ellos.',
     ['Erandy','Citlali','Marina','Escudo de Eleanor'],
     'El trance es interpretación aceptada en mesa, sin identidad divina separada ni diagnóstico. Los generales descritos como medio muertos no se registran todos como fallecidos.')
fact(112,'Lunaria utiliza un cañón como garrote y sale impulsada','01:07:07.760','01:09:48.000','01:08:42.560',
     'Lunaria ruge y arremete en forma de oso hacia un cañón. Lo toma para barrer a los marines a golpes. En uno de los movimientos el arma queda dirigida hacia abajo y dispara o estalla: le causa nueve puntos de daño y la impulsa al aire. El director describe después que cae sobre un montón de marines. Lunaria ruge hacia Etley como si mostrase cómo volar, sin convertir ese impulso en vuelo propio.',
     ['Lunaria','Etley','Marina','Cañón tomado por Lunaria'],
     'La propulsión depende del cañón. La escena usa explota y disparar sin establecer que el arma quede destruida; vuelve a utilizarla después.')
fact(113,'Eleanor marca la retaguardia y llama a cargar','01:09:48.000','01:12:11.000','01:10:33.120',
     'Molly y otros piratas alcanzan a Citlali y al oso. Al ver que Erandy se ha acercado, Eleanor clava el estandarte y le ordena no avanzar más: su lugar es la retaguardia. Reconoce a Lunaria cuando el oso cae ante ella y, viendo rota la formación enemiga, llama a los demás a cargar. Sin el escudo, combate con su espada entre los marines y ataca a un perro.',
     ['Eleanor','Erandy','Lunaria','Molly','Citlali','Marina','Estandarte de Eleanor','Espada de Eleanor'],
     'La orden del estandarte no demuestra que Erandy la obedezca. La caída del oso en esta escena no acredita que se trate de otro animal.')
fact(114,'Eleanor utiliza el perro caído para montar sobre Lunaria','01:12:11.000','01:13:34.759','01:12:31.840',
     'Eleanor aprovecha el cuerpo del perro cuando cae para saltar y subirse sobre Lunaria. La jugadora de Lunaria acepta llevarla. Eleanor anuncia que se transformará sobre el oso para infundir más miedo. Los generales de la Marina intentan recuperar la formación y ordenan acabar con el oso y con la señora que avanza golpeando con chanclas.',
     ['Eleanor','Lunaria','Citlali','Marina'],
     'Este intervalo anuncia la transformación; su apariencia concreta se describe después. Los gritos de los generales no confirman que recuperen el control.')
fact(115,'El toque de Citlali cierra sus heridas y rejuvenece su piel','01:13:34.760','01:15:59.919','01:14:56.080',
     'Citlali sigue golpeando con las chanclas como si fueran dagas hasta llegar ante un hombre y tocarle el cuello con un toque frío, descrito como de muerte. Los personajes cercanos ven que su piel arrugada se tensa y parece rejuvenecer durante unos segundos. La sangre de las heridas que había recibido deja de brotar y el director la describe totalmente curada. Continúa avanzando y abatiendo miembros de los pelotones.',
     ['Citlali','Lunaria','Eleanor','Molly','Marina'],
     'El pasaje relaciona el toque con el cambio visible y la curación; no identifica por nombre el conjuro, demuestra una juventud permanente ni explica toda su longevidad.')
fact(116,'Erandy ignora la orden y lanza rayos abrasadores','01:15:59.920','01:18:25.198','01:18:04.239',
     'Erandy no escucha la orden de Eleanor y se desplaza hacia otro general, invocando la defensa de la Madre Tierra y del Señor Sol. Lanza los tres rayos de un conjuro reconocido en mesa como scorching ray: algunos fallan y otros chamuscan y abaten marines. Sigue descrita fuera de sí. Etley permanece en medio de la batalla, entre el fuego, pese a la intención previa de Citlali de esconderlo.',
     ['Erandy','Eleanor','Etley','Citlali','Marina'],
     'No se confirma que todos los rayos acierten al general escogido. Las bromas sobre pollo asado no son una muerte documentada de Etley.')
fact(117,'Un segundo disparo lanza a Lunaria y Eleanor','01:18:25.199','01:19:43.799','01:19:28.520',
     'Lunaria golpea el cañón contra el suelo buscando hacerlo disparar otra vez. Tras un primer golpe que lo mueve, repite y consigue una nueva detonación que la lanza al aire con Eleanor montada encima. El director deja a ambas suspendidas para resolver la caída en su turno posterior.',
     ['Lunaria','Eleanor','Cañón tomado por Lunaria'],
     'No es una capacidad de vuelo autónoma. La descripción posterior dice los tres al contar la escena, sin identificar aquí a un tercer jinete o pasajero.')
fact(118,'Eleanor adopta la forma de ángel caído','01:19:43.800','01:20:48.238','01:19:57.280',
     'Eleanor concreta la transformación anunciada: la llama forma de ángel caído. Su piel se vuelve grisácea y muy pálida, aparecen alas rotas a su espalda, todo el ojo queda negro y la espada pasa de tener letras brillantes a resplandecer entera de color morado. Permanece sobre Lunaria en el aire, a la espera de la caída.',
     ['Eleanor','Lunaria','Espada de Eleanor'],
     'La forma se nombra en mesa; no fija por sí sola especie, ascendencia o afiliación a un ser celestial concreto. Las alas rotas no acreditan que sostenga el vuelo.')
fact(119,'La combatiente que acompaña al grupo protege a Citlali','01:20:48.239','01:21:50.119','01:21:26.600',
     'La combatiente que venía avanzando con los piratas observa a Eleanor sobre el oso y sigue luchando. Al pasar junto a Citlali intercepta un golpe de un marine y le advierte que debería estar en otro lugar porque corre peligro. Citlali responde «Yo soy el peligro» y continúa combatiendo. Por continuidad se conserva la escena junto a Molly.',
     ['Molly','Citlali','Eleanor','Lunaria','Marina'],
     'El director dice Bonnie al inicio y después una variante oída como Morí; el bloque había seguido a Molly en el mismo frente. La atribución se conserva como contextual y no se afirma una llegada inequívoca de Bonnie a tierra.')
fact(120,'Eleanor propone imbuir al oso con la energía de smite','01:21:50.120','01:22:34.550','01:22:11.520',
     'Todavía en el aire sobre Lunaria y en su forma de ángel caído, Eleanor propone imbuir al oso con la energía de smite durante la caída, aunque tenga que gastar sus espacios de conjuro. El director acepta resolverlo como un smite del nivel máximo disponible y empieza a concretar los dados correspondientes al segundo nivel.',
     ['Eleanor','Lunaria'],
     'El bloque termina durante la preparación mecánica: no se adelanta el impacto, el daño ni el resultado de la caída.',
     'explicacion_director')


def stage(title,text,*refs):
    return {'titulo':title,'texto':text,'referencias':list(refs)}


stages = [
    stage('Fuego solar contra los pelotones',
          'Erandy reúne fuego en manos y brazos, con los ojos dorados, e invoca al Señor Sol para proteger a los débiles. La bola de fuego explota entre los marines. Su clamor anima a unos piratas que cargan con gritos de saqueo y esclavitud, ajenos a la justificación de la escudera. Molly descubre con sorpresa la fuerza de la pequeña y avanza junto a Eleanor. Desde la jungla, Citlali y Lunaria, todavía en forma de oso, oyen los estruendos y ven una tormenta creciendo sobre el mar. En el frente cae una lluvia fina antes de que los cañones respondan: la metralla alcanza a Erandy y Molly, y una bala empuja a Eleanor incluso detrás del escudo. Otra bola de fuego de Erandy destroza hombres, caballos y piezas de artillería. Eleanor deja el escudo clavado para cubrirla y corre al frente.',
          '43-101','43-102','43-103','43-104','43-105','43-106','43-107'),
    stage('Una cría sobre la formación',
          'Las trampas de la jungla se disparan cuando llega el oso. Lunaria arroja a Etley hacia los enemigos y Citlali lanza un silbido de ataque. La cría bate las alas sin aprender a volar: cae sobre los marines y abre un hueco entre varios pelotones. Tras las explosiones y ese impacto, la formación empieza a ceder. Citlali entra con el arco, hiere a un marine y después baja del oso para correr con sus chanclas preparadas. Quiere ver a Nox, pero primero atraviesa a golpes el frente terrestre. Erandy apenas percibe lo que ocurre a su alrededor: su jugadora la describe entregada a un trance solar. Otra esfera de fuego estalla entre los generales, los arroja heridos a la jungla y espanta a sus caballos. La llegada de Citlali aumenta el desorden.',
          '43-108','43-109','43-110','43-111'),
    stage('Un oso, un cañón y una retaguardia desobedecida',
          'Lunaria toma un cañón y lo utiliza como garrote para barrer marines. Un disparo hacia el suelo la hiere y la impulsa al aire; después cae sobre los soldados. Cuando Molly y otros piratas alcanzan la lucha, Eleanor clava el estandarte para marcar el límite de la retaguardia y ordena a Erandy no avanzar más. Ella carga con la espada y aprovecha el cuerpo de un perro abatido para saltar sobre Lunaria. Los generales gritan que recuperen la formación y detengan al oso y a Citlali. Mamá sigue repartiendo golpes: toca el cuello de un enemigo y su piel parece rejuvenecer unos segundos, mientras sus heridas dejan de sangrar. Erandy no escucha la orden. Avanza por su cuenta y lanza rayos abrasadores, algunos fallidos y otros capaces de abatir marines.',
          '43-112','43-113','43-114','43-115','43-116'),
    stage('El ángel caído sale despedido',
          'Lunaria intenta repetir su inesperado impulso golpeando el cañón contra el suelo. A la segunda sacudida consigue dispararlo y vuelve a salir despedida, ahora con Eleanor a lomos. La guerrera adopta la forma que llama ángel caído: piel gris y pálida, alas rotas, ojos enteramente negros y una espada que resplandece de morado. Mientras ambas esperan la caída, la combatiente que acompaña a los piratas protege a Citlali de un golpe y le advierte del peligro; la anciana replica que el peligro es ella. Eleanor propone aprovechar el descenso para imbuir al oso con la energía de smite. El director acepta resolver el gasto al nivel máximo disponible y concreta los dados. El impacto todavía no se muestra en este tramo.',
          '43-117','43-118','43-119','43-120')
]

histories=[]


def history(name,kind,title,text,refs,new=False,description='',note=''):
    histories.append({'nombre':name,'tipo':kind,'nueva':new,'descripcion':description,'nota':note,
                      'etapas':[stage(title,text,*refs)]})


history('Erandy','personaje','El trance del fuego solar',
        'Erandy invoca al Señor Sol y utiliza sucesivas bolas de fuego para quebrar los pelotones, dañar su artillería y dispersar a los mandos de la Marina. Aunque la metralla la hiere, sigue avanzando. Su jugadora la describe en trance, ajena al escudo protector que Eleanor deja y a lo que ocurre con la cría y el oso. No escucha la orden de permanecer en retaguardia y continúa lanzando rayos abrasadores. La descripción religiosa expresa su vivencia del poder, sin acreditar una posesión divina.',
        ['43-101','43-104','43-105','43-107','43-111','43-113','43-116'])
history('Eleanor','personaje','Del escudo protector al ángel caído',
        'Eleanor resiste un cañonazo con el escudo y después lo clava delante de Erandy para protegerla. Avanza sin él, marca la retaguardia con el estandarte y llama a cargar cuando la formación enemiga flaquea. Utiliza un perro caído para saltar a lomos de Lunaria y adopta su forma de ángel caído, con alas rotas, piel pálida, ojos negros y espada violeta. Un segundo disparo del cañón las lanza al aire y propone imbuir al oso con smite para aprovechar la caída.',
        ['43-104','43-107','43-113','43-114','43-117','43-118','43-120'])
history('Lunaria','personaje','Artillería en forma de oso',
        'Lunaria atraviesa la jungla en forma de oso llevando a Citlali y arrastrando a Etley. Al llegar al frente arroja la cría contra los pelotones y después toma un cañón para golpear a los marines. La detonación del arma hacia el suelo la hiere y la impulsa antes de caer sobre los soldados. Acepta que Eleanor la monte y repite la maniobra del cañón, saliendo ambas despedidas. El espectáculo depende del disparo, sin convertir su forma animal en una criatura capaz de volar.',
        ['43-102','43-108','43-112','43-114','43-117','43-120'])
history('Citlali','personaje','El peligro llega a la jungla',
        'Citlali anima a Lunaria a acelerar cuando oye la batalla y ve la tormenta del mar. Acompaña con un silbido de ataque el lanzamiento de Etley, dispara su arco y baja para combatir con las chanclas. Expresa que quiere ver a Nox, sin conocer por ello su situación en la batalla naval. Su toque frío a un enemigo coincide con una breve tersura juvenil de su piel y el cierre de sus heridas. Cuando una aliada le advierte del peligro, responde que el peligro es ella y sigue luchando.',
        ['43-102','43-108','43-110','43-115','43-119'])
history('Etley','personaje','La cría entra en la batalla',
        'Etley llega arrastrado y atado tras el oso de Lunaria. Esta lo arroja hacia los marines y Citlali lo anima con un silbido de ataque. Aunque agita las alas, no vuela: su caída golpea a varios pelotones y abre un hueco en la formación. Permanece después en el centro de la lucha, entre bolas y rayos de fuego, pese a la intención previa de Citlali de esconderlo. Las bromas sobre cocinarlo no documentan su muerte.',
        ['43-102','43-108','43-109','43-112','43-116'])
history('Molly','personaje','Junto a la carga terrestre',
        'Molly observa la fuerza de Erandy y carga junto a Eleanor y los piratas. La metralla la alcanza, pero continúa disparando y protegiendo a sus compañeros. Más tarde se une al frente de Citlali y Lunaria. El pasaje en que una aliada intercepta un golpe contra Citlali y la advierte del peligro se conserva por continuidad junto a Molly, aunque el reconocimiento alterna Bonnie y Morí y exige cautela en la atribución.',
        ['43-101','43-104','43-106','43-107','43-113','43-119'])
history('Marina','faccion','La formación terrestre se descompone',
        'La Marina intenta mantener sus pelotones y responde con cañones que hieren a los atacantes. Las bolas de fuego destruyen artillería y caballos, mientras el lanzamiento de Etley abre un hueco y el avance de Citlali, Lunaria y Eleanor agrava el caos. Varios soldados retroceden o se separan por los caminos y los mandos gritan para recomponer la formación. La resistencia continúa y el bloque no muestra todavía el desenlace del frente.',
        ['43-103','43-104','43-105','43-108','43-109','43-111','43-113','43-114','43-116'])
history('El Garfio','lugar','Fuego y artillería entre los árboles',
        'La jungla del Garfio reúne el frente terrestre y los accesos con dardos y mecanismos de trampa. Los cañonazos y las bolas de fuego arrojan metralla, caballos y piezas de artillería entre los árboles. Al este se ve sobre el mar la tormenta de una reina pirata, mientras la formación de la Marina pierde cohesión en los caminos. Lunaria y Citlali irrumpen desde la maleza con Etley y se unen a Eleanor, Erandy y Molly.',
        ['43-102','43-103','43-105','43-108','43-111','43-113'])
history('Escudo de Eleanor','objeto','Una torre para proteger a Erandy',
        'El escudo protege parcialmente a Eleanor cuando una bala de cañón cae delante, aunque la fuerza la empuja y la hiere. En lugar de llevarlo al avance, lo clava vertical delante de Erandy para que su escudera disponga de cobertura. Eleanor continúa luchando sin él y Erandy, en trance, no repara en el gesto. El tramo no muestra una pérdida definitiva ni el regreso a recogerlo.',
        ['43-104','43-107','43-111','43-113'],True,
        'Escudo de Eleanor, empleado para contener artillería y como cobertura fija de Erandy.',
        'Entrada descriptiva sin nombre propio o poder mágico atribuido. No se confunde con los escudos de Ayoto.')
history('Estandarte de Eleanor','objeto','El límite de la retaguardia',
        'Eleanor clava el estandarte cuando Erandy se acerca a la zona del enfrentamiento y lo utiliza como referencia para ordenarle que no avance más. La escudera, absorta en el trance solar, no escucha la orden y se mueve hacia otro general. El objeto documenta la instrucción táctica, sin aportar aquí emblema, inscripción o pertenencia institucional nueva.',
        ['43-113','43-116'],True,
        'Estandarte que Eleanor utiliza para marcar dónde debe permanecer su escudera.',
        'No se infiere un escudo heráldico, reino representado o relación de identidad con otras banderas.')
history('Espada de Eleanor','objeto','La luz cambia con su portadora',
        'Eleanor combate con la espada tras dejar su escudo y abrirse paso entre los marines. Cuando adopta la forma de ángel caído sobre Lunaria, describe que el brillo deja de limitarse a las letras del arma: la espada entera resplandece de color morado. La escena vincula el cambio visible a la transformación, sin revelar nombre propio, inscripción completa o procedencia del arma.',
        ['43-113','43-118'],True,
        'Espada de Eleanor, cuyas letras brillan y que resplandece entera de morado en la forma de ángel caído.',
        'No se fija nombre propio ni relación con otras espadas por el color o el brillo.')
history('Cañón tomado por Lunaria','objeto','De garrote a propulsor',
        'Lunaria toma uno de los cañones del frente y lo utiliza en forma de oso para barrer a los marines. Un disparo hacia abajo la hiere y la impulsa al aire antes de caer sobre los enemigos. Más tarde, con Eleanor a lomos, golpea el arma contra el suelo hasta provocar otro disparo que las vuelve a lanzar. El objeto pasa de artillería enemiga a herramienta improvisada de combate y desplazamiento.',
        ['43-112','43-117','43-120'],True,
        'Pieza de artillería del frente que Lunaria usa para golpear y salir impulsada con sus disparos.',
        'La designación describe un uso temporal; no afirma propiedad permanente, encantamiento o vuelo autónomo.')

equipment_without_dossier={'Escudo de Eleanor','Espada de Eleanor'}
for item in facts:
    item['entidades']=[name for name in item['entidades'] if name not in equipment_without_dossier]
histories=[item for item in histories if item['nombre'] not in equipment_without_dossier]

delivery={'bloque':2,'lectura_completa':True,'primer_segmento':'c001843','ultimo_segmento':'c003683',
          'etapas':stages,'afirmaciones':facts,
          'misiones':[
              'Quebrar el frente terrestre de la Marina: las bolas de fuego de Erandy, la caída de Etley y las acometidas del grupo deshacen parte de su formación; el tramo no muestra su derrota definitiva (43-101, 43-105, 43-108–43-109, 43-111–43-118).',
              'Mantener a Erandy a cubierto: Eleanor deja su escudo para protegerla y marca con un estandarte el límite de la retaguardia, pero la escudera no escucha y sigue avanzando en trance (43-107, 43-111, 43-113, 43-116).',
              'Llegar a Shiaru y encontrar a Nox: Citlali impulsa el paso de Lunaria y expresa que quiere verlo, pero se suma primero a la lucha terrestre y no lo encuentra en este bloque (43-102, 43-110).',
              'Aprovechar el cañón tomado: Lunaria lo usa como garrote y propulsor, Eleanor sube sobre ella y prepara un smite para el descenso; el impacto se resolverá después del corte (43-112, 43-114, 43-117–43-120).'
          ],
          'preguntas':[
              '¿Cómo se explica el trance solar de Erandy y qué consecuencias tendrá ignorar la retaguardia ordenada por Eleanor? Aquí sigue actuando ajena a la protección y a las órdenes (43-107, 43-111, 43-113, 43-116).',
              '¿Qué causa y duración tiene el rejuvenecimiento visible de Citlali durante el toque frío? El cambio dura unos segundos y coincide con el cierre de sus heridas (43-115).',
              '¿Qué resultado tendrá la caída de Lunaria y Eleanor tras preparar el smite? Este corte termina durante la concreción de los dados (43-117–43-120).'
          ],
          'contradicciones':[
              'Las invocaciones de Erandy contra la subyugación no se convierten en una postura compartida por los piratas: estos se animan con gritos de saqueo y esclavitud (43-101).',
              'Los pelotones vuelven a aparecer o recuperan puntos en la representación de mesa; el director explica que las fichas agrupan tropas y no son resurrecciones literales (43-105).',
              'Etley bate las alas pero cae; la propulsión de Lunaria proviene de disparar el cañón. No se documenta que alguno de los dos haya adquirido vuelo autónomo (43-108, 43-112, 43-117).',
              'La explicación de Molly dispara primero a piratas y después combate con ellos contra marines; la primera formulación no basta para afirmar traición o fuego amigo deliberado (43-106).',
              'Eleanor deja el escudo para dar cobertura y ordena a Erandy quedarse tras el estandarte, pero Erandy no percibe lo primero ni escucha lo segundo (43-107, 43-111, 43-113, 43-116).',
              'El director alterna Bonnie y Morí al describir a la combatiente junto a Citlali. La continuidad del frente apunta a Molly, pero no se afirma que Bonnie haya desembarcado inequívocamente en esa escena (43-119).',
              'La cifra los tres al salir despedidos no identifica a un tercer jinete: solo se han situado expresamente a Lunaria y Eleanor sobre el cañón (43-117–43-118).',
              'La advertencia de cronología impide usar la búsqueda de Nox por Citlali como conocimiento de su despedida en el capítulo 42. Este bloque no determina por sí solo su posición exacta respecto de todos los acontecimientos navales (43-102–43-103, 43-110).'
          ],
          'nombres_dudosos':[
              'Andy, Erandy y variantes del nombre de la pequeña remiten a la escudera de Eleanor. El sol invocado no crea una persona nueva ni la identifica con Ayoto (43-101, 43-105, 43-111, 43-116).',
              'Eleanor, Eliano y Elanor remiten a la guerrera. La forma de ángel caído es su transformación declarada y no una persona aparte (43-107, 43-113–43-114, 43-118).',
              'Mamá es Citlali; Luna en forma de oso es Lunaria. Echil, Etil y el pollo o cría de dinosaurio son Etley por continuidad de los cuidados y el silbido (43-102, 43-108, 43-110, 43-112).',
              'Mole, Molly, Moni y Morí corresponden contextualmente a Molly. La aparición aislada de Bonnie en el mismo frente se conserva como duda de atribución y no identifica a otra participante con certeza (43-101, 43-106–43-107, 43-113, 43-119).',
              'El estandarte de Eleanor y el cañón tomado por Lunaria usan nombres descriptivos. El escudo y la espada se conservan como equipo descrito en sus acciones, sin inventar nombres propios, procedencias ni poderes permanentes (43-104, 43-107, 43-112–43-113, 43-117–43-118).'
          ],'historias_entidades':histories}

assert len(facts)==20
assert all(seconds(f['inicio'])<=seconds(f['evidencia_cue']['inicio'])<=seconds(f['fin']) for f in facts)
assert all(f['cita'] in f['evidencia_cue']['texto'] for f in facts)
write_json(ROOT/'borradores/43/entrega_2.json',delivery)
print(f'Entrega 2: {len(facts)} hechos validados; {len(stages)} etapas; {len(histories)} historias propuestas; '+str(sum(len(s['texto'].split()) for s in stages))+' palabras de relato.')
