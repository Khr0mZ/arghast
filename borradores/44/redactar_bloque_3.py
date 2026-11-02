"""Fichas del bloque final de 44 tras lectura íntegra de sus 839 segmentos."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import validate_fact

ROWS = json.loads((ROOT / 'borradores/44/bloque_3_segmentos.json').read_text(encoding='utf-8'))
SOURCE = ROOT / 'xoltacan_subtitulos/subtitulos/44 - KAfKPeZImT4.es-orig.vtt'
facts = []


def fact(number, title, statement, start, end, cue_start, entities, limitation='', kind='hecho_confirmado'):
    cue = next(row for row in ROWS if row['inicio'] == cue_start)
    row = dict(id=f'44-{number}', titulo=title, tipo=kind, afirmacion=statement,
               inicio=start, fin=end, cita=cue['texto_original'],
               evidencia_cue=dict(inicio=cue['inicio'], fin=cue['fin'], texto=cue['texto_original']),
               entidades=entities, ambito='extracción del ingrediente y regreso a Cuicapalli',
               conocedores=[], conocimiento_personaje='desconocido',
               nota_conocimiento='Acceso de Madame Oghma sin establecer en este pasaje.',
               confianza='lectura de subtítulos; audio no cotejado', limitacion=limitation)
    validate_fact(row, SOURCE)
    facts.append(row)


fact(201, 'Guayacán aclara que sujeta el cuello para ayudar a Leona',
     'Tlachka intenta forzar la mandíbula superior de la criatura para abrirla. El director interpreta inicialmente que Guayacán está cerrando la boca con Leona dentro, pero este aclara que solo quiere estabilizar el cuello para que su maestra pueda extraer las espinas. El director acepta la corrección; la primera tirada para agarrar la boca no consigue abrirla.',
     '01:19:07.360', '01:20:46.870', '01:20:07.239', ['Guayacán', 'Tlachka', 'Leona', 'Devorafango'],
     'La aclaración sustituye la primera interpretación de cerrar la boca. No se narra un intento deliberado de encerrar o asfixiar a Leona.')
fact(202, 'La criatura golpea con la cola y Leona extrae otra espina',
     'La criatura no puede morder bien mientras la sujetan del cuello, pero golpea a Ayoto con la cola cuando sigue en el suelo. Leona continúa arrancando espinas desde el interior y consigue extraer otra.',
     '01:20:46.880', '01:22:15.950', '01:22:10.880', ['Ayoto', 'Leona', 'Devorafango', 'Espinas del Devorafango'],
     'El perjuicio de estar en el suelo no equivale a inconsciencia. El texto no identifica por posición izquierda o derecha una espina especial.')
fact(203, 'Guayacán inmoviliza a la criatura en el suelo',
     'Guayacán refuerza su agarre por el cuello para dejar a la criatura restringida y facilitar la salida de Leona. Supera la tirada de atletismo y el director confirma que la mantiene sujeta contra el suelo. Intenta además golpearla en el ojo con el pico de su traje, aunque ese ataque no logra efecto.',
     '01:22:18.910', '01:24:46.149', '01:23:43.239', ['Guayacán', 'Leona', 'Devorafango'],
     'El pico pertenece al traje que describe Guayacán; no modifica su especie ni demuestra que tenga un pico anatómico.')
fact(204, 'Ayoto se levanta y combate cegado por el barro',
     'El director representa una intervención del chat mediante barro de las espinas de la cola que entra en los ojos de Ayoto y lo ciega. Ayoto se levanta, se orienta por el oído y trata de golpear a la criatura que sabe que tiene delante. Los ataques discutidos en este turno no alcanzan.',
     '01:24:46.159', '01:27:11.750', '01:25:15.440', ['Ayoto', 'Devorafango'],
     'La ceguera se atribuye al barro y al chat; no se diagnostica veneno ni una lesión ocular permanente. No se fija una duración que los subtítulos no completan.')
fact(205, 'Tlachka abre la mandíbula y saca a Leona con las espinas',
     'Con la criatura restringida, Tlachka vuelve a abrirle la boca hasta dejarla casi vertical. Ve a Leona arrancando espinas dentro, mantiene la mandíbula inferior con una pierna y le ofrece la mano. Leona acepta; Tlachka la saca con el ingrediente. Ella espera que las dos espinas recogidas sean suficientes.',
     '01:27:11.760', '01:28:35.830', '01:28:18.920', ['Tlachka', 'Leona', 'Guayacán', 'Devorafango', 'Espinas del Devorafango'],
     'La salida se representa expresamente, sin asumir un rescate anterior. El número de dos queda reiterado al entregar las púas a Parroter.')
fact(206, 'Leona hiere a la criatura y Guayacán la remata',
     'La criatura atrapada falla su siguiente colazo. Ya fuera de ella, Leona grita y encadena varios ataques, incluido un golpe adicional tras un crítico. Guayacán mantiene el agarre, aprieta para asfixiarla y usa el pico del traje contra sus ojos. Después de ese ataque, el director confirma que han destrozado y derrotado a la criatura.',
     '01:28:35.840', '01:31:52.070', '01:31:41.199', ['Leona', 'Guayacán', 'Devorafango'],
     'La muerte se confirma tras la intervención de Guayacán, sin adjudicar todo el combate a un único participante ni inventar un golpe de Ayoto en ese turno.')
fact(207, 'Ayoto y Tlachka arrastran el cadáver hacia Cuicapalli',
     'Ayoto y Tlachka deciden llevarse la criatura para obtener raciones y aprovechar su caparazón. La arrastran con dificultad; sus espinas se les clavan. Tlachka rompe parte de las púas de la cola con su arma para crear un lugar por donde agarrarla y continúan hasta Cuicapalli con el enorme cadáver.',
     '01:31:52.080', '01:36:43.790', '01:35:50.440', ['Ayoto', 'Tlachka', 'Devorafango', 'Cuicapalli', 'Caparazón de la criatura de la cueva'],
     'La decisión de comerla y las propuestas de aprovechar piel o partes no prueban todavía una comida cocinada, una venta ni la fabricación de equipo. La grafía del arma fluctúa y no se crea un arma nueva por cada variante.')
fact(208, 'Parroter recibe dos espinas y empieza a preparar el remedio',
     'Leona y Guayacán vuelven a Parroter. Leona anuncia que tiene dos espinas y explica que las arrancaron con la criatura viva. El alquimista los reprende porque había dicho que no era necesario matarla; Leona niega haber dado ella el golpe final. Parroter toma una púa, la rompe y tritura en su mesa de alquimia y comienza una poción que tardará un poco. También advierte que comer esa criatura les sentará mal.',
     '01:36:45.280', '01:38:38.750', '01:38:14.480', ['Parroter', 'Leona', 'Guayacán', 'Espinas del Devorafango', 'Devorafango'],
     'La reprimenda no invalida que el ingrediente se extrajera en vida. El aviso alimentario es de Parroter y no equivale a una intoxicación ya sufrida por los compañeros.')
fact(209, 'Ayoto pide un artesano del norte y paga a Tacha',
     'Junto al cadáver se discute cómo separar el caparazón para fabricar otro escudo. Ayoto pregunta dónde encontrar a quien trabaja pieles y le indican una tienda al norte. Antes de ir, entrega dos monedas de oro a Tacha porque suele darles de comer y cree que no le han pagado.',
     '01:38:38.760', '01:40:34.310', '01:40:17.599', ['Ayoto', 'Tacha', 'Tlachka', 'Caparazón de la criatura de la cueva', 'Cuicapalli'],
     'El pago a Tacha se distingue de la promesa de pagar al herrero. No se fija un precio de fabricación del nuevo escudo.')
fact(210, 'El herrero exige que Ayoto lleve el material a la tienda',
     'Ayoto llega herido a la tienda del norte y ofrece pagar e invitar a comer al artesano si lo ayuda a trabajar la criatura. El hombre no quiere dejar la tienda sola y pide que le traigan el cadáver. Ayoto propone que Baton vigile, pero el artesano lo rechaza llamándolo ladrón. Baton niega haber robado a nadie; Ayoto insiste en la invitación y regresa sin lograr que el herrero abandone su puesto.',
     '01:41:12.400', '01:43:26.629', '01:42:16.119', ['Ayoto', 'Herrero de Cuicapalli', 'Baton', 'Cuicapalli'],
     'La acusación contra Baton pertenece al herrero y queda contestada, sin prueba independiente de un robo. El oficio de herrero se confirma al describir la salida de Ayoto; no se le asigna el nombre Armin ni se confunde con el artesano de Shiaru.')
fact(211, 'Leona y Guayacán priorizan descansar y comer',
     'Guayacán se dirige a Leona como maestra y pregunta si deberían hacer algo por la criatura que los otros se han llevado. Leona considera que ya consiguieron el ingrediente, tiene hambre tras el combate y propone comer. Guayacán admite que tampoco les vendría mal un descanso.',
     '01:43:32.159', '01:44:11.669', '01:43:35.480', ['Leona', 'Guayacán'],
     'La conversación acredita el trato de maestra, no una orden religiosa o un rango nuevo. Proponer descansar no documenta todavía un descanso largo o una curación.')
fact(212, 'Guayacán usa su oficio de peletero para separar el caparazón',
     'Ayoto vuelve para pedir ayuda con el caparazón que quiere convertir en un segundo escudo. Guayacán explica que sabe tratar cuero y criaturas escamosas por su formación de peletero. El director admite una tirada con sus herramientas. Logra extraer piezas, pero el corte no queda perfecto y el trabajo le lleva un rato.',
     '01:44:11.679', '01:47:40.390', '01:46:48.599', ['Guayacán', 'Ayoto', 'Caparazón de la criatura de la cueva', 'Devorafango'],
     'El caparazón es un exoesqueleto, aclarado después por el director; no se convierte en piel convencional. Extraer piezas no significa haber fabricado el escudo.')
fact(213, 'Tlachka limpia y cocina la carne con chile',
     'Mientras Ayoto busca al artesano, Tlachka abre el cadáver, extrae carne y la limpia junto al agua. Después la prepara con chile machacado al fuego. Tacha, que primero la había olido con desagrado, se queda observando la receta por curiosidad y se acerca cuando empieza a oler bien. Tlachka prueba la carne una vez hecha.',
     '01:40:34.320', '01:48:50.350', '01:48:42.000', ['Tlachka', 'Tacha', 'Devorafango', 'Cuicapalli'],
     'Las comparaciones con gamba describen textura y caparazón, sin fijar una especie de bestiario. No se registra una intoxicación ni se demuestra que el calor elimine todos los riesgos mencionados por Parroter.')
fact(214, 'Leona prueba la carne y resiste la salsa más picante',
     'Leona toma una bebida mientras espera, prueba la carne que prepara Tlachka y pide más picante. Moja su porción en la salsa más fuerte disponible y supera la tirada de constitución para soportar el picor. Dice que está buena y continúa comiendo, aunque pide todavía más salsa.',
     '01:48:50.360', '01:50:19.470', '01:49:46.520', ['Leona', 'Tlachka', 'Tacha'],
     'La tirada se refiere al picante añadido. Su éxito no demuestra inmunidad a venenos ni que el plato sea inocuo a largo plazo.')
fact(215, 'Ayoto reúne el exoesqueleto para encargar un escudo',
     'Guayacán entrega a Ayoto las piezas extraídas. Discuten la diferencia entre escamas y caparazón hasta que el director aclara que se trata de un exoesqueleto como el de una gamba. Ayoto agradece la ayuda, propone cortar dedos de la criatura para decorar el escudo como el que ya lleva y se dispone a trasladar el material al herrero. Guayacán le ofrece el brazo al verlo caminar con tanta dificultad; los dos avanzan apoyándose hacia la tienda.',
     '01:50:19.480', '01:53:33.709', '01:53:29.719', ['Ayoto', 'Guayacán', 'Herrero de Cuicapalli', 'Caparazón de la criatura de la cueva'],
     'El nuevo escudo sigue siendo un proyecto. No se muestra un encargo aceptado, pago al herrero, acabado o estadística de armadura. El apoyo mutuo no equivale a una curación.')
fact(216, 'El remedio de Parroter reduce las venas negras de Eromov',
     'El cierre entra en la casa de Eromov, que reposa cubierto con hojas, con la piel grisácea y venas negras por el cuerpo. Parroter termina la preparación aún pastosa y se la administra mientras observan los guardias. Las venas empiezan a menguar; el alquimista sonríe, pide que avisen a Leona y anuncia que hará más porque Eromov se pondrá mejor. El director cierra diciendo que parece que mejorará bastante.',
     '01:53:33.719', '01:55:35.760', '01:54:33.239', ['Eromov', 'Parroter', 'Leona', 'Espinas del Devorafango', 'Cuicapalli'],
     'Se confirma una mejoría visible tras administrar el remedio, sin despertar, conversación, alta médica ni curación completa. La continuación del tratamiento es la intención de Parroter; no se narra una segunda dosis ya administrada.')

stages = [
    dict(titulo='Dos espinas y una salida', texto='Leona sigue dentro de la criatura mientras Tlachka intenta abrirle la mandíbula. Guayacán aclara que no pretende cerrarla con su maestra atrapada: quiere estabilizar el cuello para ayudarla a extraer el ingrediente. El primer intento de apertura falla. La criatura golpea con la cola a Ayoto, aún en el suelo, y Leona logra arrancar otra espina desde dentro. Guayacán refuerza el agarre hasta inmovilizar al monstruo contra el suelo. Ayoto se levanta cegado por el barro que le ha entrado en los ojos y trata de orientarse para combatir. Tlachka consigue abrir la boca casi en vertical, sujeta una mandíbula con la pierna y ofrece la mano a Leona. Ella se deja sacar con las dos espinas que esperaba encontrar.', referencias=['44-201', '44-202', '44-203', '44-204', '44-205']),
    dict(titulo='El regreso y el remedio', texto='La criatura, todavía retenida, no logra acertar su siguiente colazo. Leona vuelve al ataque con varios golpes y Guayacán termina de abatirla usando el agarre y el pico de su traje. Ayoto y Tlachka deciden arrastrarla hasta Cuicapalli para obtener comida y materiales, aunque el peso y las espinas convierten el traslado en otra dificultad. Tlachka rompe varias púas de la cola para poder sujetarla mejor. Leona y Guayacán entregan las espinas a Parroter y confirman que las arrancaron cuando el animal seguía vivo. El alquimista los reprende por haberlo matado, algo que no les había pedido. Aun así toma una púa, la tritura y empieza a preparar la poción. Les anuncia que tardará un poco y advierte de que comer la criatura podría sentarles mal.', referencias=['44-206', '44-207', '44-208']),
    dict(titulo='Carne, caparazón y un escudo pendiente', texto='Tlachka empieza a limpiar carne junto al agua y la cocina con chiles mientras Tacha observa con creciente curiosidad. Leona, hambrienta tras el combate, prueba el plato y añade la salsa más fuerte que encuentra; aguanta su picor y sigue comiendo. Ayoto quiere aprovechar el caparazón para un nuevo escudo. Paga a Tacha dos monedas por sus comidas y busca al artesano del norte, pero este exige que le lleven el material: no abandonará su tienda ni acepta que Baton la vigile. Guayacán ofrece su formación de peletero y logra separar piezas del exoesqueleto, aunque los cortes no quedan perfectos. Se las entrega a Ayoto, que piensa añadir dedos de la criatura como adornos. Ambos, todavía muy heridos, avanzan apoyándose hacia el herrero. La fabricación queda por hacer.', referencias=['44-209', '44-210', '44-211', '44-212', '44-213', '44-214', '44-215']),
    dict(titulo='La primera mejoría de Eromov', texto='Mientras sus compañeros comen y trasladan el material, Parroter termina el remedio en la casa de Eromov. El líder permanece acostado bajo una cubierta de hojas, con la piel grisácea y las venas negras visibles por todo el cuerpo. Los guardias observan al alquimista administrar la preparación aún pastosa. Poco a poco las venas empiezan a menguar. Parroter sonríe, pide que avisen a Leona y anuncia que preparará más para continuar ayudándolo. El capítulo termina con una mejoría visible y una esperanza concreta de recuperación, aunque Eromov todavía no se levanta ni se declara completamente curado.', referencias=['44-216']),
]


def history(name, kind, title, text, references, new=False, description='', note=''):
    return dict(nombre=name, tipo=kind, nueva=new, descripcion=description, nota=note,
                etapas=[dict(titulo=title, texto=text, referencias=references)])


histories = [
    history('Leona', 'personaje', 'Las espinas para Eromov', 'Leona arranca otra espina desde el interior de la criatura y acepta la mano de Tlachka para salir con el ingrediente. Después la ataca antes de que Guayacán la remate. Entrega dos espinas a Parroter y confirma que se extrajeron en vida, aunque recibe una reprimenda por la muerte del animal. Mientras el alquimista trabaja, prueba la carne preparada por Tlachka. Parroter pide que la avisen al ver mejorar a Eromov.', ['44-202', '44-205', '44-206', '44-208', '44-214', '44-216']),
    history('Guayacán', 'personaje', 'El agarre, la ayuda y el oficio', 'Guayacán sujeta el cuello de la criatura para facilitar el trabajo y la salida de Leona, a quien llama maestra. La inmoviliza contra el suelo y termina de abatirla tras los ataques de ella. De vuelta en Cuicapalli participa en la entrega del ingrediente. Después explica su formación de peletero, separa piezas de exoesqueleto con un corte imperfecto y ayuda al malherido Ayoto a llevarlas al herrero.', ['44-201', '44-203', '44-206', '44-208', '44-211', '44-212', '44-215']),
    history('Tlachka', 'personaje', 'El rescate y la cocina', 'Tlachka intenta abrir la boca de la criatura y, cuando Guayacán la restringe, logra sacar a Leona con las espinas. Tras la victoria arrastra el cadáver con Ayoto y quita púas de la cola para facilitar el traslado. En Cuicapalli limpia carne y la cocina con chiles ante Tacha, mientras Leona prueba el plato y busca más picante.', ['44-201', '44-205', '44-207', '44-213', '44-214']),
    history('Ayoto', 'personaje', 'Del barro a un proyecto de escudo', 'Ayoto recibe colazos mientras está en el suelo y el barro lo deja temporalmente cegado por una intervención del chat. Tras la victoria ayuda a arrastrar el cadáver y quiere aprovechar su caparazón para otro escudo. Busca a un artesano que exige recibir el material en su tienda. Guayacán extrae piezas y lo acompaña, sosteniéndolo cuando sus heridas le dificultan caminar. El escudo no llega a fabricarse en escena.', ['44-202', '44-204', '44-207', '44-209', '44-210', '44-212', '44-215']),
    history('Parroter', 'personaje', 'Una preparación que empieza a funcionar', 'Parroter recibe dos espinas arrancadas con la criatura viva y reprende a los compañeros por haberla matado innecesariamente. Tritura una púa y prepara el remedio. En el cierre lo administra a Eromov; las venas negras del líder menguan ante sus guardias. El alquimista sonríe, pide avisar a Leona y se propone preparar más, sin dar aún por terminada la recuperación.', ['44-208', '44-216']),
    history('Eromov', 'personaje', 'Las venas negras menguan', 'Eromov permanece postrado, con la piel grisácea y las venas negras marcadas por la enfermedad. Parroter le administra el preparado hecho con las espinas recuperadas y los signos negros empiezan a retroceder. La sesión cierra con una mejoría visible y el propósito de seguir tratándolo, sin representar su despertar ni una curación completa.', ['44-216']),
    history('Tacha', 'personaje', 'La carne que despierta su curiosidad', 'Ayoto entrega a Tacha dos monedas porque suele alimentar a los compañeros y cree que no le han pagado. El tabernero huele primero la carne con disgusto, pero observa cómo Tlachka la limpia y cocina con chile. Cuando el aroma mejora se acerca con interés, mientras Leona prueba el plato y añade la salsa más fuerte.', ['44-209', '44-213', '44-214']),
    history('Baton', 'personaje', 'La tienda que no le confían', 'Ayoto propone que Baton vigile la tienda para que el herrero pueda salir a examinar la criatura. El artesano se niega, lo llama ladrón y Baton responde que no ha robado a nadie. La escena conserva la acusación y su negativa sin probar el supuesto robo ni mostrar que se le entregue la tienda.', ['44-210']),
    history('Cuicapalli', 'lugar', 'El ingrediente llega al alquimista', 'Los compañeros vuelven a Cuicapalli arrastrando la criatura abatida. Leona y Guayacán llevan las espinas a Parroter, mientras Tlachka cocina parte de la carne y Ayoto busca ayuda para trabajar el caparazón. En la casa de Eromov, ante sus guardias, el remedio empieza a reducir las venas negras del líder.', ['44-207', '44-208', '44-209', '44-213', '44-215', '44-216']),
    history('Devorafango', 'personaje', 'El ingrediente y el aprovechamiento del cadáver', 'Guayacán la inmoviliza mientras Leona extrae espinas desde dentro de su boca. Tlachka abre la mandíbula y la saca. Después Leona la hiere y Guayacán la remata. Ayoto y Tlachka arrastran el cadáver hasta Cuicapalli; parte de su carne se cocina y Guayacán separa piezas del duro exoesqueleto. Sus espinas permiten a Parroter preparar un remedio con el que Eromov muestra mejoría.', ['44-201', '44-202', '44-203', '44-205', '44-206', '44-207', '44-212', '44-213', '44-216'], True, 'Gran criatura de la cueva, provista de espinas, cola y exoesqueleto, de la que se obtiene el ingrediente para tratar a Eromov.', 'Nombre descriptivo coordinado con el bloque anterior. La comparación con una gamba y la denominación incompleta de lodo no fijan una especie o nombre de bestiario.'),
    history('Espinas del Devorafango', 'objeto', 'De la extracción al remedio', 'Leona recoge dos espinas mientras la criatura aún está viva y sale con ellas gracias a Tlachka. De regreso, Parroter acepta el ingrediente, tritura una púa y prepara una poción todavía pastosa. La administra a Eromov y sus venas negras empiezan a menguar. No se muestran dosis completas posteriores ni una curación definitiva.', ['44-202', '44-205', '44-208', '44-216'], True, 'Espinas extraídas en vida de la criatura de la cueva y utilizadas por Parroter contra la enfermedad de Eromov.', 'Identidad de ingrediente compartida con el bloque anterior. No confundirlas con las púas de la cola que Tlachka rompe para transportar el cadáver ni con el fragmento de espada de Iktan.'),
    history('Caparazón de la criatura de la cueva', 'objeto', 'Material para un escudo por hacer', 'Ayoto pretende fabricar un nuevo escudo con el exoesqueleto de la criatura. Guayacán aplica su formación de peletero para separar piezas, aunque sin cortes perfectos. Ayoto las recibe y piensa añadir dedos del animal como adorno antes de ir al herrero, ayudado por Guayacán. La sesión no muestra la fabricación del escudo.', ['44-207', '44-209', '44-212', '44-215'], True, 'Piezas de exoesqueleto recuperadas por Guayacán para el proyecto de escudo de Ayoto.', 'Objeto conservado como material; no llamar escudo terminado ni atribuirle defensa, magia, precio o una entrega que no se narra.'),
    history('Herrero de Cuicapalli', 'personaje', 'El material debe llegar a la tienda', 'Ayoto busca al artesano del norte para que trabaje el cuerpo de la criatura. El herrero no quiere dejar su tienda sola y rechaza que Baton la vigile, acusándolo de ladrón. Pide que le lleven el material. Más tarde Ayoto y Guayacán se dirigen hacia él con piezas del caparazón, sin representar aún un encargo aceptado o una pieza terminada.', ['44-210', '44-215'], True, 'Artesano de la tienda del norte de Cuicapalli al que Ayoto quiere llevar el exoesqueleto para un escudo.', 'Sin nombre propio confirmado en este tramo. Se mantiene distinto de Armin, herrero de Shiaru. No inferir una identidad solo por compartir oficio; revisar referencias anteriores al herrero tabaxi de Cuicapalli.'),
]

document = dict(bloque=3, lectura_completa=True, primer_segmento='c003355', ultimo_segmento='c005033',
    etapas=stages, afirmaciones=facts,
    misiones=[
        'Conseguir el ingrediente para Eromov: Leona sale de la criatura con dos espinas extraídas en vida y las entrega a Parroter. El alquimista prepara y administra el remedio con una primera mejoría visible del líder (44-202, 44-205, 44-208, 44-216).',
        'Sacar a Leona de la criatura: Guayacán la restringe, Tlachka abre la boca y Leona acepta la mano que la lleva al exterior antes del remate (44-201, 44-203, 44-205–44-206).',
        'Aprovechar el exoesqueleto para un nuevo escudo de Ayoto: Guayacán extrae piezas y ambos se dirigen al herrero; la fabricación, aceptación del encargo y entrega quedan sin mostrar (44-209–44-210, 44-212, 44-215).',
        'Reponer fuerzas tras el combate: Tlachka cocina carne con chile y Leona la prueba. Ayoto y Guayacán siguen muy heridos al caminar juntos; no se muestra una curación del grupo (44-211, 44-213–44-215).',
    ],
    preguntas=[
        '¿Se recuperará completamente Eromov con las siguientes dosis? La primera preparación reduce sus venas negras, pero no se narra que despierte ni que termine la enfermedad (44-216).',
        '¿Qué fabricará el herrero con el exoesqueleto recuperado y en qué condiciones? Ayoto quiere otro escudo y lleva material, sin encargo aceptado, precio o pieza terminada (44-210, 44-212, 44-215).',
        '¿Cómo se recuperarán Ayoto y Guayacán de las heridas? Terminan apoyándose para caminar hacia el herrero, sin curación o descanso completo documentados (44-215).',
        '¿Tendrá alguna consecuencia comer la carne pese al aviso de Parroter? Se prueba el plato y se resiste el picante, pero no se narra una intoxicación ni un seguimiento posterior (44-208, 44-213–44-214).',
    ],
    contradicciones=[
        'Guayacán corrige al director: sujeta el cuello para estabilizar, no intenta cerrar la boca con Leona dentro. La tirada fallida de apertura es previa al segundo intento de Tlachka que sí la extrae (44-201, 44-203, 44-205).',
        'La muerte de la criatura se confirma después de los ataques de Leona y el remate de Guayacán. La negación de Leona ante Parroter se refiere a no dar el golpe final y no borra su participación en el combate (44-206, 44-208).',
        'La ceguera de Ayoto se atribuye al barro y al chat. No llamar venenosos a esos pinchazos ni diagnosticar un daño ocular permanente (44-204).',
        'El director aclara que escamas y caparazón aluden al exoesqueleto. No se extrae una piel nueva distinta ni se crea un segundo animal por esas palabras (44-212, 44-215).',
        'Tlachka rompe púas de la cola para transportar el cadáver; esto se distingue de las dos espinas extraídas en vida y entregadas a Parroter para el remedio (44-202, 44-205, 44-207–44-208).',
        'El éxito de la salvación de Leona corresponde al picante. No demuestra que el plato carezca de toxicidad ni confirma el malestar futuro que Parroter había advertido (44-208, 44-214).',
        'Eromov mejora visiblemente tras recibir el preparado, pero todavía no se levanta ni se declara una curación completa. El deseo de hacer más poción no equivale a una segunda dosis ya administrada (44-216).',
    ],
    nombres_dudosos=[
        'Traska, Trasca, Tlatchka y Tlachka se agrupan como Tlachka por continuidad de sus turnos y su presencia junto a Ayoto. No confundirlo con Tacha, tabernero hiena que observa la cocina (44-201, 44-205, 44-207, 44-213).',
        'Yoto y Ayoto designan al goliat herido; Guacayacán, Guayacá y Guayacán al monje que sujeta a la criatura. Leona es la harengon, no Naór leonina (44-201–44-205, 44-215).',
        'Parter, Parot y Parroter corresponden al alquimista kenku de Cuicapalli por su mesa, oficio y tratamiento de Eromov. La expresión aislada que parece pedir volver a Pablo no fija una persona nueva (44-208, 44-216).',
        'La criatura recibe censura automática en gran parte de sus menciones. Se conserva el nombre editorial descriptivo, el exoesqueleto y la comparación con una gamba, sin fijar un nombre de bestiario a partir de la expresión incompleta de lodo (44-206–44-207, 44-212–44-213, 44-215).',
        'El herrero de la tienda del norte pertenece a Cuicapalli. No se le asigna el nombre Armin, que corresponde al herrero de Shiaru, ni se mezcla con Tacha por las peticiones de comida (44-209–44-210).',
        'Las variantes Macawiel y Mac Winter del arma de Tlachka no crean varias armas ni fijan en este tramo un nombre propio confirmado (44-207, 44-213).',
    ],
    continuidad=[
        'P30-001 recibe avance sustancial: Parroter consigue un preparado, lo administra y reduce venas negras de Eromov. Marcar parcial mientras no se documente recuperación completa o desenlace (44-208, 44-216).',
        'P40-006: ahora hay tratamiento y mejoría de Eromov, sin probar que provengan de hombres, recetas o protecciones enviados por Walulu. No cerrar la procedencia de aquella ayuda solo por existir una cura local (44-208, 44-216).',
        'P30-002 y P41-006: el remedio no identifica al autor del envenenamiento ni demuestra igualdad de los viales verdes, la muestra del claro y el tóxico de Eromov (44-216).',
        'La trama del escudo de Ayoto avanza a material recuperado y transporte hacia un herrero; no hay un nuevo escudo terminado que añadir como si ya se usara (44-212, 44-215).',
    ], historias_entidades=histories)

path = ROOT / 'borradores/44/entrega_3.json'
path.write_text(json.dumps(document, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'{len(facts)} evidencias verificadas; {len(histories)} historias; {sum(len(s["texto"].split()) for s in stages)} palabras de relato; 839 segmentos leídos.')
