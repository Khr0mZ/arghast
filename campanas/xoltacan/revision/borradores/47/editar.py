"""Edición del coordinador tras integrar las tres lecturas y cinco escenas completas."""
from copy import deepcopy
import hashlib
from pathlib import Path

from preparar import ROOT, FOLDER, save
from construir import read_json, sha


def rol(scene, mid, description):
    path = ROOT / f'campanas/xoltacan/conocimiento/rol_escrito/escenas/{scene}.json'
    source = next(s for s in read_json(path)['fuentes'] if s['id'] == mid)
    return dict(escena=scene, mensaje_id=mid, descripcion=description,
                url=source['url_discord'], texto_sha256=source['texto_sha256'])


def preparar_edicion():
    deliveries = [read_json(FOLDER / f'entrega_{i}.json') for i in (1, 2, 3)]
    before = {q['id']:q for q in read_json(FOLDER / 'seguimiento_antes.json')}
    checks = []
    for delivery in deliveries:
        for q in delivery['cotejo_preguntas_asignadas']:
            qid = q.get('id', q.get('pregunta_id'))
            assert q['sha256_pregunta'] == hashlib.sha256(before[qid]['pregunta'].encode()).hexdigest()
            checks.append(dict(id=qid, bloque=delivery['bloque'], sha256_pregunta=q['sha256_pregunta'],
                aporte_del_bloque=q.get('observacion', q.get('observacion_bloque', q.get('respuesta_bloque'))),
                referencias_provisionales=q.get('referencias', [])))
    assert len(checks) == len({q['id'] for q in checks}) == len(before) == 284

    aliases = {'Dragón verde del bosque de Iktan':'Clolgedranx'}
    identities = read_json(FOLDER / 'identidades_contexto.json')
    # El mapa conserva las grafías confirmadas por el usuario en el editor online.
    aliases.update(identities['cambios'])
    # La cautela antigua mantenía dos fichas. El nuevo enlace de voz, encargo y
    # protección permite reunirlas, conservando todas sus etapas y etiquetas.
    catalog_path = ROOT / 'campanas/xoltacan/config/entidades.json'
    catalog = read_json(catalog_path)
    prior = next((g for g in catalog['grupos'] if g['nombre']=='Dragón verde del bosque de Iktan'), None)
    if prior:
        target = next(g for g in catalog['grupos'] if g['nombre']=='Clolgedranx')
        for key in ('referencias','etiquetas'):
            target[key] = list(dict.fromkeys(target.get(key,[]) + prior.get(key,[])))
        catalog['grupos'].remove(prior)
        save(catalog_path, catalog)
        history_path = ROOT / 'campanas/xoltacan/config/historias_personajes_complementarias.json'
        history_doc = read_json(history_path)
        history = history_doc['personajes']
        for stage in history.pop(prior['nombre']):
            if stage not in history['Clolgedranx']:
                history['Clolgedranx'].append(stage)
        save(history_path, history_doc)
    stages = [deepcopy(s) for d in deliveries for s in d['etapas']]
    stages[5]['texto'] = stages[5]['texto'].replace(
        'Su nombre queda como «Mlan» en la transcripción.', 'Se presenta como Mictlan.')
    stages[7]['texto'] = stages[7]['texto'].replace(
        'Su siguiente ataque, anunciado a nivel tres, impacta justo cuando termina el tramo. La batalla sigue abierta en el corte.',
        'Su siguiente ataque, anunciado a nivel tres, impacta. La expulsión empieza a abrir espacio entre los muertos.')
    stages[12]['texto'] = stages[12]['texto'].replace(
        'recibe la respuesta transcrita «mi clan» y propone llamarlo Mic. El bloque termina antes de que se resuelva esa ayuda o de que Tentacol alcance a los elfos.',
        'Mictlan vuelve a presentarse y Patata propone llamarlo Mic antes de atender sus heridas. Tentacol todavía no ha alcanzado a los elfos.')
    stages[14]['texto'] = stages[14]['texto'].replace(
        'El dragón responde que sus súbditos no lo respetan.',
        'El dragón responde que los súbditos de Chopito no lo respetan.')
    stages[17]['texto'] = stages[17]['texto'].replace(
        'Walulu los recibe mientras prepara medicinas con plantas.',
        'Walulu los recibe mientras prepara medicinas con plantas. Al hablar del dragón, lo identifica por su nombre: Clolgedranx.')

    histories = []
    for delivery in deliveries:
        for raw in delivery['historias_entidades']:
            h = deepcopy(raw)
            if h['nombre'] == 'Hermanos elfos buscados por el dragón':
                for name in ('Eldrath', 'Tryel'):
                    one = deepcopy(h)
                    one['nombre'] = name
                    one['nota'] = ('La identidad de los hermanos se coteja con los 80 mensajes de la escena escrita '
                        'x-1530576387507753053. No se traslada esa conversación posterior al vídeo ni se identifica '
                        'automáticamente a la pareja anónima de la habitación del capítulo 39.')
                    histories.append(one)
                continue
            for stage in h['etapas']:
                stage['texto'] = stage['texto'].replace(
                    ', sin que este tramo muestre la destrucción del objetivo', '')
                replacements = {
                    'su siguiente ataque impacta antes del corte.':'su siguiente ataque impacta.',
                    'Su origen y su relación exacta con el dragón quedan abiertos en este bloque.':'El origen arqueológico de los muros sigue sin establecerse.',
                    'el combate continúa al corte.':'el combate continúa.',
                    'El grupo no lo ve ni recibe una intrusión mental adjudicada durante este tramo.':'En ese primer aviso aún no lo han visto ni han sufrido la nueva intrusión mental.',
                    'la resolución de la ayuda queda en el bloque siguiente.':'a continuación empieza a atender sus heridas.',
                    'El tramo no muestra que Tortas enseñe':'No se representa que Tortas enseñe',
                    'sin describir en este tramo el nuevo gobierno':'sin describir el nuevo gobierno',
                }
                for old, new_text in replacements.items():
                    stage['texto'] = stage['texto'].replace(old, new_text)
            if h['nombre'] == 'Oliver':
                h['descripcion'] = 'Hermano menor de Tesara, vinculado al museo según el rol escrito, a quien amenaza Clolgedranx.'
                h['nota'] = ('Tesara ya había hablado de su hermano Oliver en el rol escrito de mayo y julio '
                    '(x-1504724660288356372 y x-1528736536982454303). El capítulo 47 incorpora la amenaza, no su primera '
                    'mención en la campaña. El vídeo no representa a Oliver o su captura; sus antecedentes familiares '
                    'proceden de las declaraciones de Tesara en esas fuentes escritas, conservadas por separado.')
            histories.append(h)

    updates = {}

    def update(qid, answer, refs=(), pending=None, state=None, sources=()):
        old = before[qid]
        entry = dict(respuesta=answer, referencias=list(dict.fromkeys(old['referencias'] + list(refs))),
                     pendiente=old['pendiente'] if pending is None else pending,
                     estado=state or old['estado'])
        if sources:
            entry['fuentes_rol'] = list(old.get('fuentes_rol', [])) + list(sources)
        updates[qid] = entry

    identity_note = (' La grafía Clolgedranx es la confirmada por el usuario; los subtítulos conservan sus variantes. '
        'Tesara reconoce la voz de la emboscada anterior y el director confirma la continuidad. '
        'Se integra así el dragón verde con el que pidió a Citlali sacar a los dos elfos en el capítulo 39; '
        'Zarynth, el pequeño dragón de Aerendriel, sigue siendo otra identidad.')
    update('P31-001', 'Walulu identifica al dragón como Clolgedranx y vincula el ataque antiguo con las ruinas de Iktan. '
        'Muestra un libro y explica que, después del desastre, un antiguo dirigente y miembros de las tribus hicieron '
        'la protección hace ciento veinte años. Es historia transmitida por Walulu, no una inspección del pasado. '
        'Las ruinas exteriores del lago visitadas por Tesara son un lugar distinto.' + identity_note,
        ['47-218','47-320'], '', 'resuelta')
    update('P31-002', 'El encuentro muestra cadáveres movidos por raíces, una intrusión mental que exige sacar a los elfos '
        'y, finalmente, al dragón que inmoviliza al grupo y reclama su hueste. El director confirma la continuidad de la voz '
        'que Tesara recuerda de la emboscada. Derrotar la masa de cuerpos no elimina a la criatura ni sus amenazas.',
        ['47-122','47-206','47-218','47-226','47-306','47-307','47-311'],
        'El mecanismo completo, sus límites y cómo neutralizar esa influencia de forma permanente.', 'parcial')
    siblings = rol('x-1530576387507753053', '1530614552239018004',
        'Eldrath se dirige a Tryel como su hermana en la conversación completa sobre el ultimátum.')
    update('P39-003', 'Walulu explica que el ritual protector de Iktan impide entrar a los dragones y obliga a Clolgedranx '
        'a exigir intermediarios. La escena escrita posterior sobre el mismo ultimátum identifica a los hermanos perseguidos '
        'como Eldrath y Tryel. Eso no enlaza de manera expresa a ambos con la habitación anónima del capítulo 39 ni diagnostica '
        'la enfermedad de aquella elfa; el relato del veneno de Tryel sigue siendo su propia continuidad.',
        ['47-307','47-318','47-320','47-321'],
        'El enlace expreso con la pareja de la habitación y el diagnóstico de la elfa de aquella escena.', 'parcial', [siblings])
    for qid in ('P40-003','P41-009'):
        update(qid, 'Walulu informa de varias guaridas dispersas que encontraron algunos guardias, sin localizarlas '
            'sobre un mapa o inspeccionar la cueva de la emboscada.' + identity_note,
            ['47-218','47-320','47-322'], 'La ubicación verificable de las guaridas y si la cueva de la emboscada es una de ellas.', 'parcial')
    update('P42-003', 'El director confirma que Patata encontró el huerto destrozado y el cuerpo de «Happy» Bonny '
        'colgado a la entrada de Shiaru. Patata atribuye la expulsión de habitantes y la pérdida de su casa a nuevos piratas. '
        'Los antiguos tripulantes se encuentran refugiados en Iktan y corroboran que los echaron. No se representa quién '
        'colgó el cuerpo ni se identifica al gobernante actual o a todos los ocupantes.',
        ['47-101','47-116','47-317'], 'La identidad y organización del poder actual en Shiaru y las circunstancias de la exposición del cuerpo.', 'parcial')
    update('P46-007', before['P46-007']['respuesta'] + ' Patata y los antiguos piratas describen la expulsión y la pérdida '
        'de sus hogares. En el rol posterior Ilikar pide ayuda a Tortas para su tripulación, sin representar la expedición de Ione.',
        ['47-101','47-116','47-317'], sources=[rol('x-1530356065936347307','1530566731804840168',
            'Ilikar relata la pérdida del hogar de su capitana y pide apoyo; no ejecuta una reconquista.')])
    school_scene = 'x-1531013198478708756'
    update('P46-008', 'Tesara lleva de nuevo a Leo al colegio y el niño le reprocha la reprimenda de la mujer que se llevó '
        'a su amigo. En la escena escrita posterior, Naór y Citlali hablan de lo ocurrido; Leo dice que Eztli es su mejor amigo '
        'y los dos niños continúan jugando juntos. El encuentro con Naór sí queda representado, pero la reunión de madres '
        'se sigue anunciando para el día siguiente.', ['47-104','47-105','47-106'],
        'La celebración de la reunión de madres y la evolución posterior de la convivencia escolar.', 'parcial', [
            rol(school_scene,'1531021544879292476','Leo llama a Eztli su mejor amigo.'),
            rol(school_scene,'1531042917127426220','La reunión escolar permanece anunciada para mañana.')])
    species = rol(school_scene,'1531028681378631700','Citlali identifica a su hijo adoptivo como un Quetzalcoatlus.')
    update('P34-004', 'La grafía Eztli está confirmada por el usuario. En el rol posterior Citlali explica que incubó '
        'el huevo e identifica a su hijo adoptivo como un Quetzalcoatlus. Los niños juegan juntos y sus alas amortiguan '
        'una caída, sin llevar el peso de Leo. Es identificación de Citlali, no un análisis externo. No hay una decisión '
        'formal sobre la residencia en Cuicapalli.', pending='La aceptación formal de su residencia en Cuicapalli.', sources=[species])
    update('P07-002', 'La cría del huevo vive bajo el cuidado de Citlali y su nombre confirmado es Eztli. En el rol escrito '
        'Citlali cuenta que lo incubó y lo identifica como un Quetzalcoatlus. Eso aporta una identificación atribuida a ella; '
        'no fija el precio ni representa que Mamá descubra el pacto de Nox con Bonny.',
        pending='El precio y el conocimiento de Mamá sobre el pacto de venta.', sources=[species])
    update('P38-002', 'Ilikar había declarado proceder de Valle Blanco. En la conversación escrita posterior al ultimátum '
        'se presenta como Thuun-kaz y explica que su tribu pacífica cultiva el valle y caza dragones blancos para protegerlo. '
        'No cuenta qué causó las heridas de su llegada a la playa; el veneno de Tryel pertenece a otra historia.',
        pending='La causa de las heridas iniciales y los antecedentes tribales todavía no relatados.', sources=[
            rol('x-1530576387507753053','1530752446165422080','Ilikar se presenta como Thuun-kaz.'),
            rol('x-1530576387507753053','1530962128729800726','Describe la vida de su tribu y la caza de dragones blancos.')])
    for qid in ('P01-006','P15-006'):
        update(qid, 'El usuario ha confirmado Zarynth como nombre del dragón de Aerendriel, distinto de Clolgedranx y '
            'de Eztli. Esa corrección fija la grafía de la ficha, pero no reconstruye qué se pronunció en las menciones '
            'antiguas transcritas como Zari o Tarin. No se añade un minuto ficticio del capítulo 47 para probar el nombre.',
            pending='La correspondencia exacta de las antiguas menciones Zari y Tarin con el nombre confirmado Zarynth.')
        updates[qid]['fuente_identidad'] = 'campanas/xoltacan/revision/identidades_confirmadas_editor_20261110.json'

    new = []
    def question(text, answer, refs, pending):
        new.append(dict(pregunta=text, respuesta=answer, referencias=refs, pendiente=pending))
    question('¿Quién gobierna ahora Shiaru y quién expuso el cuerpo de Bonny? (47-101, 47-116, 47-317).',
        'El director confirma el cuerpo colgado y la destrucción del huerto. Patata y los antiguos piratas relatan una expulsión, sin identificar a los nuevos dirigentes.',
        ['47-101','47-116','47-317'], 'La identidad y organización de los ocupantes y las circunstancias de la exposición del cuerpo.')
    question('¿Qué origen tienen las ruinas del lago y qué podrá aprender Tesara de ellas? (47-108–47-110).',
        'Angelique las distingue del barrio antiguo. Tesara encuentra muros caídos y los estudia, sin un descubrimiento arqueológico concreto.',
        ['47-108','47-109','47-110'], 'La procedencia, antigüedad e interpretación de los restos del lago.')
    question('¿Entregará Tesara la joya prometida a Angelique y conocerá a la persona por la que pregunta? (47-108).',
        'Promete buscar una joya si encuentra algo y pide continuar la conversación personal. No completa el intercambio ni obtiene el nombre en esa charla.',
        ['47-108'], 'El cumplimiento de la promesa y la conversación que ambas aplazan.')
    question('¿Quiénes son los vigilantes a los que pertenece Mictlan y qué consideran sacrilegio? (47-119–47-120).',
        'Mictlan dice que su gente vigila el lugar y permite estudiar con esa condición. No nombra al grupo ni describe sus normas.',
        ['47-119','47-120'], 'La comunidad del felino, su autoridad y sus criterios de protección.')
    question('¿Quiénes eran los cadáveres del lago y cómo se sostiene su animación por raíces? (47-122, 47-217, 47-226, 47-307).',
        'Se observa el movimiento por raíces, la reunión de los restos en una masa y su destrucción. El dragón reclama una hueste de muertos; no identifica a las víctimas o todo el mecanismo.',
        ['47-122','47-217','47-226','47-307'], 'Las identidades, el origen de los cuerpos y los límites de la animación.')
    question('¿Cuánto dura la compulsión de llevar a los elfos y cómo podrán resistirla o terminarla? (47-206, 47-210–47-211, 47-229).',
        'Todos perciben una orden ajena; Chopito la reformula como rescate y Tentacol inicia la búsqueda. No se demuestra una neutralización permanente al regresar a Iktan.',
        ['47-206','47-210','47-211','47-229','47-313'], 'La duración, condiciones y eliminación de la compulsión.')
    question('¿Quién paga a Clolgedranx por los hermanos elfos y con qué propósito? (47-310).',
        'El dragón dice que alguien los quiere y le ha prometido una recompensa. La alusión a una sierpe mayor no identifica al contratante ni demuestra que sea otro dragón.',
        ['47-310'], 'La identidad del interesado, sus motivos y los términos del encargo.')
    question('¿Cómo responderán los viajeros al plazo de una semana y a la amenaza de una hueste contra Iktan? (47-311, 47-321, 47-324).',
        'El grupo regresa sin entregar a los elfos. Walulu los acoge y distingue la protección frente a dragones de la defensa contra muertos, confiada a la guardia.',
        ['47-311','47-313','47-321','47-324'], 'La decisión del grupo, la preparación de la ciudad y el desenlace del ultimátum.')
    question('¿Cómo conoce Clolgedranx a Oliver y qué peligro corre el hermano de Tesara? (47-312).',
        'La criatura lo nombra y Tesara confirma que es su hermano. No se representa a Oliver, su localización o su captura.',
        ['47-312'], 'El origen de esa información y el alcance real de la amenaza contra Oliver.')
    question('¿Encontrará Walulu una debilidad o estrategia y se localizarán las guaridas del dragón? (47-322–47-323).',
        'Walulu informa de varias guaridas halladas por guardias y empieza a consultar los libros antiguos. Todavía no ofrece una ubicación o una estrategia probada.',
        ['47-322','47-323'], 'Los resultados de la investigación, las ubicaciones y un plan verificable.')
    question('¿De qué tratará la reunión para la que Walulu quiere a Naór y a los viajeros? (47-325).',
        'Walulu pide hablar con Naór cuando vuelva y que los viajeros la acompañen en una reunión futura. La conversación no concreta destino, asistentes o agenda.',
        ['47-325'], 'La reunión y su propósito; no se identifica automáticamente con el concilio de Tutucan.')

    # Continuidad escrita anterior y posterior: aporta contexto, sin convertir
    # recuerdos, opiniones o preparativos en sucesos del vídeo.
    later_scene = 'x-1553354971863588865'
    mental_sources = [rol(later_scene,'1553433070248398860','Tesara atribuye intrusiones y pesadillas al dragón.'),
        rol(later_scene,'1553385291870502997','Walulu sostiene que utiliza mentiras y miedos, no trucos mágicos mentales.')]
    mental_context = (' En el rol posterior Tesara atribuye al dragón nuevas intrusiones y pesadillas. '
        'Walulu sostiene, en cambio, que utiliza mentiras y miedos en lugar de magia mental. Son evaluaciones atribuidas '
        'que no anulan los efectos adjudicados en el vídeo ni explican la duración de aquella orden.')
    updates['P31-002']['respuesta'] += mental_context
    updates['P31-002']['fuentes_rol'] = mental_sources
    new[5]['respuesta'] += mental_context
    new[5]['fuentes_rol'] = mental_sources
    new[8]['respuesta'] += (' Tesara ya había descrito a Oliver antes de este encuentro: dice que es cinco años menor '
        'y está vinculado al museo. Más adelante los recuerdos familiares se deforman en pesadillas y hablar de él '
        'con Tortas la calma. Ese contexto muestra su temor y afecto, sin localizar al hermano o demostrar que esté '
        'capturado o a salvo, ni cómo obtuvo el dragón la información.')
    new[8]['fuentes_rol'] = [
        rol('x-1504724660288356372','1504868653076840561','Tesara cuenta que Oliver es cinco años menor y trabaja en el museo.'),
        rol('x-1544040982084067438','1544040982084067438','Un recuerdo familiar se deforma con la voz del dragón.'),
        rol('x-1546437630781296680','1546437630781296680','Una pesadilla impone una elección entre familiares.'),
        rol(later_scene,'1553485649699405946','Tortas observa que pensar en Oliver ha relajado a Tesara.')]
    new[9]['respuesta'] += (' En el rol posterior Tesara plantea explorar con Iker para preparar una emboscada. '
        'Walulu dice no haberse enfrentado a un dragón y no entrega mapas, ubicaciones o resultados concretos de los libros. '
        'La prueba con veneno común de Tortas no demuestra inmunidad al veneno dracónico.')
    new[9]['fuentes_rol'] = [rol(later_scene,'1553491709592076389','Walulu responde a la solicitud de estrategia y mapas.'),
        rol('x-1552369078063202355','1552424376031387712','Tortas pide probar veneno normal, no el del dragón.')]

    missions = [
        'Sobrevivir a los muertos del lago: Patata deshace la masa final y las raíces se retiran; el dragón permanece libre (47-217, 47-226).',
        'Investigar al dragón para los elfos: Tesara identifica la voz anterior, presencia el ultimátum y obtiene de Walulu la explicación de la protección de Iktan; la búsqueda de debilidades comienza sin resultado (47-218, 47-311, 47-320–47-323).',
        'Proteger a Eldrath y Tryel: Clolgedranx exige su entrega en una semana. Walulu los acoge y Tesara se niega a entregarlos; la amenaza y el plazo siguen abiertos (47-307, 47-311, 47-314, 47-324).',
        'Recuperar un refugio tras la caída de Shiaru: Patata alcanza Iktan y encuentra allí a los piratas expulsados, sin recuperar su casa o identificar a los nuevos gobernantes (47-101, 47-116, 47-317).',
        'Ampliar los seguidores de Chopito: la pareja vuelve de Perlasal y busca nuevos territorios. Patata acepta amistad sin abandonar a su diosa y Tesara no se convierte (47-103, 47-112, 47-114, 47-117).',
        'Atender a Leo y estudiar las ruinas: Tesara deja al niño en el colegio, llega a los muros del lago y promete buscar una joya para Angelique. El combate interrumpe la investigación (47-104, 47-108–47-110, 47-122).',
        'Acompañar a Walulu: Tesara acepta asistir a una reunión futura y la dirigente quiere hablar con Naór; todavía no se celebra ni se concreta su agenda (47-325).',
    ]
    occupation = next(f for f in deliveries[0]['afirmaciones'] if f['id']=='47-116')
    adjustments = {'47-116':{'entidades':occupation['entidades'] + ['Piratas ocupantes de Shiaru']}}
    def adjust(fid, **values):
        adjustments.setdefault(fid, {}).update(values)
    adjust('47-111', limitacion='El lago no recibe nombre propio en este diálogo. La referencia no identifica todos los lagos mencionados en la campaña.')
    adjust('47-119', limitacion='El VTT presenta «Mlan» sin audio cotejado. La grafía Mictlan se contrasta con las intervenciones rotuladas de la escena escrita posterior x-1531013198478708756, leída completa. Esa identificación no traslada sus acciones posteriores al vídeo. No se fija especie reglada, tribu o rango; la vigilancia es declaración suya.')
    adjust('47-130', limitacion='La imposibilidad de recuperar vida tiene la duración adjudicada, hasta el final del siguiente turno. No se extrapola una secuela permanente ni se ofrece un diagnóstico posterior.')
    adjust('47-132', titulo='Patata impacta con un ataque de nivel tres',
        afirmacion='Patata anuncia un lanzamiento de nivel tres y un ataque. El director confirma que impacta; la batalla contra los cadáveres continúa.')
    adjust('47-201', limitacion='El director distingue la expulsión de la condición de miedo. El efecto iniciado por Patata continúa y puede romperse al dañar a los objetivos.')
    adjust('47-202', limitacion='Las variantes automáticas MD y similares se conservan en los originales. La grafía Mictlan se contrasta con sus intervenciones en la escena escrita posterior x-1531013198478708756. La adjudicación no identifica una secuela permanente del veneno.')
    adjust('47-209', limitacion='Tesara llama gemelos a los elfos de las imágenes. La conversación escrita posterior x-1530576387507753053 identifica a Eldrath y Tryel como los hermanos perseguidos; el vídeo no pronuncia aquí sus nombres con claridad.')
    adjust('47-218', limitacion='El director confirma la continuidad de la voz reconocida por Tesara. El nombre Clolgedranx se integra con la explicación posterior de Walulu y la grafía confirmada por el usuario. No se identifican por ello todos los dragones verdes mencionados en otras escenas.')
    adjust('47-229', limitacion='Tentacol inicia la búsqueda, pero no encuentra, saca de la ciudad o entrega a los elfos. La propuesta de rescate de Chopito no se convierte en un secuestro ocurrido.')
    adjust('47-230', limitacion='La grafía Mictlan se contrasta con la escena escrita posterior x-1531013198478708756; la cita conserva «mi clan». La curación continúa después, en 47-301, y no se da por resuelta en este intercambio.')
    adjust('47-311', limitacion='La destrucción sigue siendo una amenaza condicional. El plazo no transcurre en este capítulo y no se narra el asalto o la entrega de los elfos.')
    adjust('47-314', limitacion='Las sospechas de Mictlan no prueban una traición. Las variantes «el Dream/Eldrin» y «Miriam» se conservan en el VTT; la conversación escrita posterior del ultimátum identifica a Eldrath y Tryel como los hermanos, sin trasladar sus acciones al vídeo.')
    edition = dict(alias_entidades=aliases, etapas=stages, historias_entidades=histories,
        ajustes_afirmaciones=adjustments,
        misiones=missions, preguntas=[q['pregunta'] for q in new], seguimiento_nuevo=[
            {k:v for k,v in q.items() if k!='pregunta'} for q in new], seguimiento_anterior=updates,
        contradicciones=deliveries[0]['contradicciones'], nombres_dudosos=[
            'Écil: mención del amigo de Leo, compatible por contexto con Eztli sin identificación inequívoca en ese diálogo.',
            'Eldrin/el Dream y Miriam: variantes del VTT de los hermanos. La escena escrita posterior, leída completa, enlaza el ultimátum con Eldrath y Tryel.',
            'Glendra Drax/Colgenrax: variantes de Clolgedranx; grafía confirmada por el usuario, distinta de Zarynth.',
            'Mlan/mi clan/Mic: nombre de Mictlan, contrastado con las intervenciones rotuladas de la escena escrita posterior.',
        ], catalogo=[
            dict(nombre='Mictlan', etiquetas=['Mictlan','Mlan','Miklan','Mic','mi clan']),
            dict(nombre='Oliver', etiquetas=['Oliver','Oli'],
                descripcion='Hermano menor de Tesara, vinculado al museo según el rol escrito, a quien amenaza Clolgedranx.',
                nota='Ya mencionado por Tesara en el rol escrito de mayo y julio: x-1504724660288356372 y x-1528736536982454303. La amenaza del 47 no representa su captura o ubicación actual. Los antecedentes del museo y la familia son declaraciones de Tesara, conservadas en las escenas escritas.'),
            dict(nombre='Clolgedranx', etiquetas=['Clolgedranx','Clodidrax','Clodidax','Dragón verde del bosque de Iktan','Serpiente del Bosque'],
                nota='Grafía confirmada por el usuario. La voz reconocida por Tesara y la explicación de Walulu en el capítulo 47 enlazan el dragón verde y su encargo de sacar a los hermanos. La protección impide su entrada en Iktan; no excluye a los no muertos. Distinto de Zarynth. Las guaridas no se localizan.'),
        ])
    # Conservar todas las etiquetas anteriores al ampliar una identidad.
    groups = {g['nombre']:g for g in read_json(ROOT / 'campanas/xoltacan/config/entidades.json')['grupos']}
    for patch in edition['catalogo']:
        patch['etiquetas'] = list(dict.fromkeys(groups.get(patch['nombre'], {}).get('etiquetas', []) + patch['etiquetas']))
    save(FOLDER / 'edicion_integrada.json', edition)
    save(FOLDER / 'cotejo_preguntas.json', dict(lecturas=checks, total=284, integracion_completa=True,
        criterio='Cada agente coteja su bloque asignado; el coordinador cruza los 90 registros de los tres bloques y las trece escenas completas revisadas por el equipo. La ausencia de resolución no elimina la pregunta.',
        actualizadas=list(updates), preguntas_nuevas=len(new)))
    temporal = read_json(FOLDER / 'rol_por_cotejar.json')
    scene_ids = ['x-1529957197948260414','x-1530316770995339374','x-1530356065936347307',
                 'x-1530576387507753053','x-1531013198478708756',
                 'x-1504724660288356372','x-1506584437201047605','x-1528736536982454303',
                 'x-1537945553915089056','x-1544040982084067438','x-1546437630781296680',
                 'x-1552369078063202355','x-1553354971863588865']
    reviews = []
    for scene_id in scene_ids:
        path = ROOT / f'campanas/xoltacan/conocimiento/rol_escrito/escenas/{scene_id}.json'
        scene = read_json(path)
        reviews.append(dict(escena=scene_id, archivo=path.relative_to(ROOT).as_posix(), sha256=sha(path),
            lectura_completa=True, mensajes_leidos=[s['id'] for s in scene['fuentes']]))
    assert sum(len(r['mensajes_leidos']) for r in reviews) == 408
    extra_reports = ['cotejo_antecedentes_b1.json','cotejo_posterior_b2.json','cotejo_posterior_b3.json']
    for filename in extra_reports:
        assert read_json(FOLDER / filename)['lectura_completa'] is True
    save(FOLDER / 'cotejo_rol.json', dict(escenas=reviews, total_mensajes=408, ancla=temporal['ancla'],
        entregas_adicionales=[dict(archivo=name, sha256=sha(FOLDER / name)) for name in extra_reports],
        cambios_ordenacion=temporal['cambios'], escenas_que_cruzan_corte=len(temporal['cruzan']),
        criterio='Corte operativo estimado con tarjeta de Twitch y duración de YouTube, no una hora narrativa exacta. Las 325 escenas se cotejan por intervalo. El coordinador lee completas las dos afectadas y tres de continuidad; los tres agentes releen ocho escenas adicionales, sin solapamiento, para antecedentes y consecuencias. Los originales no se modifican.',
        continuidad=['Mictlan: intervenciones rotuladas en la escena escolar posterior.',
            'Eldrath y Tryel: los hermanos se reconocen durante la conversación completa del ultimátum.',
            'Tessara Quinn/Tessa se conserva como alias de Tesara Queen.',
            'La sospecha de un mandante dracónico se atribuye a los personajes; el vídeo no la confirma.']))


if __name__ == '__main__':
    preparar_edicion()
