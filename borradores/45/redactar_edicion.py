"""Cotejo de identidades, desenlaces y seguimiento tras las tres lecturas completas."""
from preparar import ROOT, FOLDER, read_json, save


def main():
    deliveries = [read_json(FOLDER / f'entrega_{n}.json') for n in (1, 2, 3)]
    aliases = {'Sireno hechicero de los Profundos':'Hechicero acuático de los Profundos'}
    stages = [s.copy() for d in deliveries for s in d['etapas']]
    stages[4]['texto'] = stages[4]['texto'].replace('Coyote y Tortas miran al frente, donde el descubrimiento siguiente queda fuera de este primer tramo.', 'Coyote y Tortas miran al frente mientras continúan siguiendo el rastro.')
    stages[8]['texto'] = stages[8]['texto'].replace('otro sirénido de aspecto diferente', 'otro ser acuático de aspecto diferente')
    proposals = [p for d in deliveries for p in d['historias_entidades']]
    catalog = read_json(ROOT / 'config/entidades.json')
    groups = {g['nombre']:g for g in catalog['grupos']}
    grouped = {}
    for p in proposals:
        name = aliases.get(p['nombre'],p['nombre'])
        if name in groups and groups[name].get('visible') is False:
            continue
        grouped.setdefault(name,[]).append(p)

    core = {
        'Naór': ('De Iktan a la audiencia de Perlasal',
            'Naór prepara la visita de Perlasal por la convocatoria de Tutucan. Antes negocia dos horas más de permanencia de Leo en el colegio, tras una discusión sobre su conducta, y autoriza a otra persona para recogerlo. Walulu ofrece una burbuja de una hora que quizá no baste; la princesa obtiene después respiración acuática mediante el beso de una enviada de Maris. Su miedo al agua persiste y se aferra a Tortas. Ayuda a buscar al escuadrón de la guía, detecta magia residual de armas y lo impulsa hacia el norte para dejar atrás cuatro tiburones. En el escondite combate junto a los compañeros, aparta a un defensor de Tentacol y cae sobre él con el hacha. En el altar queda aturdida por el grito de una criatura y consigue después dejar inconsciente al sacerdote, aunque Chopito lo mata. Detecta magia intensa en el altar y en el agua antes de salir con la cautiva rescatada. Maris le consigue una audiencia con Ivet. La princesa defiende la actuación de Atlan y pide acudir al concilio, sin obtener todavía la aceptación de Perlasal.'),
        'Tortas': ('El viaje, los brazos astrales y los trofeos',
            'Tortas acepta acompañar a Bigotitos a Perlasal, sin aceptar el culto que pretende Chopito. Su pregunta por el año y la hora provoca un destello cuyo significado no se explica. La guía le concede respiración acuática y lleva a Naór y otros compañeros sobre el caparazón. Grita los nombres del escuadrón mediante la voz astral; no obtiene respuesta y el grupo huye de los tiburones. Gira hacia un túnel y se raspa el caparazón antes de emerger a una cámara de aire. En la primera lucha utiliza brazos astrales azules y, al terminar, guarda una mano de un cadáver. En el islote del altar se repliega en la concha, recibe zarpas y un mordisco, y vuelve a manifestar los brazos cuando los anteriores ya han terminado. Enfadado por el daño al caparazón, acaba con la criatura que aturdió a Naór y conserva un fragmento de su rostro, distinto de la mano anterior. Llega a Perlasal con los compañeros y sigue buscando una piedra donde estar cómodo. Sus manifestaciones y bromas no resuelven la discrepancia entre las edades que se le atribuyen.'),
        'Triel': ('La apnea, las luces y los dos combates',
            'Triel sale del lago con un pez tras practicar la apnea. Las manos arrugadas no prueban una transformación; obtiene el medio real de respirar cuando Naór acerca a la guía para que también la bese. Disfruta del recorrido por las corrientes y de la velocidad de Tortas. En la cueva aporta luces, pregunta cómo distinguir a los aliados y combate a los defensores deformados. En la segunda lucha recibe heridas, mata al enemigo que la atacaba en el agua y ayuda mágicamente a Naór; Coyote consigue curarla después de un primer intento que no alcanzaba. Su propuesta de atacar a la cautiva es detenida y no se ejecuta. Guarda un hueso para su hermano, sin entregárselo en el vídeo. Al terminar la audiencia se interesa por un caballo de cola marina y pregunta si puede probarlo. La monta se representa posteriormente en el rol escrito, no en el cierre del vídeo.'),
        'Tentacol': ('Buscar a los desaparecidos y servir a Chopito',
            'Tentacol busca compañeros para ir a Perlasal y transmite las pretensiones de Chopito. Ya puede desenvolverse bajo el agua y sigue a la guía por las corrientes. Examina coral roto y señales de armas en las ruinas del ataque. En la cámara oscura utiliza los ojos del pulpo y combate con rayos y un tentáculo mágico distinto de su familiar. Traduce las instrucciones de su señor cuando el grupo oye la conversación en Aquan. Ante el altar ataca a los oficiantes, reduce parte del daño de Tortas y pide conservar vivo al sacerdote. Lo coloca inconsciente junto a Chopito y prepara humo y luces que agrandan la sombra del pulpo; la escena termina con la muerte del cautivo, sin interrogatorio. Encuentra una perla al registrar un cuerpo y recuerda leyendas de un kraken de otro plano, mientras afirma su fe en Chopito. Maris lo reconoce al llegar a Perlasal. Nada de ello explica retrospectivamente su excepción a la compulsión del bosque del capítulo 41.'),
        'Chopito': ('Un culto rechazado y un sacerdote ejecutado',
            'Chopito pretende reclutar a Tortas como súbdito y dirige a Tentacol, pero el Anciano solo acepta el viaje. Ayuda a guiar en la oscuridad, presta sus sentidos y combate junto al grupo. Al escuchar a los oficiantes pedir sacrificios para resucitar a un dios interpreta que hablan de él y se presenta en Aquan como su divinidad. Los enemigos no lo reconocen y ordenan atacar y capturar a Tentacol. El pulpo manda combatirlos y falla un intento de agarrarse a la cara de uno. Después Naór deja inconsciente al sacerdote a petición de Tentacol. Entre humo y una sombra agrandada, Chopito proclama su supremacía y lo mata abriéndose paso por su cuerpo. La muerte sí se representa; la divinidad, el culto previo y sus supuestas víctimas anteriores siguen siendo afirmaciones suyas.'),
        'Coyote': ('El contacto con Maris y el rescate',
            'Expulsado otra vez de la taberna de Iktan tras sus cortejos, Coyote se une a la visita que prepara Naór. Sumerge su perla para hablar con Maris y recibe la noticia de nuevos secuestros. La enviada le concede respiración acuática y él insiste en ayudar a encontrar a su escuadrón antes de ir a Perlasal. El viaje le causa mareo. En los combates falla varios ataques con el cuchillo, pero inspira a Naór, Chopito y Triel y aparta a un enemigo mediante susurros. Su orden de alto a tres rivales fracasa y el sacerdote consigue imponerle otra. Liberado al quedar inconsciente el oficiante, cura a Triel y desata a la sirena. La ayuda a salir porque la herida de la cola le impide nadar. Maris lo recibe de nuevo con alegría. Las bromas sobre la suegra no convierten esa relación en un matrimonio ni su aspecto majestuoso en divinidad.'),
        'Maris': ('Ayuda desde la perla y una nueva audiencia',
            'Maris informa por la perla de nuevos ataques de los Profundos, secuestros y el cierre de Perlasal. Envía a una sirénida para facilitar la respiración del grupo y ayudarlo a regresar. La enviada y la cautiva posterior son personas distintas de ella. Al llegar los viajeros con la rescatada, Maris agradece a Coyote la nueva ayuda, reconoce a Tentacol y recibe la petición diplomática de Naór. Los conduce al templo y presenta a Ivet como su madre. La audiencia no consigue todavía una promesa de asistencia al concilio.'),
        'Ivet': ('La audiencia y la antigua promesa',
            'Maris presenta a Ivet como su madre y facilita la entrada al templo. La oficiante reconoce a la princesa de Atlan y permite que exponga la convocatoria. Recuerda la promesa del padre de Naór de mantener juntas a las tribus y reprocha los años de separación, ataques y abandonos. Naór replica que Atlan ha protegido el sur y ayudado a otros pueblos. Ivet responde que meditará acudir al concilio de Tutucan, aunque por ahora es poco favorable a causa de los problemas de Perlasal. También menciona el regreso de los yuan-ti. Vuelve a sus salmos en Aquan y permite que los visitantes permanezcan. El tratamiento de majestad y su autoridad no identifican la deidad a la que oficia.'),
        'Profundos': ('Un escondite y un rito interrumpido',
            'Maris atribuye al grupo un nuevo ataque y el secuestro de habitantes de Perlasal. La guía muestra las ruinas donde cayó su escuadrón y admite haber huido cuando aún quedaban compañeros. El rastro conduce a un escondite con defensores deformados, una cámara de aire y un islote ritual. Los aventureros oyen reclamar más sacrificios y algo que las sirenas tienen para resucitar a un dios. Los oficiantes rechazan a Chopito como divinidad y atacan. Los defensores son vencidos y la sirena atada es rescatada, pero el sacerdote muere antes de que lo interroguen. El altar y el agua conservan magia al partir. No se identifica a la deidad, se inspecciona un kraken o se demuestra la desaparición de toda la red.'),
        'Perlasal': ('El regreso con una rescatada',
            'El nuevo ataque de los Profundos lleva a cerrar la población según Maris. La guía enviada a Iktan conduce al grupo por el lugar donde perdió a su escuadrón y después espera junto al agua mientras los viajeros exploran el escondite. Tras el combate regresa con ellos y con una cautiva de cola herida. Ambas facilitan el paso de los visitantes ante los guardias. Maris recibe a Coyote y presenta a Naór a su madre Ivet en el templo. La princesa convoca al concilio de Tutucan y la oficiante solo promete meditarlo. La visita y el rescate están representados; la alianza política y la eliminación de la amenaza siguen pendientes.'),
        'Atlan': ('La convocatoria ante Ivet',
            'Naór se presenta en Perlasal como princesa de Atlan y ofrece una respuesta común a las amenazas de la isla y el mar. Ivet reprocha al padre de la princesa la promesa incumplida de mantener unidas a las tribus. Naór defiende que el reino ha ayudado a otros pueblos y sostenido la frontera sur pese al aislamiento. Son posiciones de las interlocutoras, sin un relato completo de cada pacto o ayuda. Perlasal no queda comprometida a enviar tropas o asistir al concilio.'),
        'Camar Taruan': ('Una promesa discutida por Ivet',
            'En la audiencia de Perlasal, Ivet recuerda que el padre de Naór prometió mantener unidas a las tribus y sostiene que la separación continuó. La princesa defiende la ayuda y protección prestadas por Atlan. El intercambio documenta dos posiciones sobre la promesa de Camar, sin reconstruir todos sus términos, confirmar quién incumplió cada parte o mostrar un nuevo acuerdo.'),
    }
    histories = []
    for name, parts in grouped.items():
        refs = list(dict.fromkeys(r for p in parts for s in p['etapas'] for r in s['referencias']))
        entity = dict(nombre=name,tipo=parts[0]['tipo'],descripcion=parts[0]['descripcion'],nota=parts[0]['nota'])
        if name in core:
            title,text = core[name]
            entity['etapas'] = [dict(titulo=title,texto=text,referencias=refs)]
        else:
            entity['etapas'] = [dict(s) for p in parts for s in p['etapas']]
            for stage in entity['etapas']:
                stage['texto'] = stage['texto'].replace(' en este tramo','').replace('aquí cuánto tiempo','cuánto tiempo')
        if name == 'Templo de Perlasal':
            entity['etapas'].insert(0,dict(titulo='La visita anterior y el acceso restringido',
                texto='Maris lleva a Coyote y sus compañeros al templo de una gran concha decorada. Ivet oficia con tocado y joyas y desconfía de los habitantes de la superficie. Hace responsable a Maris de haberlos traído. Cuando Ayoto intenta volver para conocer sus creencias, los guardias exigen permiso y la oficiante le pide actos que demuestren sus intenciones, sin revelar el nombre de su deidad.',
                referencias=['29-020','29-021','29-025']))
        histories.append(entity)
    histories.append(dict(nombre='Fragmento del rostro de la criatura del altar',tipo='objeto',
        descripcion='Trofeo que Tortas arranca del rostro de la criatura que lo atacó en el altar.',
        nota='Se describe primero como oreja y después como parte de la boca. No se fija una anatomía más precisa ni se fusiona con la mano guardada tras la primera lucha.',
        etapas=[dict(titulo='Un recuerdo del daño al caparazón',texto='Tras matar con sus puños astrales a la criatura del altar, Tortas arranca un fragmento de su rostro y continúa golpeando el cadáver mientras se queja del caparazón. La pieza se conserva como trofeo, sin propiedades mágicas o uso posterior demostrados.',referencias=['45-216'])]))

    def override(name, description, note):
        e = next(e for e in histories if e['nombre']==name)
        e['descripcion'],e['nota'] = description,note
    override('Hechicero acuático de los Profundos','Ser acuático de aspecto distinto al de los sirénidos aliados que emplea rayos, imágenes y curación junto al altar.',
        'Nombre descriptivo por su función. No se fija una especie de bestiario o un nombre propio, ni se lo confunde con el sacerdote o la criatura que grita.')
    override('Criatura tentacular del altar','Criatura del escondite que ataca el caparazón de Tortas y aturde a Naór mediante un grito.',
        'Adversario distinto del sacerdote de barbilla tentacular, Chopito y el kraken de las leyendas. Su grito no es un conjuro ni depende de concentración.')
    override('Escondite de los Profundos','Refugio accesible por un túnel submarino, con una cámara de aire, estanques e islote ritual.',
        'Nombre editorial descriptivo. Distinto de Perlasal, de las ruinas del ataque al escuadrón y de otras cuevas de la campaña. La salida no demuestra que su magia quede desactivada.')
    override('Altar de los Profundos','Altar del islote interior donde se retiene a una sirena y se detecta una intensa concentración de magia.',
        'Distinto del altar del templo de Perlasal y del altar de los símbolos de Citlali. No queda identificado su consagrante ni el origen de la magia del agua.')
    override('Ivet','Oficiante y autoridad de Perlasal, madre de Maris.',
        'Ivet/Irbet/Irvete/Irbetta se enlazan por localidad, función y continuidad con Maris. Su parentesco se explicita en el capítulo 45; no se identifica una deidad a partir de las bromas de los visitantes.')

    fixes = {
        '45-027':dict(limitacion='El grupo deja atrás a los tiburones sin un combate contra ellos ni bajas representadas. La velocidad es la resolución particular de la mesa, no un vehículo o poder de rastreo nuevo.'),
        '45-120':dict(limitacion='Sacerdote y hechicero acuático son etiquetas descriptivas de función, sin nombres personales o especies de bestiario fijados. La cautiva no se identifica por nombre con Maris o con una de las personas desaparecidas.'),
        '45-201':dict(afirmacion='Chopito se acerca al agua y empieza a nadar. El ser acuático de aspecto extraño se toca a sí mismo para prepararse, mientras el otro enemigo levanta un cuchillo ante la cautiva y recita palabras extrañas. Tentacol avanza nadando y lanza un rayo que atraviesa a ambos adversarios; invoca además su tentáculo, cuyo ataque no alcanza en ese turno.'),
        '45-206':dict(afirmacion='Chopito vuelve al frasco de Tentacol. El hechicero acuático habla en Aquan, llama inferiores a los aventureros y sostiene que su dios les enseñará el verdadero poder cuando venga. Lanza un enorme rayo en una línea que afecta a Tortas, Coyote y Tentacol. Coyote supera después la prueba para mantener la concentración.'),
    }
    facts = {f['id']:f for d in deliveries for f in d['afirmaciones']}
    fixes['45-216'] = dict(entidades=list(dict.fromkeys(facts['45-216']['entidades']+['Fragmento del rostro de la criatura del altar'])))
    missions = [
        'Visitar Perlasal: Naór obtiene respiración acuática de la enviada de Maris y viaja con Tortas, Triel, Coyote y Tentacol. La ruta cruza túneles y corrientes y termina con una entrada efectiva en la población submarina (45-008–45-019, 45-101–45-102, 45-222–45-224).',
        'Buscar al escuadrón desaparecido: la guía corrige su versión inicial y da cuatro nombres. El rastro conduce a una cautiva sin nombre, que sale con el grupo y llega a Perlasal; no se establece el destino de cada integrante enumerado (45-020–45-025, 45-104, 45-120, 45-217, 45-222).',
        'Interrumpir el sacrificio: el grupo vence a los defensores y Coyote desata a la sirena. El sacerdote conservado inconsciente muere ejecutado por Chopito, sin un interrogatorio o confesión (45-118–45-124, 45-201, 45-212, 45-216–45-218).',
        'Investigar el culto: oyen reclamar sacrificios para resucitar a un dios y detectan magia en el altar y el agua. La identidad del dios, el alcance de la red y el destino del kraken no se resuelven; el altar no se desactiva (45-118, 45-206, 45-218, 45-220–45-221).',
        'Convocar a Ivet al concilio de Tutucan: Maris facilita la audiencia. Naór presenta la invitación y defiende a Atlan; Ivet solo promete meditarla y no confirma asistencia o tropas (45-223–45-226).',
        'Organizar el cuidado de Leo: Naór negocia dos horas más y autoriza una recogida alternativa. El vídeo no representa esa recogida; las escenas escritas posteriores conservan su espera y la llegada de Tessa (45-003–45-004, 45-010–45-011).',
        'Atender a los heridos: Tortas bebe una poción, Tentacol lo protege y Coyote cura a Triel. La rescatada sigue necesitando ayuda por la herida de la cola y no se muestra su curación completa (45-208, 45-214, 45-217, 45-222).',
    ]
    questions = [
        '¿Qué destino tuvieron Alfira, Zamuria, Jariora y María Antonieta? La guía huyó cuando quedaban compañeros y la cautiva del altar no se identifica con uno de esos nombres (45-020, 45-024–45-025, 45-217).',
        '¿Quién es el dios que los oficiantes quieren resucitar y qué poseen las sirenas que necesitan para ello? Las palabras del culto no identifican a esa divinidad con Chopito o el kraken ni demuestran la eficacia del rito (45-118, 45-121, 45-206, 45-221).',
        '¿Qué consagra el altar y por qué toda el agua del escondite emite magia? La detección no identifica el origen, el efecto completo o una forma de desactivarlo (45-220–45-221).',
        '¿Quedan otros Profundos, cautivos o rituales activos? Se vence a los defensores y se rescata a una sirena, pero no se interroga al sacerdote ni se desactiva el lugar o documenta toda la red (45-116, 45-218, 45-220, 45-222).',
        '¿Aceptará Ivet acudir al concilio de Tutucan? Su respuesta queda en meditarlo, de momento poco favorable por los problemas de Perlasal (45-226).',
        '¿Qué términos tuvo la antigua promesa de unión entre las tribus y qué explica su ruptura? Ivet y Naór ofrecen posiciones distintas sin reconstruir todo el pacto (45-225–45-226).',
        '¿Qué propiedades o utilidad tiene la perla hallada por Tentacol? Su obtención no identifica un efecto, precio o uso (45-219).',
        '¿Se recuperará la cola de la sirena rescatada? Llega a Perlasal con ayuda, pero no se representa un tratamiento o una curación completa (45-217, 45-222).',
        '¿Qué significa el destello de Tortas tras preguntar el año y la hora? La manifestación no fija un cambio de edad o capacidades ni concilia sus cronologías (45-011).',
    ]
    previous = {q['id']:q for q in read_json(FOLDER / 'seguimiento_antes.json')['preguntas']}
    updates = {}
    def update(qid,answer,refs,pending,state=None,role=None):
        updates[qid] = dict(respuesta=answer,referencias=list(dict.fromkeys(previous[qid]['referencias']+refs)),pendiente=pending)
        if state: updates[qid]['estado'] = state
        if role: updates[qid]['fuentes_rol'] = role
    def roles(scene,*ids):
        return [dict(escena=scene,mensaje_id=mid) for mid in ids]
    concilio_role = roles('x-1527436690531029186','1527443109590466710','1527449224642433127')
    update('P29-001','Maris vuelve a informar de secuestros y el grupo inspecciona unas ruinas y un escondite con defensores, un altar y una sirena cautiva. Oyen pedir más sacrificios y algo que poseen las sirenas para resucitar a un dios. Liberan a una cautiva y vencen a los adversarios, pero el sacerdote muere sin ser interrogado y el altar conserva magia. No se localiza un kraken ni se identifica con certeza a ese dios.',
        ['45-013','45-020','45-118','45-120','45-217','45-218','45-220','45-221','45-222'], 'La organización completa, la identidad del dios y el kraken, el funcionamiento del rito y el destino de todos los desaparecidos.', 'parcial')
    update('P29-002','Una enviada anónima de Maris concede respiración acuática a Coyote, Naór, Tortas y Triel mediante besos. Esto añade otro caso observado a los del capítulo 29, sin fijar una duración exacta o una regla general sobre quién puede otorgarla. La burbuja de una hora ofrecida por Walulu es otro método y no llega a aplicarse.',
        ['45-009','45-015','45-016','45-017'], 'La duración del efecto y las condiciones o personas capaces de otorgarlo.')
    update('P29-003','El grupo vuelve con una cautiva liberada y Maris consigue que Ivet reciba a Naór, reconocida como princesa de Atlan. La oficiante permite la audiencia y que permanezcan en el templo, pero no se muestra confianza plena ni una aceptación del concilio. Sus salmos en Aquan no revelan una deidad; el altar hostil pertenece a otro lugar y no identifica su religión.',
        ['45-217','45-222','45-223','45-224','45-226','45-227'], 'La religión y deidad de Ivet y las condiciones para obtener su confianza.')
    update('P41-010','Naór obtiene respiración acuática mediante el beso de la guía enviada por Maris, recorre las corrientes y participa en el rescate. Llega a Perlasal y visita el templo para hablar con Ivet. La visita y el medio de permanecer bajo el agua quedan representados, aunque la duración general del efecto pertenece a otra pregunta.',
        ['45-016','45-017','45-019','45-222','45-223','45-224'], '', 'resuelta')
    for qid in ['P16-004','P17-003','P22-004']:
        answer = previous[qid]['respuesta'] + ' En el capítulo 45 Naór extiende la convocatoria a Ivet, que solo promete meditarla. El rol escrito posterior recoge la explicación de Naór sobre las reliquias de los líderes, la Llave del Sol y la Cámara de los Clanes Elementales; sigue siendo su relato y no se representa la reunión o la apertura.'
        update(qid,answer,['45-008','45-225','45-226'],previous[qid]['pendiente'],role=concilio_role)
    update('P21-004','Leo permanece a cargo de Naór y en el colegio de Iktan; la discusión escolar y la preocupación de Walulu no muestran una aceptación formal de custodia por Eromov o un diagnóstico de secuelas. El rol posterior muestra al niño esperando bajo la lluvia y a Tessa recogiéndolo tras recibir tarde el aviso. El vínculo con Naór continúa, sin formalizar la situación política o jurídica del menor.',
        ['45-003','45-004','45-010','45-018'], 'La aceptación formal de la custodia y la evolución del niño.',
        role=roles('x-1527444416187596951','1527444416187596951')+roles('x-1527455379028574428','1527455379028574428','1527456867213643777'))
    update('P40-005','La respuesta de 1496 y las diez y cuarenta y tres pertenece al calendario ficticio y el destello de Tortas no explica su edad. El rol posterior añade su afirmación de llevar unos setecientos años sin probar otra roca, sin conciliarla con los 77 años declarados y los siglos de inmovilidad que recuerda Walulu.',
        ['45-011'], 'La explicación de las cifras y su cronología personal.', role=roles('x-1527436690531029186','1527458312293974169'))
    tracking = [
        dict(respuesta='La guía da cuatro nombres y corrige su primera afirmación de ser la única superviviente. La sirena rescatada no se presenta con nombre propio.',referencias=['45-020','45-024','45-025','45-217'],pendiente='El destino e identidad de cada persona nombrada y de los demás integrantes.'),
        dict(respuesta='Los oficiantes piden sacrificios y algo que las sirenas poseen para resucitar a su dios. Sus anuncios y las leyendas del kraken no identifican de manera inequívoca a ese ser.',referencias=['45-118','45-121','45-206','45-221'],pendiente='La identidad del dios y los requisitos y eficacia del rito.'),
        dict(respuesta='Naór detecta intensa magia en el altar y extendida por el agua. El grupo parte sin desactivar el lugar o identificar su consagrante.',referencias=['45-220','45-221','45-222'],pendiente='El origen, alcance y consecuencias de la magia y su posible desactivación.'),
        dict(respuesta='Los defensores de las salas son vencidos y se libera a una cautiva, pero el sacerdote muere antes de un interrogatorio y la instalación sigue mágica.',referencias=['45-116','45-218','45-220','45-222'],pendiente='El alcance restante de la red, los demás cautivos y la actividad de otros rituales.'),
        dict(respuesta='Ivet promete meditar la invitación y advierte que su respuesta actual es poco favorable. La discusión posterior entre los viajeros no es una nueva aceptación suya.',referencias=['45-226'],pendiente='Su decisión definitiva y una eventual asistencia.'),
        dict(respuesta='Ivet reprocha la unión incumplida y Naór defiende la protección del sur. En el rol posterior, Naór relata una guerra bajo su abuelo y una tregua mantenida por su padre, sin reconstruir todos los compromisos o confirmar cada atribución.',referencias=['45-225','45-226'],pendiente='Los términos completos del pacto y la historia contrastada de sus incumplimientos.',fuentes_rol=concilio_role),
        dict(respuesta='Tentacol recoge una perla al registrar un cadáver. No se identifica una propiedad, valor o uso y se mantiene distinta de la perla de comunicación de Coyote.',referencias=['45-219'],pendiente='Su utilidad, propiedades y destino posterior.'),
        dict(respuesta='La herida impide nadar a la cautiva y Coyote la ayuda. Sale de la cueva y llega a Perlasal sin curación completa representada.',referencias=['45-217','45-222'],pendiente='El tratamiento y recuperación de la cola.'),
        dict(respuesta='Tortas se ilumina tras recibir la fecha y hora ficticias. No se explica una modificación concreta de edad, poder o estado.',referencias=['45-011'],pendiente='El sentido de la manifestación.'),
    ]
    notes = [
        'Naór leonina y Leona harengon son personas distintas. El vocativo Leona se corrige por la continuidad de la princesa en esta expedición; Triel, Leo y Tessa tampoco se intercambian por una descripción del pelo (45-003–45-004, 45-017–45-018, 45-223).',
        'La directora admite que el incidente del hámster le fue contado por los niños. No se presenta como una acción observada en escena o una acusación probada por ella (45-003).',
        'La burbuja de Walulu solo se ofrece. La respiración representada procede de los besos de la guía, sin una duración exacta que permita igualar ambos métodos (45-009, 45-015–45-017).',
        'La guía corrige su relato de única superviviente: huyó cuando quedaban compañeros. Alfira, Zamuria, Jariora y María Antonieta no se identifican con la cautiva ni con las sombras por conjetura (45-020, 45-024–45-025, 45-104, 45-217).',
        'El rastro de magia residual de armas no es el olor personal de Maris. Las ruinas del ataque, el escondite y Perlasal son lugares distintos. La cueva contiene una cámara de aire y zonas inundadas (45-021, 45-023, 45-101–45-102, 45-120, 45-222).',
        'Aquan sustituye la primera mención a Auran. La familiaridad declarada por Coyote con Auran no garantiza que traduzca el diálogo corregido (45-117–45-118).',
        'El sacerdote, el hechicero acuático y la criatura que grita son adversarios distintos. El grito no es un conjuro ni concentración y el segundo uso anunciado se retira (45-120, 45-204–45-206, 45-213).',
        'Chopito no es reconocido como dios por los oficiantes. Sus proclamas, el humo y la sombra agrandada no acreditan divinidad ni una identidad con el kraken o la deidad buscada por el rito (45-118, 45-121, 45-218, 45-221).',
        'Naór deja al sacerdote inconsciente y Chopito lo ejecuta después. No queda un cautivo vivo o una confesión al cierre; la sirena sí es liberada (45-212, 45-217–45-218).',
        'La detección del altar y el agua confirma magia, sin identificar una maldición concreta o una invocación consumada. Nadie desactiva la instalación (45-220–45-222).',
        'Ivet promete meditar y no confirma asistir. Las afirmaciones sobre las antiguas promesas son posiciones políticas, sin tropas o una alianza ya acordadas (45-225–45-226).',
        'El vídeo termina con la pregunta de Triel sobre el caballo marino. La monta y la recogida de Leo se documentan en escenas escritas posteriores, sin anticiparlas en el metraje (45-004, 45-227).',
    ]
    names = [
        'Naór/Naor/Noor y Bigotitos son la princesa leonina; Leona sigue siendo la harengon de Cuicapalli. Tenta/Tentacol viaja con Chopito, cuyo cuerpo es distinto del tentáculo mágico (45-001, 45-006, 45-110, 45-223).',
        'Ivet/Irbet/Irvete/Irbetta se agrupan por la autoridad y oficiante de Perlasal. Maris se identifica como su hija; la guía enviada y la cautiva son dos sirénidas anónimas distintas (45-015, 45-217, 45-222–45-224).',
        'Sacerdote de los Profundos, Hechicero acuático de los Profundos y Criatura tentacular del altar son etiquetas descriptivas. El director descarta azotamentes para el sacerdote y no se importan otras especies de bestiario (45-120, 45-204–45-206, 45-219).',
        'Alfira, Zamuria, Jariora y María Antonieta conservan grafías provisionales y destinos sin verificar. La broma María Carmen no identifica a la cautiva con una de esas personas (45-024–45-025, 45-217).',
        'Lago Tachan, la directora y el colegio mantienen los límites de su denominación. Musí es una lectura incierta del posible nombre de la docente; el colegio no se equipara automáticamente con la academia de guerreros anterior (45-002–45-004, 45-008).',
        'Angelita/Angelique se mantienen como atribución contextual provisional de la taberna, sin fusionar la identidad con Angélica Thunder por el diminutivo. El caballo de cola marina no recibe nombre o número de montura en el vídeo (45-007, 45-011, 45-227).',
        'La perla de botín no es la perla de comunicación. La mano y el fragmento facial guardados por Tortas son piezas de enemigos diferentes, y el altar del escondite no es el de Citlali o el del templo de Perlasal (45-012, 45-116, 45-216, 45-219–45-220, 45-224).',
    ]
    patches = [dict(nombre=e['nombre'],descripcion=e['descripcion'],nota=e['nota']) for e in histories if e['nombre'] not in groups or e['nombre']=='Ivet']
    save(FOLDER / 'edicion_integrada.json',dict(alias_entidades=aliases,etapas=stages,historias_entidades=histories,
        ajustes_afirmaciones=fixes,misiones=missions,preguntas=questions,contradicciones=notes,nombres_dudosos=names,
        catalogo=patches,seguimiento_anterior=updates,seguimiento_nuevo=tracking))
    print(f'Edición: {len(histories)} historias, {len(questions)} preguntas nuevas, {len(updates)} seguimientos actualizados.')


if __name__ == '__main__':
    main()
