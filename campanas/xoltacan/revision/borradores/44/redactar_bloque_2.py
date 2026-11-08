"""Entrega editorial tras leer los 839 segmentos del bloque segundo."""
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'scripts'))
from construir import validate_fact,write_json,seconds

rows=json.loads((ROOT / 'campanas/xoltacan/revision/borradores/44/bloque_2_segmentos.json').read_text(encoding='utf-8'))
source=ROOT / 'campanas/xoltacan/fuentes/44 - KAfKPeZImT4.es-orig.vtt'
facts=[]


def fact(number,title,start,end,quote_time,text,entities,limitation='',kind='hecho_confirmado'):
    cue=next(s for s in rows if s['inicio'].startswith(quote_time))
    item={'id':f'44-{number:03d}','titulo':title,'tipo':kind,'afirmacion':text,
          'inicio':start,'fin':end,'cita':cue['texto_original'],
          'evidencia_cue':{'inicio':cue['inicio'],'fin':cue['fin'],'texto':cue['texto_original']},
          'entidades':entities,'ambito':'obtención de las espinas para la cura de Eromov',
          'conocedores':[],'conocimiento_personaje':'desconocido',
          'nota_conocimiento':'Acceso de Madame Oghma sin establecer en este pasaje.',
          'confianza':'lectura de subtítulos; audio no cotejado','limitacion':limitation}
    validate_fact(item,source)
    facts.append(item)


fact(101,'Ayoto atrae la atención de la masa de moho','00:39:10.440','00:41:10.959','00:40:20.720',
     'Ayoto corre para dejar espacio a sus compañeros y golpea a la criatura con el escudo de pinchos. Utiliza una maniobra de provocación y el director confirma que pasa a ser el objetivo de la masa. Los golpes siguientes no alcanzan al rival.',
     ['Ayoto','Masa de moho de la cueva'],
     'La provocación se conserva como resolución de la maniobra en combate; no permite atribuir inteligencia, lenguaje o una especie precisa al moho.')
fact(102,'Tlachka extrae huesos humanoides del moho','00:41:10.960','00:42:32.598','00:42:09.520',
     'Tlachka intenta abrir la boca de la criatura para buscar una espina, pero el director aclara que es una masa de moho sin boca propiamente dicha. Introduce la mano y tira del material: extrae restos de huesos que parecen humanoides y se están consumiendo. Dice a Leona que no encuentra lo que buscan y ella decide probar.',
     ['Tlachka','Leona','Masa de moho de la cueva'],
     'Los huesos no reciben identidad personal, fecha o procedencia. Buscar una espina en el moho no demuestra que sea el Devorafango del encargo.')
fact(103,'Leona se introduce en la masa para desgarrarla','00:42:32.599','00:44:16.479','00:42:59.720',
     'Leona se enfurece por los golpes recibidos y decide introducirse en la masa para arrancar su contenido desde dentro. El director insiste en que no tiene una boca definida, pero acepta que se lance al interior. Queda retenida y sin visión mientras desgarra trozos del moho con las manos.',
     ['Leona','Masa de moho de la cueva'],
     'La entrada en la masa es voluntaria. El material desgarrado no se registra como las espinas necesarias para el remedio.')
fact(104,'La angustia de Guayacán acompaña sus golpes no letales','00:44:16.480','00:46:05.519','00:45:30.040',
     'Guayacán quiere debilitar a la criatura sin matarla para que Leona pueda arrancar una espina. Declara sus golpes no letales y pretende aturdir al rival si consigue impactar, pero falla los ataques de este turno. Explica que está angustiado al ver a Leona dentro y que esa preocupación lo vuelve torpe.',
     ['Guayacán','Leona','Masa de moho de la cueva'],
     'El propósito de dejar inconsciente al rival no significa que lo consiga en este turno. No se atribuye a Leona una relación familiar o romántica nueva por la angustia de Guayacán.')
fact(105,'La criatura hiere desde dentro y Ayoto replica a un fallo','00:46:05.520','00:48:27.000','00:46:54.720',
     'Leona resiste el daño que recibe en el interior de la masa. El rival intenta golpear a Ayoto y falla el primer ataque; el goliat aprovecha para responder con una réplica que impacta. La criatura efectúa después otro ataque contra él.',
     ['Leona','Ayoto','Masa de moho de la cueva'],
     'Las reducciones de daño se discuten en mesa sin describir un nuevo poder narrativo separado. El resultado exacto del segundo ataque no queda verbalmente fijado con la misma claridad.')
