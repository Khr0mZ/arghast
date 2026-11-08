"""Lectura editorial íntegra del bloque 1 del capítulo 44 de Xoltacan."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import validate_fact

rows = json.loads((ROOT / 'campanas/xoltacan/revision/borradores/44/bloque_1_segmentos.json').read_text(encoding='utf-8'))
source = ROOT / 'campanas/xoltacan/fuentes/44 - KAfKPeZImT4.es-orig.vtt'
facts = []

def fact(a, b, anchor, title, statement, names, kind='hecho_confirmado', limit=''):
    cue = rows[anchor]
    item = dict(id=f'44-{len(facts)+1:03d}', titulo=title, tipo=kind,
                afirmacion=statement, inicio=rows[a]['inicio'], fin=rows[b]['fin'],
                cita=cue['texto_original'],
                evidencia_cue=dict(inicio=cue['inicio'], fin=cue['fin'], texto=cue['texto_original']),
                entidades=names, ambito='búsqueda del ingrediente para tratar a Eromov',
                conocedores=[], conocimiento_personaje='desconocido',
                nota_conocimiento='Acceso de Madame Oghma sin establecer en este pasaje.',
                confianza='lectura de subtítulos; audio no cotejado', limitacion=limit)
    validate_fact(item, source)
    facts.append(item)

fact(20,36,34,'Leona busca rastros tras su misión de aviso',
     'Leona recuerda que salió por órdenes para avisar sobre las serpientes y pedir que acudieran personas capaces de ayudar. Se ha reunido de nuevo con Guayacán y, mientras espera los resultados de esa ayuda, ha buscado pistas de las serpientes cerca del poblado.',
     ['Leona','Guayacán','Cuicapalli','Iktan','Yuan-ti'], 'declaracion_personaje',
     'El contexto enlaza el aviso previo a Iktan, sin detallar en este repaso una llegada efectiva de recetas, protecciones o refuerzos. La presentación de Leona como posible futura líder no equivale a una investidura.')
fact(38,58,52,'Tlachka recuerda Iktan y prepara fruta y mazorcas',
     'Tlachka relata su paso por Iktan y recuerda personas que se transformaban en serpientes. Ha buscado descanso apartado de Coyote, recogido frutas en los alrededores y preparado mazorcas para vender.',
     ['Tlachka','Iktan','Coyote','Yuan-ti'], 'declaracion_personaje',
     'El repaso no identifica una nueva infiltrada o un combate distinto. Su recuerdo de Iktan no le atribuye por sí solo las acciones del grupo del capítulo 41.')
fact(60,78,65,'Guayacán cuida la ciudad en ausencia de Leona',
     'Guayacán explica que, por petición de Leona y decisión propia, ha cuidado Cuicapalli mientras ella estaba fuera. Ha estudiado la vigilancia, los puntos por donde entran bestias, la distribución del lugar y el ánimo de los habitantes.',
     ['Guayacán','Leona','Cuicapalli'], 'declaracion_personaje',
     'La responsabilidad de vigilancia no implica que haya sido nombrado dirigente ni que los peligros de la ciudad hayan desaparecido.')
fact(79,122,91,'Leona y Guayacán vuelven de las rondas y comen junto a Tlachka',
     'Leona y Guayacán regresan a Cuicapalli cubiertos de hojas y con marcas de sus rondas por los alrededores. Esperan que Eromov mejore y que lleguen refuerzos. Se acercan a Tacha y piden comida. Tlachka se ha hecho un hueco junto a la cocina para tostar mazorcas como acompañamiento.',
     ['Leona','Guayacán','Cuicapalli','Eromov','Tacha','Tlachka','El Bocado del Jaguar'],
     limit='La expectativa de refuerzos no representa su llegada. El establecimiento se vincula contextualmente a la taberna de Tacha ya catalogada; no se pronuncia un nombre nuevo para el local.')
fact(124,193,130,'Guayacán cambia la voz al reconocer a Tlachka',
     'La interpretación distingue una voz normal de Guayacán y otra que adopta al ponerse firme ante Tlachka, a quien reconoce del enfrentamiento contra la Marina. Hablan de las serpientes de Iktan y de la búsqueda de venenos, sin aportar una muestra nueva. Tacha sirve tres platos de lechón y Guayacán cambia su porción de carne por una mazorca de Tlachka.',
     ['Guayacán','Tlachka','Leona','Tacha','Iktan','Marina'],
     limit='El cambio de voz no declara la especie o identidad oculta de Guayacán. Las alusiones humorísticas al perro y a su cola no prueban una acción nueva de Coyote o un conocimiento del veneno.')
fact(194,267,214,'Ayoto se reúne con sus compañeros y cuenta sus viajes',
     'Ayoto llega a la comida, saluda a Tlachka, Leona y Guayacán y cuenta que ha vuelto de Iktan a Cuicapalli para informarse de lo ocurrido. Recuerda su estancia bajo el mar, su desorientación en el bosque, las amenazas en una ciudad oculta y la ayuda de un perro extraño. Afirma haber ayudado en el agua y querer hacerlo también en tierra.',
     ['Ayoto','Tlachka','Leona','Guayacán','Iktan','Cuicapalli'], 'declaracion_personaje',
     'El repaso es su testimonio. La mención del perro no contiene un nombre y no crea una identidad nueva; tampoco demuestra una misión submarina distinta o resultados no representados aquí.')
fact(268,330,280,'Un guardia lleva a Leona y Guayacán ante Parroter',
     'Un guardia busca a Leona porque Parroter la reclama con urgencia. Guayacán sigue a su maestra hasta la choza de Eromov. Ayoto y Tlachka se quedan comiendo con Tacha; Ayoto ofrece comida a otro guardia, que la acepta sin abandonar expresamente su puesto.',
     ['Leona','Guayacán','Parroter','Eromov','Ayoto','Tlachka','Tacha','Cuicapalli'],
     limit='Los guardias permanecen sin nombre y no se fusionan por compartir función. La demora en la comida no se convierte en un daño concreto a Eromov.')
fact(331,348,337,'Eromov sigue postrado y Parroter lo refresca',
     'Al entrar, Leona comprueba el estado de Eromov. Está tendido en la cama bajo mantas de hojas, tiembla y tose. Parroter cambia las hojas mojadas de su frente para refrescarlo. El dirigente apenas consigue levantar la trompa para saludar y Leona le pide que no se esfuerce.',
     ['Leona','Eromov','Parroter','Guayacán','Cuicapalli'],
     limit='La escena confirma que Eromov sigue vivo y enfermo en ese momento. No acredita todavía un antídoto administrado, una recuperación ni un fallecimiento posterior.')
fact(349,363,355,'Parroter ha avanzado pero necesita otro ingrediente',
     'Leona dice que no encuentra el rastro de las serpientes. Parroter le indica que ahora necesita otra cosa: con lo que ella trajo ha podido avanzar, pero le falta un ingrediente peligroso. Leona se ofrece a ir por él de inmediato.',
     ['Leona','Parroter','Eromov'], 'declaracion_personaje',
     'Parroter no identifica aquí cada material recibido. No se equiparan por esta frase las muestras de la Hoja Caída, del claro del dragón y de los viales verdes de Iktan, ni se da por terminado el remedio.')
fact(364,410,406,'Parroter describe al devorafango y dónde buscarlo',
     'Parroter nombra al devorafango. Leona y Guayacán no logran identificarlo mediante las tiradas de historia. El alquimista lo describe como una criatura peligrosa que escupe sustancias capaces de quemar la piel y que vive en cuevas junto a ríos, lagos y zonas con agua. Leona decide buscar en lugares húmedos.',
     ['Parroter','Leona','Guayacán','Devorafango'], 'declaracion_personaje',
     'El nombre se conserva como lectura provisional de Débora Fango/Borafango y variantes. La descripción aún es información de Parroter, no observación del grupo. El intercambio sobre la procedencia de Guayacán no fija una ciudad natal o su especie.')
fact(411,447,418,'Las espinas deben extraerse mientras el devorafango vive',
     'Parroter precisa que necesita las espinas del interior de la boca del devorafango y que deben arrancarlas mientras siga vivo: si lo matan antes no servirán. Pueden matarlo después si quieren. Advierte que Eromov quizá no aguante mucho más y Leona se compromete a volver deprisa, con ayuda de los dos compañeros que siguen comiendo.',
     ['Parroter','Leona','Guayacán','Eromov','Devorafango','Espinas del devorafango'], 'declaracion_personaje',
     'El encargo requiere espinas en plural; los viajeros lo simplifican después a una espina, sin fijar aquí una cantidad exacta suficiente. Entrar en la boca es la propuesta de Leona, no el único método expresamente impuesto por Parroter. No se han obtenido o utilizado todavía.')
fact(450,558,483,'Leona recluta a Ayoto y Tlachka para buscar las espinas',
     'Mientras Tacha continúa sirviendo comida, Leona y Guayacán vuelven a buscar a Ayoto y Tlachka. La harengon explica la urgencia de salvar a Eromov y solicita ayuda a ambos. Tras un equívoco sobre si el dirigente tiene una espina en la garganta, aclara que deben buscar una criatura de barro y sacar de su boca el ingrediente mientras viva. El grupo acepta salir con ella hacia cuevas, ríos o lagos.',
     ['Leona','Guayacán','Ayoto','Tlachka','Eromov','Tacha','Devorafango','Espinas del devorafango'],
     limit='La espina en la garganta de Eromov es un malentendido corregido, no un diagnóstico. Las dificultades de conexión pertenecen a la mesa y no se convierten en sucesos de la ficción.')
fact(560,619,607,'Leona recuerda una cueva de su infancia junto a un lago',
     'Los cuatro salen de Cuicapalli y se internan en la jungla. Leona busca agua estancada y lugares húmedos mientras Ayoto rastrea sin conocer bien al animal. Tras la búsqueda, la harengon recuerda un lago cercano y una gran cueva donde jugaba con otros niños. Considera que su barro y humedad encajan con la descripción y conduce allí a sus compañeros.',
     ['Leona','Guayacán','Ayoto','Tlachka','Cuicapalli','Cueva del lago cercano a Cuicapalli'],
     limit='La cueva carece de topónimo en el pasaje. El recuerdo de Leona no la identifica con la Hoja Caída o con la cueva derrumbada del capítulo 39, ni confirma todavía la presencia del devorafango.')
fact(620,677,628,'Las frutas afectan las sombras y el brillo de los viajeros',
     'Al comer frutas, la sombra de Leona grita sin sonido cuando ataca; Ayoto pasa a temer a su propia sombra; Guayacán brilla de verde, con desventaja para el sigilo y ventaja para el carisma. Durante el mismo intercambio, el director concede al grupo bendición y un dado de cuatro para la partida.',
     ['Leona','Ayoto','Guayacán','Tlachka'], 'explicacion_director',
     'No se adjudica inequívocamente un efecto individual de fruta a Tlachka. La procedencia de la bendición colectiva no se explica con suficiente claridad para atribuírsela a su fruta. Los efectos no acreditan rasgos permanentes o una identidad nueva de las sombras.')
fact(678,709,699,'El viaje continúa entre sombras y una interrupción del mono',
     'Los compañeros siguen a Leona. Ayoto, temblando por el temor a su sombra, busca la cobertura de un árbol, aunque el director recuerda que la sombra lo sigue. Un mono observa a los viajeros y, tras unos segundos de miradas, lanza una piel de plátano; uno declara una caída cómica. El animal se ríe y trepa para alejarse.',
     ['Ayoto','Leona','Guayacán','Tlachka'],
     limit='No queda fijado con seguridad el actor de todas las intervenciones del incidente. El mono no recibe nombre ni se identifica con Pix; tampoco se narra que sea capturado o comido.')
fact(710,748,733,'La cueva junto al lago huele mal y contiene huesos',
     'Los viajeros llegan al lago y a la cueva embarrada que recuerda Leona. Ella se aproxima a la entrada y observa un interior de olor pestilente con huesos por el suelo. Los interpreta como restos de comida de la criatura buscada y llama a los demás para que se acerquen.',
     ['Leona','Guayacán','Ayoto','Tlachka','Cueva del lago cercano a Cuicapalli'],
     limit='Los huesos no se identifican por especie, nombre o causa exacta de muerte. Su presencia no demuestra aún qué criatura los dejó ni una conexión con los restos envenenados de Iktan.')
fact(749,760,757,'El grupo se reúne ante la entrada y recuerda la condición del encargo',
     'Los cuatro alcanzan la cueva. Leona intenta atraer a la bestia con llamadas como si fuese un gato y promete no matarla por un rato. Guayacán recuerda que deben extraer la espina mientras viva o la misión no servirá, y Leona confirma la instrucción.',
     ['Leona','Guayacán','Ayoto','Tlachka','Devorafango','Espinas del devorafango','Cueva del lago cercano a Cuicapalli'],
     limit='Las llamadas no identifican al animal como felino ni prueban que responda. El recordatorio habla de la criatura del encargo antes de que el grupo identifique a su primer adversario.')
fact(761,777,765,'Una masa de moho se alza cerca de Leona',
     'Guayacán advierte que el suelo junto a Leona empieza a moverse de forma extraña. Le avisa del peligro y la materia del suelo se levanta como una masa enorme, dando comienzo al enfrentamiento en la entrada de la cueva.',
     ['Guayacán','Leona','Masa de moho de la cueva','Cueva del lago cercano a Cuicapalli'],
     limit='Masa de moho es una etiqueta editorial descriptiva. El pasaje no la llama devorafango ni muestra espinas bucales; se conserva separada de la criatura del encargo y de la masa zombi del capítulo 40.')
fact(778,812,800,'Guayacán entra en furia y golpea dos veces a la masa',
     'Guayacán quiere demostrar a Leona que su entrenamiento ha dado resultado. Entra en furia, se acerca a la masa y conecta dos golpes. Intenta añadir una ráfaga de golpes, pero el director la anula porque ya ha utilizado la acción adicional para entrar en furia. Acepta la corrección y termina su turno.',
     ['Guayacán','Leona','Masa de moho de la cueva'],
     limit='La ráfaga anunciada no se cuenta como ataques realizados. El pasaje confirma dos impactos, sin derrota de la masa ni recuperación de las espinas.')
fact(813,837,830,'Leona evita que la masa la envuelva',
     'La masa se lanza sobre Leona para intentar envolverla. Tras una salvación de Constitución, la harengon se aparta y la criatura cae al suelo y sigue moviéndose sin golpearla. El director da paso al turno de Ayoto al final del bloque.',
     ['Leona','Masa de moho de la cueva','Ayoto'],
     limit='El ataque no la engulle ni la obliga a entrar en la boca del devorafango. El combate continúa en el bloque siguiente y no se anticipa un resultado para la misión.')

stages = [
    dict(titulo='Un regreso a Cuicapalli', referencias=['44-001','44-002','44-003','44-004','44-005','44-006','44-007'], texto=
         'Leona ha regresado de su misión de aviso y busca rastros de las serpientes mientras espera ayuda para Cuicapalli. Guayacán cuenta que cuidó la ciudad durante su ausencia, estudiando la vigilancia y el ánimo de sus habitantes. Tlachka vuelve a preparar frutas y mazorcas después de su estancia en Iktan. Los tres se reúnen junto a la cocina de Tacha al terminar las rondas. El aspecto de Guayacán y su voz cambiante provocan bromas, pero la conversación no revela su identidad oculta. Ayoto llega poco después, saluda a sus compañeros y recuerda sus viajes bajo el mar y por el bosque. Quiere conocer qué ha ocurrido y ayudar en tierra. El encuentro queda interrumpido por un guardia que reclama a Leona: Parroter necesita verla con urgencia. Guayacán la acompaña mientras Ayoto y Tlachka siguen comiendo. El goliat comparte además un trozo con un guardia que permanece de servicio.'),
    dict(titulo='Un ingrediente que debe seguir vivo', referencias=['44-008','44-009','44-010','44-011','44-012','44-013'], texto=
         'En la choza, Eromov sigue postrado bajo hojas, temblando y tosiendo. Parroter lo refresca y el dirigente apenas puede levantar la trompa para saludar. Leona no ha encontrado a las serpientes, pero el alquimista ya necesita otra búsqueda: ha avanzado con los materiales recibidos y le falta un ingrediente peligroso. Describe al devorafango, que vive en cuevas cercanas al agua y escupe sustancias capaces de quemar la piel. Necesita las espinas del interior de su boca, extraídas mientras viva; matarlo antes las inutilizaría. La urgencia aumenta porque teme que Eromov no resista mucho más. Leona promete regresar deprisa y recluta a Ayoto y Tlachka. Un equívoco hace pensar que el dirigente tiene una espina en la garganta, hasta que aclaran el encargo. Los cuatro salen a la jungla. Buscando lugares húmedos, Leona recuerda una cueva grande junto a un lago donde jugaba de pequeña y decide conducirlos allí.'),
    dict(titulo='La primera amenaza de la cueva', referencias=['44-014','44-015','44-016','44-017','44-018','44-019','44-020'], texto=
         'Las frutas alteran el viaje: la sombra de Leona grita sin sonido, Ayoto teme la suya y Guayacán brilla de verde. Entre comentarios y la interrupción de un mono que lanza una piel de plátano, siguen a la harengon hasta el lago. La cueva contiene barro, un olor pestilente y huesos que ella interpreta como restos de comida. Llama a la bestia como si fuese un gato, mientras Guayacán insiste en que deben sacarle la espina antes de matarla. Entonces el suelo junto a Leona se mueve y se alza una enorme masa de moho, todavía sin identificar con el devorafango. Guayacán avisa a su maestra, entra en furia y conecta dos golpes; su intento de añadir una ráfaga se corrige porque ya ha empleado la acción adicional. La masa responde lanzándose sobre Leona para envolverla. Ella consigue apartarse y la criatura cae al suelo sin alcanzarla. El turno pasa a Ayoto con el combate todavía abierto.')
]

histories = []
def history(name, kind, title, text, refs, new=False, description='', note=''):
    histories.append(dict(nombre=name,tipo=kind,nueva=new,descripcion=description,nota=note,
                          etapas=[dict(titulo=title,texto=text,referencias=refs)]))

history('Leona','personaje','Una búsqueda urgente para salvar al jefe',
        'Tras regresar de la misión de aviso, Leona busca rastros de las serpientes y participa en las rondas de Cuicapalli. Parroter la reclama ante el estado de Eromov y le encarga obtener espinas de la boca de un devorafango vivo. La harengon promete actuar deprisa y recluta a Guayacán, Ayoto y Tlachka. Su recuerdo de los juegos infantiles junto a un lago orienta al grupo hacia una cueva húmeda. Allí llama a la bestia, pero la primera amenaza es una masa de moho que intenta envolverla. Leona la esquiva. Su decisión de actuar por el dirigente no constituye todavía una investidura como sucesora.', ['44-001','44-004','44-007','44-008','44-009','44-011','44-012','44-013','44-016','44-017','44-018','44-020'])
history('Guayacán','personaje','De la vigilancia a proteger a su maestra',
        'Guayacán cuenta que se ha ocupado de la vigilancia y de conocer el ánimo de Cuicapalli mientras Leona estaba fuera. La acompaña a ver al enfermo y escucha las condiciones del encargo de Parroter. Su voz cambia al reconocer a Tlachka, pero no revela por ello su especie o su identidad oculta. Ya en la cueva recuerda que necesitan la espina con la bestia viva, detecta el movimiento del suelo y avisa a su maestra. Entra en furia y golpea dos veces a la masa que se alza; el intento de ráfaga se anula por haber gastado antes su acción adicional.', ['44-003','44-005','44-007','44-010','44-011','44-017','44-018','44-019'])
history('Ayoto','personaje','Unirse al remedio de Eromov',
        'Ayoto se reúne con los compañeros en Cuicapalli después de sus viajes y quiere saber qué ha ocurrido. Comparte la comida de Tacha y ofrece una porción a un guardia. Al escuchar la urgencia de Leona acepta buscar las espinas para tratar a Eromov. No conoce bien al animal y sigue la orientación de la harengon. Una fruta le provoca miedo a su propia sombra, que intenta disimular bajo la de un árbol. Llega con el grupo a la cueva y su turno comienza después de que Leona evite a la masa.', ['44-006','44-007','44-012','44-013','44-014','44-015','44-016','44-020'])
history('Tlachka','personaje','De las mazorcas a una nueva expedición',
        'Tlachka vuelve a preparar fruta y mazorcas después de su estancia en Iktan, donde procuró descansar lejos de Coyote. Comparte comida junto a Tacha, Leona y Guayacán y recibe después a Ayoto. Cuando Leona les explica la amenaza sobre Eromov, deja la comida para acompañar la búsqueda del ingrediente. Sigue al grupo a la cueva del lago, cuyo olor y huesos sugieren un refugio de criaturas sin identificar todavía a sus ocupantes.', ['44-002','44-004','44-005','44-006','44-007','44-012','44-013','44-016'])
history('Eromov','personaje','El tiempo apremia para conseguir otro ingrediente',
        'Eromov continúa vivo y enfermo en su choza de Cuicapalli. Tiembla y tose bajo las hojas, mientras Parroter lo refresca y él apenas saluda con la trompa. El alquimista teme que no aguante mucho más. Su estado impulsa a Leona a buscar con Guayacán, Ayoto y Tlachka las espinas de un devorafango vivo. Este primer tramo muestra la búsqueda, sin dar todavía por administrado un remedio o recuperado al dirigente.', ['44-008','44-009','44-011','44-012'])
history('Parroter','personaje','Las condiciones de una posible cura',
        'Parroter sigue atendiendo a Eromov y manda buscar a Leona. Dice que los materiales recibidos le han permitido avanzar, pero que necesita espinas del interior de la boca de un devorafango. Explica dónde buscarlo y advierte de su escupitajo corrosivo. Insiste en que la criatura debe vivir al extraerlas, pues de otro modo no servirán, y urge al grupo a volver antes de que el dirigente empeore. Su explicación no identifica por separado todas las muestras estudiadas ni completa aún la cura.', ['44-007','44-008','44-009','44-010','44-011'])
history('Tacha','personaje','La comida interrumpida por el encargo',
        'Tacha sirve lechón y acompaña la reunión en la que Tlachka prepara mazorcas. Continúa trayendo platos mientras Leona y Guayacán acuden a Parroter. Ayoto y Tlachka se quedan comiendo hasta que la harengon vuelve para pedir su ayuda. La escena documenta su hospitalidad habitual y no aporta una confesión o una nueva prueba sobre quién envenenó la comida de Eromov.', ['44-004','44-005','44-007','44-012'])
history('Cuicapalli','lugar','La búsqueda parte de la enfermedad de su dirigente',
        'La ciudad sigue siendo objeto de rondas y vigilancia de Leona y Guayacán mientras Eromov permanece enfermo. Una reunión junto a la cocina de Tacha reúne a Ayoto y Tlachka con ambos. Parroter interrumpe la comida para pedir un ingrediente y los cuatro salen a la jungla. La expectativa de refuerzos continúa sin una llegada representada en este primer tramo.', ['44-001','44-003','44-004','44-007','44-008','44-011','44-012','44-013'])
history('El Bocado del Jaguar','lugar','Una comida antes de la urgencia',
        'El entorno de Tacha vuelve a reunir a los viajeros: Tlachka tuesta mazorcas, el tabernero sirve lechón y Leona y Guayacán se sientan tras sus rondas. Ayoto llega para encontrarse con ellos. La reunión se transforma en el reclutamiento para buscar un ingrediente de la cura de Eromov cuando Leona vuelve de hablar con Parroter.', ['44-004','44-005','44-006','44-007','44-012'],
        note='Identificación contextual con el establecimiento de Tacha ya catalogado; la sesión no vuelve a pronunciar el rótulo.')
history('Cueva del lago cercano a Cuicapalli','lugar','El recuerdo de los juegos infantiles',
        'Al buscar un lugar húmedo donde pudiera vivir el devorafango, Leona recuerda una gran cueva junto a un lago cercano donde jugaba con otros niños. Conduce allí a Guayacán, Ayoto y Tlachka. Encuentran barro, olor pestilente y huesos en el interior. La primera amenaza que se levanta cerca de la entrada es una masa de moho que intenta envolver a Leona, sin que esa aparición identifique aún al objetivo del encargo.', ['44-013','44-016','44-017','44-018','44-020'], True,
        'Cueva húmeda junto a un lago cercano a Cuicapalli, recordada por Leona desde sus juegos infantiles y visitada al buscar el ingrediente para Eromov.',
        'Nombre editorial descriptivo, sin topónimo pronunciado. Mantener separada de la Hoja Caída, de la cueva derrumbada del39 y de los focos envenenados de Iktan salvo prueba posterior.')
history('Masa de moho de la cueva','personaje','Una emboscada al entrar',
        'En el suelo cercano a Leona empieza a moverse una materia que se levanta como una enorme masa. Guayacán avisa a su maestra y la golpea dos veces en furia. La masa intenta caer encima de Leona para envolverla, pero ella se aparta y el ataque no la alcanza. El combate continúa cuando comienza el turno de Ayoto.', ['44-018','44-019','44-020'], True,
        'Masa de materia del suelo que se alza junto a Leona en la cueva del lago e intenta envolverla.',
        'Etiqueta descriptiva de lectura provisional. No se identifica con el devorafango del encargo, un no muerto, una gelatina de especie concreta o la masa zombi del40.')
history('Devorafango','personaje','La criatura descrita por Parroter',
        'Parroter pide localizar a un devorafango para extraer las espinas del interior de su boca mientras vive. Lo describe como peligroso, capaz de escupir sustancias que queman la piel y habitante de cuevas junto a ríos o lagos. Leona y Guayacán no lo reconocen por su conocimiento previo y parten con Ayoto y Tlachka hacia una cueva húmeda. La masa de moho que encuentran primero no recibe ese nombre, por lo que ambas identidades se conservan separadas.', ['44-010','44-011','44-012','44-013','44-017','44-018'], True,
        'Criatura buscada por encargo de Parroter, que necesita las espinas de su boca para avanzar en el tratamiento de Eromov.',
        'Nombre provisional leído en Débora Fango/Borafango y variantes. Las características de este primer tramo proceden de Parroter; la identificación con la criatura espinosa del tramo posterior debe cotejarse durante la integración.')
history('Espinas del devorafango','objeto','El ingrediente que debe extraerse en vida',
        'Parroter precisa que el tratamiento de Eromov requiere espinas del interior de la boca de un devorafango. La condición decisiva es sacarlas mientras el animal siga vivo; después pueden matarlo si quieren. Leona transmite la instrucción a Ayoto y Tlachka y Guayacán la repite al llegar a la cueva. En este primer tramo las espinas son el objetivo de la búsqueda, sin recuperación o administración representadas.', ['44-011','44-012','44-017'], True,
        'Espinas bucales de devorafango solicitadas por Parroter como ingrediente para tratar a Eromov, útiles solo si se extraen con el animal vivo.',
        'La utilidad es la explicación de Parroter. No se fija una cantidad exacta, una extracción ya realizada o el éxito del tratamiento antes de leer el resto del capítulo.')

delivery = dict(bloque=1, lectura_completa=True, primer_segmento='c000001', ultimo_segmento='c001675',
    etapas=stages, afirmaciones=facts,
    misiones=[
        'Conseguir el ingrediente para Eromov: Parroter pide espinas del interior de la boca de un devorafango, extraídas mientras vive. Leona reúne a Guayacán, Ayoto y Tlachka y los guía hacia una cueva húmeda; no se recuperan aún en este bloque (44-008–44-013, 44-016–44-017).',
        'Sobrevivir a la primera amenaza de la cueva: una masa de moho se levanta junto a Leona. Guayacán la golpea y Leona evita su intento de envolverla; el combate sigue abierto al comenzar el turno de Ayoto (44-018–44-020).',
        'Vigilar Cuicapalli y buscar a las serpientes: Guayacán describe sus tareas de cuidado y Leona sus rondas y rastreos. La búsqueda del remedio pasa a ser urgente, sin que esas declaraciones eliminen la amenaza de infiltración (44-001, 44-003–44-004, 44-009).'
    ],
    preguntas=[
        '¿Cómo permitirán las espinas del devorafango completar el tratamiento y qué cantidad necesita Parroter? La condición de extraerlas en vida queda clara, pero todavía no se representa la preparación o administración (44-009–44-011).',
        '¿Qué materiales recibió Parroter y qué ha descubierto sobre el veneno? Su afirmación de haber avanzado no identifica por separado las muestras de distintas procedencias ni su composición (44-009).'
    ],
    contradicciones=[
        'Leona es la harengon relacionada con Cuicapalli, no Naór, la princesa leonina. Los lapsus que la describen como una leona no crean una transformación o una identidad común (44-001, 44-004, 44-012).',
        'Guayacán alterna su voz normal e impostada y mantiene gestos aviares. Eso no declara la especie que oculta su traje ni demuestra que los demás conozcan su secreto (44-005).',
        'La frase de Parroter sobre los materiales traídos no convierte los venenos de la Hoja Caída, del claro dracónico y de los viales verdes en una misma sustancia analizada (44-009).',
        'Entrar en la boca es la interpretación práctica de Leona; Parroter exige obtener las espinas de su interior mientras el animal viva, sin imponer expresamente el método. El equívoco de la espina en la garganta de Eromov se corrige (44-011–44-012).',
        'La primera masa de la cueva no recibe el nombre devorafango ni se ve una boca con espinas. No se fusiona con la bestia buscada o con los restos animados del claro de Iktan (44-010–44-011, 44-018–44-020).',
        'La ráfaga adicional anunciada por Guayacán se anula: solo quedan dos golpes y la furia. El ataque de la masa falla y no engulle a Leona (44-019–44-020).'
    ],
    nombres_dudosos=[
        'Tlachka/Tlatka/Traska/Trasca y otras formas remiten al vendedor de mazorcas ya catalogado; Ayoto/Yoto/Aoto es el goliat que llega después a la comida (44-002, 44-004–44-006).',
        'Parroter/Parro/Parro te y variantes son el alquimista kenku ya catalogado. Tacha es el tabernero, sin crear otra identidad por los cambios de pronunciación (44-004–44-005, 44-007–44-011).',
        'Débora Fango/Borafango y variantes se presentan provisionalmente como Devorafango, el objetivo descrito por Parroter. El nombre no convierte automáticamente a la primera masa en esa criatura (44-010–44-011, 44-018).',
        'Cueva del lago cercano a Cuicapalli y Masa de moho de la cueva son etiquetas editoriales descriptivas. No existe un topónimo inequívoco o una especie fijada en este primer tramo (44-013, 44-016, 44-018–44-020).',
        'El perro referido en los repasos no recibe nombre en esos pasajes. No se crea otra ficha ni se atribuyen por esas alusiones acciones nuevas a Coyote; el mono del camino no se identifica con Pix (44-005–44-006, 44-015).'
    ],
    continuidad=[
        dict(pregunta_id='P30-001', hechos=['44-008','44-009','44-010','44-011','44-012'],
             nota='Eromov está vivo pero sigue muy enfermo. Parroter muestra un nuevo paso concreto: ingrediente y condición de extracción. Este bloque no basta para cerrar la supervivencia, el antídoto o la recuperación; integrar el resto44.'),
        dict(pregunta_id='P40-006', hechos=['44-001','44-004','44-008','44-009'],
             nota='El repaso alude a pedir ayuda y los viajeros esperan refuerzos, sin una llegada descrita aquí de hombres, recetas o protecciones de Walulu. No convertir la alusión imprecisa en entrega comprobada.'),
        dict(pregunta_id='P22-003', hechos=['44-005'],
             nota='Hay cambio de voz al reconocer a Tlachka, sin declaración de especie o linaje. Conservar la incertidumbre de Guayacán.'),
        dict(pregunta_id='P27-002', hechos=['44-005'],
             nota='La voz normal e impostada suma un gesto interpretativo, sin precisar qué oculta el traje o quién conoce su identidad.'),
        dict(pregunta_id='P40-001', hechos=['44-009'],
             nota='No se identifica qué muestras han servido a Parroter ni se explica la animación de restos del claro. Mantener separadas las procedencias.'),
        dict(pregunta_id='P41-006', hechos=['44-009'],
             nota='No se mencionan explícitamente los viales verdes de la roca norte ni se compara su contenido con el veneno de Eromov.'),
        dict(pregunta_id='P30-002', hechos=['44-004','44-005','44-007','44-009'],
             nota='Tacha sigue sirviendo comida. La escena no identifica a quien añadió el veneno ni confiesa la participación de las visitantes de la reunión anterior.')
    ],
    historias_entidades=histories)
assert len(rows) == 838
assert rows[0]['id'] == delivery['primer_segmento'] and rows[-1]['id'] == delivery['ultimo_segmento']
(ROOT / 'campanas/xoltacan/revision/borradores/44/entrega_1.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
print(f'Entrega 1: {len(facts)} afirmaciones validadas, {len(stages)} etapas, {sum(len(s["texto"].split()) for s in stages)} palabras y {len(histories)} propuestas de historia.')
