import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import validate_fact

rows = json.loads((ROOT / 'borradores/42/bloque_1_segmentos.json').read_text(encoding='utf-8'))
source = ROOT / 'xoltacan_subtitulos/subtitulos/42 - 3IUV_YN_zxM.es-orig.vtt'
facts = []

def fact(a, b, anchor, title, statement, names, kind='hecho_confirmado', limit=''):
    cue = rows[anchor]
    item = dict(id=f'42-{len(facts)+1:03d}', titulo=title, tipo=kind,
                afirmacion=statement, inicio=rows[a]['inicio'], fin=rows[b]['fin'],
                cita=cue['texto_original'],
                evidencia_cue=dict(inicio=cue['inicio'], fin=cue['fin'], texto=cue['texto_original']),
                entidades=names, ambito='preparativos y comienzo de la batalla por Shiaru',
                conocedores=[], conocimiento_personaje='desconocido',
                nota_conocimiento='Acceso de Madame Oghma sin establecer en este pasaje.',
                confianza='lectura de subtítulos; audio no cotejado', limitacion=limit)
    validate_fact(item, source)
    facts.append(item)

fact(35,45,41,'Poncelot regresa con un paquete para Ione',
     'Sir Poncelot cuenta que ha ayudado a Ione a preparar el barco para la batalla. Antes de zarpar corre a recoger un paquete encargado a Alice y regresa al puerto con él.',
     ['Sir Poncelot','Ione','Shiaru'], 'declaracion_personaje',
     'Alice solo se menciona como destinataria del encargo; no queda identificada con una persona del catálogo. El contenido del paquete se muestra más tarde.')
fact(61,82,64,'Ione prepara al Zampaolas para el enfrentamiento directo',
     'Ione relata la reparación y el aprovisionamiento del Zampaolas: barriles de pólvora, aceite hirviendo, una cadena procedente de un barco naufragado para Ilikar, una ballesta para Poncelot, cañones, balas y munición unida por cadenas. Recuerda una profecía que aconsejaba hacerse pasar por marines, pero opta por prepararse para luchar de frente.',
     ['Ione','Zampaolas','Sir Poncelot','Ilikar','Marina'], 'declaracion_personaje',
     'No se reproduce la profecía completa ni se demuestra en este pasaje que todos los recursos preparados lleguen a utilizarse.')
fact(99,117,107,'Ilikar vuelve de Iktan y busca aliados contra el dragón',
     'Ilikar recuerda que ha cruzado la isla, comparte un enemigo en el dragón verde y ha entrenado como monje gracias a Tortas. Vuelve a Shiaru en busca de su tripulación y de Poncelot, a quien considera experto en dragones. La necesidad de Ione lo lleva a preparar el barco y recoger un arma nueva para el combate próximo.',
     ['Ilikar','Tortas','Dragón verde del bosque de Iktan','Shiaru','Sir Poncelot','Ione','Tripulación del Zampaolas'], 'declaracion_personaje',
     'El nombre entrecortado del dragón no fija su grafía ni lo identifica con Clodidrax. No se representa una aceptación de la caza por Poncelot o Ione; tampoco se identifica aquí el arma recién recogida.')
fact(133,156,136,'Nox busca una patente de corso con la Marina',
     'Nox explica que su trato con la Marina pretende obtener una patente de corso y seguir su propio rumbo después de que lo echaran de la tripulación. Ha examinado timones, cabos y velas de tres barcos y hablado con el almirante sobre el ataque y la defensa de Shiaru.',
     ['Nox','Marina','Tórtola','Tripulación del Zampaolas','Shiaru'], 'declaracion_personaje',
     'La patente es el objetivo declarado del trato, no un documento cuya entrega se muestre. El apelativo Paloma del repaso inicial se vincula a Tórtola por la continuidad de la misma operación naval, sin crear un almirante nuevo.')
fact(50,168,122,'Las frutas alteran temporalmente a los cuatro viajeros',
     'El director resuelve cuatro efectos de fruta: la lengua de Poncelot puede alcanzar objetos pequeños a diez pies; Ione gana dos puntos de Fuerza durante la partida; la sombra de Ilikar se estira y puede señalar objetos para avisar a sus compañeros; la piel de Nox desarrolla espinas que dañan a quien lo golpee cuerpo a cuerpo.',
     ['Sir Poncelot','Ione','Ilikar','Nox'], 'explicacion_director',
     'Los efectos son resoluciones de la sesión. No acreditan cambios permanentes ni una conexión narrativa con Kuroto, citado en una broma de mesa.')