fact(106,'Ayoto vuelve a provocar y Tlachka mantiene golpes no letales','00:48:27.000','00:50:20.639','00:49:05.720',
     'Ayoto intenta nuevos golpes y vuelve a aplicar su maniobra de provocación cuando uno alcanza a la masa. El director confirma el fallo de su salvación. Después Tlachka golpea con su macuahuitl y acuerda emplear daño no letal.',
     ['Ayoto','Tlachka','Masa de moho de la cueva'],
     'La intención de evitar la muerte se refiere a los golpes declarados en esta fase; no determina por sí sola el estado final de la criatura.')
fact(107,'Leona sigue arrancando material sin encontrar la espina','00:50:20.640','00:51:43.879','00:50:49.319',
     'Leona continúa dentro de la masa y vuelve a arrancar trozos con las manos. Causa daño al desgarrarla y sigue intentando llevarse la espina que busca, sin que en esta acción se describa su extracción.',
     ['Leona','Masa de moho de la cueva'],
     'Un efecto de carta provoca aparte cinco puntos de daño a los presentes; la broma sobre picante no se convierte en una causa fisiológica o un acontecimiento nuevo del mundo.')
fact(108,'Guayacán logra aturdir a la masa','00:51:43.880','00:54:29.279','00:52:53.160',
     'Guayacán insiste en golpear de forma no letal y logra aplicar un golpe aturdidor. Con el rival aturdido, sus siguientes golpes se resuelven con ventaja. Leona sigue expuesta al daño del interior, pero la masa no realiza el ataque que iba a dirigir contra Ayoto porque está aturdida.',
     ['Guayacán','Leona','Ayoto','Masa de moho de la cueva'],
     'El aturdimiento no equivale a una muerte ni acredita haber obtenido el ingrediente.')
fact(109,'Ayoto saca a Leona y ocupa su lugar dentro de la masa','00:54:29.280','00:57:52.798','00:57:39.960',
     'Ayoto combate con sus dos escudos y emplea la última carga de uno para rasgar la masa y abrir un hueco. A través de él ve a Leona arrancando material. Utiliza una maniobra para alcanzarla y tirar de ella mientras la harengon desgarra cuanto puede. El director resuelve el intercambio: Leona sale y Ayoto queda dentro.',
     ['Ayoto','Leona','Masa de moho de la cueva'],
     'Las explicaciones de la dote y la maniobra no establecen reglas generales fuera de esta resolución. No se confirma la identidad del material arrancado como ingrediente del antídoto.')
fact(110,'La masa queda moribunda entre restos de huesos','00:57:52.799','01:00:31.239','00:58:50.119',
     'Tlachka continúa atacando y la masa queda a un punto de vida según la resolución del director. Al abrir y apartar el moho salen nuevos restos de huesos que parecían estar siendo consumidos en su interior. Más tarde se corrige el comentario de que está muerta: seguía moribunda al comenzar la siguiente amenaza.',
     ['Tlachka','Ayoto','Masa de moho de la cueva'],
     'El reconocimiento alterna formulaciones de letal y no letal en estos golpes; se conserva el estado explícito de un punto de vida. No se fija aquí su muerte ni la identidad de los restos.')
fact(111,'El Devorafango entra y cubre la sala de ácido','00:59:10.680','01:02:17.558','01:01:31.599',
     'Guayacán oye ruido detrás del grupo. Una criatura enorme entra por la boca de la cueva: está cubierta de barro, tiene ojos grandes y saltones, espinas en la espalda y protuberancias dentadas alrededor de la boca. Escupe una gran descarga que llena de ácido la sala y alcanza también la zona de la masa de moho. Ayoto describe el ácido cayéndole sobre la espalda cuando el moho se abre encima de él y utiliza su resistencia para mitigar el daño.',
     ['Guayacán','Ayoto','Devorafango','Masa de moho de la cueva','Cueva del lago cercano a Cuicapalli'],
     'La identificación con el Devorafango enlaza sus rasgos con el encargo, sin añadir una especie de bestiario. Una reacción de absorción de ácido se declara sin nombre del actor suficientemente claro en ese instante; el arma de Tlachka se describe luego cargada con ese ácido.')
