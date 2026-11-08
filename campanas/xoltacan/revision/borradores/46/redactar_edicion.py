"""Integra las tres lecturas y el cotejo de las 276 preguntas anteriores."""
from copy import deepcopy
from preparar import ROOT, FOLDER, read_json, save

deliveries = [read_json(FOLDER / f'entrega_{n}.json') for n in (1, 2, 3)]
stages = [deepcopy(s) for d in deliveries for s in d['etapas']]
for stage in stages:
    stage['texto'] = stage['texto'].replace('Cuando se dan la mano, la humedad que él conserva descarga electricidad sobre ella.',
        'Cuando se dan la mano, el contacto descarga electricidad sobre ella.')
histories = [deepcopy(h) for d in deliveries for h in d['historias_entidades']]
angelique = next(h for h in histories if h['nombre'] == 'Angelique')
angelique['etapas'].insert(0, dict(titulo='Los intentos de Coyote',
    texto='Antes del encuentro con Zoltan, Coyote intenta cortejar a Angelique en la taberna de Iktan y acaba expulsado. Su insistencia vuelve a recordarse y representarse cuando Naór lo busca antes de ir a Perlasal. La continuidad del lugar y el cortejo permite reunir estos pasajes con la presentación posterior de la encargada, conservando la grafía provisional y sin identificarla con Angélica Thunder.',
    referencias=['39-020', '45-007', '45-011']))
for history in histories:
    if history['nombre'] == 'Aldea caníbal de la cascada' and history['etapas'][0]['referencias'][0] == '46-101':
        history['etapas'].append(dict(titulo='Las chispas antes de marcharse',
            texto='Después de vencer a los tiranosaurios, Zoltan vuelve a registrar las casas sin encontrar botín. Sus chispas prenden pequeños fuegos y decide dejar la investigación para seguir al grupo. La corrección de la narración no verifica que arda toda la aldea ni explica las muertes previas de la cueva.',
            referencias=['46-206', '46-207']))

previous = {q['id']: q for q in read_json(FOLDER / 'seguimiento_antes.json')}
updates = {}


def patch(qid, answer, refs, pending=None, state=None, role=None):
    q = previous[qid]
    item = dict(respuesta=answer, referencias=list(dict.fromkeys(q['referencias'] + refs)),
        pendiente=q['pendiente'] if pending is None else pending,
        estado=q['estado'] if state is None else state)
    if role:
        item['fuentes_rol'] = list(q.get('fuentes_rol', [])) + role
    updates[qid] = item


patch('P43-005',
    'Las recapitulaciones del capítulo 46 documentan que Eleanor y los demás siguieron a Citlali hasta la playa, donde hubo una discusión con Ione y un disparo. Después emprendieron juntos el camino a Iktan. Esto confirma el encuentro, pero no reproduce el diálogo entero, el autor y blanco exactos del disparo, una entrada al Zampaolas o todas las noticias recibidas sobre Nox.',
    ['46-001', '46-002', '46-003', '46-004'],
    'El diálogo completo del encuentro, la atribución del disparo y la información recibida de la tripulación.', 'parcial')
patch('P43-004',
    'Citlali conserva una apariencia más joven, rehúsa explicar el cambio y se describe resentida entre siseos. Durante el ataque de los tiranosaurios vuelve a drenar vida: brillan sus tatuajes y mejora, aunque conserva mordiscos y dificultad para andar. Explica a Ione que el drenaje forma parte de su maldición y recuerda haberlo descubierto con Patata. Plantean consultar a Walulu, sin llegar a la audiencia. Estas escenas documentan la continuidad y el uso del efecto, sin una edad final, duración, origen o cura.',
    ['46-003', '46-006', '46-008', '46-201', '46-205', '46-216'],
    'La duración y edad final del rejuvenecimiento, el origen y los límites del poder y una posible cura de la maldición.', 'parcial')
patch('P43-006',
    'La recapitulación recuerda que Eleanor protegió el descanso de Erandy y la sitúa entre los viajeros hacia Iktan. Más tarde la encuentran viva en la taberna y Eleanor comprueba cómo está. Los dos mensajes escritos posteriores muestran el abrazo: Erandi despierta desorientada y mareada, y reconoce a Eleanor. No recibe un diagnóstico del trance ni se demuestra una recuperación completa.',
    ['46-001', '46-004', '46-208', '46-213'],
    'Su recuperación completa, la causa del mareo y las consecuencias del trance.', 'parcial',
    [dict(escena='x-1529957197948260414', mensaje_id='1529957197948260414',
        descripcion='Eleanor encuentra y abraza a Erandi después de llegar a Iktan.'),
     dict(escena='x-1529957197948260414', mensaje_id='1529959568187068486',
        descripcion='Erandi despierta desorientada y dice que le da vueltas la cabeza.')])
patch('P42-006',
    'Ione viaja por tierra hacia Iktan con los supervivientes, se separa de ellos y termina reuniéndose con sus hombres en la taberna. Quiere conseguir dinero y apoyos para recuperar Shiaru y averiguar si el novato ausente ha vuelto por allí. No representa una nueva búsqueda de Nox o su cuerpo ni una activación de la moneda pirata. Las monedas usadas para elegir una dirección al azar no se identifican como el objeto recibido de Bonnie.',
    ['46-002', '46-004', '46-010', '46-011', '46-208', '46-214', '46-215', '46-218'])