fact(189,247,199,'Shiaru reúne a sus defensores en la plaza',
     'La plaza reúne a los habitantes y aliados de Shiaru. Gobs prepara agujas, una sierra y un taladro; Armin espera con dos enormes mazos. Un grupo de mujeres prepara armas de fuego. Eleanor y Erandy están presentes junto a miembros del Zampaolas. Jack aparece nervioso detrás de Ilikar; también se muestran Baps, Mugre y Ojo Ausente. Bonnie conversa con Molly.',
     ['Shiaru','Gobs','Armin','Eleanor','Erandy','Jack','Ilikar','Baps','Mugre','Ojo Ausente','Bonnie','Molly','Tripulación del Zampaolas'],
     limit='El pasaje no nombra con claridad a la mujer que encabeza al grupo armado. Su contexto no basta para atribuir a Liz cada intervención o confirmar que Gobs opere a alguien.')
fact(251,288,283,'La tripulación sitúa al supuesto dragón de Ilikar en un barril de arena',
     'Poncelot pregunta por el pequeño ser de fuego que acompaña a Ilikar, lo llama bebé dragón rojo y teme nuevos incendios. Ilikar asegura que está en el barco; Ione explica que el goliat lo ha puesto en un barril con arena. La capitana lo llama demonio por los desperfectos que le atribuye.',
     ['Sir Poncelot','Cipo','Ilikar','Ione','Zampaolas'], 'declaracion_personaje',
     'No se abre el barril en este intervalo. La identificación contextual con Cipo se apoya en su vínculo con Ilikar desde el capítulo 40 y su presencia posterior en el Zampaolas; no se identifica con el Dragón de Erendriel. Dragón y demonio son denominaciones de los viajeros, sin cambio de naturaleza demostrado.')
fact(360,393,373,'Ione promete proteger a Jack y le confía su gorro',
     'Jack reconoce que antes pertenecía a la Marina y teme no ser un buen pirata al combatir contra ella. Ione le promete que saldrá vivo mientras permanezca en su barco y participe a su lado. Le entrega su gorro de capitana para que lo guarde y le pide que se lo devuelva al terminar. Sonríe para animarlo aunque también siente miedo.',
     ['Jack','Ione','Marina','Zampaolas','Gorro de capitana de Ione'],
     limit='La promesa no demuestra la supervivencia posterior de Jack. Jacki se vincula al Jack exmarine ya catalogado por el nombre, su pasado y su pertenencia a la misma tripulación.')
fact(395,435,418,'Poncelot regala a Ione un fular de alas de mosca',
     'Poncelot agradece a Ione que lo acogiera y lo tratara como uno de los suyos. Le entrega el paquete: un fular descrito por las vetas de alas de mosca y su transparencia. Ione se lo pone como bufanda, le da las gracias y lo abraza, para incomodidad protocolaria del caballero.',
     ['Sir Poncelot','Ione','Fular de alas de mosca de Ione'],
     limit='La descripción de los subtítulos es vacilante. No se atribuyen propiedades mágicas al fular ni se confirma que el material proceda de Merlucilla III.')
fact(436,478,469,'Mugre dispara accidentalmente contra Ione',
     'Un disparo interrumpe el abrazo. El director aplica tres puntos de daño a Ione y una ceguera de un turno a Poncelot por el contenido de la bolita que estalla. Mugre sostiene la pistola y pide perdón. La pérdida adicional de cuatro monedas no se ejecuta como tal porque Ione dice no tener dinero.',
     ['Mugre','Ione','Sir Poncelot'],
     limit='El proyectil se describe alternativamente con comida y un término censurado. No hay ataque confirmado de la Marina en la plaza; los efectos mezclan cartas o intervenciones de la mesa con la narración.')
fact(479,513,487,'Bonnie reclama la defensa de la libertad de Shiaru',
     'Bonnie impone silencio y llama a los presentes a defender Shiaru contra la Marina. Recuerda que acogió a compañeros como Eleanor, Poncelot e Ilikar y les exige permanecer en sus puestos. Presenta el poblado como un lugar donde ser libres bajo su autoridad y amenaza a quienes huyan.',
     ['Bonnie','Shiaru','Marina','Eleanor','Sir Poncelot','Ilikar'],
     limit='Las amenazas y la declaración de libertad pertenecen al discurso de Bonnie; no se representan huidas ni ejecuciones de desertores.')
fact(514,539,515,'La moneda de Bonnie acompaña su transformación eléctrica',
     'Bonnie saca la moneda de los capitanes piratas y la aprieta. Chisporrotea, sus ojos brillan azules y su aspecto cambia entre rayos; aparece un símbolo de rayo y se oscurece el cielo. Proclama que solo uno de los bandos conservará esas tierras y se dirige al muelle para embarcar.',
     ['Bonnie','Moneda pirata de Bonnie','Cinco reyes piratas','Shiaru'],
     limit='Se representa la activación y sus efectos visibles, sin explicar el origen de la moneda, sus límites completos o una maldición demostrada.')