fact(112,'Leona se mete en la boca de la nueva criatura','01:02:17.559','01:03:53.719','01:03:34.880',
     'Leona aprovecha la boca abierta tras la descarga y se introduce en el Devorafango, pese al peligro. Empieza a arrancar desde dentro dientes, cartílagos o lo que puede alcanzar. El director confirma que permanece en su boca mientras desgarra esas estructuras.',
     ['Leona','Devorafango'],
     'Es la segunda criatura, distinta de la masa sin boca de la que Ayoto la había sacado. Entrar voluntariamente no equivale a describir una deglución completa o llegar a un estómago.')
fact(113,'Guayacán bebe una poción antes de volver a atacar','01:03:53.720','01:06:05.118','01:04:10.240',
     'Guayacán se acerca al nuevo rival y utiliza una poción de curación que tenía entre sus pertenencias. En mesa se aclara que las pociones proceden de la recompensa de Discord. Después intenta golpear a la criatura, pero los ataques mostrados en esta acción fallan.',
     ['Guayacán','Devorafango'],
     'La referencia a Discord explica la procedencia de un recurso de juego; no crea una facción o comercio del mundo. No se cuantifica verbalmente la curación obtenida.')
fact(114,'Ayoto sube al lomo y derriba al Devorafango','01:06:05.119','01:09:11.158','01:08:25.480',
     'Ayoto corre hacia el nuevo enemigo, salta con el escudo y consigue subir encima. Lo golpea desde arriba, pero las espinas dorsales se le clavan al contacto. El director aclara que es daño de los pinchazos y no envenenamiento. El goliat se arroja hacia un lado y dirige un golpe a una rodilla para derribarlo; la criatura cae al suelo.',
     ['Ayoto','Devorafango'],
     'No se inventa cómo termina la estancia anterior de Ayoto en el moho: esta acción lo sitúa ya atacando al nuevo rival. El daño de las espinas se distingue del ácido y del veneno que afecta a Eromov.')
fact(115,'Tlachka golpea el vientre desprotegido con ácido en el arma','01:09:11.159','01:10:42.519','01:09:30.400',
     'Tlachka se acerca con el arma descrita como cargada por el escupitajo ácido y ataca al Devorafango derribado. El director precisa que el vientre no tiene las espinas que cubren la espalda. Tlachka encadena golpes y suma el ácido al daño. Los impactos hacen que la criatura se agite y Leona se golpee de un lado a otro dentro de su boca.',
     ['Tlachka','Leona','Devorafango'],
     'El ácido en el arma se conserva como efecto resuelto en esta acción, no como una modificación permanente del arma. La sucesión de ataques no se convierte en varios turnos o personas distintas.')
fact(116,'Un mordisco deja a Guayacán al límite y la cola derriba a Ayoto','01:10:42.520','01:13:10.879','01:12:00.840',
     'El Devorafango se levanta a cuatro patas y empieza a regurgitar, sin expulsar todavía a Leona. Muerde a Guayacán, que queda a un punto de vida tras aplicar la reducción de su furia. Luego golpea a Ayoto con la cola; el goliat falla la salvación de fuerza y cae al suelo.',
     ['Devorafango','Leona','Guayacán','Ayoto'],
     'Guayacán queda gravemente herido pero consciente, sin una muerte representada. La regurgitación no se confunde con una salida de Leona en ese momento.')
fact(117,'Leona arranca una espina recordando a Eromov','01:13:10.880','01:14:33.039','01:14:07.040',
     'Dentro de la boca, Leona clava el hacha para estabilizarse y se esfuerza por arrancar una protuberancia espinosa. Se engancha a una de las muelas descritas por el director. La pieza se resiste, pero el recuerdo de Eromov cuando la encontró de pequeña refuerza su rabia: finalmente consigue arrancar una de las espinas. Desde fuera se oye a la criatura gritar y agitarse.',
     ['Leona','Eromov','Devorafango','Espinas del Devorafango'],
     'La extracción ocurre mientras el animal sigue vivo, conforme al encargo. El recuerdo atribuye a Eromov haberla encontrado de niña, sin fijar adopción legal, parentesco biológico o toda su crianza.')
fact(118,'Guayacán se cura y sujeta al rival por la boca','01:14:33.040','01:16:18.559','01:15:50.000',
     'Muy herido, Guayacán utiliza otra curación sobre sí mismo y decide apoyar la extracción en lugar de seguir fallando golpes. Intenta sujetar al animal por el cuello o la boca y el director resuelve que lo agarra de la boca. Mantiene al Devorafango apresado para ayudar a sus compañeros.',
     ['Guayacán','Leona','Devorafango'],
     'Se declara una curación pero su cantidad no queda verbalmente especificada. Sujetar la boca no asegura que Leona pueda salir: los compañeros aún no conocen bien su situación interior.')