patch('P42-003',
    'Taylor dispara a Bonnie y el director la despide. En Iktan, Ione recuerda que Bonnie ya no está, promete proteger a sus tripulantes y plantea recaudar recursos y reclutar apoyos para recuperar Shiaru. El plan no incluye una inspección del puerto ni identifica su gobierno actual o todas las consecuencias del disparo.',
    ['46-215', '46-218'])
patch('P42-005',
    'La captura del joven rumbo a Puerto de Espadas sigue procediendo del relato de Taylor. En Iktan aparece otra mención sin resolver: los hombres de Ione no encuentran al novato que llaman Jacki y dicen que faltaba desde la playa. Ese testimonio no establece su identidad con el exmarine Jack ni con el cautivo de Taylor, ni demuestra una segunda captura, muerte o regreso.',
    ['46-214', '46-215'])
patch('P43-001',
    'La entidad de la visión y del altar no recibe nombre propio. La recapitulación del capítulo 46 vuelve a describir siseos que tientan a Citlali y un rencor creciente, sin que ese estado interior revele a sus compañeros el plan o la naturaleza completa del ser. Los nuevos drenajes no identifican por sí solos a su instigador.',
    ['46-003', '46-008', '46-201', '46-216'])
patch('P19-002',
    previous['P19-002']['respuesta'] + ' En el capítulo 46 Citlali vuelve a drenar a una criatura y recuperar parte de sus fuerzas, y lo explica a Ione como parte de su maldición, recordando a Patata. No ofrece una explicación completa de por qué una curación anterior causó daño o de las reglas del rejuvenecimiento. El apretón de manos con Zoltan tiene una descarga eléctrica propia y no se confunde con ese drenaje.',
    ['46-105', '46-201', '46-216'])
patch('P39-004',
    previous['P39-004']['respuesta'] + ' Ione propone llevar su nueva pregunta sobre los tatuajes y el drenaje a Walulu, y Citlali acepta acompañarla. La venta del collar y las otras escenas dejan esa consulta sin representar: no se completa el té, el examen o la explicación pendiente.',
    ['46-216', '46-217', '46-218'])
patch('P21-004',
    previous['P21-004']['respuesta'] + ' En Iktan, Leo llama madre a Naór al amenazar a Miausi. Citlali lo reprende cuando lo encuentra con Etley y él sale llorando a buscarla. Esa identificación afectiva y el nuevo episodio escolar no acreditan custodia formal por Eromov ni una recuperación psicológica del niño.',
    ['46-209', '46-210', '46-211'])
patch('P40-007',
    previous['P40-007']['respuesta'] + ' La marcha hacia Iktan sitúa a Cipo con los viajeros y, tras la separación del trío, vuelve a aparecer jugando con Ilikar en la taberna. No aporta una procedencia nueva del fragmento de espada.',
    ['46-004', '46-213'])