fact(540,668,574,'Los defensores embarcan y ocupan sus puestos',
     'Los piratas corren a los muelles. Ione llama a los Zampaolas a hacer rugir los mares y los cañones y procura dar seguridad a sus compañeros. Poncelot monta al tigre y embarca; Ilikar sigue a su capitana y Jack va tras él. Mugre orienta a Ojo Ausente cuando toma la dirección equivocada. En el Zampaolas están los trillizos, los cañones y la ballesta; Ojo Ausente sube a vigilar, Mugre baja a preparar comida y Baps revisa los cañones olfateándolos.',
     ['Ione','Tripulación del Zampaolas','Zampaolas','Sir Poncelot','Merlucilla IV','Ilikar','Jack','Mugre','Ojo Ausente','Baps'],
     limit='La mención colectiva de los trillizos no asigna acciones separadas a Mingo, Mango o Mungo. No debe confundirse el tigre con el tiburón Merlucilla V de la extracción anterior.')
fact(670,703,675,'Poncelot prepara una armadura improvisada para el tigre',
     'Sir Poncelot ajusta su armadura y armas y explica que ha preparado una protección improvisada para su montura con maderos y trozos de barril. Lleva casco y capa que describe como de sierpes. La mesa aclara entre bromas que esas piezas no prueban trofeos de auténticos dragones.',
     ['Sir Poncelot','Merlucilla IV'], 'declaracion_personaje',
     'Las bromas sobre un conjunto de matadragones no acreditan que Poncelot haya matado a esos dragones ni permiten identificar el origen de cada pieza.')
fact(706,729,710,'Siete barcos piratas salen bajo la tormenta',
     'El director describe cinco barcos piratas además del Zampaolas y del enorme buque de Bonnie. La pequeña flota incluye cascos deteriorados y artillería de funcionamiento incierto. Dejan espacio para el Zampaolas y avanzan bajo un cielo negro, lluvia y relámpagos.',
     ['Bonnie','Zampaolas','Relámpago del Mar','Shiaru','Tripulación del Zampaolas'], 'explicacion_director',
     'La cifra corresponde a la flota descrita antes del enfrentamiento, no a los supervivientes posteriores. La artillería averiada se plantea como posibilidad general, sin inventario por buque.')
fact(739,825,822,'La Marina forma dos líneas de fuego frente a los piratas',
     'Numerosos barcos de guerra de la Marina aparecen desde el sur, en dirección del Fuerte Aurora, con velas blancas, madera cuidada y muchos cañones. Los piratas empiezan a disparar sin una formación clara. La Marina espera, gira sus naves de costado y escalona dos filas para permitir que ambas disparen sin alcanzarse entre sí.',
     ['Marina','Fuerte Aurora','Shiaru','Bonnie'],
     limit='No se da un total exacto de barcos de la Marina. La formación táctica no demuestra todavía que haya destruido ningún buque pirata.')
fact(829,884,859,'Ione decide flanquear por los arrecifes',
     'Ione pregunta si el Zampaolas puede cruzar entre las rocas. El director permite el paso, advirtiendo del riesgo de roturas en el arrecife. La capitana ordena dirigirse allí para rodear a la Marina y atacar por detrás, aprovechando el menor calado de su barco. El Zampaolas empieza la maniobra.',
     ['Ione','Zampaolas','El Garfio','Marina'],
     limit='La decisión y el movimiento inicial no garantizan el flanqueo completo ni que otros barcos puedan seguir el mismo recorrido sin daños.')
fact(885,898,886,'El Relámpago del Mar avanza con Bonnie preparando rayos',
     'El buque de Bonnie, llamado Relámpago del Mar, avanza entre las otras naves. Parece despedir rayos. Bonnie reprende a los piratas por gastar munición antes de tiempo y levanta una mano donde se acumulan chispas, preparando una acción.',
     ['Bonnie','Relámpago del Mar','Moneda pirata de Bonnie'],
     limit='El nombre del buque procede de la continuidad del pasaje. La acción preparada aún no se resuelve en este bloque y no se atribuye cada descarga del barco directamente a la moneda.')
fact(900,945,906,'Nox navega con Tórtola a bordo del Invictus',
     'La narración muestra al Invictus, buque de Tórtola, navegando hacia el norte fuera del primer despliegue. El director lo presenta como un barco al que nadie ha logrado derrotar ni dañar el casco. Tórtola gobierna un pequeño timón instalado en el enorme principal, asistido por un hombre. Nox come junto al timón, vestido con ropa limpia y nueva, antes de observar las naves con el catalejo.',
     ['Invictus','Tórtola','Nox','Marina'], 'explicacion_director',
     'La reputación de invicto no equivale a una invulnerabilidad mecánica demostrada. No se crea un personaje para el ayudante sin nombre.')
fact(946,997,987,'Nox advierte del poder de Bonnie y Tórtola muestra una luz verde',
     'Tórtola dice mantener a Nox a bordo porque todavía puede utilizarlo. Ambos observan la formación pirata y hablan de atacar por detrás. Nox llama la atención sobre el buque mayor y la tormenta repentina y advierte del poder de Bonnie. Tórtola responde que también tiene sus trucos y muestra una luz verde al mover el ala. En la mesa se identifica el gesto con desintegrar.',
     ['Nox','Tórtola','Bonnie','Invictus','Relámpago del Mar','Marina'],
     limit='La identificación de desintegrar se comenta fuera del diálogo: el director distingue lo que reconocen los jugadores de lo que saben sus personajes. No se ha lanzado aún el conjuro contra un objetivo en este intervalo.')