fact(119,'Ayoto dirige sus golpes hacia la cola','01:16:18.560','01:18:34.279','01:18:08.679',
     'Ayoto reanuda sus ataques contra el Devorafango. Tras resolver los impactos, precisa que quiere concentrarlos en la cola para dañarla todo lo posible.',
     ['Ayoto','Devorafango'],
     'La elección de blanco no documenta que corte o inutilice la cola. Los ajustes de dados, críticos y selección de objetivos se conservan como correcciones de mesa, sin una curación del enemigo por error de interfaz.')
fact(120,'Tlachka intenta abrir la mandíbula mientras Leona sigue dentro','01:18:34.280','01:19:07.350','01:18:48.080',
     'Tlachka quiere seguir golpeando y pregunta si Leona ya tiene la espina. El director recuerda que ella sigue encerrada dentro y los demás no pueden saberlo automáticamente. Guayacán pide obtener más. Al advertir que el agarre mantiene la boca cerrada con Leona dentro, Tlachka coloca un pie en la mandíbula inferior y prepara la otra parte del apoyo para forzar su apertura.',
     ['Tlachka','Leona','Guayacán','Devorafango','Espinas del Devorafango'],
     'La propuesta de abrir la boca se inicia aquí; su resolución pertenece a la continuación de la misma sesión y debe integrarse con ella. Tener una espina dentro de la boca no equivale a haberla entregado ya al alquimista.')


def stage(title,text,*refs):
    return {'titulo':title,'texto':text,'referencias':list(refs)}


stages=[
    stage('No es la boca que buscaban',
          'Ayoto deja espacio para sus compañeros y golpea con el escudo de pinchos, provocando a la masa para atraer sus ataques. Tlachka intenta abrirle la boca, pero descubre que el moho no tiene una boca definida. Al hurgar saca huesos que parecen humanoides y se están consumiendo. Leona no quiere seguir esperando: se lanza dentro y comienza a desgarrar el material con las manos. Guayacán la ve desaparecer, se angustia y falla los golpes con los que pretendía debilitar al rival sin matarlo. La masa sigue dañando a Leona desde el interior y ataca a Ayoto; el goliat responde con una réplica cuando uno de los golpes falla.',
          '44-101','44-102','44-103','44-104','44-105'),
    stage('Un rescate dentro del moho',
          'Leona arranca trozos sin encontrar la espina. Guayacán logra por fin aturdir a la criatura y mantiene sus golpes no letales. Ayoto aprovecha la abertura que hace con el escudo para alcanzar a Leona: tira de ella mientras desgarra el interior y consigue sacarla, ocupando su lugar dentro de la masa. Tlachka continúa golpeando hasta dejar al moho moribundo y, al apartarlo, aparecen más restos de huesos. Entonces Guayacán oye algo detrás. Por la entrada surge una enorme criatura cubierta de barro, con ojos saltones, espinas en el lomo y protuberancias alrededor de la boca. Su descarga ácida llena la sala y alcanza a quienes todavía están junto al moho. Ayoto resiste el ácido que cae sobre su espalda.',
          '44-106','44-107','44-108','44-109','44-110','44-111'),
    stage('Bajo las espinas del Devorafango',
          'Leona aprovecha la boca abierta del Devorafango y se introduce para arrancarle dientes o cartílagos. Guayacán bebe una poción y trata de volver al combate, todavía sin fortuna. Ayoto salta sobre el lomo, pero las espinas se le clavan al golpear: el director distingue los pinchazos del veneno. El goliat se deja caer hacia un lado y derriba al animal con un golpe dirigido a la rodilla. Tlachka ataca el vientre, libre de espinas, con el arma cargada del ácido recibido. Los impactos sacuden a Leona de pared a pared dentro de la boca. El rival se incorpora, muerde a Guayacán y lo deja al límite de sus fuerzas; después derriba a Ayoto con la cola.',
          '44-112','44-113','44-114','44-115','44-116'),
    stage('La primera espina',
          'Leona clava el hacha para afirmarse y fuerza una de las protuberancias del interior. Se resiste, pero un recuerdo de Eromov, de cuando la encontró siendo pequeña, alimenta su rabia. Termina arrancando una espina mientras el Devorafango sigue vivo. Desde fuera solo se oye el grito del animal. Guayacán se cura y lo agarra por la boca para ayudar, mientras Ayoto concentra sus golpes en la cola. Tlachka pregunta por el ingrediente y el director recuerda que Leona sigue encerrada: sus compañeros no conocen automáticamente lo que ha conseguido. Al advertir el problema de la boca cerrada, el guerrero prepara un apoyo en la mandíbula inferior para abrirla y facilitar su salida.',
          '44-117','44-118','44-119','44-120')
]