questions = [
    ('¿Quién mató a los ocupantes de la cueva y qué relación tiene Zoltan con esos cadáveres? El aspecto eléctrico y la sospecha de Eleanor no demuestran su autoría (46-019, 46-021, 46-105, 46-204).',
     'Encuentran cuerpos ennegrecidos como por una descarga y a Zoltan vivo y encadenado. Eleanor sospecha de él; sus descargas posteriores muestran capacidades, sin reconstruir las muertes anteriores.',
     ['46-019', '46-021', '46-105', '46-204'], 'La autoría, los motivos y la secuencia de las muertes de la cueva.'),
    ('¿Qué cartel recuerda Zoltan al conocer a Ione y qué causa su dolor? El flash es borroso e ilegible y no fija una recompensa, acusación o vínculo previo concreto (46-024).',
     'El nombre y el aspecto de Ione provocan un pinchazo y una imagen fugaz. Citlali lo sostiene, pero no se explica o lee el cartel.',
     ['46-023', '46-024'], 'El contenido del cartel, el origen del recuerdo y su relación con Ione.'),
    ('¿De dónde proceden la cicatriz y la mancha oscura de Zoltan, y por qué estaba cautivo? Su presentación no reconstruye el origen de las marcas ni la duración y circunstancias del encierro (46-019–46-025, 46-101).',
     'Zoltan está débil, hambriento, marcado y encadenado. Ione rompe el soporte que lo retiene. Él no sabe precisar cuánto tiempo ha pasado allí.',
     ['46-019', '46-020', '46-022', '46-023', '46-025', '46-101'], 'El pasado de Zoltan, sus marcas y quién y por qué lo encerró.'),
    ('¿Cuál es el origen de la electricidad de Zoltan y conseguirá controlarla? Descargas de contacto, barrera y rayos son observables; la extracción del colmillo y las chispas de las casas muestran descontrol (46-105, 46-107, 46-109, 46-116, 46-120, 46-204, 46-206).',
     'La electricidad hiere a compañeras por contacto y lo protege de un coletazo. Zoltan la canaliza en rayos durante la lucha, pero después chamusca el cadáver y prende pequeños fuegos sin querer. Admite que no controla bien el efecto.',
     ['46-105', '46-107', '46-109', '46-111', '46-116', '46-120', '46-204', '46-206'], 'El origen, condiciones, límites y dominio estable de sus capacidades.'),
    ('¿Qué dicen las inscripciones de la copa hallada por Eleanor y cuál es su procedencia? Se distingue de otra copa anterior y se presenta como tesoro, sin lectura o poder ritual probado (46-102).',
     'La copa de apariencia dorada tiene joyas e inscripciones. El director la distingue de la anterior y la describe como tesoro para vender; no se interpreta su escritura.',
     ['46-102', '46-220'], 'Su procedencia y la lectura de las inscripciones; la venta general no documenta un análisis.'),
    ('¿Dónde está el novato llamado Jacki y a quién corresponde esa mención? Sus compañeros dicen que faltaba desde la playa, sin confirmar su identidad con Jack o el cautivo de Taylor ni su destino (46-214–46-215).',
     'Ione lo echa de menos al revisar a sus hombres. Los trillizos lo recuerdan ausente al dejar la playa. Las conjeturas de tiburones o muerte no son un desenlace demostrado.',
     ['46-214', '46-215'], 'Su identidad, paradero y circunstancias de la desaparición.'),
    ('¿Cómo reunirá Ione los apoyos para recuperar Shiaru y qué encontrará al volver? La venta a Froger aporta veinticuatro monedas, sin reclutamiento o reconquista representados (46-215, 46-218).',
     'Ione anuncia que venderá una joya y buscará gente nueva para su causa. Obtiene veinticuatro monedas, pero todavía no organiza o ejecuta el regreso al puerto.',
     ['46-215', '46-218'], 'Los apoyos, la expedición, la situación del puerto y el resultado del plan.'),
    ('¿Se celebrará la reunión de madres con Citlali y cómo continuará la convivencia escolar de Leo y Etley? La invitación de Miausi y la reprimenda no representan la reunión o el regreso del niño (46-209–46-211, 46-219).',
     'Miausi invita a Citlali a la reunión del domingo. Citlali reprende a Leo y se lleva a Etley; el niño corre a buscar a Naór y no se muestra su encuentro.',
     ['46-209', '46-210', '46-211', '46-219'], 'La reunión, el regreso de Leo y la evolución de la convivencia en el colegio.'),
]

missions = [
    'Llegar a Iktan y reencontrar a los compañeros: la estampida y el río separan a Ione, Eleanor y Citlali. Las primeras rutas fallan, pero Citlali acaba reconociendo los senderos y llegan a la ciudad y su taberna (46-004–46-015, 46-207–46-208).',
    'Rescatar y atender al cautivo: Ione despierta y libera a Zoltan rompiendo el soporte de madera; Citlali lo sostiene, lo acompaña a limpiarse y le busca ropa. El rescate se completa, sin explicar su pasado o el cartel que recuerda (46-019–46-025, 46-101, 46-103–46-105).',
    'Sobrevivir a los dos tiranosaurios: los rayos de Zoltan matan a uno y Citlali drena al último; ambos quedan muertos. La recuperación de los viajeros es parcial y el intento eléctrico de obtener un colmillo lo destroza (46-107–46-120, 46-201–46-205).',
    'Reunir a la tripulación: encuentran a varios hombres y compañeros que esperaban en Iktan, pero el novato llamado Jacki sigue ausente y su destino no se conoce (46-208, 46-213–46-215).',
    'Preparar la recuperación de Shiaru: Ione plantea financiarse y reclutar apoyos; vende el collar a Froger por veinticuatro monedas. No se ejecutan todavía el reclutamiento o la reconquista (46-215, 46-217–46-218).',
    'Consultar a Walulu por la maldición: Citlali explica el drenaje como parte de ella y acepta acompañar a Ione ante la chamana. La consulta queda pendiente y no se representa una cura o lectura de los tatuajes (46-216–46-218).',
    'Volver a cuidar de Etley: Citlali lo encuentra con Leo en el colegio, lo recoge y recibe la invitación de Miausi a la reunión de madres. La cría sigue siendo un dinosaurio y no demuestra entender las lecciones de modales (46-209–46-211, 46-219).',
]

editorial = dict(etapas=stages, historias_entidades=histories, misiones=missions,
    preguntas=[item[0] for item in questions],
    contradicciones=[v for d in deliveries for v in d['contradicciones']],
    nombres_dudosos=[v for d in deliveries for v in d['nombres_dudosos']],
    seguimiento_anterior=updates,
    seguimiento_nuevo=[dict(respuesta=answer, referencias=refs, pendiente=pending) for _, answer, refs, pending in questions],
    catalogo=[dict(nombre='Angelique', visible=True, descripcion=angelique['descripcion'], nota=angelique['nota'])])
save(FOLDER / 'edicion_integrada.json', editorial)
print(f"Edición: {len(stages)} etapas; {len(updates)} preguntas anteriores con nuevas evidencias; {len(questions)} preguntas nuevas.")
