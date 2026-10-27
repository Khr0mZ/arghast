"""Entrega editorial del primer bloque íntegro del capítulo 43 de Xoltacan."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import validate_fact

rows = json.loads((ROOT / 'borradores/43/bloque_1_segmentos.json').read_text(encoding='utf-8'))
source = ROOT / 'xoltacan_subtitulos/subtitulos/43 - tSdmoZCWEZQ.es-orig.vtt'
facts = []

def fact(a, b, anchor, title, statement, names, kind='hecho_confirmado', limit=''):
    cue = rows[anchor]
    item = dict(id=f'43-{len(facts)+1:03d}', titulo=title, tipo=kind,
                afirmacion=statement, inicio=rows[a]['inicio'], fin=rows[b]['fin'],
                cita=cue['texto_original'],
                evidencia_cue=dict(inicio=cue['inicio'], fin=cue['fin'], texto=cue['texto_original']),
                entidades=names, ambito='preparativos y comienzo del frente terrestre del Garfio',
                conocedores=[], conocimiento_personaje='desconocido',
                nota_conocimiento='Acceso de Madame Oghma sin establecer en este pasaje.',
                confianza='lectura de subtítulos; audio no cotejado', limitacion=limit)
    validate_fact(item, source)
    facts.append(item)

fact(0,9,7,'La sesión comienza al mismo tiempo que el capítulo naval',
     'El director sitúa el comienzo de esta sesión en el mismo momento en que empezó la partida del grupo anterior. El frente terrestre de la defensa del Garfio se presenta así en paralelo al inicio del capítulo naval, antes de conocer en escena todos sus resultados.',
     ['Shiaru','El Garfio'], 'explicacion_director',
     'La numeración de los capítulos no demuestra que toda esta acción suceda después del final del 42. No se trasladan sus muertes, decisiones o ausencias al inicio del 43.')
fact(15,73,23,'Erandy y Eleanor se preparan para la defensa terrestre',
     'Erandy relata que ella y Eleanor, tras conocer la amenaza de los chaquetas azules, hablaron en la taberna con Bonnie y Molly y pensaron en colocar trampas. Entiende que Molly encabeza el frente terrestre. Eleanor recuerda sus entrenamientos y que un enano azul anunciando el fin le hizo conocer el peligro, tras lo cual fue con su escudera a hablar con Bonnie e inspeccionar el punto que debían proteger.',
     ['Erandy','Eleanor','Bonnie','Molly','Marina','Shiaru'], 'declaracion_personaje',
     'El enano del repaso no queda nombrado; la apariencia y el cartel no bastan para crear o asignar una identidad. Los preparativos se cuentan como contexto de lo sucedido entre sesiones.')
fact(83,117,90,'Citlali recuerda la caja de música y huye de Iktan con la cría',
     'Citlali relata que permaneció en Iktan cuidando al pequeño hasta su recuperación y que los recuerdos volvieron a impedirle dormir. Encontró una caja de música; su melodía le recordó a sus hijos y a Nox. Sintió un dolor intenso y vio algo extraño en la piel. Interpretando que algo iba mal, tomó a la cría y echó a correr por la jungla. El director incorpora al pequeño a la escena, aclarando que aún no ataca.',
     ['Citlali','Etley','Nox','Iktan','Caja de música de Citlali'], 'declaracion_personaje',
     'El repaso no identifica el mecanismo o la causa del dolor. El recuerdo de Nox y la intuición maternal no prueban su muerte ni fijan una hora con respecto al desenlace del capítulo 42. Las bromas sobre usar al pequeño de escudo no representan que lo hagan aquí.')
fact(128,146,135,'Lunaria explora el poblado y busca respuestas',
     'Lunaria, llamada Luna, cuenta que ha recorrido el poblado que desconocía y preguntado a sus habitantes y a la chamana. Se sitúa ahora en la jungla después de sus insistentes preguntas.',
     ['Lunaria','Iktan'], 'declaracion_personaje',
     'El lugar se identifica contextualmente con Iktan por la continuidad del capítulo anterior de su grupo. No se expone una respuesta concreta de la chamana ni se atribuye un conocimiento nuevo a Luna.')
fact(148,179,170,'Las defensas de la jungla ya han sido inspeccionadas',
     'El director recuerda que Molly y Bonnie colaboraban para proteger Shiaru y que la exmarina advirtió del ataque tras su destitución. Molly ha llevado a Erandy y Eleanor al punto defensivo: hay cuerdas, trampas y combatientes escondidos para disparar desde la jungla. Después de revisar el despliegue vuelven al poblado para recibir las últimas órdenes.',
     ['Molly','Bonnie','Erandy','Eleanor','Shiaru','Marina','El Garfio'], 'explicacion_director',
     'La colaboración y la destitución se recuerdan como antecedentes. El pasaje no nombra las ruinas del capítulo 36 y no basta para identificar ese punto con su ocupación definitiva.')
fact(181,228,205,'Los habitantes se concentran en Shiaru',
     'La plaza de Shiaru reúne a los defensores. Gobs guarda una sierra y otras herramientas en su bolsa; Armin lleva dos enormes mazas. Liz y sus compañeras preparan armas de fuego, entre ellas una escopeta y un rifle largo. Ione, Ilikar y Sir Poncelot están con la tripulación del Zampaolas mientras Bonnie pronuncia su discurso.',
     ['Shiaru','Gobs','Armin','Liz','Ione','Ilikar','Sir Poncelot','Tripulación del Zampaolas','Bonnie'],
     limit='La presencia de los viajeros corresponde a la concentración anterior a la batalla naval, no confirma su supervivencia después del capítulo 42. Las comparaciones con Frankenstein describen humorísticamente a Gobs y no acreditan una operación realizada aquí.')
fact(229,245,230,'La moneda de Bonnie convoca la tormenta de la partida',
     'Bonnie sostiene la moneda de los reyes piratas. Empieza a brillar y de ella salen rayos que la envuelven; el director la presenta como una de las cinco reinas piratas. Tras su grito, los piratas corren a los muelles y unas nubes negras levantan una tormenta atribuida a su poder.',
     ['Bonnie','Moneda pirata de Bonnie','Cinco reyes piratas','Shiaru'],
     limit='Es la preparación compartida con el comienzo del capítulo 42, vista desde el otro grupo. No se cuentan dos activaciones distintas ni se describe un nuevo origen de la moneda.')
fact(247,262,251,'Liz y otros defensores permanecen tras barricadas',
     'Después de la marcha de los barcos quedan pocos defensores en Shiaru. Liz y sus mujeres se reparten por las esquinas con rifles y barricadas. Otros piratas de movilidad reducida permanecen en posiciones estables para defender el poblado.',
     ['Liz','Shiaru'],
     limit='Las exageraciones sobre el número de patas de palo no fijan un censo o diagnósticos. La escena no describe todavía un ataque contra esas barricadas.')
fact(267,328,321,'Erandy protege a Eleanor antes de marchar',
     'Molly llama a Eleanor para partir. Erandy pide un momento y posa la mano sobre el hombro de su señora, invocando la virtud y la calidez del Sol. En la mesa se establece una protección de ocho horas que, al caer a cero puntos de vida, permite quedar con uno.',
     ['Erandy','Eleanor','Molly'],
     limit='El nombre inglés del hechizo se oye de forma incompleta. Se conserva el efecto explicado en la mesa, sin presentarlo como inmortalidad ni como una activación ya consumida al recibir daño.')
fact(329,357,336,'Molly conduce a unos veinte piratas hacia el embudo',
     'Molly muestra a Eleanor un grupo de aproximadamente veinte piratas y reconoce la diferencia con los soldados de la Marina en la que sirvió. Aunque están decididos, su preparación es deficiente. Ordena marchar por la jungla para defender un embudo e impedir que el enemigo llegue a Shiaru.',
     ['Molly','Eleanor','Erandy','Shiaru','El Garfio','Marina'],
     limit='La cifra se plantea como aproximación narrativa. No indica el número de supervivientes al terminar el combate ni vuelve a otorgar a Molly un cargo vigente en la Marina.')
fact(384,443,436,'El malestar de Citlali la lleva a pedir ayuda a Luna',
     'Mientras corre, Citlali vuelve a sentir que algo va mal y un pinchazo en la cabeza. Encuentra a Lunaria recogiendo hierbas que no identifica bien y llega con la cría medio dormida, arrastrada del ala. Luna le ofrece un té, pero Citlali insiste en que necesitan llegar a Shiaru cuanto antes y le pide ayuda.',
     ['Citlali','Etley','Lunaria','Shiaru'],
     limit='La intuición no identifica el peligro o el estado de Nox. Recoger hierbas y proponer un té no demuestra un conocimiento botánico seguro ni que llegue a administrar una infusión.')
fact(444,466,448,'Luna se transforma en oso para transportar a Citlali',
     'Para acelerar el viaje, Luna se transforma en oso. Antes ata una cuerda a la cría, después la sujeta con los dientes y lleva a Citlali encima mientras el pequeño sigue arrastrado y corre como puede detrás.',
     ['Lunaria','Citlali','Etley'],
     limit='La transformación corresponde a Lunaria, no a Erandy. La narración describe un transporte incómodo; no comunica en este intervalo heridas, muerte o abandono de la cría.')
fact(468,511,478,'Citlali tiene una visión de un pirata y de la batalla bajo el agua',
     'Mientras monta al oso, Citlali tiene otra visión. Ve de espaldas a un pirata con adornos en el pelo y aspecto desaliñado que empieza a girarse. Unas burbujas la envuelven y siente que está bajo el agua, aunque puede respirar. Desde abajo contempla una batalla de barcos, fuego y restos que caen al mar junto con piratas y marines. Al abrir los ojos sigue viajando sobre Luna hacia Shiaru; el director aclara que la visión no le causa daño.',
     ['Citlali','Lunaria','Shiaru','Marina'],
     limit='El pirata no recibe nombre en esta visión. El punto de vista submarino no prueba un ahogamiento real de Citlali o Nox, una muerte individual ni la posición exacta de la visión dentro de la batalla naval.')
fact(516,578,535,'Molly llega al punto defensivo y permite huir si es necesario',
     'Erandy, Eleanor y Molly avanzan entre trampas, tiradores ocultos y vallas bajas hasta el punto acordado. Molly reconoce que no cree que puedan ganar y asegura que comprenderá que huyan si corren peligro. Erandy no quiere dejarla a su suerte. Molly aclara que ya no es capitana y dirige a Eleanor una mirada para que proteja a la escudera si la situación se vuelve insostenible.',
     ['Molly','Erandy','Eleanor','El Garfio'],
     limit='La derrota es la valoración previa de Molly, no el resultado confirmado de la sesión. No se representa todavía una huida ni el sacrificio de nadie.')
fact(579,601,589,'Eleanor entrega a Molly el broche de su tierra',
     'Eleanor explica que ayuda a los defensores por el buen trato que han dado a Erandy, que no habría recibido lo mismo en el reino de la caballera. Se quita el broche de su tierra y se lo entrega a Molly. Alude a una leyenda y dice que, si recuperase su cuerpo, quizá podría intentar hacer algo; espera no necesitar comprobarlo. Molly agradece el gesto.',
     ['Eleanor','Erandy','Molly','Broche de Eleanor'],
     limit='La alusión a recuperar el cuerpo es hipotética. No demuestra que Eleanor pueda resucitar a Molly, que la leyenda sea cierta o que Molly haya muerto. No se ve ni se describe el emblema del broche.')
fact(602,657,633,'El grupo despliega una emboscada y refuerza sus defensas',
     'Además del grupo de piratas, dos miembros más seguros de la tripulación de Bonnie ayudan a ordenar las posiciones. Molly espera pelotones con caballos, cañones y rifles por un solo camino y quiere canalizarlos para evitar un ataque simultáneo. Eleanor aplica una protección de cinco puntos de vida temporales a Molly, Erandy y ella misma. Erandy prepara sus espíritus guardianes para cuando el enemigo se acerque. Molly distribuye a sus hombres entre el bosque y la retaguardia y queda en medio del terreno.',
     ['Molly','Eleanor','Erandy','Bonnie','El Garfio'],
     limit='Se conserva la explicación de puntos temporales usada en la partida, sin corregirla mediante reglas externas. Los espíritus se dejan preparados; este intervalo no muestra su daño ni su duración efectiva.')
fact(658,675,663,'Eleanor intenta ocultarse bajo hojas y prepara su transformación',
     'Eleanor pide cubrirse de hojas y tumbarse para ocultarse; el director exige una tirada de sigilo. Planea activar una transformación al acercarse los enemigos y en la mesa corrigen que procede de la opción racial del caído, no de su juramento de conquista.',
     ['Eleanor','El Garfio'],
     limit='La preparación no muestra todavía la transformación o su efecto. La referencia al caído no fija por sí sola un origen biográfico nuevo ni justifica atribuir un resultado de sigilo no verbalizado.')
fact(684,741,701,'Los marines llegan con perros, artillería y oficiales montados',
     'Se oyen pasos, ramas y ruedas. Avanzan grupos de marines con pistolas y perros que rastrean trampas; detrás vienen pelotones ordenados, fusileros con armas largas, equipos que arrastran cañones y capitanes sobre caballos de guerra. Los perros olfatean las trampas laterales, dispuestas para impedir que se desvíen del embudo. Al verlos, Eleanor abandona la idea de permanecer tumbada.',
     ['Marina','Eleanor','El Garfio'],
     limit='Los oficiales, perros y caballos carecen aquí de nombres individuales. No se afirma que todos los perros queden atrapados o que las trampas ya hayan causado bajas.')
fact(750,817,804,'Erandy invoca al Sol y prepara una bola de fuego',
     'Ante el avance enemigo, Erandy propone usar los espíritus guardianes como barrera. El director le advierte que esperar a ese alcance pondría al ejército encima del grupo y le anima a aprovechar la distancia. Eleanor declara favor divino y empieza a leer las escrituras de su espada. Erandy junta las manos, pide al Sol ayuda para defender a los débiles y prepara una bola de fuego para cuando los marines estén a distancia.',
     ['Erandy','Eleanor','Marina'],
     limit='La plegaria y la preparación no muestran todavía el resultado de la bola de fuego. El discurso completo de la espada de Eleanor aún no se desarrolla en este bloque.')
fact(818,869,860,'La primera descarga de la Marina mata a piratas de la defensa',
     'Los marines ven a Molly y a los piratas. Un oficial ordena a los fusileros acabar con ellos y las líneas disparan por turnos. Las ráfagas alcanzan los pequeños grupos de defensores; algunos piratas próximos a Erandy mueren mientras continúa el fuego intenso.',
     ['Marina','Molly','Erandy','El Garfio'],
     limit='Las bajas son piratas sin nombre y no se da un total. No se atribuyen a esos muertos identidades catalogadas ni se presenta la descarga como la caída definitiva de la defensa.')
fact(870,894,881,'Eleanor levanta el escudo y Erandy recibe heridas de bala',
     'El director pide a Eleanor y Erandy que se defiendan de la descarga. Eleanor levanta el escudo y siente impactos que parecen empujarla hacia atrás. Erandy recibe roces y pequeñas heridas de algunos proyectiles. La Marina permanece parada disparando contra sus posiciones.',
     ['Eleanor','Erandy','Marina'],
     limit='No se comunica aquí una muerte, caída a cero o activación de la protección de ocho horas. El relato no fija una cantidad de daño numérica para cada una.')
fact(894,920,896,'Erandy elige el lugar para lanzar su bola de fuego',
     'Tras la descarga, Erandy recuerda que tenía preparada una bola de fuego y confirma con el director que llega a la posición enemiga. Señala dónde lanzarla y ajustan el punto para abarcar a varios grupos. El bloque termina cuando el director le pide representar el lanzamiento.',
     ['Erandy','Marina','El Garfio'],
     limit='El lanzamiento comienza a narrarse al corte; su impacto, daño, bajas y efecto en el resto de la batalla deben integrarse desde los bloques posteriores.')

stages = [
    dict(titulo='La misma partida, vista desde tierra', referencias=['43-001','43-002','43-004','43-005','43-006','43-007','43-008','43-009','43-010'], texto=
         'El director sitúa el comienzo al mismo tiempo que la partida del grupo naval. Erandy y Eleanor han conocido la amenaza de la Marina y hablado con Bonnie y Molly sobre la defensa terrestre. Tras inspeccionar el punto preparado en la jungla, vuelven a Shiaru para las últimas órdenes. En la plaza, Gobs reúne instrumental, Armin espera con sus mazas y Liz y sus compañeras se arman. Ione, Ilikar y Poncelot están con los Zampaolas. Bonnie anima a los defensores y activa la moneda entre rayos: las nubes negras anuncian la tormenta mientras los piratas corren a embarcar. Liz y otros habitantes permanecen tras las barricadas del poblado. Molly reúne a unos veinte piratas, decididos pero mal preparados. Antes de partir, Erandy posa una mano sobre Eleanor y la envuelve en la calidez del Sol. La protección explicada en la mesa durará ocho horas y puede evitar que caiga a cero. El grupo marcha a defender el embudo de la jungla.'),
    dict(titulo='Citlali corre hacia una visión', referencias=['43-003','43-011','43-012','43-013'], texto=
         'Citlali recuerda cómo permaneció en Iktan cuidando a la cría. El insomnio y los recuerdos la condujeron a una caja de música cuya melodía le evocó a sus hijos y a Nox. Un dolor y una señal extraña en la piel la empujaron a tomar al pequeño y correr, convencida de que debía averiguar qué ocurría. En la jungla vuelve a sentir un pinchazo en la cabeza y encuentra a Luna recogiendo hierbas. Rechaza el té que le propone y le pide ayuda para llegar a Shiaru cuanto antes. Luna se transforma en oso, carga a Citlali y lleva atada a la cría, que se arrastra y corre detrás como puede. Durante el viaje, Citlali ve a un pirata desaliñado de espaldas. Las burbujas la rodean y la visión cambia a una batalla naval contemplada desde debajo del agua: caen fuego, restos, piratas y marines. Cuando abre los ojos sigue sobre el oso. La visión no la ha trasladado al mar ni identifica una muerte individual.'),
    dict(titulo='Promesas y disparos en el embudo', referencias=['43-014','43-015','43-016','43-017','43-018','43-019','43-020','43-021','43-022'], texto=
         'Molly y las dos viajeras llegan entre trampas y posiciones ocultas. La ex capitana reconoce que cree imposible vencer y les permite huir si el peligro lo exige. Erandy se niega a abandonarla. Eleanor explica que ayuda por el trato que han dado a su escudera, entrega a Molly el broche de su tierra y menciona una leyenda con la que quizá podría hacer algo si recuperase su cuerpo; todavía es una posibilidad temida. Refuerzan sus protecciones y distribuyen a los piratas para emboscar. Eleanor intenta esconderse entre hojas, pero reconsidera la posición al ver los perros. Los marines llegan con rastreadores, fusileros, cañones y oficiales montados. Erandy invoca al Sol y prepara fuego mientras Eleanor lee las escrituras de su espada. La Marina se detiene y dispara en filas: mueren piratas próximos a la escudera. Eleanor recibe los impactos sobre el escudo y Erandy sufre pequeñas heridas. La kender confirma el alcance de su bola de fuego y elige el lugar del lanzamiento; su resultado queda en el tramo siguiente.')
]

histories = []
def history(name, kind, title, text, refs, new=False, description='', note=''):
    histories.append(dict(nombre=name,tipo=kind,nueva=new,descripcion=description,nota=note,
                          etapas=[dict(titulo=title,texto=text,referencias=refs)]))

history('Erandy','personaje','Proteger a su señora y sostener la defensa',
        'Erandy acompaña a Eleanor en la preparación del frente terrestre y piensa en trampas para detener a la Marina. Antes de marchar, envuelve a su señora en una protección del Sol que puede evitar su caída. Cuando Molly advierte que quizá deban huir, Erandy no quiere dejarla a su suerte. En el embudo prepara sus espíritus guardianes, pero recibe el consejo de aprovechar la distancia e invoca al Sol para lanzar una bola de fuego. La primera descarga mata a algunos defensores cercanos y le causa pequeñas heridas; el impacto de su respuesta comienza en el tramo posterior.', ['43-002','43-009','43-014','43-016','43-019','43-020','43-021','43-022'])
history('Eleanor','personaje','El broche y el deber hacia Erandy',
        'Eleanor participa en la preparación del embudo con Erandy y recibe su protección antes de partir. Explica a Molly que ayuda por el buen trato dado a la escudera, que contrasta con lo que esta habría recibido en su reino. Entrega a la ex capitana el broche de su tierra y alude a una leyenda con la que quizá podría intentar algo si recuperara su cuerpo. A continuación refuerza a sus aliadas, considera ocultarse bajo hojas y prepara su poder mientras llegan los marines. Durante la primera descarga sostiene el escudo contra las balas. La leyenda no confirma un poder de resurrección ni una muerte ya ocurrida.', ['43-002','43-009','43-014','43-015','43-016','43-017','43-019','43-021'])
history('Molly','personaje','Al frente del embudo terrestre',
        'Molly prepara la defensa de tierra de Shiaru y acompaña a Eleanor y Erandy al punto protegido por trampas y tiradores. Reconoce la inferior preparación de sus aproximadamente veinte piratas y cree que no podrán vencer. Les permite retirarse si es necesario, especialmente para proteger a Erandy, y recuerda que ya no ostenta su antiguo cargo de capitana. Recibe de Eleanor un broche y un ofrecimiento ligado a una leyenda. Después distribuye la emboscada y espera en el terreno cuando los fusileros de la Marina abren fuego.', ['43-005','43-010','43-014','43-015','43-016','43-020'])
history('Citlali','personaje','La caja de música y el viaje sobre el oso',
        'Citlali relata su estancia en Iktan, el cuidado de la cría y el insomnio. Una caja de música le devuelve recuerdos de sus hijos y de Nox; el dolor y una señal extraña en la piel la llevan a correr con el pequeño. En la jungla pide ayuda a Lunaria para llegar a Shiaru y viaja sobre ella cuando adopta forma de oso. Tiene una visión de un pirata sin nombre y de una batalla naval vista desde debajo del agua. Vuelve en sí todavía sobre su compañera, sin daño por la visión. Su urgencia y las imágenes no determinan la muerte de Nox ni el significado de la marca.', ['43-003','43-011','43-012','43-013'])
history('Lunaria','personaje','Un oso para ayudar a Mamá',
        'Tras recorrer Iktan y preguntar por sus misterios, Lunaria aparece en la jungla recogiendo hierbas que no conoce con precisión. Al encontrar a Citlali angustiada, primero le ofrece un té. Cuando la anciana insiste en llegar cuanto antes a Shiaru, se transforma en oso, la transporta y sujeta con los dientes una cuerda atada a la cría, que sigue detrás con dificultad. No presencia como propia la visión de Citlali.', ['43-004','43-011','43-012','43-013'])
history('Etley','personaje','La cría en el viaje apresurado',
        'Citlali dice haber cuidado a la cría hasta su recuperación en Iktan y después se la lleva al comenzar su carrera. El pequeño, todavía sin intervenir en combate, aparece medio dormido y arrastrado del ala. Cuando Lunaria se convierte en oso, queda sujeto con una cuerda y sigue como puede mientras ella lleva a Citlali. El transporte es incómodo, pero este tramo no narra su muerte o una herida concreta.', ['43-003','43-011','43-012'],
        note='Las variantes Ezir y otras del pequeño se agrupan contextualmente con Etley, la cría de Citlali; no confundir con Cipo ni con un hijo humano.')
history('Liz','personaje','Rifles y barricadas en Shiaru',
        'Liz prepara armas con sus compañeras durante la concentración en la plaza. Después de que los barcos zarpen permanece en Shiaru, distribuyendo a las mujeres con rifles por esquinas y barricadas para defender el poblado. La sesión todavía no muestra que la Marina alcance esas posiciones.', ['43-006','43-008'])
history('Bonnie','personaje','Una partida compartida por ambos frentes',
        'La concentración de la defensa se presenta de nuevo desde el grupo terrestre. Bonnie pronuncia su discurso, sostiene la moneda de los reyes piratas y se transforma entre rayos mientras convoca una tormenta. Los barcos parten y Molly dirige la defensa terrestre. Se trata del mismo comienzo de la batalla naval mostrado antes, no de una nueva activación posterior.', ['43-001','43-005','43-006','43-007','43-010'],
        note='Integrar como otra evidencia de la partida compartida con 42, sin duplicar el acontecimiento ni trasladarlo después de su final.')
history('Gobs','personaje','Herramientas durante la concentración',
        'En la concentración anterior a la batalla, Gobs reúne herramientas en una bolsa, entre ellas una sierra. El relato vuelve a su preparación médica peculiar sin mostrar una intervención nueva ni situarlo después del desenlace naval.', ['43-001','43-006'],
        note='Es la concentración ya descrita en42. Esta reaparición no demuestra supervivencia posterior a esa batalla.')
history('Armin','personaje','Las mazas antes de zarpar',
        'Armin está presente en la plaza de Shiaru con dos enormes mazas durante la preparación común de la batalla. Su aparición aporta el punto de vista del grupo terrestre a la misma concentración, sin adjudicarle acciones posteriores en el combate.', ['43-001','43-006'],
        note='Evitar narrar esta escena como posterior al cierre42.')
history('Shiaru','lugar','La defensa que permanece en tierra',
        'Mientras Bonnie y los barcos parten bajo la tormenta, Liz y sus compañeras se sitúan con rifles y barricadas en el poblado. Molly marcha con Eleanor, Erandy y un pequeño contingente hacia un embudo de la jungla para impedir que la Marina llegue a Shiaru. Al mismo tiempo, Citlali intenta regresar con ayuda de Lunaria, impulsada por un dolor y una visión que aún no sabe interpretar.', ['43-001','43-005','43-006','43-007','43-008','43-010','43-011','43-012','43-013'])
history('El Garfio','lugar','Un embudo defendido en la jungla',
        'El frente de tierra del Garfio se prepara con cuerdas, trampas, vallas bajas y tiradores ocultos. Molly, Eleanor y Erandy regresan al punto acordado con un pequeño grupo de piratas. La Marina avanza con perros rastreadores y una columna de fusileros, cañones y oficiales montados. El terreno pretende impedir que todos ataquen al mismo tiempo, pero la primera descarga causa bajas antes de que se complete la respuesta de Erandy.', ['43-005','43-010','43-014','43-016','43-018','43-020','43-022'],
        note='Embudo es una denominación funcional del punto del frente terrestre, no un topónimo dado. No equiparar con las ruinas del36 sin confirmación.')
history('Iktan','lugar','La salida urgente de Citlali',
        'Citlali recuerda que en Iktan cuidó a la cría y volvió a sufrir insomnio. Allí encontró una caja de música ligada a recuerdos de sus hijos y de Nox; después del dolor y la señal extraña en la piel decidió marcharse. Lunaria había estado recorriendo el poblado e interrogando a sus habitantes antes de aparecer en la jungla. Estos repasos no confirman nuevas respuestas sobre sus misterios.', ['43-003','43-004'])
history('Marina','faccion','Una columna contra el embudo',
        'En paralelo al despliegue naval, la Marina avanza por tierra hacia Shiaru. Los perros rastrean las trampas del camino, seguidos por pelotones, fusileros con armas largas, equipos de cañón y capitanes montados. Al descubrir a Molly y a los defensores, los fusileros disparan en líneas alternas: matan a piratas sin nombre y hieren a Erandy. La escudera prepara una respuesta de fuego que aún no se resuelve en este primer tramo.', ['43-001','43-018','43-019','43-020','43-021','43-022'])
history('Moneda pirata de Bonnie','objeto','La tormenta vista desde la plaza',
        'El grupo que defenderá tierra contempla la misma activación de la moneda que precede a la partida de la flota. De ella surgen rayos que envuelven a Bonnie y la tormenta comienza a levantarse mientras los piratas corren a los muelles. La visión desde otro grupo confirma ese momento compartido sin contar un segundo uso.', ['43-001','43-007'],
        note='Añadir evidencia a la etapa de la partida del42, sin fabricar una activación posterior.')
history('Broche de Eleanor','objeto','Un ofrecimiento antes del combate',
        'En el punto defensivo de la jungla, Eleanor se quita el broche de su tierra y se lo entrega a Molly. Explica que ayuda por el buen trato dado a Erandy y alude a una leyenda con la que quizá podría intentar algo si recuperara el cuerpo de Molly. El gesto expresa el compromiso anterior al combate; no identifica el emblema del objeto, garantiza una resurrección o demuestra que la ex capitana haya muerto.', ['43-015'], True,
        'Broche de la tierra de Eleanor que la caballera entrega a Molly antes del combate terrestre del Garfio.',
        'No se describe el símbolo ni se demuestra un poder propio del objeto. La leyenda evocada permanece hipotética.')
history('Caja de música de Citlali','objeto','Una melodía antes de la carrera',
        'Citlali cuenta que encontró una caja de música durante su estancia en Iktan. La melodía le hizo recordar a sus hijos y a Nox. Después sintió dolor y vio algo extraño en su piel, acontecimientos que la impulsaron a llevarse a la cría y correr hacia Shiaru. La sucesión de hechos no demuestra que la caja causara el dolor o la marca; su origen y mecanismo permanecen sin explicar en este repaso.', ['43-003'], True,
        'Caja de música hallada por Citlali en Iktan cuya melodía evoca a sus hijos y a Nox antes de su carrera hacia Shiaru.',
        'Vincular con las escenas escritas revisadas de Citlali, sin convertir la proximidad temporal de la música y el dolor en causa probada.')

delivery = dict(bloque=1, lectura_completa=True, primer_segmento='c000001', ultimo_segmento='c001841',
    etapas=stages, afirmaciones=facts,
    misiones=[
        'Detener el avance terrestre contra Shiaru: Molly conduce a la defensa a un embudo preparado con trampas y tiradores. La Marina llega, dispara y causa las primeras bajas; este tramo no decide el resultado (43-005, 43-010, 43-014, 43-016–43-022).',
        'Proteger a Erandy y a los compañeros: la kender protege a Eleanor y esta refuerza a sus aliadas. Molly permite que huyan si la vida de la escudera corre peligro; no se muestra una retirada en este bloque (43-009, 43-014, 43-016, 43-021).',
        'Llegar a Shiaru: Citlali corre con la cría por su dolor e intuición; Lunaria se transforma en oso para llevarla y continuar el viaje. La visión no acredita la llegada ni una muerte concreta (43-003, 43-011–43-013).',
        'Mantener la defensa del poblado: Liz y sus compañeras se quedan tras barricadas cuando parte la flota. La Marina aún no alcanza esas posiciones en este tramo (43-008).'
    ],
    preguntas=[
        '¿Qué significa la señal de la piel y el dolor de Citlali, y qué vínculo tienen con sus recuerdos de Nox y la caja de música? El repaso no demuestra la causa ni una muerte (43-003, 43-011, 43-013).',
        '¿Quién es el pirata de la visión de Citlali y en qué momento de la batalla se sitúa la perspectiva submarina? Las imágenes no identifican por sí solas a una víctima (43-013).',
        '¿Qué leyenda evoca Eleanor al entregar su broche a Molly y qué podría intentar si recuperara su cuerpo? El ofrecimiento todavía es hipotético y no demuestra una resurrección (43-015).'
    ],
    contradicciones=[
        'La apertura43 ocurre a la vez que el comienzo42. La plaza, la partida y la tormenta no son hechos nuevos posteriores al desenlace naval; las presencias de Ione, Ilikar y Poncelot no demuestran supervivencia después de42 (43-001, 43-006–43-007).',
        'Citlali relata el recuerdo de Nox y tiene después una visión de un pirata que no recibe nombre. No se afirma por semejanza que vea su muerte o un ahogamiento real, ni se convierte la visión en un conocimiento compartido por Lunaria (43-003, 43-013).',
        'Luna/Lunaria es la kender que se transforma en oso para llevar a Citlali; Erandy es la escudera que protege a Eleanor y responde a los fusileros. Comparten especie, no identidad (43-002–43-004, 43-009, 43-011–43-013, 43-019–43-022).',
        'La posibilidad de huir procede de la valoración pesimista de Molly. No se marca la defensa como perdida por sus palabras ni la leyenda de Eleanor como una capacidad probada de resurrección (43-014–43-015).',
        'El director usa grupos de tokens como representación de más combatientes; no se calcula una cifra exacta de bajas a partir de fichas o de los objetivos que caben en la futura bola de fuego (43-010, 43-016, 43-020, 43-022).'
    ],
    nombres_dudosos=[
        'Erandy/Erandi/Randy/Andy es la escudera de Eleanor; Luna/Lunaria es otra kender, compañera de Citlali en la jungla. No fusionarlas por las formas de tratamiento de la mesa (43-002, 43-004, 43-009, 43-012).',
        'La cría llamada Ezir y otras variantes corresponde por continuidad a Etley, el pequeño que cuida Citlali en Iktan y lleva a la jungla. No se inventa un hijo humano ni se confunde con Cipo (43-003, 43-011–43-012).',
        'Gobs/Cops, Armin, Liz/Lis, Molly/Moli y Bonnie/Pigoni/Happy Bonnie se mantienen en las identidades ya catalogadas de Shiaru (43-002, 43-005–43-008).',
        'El enano azul que anunciaba el fin no queda identificado por nombre y el pirata de la visión de Citlali tampoco. No se crean fichas personales a partir de esos indicios (43-002, 43-013).',
        'El punto acordado se denomina embudo por su función defensiva. El título y el frente lo vinculan al Garfio, sin un topónimo independiente ni una identificación comprobada con las ruinas del capítulo36 (43-005, 43-010, 43-014, 43-016).',
        'El nombre del hechizo protector se transcribe incompleto; se conserva la duración de ocho horas y el efecto de permanecer con un punto de vida tal como se explica en la mesa (43-009).'
    ],
    historias_entidades=histories)
(ROOT / 'borradores/43/entrega_1.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
print(f'Entrega 1: {len(facts)} afirmaciones validadas, {len(stages)} etapas, {sum(len(s["texto"].split()) for s in stages)} palabras y {len(histories)} propuestas de historia.')