histories=[]


def history(name,kind,title,text,refs,new=False,description='',note=''):
    histories.append({'nombre':name,'tipo':kind,'nueva':new,'descripcion':description,'nota':note,
                      'etapas':[stage(title,text,*refs)]})


history('Ayoto','personaje','Los escudos entre el moho y las espinas',
        'Ayoto atrae los ataques de la masa de moho y abre un hueco para rescatar a Leona, ocupando su lugar dentro. Cuando aparece el Devorafango resiste el ácido y cambia al nuevo rival: se sube a su lomo, sufre los pinchazos de las espinas y lo derriba con un golpe a la rodilla. La cola del animal lo arroja después al suelo. Reanuda el ataque concentrando sus golpes en ella, sin que se describa una amputación.',
        ['44-101','44-105','44-106','44-109','44-111','44-114','44-116','44-119'])
history('Leona','personaje','La espina y el recuerdo de Eromov',
        'Leona se introduce voluntariamente en la masa de moho para buscar el ingrediente, pero solo arranca material hasta que Ayoto la saca. Ante el Devorafango vuelve a elegir el interior, esta vez su boca. Sacudida por los golpes desde fuera, clava el hacha para afirmarse y fuerza una protuberancia. El recuerdo de Eromov cuando la encontró de pequeña aviva su esfuerzo y consigue arrancar una espina con el animal vivo. Permanece aún dentro mientras sus compañeros intentan ayudarla.',
        ['44-103','44-107','44-109','44-112','44-115','44-117','44-120'])
history('Guayacán','personaje','Del temor por Leona al apoyo de la extracción',
        'Guayacán se angustia al ver a Leona dentro del moho y falla los primeros golpes con los que busca dejarlo inconsciente. Después logra aturdirlo. El Devorafango lo alcanza con ácido y más tarde con un mordisco que lo deja a un punto de vida. Utiliza curaciones y decide sujetar la boca del animal para facilitar el trabajo de sus compañeros. Esa ayuda mantiene a Leona encerrada hasta que se pueda forzar la mandíbula.',
        ['44-104','44-108','44-111','44-113','44-116','44-118','44-120'])
history('Tlachka','personaje','Hurgar, golpear y abrir paso',
        'Tlachka busca la espina en la masa de moho y encuentra huesos humanoides en descomposición. Mantiene golpes no letales durante parte del combate y deja al rival moribundo. Al aparecer el Devorafango aprovecha que Ayoto lo derriba para atacar su vientre sin espinas; el arma lleva el ácido absorbido de la descarga. Cuando comprende que Leona sigue dentro de la boca, prepara una palanca con el cuerpo para forzar la mandíbula y abrirle paso.',
        ['44-102','44-106','44-110','44-115','44-120'])
history('Eromov','personaje','Un recuerdo que sostiene la búsqueda',
        'Leona recuerda a Eromov cuando la encontró de pequeña durante el esfuerzo por arrancar una espina al Devorafango. Ese recuerdo refuerza su determinación y consigue extraer el ingrediente del animal vivo. El pasaje concreta un episodio del vínculo entre ambos, sin fijar parentesco biológico, adopción formal o toda la historia de su infancia.',
        ['44-117'])
history('Masa de moho de la cueva','personaje','Los huesos del interior',
        'La masa de moho no tiene una boca definida, pero su interior contiene huesos aparentemente humanoides que se están consumiendo. Leona se introduce para buscar una espina, mientras sus compañeros la golpean e intentan aturdirla. Ayoto abre un hueco, saca a Leona y ocupa su lugar. Tras nuevos ataques queda moribunda. La entrada del Devorafango y su descarga de ácido interrumpen la atención del grupo sin que se confirme aquí el destino final del moho.',
        ['44-102','44-103','44-108','44-109','44-110','44-111'],True,
        'Masa móvil de moho que ataca en la cueva y contiene restos de huesos humanoides.',
        'Rival distinto del Devorafango: carece de boca propiamente dicha. No se fija especie de bestiario ni identidad de sus víctimas.')