fact(998,1021,1003,'Nox propone una ruta por el arrecife y Tórtola manda barcos delante',
     'Nox recomienda que los barcos de detrás sigan en línea recta para no encallar. Tórtola advierte que el plan debe funcionar por el bien de ambos y ordena situar delante las naves pequeñas, de modo que encallen antes que el Invictus si algo falla. Nox anuncia que irá a proa para señalar el camino, pero mira a ambos lados y entra en el interior del barco.',
     ['Nox','Tórtola','Invictus','Marina','El Garfio'],
     limit='El pasaje no prueba por sí solo un sabotaje consumado ni que las naves lleguen a encallar. La promesa de ir a proa precede a la decisión visible de bajar al interior.')
fact(1023,1058,1051,'Nox encuentra a una figura encadenada en los calabozos del Invictus',
     'Al bajar, Nox se cruza con un marine que se queja de algo que el capitán ha traído. Sigue hacia los calabozos que había examinado. Un guardia abandona la zona al oír órdenes de preparación y Nox ve una gran jaula con una figura humanoide agachada y oscura, suspendida o sujeta por enormes cadenas en los brazos.',
     ['Nox','Invictus','Marina','Pinky'],
     limit='En este intervalo no se identifica la especie, nombre o naturaleza de la figura. La etiqueta Pinky procede de la identificación posterior del mismo cautivo en el capítulo; su silueta no demuestra por sí sola una conexión con la criatura de Aurora. No se representa aún su liberación.')
fact(1059,1077,1066,'La Marina comienza a avanzar y disparar',
     'La narración vuelve al enfrentamiento naval. Las naves de la Marina empiezan a avanzar y a disparar; el director sitúa impactos sobre objetivos del combate. El bloque termina mientras continúa esa primera descarga.',
     ['Marina','El Garfio'],
     limit='El corte del bloque no contiene aún un balance de daños, hundimientos ni bajas.')

stages = [
    dict(titulo='Preparar el Zampaolas y elegir un bando', referencias=['42-001','42-002','42-003','42-004','42-005','42-006','42-007'], texto=
         'Sir Poncelot regresa al puerto con un paquete para Ione después de ayudar a preparar el Zampaolas. La capitana ha reparado y armado su nave con cañones, munición encadenada, pólvora, aceite y una ballesta para el gnomo. Recuerda que una profecía aconsejaba hacerse pasar por marines, pero prefiere afrontar la batalla. Ilikar vuelve de su entrenamiento con Tortas y de la investigación del dragón verde para buscar aliados en Shiaru; al encontrar a su capitana necesitada de ayuda, se suma a los preparativos. Nox ha tomado otro camino: declara que trabaja con la Marina para conseguir una patente de corso y marcar su propio rumbo tras su expulsión de la tripulación. Las frutas añaden efectos peculiares a los cuatro: lengua extensible, fuerza aumentada, sombra capaz de señalar y piel espinosa. En la plaza se reúnen los defensores. Gobs ordena instrumental, Armin espera con sus mazos y los compañeros comprueban sus armas. La ausencia del pequeño dragón alarma a Poncelot, aunque Ilikar e Ione aseguran haberlo dejado en un barril de arena en el barco.'),
    dict(titulo='Promesas antes de zarpar', referencias=['42-008','42-009','42-010','42-011','42-012','42-013','42-014','42-015'], texto=
         'Jack confiesa su miedo a combatir contra la Marina, a la que perteneció. Ione le promete protección mientras luche a su lado y le entrega su gorro para que lo conserve hasta el final. También ella siente miedo, aunque intenta ocultarlo. Poncelot le agradece la acogida con un fular de alas de mosca; Ione se lo pone y abraza al caballero. Un disparo accidental de Mugre interrumpe el momento y deja herida a la capitana y brevemente ciego al gnomo. Bonnie impone silencio y exige defender la libertad de Shiaru. Aprieta su moneda pirata: su cuerpo chisporrotea, brillan sus ojos y se forman nubes negras. Los piratas corren a embarcar. Ione anima al Zampaolas; Poncelot llega montado en su tigre, al que ha preparado una armadura improvisada. Ilikar y Jack siguen a su capitana mientras los demás ocupan sus puestos. La flotilla reúne cinco buques además del Zampaolas y de la nave de Bonnie. Bajo lluvia y relámpagos, los cascos deteriorados avanzan hacia la batalla.'),
    dict(titulo='Dos maniobras en el arrecife', referencias=['42-016','42-017','42-018','42-019','42-020','42-021','42-022','42-023'], texto=
         'La Marina aparece desde el sur con numerosos barcos de guerra bien cuidados. Los piratas disparan sin orden, mientras sus enemigos forman dos filas escalonadas y esperan. Ione decide aprovechar el menor calado del Zampaolas para cruzar el arrecife y atacar por detrás, aunque el paso amenaza con dañar el casco. Bonnie adelanta su Relámpago del Mar, reprende el gasto prematuro de munición y prepara chispas en una mano. En otra parte de la flota navega el Invictus de Tórtola, cuya reputación lo presenta como nunca derrotado. Nox se encuentra a bordo. Advierte al almirante sobre la tormenta y el poder de Bonnie; Tórtola responde mostrando una luz verde cuya identificación como desintegrar pertenece a los comentarios de mesa. Nox aconseja mantener una ruta recta por el arrecife y Tórtola manda las naves pequeñas por delante. El pirata anuncia que señalará el camino desde proa, pero baja al interior. En los calabozos encuentra una figura humanoide encadenada dentro de una gran jaula, todavía sin identidad. La escena vuelve al mar cuando la Marina empieza a avanzar y disparar.')
]

