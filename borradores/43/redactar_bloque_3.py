"""Entrega del tramo final de 43, redactada tras lectura íntegra de sus 921 segmentos."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import validate_fact

ROWS = json.loads((ROOT / 'borradores/43/bloque_3_segmentos.json').read_text(encoding='utf-8'))
SOURCE = ROOT / 'xoltacan_subtitulos/subtitulos/43 - tSdmoZCWEZQ.es-orig.vtt'
facts = []


def fact(number, title, statement, start, end, cue_start, entities, limitation='', kind='hecho_confirmado'):
    cue = next(row for row in ROWS if row['inicio'] == cue_start)
    row = dict(id=f'43-{number}', titulo=title, tipo=kind, afirmacion=statement,
               inicio=start, fin=end, cita=cue['texto_original'],
               evidencia_cue=dict(inicio=cue['inicio'], fin=cue['fin'], texto=cue['texto_original']),
               entidades=entities, ambito='desenlace terrestre en la jungla del Garfio',
               conocedores=[], conocimiento_personaje='desconocido',
               nota_conocimiento='Acceso de Madame Oghma sin establecer en este pasaje.',
               confianza='lectura de subtítulos; audio no cotejado', limitacion=limitation)
    validate_fact(row, SOURCE)
    facts.append(row)


fact(201, 'Eleanor prepara el descenso de Lunaria con un golpe divino',
     'Mientras descienden, Eleanor guarda la espada y pone su símbolo en la frente de Lunaria, transformada en oso. Invoca la corona de Castilla y le ordena acabar con los enemigos. Busca entre los generales a la amenaza mayor. El director sitúa al grupo por delante de una formación de la Marina que está cediendo.',
     '01:22:34.560', '01:23:54.510', '01:23:12.080', ['Eleanor', 'Lunaria', 'Marina'],
     'La invocación de Castilla no corrige retroactivamente las declaraciones anteriores de Aragón ni fija una nueva nacionalidad. La caída se resuelve después.')
fact(202, 'La explosión en el mar interrumpe el combate y hace arder los tatuajes de Citlali',
     'Una explosión tremenda silencia momentáneamente el campo terrestre. Todos miran hacia el mar; Eleanor y Lunaria, aún en altura, ven una columna de fuego entre los barcos de guerra de la costa del Garfio. Al mismo tiempo, Citlali siente un dolor devastador en sus tatuajes, suelta las alpargatas y cae de rodillas gritando y arañándose.',
     '01:23:57.280', '01:26:01.350', '01:25:21.920', ['Citlali', 'Eleanor', 'Lunaria', 'El Garfio'],
     'La escena terrestre registra la explosión y la reacción de Citlali; no convierte a quienes miran desde la jungla en testigos de cada acción de Nox en el Invictus.')
fact(203, 'Una visión de Nox y el ser serpentino incita a Citlali a matar',
     'Citlali siente un vacío y revive una escena de agua que la ahoga y de Nox cayendo entre quienes se precipitan de los barcos. Intenta alcanzarlo sin poder. Tras un siseo, una criatura le toma el brazo y la mano como para ayudarla a llegar a él, y le susurra que use su poder y mate a todos. Ve los rostros de los marines y vuelve a escuchar la orden.',
     '01:26:01.360', '01:28:14.070', '01:27:37.320', ['Citlali', 'Nox', 'Entidad serpentina vinculada a Citlali', 'Marina'],
     'Es una experiencia de Citlali, no la recuperación física de Nox ni una prueba del nombre o naturaleza divina del interlocutor. No se identifica al ser con Set, el ojo-orbe o cualquier serpiente de otra escena.')
fact(204, 'Citlali cambia la curación por la absorción violenta de vida',
     'Citlali se levanta con los tatuajes brillando entre carmesí y verde, extendidos por casi todo su cuerpo. La voz le ordena matar y arrebatar juventud. Agarra a los marines por el cuello y absorbe su energía vital; sus manos y tatuajes brillan con mayor intensidad. El director muestra a Erandy que la anciana avanza ahora más deprisa y arroja a sus víctimas como despojos.',
     '01:28:17.920', '01:30:41.669', '01:29:48.480', ['Citlali', 'Erandy', 'Entidad serpentina vinculada a Citlali', 'Marina'],
     'La palabra curar al comienzo de la descripción no significa una curación beneficiosa para los marines: se narra explícitamente su drenaje. La voz es una incitación, no una regla universal del poder.')
fact(205, 'Erandy interpreta la explosión como presencia del dios solar y vuelve a atacar',
     'Erandy interpreta la explosión como si el propio dios del sol se presentara ante ella y la invitara a quemarlo todo. Con una sonrisa exaltada solicita gastar sus usos para lanzar otra bola de fuego contra un pelotón. El director admite la acción y describe a los marines saliendo por los aires; Erandy comienza a acusar el agotamiento de tanta magia.',
     '01:30:41.679', '01:33:30.350', '01:31:04.560', ['Erandy', 'Marina'],
     'La divinidad solar pertenece a la interpretación de Erandy. París y las comparaciones de los jugadores no añaden un destino o una aparición divina objetiva.', 'declaracion_personaje')
fact(206, 'El oso de Lunaria impacta con la energía de Eleanor',
     'Lunaria y Eleanor descienden desde cien pies y resuelven la caída del oso con un golpe divino. El resultado anunciado es de setenta y siete puntos de daño. El oso se ilumina, golpea el suelo y lanza por los aires a quienes lo rodean, desplazando también a Citlali. Lunaria abandona la forma de oso después del impacto; Molly permanece luchando en el terreno.',
     '01:33:33.920', '01:36:15.390', '01:34:32.119', ['Lunaria', 'Eleanor', 'Citlali', 'Molly', 'Marina'],
     'La narración confunde un vocativo al situar al jinete, pero las tiradas y turnos mantienen la combinación de Lunaria y Eleanor. No se presenta la cifra como daño sufrido por Lunaria ni como una muerte suya.')
fact(207, 'Eleanor aterroriza a los marines, pero falla su orden de arrodillarse',
     'Eleanor se acerca a los enemigos y muestra su aura de temor mientras los golpea con la espada. Algunos quedan aterrorizados e inmóviles ante ella. Dirige un conjuro de orden a un enemigo herido con la espada ante su rostro, pero el director confirma que supera la salvación y no se arrodilla.',
     '01:37:05.639', '01:39:18.870', '01:39:09.719', ['Eleanor', 'Marina'],
     'La resolución corrige la primera descripción de un retroceso por miedo. La rodilla inclinada sugerida inicialmente no se conserva como resultado del conjuro.')
fact(208, 'Los compañeros ven rejuvenecer a Citlali y envejecer a sus víctimas',
     'Los marines están aterrados por la caballera, las bolas de fuego y la violencia de Citlali. Mientras ella oye los siseos como algo cada vez más agradable, pasa delante de Lunaria, Eleanor y Erandy. Los demás ven que ya no parece una anciana: está más joven, mientras los restos que deja en el suelo se ven arrugados y envejecidos.',
     '01:39:22.000', '01:41:50.390', '01:41:37.520', ['Citlali', 'Lunaria', 'Eleanor', 'Erandy', 'Entidad serpentina vinculada a Citlali', 'Marina'],
     'En una frase el reconocimiento escribe piratas para los restos, pero la secuencia continua describe el ataque a los marines. No se inventa una edad exacta ni duración permanente del rejuvenecimiento.')
fact(209, 'Citlali mata al general mientras los marines huyen hacia las trampas',
     'Citlali busca a quien aún da órdenes y atraviesa las filas para agarrarlo por el cuello. Le reprocha que todos le arrebataron a su hijo y vuelve a absorber su energía. Una carta del chat añade furia como la de un bárbaro. El director confirma la muerte del general. Otros marines retroceden y algunos gritan al caer en trampas de la jungla.',
     '01:41:50.400', '01:44:54.510', '01:44:13.239', ['Citlali', 'Nox', 'Marina', 'El Garfio'],
     'El cargo es descriptivo y el general no recibe un nombre. La acusación de Citlali expresa su duelo y rabia, sin probar que este oficial causara personalmente lo ocurrido a Nox. La carta es una ayuda de juego, no un nuevo origen biográfico de sus poderes.')
fact(210, 'Erandy recupera magia por el chat y lanza fuego cerca de sus aliados',
     'Aunque está cansada, Erandy siente una última chispa y recupera por intervención del chat un espacio de conjuro de tercer nivel para lanzar una bola de fuego. Sigue invitando a los enemigos a recibir el abrazo del dios del sol y hace estallar el conjuro. La discusión de alcance incluye a aliados y a Citlali, y el director exige las salvaciones correspondientes.',
     '01:44:54.520', '01:47:48.589', '01:45:24.199', ['Erandy', 'Citlali', 'Marina'],
     'La chispa se concede explícitamente por el chat. No se presenta como restauración ilimitada ni como prueba objetiva de favor divino; no se infiere daño individual de quienes no muestran su tirada.')
fact(211, 'Eleanor se cura al atravesar el fuego',
     'Eleanor levanta la mano hacia la bola de fuego que cae, representa tomar una parte de la llama y llevarla al pecho, y se dirige sonriendo al enemigo que queda vivo. El director resuelve una recuperación de treinta y cinco puntos de vida y confirma que vuelve a estar completamente curada.',
     '01:47:54.800', '01:48:36.709', '01:48:32.440', ['Eleanor', 'Erandy'],
     'La curación se resuelve en su turno; la representación de coger fuego no demuestra una capacidad universal de absorber cualquier conjuro ni inmunidad general al fuego.')
fact(212, 'Lunaria protege a Citlali y Etley antes de lanzar otra bola de fuego',
     'Ya fuera de la forma de oso, Lunaria propone combinar sus puntos de hechicería con los usos de una dote del dragón cromático para excluir del daño a Citlali y a la cría llamada pollo. El director acepta la propuesta. Unas alas espectrales de dragón rodean a ambos y los protegen durante la explosión.',
     '01:48:39.760', '01:51:11.910', '01:50:58.840', ['Lunaria', 'Citlali', 'Etley', 'Marina'],
     'La combinación se admite para esta representación concreta, sin convertirla en una regla general. La protección no prueba que Citlali no hubiera recibido quemaduras del fuego anterior.')
fact(213, 'La caída de los generales rompe la resistencia terrestre',
     'Molly y los piratas combaten por los laterales, junto a la jungla, contra los marines que intentan huir. Eleanor imbuye su espada con la energía usada en el oso y parte a un general por la mitad. El director confirma que Citlali ha matado a otro mando y que las bolas de fuego han deshecho la formación. Los supervivientes sueltan las armas y corren; los piratas persiguen a quienes huyen hacia la jungla.',
     '01:51:11.920', '01:53:22.189', '01:53:04.239', ['Molly', 'Eleanor', 'Citlali', 'Erandy', 'Lunaria', 'Marina', 'El Garfio'],
     'Bonnie aparece como vocativo aislado del director en la escena terrestre; se mantiene la continuidad de Molly, sin transportar a Bonnie desde el combate naval. No se establece la muerte de todos los miembros de la Marina de la isla.')
fact(214, 'Eleanor retiene a un marine para Citlali sin rematarlo ella',
     'Eleanor agarra por el cuello y la nuca al marine que tiene delante para mantenerlo quieto. Explica que reconoce la venganza en los ojos de Citlali, siente que algo va mal y decide no matarlo ella. El enemigo queda retenido frente a la joven Mamá.',
     '01:53:22.199', '01:54:11.430', '01:53:47.320', ['Eleanor', 'Citlali', 'Marina'],
     'No es un rescate del marine ni una orden de rendición aceptada. Eleanor lo inmoviliza y deja su siguiente destino a Citlali.')
fact(215, 'Citlali consume la vida del marine retenido',
     'Citlali aparta las alas que la protegían; su ropa aún tiene fuego y algunas partes de su piel están quemadas, aunque no manifiesta dolor. Coloca una mano en el pecho del marine que retiene Eleanor y sigue absorbiéndolo hasta dejarlo envejecido, consumido y reducido a huesos y piel. Lo suelta como un despojo.',
     '01:54:11.440', '01:55:28.830', '01:55:18.920', ['Citlali', 'Eleanor', 'Lunaria', 'Marina'],
     'La ausencia de una queja no significa invulnerabilidad al fuego ni curación automática de las quemaduras. No se asignan una edad ni una cantidad numérica de energía robada.')
fact(216, 'Los piratas celebran la victoria y Molly llega herida',
     'El director da por terminado el combate: la mayoría de los marines han caído y los pocos que quedan huyen. Los piratas celebran mientras los combatientes recuperan el aliento. Molly se acerca cansada, respira con dificultad y tiene heridas, disparos y manchas de sangre. Expresa su sorpresa por el oso gigante y la cría arrojada, y se detiene al mirar a Citlali.',
     '01:55:31.560', '01:57:06.030', '01:56:19.159', ['Molly', 'Citlali', 'Lunaria', 'Etley', 'Marina'],
     'La victoria se limita al frente terrestre mostrado. Los gritos de haber acabado con todos se matizan con los supervivientes que el propio director describe huyendo.')
fact(217, 'La caja musical acompaña el duelo de Citlali por Nox',
     'Citlali vuelve la mirada hacia la explosión con su rostro rejuvenecido lleno de lágrimas. Saca una caja musical de la falda y dice que Nox se ha ido. Mientras mueve la caja no puede dejar de llorar. Mira a Molly; el director explica que esta comprende la mirada de quien acaba de perder a su hijo. Molly abre los ojos, deja caer el arma y queda inmóvil.',
     '01:57:06.040', '01:58:56.470', '01:57:51.760', ['Citlali', 'Nox', 'Molly', 'Caja musical de Citlali'],
     'La escena presenta el duelo y la comprensión de Molly; no muestra el cuerpo de Nox ni explica el origen de la caja. Las réplicas sobre que Nox siempre vuelve no anulan ese duelo.', 'declaracion_personaje')
fact(218, 'Eleanor comprueba el agotamiento extremo de Erandy',
     'Eleanor se gira para comprobar cómo está Erandy. La escudera permanece con la cabeza baja, temblando y con la mirada fija en el suelo. Su jugadora describe que el cuerpo está agotado y en shock, sostenido apenas por su voluntad y su entrega al dios; si la movieran, se desplomaría. Lunaria y Etley no comprenden bien el duelo de Citlali, aunque perciben que algo grave ocurre.',
     '01:58:56.480', '02:01:24.790', '02:00:34.599', ['Eleanor', 'Erandy', 'Lunaria', 'Etley', 'Citlali'],
     'No se declara la muerte de Erandy ni se describe que ya la hayan movido o trasladado. Las comparaciones con otras obras son referencias de la jugadora, no identidades de campaña.')
fact(219, 'Citlali ve el Zampaolas detenido en la costa y trata de alcanzarlo',
     'Citlali observa hacia la costa por encima de los árboles y ve velas negras y el pabellón del Zampaolas. El barco avanza como a la deriva y se detiene meciéndose, descrito como varado al este. Ella intenta ir hacia él con la esperanza de volver a ver a Amaru, recordando sus trenzas, el olor a ron y sus malos chistes. Sus piernas flaquean, pero insiste en caminar o arrastrarse. Los demás también pueden ver la bandera y parte de las velas. La sesión no narra un encuentro con quienes van a bordo.',
     '02:01:24.800', '02:05:14.549', '02:02:40.079', ['Citlali', 'Nox', 'Zampaolas', 'El Garfio'],
     'El duelo por Nox y la memoria de Amaru se enlazan expresamente mediante sus trenzas, ron, chistes y el contraste entre ni?o y hombre: Citlali reconoce al hijo perdido en Nox. No se cuenta c?mo sobrevivi? o sali? del cofre ni se reconstruye su crianza. Varado es la descripción visual desde la jungla, no una inspección del casco ni prueba de otro naufragio. La corrección de Kuroto a Xoltacan al cerrar no traslada la escena a otra campaña.')
fact(220, 'El ser serpentino activa un altar con los símbolos de Citlali',
     'En un epílogo separado de los personajes, el director vuelve al ser que lleva tiempo hablando con Mamá. Se acerca a una especie de altar y pasa la mano por encima. Se iluminan marcas y símbolos que son exactamente los que Citlali tiene en el cuerpo. La serpiente sisea que ya es la hora, y termina el capítulo.',
     '02:05:14.559', '02:06:16.559', '02:05:45.599', ['Entidad serpentina vinculada a Citlali', 'Altar de los s?mbolos de Citlali', 'Citlali'],
     'No se indica dónde está el altar ni qué acontecimiento anuncia la frase. El epílogo es información para los espectadores, sin acceso de los combatientes establecido. No identifica al ser por nombre ni lo equipara automáticamente con otras serpientes.')

stages = [
    dict(titulo='La explosión y la voz', texto='Eleanor prepara el descenso de Lunaria colocando su símbolo sobre la frente del oso, mientras la resistencia de la Marina empieza a ceder. Una explosión enorme interrumpe el combate. Desde la altura ven una columna de fuego alzarse entre los barcos de la costa del Garfio. Citlali cae de rodillas: sus tatuajes le duelen como si la piel ardiera. Siente un vacío y una visión le devuelve a Nox cayendo entre el agua y los cuerpos. Trata de alcanzarlo sin conseguirlo. Un ser se aproxima entre siseos, le toma la mano y le ordena usar su poder para matar a los marines. Citlali se levanta con los tatuajes encendidos en carmesí y verde, agarra a sus enemigos por el cuello y absorbe su vida. Erandy interpreta la explosión como la presencia de su dios solar y vuelve a lanzar fuego, extasiada pero cada vez más agotada.', referencias=['43-201', '43-202', '43-203', '43-204', '43-205']),
    dict(titulo='La formación de la Marina se rompe', texto='Lunaria y Eleanor completan su caída desde cien pies. El oso se ilumina con el golpe divino e impacta contra el suelo, haciendo volar a los enemigos y desplazando a Citlali. Lunaria recupera después su forma habitual. Eleanor avanza con un aura que aterroriza a los marines, aunque uno resiste su orden de arrodillarse. Los compañeros ven pasar a Citlali rejuvenecida entre víctimas consumidas y arrugadas. Ella busca al general que aún intenta organizar la resistencia, lo acusa de haberle arrebatado a su hijo y lo mata absorbiéndolo. Algunos fugitivos caen en las trampas de la jungla. Erandy recibe del chat una última chispa de magia y lanza otra bola de fuego. Eleanor se cura y Lunaria prepara su propia explosión, cubriendo a Citlali y a Etley con alas espectrales de dragón para protegerlos.', referencias=['43-206', '43-207', '43-208', '43-209', '43-210', '43-211', '43-212']),
    dict(titulo='La victoria deja un vacío', texto='Molly y los piratas combaten por los flancos. Eleanor acaba con otro general y los supervivientes de la Marina sueltan las armas y huyen. Después retiene a un marine ante Citlali, que vuelve a consumir su vida hasta dejarlo reducido a huesos y piel. La batalla termina y los piratas celebran. Molly, herida y exhausta, se acerca a los compañeros. Citlali mira hacia el fuego del mar con lágrimas sobre su rostro joven. Saca una caja musical y dice que Nox se ha ido. La mirada basta para que Molly comprenda su pérdida: deja caer el arma y queda inmóvil. Eleanor comprueba el estado de Erandy, que apenas se mantiene en pie, temblando y con la mirada perdida. Lunaria y la cría no entienden del todo lo sucedido, pero perciben el dolor de quienes los rodean.', referencias=['43-213', '43-214', '43-215', '43-216', '43-217', '43-218']),
    dict(titulo='El barco en la costa y los símbolos', texto='Por encima de los árboles, Citlali distingue las velas negras y la bandera del Zampaolas. Lo ve avanzar junto a la costa y detenerse al este. Intenta llegar con la esperanza de volver a ver a Amaru, evocando las trenzas, el olor a ron y los malos chistes de Nox. Sus piernas flaquean y trata de seguir incluso arrastrándose. Los compañeros también alcanzan a ver parte del barco, pero no se narra el encuentro. El relato se aparta entonces de ellos y vuelve al ser serpentino que habla con Citlali. Ante una especie de altar, pasa la mano sobre unas marcas y las enciende: son exactamente los símbolos de su cuerpo. La serpiente anuncia que ya es la hora.', referencias=['43-219', '43-220']),
]


def history(name, kind, title, text, references, new=False, description='', note=''):
    return dict(nombre=name, tipo=kind, nueva=new, descripcion=description, nota=note,
                etapas=[dict(titulo=title, texto=text, referencias=references)])


histories = [
    history('Citlali', 'personaje', 'La pérdida, el drenaje y los símbolos', 'La explosión marítima provoca un dolor devastador en los tatuajes de Citlali y una visión de Nox cayendo entre el agua. El ser que la acompaña le ordena matar y arrebatar juventud. Citlali drena a los marines, rejuvenece ante sus compañeros y mata a un general entre reproches por la pérdida de su hijo. Después saca una caja musical y llora a Nox; Molly comprende su dolor. Al ver el Zampaolas intenta llegar a la costa, pero las piernas le flaquean. El epílogo revela al público que los símbolos de su cuerpo coinciden con los que el ser activa en un altar.', ['43-202', '43-203', '43-204', '43-208', '43-209', '43-215', '43-217', '43-219', '43-220']),
    history('Nox', 'personaje', 'La pérdida vivida desde la jungla', 'El estallido naval se contempla desde el frente terrestre. Citlali ve a Nox cayendo en una experiencia acompañada por el dolor de sus tatuajes y la intervención de un ser serpentino. Después dice que se ha ido y lo llora como a un hijo, mientras Molly queda conmocionada. El Zampaolas detenido en la costa le devuelve una esperanza desesperada de encontrarlo; la sesión no representa ese encuentro ni una recuperación del cuerpo.', ['43-202', '43-203', '43-209', '43-217', '43-219']),
    history('Eleanor', 'personaje', 'El impacto y los últimos mandos', 'Eleanor imbuye el descenso de Lunaria en forma de oso con un golpe divino. Tras el impacto aterroriza a algunos marines con su aura, aunque su orden de arrodillarse es resistida. Se cura antes de acabar con un general. Luego inmoviliza a un marine y deja que Citlali lo drene, preocupada por lo que ve en ella. Al terminar comprueba el agotamiento extremo de Erandy.', ['43-201', '43-206', '43-207', '43-211', '43-213', '43-214', '43-218']),
    history('Lunaria', 'personaje', 'Del oso luminoso a las alas protectoras', 'Lunaria cae como un gran oso bajo la energía divina de Eleanor, impacta en la formación y recupera después su forma habitual. Combina sus recursos de hechicería y una dote cromática para que unas alas espectrales protejan a Citlali y Etley mientras lanza otra bola de fuego. Al acabar la batalla no comprende del todo lo ocurrido a Nox, pero ve el llanto de Citlali.', ['43-206', '43-212', '43-218']),
    history('Erandy', 'personaje', 'El fuego del dios y el agotamiento', 'Erandy interpreta la columna de fuego como la presencia de su dios solar y transforma esa creencia en una nueva ofensiva incendiaria. Recupera por ayuda del chat un último espacio de conjuro y vuelve a lanzar fuego contra los marines. Terminada la batalla queda temblando, agotada y apenas sostenida por su voluntad y devoción, mientras Eleanor comprueba cómo está.', ['43-205', '43-210', '43-218']),
    history('Molly', 'personaje', 'La victoria terrestre y la noticia de Nox', 'Molly sigue luchando en el frente de la jungla y recorre los flancos con los piratas durante la retirada de los marines. Al terminar se acerca herida, ensangrentada y sin aliento. La expresión de Citlali, que llora a Nox como a un hijo, la deja inmóvil y hace que se le caiga el arma.', ['43-206', '43-213', '43-216', '43-217']),
    history('Etley', 'personaje', 'Entre las alas y el duelo', 'Lunaria protege a la cría de Citlali, llamada pollo durante la batalla, con alas espectrales al preparar su explosión de fuego. La cría sobrevive al combate mostrado y al terminar permanece agazapada, sin entender la pérdida pero percibiendo que algo grave les ha ocurrido a sus compañeros.', ['43-212', '43-216', '43-218']),
    history('Marina', 'faccion', 'La derrota del frente de la jungla', 'La formación terrestre pierde hombres y mandos ante el impacto del oso, las bolas de fuego y el drenaje de Citlali. Eleanor y Citlali eliminan a los últimos generales; los supervivientes sueltan las armas e intentan huir, perseguidos por piratas o atrapados en la jungla. La victoria proclamada por sus adversarios se limita a esta batalla, sin demostrar la eliminación de toda la organización.', ['43-206', '43-209', '43-210', '43-213', '43-215', '43-216']),
    history('El Garfio', 'lugar', 'La columna de fuego sobre la batalla', 'Quienes combaten en la jungla del Garfio ven levantarse una columna de fuego entre los barcos de la costa. El combate terrestre continúa hasta que los marines pierden a sus mandos y huyen hacia las trampas de la vegetación. Tras la victoria, Citlali y sus compañeros distinguen al Zampaolas detenido en la costa oriental por encima de los árboles.', ['43-202', '43-209', '43-213', '43-216', '43-219']),
    history('Zampaolas', 'objeto', 'Visto desde la jungla', 'Después del combate terrestre, Citlali reconoce por encima de los árboles sus velas negras y su bandera. El barco parece ir a la deriva junto a la costa y se detiene, meciéndose como varado al este. Citlali intenta alcanzarlo esperando encontrar a Nox, sin que se muestre el encuentro ni una inspección de la nave.', ['43-219']),
    history('Entidad serpentina vinculada a Citlali', 'personaje', 'La orden de matar y el altar encendido', 'El ser se aproxima durante la visión en que Citlali intenta alcanzar a Nox y le toma la mano. Le ordena matar a los marines y quitarles la juventud; su siseo se vuelve agradable mientras ella drena a sus enemigos. En el epílogo, la misma figura se acerca a un altar y enciende símbolos idénticos a los tatuajes de Citlali, anunciando que ya es la hora.', ['43-203', '43-204', '43-208', '43-220'], True, 'Ser serpentino que habla con Citlali, la incita a drenar vida y activa un altar vinculado a sus tatuajes.', 'Identidad descriptiva sin nombre propio ni naturaleza divina confirmada. La continuidad del interlocutor y el epílogo no identifica automáticamente a todas las serpientes de visiones previas con él.'),
    history('Altar de los s?mbolos de Citlali', 'objeto', 'Los símbolos de Citlali', 'El epílogo muestra una especie de altar al que se acerca el ser que habla con Citlali. Al pasar la mano sobre él enciende marcas y símbolos exactamente iguales a los de su cuerpo. La localización y la función completa del altar no se revelan.', ['43-220'], True, 'Altar de localización no revelada cuyos símbolos coinciden con los tatuajes de Citlali.', 'Se clasifica como lugar de la escena final, sin coordenadas ni identificación con ningún templo anterior. El acceso de los personajes a esta imagen no está establecido.'),
    history('Caja musical de Citlali', 'objeto', 'La música junto al llanto', 'Terminada la batalla, Citlali saca de la falda una caja musical y la mueve mientras dice que Nox se ha ido. Las lágrimas continúan y su mirada hace comprender a Molly la pérdida que siente. La escena no explica de dónde procede el objeto ni qué melodía reproduce.', ['43-217'], True, 'Caja musical que Citlali lleva consigo y saca durante su duelo por Nox.', 'No se inventa procedencia, propietario anterior, poderes mágicos ni una canción concreta.'),
]

document = dict(bloque=3, lectura_completa=True, primer_segmento='c003685', ultimo_segmento='c005525',
    etapas=stages, afirmaciones=facts,
    misiones=[
        'Derrotar a la Marina en el frente terrestre del Garfio: caen los mandos y la mayoría de los soldados; los pocos supervivientes huyen y los piratas celebran la victoria. No equivale a eliminar toda la Marina de la isla (43-206–43-216).',
        'Proteger a la cría de Citlali: Lunaria cubre a Etley y a Citlali con alas espectrales durante su ataque de fuego. La cría permanece viva en el cierre terrestre (43-212, 43-216, 43-218).',
        'Llegar al Zampaolas: Citlali ve sus velas y su pabellón hacia la costa oriental e intenta caminar o arrastrarse hasta él, esperando encontrar a Nox. La sesión se corta antes del encuentro (43-219).',
        'Comprender el vínculo de Citlali con el ser serpentino: se ven la incitación al drenaje, el rejuvenecimiento y la coincidencia de los símbolos del altar con sus tatuajes, sin revelar nombre o propósito completo (43-203–43-204, 43-208, 43-220).',
    ],
    preguntas=[
        '¿Quién es el ser serpentino y qué anuncia con «ya es la hora»? Incita a Citlali a quitar juventud y activa símbolos iguales a sus tatuajes, sin revelar su nombre ni su plan (43-203–43-204, 43-220).',
        '¿Dónde está el altar de símbolos idénticos a los de Citlali y qué hace al activarse? El epílogo no lo localiza ni muestra la consecuencia de encenderlo (43-220).',
        '¿Qué encuentra Citlali cuando llegue al Zampaolas? Su visión y su duelo por Nox no sustituyen el encuentro con los tripulantes, que no se representa en esta sesión (43-217, 43-219).',
        '¿Cómo evolucionan el drenaje, el rejuvenecimiento y las quemaduras de Citlali tras la batalla? Se ve el cambio físico y la violencia, sin fijar una edad final, duración o recuperación posterior (43-208–43-209, 43-215).',
        '¿Cómo se recupera Erandy de su agotamiento extremo? Eleanor comprueba su estado, pero la sesión no narra descanso, curación o traslado de la escudera (43-218).',
    ],
    contradicciones=[
        'La visión de Citlali sobre Nox y el dolor de sus tatuajes se presentan como experiencia suya. Su duelo y la reacción de Molly no añaden una recuperación física del cuerpo de Nox (43-202–43-203, 43-217).',
        'Erandy cree ver al dios del sol en la explosión; el director no confirma una aparición divina. La recuperación de un espacio de conjuro se atribuye expresamente al chat (43-205, 43-210).',
        'La narración rectifica la primera reacción al miedo: los afectados quedan aterrados sin moverse, y el enemigo al que Eleanor dirige la orden supera su salvación y no se arrodilla (43-207).',
        'Los restos arrugados reciben una vez la palabra piratas en subtítulos, pero la escena continua y las intervenciones anteriores y posteriores describen marines drenados por Citlali (43-204, 43-208–43-209).',
        'Molly sigue en el combate terrestre. Los vocativos aislados Bonnie o Mori no justifican traer a Bonnie a la jungla desde la batalla naval; conservar continuidad y cautela de reconocimiento (43-206, 43-213, 43-216–43-217).',
        'Los gritos de haber acabado con todos los marines conviven con una descripción explícita de algunos que huyen. La victoria no demuestra una extinción de la organización (43-213, 43-216).',
        'El Zampaolas se describe como varado desde la jungla. Sin una inspección, esto no confirma un nuevo naufragio ni modifica por sí solo la descripción de la costa del capítulo 42 (43-219).',
        'El epílogo del altar es para los espectadores. Los personajes no obtienen automáticamente esos conocimientos y el desliz verbal Kuroto al despedir la escena no cambia la campaña (43-219–43-220).',
    ],
    nombres_dudosos=[
        'Mamá, mama, Citiali, Sitlali y Citlali corresponden a Citlali por continuidad. No confundir sus marcas con los tatuajes de Nox ni crear una persona distinta al rejuvenecer (43-202–43-204, 43-208, 43-217).',
        'Luna es Lunaria, la misma kender que actúa en forma de oso y luego usa alas espectrales de dragón. No se identifica con el dios del sol ni con una criatura nueva por cada transformación (43-206, 43-212).',
        'Elianor, El honor y Eleanor designan a la caballera; Erandi, Andy y Erandy a su escudera. El vocativo aislado Erandy al hablar del jinete tras el impacto no intercambia sus turnos ni sus identidades (43-201, 43-206–43-207, 43-211, 43-218).',
        'Pollo o pollito designan aquí la cría de Citlali, Etley, según continuidad cotejada con el bloque anterior. No es Armin ni el oso de Lunaria (43-212, 43-216, 43-218).',
        'Amaru aparece en el recuerdo de Citlali ligado a la esperanza de reencontrar a Nox. Se conserva el apelativo contextual sin imponer una grafía o identidad civil no verificada (43-219).',
        'El ser del epílogo es el interlocutor serpentino de Citlali. No recibe nombre ni identificación explícita con Set, otras serpientes, el orbe de Nox o las figuras de otras campañas (43-203, 43-220).',
    ], historias_entidades=histories)

path = ROOT / 'borradores/43/entrega_3.json'
path.write_text(json.dumps(document, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'{len(facts)} evidencias verificadas; {len(histories)} historias; {sum(len(s["texto"].split()) for s in stages)} palabras de relato; 921 segmentos leídos.')