history('Devorafango','personaje','El ácido y la espina arrancada en vida',
        'El Devorafango entra en la cueva cubierto de barro, con ojos grandes, espinas dorsales y protuberancias dentro de la boca. Descarga ácido sobre la sala. Leona se introduce en su boca para arrancar el ingrediente, mientras Ayoto lo derriba y Tlachka golpea su vientre libre de espinas. El animal vuelve a incorporarse, deja muy herido a Guayacán y derriba a Ayoto con la cola. Leona consigue una espina antes de que el grupo pueda abrir de nuevo sus mandíbulas.',
        ['44-111','44-112','44-114','44-115','44-116','44-117','44-118','44-120'],True,
        'Gran criatura cubierta de barro que escupe ácido y presenta espinas en el lomo y el interior de la boca.',
        'El nombre procede del encargo de Parroter y la identificación se apoya en sus rasgos. No se añade especie de bestiario o una naturaleza distinta del ejemplar encontrado.')
history('Espinas del Devorafango','objeto','La primera pieza del remedio',
        'La búsqueda comienza equivocadamente en la masa de moho, donde solo aparecen huesos y material desgarrado. Leona entra después en la boca del Devorafango y, afirmada con el hacha, fuerza una protuberancia hasta arrancarla. La criatura sigue viva durante la extracción. El ingrediente permanece con Leona dentro de la boca mientras Tlachka se dispone a abrir la mandíbula; su entrega y uso deben enlazarse con la continuación de la sesión.',
        ['44-102','44-107','44-112','44-117','44-120'],True,
        'Espinas del interior de la boca del Devorafango buscadas como ingrediente para el remedio de Eromov.',
        'La extracción en vida es condición del encargo. No se confunden con los huesos del moho, el fragmento de espada del capítulo 40 o las espinas de otros objetos.')
history('Cueva del lago cercano a Cuicapalli','lugar','Dos amenazas en la misma sala',
        'La cueva alberga una masa móvil de moho que consume restos de huesos. Mientras el grupo lucha contra ella y trata de sacar a Leona de su interior, entra el Devorafango y cubre la sala de ácido. La extracción de sus espinas exige combatir alrededor de su boca y forzar después las mandíbulas para abrir paso a la harengon.',
        ['44-102','44-109','44-111','44-117','44-120'],True,
        'Cueva recordada por Leona junto a un lago cercano a Cuicapalli, donde el grupo busca al Devorafango.',
        'Descripción geográfica provisional, sin topónimo propio. No se identifica con la cueva de la Hoja Caída o el refugio yuan-ti por compartir un entorno subterráneo.')