histories = []
def history(name, kind, title, text, refs, new=False, description='', note=''):
    histories.append(dict(nombre=name,tipo=kind,nueva=new,descripcion=description,nota=note,
                          etapas=[dict(titulo=title,texto=text,referencias=refs)]))

history('Sir Poncelot','personaje','Un obsequio antes de la batalla',
        'Poncelot ayuda a preparar el Zampaolas y recoge un regalo para Ione. Le agradece que lo haya acogido y le entrega un fular de alas de mosca; ella se lo pone y lo abraza. Tras el accidente de Mugre y el llamamiento de Bonnie, embarca con el tigre Merlucilla IV, protegido con maderos y trozos de barril. La experiencia contra dragones que le atribuye Ilikar no representa una nueva hazaña ni su aceptación de esa caza.', ['42-001','42-003','42-009','42-010','42-013','42-014'])
history('Ione','personaje','Capitana entre el miedo y las promesas',
        'Ione prepara el Zampaolas para un combate frontal y trata de sostener el ánimo de sus compañeros. A Jack, preocupado por enfrentarse a su antigua Marina, le promete que saldrá vivo y le confía el gorro de capitana para que se lo devuelva al terminar. Recibe con afecto el regalo de Poncelot y después anima a la tripulación a embarcar. Ante la formación enemiga, decide buscar su retaguardia cruzando el arrecife con el barco de menor calado.', ['42-002','42-008','42-009','42-013','42-017'])
history('Ilikar','personaje','El regreso a la tripulación',
        'Después de entrenar con Tortas y compartir la amenaza del dragón verde, Ilikar vuelve a Shiaru para buscar ayuda. Encuentra a Ione preparando la defensa y la acompaña: ayuda con el barco, recoge un arma y asegura que el pequeño dragón está apartado en un barril de arena. Embarca tras su capitana mientras Jack lo sigue. No se representa un acuerdo nuevo para cazar al dragón.', ['42-003','42-007','42-013'])
history('Nox','personaje','A bordo del Invictus',
        'Nox declara que busca una patente de corso mediante su trato con la Marina. Tras examinar varios barcos, navega con Tórtola en el Invictus y conversa con él sobre cómo atacar a los piratas. Advierte del poder de Bonnie y recomienda mantener una ruta por el arrecife. Aunque dice que irá a proa, baja al interior y encuentra una figura humanoide encadenada en una jaula. Su presencia a bordo no demuestra que ya haya recibido la patente ni explica aún su decisión de buscar los calabozos.', ['42-004','42-019','42-020','42-021','42-022'])
history('Bonnie','personaje','La tormenta sobre Shiaru',
        'Bonnie reúne a los defensores de Shiaru y los exhorta a combatir a la Marina. Al apretar su moneda pirata cambia de aspecto entre rayos y el cielo se oscurece. Embarca, avanza en el Relámpago del Mar y prepara una nueva descarga mientras exige a sus aliados que dejen de malgastar munición. El discurso y la transformación no resuelven todavía el resultado de la batalla ni el origen de su poder.', ['42-011','42-012','42-015','42-018'])
history('Jack','personaje','El gorro confiado por Ione',
        'Antes de la batalla Jack reconoce que su pasado en la Marina lo hace temer no estar a la altura como pirata. Ione le ofrece protección y le entrega su gorro de capitana, que Jack promete devolver cuando termine el enfrentamiento. Sigue a Ilikar al embarcar. La promesa compartida documenta confianza y preocupación; no anticipa su supervivencia.', ['42-008','42-013'], note='Jacki es una variante contextual del Jack exmarine del Zampaolas, sin nueva identidad.')
