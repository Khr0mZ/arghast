"""Integra la lectura completa y el cotejo entre sesiones del capítulo 48."""
import hashlib
from pathlib import Path
from preparar import ROOT,FOLDER,save
from construir import read_json,sha


def role(scene,mid,description):
    path=ROOT/f'campanas/xoltacan/conocimiento/rol_escrito/escenas/{scene}.json'
    source=next(m for m in read_json(path)['fuentes'] if m['id']==mid)
    return dict(escena=scene,mensaje_id=mid,descripcion=description,url=source['url_discord'],texto_sha256=source['texto_sha256'])


def main():
    ds=[read_json(FOLDER/f'entrega_{i}.json') for i in (1,2,3)]
    before={q['id']:q for q in read_json(FOLDER/'seguimiento_antes.json')}
    checks=[]
    for d in ds:
        for q in d['cotejo_preguntas_asignadas']:
            assert q['sha256_pregunta']==hashlib.sha256(before[q['id']]['pregunta'].encode()).hexdigest()
            checks.append(dict(id=q['id'],bloque=d['bloque'],sha256_pregunta=q['sha256_pregunta'],observacion=q['observacion'],referencias_provisionales=q.get('referencias',[])))
    assert len(checks)==len({q['id'] for q in checks})==295
    stages=[s for d in ds for s in d['etapas']]
    histories=[h for d in ds for h in d['historias_entidades']]
    for h in histories:
        for stage in h['etapas']:
            stage['texto']=stage['texto'].replace(
                'La atribución debe cotejarse con el relato de Walulu del capítulo anterior, que había hablado del ataque del dragón y de ciento veinte años.',
                'La atribución difiere del relato de Walulu del capítulo anterior, que había hablado del ataque del dragón y de ciento veinte años; se conserva esa diferencia sin imponer identidad al atacante antiguo.')
    updates={}
    def update(qid,answer,refs=(),pending=None,state=None,sources=()):
        old=before[qid]
        updates[qid]=dict(respuesta=answer,referencias=list(dict.fromkeys(old['referencias']+list(refs))),
            pendiente=old['pendiente'] if pending is None else pending,estado=state or old['estado'])
        if sources:updates[qid]['fuentes_rol']=list(old.get('fuentes_rol',[]))+list(sources)
    update('P31-001','La grafía confirmada sigue siendo Clolgedranx y la continuidad de la voz no cambia. '
        'La investigación del capítulo 48 obliga a reabrir la parte histórica: el director cuenta un ataque dracónico '
        'antiguo seguido de un ritual y Tesara lo atribuye expresamente a otro dragón. No se proporciona nombre ni color '
        'de aquel atacante. Se conserva la diferencia respecto al relato de Walulu del 47, sin imponer que ambos sean '
        'el mismo individuo o que el empleador actual sea el atacante antiguo.',
        ['48-108','48-109','48-110','48-111','48-112'],
        'La identidad del atacante antiguo y la conciliación de las atribuciones históricas; la fecha de cien o doscientos años es aproximada.', 'parcial')
    update('P31-002',before['P31-002']['respuesta']+' La investigación atribuye al dragón una historia de creación de '
        'no muertos. La nueva cueva vuelve a presentar cadáveres que atacan y un rastro mágico que se disipa, sin '
        'mostrar el mecanismo completo de su animación. La conexión de seis horas es Susurro psiónico de Eldrath '
        'y el miedo inicial de Tesara procede del rugido de Naór; ninguno demuestra la terminación de la influencia dracónica.',
        ['48-108','48-134','48-138','48-139','48-208','48-318','48-331','48-338'])
    # Conservar también las fuentes escritas del cotejo anterior.
    updates['P31-002']['fuentes_rol']=before['P31-002'].get('fuentes_rol',[])
    cave=('Tryel recuerda la cueva en la que se envenenó y vuelve a reconocer el recorrido. El grupo llega siguiendo '
        'rastros y señales del terreno, explora sus salas y derrota a una serpiente esquelética y otros muertos. '
        'Naór y Tesara perciben magia antigua que se apaga; el director orienta su interpretación hacia la ausencia '
        'de un dragón. Es un avance sobre aquella localización atribuida a Tryel, sin coordenadas o aparición de '
        'Clolgedranx que prueben la propiedad, ni localización de todas las guaridas.')
    for qid in ('P40-003','P41-009'):
        update(qid,cave,['48-114','48-136','48-137','48-140','48-333','48-337','48-338'],
            'La propiedad y uso preciso de la cueva, la posición actual del dragón y las demás guaridas.', 'parcial')
    update('P40-001',before['P40-001']['respuesta']+' El director describe una historia del dragón creando no muertos '
        'para sobrevivir, pero la cueva del 48 y sus muestras no identifican los cuerpos del claro ni prueban que el '
        'veneno sea el agente de animación. Tesara no encuentra una marca en la serpiente y el rastro mágico se distingue de las pozas.',
        ['48-108','48-331','48-338','48-339','48-341'])
    update('P40-004',before['P40-004']['respuesta']+' Eldrath participa en la exploración y recoge veneno para preparar '
        'defensas. No realiza el interrogatorio ni revela las preguntas pendientes, y la ausencia de Ilikar, Ione y '
        'Poncelot en esta expedición no acredita su aceptación o rechazo del acuerdo.', ['48-114','48-130','48-339','48-340'])
    update('P47-003',before['P47-003']['respuesta']+' Tesara encuentra y guarda un collar durante la exploración, '
        'pero no declara que sea la joya prometida ni lo entrega a Angelique. La conversación personal aplazada tampoco se celebra.',
        ['48-311','48-335'])
    update('P47-005',before['P47-005']['respuesta']+' La historia consultada del dragón habla de crear no muertos, '
        'sin identificar a las víctimas del lago. Los restos y la serpiente de la nueva cueva se mantienen separados '
        'y no ofrecen una demostración del mecanismo de los cadáveres del capítulo 47.', ['48-108','48-331','48-338'])
    update('P47-006',before['P47-006']['respuesta']+' En el 48 Eldrath crea un enlace psiónico de seis horas con '
        'Tryel, Tesara y Coyote, excluyendo a Naór. Ese poder voluntario, el rugido de Naór y la parálisis causada '
        'por Tryel no se identifican con la compulsión dracónica ni prueban que haya acabado.', ['48-134','48-138','48-139','48-330'])
    updates['P47-006']['fuentes_rol']=before['P47-006'].get('fuentes_rol',[])
    update('P47-007',before['P47-007']['respuesta']+' Tesara vuelve de los archivos convencida de que parece '
        'trabajar para otro dragón. Esa interpretación no identifica ni verifica la naturaleza del contratante; '
        'tampoco lo equipara con el dragón del ataque antiguo.', ['48-112'])
    update('P47-008','Tesara dice que queda un plazo de seis días y el grupo decide investigar en vez de entregar '
        'a los hermanos. Se prepara, sigue el recuerdo de Tryel, explora la cueva y recoge material para futuras '
        'pociones. El rol anterior muestra rondas y defensas intensificadas según Naór, pero no se representa un '
        'ataque a Iktan, una entrega o el desenlace del ultimátum.',
        ['48-113','48-114','48-115','48-130','48-339','48-340','48-341','48-342'],
        'La preparación efectiva contra la hueste, la elaboración de las defensas y el desenlace del plazo.', 'parcial',
        [role('x-1530967691991584870','1530974657724022834','Naór cuenta que Walulu intensifica rondas y defensas; es anterior al vídeo 48.')])
    update('P47-010','Tesara estudia con los documentos de Walulu y obtiene historia del dragón y del ritual, '
        'sin una debilidad explotable o una fórmula que pueda reproducir. La expedición llega a una cueva vinculada '
        'por Tryel con su emboscada y obtiene rastros de presencia dracónica y muestras de veneno. No fabrica '
        'un antídoto o una defensa probada ni ve a Clolgedranx.',
        ['48-103','48-108','48-109','48-110','48-111','48-112','48-140','48-333','48-338','48-339','48-340','48-341'],
        'La identificación y localización actual del dragón, el análisis y elaboración de las muestras y una estrategia eficaz.', 'parcial')
    updates['P47-010']['fuentes_rol']=before['P47-010'].get('fuentes_rol',[])
    update('P47-011',before['P47-011']['respuesta']+' La escena de Naór con Walulu y la tortuga trata del control '
        'de la ira y de sus obligaciones con Leo. No se identifica con la reunión futura del 47 o el concilio de Tutucan.', ['48-118','48-119','48-120'])
    post='x-1532155716633231392'
    school_sources=[role(post,'1532164256433442926','Naór toma a Leo en brazos y se lo lleva con Citlali después del vídeo.'),
        role(post,'1532168093055320195','Naór propone ayuda mutua para recoger a los niños.'),
        role(post,'1532168948521373836','Citlali acepta; no se representa el cambio de autorizaciones ante la directora.')]
    update('P46-008','El epílogo del 48 deja a Leo esperando y a Naór corriendo todavía por la jungla. El rol '
        'posterior sí representa la recogida: Naór toma al niño en brazos y lo lleva con Citlali; Leo y Eztli juegan '
        'juntos. Las madres acuerdan ayudarse a recogerlos, sin representar una autorización escolar actualizada '
        'o la reunión de madres pendiente.', ['48-122','48-123','48-233','48-343'],
        'La celebración de la reunión de madres, la formalización del acuerdo de recogidas y la convivencia posterior.', 'parcial',school_sources)
    update('P21-004',before['P21-004']['respuesta']+' Naór vuelve a asumir la recogida, aunque llega tarde; '
        'el encuentro efectivo ocurre en el rol posterior. Su acuerdo de ayuda con Citlali no formaliza una '
        'custodia por Eromov ni evalúa las secuelas del niño.', ['48-122','48-123','48-343'],sources=school_sources)
    update('P43-006',before['P43-006']['respuesta']+' La siguiente escena escrita muestra a Erandi sobresaltada '
        'por el recuerdo de la batalla. Eleanor la calma, le explica que están en Iktan y la saca a explorar. '
        'No se observa una recuperación plena o un diagnóstico del trance.',sources=[
            role('x-1530518117015490690','1530518117015490690','Erandi teme que continúe la batalla.'),
            role('x-1530518117015490690','1530566908557136032','Eleanor la tranquiliza y sitúa el reencuentro en Iktan.')])
    update('P46-002',before['P46-002']['respuesta']+' En el rol previo al 48, hablar de barco y naufragio '
        'provoca nuevos flashes y dolor. Zoltan confunde a Citlali con otra mujer y pierde el conocimiento, '
        'sin identificarla o aclarar el cartel o su relación con Ione.',sources=[
            role('x-1530644840214429887','1530659335040925767','Las palabras sobre barco y naufragio desencadenan dolor.'),
            role('x-1530644840214429887','1530662576520958003','Zoltan percibe a otra mujer sin identificarla.')])
    update('P46-004',before['P46-004']['respuesta']+' El rol previo muestra una descarga que quema un árbol '
        'y una calma momentánea junto a Citlali. En la huida posterior junto a Naór intenta lanzar rayos y no '
        'consigue hacerlo. Son oscilaciones observadas, sin origen o dominio estable explicados.',sources=[
            role('x-1530644840214429887','1530653941413711952','Una descarga involuntaria quema un árbol.'),
            role('x-1531074007103832238','1531079941637013686','Zoltan intenta usar sus rayos mientras huye, sin resultado.')])

    new=[]
    def question(text,answer,refs,pending):new.append(dict(pregunta=text,respuesta=answer,referencias=refs,pendiente=pending))
    question('¿Cómo funciona el ritual protector de Iktan y cuáles son sus límites precisos? (48-110–48-111).',
        'Tesara conoce su finalidad general, pero carece de la capacidad mágica necesaria para comprenderlo por entero. No recibe una fórmula reproducible.',
        ['48-110','48-111'],'La explicación del ritual, sus condiciones y límites más allá de la protección descrita.')
    question('¿Se completará el tatuaje de Eldrath y qué efecto tiene llevarlo a medias? (48-126, 48-128, 48-130).',
        'Naór interrumpe al minotauro y se lleva a Eldrath cuando solo ha dibujado la mitad. No se describe una facultad adquirida.',
        ['48-126','48-128','48-130'],'El diseño, terminación y posibles efectos del tatuaje; no se inventa una propiedad por el pago.')
    question('¿Quiénes son los clientes que Eldrath toma por piratas de Shiaru y qué relación tienen con Molly? (48-106, 48-117).',
        'Eldrath sospecha por su apariencia y Molly está próxima a ellos. No se identifican sus nombres, afiliación o participación en la ocupación.',
        ['48-106','48-117'],'La identidad y afiliación de los clientes y su relación concreta con Molly.')
    question('¿Quién anima a los muertos de la cueva y qué relación tiene con la magia que se disipa? (48-318, 48-331, 48-333, 48-338).',
        'Los esqueletos despiertan durante la lucha con la serpiente. Tesara no encuentra marcas; el director distingue la huella mágica dracónica del veneno de las pozas.',
        ['48-318','48-331','48-333','48-337','48-338'],'El creador y mecanismo de animación, el origen del rastro y el vínculo causal que pueda demostrarse.')
    question('¿Servirán las muestras de la cueva para preparar una defensa eficaz contra el dragón verde? (48-339–48-341).',
        'Eldrath y Tesara recogen veneno de las pozas. Coyote obtiene el suyo del colmillo restante. Son materiales para futuras preparaciones, sin receta o ensayo.',
        ['48-339','48-340','48-341'],'El análisis, la equivalencia o diferencia entre muestras, la elaboración de las pociones y su eficacia.')
    question('¿Qué valor, procedencia y destino tendrán los objetos recuperados del tesoro? (48-301, 48-306, 48-311, 48-335).',
        'Hay piezas corroídas y otras conservadas. Tesara guarda un collar y los compañeros continúan registrando; no se valora el conjunto ni se entrega una joya a Angelique.',
        ['48-301','48-306','48-311','48-335'],'Un inventario, valoración y destino del botín sin equipararlo a otros tesoros o collares.')
    notes=[
        'La historia del ataque antiguo conserva la diferencia entre Walulu en el 47 y la atribución de Tesara a otro dragón en el 48. La estimación oral de cien o doscientos años no sustituye automáticamente los ciento veinte del testimonio anterior.',
        'El empleador dracónico es una interpretación de Tesara, sin nombre o naturaleza confirmados.',
        'La red psiónica de Eldrath excluye a Naór; la confusión posterior se corrige y no acredita lectura de mentes o comunicación libre de todos los receptores.',
        'El lanzamiento de Naór contra Coyote se repite y falla. La caída de la serpiente tras el disparo de Tesara se corrige: resiste a un punto y Naór la remata.',
        'El rastro mágico se distingue del veneno. La relación con el dragón se orienta mediante pistas del director, sin aparición física o identidad demostrada del creador de cada muerto.',
        'El epílogo no representa la recogida de Leo; esta queda documentada en la escena escrita posterior y no se adelanta al relato del vídeo.',
    ]
    uncertain=[
        'Reotra: posible grafía del saludo al comerciante minotauro; se mantiene una ficha descriptiva.',
        'La tortuga terapeuta no recibe nombre y no se identifica con Tortas.',
        'Naór es la interlocutora de la clase y madre de Leo; la referencia leonina no incorpora a Leona a la expedición.',
        'Tryel conserva las variantes Triel/Mirien/Miriam por la continuidad de los hermanos. Eldrath sigue distinto de Aerendriel y Clolgedranx de Zarynth.',
        'La profesora felina del epílogo y la directora del rol posterior no reciben nombre propio; no se fusionan automáticamente Miaussy y Miausi.',
    ]
    edition=dict(alias_entidades={},etapas=stages,historias_entidades=histories,
        ajustes_afirmaciones={'48-147':dict(limitacion='La luz de la entrada se pierde durante el descenso; no implica ceguera permanente. Clolgedranx no aparece físicamente en este capítulo.'),
            '48-337':dict(limitacion='La interpelación Mirien se mantiene dentro de la continuidad de Tryel, contrastada con los otros diálogos y la escena escrita de los hermanos. Coyote no carece de toda magia: declara no disponer de una habilidad útil para rastrear esta señal.')},
        misiones=[
            'Investigar la amenaza del dragón: Tesara obtiene historia y límites generales del ritual. El grupo explora la cueva recordada por Tryel y encuentra huella mágica y materiales, sin localizar al dragón o descubrir una debilidad probada (48-108–48-115, 48-333–48-341).',
            'Sobrevivir a la cueva: superan plantas y veneno, derrotan a los no muertos y a la serpiente esquelética y emprenden el regreso, heridos y debilitados (48-202–48-239, 48-327–48-342).',
            'Preparar defensas para el plazo restante: mantienen a los hermanos con el grupo y recogen muestras para posibles pociones. No entregan a los elfos ni fabrican el remedio (48-113, 48-130, 48-339–48-342).',
            'Recoger a Leo: Naór fija una hora de regreso, rechaza un descanso de una hora y parte antes que los demás. El vídeo termina con el niño esperando; el rol posterior representa la recogida y el acuerdo de ayuda entre las madres (48-123, 48-233, 48-334, 48-343).',
            'Controlar la ira y atender los cuidados: Naór realiza una clase con la tortuga y Walulu financia su continuación. Los ejercicios no impiden sus nuevas recaídas durante la expedición (48-118–48-122, 48-128, 48-134).',
            'Equipar la expedición: Eldrath vende un jade, compra armadura y antitoxinas y parte con un tatuaje incompleto. Más tarde el grupo recupera tres botellas y las reparte (48-124–48-130, 48-230–48-232).',
        ],preguntas=[q['pregunta'] for q in new],seguimiento_nuevo=[{k:v for k,v in q.items() if k!='pregunta'} for q in new],
        seguimiento_anterior=updates,contradicciones=notes,nombres_dudosos=uncertain,catalogo=[])
    save(FOLDER/'edicion_integrada.json',edition)
    save(FOLDER/'cotejo_preguntas.json',dict(total=295,lecturas=checks,integracion_completa=True,actualizadas=list(updates),preguntas_nuevas=6,
        criterio='Lectura íntegra por bloques, seguida del cruce del coordinador con los 129 registros y el rol cotejado.',
        propuestas_no_convertidas_en_nuevas_preguntas=['La recogida de Leo está representada en el rol posterior.',
            'El peligro tras la primera sala se concreta en el combate posterior, no queda como misterio abierto.',
            'Las botellas se identifican como antitoxinas y se aclara que Naór no recibe una de las tres dosis.',
            'La propiedad de la cueva, el empleador y el ataque antiguo se siguen en preguntas históricas existentes.']))
    proof=read_json(FOLDER/'cotejo_rol.json');postpath=ROOT/f'campanas/xoltacan/conocimiento/rol_escrito/escenas/{post}.json';source=read_json(postpath)
    agent=read_json(FOLDER/'cotejo_rol_posterior_b2.json')
    assert agent['lectura_completa'] and agent['fuente_sha256']==sha(postpath)
    assert agent['mids_leidos']==[m['id'] for m in source['fuentes']]
    if not any(r['escena']==post for r in proof['escenas']):
        proof['escenas'].append(dict(escena=post,archivo=postpath.relative_to(ROOT).as_posix(),sha256=sha(postpath),
            lectura_completa=True,leido_por='cap48_bloque2',mensajes_leidos=agent['mids_leidos']))
    proof.update(total_mensajes=349,mensajes_leidos_nuevamente=226,mensajes_con_lectura_previa_verificada=123,
        cotejo_posterior=dict(archivo='cotejo_rol_posterior_b2.json',sha256=sha(FOLDER/'cotejo_rol_posterior_b2.json')))
    save(FOLDER/'cotejo_rol.json',proof)
    print('Edición integrada:129 evidencias,23 etapas,295 preguntas cotejadas y6 nuevas.')


if __name__=='__main__':main()
