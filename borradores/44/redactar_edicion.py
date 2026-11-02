"""Cotejo editorial de los tres bloques: identidades, desenlaces e historias completas."""
from preparar import ROOT, FOLDER, read_json, save


def main():
    deliveries = [read_json(FOLDER / f'entrega_{n}.json') for n in (1, 2, 3)]
    stages = [s.copy() for d in deliveries for s in d['etapas']]
    stages[1]['titulo'] = 'Espinas arrancadas en vida'
    stages[2]['texto'] = stages[2]['texto'].replace('El turno pasa a Ayoto con el combate todavía abierto.', 'Ayoto se prepara para entrar en combate.')
    stages[6]['texto'] = stages[6]['texto'].replace('Al advertir el problema de la boca cerrada,', 'Al advertir que Leona sigue dentro,')
    stages[7]['texto'] = stages[7]['texto'].replace('con las dos espinas que esperaba encontrar.', 'con las dos espinas que ha arrancado.')
    aliases = {'Espinas del devorafango':'Espinas del Devorafango',
               'Caparazón de la criatura de la cueva':'Caparazón del Devorafango'}
    proposals = [e for d in deliveries for e in d['historias_entidades']]
    histories = []

    def history(name, title, text, *, kind=None, description=None, note=None):
        parts = [p for p in proposals if aliases.get(p['nombre'], p['nombre']) == name]
        assert parts, name
        refs = list(dict.fromkeys(r for p in parts for s in p['etapas'] for r in s['referencias']))
        histories.append(dict(nombre=name, tipo=kind or parts[0]['tipo'],
            descripcion=description if description is not None else parts[0]['descripcion'],
            nota=note if note is not None else parts[0]['nota'],
            etapas=[dict(titulo=title, texto=text, referencias=refs)]))

    history('Leona', 'Las espinas para salvar a Eromov',
        'De nuevo en Cuicapalli tras su misión de aviso, Leona busca rastros de las serpientes y participa en las rondas de vigilancia. Parroter la llama ante el empeoramiento de Eromov y le encarga espinas de la boca de un devorafango, que deben arrancarse con el animal vivo. Reúne a Guayacán, Ayoto y Tlachka y los guía hacia una cueva junto a un lago donde jugaba de pequeña. Allí entra voluntariamente en una masa de moho buscando el ingrediente; Ayoto logra sacarla ocupando su lugar. Cuando aparece el devorafango, se introduce en su boca. Clava el hacha para afirmarse y el recuerdo de Eromov cuando la encontró de niña aviva su esfuerzo. Arranca dos espinas y acepta la mano de Tlachka para salir. Después ataca al animal antes del remate de Guayacán. Entrega las espinas a Parroter, confirma que las obtuvo en vida y prueba la carne que prepara Tlachka. El alquimista pide avisarla al ver mejorar al dirigente. Ni este vínculo de infancia ni su responsabilidad en la misión equivalen a una adopción formal o una investidura como sucesora.')
    history('Guayacán', 'Vigilancia, rescate y oficio de peletero',
        'Guayacán cuenta que ha cuidado Cuicapalli mientras Leona estaba fuera, estudiando sus defensas y el ánimo de sus habitantes. Alterna la voz al reconocer a Tlachka, sin revelar su especie. Acompaña a su maestra ante Parroter y a la cueva. La angustia al verla dentro del moho lo hace fallar algunos golpes, pero acaba aturdiendo a la masa para facilitar el rescate. El devorafango lo hiere con ácido y un mordisco que lo deja al límite de sus fuerzas. Usa curaciones y aclara que su agarre pretende estabilizar el cuello para que Leona pueda trabajar. Inmoviliza al animal y, después de la salida de ella y sus ataques, lo remata con el pico de su traje. De vuelta participa en la entrega del ingrediente. Su formación de peletero le permite extraer piezas del exoesqueleto, aunque los cortes no quedan perfectos. Termina ayudando al también malherido Ayoto a llevarlas al herrero; el apoyo no sustituye una curación.')
    history('Ayoto', 'Dos rescates y un escudo por hacer',
        'Ayoto vuelve a aparecer en Cuicapalli, relata su regreso de Iktan y recuerda sus viajes por el mar y el bosque. Comparte comida con los compañeros y un guardia antes de aceptar la misión de Leona. Una fruta lo hace temer a su propia sombra. En la cueva atrae los ataques del moho, abre un hueco con sus escudos y saca a Leona ocupando su lugar dentro. Después resiste el ácido del devorafango, salta a su lomo y lo derriba, sufriendo los pinchazos de las espinas y los golpes de su cola. El barro lo ciega durante una intervención del chat. Tras la victoria arrastra el cadáver con Tlachka y quiere aprovechar el caparazón para un nuevo escudo. Paga a Tacha dos monedas por la comida y busca al herrero del norte, que exige recibir el material en su tienda. Guayacán separa las piezas y lo ayuda a caminar hacia ella. No se representa la fabricación, el precio ni la entrega de otro escudo.')
    history('Tlachka', 'Del rescate a la cocina de Cuicapalli',
        'Tlachka recuerda su estancia en Iktan, donde buscó descanso apartado de Coyote, y vuelve a preparar frutas y mazorcas junto a Tacha. Deja la comida para acompañar la búsqueda del ingrediente de Eromov. Al hurgar en el moho encuentra huesos aparentemente humanoides, no las espinas buscadas. Sus golpes dejan a la masa moribunda. Ante el devorafango ataca el vientre sin espinas con el arma cargada por el ácido recibido. Cuando Guayacán inmoviliza al animal, abre sus mandíbulas y ofrece a Leona la mano para sacarla con el ingrediente. Después ayuda a Ayoto a arrastrar el cadáver, rompe púas de la cola para facilitar el traslado y cocina carne con chiles junto al agua. Tacha observa la preparación y Leona prueba el plato. Su presencia en Cuicapalli no acredita que se haya revocado formalmente su destierro.')
    history('Eromov', 'La primera mejoría tras el remedio',
        'Eromov sigue postrado en Cuicapalli, temblando y tosiendo bajo las hojas con que Parroter lo cuida. Apenas levanta la trompa para saludar a Leona. El alquimista teme que no aguante mucho más y solicita un ingrediente que obliga a una nueva expedición. Durante la extracción, Leona recuerda que Eromov la encontró de pequeña; la escena no reconstruye toda su infancia. Al cierre Parroter administra la preparación ante los guardias. Las venas negras visibles sobre la piel grisácea empiezan a menguar y el alquimista anuncia que hará más. Hay una mejoría representada, sin una recuperación completa ni un regreso del dirigente a sus funciones.')
    history('Parroter', 'Un antídoto que empieza a funcionar',
        'Parroter sigue atendiendo a Eromov y manda llamar a Leona. Dice haber avanzado con los materiales recibidos, sin identificar por separado todas sus procedencias. Pide espinas del interior de la boca de un devorafango, extraídas mientras viva, y describe su hábitat húmedo y el peligro de sus secreciones corrosivas. Leona y Guayacán regresan con dos espinas obtenidas en vida. El alquimista los reprende por haber matado al animal, algo que no era necesario para el encargo, pero acepta el ingrediente. Tritura una púa y prepara el remedio. Tras administrarlo ve menguar las venas negras de Eromov, pide avisar a Leona y anuncia que hará más para continuar el tratamiento.')
    history('Tacha', 'El plato que despierta su curiosidad',
        'Tacha sirve lechón mientras Tlachka prepara mazorcas junto a su cocina. La reunión se interrumpe cuando Parroter llama a Leona; Ayoto y Tlachka siguen comiendo hasta que ella vuelve para pedirles ayuda. Tras la expedición, Ayoto le entrega dos monedas porque cree que no han pagado sus comidas. Tacha huele con desagrado la carne del animal traído, pero observa cómo Tlachka la limpia y cocina con chiles. Cuando el aroma mejora se acerca con curiosidad y Leona prueba el plato con la salsa más fuerte. Estas comidas no aportan una confesión sobre el envenenamiento anterior de Eromov.')
    history('Baton', 'La tienda que no le confían',
        'Ayoto propone que Baton vigile la tienda para que el herrero pueda salir a examinar la criatura. El artesano se niega, lo llama ladrón y Baton responde que no ha robado a nadie. No se prueba el supuesto robo ni se le entrega la vigilancia del establecimiento.')
    history('Cuicapalli', 'Una expedición y el regreso del ingrediente',
        'Leona y Guayacán mantienen las rondas de vigilancia mientras Eromov sigue enfermo. Tlachka y Ayoto se reúnen con ellos junto a la cocina de Tacha. La llamada urgente de Parroter lleva a los cuatro a buscar espinas en una cueva junto a un lago cercano. Vuelven con el ingrediente y con el cadáver del devorafango. Mientras Tlachka cocina y Ayoto busca ayuda para trabajar el caparazón, el alquimista administra el remedio a Eromov ante sus guardias. Sus venas negras empiezan a menguar. La cura local no demuestra que hayan llegado los expertos esperados de Iktan ni identifica todas las muestras utilizadas.')
    history('El Bocado del Jaguar', 'Una comida antes de la urgencia',
        'El entorno de Tacha reúne de nuevo a los viajeros: Tlachka tuesta mazorcas, el tabernero sirve lechón y Leona y Guayacán comen tras sus rondas. Ayoto se incorpora al encuentro. La reunión se transforma en el reclutamiento para buscar un ingrediente de la cura de Eromov cuando Leona vuelve de hablar con Parroter.')
    history('Cueva del lago cercano a Cuicapalli', 'Dos amenazas en una cueva de la infancia',
        'Al buscar un hábitat húmedo para el devorafango, Leona recuerda una gran cueva junto a un lago donde jugaba con otros niños. Guía allí a sus compañeros, que encuentran barro, olor pestilente y huesos. Una masa de moho se alza cerca de la entrada. Contiene restos aparentemente humanoides y no tiene una boca definida. Leona entra en ella buscando el ingrediente y Ayoto la rescata. Después llega el devorafango y llena la sala de ácido. El grupo combate mientras Leona obtiene espinas desde su boca. La cueva no se identifica con la Hoja Caída, el refugio derrumbado de Citlali o la guarida del dragón.',
        description='Cueva húmeda junto a un lago cercano a Cuicapalli, recordada por Leona desde sus juegos infantiles y visitada al buscar el ingrediente para Eromov.',
        note='Nombre editorial descriptivo, sin topónimo propio confirmado. Sus habitantes y restos se mantienen separados de otras cuevas y focos de veneno de la campaña.')
    history('Masa de moho de la cueva', 'Los huesos del interior',
        'La materia del suelo se levanta junto a Leona y trata de envolverla. Guayacán la golpea y más adelante consigue aturdirla. Cuando Tlachka intenta encontrar una boca, descubre huesos aparentemente humanoides que la masa está consumiendo. Leona entra voluntariamente para buscar una espina, pero solo arranca material hasta que Ayoto abre un hueco y la saca, quedándose dentro. Tras nuevos ataques la masa queda moribunda. Un comentario que la da por muerta se corrige; la llegada del devorafango y su ácido no confirma su destino final ni identifica a las víctimas de los huesos.',
        description='Masa móvil de moho que ataca en la cueva del lago y consume restos de huesos aparentemente humanoides.',
        note='Rival distinto del devorafango. Carece de boca definida y no recibe una especie de bestiario ni una identidad común con los no muertos del claro de Iktan.')
    history('Devorafango', 'El animal buscado y el ingrediente extraído',
        'Parroter describe al devorafango como una criatura peligrosa de cuevas húmedas, capaz de escupir sustancias que queman la piel. El objetivo se distingue de la masa de moho que los viajeros encuentran primero. Después entra un animal enorme cubierto de barro, con ojos saltones, espinas dorsales, protuberancias bucales y una cola poderosa. Escupe ácido sobre la sala. Leona se mete en su boca para extraer las espinas; Ayoto lo derriba y Tlachka ataca su vientre desprotegido. La criatura se incorpora, hiere gravemente a Guayacán y derriba a Ayoto. Guayacán logra inmovilizarla y Tlachka saca a Leona con dos espinas obtenidas en vida. Leona vuelve a golpear y Guayacán la remata. El cadáver llega a Cuicapalli, donde se cocina parte de la carne y se recupera exoesqueleto para un proyecto de escudo.',
        description='Gran criatura de hábitats húmedos que escupe ácido y posee cola, exoesqueleto y espinas dorsales y bucales.',
        note='Nombre provisional leído en «Débora Fango», «Borafango» y variantes. La descripción de Parroter se enlaza con los rasgos del ejemplar encontrado; no se añade una especie de bestiario. Es distinto de la masa de moho.')
    history('Espinas del Devorafango', 'De la boca al remedio',
        'Parroter necesita las espinas bucales del devorafango y exige que se arranquen mientras viva. Tras buscar sin éxito en el moho, Leona entra en la boca del animal y fuerza una protuberancia afirmándose con el hacha. Consigue dos espinas y sale con ayuda de Tlachka. Parroter acepta el ingrediente, tritura una púa y prepara una poción aún pastosa. Al administrarla a Eromov sus venas negras empiezan a menguar, aunque el tratamiento y la recuperación no quedan completos.',
        description='Espinas bucales extraídas del devorafango vivo y utilizadas por Parroter en el remedio de Eromov.',
        note='Se distinguen de las púas de la cola retiradas para transportar el cadáver. La mejoría observada no fija composición, dosis totales o todas las propiedades del ingrediente.')
    history('Caparazón del Devorafango', 'Material para un escudo por hacer',
        'Ayoto quiere un nuevo escudo hecho con el exoesqueleto del animal abatido. El herrero exige que le lleven el material y Guayacán aplica su formación de peletero para separar piezas, con cortes imperfectos. Ayoto las recibe, piensa añadir dedos como adornos y se dirige hacia la tienda apoyado en Guayacán. El capítulo no muestra un encargo aceptado ni un escudo terminado.',
        description='Piezas del exoesqueleto recuperadas por Guayacán para el proyecto de escudo de Ayoto.',
        note='Material conservado, sin estadísticas de defensa, magia, precio o fabricación concluida. No se convierte en otro escudo ya utilizable.')
    history('Herrero de Cuicapalli', 'El material debe llegar a la tienda',
        'Ayoto busca al artesano del norte para trabajar el caparazón del animal. El herrero no quiere dejar su tienda y rechaza que Baton la vigile, acusándolo de ladrón. Pide que le lleven el material. Después Ayoto y Guayacán van hacia él con piezas del exoesqueleto, sin que se represente aún la aceptación del trabajo o la entrega de un escudo.',
        description='Herrero de la tienda del norte de Cuicapalli al que Ayoto quiere llevar material para un nuevo escudo.',
        note='Nombre propio y especie sin confirmar en esta escena. No se identifica automáticamente con el herrero tabaxi de la Forja del Águila de Sangre del capítulo 30 ni con Armin, de Shiaru; compartir oficio no acredita identidad.')

    missions = [
        'Tratar a Eromov: Leona reúne al grupo, consigue dos espinas bucales arrancadas con el devorafango vivo y las entrega a Parroter. El alquimista prepara y administra el remedio; las venas negras menguan, sin recuperación completa representada (44-008–44-013, 44-117, 44-202, 44-205, 44-208, 44-216).',
        'Sacar a Leona de las dos criaturas: Ayoto la extrae del moho intercambiando posiciones. Después Guayacán inmoviliza al devorafango y Tlachka abre sus mandíbulas para sacarla con las espinas (44-109, 44-112, 44-201, 44-203, 44-205).',
        'Aprovechar el caparazón para un nuevo escudo de Ayoto: Guayacán separa piezas y ambos van hacia el herrero. La fabricación, el precio, la aceptación y la entrega quedan sin mostrar (44-209–44-210, 44-212, 44-215).',
        'Reponer fuerzas tras la expedición: Tlachka cocina la carne con chile y Leona la prueba pese al aviso de Parroter. Ayoto y Guayacán siguen muy heridos; no se representa una curación completa o un descanso largo del grupo (44-208, 44-211, 44-213–44-215).',
        'Vigilar Cuicapalli y buscar a las serpientes: Guayacán describe sus cuidados de la ciudad y Leona sus rondas. Los expertos de Iktan siguen siendo esperados y no se identifica al autor material del envenenamiento (44-001, 44-003–44-004, 44-009).',
    ]
    questions = [
        '¿Se recuperará completamente Eromov con el tratamiento posterior? La primera preparación reduce sus venas negras y Parroter anuncia más remedio, sin vuelta a sus funciones o final de la enfermedad (44-216).',
        '¿Qué fabricará el herrero con el exoesqueleto y en qué condiciones? Ayoto lleva material para otro escudo, sin un encargo aceptado, precio o pieza terminada (44-210, 44-212, 44-215).',
        '¿Quiénes son los restos humanoides que consume el moho y cuál es el destino de la masa? Queda moribunda antes de la descarga ácida, sin una muerte confirmada (44-102, 44-110–44-111).',
        '¿Cómo encontró Eromov a Leona cuando era pequeña y qué historia comparten desde entonces? El recuerdo impulsa la extracción sin reconstruir su infancia ni fijar toda su filiación (44-117).',
        '¿Tendrá consecuencias comer la carne del devorafango pese al aviso de Parroter? Se prueba el plato y Leona soporta el picante, sin una intoxicación o seguimiento posterior mostrados (44-208, 44-213–44-214).',
        '¿Cómo se recuperarán Ayoto y Guayacán de las heridas? Terminan apoyándose para caminar hacia el herrero, sin una recuperación completa o un descanso final representados (44-215).',
    ]
    previous = {q['id']:q for q in read_json(FOLDER / 'seguimiento_antes.json')['preguntas']}
    updates = {}
    def update(qid, answer, refs, pending, state=None):
        updates[qid] = dict(respuesta=answer, referencias=list(dict.fromkeys(previous[qid]['referencias']+refs)), pendiente=pending)
        if state:
            updates[qid]['estado'] = state
    update('P30-001', 'Parroter prepara y administra un remedio con las espinas extraídas del devorafango vivo. Las venas negras de Eromov empiezan a menguar ante sus guardias y el alquimista anuncia que hará más. Ya hay un antídoto utilizado y una mejoría visible; la recuperación completa y la supervivencia posterior siguen sin representarse.',
        ['44-008','44-011','44-117','44-205','44-208','44-216'], 'La evolución con las dosis posteriores y la recuperación completa de Eromov.', 'parcial')
    update('P40-006', 'Walulu había confirmado precauciones tras el aviso de Leona y el grupo de Iktan venció a los adversarios localizados al norte. La escena escrita «Guayacán vigila y Leona vuelve con ayuda de Iktan» documenta que Leona entrega viales y recetas a Parroter, quien empieza a trabajar con ellos; los expertos quedan anunciados. En el capítulo 44 el alquimista prepara y administra el remedio con las espinas y Eromov mejora. Hay entrega de materiales y avance del tratamiento, sin llegada comprobada de los expertos, composición completa del remedio o recuperación definitiva.',
        ['44-001','44-004','44-009','44-208','44-216'], 'La llegada de los expertos prometidos, la recuperación completa de Eromov y el alcance restante de la operación contra Iktan.')
    updates['P40-006']['fuentes_rol'] = [dict(escena='x-1525362897662906398', mensaje_id=mid) for mid in ('1525820723434618981','1525825232810541056')]
    update('P22-003', 'Las fisuras del pico, los dientes y las reparaciones del traje siguen siendo indicios sobre su apariencia. En el capítulo 44 Guayacán alterna la voz normal e impostada y combate usando el pico del traje, sin declarar su especie real ni completar la genealogía del linaje.',
        ['44-005','44-203','44-206'], 'Confirmar su especie real y el linaje declarado.')
    update('P27-002', 'Guayacán había reparado el traje y ahora alterna su voz al reconocer a Tlachka. El pico utilizado en el combate se describe como parte del traje. No revela su identidad precisa ni establece qué personajes conocen el secreto.',
        ['44-005','44-203','44-206'], 'Su identidad precisa y quién conoce el secreto del traje y del pico.')
    update('P27-003', 'Tlachka participa de nuevo en la vida de Cuicapalli: cocina junto a Tacha, acepta la expedición por Eromov y regresa con el cadáver de la criatura. Esa presencia y la cooperación con los habitantes no muestran una revocación formal del destierro.',
        ['44-002','44-004','44-012','44-207','44-213'], 'Si el destierro ha sido revocado y con qué autorización puede permanecer en Cuicapalli.')
    update('P41-006', 'Los viales verdes de Iktan siguen sin un análisis que los identifique con el veneno de Eromov o la muestra del claro. Parroter afirma haber avanzado con materiales recibidos y luego prepara el remedio con espinas, pero no enumera sus procedencias ni demuestra una equivalencia química entre esas muestras.',
        ['44-009','44-208','44-216'], 'La composición de los viales y la relación comprobada entre las distintas muestras de veneno.')
    new_tracking = [
        dict(respuesta='Las venas negras menguan después de la preparación administrada. Parroter sonríe, pide avisar a Leona y anuncia que preparará más, sin representar las dosis siguientes.', referencias=['44-216'], pendiente='La evolución posterior y la recuperación completa.'),
        dict(respuesta='Guayacán extrae piezas de exoesqueleto con cortes imperfectos y Ayoto las lleva hacia el herrero, que exige recibir el material en su tienda.', referencias=['44-210','44-212','44-215'], pendiente='La aceptación del encargo, el precio y el equipo finalmente fabricado.'),
        dict(respuesta='Tlachka extrae restos aparentemente humanoides y la masa queda a un punto de vida. Un comentario sobre su muerte se corrige; la llegada del devorafango no identifica a las víctimas ni confirma el final del moho.', referencias=['44-102','44-110','44-111'], pendiente='La identidad y procedencia de los restos y el destino de la masa.'),
        dict(respuesta='Leona recuerda a Eromov encontrándola de pequeña durante el esfuerzo por arrancar la espina. No se desarrolla cómo ocurrió ni toda la historia del vínculo.', referencias=['44-117'], pendiente='Las circunstancias de aquel encuentro y la historia de su crianza.'),
        dict(respuesta='Parroter advierte que comer la criatura puede sentar mal. Tlachka cocina la carne y Leona soporta la salsa picante; esa tirada no demuestra inocuidad o inmunidad al veneno.', referencias=['44-208','44-213','44-214'], pendiente='Si aparecen consecuencias posteriores de comer la carne.'),
        dict(respuesta='Aunque Guayacán utiliza curaciones durante el combate, él y Ayoto siguen muy heridos y avanzan apoyándose al terminar.', referencias=['44-113','44-118','44-215'], pendiente='La recuperación posterior de ambos y sus posibles secuelas.'),
    ]
    notes = [
        'La masa inicial carece de boca definida y consume huesos. El devorafango llega después con espinas y ácido: no son dos formas del mismo rival ni se equiparan con los no muertos del claro de Iktan (44-018, 44-102, 44-110–44-112).',
        'El moho queda a un punto de vida y un comentario que lo da por muerto se corrige. No se fuerza una muerte a partir de las expresiones alternas de daño letal y no letal (44-104, 44-106, 44-108, 44-110).',
        'Guayacán aclara que su agarre estabiliza el cuello para ayudar a Leona, frente a la interpretación inicial de cerrar la boca. Tlachka consigue después abrir las mandíbulas y extraerla; esa salida no queda como pregunta pendiente (44-118, 44-120, 44-201, 44-203, 44-205).',
        'El ingrediente se obtiene con la criatura viva. La autorización de Parroter para matarla después y su posterior reprimenda por una muerte innecesaria se conservan sin inventar una orden incumplida de capturarla (44-011, 44-117, 44-202, 44-205–44-208).',
        'Ácido, pinchazos y barro son efectos distintos: el director niega veneno en las espinas dorsales y la ceguera de Ayoto se atribuye al barro y al chat. No se convierten en el tóxico de Eromov (44-111, 44-114, 44-204).',
        'Parroter no identifica por separado todos los materiales recibidos. No se equiparan las muestras de la Hoja Caída, el claro dracónico y los viales verdes. El rol previo ya documenta la entrega de viales y recetas de Iktan, mientras los expertos siguen esperados (44-001, 44-004, 44-009, 44-216; escena escrita x-1525362897662906398).',
        'El éxito de Leona al comer se refiere al picante, sin demostrar que la carne sea inocua. El exoesqueleto se recupera como material, sin crear un escudo terminado (44-208, 44-212–44-215).',
        'Eromov mejora después del remedio, pero no vuelve a sus funciones ni queda completamente curado. La intención de preparar más no documenta una segunda dosis ya administrada (44-216).',
        'La voz y el pico del traje de Guayacán no revelan su especie. Leona sigue siendo la harengon de Cuicapalli, distinta de Naór; actuar por el dirigente no la inviste como sucesora (44-001, 44-005, 44-203, 44-206).',
        'El recuerdo de Eromov encontrando a Leona de niña no fija filiación biológica o adopción formal. La cueva recordada de su infancia no se identifica con la Hoja Caída, el refugio de Citlali o una guarida del dragón (44-013, 44-117).',
    ]
    names = [
        'Tlachka/Tlatka/Traska/Trasca designan al guerrero nativo por continuidad de sus turnos y su presencia con Ayoto. No es Tacha, el tabernero hiena (44-002, 44-005, 44-102, 44-205, 44-213).',
        'Ayoto/Yoto/Aoto es el goliat de los dos escudos; Guayacán/Guayacá y variantes corresponden al combatiente del traje aviar. Leona es la harengon, no Naór (44-005–44-006, 44-109, 44-203).',
        'Parroter/Parro/Parter/Parot remiten al alquimista kenku ya catalogado. Erom/Eromov es el dirigente enfermo y la figura del recuerdo infantil de Leona (44-007–44-011, 44-117, 44-208, 44-216).',
        'Devorafango es la lectura provisional de Débora Fango/Borafango y variantes del encargo. Sus rasgos se cotejan con el animal espinoso y corrosivo encontrado; no se fija una especie de bestiario (44-010–44-011, 44-111, 44-215).',
        'Cueva del lago cercano a Cuicapalli y Masa de moho de la cueva son etiquetas descriptivas. Espina, muela, diente y protuberancia se conservan como denominaciones de la extracción bucal, separada de las púas de la cola (44-013, 44-102, 44-112, 44-117, 44-202, 44-207).',
        'El herrero de la tienda del norte no recibe nombre o especie inequívocos en esta escena. No se lo identifica automáticamente con Armin ni con el herrero tabaxi del capítulo 30. El mono del camino no se identifica con Pix (44-015, 44-210).',
    ]
    fixes = {
        '44-020':dict(afirmacion='La masa se lanza sobre Leona para envolverla. Tras la salvación, la harengon se aparta y la criatura cae al suelo sin alcanzarla. Ayoto se prepara para actuar.', limitacion='Este intento falla. Leona entra voluntariamente en la masa más adelante (44-103); es distinta del devorafango.'),
        '44-118':dict(limitacion='La curación se declara sin cantidad inequívoca. La interpretación inicial del agarre se aclara después: Guayacán intenta estabilizar el cuello para ayudar a Leona (44-201).'),
        '44-120':dict(afirmacion='Tlachka pregunta si Leona ya tiene la espina y el director recuerda que sigue dentro y sus compañeros no pueden saberlo automáticamente. Guayacán pide obtener más. Ante la interpretación de que el agarre dificulta la salida, Tlachka coloca un pie en la mandíbula inferior y prepara un apoyo para forzar su apertura.', limitacion='Guayacán aclara después que pretende estabilizar el cuello y no cerrar deliberadamente la boca (44-201). Tlachka abre las mandíbulas y saca a Leona en 44-205.'),
        '44-216':dict(limitacion='Se representa una mejoría visible tras administrar el remedio, sin vuelta a sus funciones o curación completa. La continuación del tratamiento es la intención de Parroter; no se narra una segunda dosis ya administrada.'),
    }
    catalog = [dict(nombre=e['nombre'], descripcion=e['descripcion'], nota=e['nota']) for e in histories if e['nombre'] in {
        'Devorafango','Espinas del Devorafango','Caparazón del Devorafango','Masa de moho de la cueva','Cueva del lago cercano a Cuicapalli','Herrero de Cuicapalli'}]
    save(FOLDER / 'edicion_integrada.json',dict(alias_entidades=aliases, etapas=stages, historias_entidades=histories,
        ajustes_afirmaciones=fixes, misiones=missions, preguntas=questions, contradicciones=notes,
        nombres_dudosos=names, catalogo=catalog, seguimiento_anterior=updates, seguimiento_nuevo=new_tracking))
    print('Cotejo: 16 historias, seis preguntas nuevas y seis seguimientos anteriores con evidencia nueva.')


if __name__ == '__main__':
    main()