history('Tórtola','personaje','Una aproximación por la retaguardia',
        'Tórtola gobierna el Invictus mientras su armada encara a los defensores de Shiaru. Mantiene a Nox a bordo por su utilidad y escucha sus advertencias sobre Bonnie. Responde mostrando una luz verde y ordena que los barcos pequeños entren antes que su nave en la ruta del arrecife. Los rangos de capitán y almirante alternan en el diálogo; no crean dos personas en esta escena.', ['42-019','42-020','42-021'])
history('Mugre','personaje','Un disparo antes del combate',
        'En los preparativos de Shiaru Mugre dispara accidentalmente una pistola y alcanza a Ione; pide perdón y aparta el arma. Después ayuda a Ojo Ausente a tomar el camino de los muelles y, ya en el Zampaolas, baja a preparar comida mientras la tripulación ocupa sus puestos.', ['42-010','42-013'])
history('Ojo Ausente','personaje','Volver al puesto de vigía',
        'La confusión de Ojo Ausente persiste durante la concentración: mira en dirección contraria a Bonnie y después se encamina hacia el lado equivocado. Mugre lo corrige. En el Zampaolas vuelve a subir al puesto de vigía pese a sus problemas de visión.', ['42-006','42-013'])
history('Baps','personaje','Preparativos entre comida y cañones',
        'Baps aparece más pendiente de lo que encuentra en el suelo que de la reunión. Cuando advierte que los demás se han marchado, corre al muelle y embarca. A bordo del Zampaolas se acerca a olfatear los cañones como parte de su revisión.', ['42-006','42-013'])
history('Gobs','personaje','Instrumental para la defensa',
        'Gobs acude a la concentración de Shiaru y organiza agujas, una sierra y un taladro en su mochila antes de la batalla. El pasaje muestra su disposición y su instrumental, sin representar una intervención médica.', ['42-006'])
history('Armin','personaje','Dos mazos en la plaza',
        'Armin espera entre los defensores reunidos en la plaza de Shiaru con dos mazos enormes. Su presencia lo sitúa en la preparación de la defensa, sin atribuirle todavía bajas o reparaciones concretas durante el enfrentamiento.', ['42-006'])
history('Molly','personaje','Junto a Bonnie en los preparativos',
        'Molly conversa con Bonnie durante la concentración de los defensores de Shiaru. La escena conserva su cercanía en los preparativos contra la armada, sin transcribir el contenido de esa conversación ni adjudicarle una orden naval.', ['42-006','42-011'])
history('Merlucilla IV','personaje','Un tigre a bordo del Zampaolas',
        'Poncelot monta de nuevo al tigre para llegar al muelle y embarcar en el Zampaolas. Antes de la batalla explica que le ha improvisado protección con maderos y partes de barril. Este regreso corresponde al tigre Merlucilla IV, no transforma al tiburón de la extracción del barco en un felino.', ['42-013','42-014'])
history('Cipo','personaje','El supuesto dragón en un barril de arena',
        'Durante los preparativos, Poncelot pregunta por el ser de fuego que acompaña a Ilikar y lo llama bebé dragón rojo. Ilikar afirma que está en el barco e Ione explica que lo han dejado en un barril de arena. La continuidad con el acompañante de Ilikar y la presencia posterior de Cipo en el Zampaolas sostienen la identificación contextual. Las denominaciones de dragón y demonio usadas por los viajeros no lo convierten en el Dragón de Erendriel ni establecen una naturaleza demoníaca.', ['42-007'])
history('Shiaru','lugar','Una defensa reunida en la plaza',
        'Los habitantes y aliados de Shiaru se concentran en la plaza para afrontar a la Marina. Bonnie invoca la acogida dada a los viajeros y reclama defender la libertad del poblado. Después de los discursos los piratas embarcan y la defensa se desplaza al mar, donde se aproxima una flota mayor desde Aurora.', ['42-006','42-011','42-013','42-016'])
history('El Garfio','lugar','Un arrecife entre dos maniobras',
        'El arrecife condiciona la primera fase de la batalla naval. Ione intenta aprovechar el menor calado del Zampaolas para rodear la formación enemiga; el director advierte que cruzarlo puede romper el casco. En el Invictus, Nox propone una ruta recta y Tórtola manda las naves pequeñas delante para proteger la suya. La coincidencia de ambas maniobras no demuestra por sí sola que el paso sea seguro o que los barcos encallen.', ['42-017','42-021'])
history('Zampaolas','objeto','Preparado para cruzar el arrecife',
        'Ione repara y equipa el Zampaolas con artillería, munición encadenada, pólvora, aceite y una ballesta. La tripulación ocupa sus puestos y el barco se integra en la pequeña flota de Bonnie. Al ver las filas de la Marina, la capitana decide cruzar el arrecife para atacar por detrás, aprovechando su menor calado sin eliminar el riesgo de daños.', ['42-002','42-013','42-015','42-017'])