delivery={'bloque':2,'lectura_completa':True,'primer_segmento':'c001677','ultimo_segmento':'c003353',
          'etapas':stages,'afirmaciones':facts,'historias_entidades':histories,
          'misiones':[
              'Obtener las espinas para el remedio: tras buscar sin éxito en el moho, Leona entra en el Devorafango y arranca una espina mientras sigue vivo; aún permanece con el ingrediente dentro de su boca (44-102–44-103, 44-107, 44-112, 44-117, 44-120).',
              'Sacar a Leona del peligro: Ayoto la extrae del moho intercambiando posiciones; luego la harengon se mete en la boca del nuevo rival y Tlachka prepara otra apertura para facilitarle la salida (44-109, 44-112, 44-118, 44-120).',
              'Debilitar y sujetar al Devorafango: Ayoto lo derriba, Tlachka ataca el vientre y Guayacán, tras quedar al límite y curarse, lo agarra por la boca para ayudar al grupo. No se afirma en este bloque una muerte del animal (44-114–44-120).'
          ],
          'preguntas':[
              '¿Qué identidad tienen los restos humanoides que el moho consume y cuál es el destino de la masa tras la descarga de ácido? El combate la deja moribunda, sin muerte inequívocamente narrada (44-102, 44-110–44-111).',
              '¿Cómo se produjo el encuentro de Eromov con Leona cuando era pequeña? El recuerdo la impulsa, pero no reconstruye su infancia ni establece toda su filiación (44-117).',
              '¿Cómo se abrirá la boca para sacar a Leona y el ingrediente? El corte deja a Tlachka preparando el apoyo, pero la pregunta necesita integrarse con la continuación de esta misma sesión (44-118, 44-120).'
          ],
          'contradicciones':[
              'La masa inicial de moho carece de boca definida y contiene huesos consumidos; el Devorafango llega después con dientes, espinas y ácido. No se fusionan por ser dos rivales dentro de la cueva (44-102–44-103, 44-110–44-112).',
              'El moho queda a un punto de vida. El comentario posterior que lo da por muerto se corrige inmediatamente; no debe afirmarse su muerte sin otra evidencia (44-110–44-111).',
              'Guayacán declara daño no letal para debilitar al primer rival. El reconocimiento alterna letal y no letal en los golpes de Tlachka; el estado confirmado de la masa y las declaraciones puntuales se conservan sin uniformar todo el combate (44-104, 44-106, 44-108, 44-110).',
              'Las espinas dorsales hieren a Ayoto por los pinchazos y el director niega que lo envenenen. El ácido, el daño perforante y el veneno de Eromov no son un único efecto (44-111, 44-114).',
              'El director mantiene a Leona dentro de la boca cuando el animal regurgita. La espina extraída no se vuelve automáticamente conocida por quienes están fuera, y el agarre de Guayacán mantiene la boca cerrada (44-116–44-120).',
              'Los ajustes de objetivos y dados no documentan curaciones accidentales del monstruo. Discord y la carta son recursos de la mesa y no organizaciones o causas nuevas del mundo (44-107, 44-113, 44-119).'
          ],
          'nombres_dudosos':[
              'Traska, Trasca y variantes corresponden al guerrero Tlachka por continuidad del orden de turnos, sus armas y sus intervenciones; no se crea un personaje nuevo (44-102, 44-106, 44-110, 44-115, 44-120).',
              'Ayoto, Yoto y Hayot corresponden al goliat de los dos escudos. Leona es la harengon, distinta de Naór; Guayacán continúa como el combatiente aviar que la acompaña (44-101, 44-103–44-105, 44-109, 44-114, 44-116–44-119).',
              'La criatura espinosa y cubierta de barro se enlaza al Devorafango del encargo de Parroter. El relato no ofrece un nombre propio individual ni una identificación de bestiario adicional (44-111–44-112, 44-117).',
              'Erom en el recuerdo de Leona corresponde a Eromov. Haberla encontrado de pequeña no determina por sí solo parentesco biológico o adopción formal (44-117).',
              'Espina, diente, muela y protuberancia son expresiones usadas durante la extracción oral. Se mantiene el ingrediente como espina del Devorafango sin multiplicarlo por cada descripción de su forma (44-112, 44-117).'
          ],
          'continuidad':[
              {'pregunta_id':'P30-001','nota':'Avance de la búsqueda del antídoto de Parroter: Leona obtiene la primera espina en vida. La administración y recuperación de Eromov pertenecen a la integración con el desenlace de la sesión.','referencias':['44-117']},
              {'pregunta_id':'P40-006','nota':'La búsqueda del ingrediente continúa la ayuda prometida a Eromov; este bloque no retoma el ataque al festival ni muestra la entrega de la cura.','referencias':['44-112','44-117','44-120']},
              {'pregunta_id':'P40-001','nota':'No hay análisis de la muestra del claro ni explicación causal nueva de la animación de restos; los huesos consumidos del moho no se equiparan con los no muertos del claro.','referencias':['44-102','44-110','44-114']},
              {'pregunta_id':'P41-006','nota':'No aparecen ni se analizan los viales verdes. El ácido del Devorafango y las espinas obtenidas no acreditan identidad química con esos líquidos o la muestra de Leona.','referencias':['44-111','44-114','44-117']}
          ]}

assert len(rows)==839
assert rows[0]['id']=='c001677' and rows[-1]['id']=='c003353'
assert len(facts)==20
assert all(seconds(f['inicio'])<=seconds(f['evidencia_cue']['inicio'])<=seconds(f['fin']) for f in facts)
write_json(ROOT / 'campanas/xoltacan/revision/borradores/44/entrega_2.json',delivery)
print(f'Entrega 2: {len(facts)} hechos validados, {len(stages)} etapas y {len(histories)} historias propuestas; '+str(sum(len(s['texto'].split()) for s in stages))+' palabras de relato.')