history('Tripulación del Zampaolas','faccion','Lealtades antes de la batalla',
        'Ione prepara a sus compañeros para combatir y les dirige palabras de ánimo. Jack expresa su miedo a pelear contra su antigua Marina y recibe una promesa de protección. Poncelot e Ilikar la siguen al barco junto a los demás; Ojo Ausente vuelve a vigilar y Mugre baja a la cocina. Nox, expulsado según su propio relato, está entretanto con Tórtola buscando una patente de corso.', ['42-004','42-008','42-013'])
history('Marina','faccion','La armada ante Shiaru',
        'La Marina despliega desde el sur numerosos barcos de guerra y espera el avance de los piratas con dos filas escalonadas. Tórtola navega en el Invictus junto a Nox, que ha estudiado varios buques y colabora en la aproximación por el arrecife. El almirante coloca barcos menores delante del suyo y las primeras naves comienzan a avanzar y disparar. Todavía no hay un balance de la batalla.', ['42-004','42-016','42-019','42-020','42-021','42-023'])
history('Moneda pirata de Bonnie','objeto','Rayos y cambio de aspecto',
        'Bonnie aprieta la moneda de los capitanes piratas durante su discurso. Su cuerpo chisporrotea, sus ojos brillan azules y aparece un aspecto marcado por el rayo mientras se oscurece el cielo. Después prepara descargas desde el barco. La activación se observa, pero no explica la procedencia del objeto o todos sus límites.', ['42-012','42-018'])
history('Gorro de capitana de Ione','objeto','Una custodia para el final de la batalla',
        'Ante el miedo de Jack, Ione se quita el gorro de capitana y se lo entrega para que lo guarde. Le pide que se lo devuelva al terminar el combate y él acepta. El objeto convierte la promesa de protección en una tarea compartida, todavía sin devolución mostrada en este tramo.', ['42-008'], True,
        'Gorro de capitana que Ione confía a Jack antes de la batalla del Arrecife del Garfio.',
        'No confundirlo con el casco de Poncelot. La entrega no otorga a Jack el mando del Zampaolas.')
history('Fular de alas de mosca de Ione','objeto','Un agradecimiento de Poncelot',
        'Poncelot encarga y recoge un paquete antes de embarcar. Se lo entrega a Ione como agradecimiento por haberlo acogido y tratado como compañero. El regalo se describe como un fular transparente con vetas de alas de mosca; Ione se lo pone y abraza al gnomo. No se presentan propiedades mágicas ni una procedencia de Merlucilla III.', ['42-001','42-009'], True,
        'Fular transparente descrito con alas de mosca, regalado por Poncelot a Ione antes de la batalla.',
        'Descripción y material de lectura provisional; no establecer que proceda de la montura muerta del gnomo.')
history('Relámpago del Mar','objeto','La nave de Bonnie entre rayos',
        'El enorme barco de Bonnie forma con el Zampaolas y otras cinco naves la pequeña flota defensora de Shiaru. Bajo la tormenta adelanta a los barcos piratas y parece desprender rayos mientras Bonnie prepara chispas y ordena no malgastar munición. El relato lo llama Relámpago del Mar.', ['42-015','42-018'], True,
        'Enorme buque de Bonnie que participa en la defensa naval de Shiaru.',
        'Nombre leído en el pasaje del avance; no confundirlo con el Zampaolas ni atribuirle la reputación del Invictus.')
history('Invictus','objeto','La aproximación de Tórtola',
        'El Invictus navega hacia el norte con Tórtola y Nox a bordo mientras el resto de la armada forma ante los piratas. El director lo presenta como una nave nunca derrotada ni dañada. Tórtola ordena colocar barcos menores delante durante la aproximación por el arrecife. En sus niveles inferiores Nox encuentra una jaula con una figura humanoide encadenada, aún sin identificar.', ['42-019','42-020','42-021','42-022'], True,
        'Buque de Tórtola, presentado como nunca derrotado, donde Nox encuentra una jaula en los calabozos.',
        'La reputación de invicto no acredita invulnerabilidad mecánica. Su cautivo no queda identificado en el primer tramo.')
history('Pinky','personaje','Una silueta en los calabozos del Invictus',
        'Al bajar por el interior del Invictus, Nox encuentra una gran jaula vigilada por un marine que se marcha al comenzar los preparativos. Dentro hay una figura humanoide oscura y agachada, sujeta por enormes cadenas en los brazos. La primera visión no la identifica; el nombre Pinky procede del reconocimiento posterior en este capítulo. El aspecto inicial no establece por sí solo motivo o duración del cautiverio.', ['42-022'],
        note='Identidad integrada tras la identificación del bloque posterior; el relato de la primera visión conserva la incertidumbre de Nox.')

stages[0]['texto'] = stages[0]['texto'].replace('La ausencia del pequeño dragón alarma', 'La ausencia del ser de fuego al que llaman pequeño dragón alarma')
for entry in histories:
    if entry['nombre'] == 'Ilikar':
        entry['etapas'][0]['texto'] = entry['etapas'][0]['texto'].replace('que el pequeño dragón está apartado', 'que el ser de fuego al que llaman pequeño dragón está apartado')

delivery = dict(bloque=1, lectura_completa=True, primer_segmento='c000001', ultimo_segmento='c002155',
    etapas=stages, afirmaciones=facts,
    misiones=[
        'Defender Shiaru: Ione arma el Zampaolas y Bonnie reúne siete barcos piratas frente a una armada mayor. Empieza el combate sin resultado decidido en este tramo (42-002, 42-011–42-018, 42-023).',
        'Flanquear a la Marina: Ione ordena cruzar el arrecife para buscar la retaguardia; el paso puede dañar el casco y la maniobra aún continúa (42-017).',
        'Conseguir una patente de corso: Nox describe su trato con la Marina y colabora con Tórtola a bordo del Invictus, sin entrega documental mostrada (42-004, 42-019–42-021).',
        'Buscar aliados para cazar al dragón: Ilikar regresa a Shiaru con esa intención, pero se incorpora a la batalla y no obtiene aquí una aceptación de Ione o Poncelot (42-003).',
        'Proteger a Jack y conservar el gorro: Ione le promete apoyo y le confía el gorro hasta el final de la batalla; la devolución queda por comprobar (42-008).'
    ],
    preguntas=[
        '¿Qué ocurre con la figura humanoide encadenada que Nox encuentra en los calabozos del Invictus y por qué la transporta Tórtola? La silueta inicial no establece identidad ni especie (42-022).',
        '¿Obtendrá Nox la patente de corso que persigue y qué pretende al bajar a los calabozos después de anunciar que guiaría desde proa? Su presencia con la Marina no acredita todavía el resultado de su trato (42-004, 42-019–42-022).',
        '¿Conseguirá el Zampaolas cruzar el arrecife y flanquear a la Marina sin romper el casco? La orden y el movimiento inicial no prueban el éxito (42-017).',
        '¿Volverá Jack para devolver el gorro a Ione cuando termine la batalla? La promesa de protección no anticipa su supervivencia (42-008).'
    ],
    contradicciones=[
        'El director llama a Tórtola capitán y almirante durante la misma operación. El apelativo inicial Paloma parece un juego o variante; no se crea otra autoridad ni se resuelve por ello la identidad del Tórtola distinto referido en órdenes antiguas (42-004, 42-019–42-021).',
        'La mesa reconoce desintegrar en la luz verde de Tórtola, pero el director distingue el conocimiento de jugadores y personajes. No se atribuye automáticamente ese saber a Nox u otros viajeros (42-020).',
        'La patente de corso es el objetivo de Nox, la seguridad de Jack es una promesa y el flanqueo por el arrecife una maniobra iniciada: ninguna de esas formulaciones demuestra su resultado (42-004, 42-008, 42-017).',
        'El tigre embarcado es Merlucilla IV, distinto del tiburón Merlucilla V. Las bromas sobre objetos de matadragones no convierten sus materiales en trofeos de dragones verdaderos (42-013–42-014).',
        'La activación de la moneda y la transformación eléctrica de Bonnie se muestran; el origen, la maldición y los límites del poder no se explican por completo (42-012, 42-018).'
    ],
    nombres_dudosos=[
        'Sir Poncelot/Sir Ponce y variantes, Ione/Yone/Jones e Ilikar/Ilicar/Icar corresponden a los viajeros ya catalogados por continuidad de sus turnos (42-001–42-003, 42-008–42-009).',
        'Jacki/Jack es el exmarine del Zampaolas ya catalogado, por nombre, pasado y pertenencia al mismo grupo. No se crea una segunda persona por la variante de los subtítulos (42-006, 42-008, 42-013).',
        'El nombre cortado cloroalgo del dragón no basta para fijar una grafía o unir al dragón de Iktan con Clodidrax. Poncelot sigue siendo un aliado buscado, sin aceptación representada (42-003).',
        'Relámpago del Mar denomina el buque de Bonnie en el avance. Invictus es el de Tórtola; ambos permanecen separados del Zampaolas (42-018–42-019).',
        'Alice es un nombre mencionado en el encargo del paquete, sin identificación suficiente para nueva ficha. El fular no queda ligado materialmente a Merlucilla III (42-001, 42-009).',
        'La figura encadenada del Invictus no se nombra en su primera aparición. La identificación posterior con Pinky se integra en la ficha, manteniendo la incertidumbre de esa primera visión y sin crear otra identidad (42-022).',
        'El ser del barril de arena se vincula contextualmente a Cipo por su relación con Ilikar y su presencia posterior en el Zampaolas. Los viajeros lo llaman bebé dragón o demonio, sin identificarlo con el Dragón de Erendriel (42-007).'
    ],
    historias_entidades=histories)
(ROOT / 'borradores/42/entrega_1.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
print(f'Entrega 1: {len(facts)} afirmaciones validadas, {len(stages)} etapas, {sum(len(s["texto"].split()) for s in stages)} palabras y {len(histories)} propuestas de historia.')
