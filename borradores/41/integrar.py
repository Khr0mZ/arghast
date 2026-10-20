"""Integra decisiones editoriales tras la lectura integral de los tres bloques.

No extrae ni resume automáticamente fuentes: los textos y cotejos son editoriales.
La receta conserva los borradores de cada lector y no modifica ningún original.
"""
import copy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import read_json, write_json


def refs(*numbers):
    return [f'41-{number:03d}' if isinstance(number, int) else number for number in numbers]


def stage(title, text, *numbers):
    return dict(titulo=title, texto=text, referencias=refs(*numbers))


blocks = [read_json(ROOT / f'borradores/41/bloque_{i}.json') for i in (1, 2, 3)]
assert all(block['lectura_completa'] for block in blocks)
assert [len(block['registros']) for block in blocks] == [20, 18, 17]
records = copy.deepcopy([row for block in blocks for row in block['registros']])
assert len(records) == 55

# Ajustes del coordinador: no convertir el pronombre «ella» en especie o identidad.
records[22][4] = records[22][4].replace(
    'una mujer no identificada ya viene', 'alguien a quien solo llama «ella» ya viene')
# Solo una abominación es descrita apareciendo; las otras figuras ya combatían.
for index in (37, 38, 45):
    if 'Abominaciones serpiente del festival (capítulo 41)' not in records[index][5]:
        records[index][5].append('Abominaciones serpiente del festival (capítulo 41)')

paragraphs = [
    'Blink relata que por fin salió de Shiaru y despertó fuera del poblado, aunque lleva días perdida mientras busca Cuicapalli. Una fruta le altera la voz. Naór cuenta que consiguió, con ayuda de Walulu, que Leo entrara en la academia de guerreros de Iktan después de un rechazo por su tamaño. El niño sigue teniendo dificultades con otros alumnos. La leonina espera desde hace días a un emisario de Atlan que debía llegar para el festival; pide noticias en la taberna, sin obtener respuesta. Winscore llega desde Cuicapalli atraído por la celebración y observa el contraste entre la vegetación colorida y la zona de casas arruinadas donde se reúne la población. Naór y Leo preparan figuras talladas como ofrendas y se encuentran con Blink. Naór advierte del peligro de una serpiente verde alada, aunque rechaza la explicación de Triel de que sea un dragón.',
    'Tentacol llega nadando con Chopito, un pulpo que transporta en un frasco y al que trata como su señor. Los vecinos reciben a los visitantes con flores y bebida; Blink reconoce a Winscore y lo presenta a Naór. Chopito descubre una silueta en el agua: es Cipo, ennegrecido y debilitado. Tentacol lo recoge y lo coloca junto al fuego, donde recupera poco a poco el color y las llamas. Naór reconoce al elemental. Después presenta sus respetos en nombre de Atlan ante la tortuga venerada, recuerda las visitas de su infancia con Walulu y encarga a Leo observarla sin parpadear como ejercicio de paciencia. Tentacol declara proceder de bosques de algas próximos a Perlasal. Naór desea visitar esas aguas, pero no consiguen un medio para que pueda respirar allí. La comunicación de Chopito es telepática; las burbujas no hacen que todos oigan necesariamente sus palabras.',
    'Una mujer sugiere a Winscore que se lleve la tortuga. El enano resiste la influencia, detecta una ilusión a su alrededor y descubre incoherencias en sus respuestas sobre la fiesta y los hombres serpiente. La golpea con el bastón y provoca la intervención de un guardia. Durante el altercado se pide producir olor a serpiente; el olor que después percibe el guardia no constituye una prueba natural independiente. Los conduce al templo, mientras Naór y Blink se acercan y Leo queda vigilando la figura. Walulu confirma que Leona los avisó desde Cuicapalli y que aumentaron las precauciones. Examina a la sospechosa y la enreda con raíces. Al desaparecer la ilusión quedan expuestos sus rasgos y escamas serpentinos, y el guardia la retiene.',
    'La cautiva se niega a hablar. Walulu explica que puede sujetarla, pero no domina la magia necesaria para forzar su mente. Winscore le quema la cara y un pie con una antorcha. Ella anuncia que algo está por llegar y hará sufrir a sus captores. Walulu atribuye la infiltración al grupo que envenenó a Eromov, sin identificar a quien administró el veneno. Chopito encanta a la mujer y consigue que pida ayuda a Tentacol. Cuando trata de informar, empieza a padecer un dolor que no desaparece al curarle las quemaduras y cuyo origen no se identifica. Tentacol le sumerge la cabeza por indicación de Chopito, rompiendo el encantamiento con la agresión. La prisionera advierte que «ella» viene y no permitirá que descubran lo que buscan. Sitúa a dos sacerdotes al norte de una roca y empieza a mencionar dos grandes abominaciones. Vomita numerosas serpientes, cae muerta y los reptiles huyen a la jungla. No se establece la causa del fenómeno ni la identidad de la presencia anunciada.',
    'Los compañeros vigilan el festival y buscan otras ilusiones. Detectan el rastro de la infiltrada hacia la entrada, sin encontrar otra aura semejante en el poblado. La tortuga también brilla ante detectar magia, sin que se explique la naturaleza de ese brillo. Leo vuelve a la taberna y Cipo aparece ya como una pequeña llama que se mueve. Tentacol transmite el informe y representa la salida de serpientes mediante prestidigitación. Winscore propone cancelar la fiesta o reforzar la vigilancia, pero un guardia exige órdenes de su jefa. Reúnen a los asistentes cerca de la hoguera y del Anciano con el pretexto de los discursos de Walulu; no se confirma una cancelación oficial. El grupo sale al norte bajo una protección que mejora su sigilo. Blink consulta a un conejo cornudo: el animal habla de una gran serpiente que se proclama dueña del bosque y, al precisar la búsqueda de humanoides, recuerda unas mujeres junto a una piedra y señala la dirección.',
    'Junto a la roca encuentran dos mujeres con aspecto de nativas y la misma aura ilusoria. Preparan viales y vigilan el entorno. Una mano de mago acerca el frasco de Chopito y Tentacol percibe a través del familiar un líquido verdoso. Los compañeros sospechan veneno y deciden conservar al menos una enemiga para interrogarla. Chopito cae sobre ellas y les cubre la cara de tinta; una botella se rompe. Winscore golpea y Naór sujeta a una rival contra el suelo. Blink intenta inmovilizar a ambas con magia, pero la resolución se corrige por su resistencia: no quedan las dos paralizadas. Tentacol manifiesta un tentáculo de frío y se oculta mientras Chopito avanza hacia un estanque. Los ataques no letales de Winscore rompen una ilusión. Una adversaria intenta protegerse con santuario y Tentacol lo contrarresta.',
    'La enemiga retenida sugiere a Naór que la suelte. Ella obedece, pero el efecto termina al cumplir la petición y puede volver a golpearla cuando intenta escapar. La criatura cae y sisea. Un ataque con hacha y una furia radiante dejan cegada a una rival; ese turno no nombra con claridad al actor y se conserva sin atribución definitiva. Blink combina metamagia y ataques psíquicos que fuerzan el movimiento de una enemiga. Tentacol ralentiza y empuja con el tentáculo y sus descargas, mientras Winscore insiste en golpear sin matar. Una gran abominación emerge de la vegetación. Apresa a Naór con la cola y la hiere con cimitarra y mordisco venenoso. El anuncio previo de dos abominaciones no se convierte en dos apariciones confirmadas.',
    'Blink libera a Naór mediante telequinesis y aumenta su tamaño. Tentacol mantiene el apoyo con frío, descargas y protecciones, mientras un arquero entre las ramas hiere a Blink con flechas envenenadas sin hacerle perder la concentración en las tiradas mostradas. Uno de los adversarios queda inconsciente por daño no letal. Naór recibe nuevos golpes, se cura parcialmente y logra apartarse; Blink busca cobertura y utiliza magia para desaparecer intermitentemente y atacar la mente de los rivales. Winscore combate con su bastón, soporta ataques reducidos por reacciones de sus compañeros y conserva la concentración. Después de los últimos intercambios, el director confirma la derrota de la abominación. Esto no mata al adversario que habían dejado inconsciente.',
    'El grupo registra y ata al superviviente con intención de interrogarlo. Encuentra veinticuatro monedas y examina cimitarras de buena factura, que los personajes interpretan como indicio de una organización mayor. Naór corta dos cabezas destinadas a Leo y Walulu; Tentacol devuelve a Chopito a la botella y Winscore recoge los recipientes que consideran venenos. Una voz enorme les exige dejar los cuerpos en el bosque para alimentarse. Todos la escuchan, pero Tentacol no sufre la compulsión de los demás. Chopito presenta al emisor como un súbdito suyo, afirmación que no demuestra esa jerarquía. Naór, aún agrandada, carga a sus compañeros y regresa a Iktan. Winscore mira atrás y ve un dragón verde entre las ramas. Se permite conservar las cabezas, pero no se narra que el cautivo sea trasladado, interrogado o devorado. La voz y el dragón quedan asociados por el contexto, sin una identificación verbal inequívoca del emisor.',
    'En Iktan encuentran a Tortas moviéndose y hablando ante la población. Naór se arrodilla, ofrece las cabezas y llora porque en sus visitas infantiles nunca había conseguido verlo moverse. El anciano recuerda sus primeros bigotes. Winscore se presenta como explorador y se cuenta la tradición de que la ciudad se construyó alrededor de la tortuga. Blink se acerca y le aparta el pelo; al rozarla con la nariz, Tortas reconoce un olor antiguo del bosque que el director confirma como olor de dragón verde. La explicación de Blink sobre un rastro de aura sigue siendo una propuesta suya. Naór trae a Leo desde la taberna. Tortas intenta recordar y deletrear el nombre del dragón mientras Winscore toma notas, pero los subtítulos no fijan una grafía segura. El director aclara que desconoce la guarida. La noche llega y la fiesta se disuelve con el anciano aún pronunciando el nombre y Leo vencido por el sueño. No se ejecuta la caza pactada por Eldrat e Ilikar, ni se muestra una cura de Eromov o un análisis de las muestras anteriores.',
]

missions = [
    'Proteger el festival y al Anciano: descubren a una infiltrada, localizan a los sacerdotes del norte y derrotan la amenaza inmediata del combate. No se confirma la eliminación de toda la red ni una cancelación oficial de la fiesta (41-011–41-026, 41-028–41-046).',
    'Recuperar a Cipo: Tentacol lo encuentra debilitado tras salir del agua y lo acerca al fuego. Recupera las llamas y aparece después en el festival; no se informa a Ilikar en escena ni se explica la procedencia del fragmento de espada (41-008, 41-014, 41-024).',
    'Obtener información de la infiltrada: revela la posición de dos sacerdotes y anuncia una presencia llamada «ella», pero muere expulsando serpientes antes de completar la explicación (41-017–41-023).',
    'Interrogar a un superviviente: uno queda inconsciente, es registrado y atado. La voz exige abandonar los cuerpos y no se representa su interrogatorio o traslado a Iktan (41-042, 41-047, 41-049–41-051).',
    'Reunir pruebas de los atacantes: conservan monedas, observaciones de las armas, recipientes de líquido verde y dos cabezas. Naór ofrece las cabezas a Tortas; no se muestra entrega o análisis por Walulu (41-029–41-030, 41-047–41-048, 41-051–41-052).',
    'Esperar al emisario de Atlan: Naór vigila su llegada y pide noticias en la taberna. No aparece ni se explica el retraso (41-002, 41-004).',
    'Acompañar la educación de Leo: Naór relata su admisión en la academia, le encarga observar al Anciano y lo trae al final para verlo moverse. El entrenamiento continúa sin acreditar un rango o sucesión nuevos (41-002, 41-004, 41-009, 41-024, 41-055).',
    'Investigar al dragón: Winscore lo observa y Tortas reconoce su olor en Blink. El nombre sigue incierto y la guarida sin localizar; no se representa un enfrentamiento ni el pacto del capítulo 40 (41-049–41-055).',
    'Visitar Perlasal: Naór expresa el deseo y Tentacol describe su procedencia próxima. No obtiene respiración acuática ni comienza el viaje (41-010).',
]
questions = [
    '¿Quién es el emisario de Atlan esperado por Naór y qué explica su retraso? Su ausencia no demuestra captura, muerte o responsabilidad de los hombres serpiente (41-002, 41-004).',
    '¿Quién es «ella», qué está viniendo a hacer y qué no permitirá descubrir? La prisionera no la nombra y no se identifica su llegada (41-018, 41-023).',
    '¿Qué causa el dolor inexplicado, la expulsión de serpientes y la muerte de la infiltrada? La curación de las quemaduras no lo detiene y no se identifica un agente (41-021–41-023).',
    '¿Por qué querían retirar al Anciano y qué alcance tiene la operación contra Iktan? Se localizan dos sacerdotes y se ve una abominación, sin verificar la segunda anunciada ni toda la red de mando (41-011, 41-023, 41-028, 41-038, 41-046).',
    '¿Qué ocurre con el cautivo vivo después de que la voz exija dejar los cuerpos? No se representa su traslado, interrogatorio o muerte (41-042, 41-047, 41-049–41-051).',
    '¿Qué contienen los viales verdes y qué relación tienen con el veneno de Eromov o la muestra del claro? Winscore recoge recipientes, pero no se analiza su composición ni se equiparan las fuentes (41-019, 41-028–41-030, 41-051).',
    '¿Quién fabrica o proporciona las cimitarras de buena factura y qué organización equipa a los atacantes? La calidad observada no identifica proveedor o mando (41-047).',
    '¿Por qué Tentacol escucha la voz sin sentir la compulsión? La sugerencia de que Chopito lo protege no confirma una causa o inmunidad (41-049–41-050).',
    '¿Cuál es la grafía del nombre del dragón verde, dónde está su guarida y qué relación de identidad tiene con Clodidrax? El olor queda reconocido, pero el deletreo no es seguro y Tortas desconoce la guarida (41-051, 41-054–41-055).',
    '¿Podrá Naór visitar Perlasal y permanecer bajo el agua? La consulta a Chopito no proporciona un medio para respirar allí (41-010).',
    '¿Qué explica el brillo mágico del Anciano durante la vigilancia del festival? La detección no identifica origen o función, ni atribuye ese brillo a la piedra que lo sostiene (41-024).',
]
notes = [
    'Naór, la leonina con Leo, y Leona, la harengon que dio el aviso en el capítulo 40, son personas distintas. El vocativo Leona en un turno del 41 se conserva como desliz o reconocimiento dudoso; la mensajera no recibe acciones por ese nombre aislado (41-002, 41-015, 41-019, 41-025).',
    'El olor a serpiente del primer arresto fue solicitado artificialmente. Las pruebas posteriores son la ilusión detectada y la forma revelada por Walulu, no un olfato natural demostrado del guardia (41-012–41-013, 41-016).',
    'Walulu atribuye la infiltrada al grupo que envenenó a Eromov. No demuestra qué individuo añadió el veneno ni identifica a las dos visitantes anteriores (41-019).',
    'La prisionera cae muerta y las serpientes se dispersan: no se describe una fuga mediante transformación de todo su cuerpo. La violencia, el dolor inexplicado y su muerte se conservan sin inventar una causalidad o autoría (41-018, 41-021–41-023).',
    'La inmovilización inicial de las dos sacerdotisas se corrige por su resistencia a la magia. La sugestión de soltar a una rival termina cuando Naór cumple esa petición; no mantiene un dominio general sobre ella (41-031, 41-034).',
    'Solo se describe la aparición de una abominación. Las referencias de turno a otra serpiente no acreditan una segunda criatura de ese tipo; el número anunciado permanece como testimonio (41-023, 41-038–41-039, 41-046).',
    'Los recipientes verdes de los sacerdotes y la muestra entregada por Leona a Walulu son fuentes materiales diferentes. La tinta de Chopito tampoco se resuelve como veneno ni como oscuridad para todo el grupo (41-029–41-030, 41-051).',
    'La voz del bosque, el dragón observado y el olor reconocido aportan una asociación contextual fuerte, sin identificación verbal inequívoca del emisor, alianza demostrada con los yuan-ti o explicación completa del mecanismo (41-049–41-051, 41-054).',
    'Chopito reclama adoración y llama súbdito al emisor. Sus palabras no prueban divinidad, jerarquía o protección causal de Tentacol frente a la compulsión (41-006, 41-010, 41-049–41-050).',
    'Naór ve moverse a Tortas por primera vez para ella. No implica un segundo despertar, suplantación o inmovilidad entre escenas del 40 y del 41. Sus recuerdos y las bromas sobre antigüedad no resuelven los 77 años frente a los siglos atribuidos (41-003, 41-009, 41-052–41-055).',
    'El reconocimiento olfativo de Tortas por contacto con Blink no amplía su percepción del veneno a una localización general de dragones. El director niega que conozca la guarida y los comentarios previos sobre una ruta no dan coordenadas (41-054–41-055).',
    'Las cabezas se conservan y se ofrecen ante Tortas. No se muestra una entrega a Walulu ni el final del cautivo que dejaron atado; tampoco una cura de Eromov, análisis de la muestra del 40 o recuperación de la vegetación (41-047–41-055).',
]
names = [
    'Tentacol/Tentac/Tenta es una sola identidad nueva de grafía provisional. Tenta se presenta expresamente; las demás variantes se enlazan por continuidad de sus intervenciones y su vínculo con Chopito. No se fija raza, patrón o identidad anterior (41-006, 41-010, 41-022).',
    'Chopito/Choquito/Chapito es el pulpo transportado en un frasco. Se conserva como personaje separado de Tentacol y de Cipo; no se confunde al familiar con cada tentáculo mágico del combate (41-006, 41-010, 41-029–41-032, 41-048).',
    'Winscore/Winscor/Wincore y variantes corresponden al explorador enano ya catalogado. Blink/Bling/Brink corresponden al hada. Naor/Noor/Naór corresponden a Naór, no a Leona ni a Nox (41-001–41-007, 41-024–41-025, 41-034, 41-053).',
    'La tabernera llamada Angelic permanece vinculada a la etiqueta provisional Angelique de la escena del capítulo 39, sin fusionarla por este pasaje con Angélica Thunder. El vocativo aislado Isabel no basta para crear una identidad (41-004, 41-014).',
    'La infiltrada, los dos sacerdotes, el conejo cornudo y la abominación reciben nombres editoriales descriptivos, sin nombres personales o subespecies inventados. La roca exterior es distinta de la piedra sagrada del festival (41-011–41-016, 41-023, 41-027–41-030, 41-038).',
    'Colgen, Los del Grax for Snake y las letras del deletreo no fijan el nombre del dragón. Se mantiene Dragón verde del bosque de Iktan sin fusionarlo con Clodidrax ni afirmar que sean necesariamente distintos (41-054–41-055).',
    'Tortas/torta/Anciano remiten a la tortuga venerada; Bigotitos es el apelativo que da a Naór. Leo es el niño harengon a su cargo. Ictan/Itan/Ian e Iktan se enlazan por el contexto del mismo festival (41-002–41-003, 41-052–41-055).',
]

draft = dict(capitulo=41, estado_revision='revisado', resumen=' '.join(paragraphs),
             registros=records, misiones=missions, preguntas=questions,
             contradicciones=notes, nombres_dudosos=names)
write_json(ROOT / 'borradores/41.json', draft)

divisions = [
    ('Los viajeros, Leo y el emisario ausente', [1, 2, 3, 4, 5]),
    ('Tentacol, Chopito y el rescate de Cipo', [6, 7, 8, 9, 10, 14]),
    ('Una ilusión entre los celebrantes', [11, 12, 13, 15, 16]),
    ('Las últimas palabras de la infiltrada', [17, 18, 19, 20, 21, 22, 23]),
    ('Vigilar la fiesta y buscar al norte', [24, 25, 26, 27]),
    ('Los viales y la emboscada de tinta', [28, 29, 30, 31, 32, 33]),
    ('La sugestión y la abominación', [34, 35, 36, 37, 38, 39]),
    ('Liberar a Naór y sostener el combate', [40, 41, 42, 43, 44, 45, 46]),
    ('Un cautivo y la voz del bosque', [47, 48, 49, 50, 51]),
    ('Tortas y el nombre que no termina', [52, 53, 54, 55]),
]
relatos = read_json(ROOT / 'config/relatos_capitulos.json')
relatos['capitulos']['41'] = [[title, '' if i == 0 else paragraphs[i].split('.')[0] + '.', refs(*numbers)]
                            for i, (title, numbers) in enumerate(divisions)]
write_json(ROOT / 'config/relatos_capitulos.json', relatos)

new_entities = [
    ('Tentacol', 'personaje', ['Tentacol / Tentac (viajero acuático, grafía provisional)', 'Tentacol', 'Tentac', 'Tenta'], [6, 8, 10, 22, 29, 49],
     'Viajero acuático próximo a Perlasal que lleva a Chopito en un frasco y combate junto a Naór, Blink y Winscore.',
     'Grafía provisional. La presentación Tenta y la continuidad con el pulpo enlazan las variantes; no se fija raza ni una identidad anterior.'),
    ('Chopito', 'personaje', ['Chopito (pulpo, grafía provisional)', 'Chopito'], [6, 10, 20, 29, 30, 50],
     'Pulpo telepático vinculado a Tentacol, transportado en un recipiente con agua y capaz de intervenir en la investigación.',
     'Su pretensión de recibir adoración o poseer súbditos es testimonio suyo, sin divinidad ni mando sobre el dragón demostrados.'),
    ('Infiltrada serpiente del festival de Iktan', 'personaje', ['Infiltrada serpiente del festival de Iktan (41)', 'Prisionera serpiente del festival de Iktan (capítulo 41)'], [11, 12, 16, 19, 23],
     'Mujer con apariencia ilusoria de nativa que intenta inducir a Winscore a retirar al Anciano y muere durante el interrogatorio.',
     'Identidad descriptiva sin nombre ni rango. Walulu la vincula al grupo del veneno de Eromov; la causa de su muerte y la presencia que anuncia siguen abiertas.'),
    ('Sacerdotes serpiente de la roca norte', 'personaje', ['Sacerdotes serpiente de la roca norte (capítulo 41)'], [23, 28, 29, 30, 33, 34],
     'Dos adversarios localizados fuera de Iktan bajo apariencia de mujeres nativas, preparando viales junto a una roca.',
     'Ficha colectiva descriptiva. Sus capacidades se registran por intervención; no se atribuye a ambos todo efecto individual ni se identifica por nombre al superviviente.'),
    ('Abominación de la roca norte', 'personaje', ['Abominaciones serpiente del festival (capítulo 41)', 'Abominación de la roca norte'], [23, 38, 39, 46],
     'Gran criatura serpentina que sale de la vegetación, apresa a Naór con la cola y es derrotada en el combate del capítulo 41.',
     'Solo una aparición confirmada. La mención previa de dos grandes abominaciones permanece como declaración no verificada; no se fija subespecie de bestiario.'),
    ('Conejo cornudo del bosque de Iktan', 'personaje', ['Conejo cornudo del bosque de Iktan (capítulo 41)'], [27],
     'Animal consultado por Blink que señala la dirección de las mujeres junto a la roca al norte de Iktan.',
     'Nombre editorial descriptivo, sin identificar especie fantástica por parecido. Su relato de la gran serpiente conserva atribución y no confirma identidad con el dragón.'),
    ('Roca de los sacerdotes al norte de Iktan', 'lugar', ['Roca de los sacerdotes al norte de Iktan (capítulo 41)'], [23, 27, 28, 29, 38],
     'Lugar exterior al poblado donde dos figuras con ilusiones preparan viales y el grupo libra el combate.',
     'Etiqueta descriptiva sin coordenadas precisas. Es distinta de la piedra sagrada del Anciano y del claro de los restos envenenados del capítulo 40.'),
    ('Viales verdes de la roca norte', 'objeto', ['Viales verdes de la roca norte (capítulo 41)'], [28, 29, 30, 51],
     'Recipientes de líquido verdoso preparados por los adversarios del norte de Iktan; Winscore recoge recipientes tras el combate.',
     'El grupo los trata como venenos, sin análisis de composición. No se fusionan con la botella de Leona ni con la tinta del familiar.'),
]
catalog = read_json(ROOT / 'config/entidades.json')
for name, kind, labels, numbers, description, note in new_entities:
    group = dict(nombre=name, tipo=kind, etiquetas=labels, referencias=refs(*numbers), descripcion=description, nota=note)
    existing = next((i for i, old in enumerate(catalog['grupos']) if old['nombre'] == name), None)
    if existing is None:
        catalog['grupos'].append(group)
    else:
        catalog['grupos'][existing] = group
write_json(ROOT / 'config/entidades.json', catalog)

updates = {
    'Tentacol': [
        stage('Un viajero de las aguas profundas', 'Llega a Iktan nadando con Chopito en un frasco. Se presenta como Tenta y declara proceder de bosques de algas próximos a Perlasal. Trata al pulpo como señor, sin que eso acredite divinidad. Descubre junto a él a Cipo debilitado y lo acerca al fuego hasta que recupera sus llamas. Naór desea visitar su lugar de origen, pero la conversación no proporciona respiración acuática para ella.', 6, 8, 10, 14, 22),
        stage('La infiltrada y el combate del norte', 'Participa en el interrogatorio y, siguiendo la propuesta de Chopito, sumerge la cabeza de la cautiva. Presencia su muerte y transmite las últimas palabras. Percibe a través del familiar los viales verdosos antes de la emboscada. Utiliza un tentáculo de frío, descargas y contrahechizo para apoyar al grupo. Al terminar escucha la voz del bosque, pero no siente la compulsión de sus compañeros; la causa no queda establecida. Regresa con ellos a Iktan.', 22, 23, 25, 29, 32, 33, 37, 40, 49, 51),
    ],
    'Chopito': [
        stage('El pulpo al que se pide consejo', 'Viaja en un recipiente de agua con Tentacol y se comunica telepáticamente; los demás no oyen por ello cada frase. Desea obtener súbditos y adoración. Señala la silueta de Cipo y propone ayudarlo. Encanta a la infiltrada para cambiar su actitud, pero el posterior daño rompe ese efecto. Sus palabras de autoridad no bastan para acreditar condición divina.', 6, 8, 10, 20, 22),
        stage('Reconocimiento, tinta y una pretensión de mando', 'Tentacol comparte sus sentidos para reconocer el líquido verde. El pulpo abre la emboscada cubriendo los ojos de las adversarias con tinta; después avanza con lentitud hacia un estanque y vuelve a la botella al terminar. Cuando la voz pide abandonar los cuerpos, la presenta como un súbdito necesitado de alimento. Esa explicación es suya y no demuestra subordinación del dragón.', 29, 30, 32, 48, 50),
    ],
    'Infiltrada serpiente del festival de Iktan': [
        stage('La falsa celebrante', 'Bajo apariencia de nativa intenta persuadir a Winscore para que retire al Anciano. El enano resiste, detecta una ilusión y descubre incoherencias; al golpearla provoca la intervención del guardia. Walulu revela su forma serpentina mediante raíces. La dirigente la atribuye al grupo que envenenó a Eromov, sin demostrar autoría personal de esta mujer.', 11, 12, 13, 15, 16, 19),
        stage('Un informe interrumpido por la muerte', 'Se niega a responder y Winscore la quema. Chopito la encanta y ella pide ayuda a Tentacol. Un dolor inexplicado persiste pese a curarle las quemaduras. Tras la inmersión forzada que rompe el encantamiento anuncia a «ella», sitúa a dos sacerdotes al norte e intenta mencionar dos grandes abominaciones. Vomita serpientes y cae muerta; los reptiles se dispersan. No se identifica el agente del fenómeno ni a la presencia anunciada.', 17, 18, 20, 21, 22, 23),
    ],
    'Sacerdotes serpiente de la roca norte': [
        stage('La operación junto a la piedra', 'La cautiva informa de dos sacerdotes al norte. El grupo encuentra allí dos mujeres con la misma magia ilusoria, ocupadas en llenar viales de líquido verde y vigilar el entorno. Chopito les arroja tinta y comienza una emboscada. Los golpes deshacen una ilusión y dejan ver la forma serpentina; sus intervenciones incluyen sugestión, resistencia mágica y una protección que Tentacol contrarresta.', 23, 28, 29, 30, 31, 33, 34),
        stage('Derrota local y un cautivo incierto', 'El combate continúa cuando aparece una gran abominación. Los aventureros se protegen y terminan venciendo a la criatura. Mantienen con vida a un adversario, lo registran y atan para interrogarlo, pero la voz del bosque exige abandonar los cuerpos y no se muestra su desenlace. No se identifica por nombre o rango al superviviente ni se establece la jerarquía de toda la operación.', 38, 39, 42, 46, 47, 49, 51),
    ],
    'Abominación de la roca norte': [stage('El refuerzo que atrapa a Naór', 'Una gran criatura sale de la vegetación durante el combate. Enrosca la cola alrededor de Naór y la hiere con cimitarra y mordisco venenoso. Blink libera y agranda a la leonina. El grupo sostiene la lucha y el director confirma la derrota de la abominación. Solo una aparición de ese tipo queda descrita; el anuncio previo de dos no acredita una segunda.', 23, 38, 39, 40, 43, 46)],
    'Conejo cornudo del bosque de Iktan': [stage('Una dirección ofrecida a Blink', 'Blink habla con el animal durante la búsqueda al norte. Este afirma haber visto una gran serpiente que se proclama dueña del bosque y, al saber que buscan humanoides, recuerda unas mujeres junto a una piedra y señala dónde. La pista conduce a los adversarios. No recibe nombre propio ni se confirma por su testimonio la identidad de la gran serpiente.', 27, 28)],
    'Roca de los sacerdotes al norte de Iktan': [stage('El lugar de los viales y la emboscada', 'La confesión incompleta y la indicación del conejo llevan al grupo hasta una roca exterior al norte del poblado. Allí dos figuras con ilusiones llenan viales de líquido verdoso. Un estanque cercano ofrece agua a Chopito. Los aventureros preparan una emboscada y afrontan después una abominación. El lugar no se identifica con la piedra sagrada del festival ni con el claro contaminado de la expedición anterior.', 23, 27, 28, 29, 30, 32, 38, 46)],
    'Viales verdes de la roca norte': [stage('De la preparación a la recogida', 'Las dos figuras llenan pequeños viales de líquido verdoso a partir de recipientes mayores. Tentacol observa el color a través de Chopito y el grupo sospecha veneno. Una botella se rompe durante la emboscada. Tras el combate Winscore recoge recipientes que considera venenos; no se realiza un análisis ni se demuestra relación con la muestra del claro entregada antes a Walulu.', 28, 29, 30, 51)],
    'Naór': [
        stage('Leo y un emisario que no llega', 'Relata que consiguió con Walulu la entrada de Leo en la academia, después del rechazo por pequeño. El niño tiene dificultades con compañeros y ella insiste en que aprenda a defenderse. Espera a un emisario de Atlan anunciado para el festival y pregunta por él sin obtener noticias. Presenta una ofrenda en nombre de su reino y deja a Leo observando al Anciano como ejercicio de paciencia.', 2, 4, 9, 14),
        stage('De la infiltración a la retirada', 'Se reúne con Blink y Winscore, conoce a Tentacol y participa en la búsqueda al norte. Mantiene a una adversaria contra el suelo, pero una sugestión la obliga a soltarla; puede actuar de nuevo al terminar la petición. La abominación la apresa y envenena. Blink la libera y agranda; Naór sostiene el combate, recoge dos cabezas y carga a sus compañeros para salir del bosque tras la orden de la voz.', 5, 7, 10, 19, 24, 30, 34, 39, 40, 43, 48, 49, 51),
        stage('Ver al Anciano junto a Leo', 'Regresa a Iktan y por primera vez para ella ve a Tortas moverse y hablar. Ofrece las cabezas, se arrodilla y llora; el monje recuerda sus primeros bigotes y sus visitas infantiles. Trae a Leo desde la taberna para que asista al encuentro. El episodio no explica el retraso del emisario ni acredita una sucesión legal del niño.', 52, 53, 55),
    ],
    'Blink': [
        stage('Salir de Shiaru y reencontrarse en Iktan', 'Relata que consiguió despertar fuera de Shiaru tras varios intentos, aunque lleva días perdida buscando Cuicapalli. Esa salida no explica sus lagunas de memoria. Llega a Iktan por el aire, se reencuentra con Naór y reconoce a Winscore. Conoce a Tentacol y Chopito, vigila el festival y obtiene de un conejo cornudo una dirección útil para localizar a los enemigos.', 1, 5, 7, 10, 24, 27),
        stage('La defensa de sus compañeros y el olor del bosque', 'Participa en la emboscada con magia de control, aunque se corrige la inmovilización de ambas enemigas. Libera a Naór de la cola y aumenta su tamaño. Resiste flechas envenenadas, mantiene la concentración y busca cobertura mientras ataca la mente de los adversarios. Tras sentir la orden de dejar los cuerpos vuelve a Iktan. Tortas reconoce en ella olor de dragón verde; la idea de un rastro de aura sigue siendo una explicación propuesta por Blink.', 31, 36, 40, 41, 43, 45, 49, 51, 54),
    ],
    'Winscore': [
        stage('Descubrir a la falsa celebrante', 'Llega al festival desde Cuicapalli. Resiste una sugerencia de llevarse la tortuga, detecta la ilusión de la mujer y encuentra mentiras en su relato. La golpea y acaba ante Walulu con un guardia. La dirigente revela su forma serpentina. Winscore intenta obtener información mediante quemaduras, sin que eso identifique el plan completo.', 3, 7, 11, 12, 13, 15, 16, 17, 18),
        stage('Un cautivo que no llega a ser interrogado', 'Busca otros infiltrados, pide precauciones a un guardia sin obtener obediencia y propone una expedición discreta al norte. Mantiene ataques no letales y participa en la lucha con el bastón. Un adversario queda vivo, es registrado y atado; obtienen monedas y observan armas de buena factura. La orden del bosque interrumpe el proyecto de interrogatorio. Winscore recoge los recipientes y ve un dragón verde entre las ramas durante la retirada.', 24, 25, 26, 30, 33, 37, 42, 44, 46, 47, 49, 51),
        stage('Las notas ante Tortas', 'Se presenta al monje como explorador interesado en los tesoros de aquellas tierras. Escucha la tradición de Iktan y anota el nombre que Tortas intenta pronunciar. No desea combatir al dragón. El deletreo no ofrece una grafía segura y el anciano no sabe dónde se encuentra la guarida.', 53, 55),
    ],
    'Walulu': [stage('Las precauciones se ponen a prueba', 'Confirma que aumentó las precauciones tras el aviso de Leona, pero una infiltrada logra entrar. Mediante raíces revela sus rasgos serpentinos y la retiene. Atribuye su grupo al del veneno de Eromov. Presencia un interrogatorio que acaba con la muerte de la cautiva y pide a Tentacol ayudar a los compañeros. No se muestra una cura de Eromov ni un análisis de las nuevas muestras o entrega de las cabezas a la dirigente.', 15, 16, 17, 19, 21, 22, 23, 25, 48, 52)],
    'Tortas': [stage('Los visitantes del festival y el olor del dragón', 'Otro grupo se reúne ante el Anciano de barba mojada, inicialmente inmóvil. Una infiltrada pretende que lo retiren y durante la vigilancia se detecta brillo mágico en él, sin explicarlo. Al volver del combate, Naór lo ve moverse y hablar y él recuerda sus primeros bigotes. Reconoce olor de dragón verde en Blink por contacto con la nariz. Su lenta tentativa de recordar el nombre no fija grafía y el director aclara que desconoce la guarida. La experiencia de este grupo no reescribe la actividad del capítulo 40 ni resuelve su edad.', 3, 9, 11, 24, 52, 53, 54, 55)],
    'Cipo': [stage('Recuperar el fuego en Iktan', 'Chopito descubre una silueta en el agua y Tentacol encuentra a Cipo ennegrecido, humeante y debilitado. Lo acerca al fuego hasta que recupera el rojo y las llamas. Naór lo reconoce y más tarde el director lo señala entre los asistentes al festival. Queda documentado su paradero después de la patada, sin que se informe a Ilikar en escena o se revele la historia del fragmento de espada.', 8, 9, 14, 24)],
    'Leo': [stage('Academia, ofrendas y una lección de paciencia', 'Naór relata que lo admitieron en la academia de guerreros de Iktan gracias a su conversación con Walulu. En la taberna presenta moratones y le falta algún diente; su protectora le exige defenderse. Deposita una figura tallada y recibe el encargo de vigilar al Anciano. Durante la crisis vuelve a la taberna. Naór lo trae al final para ver a Tortas moverse y hablar, aunque el niño acaba adormeciéndose. No se fija un rango, avance de nivel ni reconocimiento sucesorio.', 2, 4, 9, 14, 24, 55)],
    'Leona': [stage('El aviso recordado en Iktan', 'Walulu confirma que su advertencia desde Cuicapalli motivó un aumento de las precauciones. La infiltración se descubre pese a esas medidas y los visitantes localizan después a los adversarios del norte. Leona es citada como mensajera, sin atribuirle las acciones de Naór ni un regreso representado a Cuicapalli.', 15, 19, 23, 38, 46)],
    'Eromov': [stage('La atribución de Walulu sigue sin una cura', 'Walulu identifica a la infiltrada como parte del grupo que lo envenenó y recuerda la información transmitida por Leona. Eso amplía la atribución de la dirigente, sin señalar al individuo que contaminó la comida. La sesión no muestra la llegada de la ayuda prometida, un antídoto administrado o la recuperación de Eromov.', 15, 19)],
    'Dragón verde del bosque de Iktan': [stage('La mirada entre las ramas y el olor reconocido', 'Tras la victoria sobre los adversarios, una voz exige dejar los cuerpos como alimento y provoca compulsión en todos los viajeros salvo Tentacol. Durante la retirada Winscore ve un dragón verde entre las ramas. Tortas reconoce después el mismo tipo de olor en Blink. La asociación contextual no establece verbalmente quién emitió la voz ni una alianza con los yuan-ti. El nombre sigue mal reconocido, la guarida desconocida y la identidad con Clodidrax sin demostrar; no se cumple la caza pactada por Eldrat e Ilikar.', 49, 50, 51, 54, 55)],
    'Iktan': [
        stage('El festival entre recuerdos y recién llegados', 'Naór relata la admisión de Leo en la academia y espera a un emisario de Atlan. Los vecinos reciben con flores y bebida a los viajeros, mientras la fiesta se concentra junto a las casas arruinadas y el Anciano. Tentacol rescata a Cipo y Naór recuerda sus visitas infantiles con Walulu. No se explica por esta celebración la destrucción de las casas ni se fija una fecha de fundación.', 2, 3, 6, 7, 8, 9, 53),
        stage('Una infiltración y el combate exterior', 'Walulu confirma precauciones y deshace el disfraz de una infiltrada, que muere después de revelar la posición de otros adversarios. Los visitantes vigilan el festival, reúnen a la población y buscan al norte. Vencen en el combate junto a una roca y regresan tras la orden de una voz del bosque. Tortas se mueve y habla al terminar la fiesta. La amenaza inmediata se combate, sin acreditar la eliminación de toda la red o de la presencia dracónica.', 15, 16, 23, 24, 25, 26, 28, 38, 46, 49, 51, 52, 55),
    ],
    'Perlasal': [stage('Una procedencia cercana y una visita deseada', 'Tentacol declara proceder de aguas profundas y bosques de algas próximos a Perlasal. Naór conoce el nombre y desea visitar esas aguas, pero sus intentos anteriores acabaron cerca del ahogamiento. La consulta a Chopito no proporciona un medio de respiración ni inicia un viaje; tampoco resuelve la crisis de los profundos documentada por Maris.', 10)],
    'Atlan': [stage('Una ofrenda y un emisario pendiente', 'Naór lleva días esperando a un emisario de su tierra que debía llegar durante el festival de Iktan. Pide noticias y presenta una ofrenda en nombre del reino. La ausencia no se explica: no se identifica al mensajero ni se acredita captura, muerte o un cambio político en Atlan.', 2, 4, 9)],
    'Piedra sagrada de Iktan': [stage('La observación de Leo durante la fiesta', 'El Anciano aparece inmóvil sobre el soporte mientras recibe ofrendas. Naór lleva las figuras talladas y encarga a Leo esperar un movimiento como ejercicio de paciencia. Más tarde el grupo observa a Tortas hablar. El brillo detectado durante la vigilancia corresponde al Anciano y no demuestra magia propia de esta piedra, que sigue separada de la roca exterior de los sacerdotes.', 3, 9, 24, 52, 55)],
    'Yuan-ti': [
        stage('El disfraz del festival', 'Una infiltrada intenta inducir a Winscore a retirar al Anciano. La ilusión queda detectada y Walulu revela su aspecto serpentino con raíces. La dirigente vincula su grupo al veneno de Eromov. Bajo interrogatorio, la cautiva anuncia a «ella», señala sacerdotes al norte y muere expulsando serpientes. No se establece quién provoca esa muerte o dirige toda la operación.', 11, 12, 16, 19, 21, 22, 23),
        stage('Viales, armas y un superviviente', 'Los viajeros encuentran a dos figuras ilusorias preparando líquido verde y las atacan por sorpresa. Aparece una abominación, que termina derrotada. Un adversario queda vivo y atado para interrogarlo, pero la orden del bosque impide completar esa investigación. La calidad de las armas y los recipientes ofrecen pistas sin identificar proveedor, jerarquía o alianza con el dragón.', 28, 29, 30, 38, 39, 42, 46, 47, 49, 51),
    ],
}

history_files = [
    ('historias_personajes.json', 'personajes'),
    ('historias_personajes_complementarias.json', 'personajes'),
    ('historias_lugares.json', 'entidades'),
    ('historias_facciones.json', 'entidades'),
    ('historias_objetos.json', 'entidades'),
]
documents = {filename: read_json(ROOT / 'config' / filename) for filename, _ in history_files}
kind_by_name = {group['nombre']: group.get('tipo') for group in catalog['grupos']}
for name, stages in updates.items():
    destination = next(((filename, collection) for filename, collection in history_files
                        if name in documents[filename][collection]), None)
    if destination is None:
        kind = kind_by_name[name]
        destination = (('historias_personajes_complementarias.json', 'personajes') if kind == 'personaje'
                       else (f'historias_{dict(lugar="lugares", faccion="facciones", objeto="objetos")[kind]}.json', 'entidades'))
    filename, collection = destination
    previous = documents[filename][collection].get(name, [])
    # Una segunda ejecución sustituye solo las etapas de este capítulo.
    previous = [item for item in previous if not all(ref.startswith('41-') for ref in item['referencias'])]
    documents[filename][collection][name] = previous + stages
for filename, _ in history_files:
    documents[filename]['revisado_hasta'] = 41
    write_json(ROOT / 'config' / filename, documents[filename])

# La ficha con anclas debe existir antes de validar seguimientos hasta el 41.
subprocess.run([sys.executable, str(ROOT / 'scripts/redactar.py'), 'borradores/41.json'], check=True)

tracking_updates = {
    'P17-004': ('pendiente', 'Walulu atribuye a la infiltrada del festival el mismo grupo que envenenó a Eromov. El grupo localiza después a sacerdotes al norte de Iktan, pero esa declaración no identifica a los individuos avistados por la patrulla de Ras Racor ni prueba una relación directa con aquel informe.', [19, 23, 28], 'Establecer la relación directa entre los avistamientos de la patrulla y la crisis de Cuicapalli.'),
    'P21-004': ('parcial', 'Leo sigue al cuidado de Naór. Ella relata que consiguió su admisión en la academia de Iktan con ayuda de Walulu y continúa su entrenamiento; lo trae a ver a Tortas al final del festival. Esto amplía su vida posterior, sin mostrar aceptación formal de custodia por Eromov ni una evaluación de sus secuelas.', ['31-028', 2, 4, 9, 24, 55], 'Confirmar la decisión de Eromov sobre la custodia y las consecuencias duraderas para Leo.'),
    'P30-002': ('pendiente', 'Walulu afirma que la infiltrada del festival pertenece al grupo que envenenó a Eromov. Es una atribución de la chamana, sin confesión del individuo que contaminó la comida o identificación de las dos visitantes. La muerte de la cautiva impide completar su interrogatorio.', ['30-005', '30-006', '30-009', 19, 23], 'Identificar a quien añadió el veneno y a las dos visitantes anteriores.'),
    'P30-005': ('pendiente', 'La previsión de ataque a Iktan se concreta en una infiltrada, dos sacerdotes localizados junto a una roca y una abominación observada. La cautiva anuncia a «ella» y muere sin nombrarla. No se reconstruye la jerarquía, la relación exacta con Hoja Caída ni una alianza con el dragón que aparece después.', ['39-010', '40-002', '40-006', 16, 23, 28, 38, 46, 51], 'La organización de los grupos, sus aliados y las relaciones entre las distintas operaciones.'),
    'P31-001': ('pendiente', 'Tortas reconoce olor de dragón verde en Blink e intenta pronunciar y deletrear el nombre. Los reconocimientos Colgen y Los del Grax for Snake y las letras sueltas siguen sin dar grafía segura. No se prueba quién destruyó las casas antiguas ni se identifica expresamente a esta criatura con Clodidrax.', ['40-030', '40-032', 54, 55], 'La grafía exacta y la relación demostrada del dragón con las ruinas.'),
    'P31-002': ('pendiente', 'Tras el combate del norte una voz exige dejar los cuerpos como alimento y provoca compulsión en el grupo, salvo Tentacol, que también la escucha. Winscore ve después un dragón verde y Tortas reconoce olor dracónico en Blink. La asociación contextual no identifica verbalmente al emisor ni explica todo el mecanismo, su alcance o cómo romperlo de forma permanente.', ['40-024', '40-032', 49, 50, 51, 54], 'El mecanismo completo de la influencia y una neutralización permanente.'),
    'P31-005': ('pendiente', 'Iktan admite a nuevos visitantes durante el festival y sufre una infiltración bajo ilusiones. No se atribuye esa entrada a una revelación de ruta de los viajeros anteriores, se ejecuta el castigo anunciado o se celebra el concilio. La crisis local no resuelve la asistencia efectiva a Tutucan.', ['39-017', '39-019', '39-020', 3, 6, 16, 23], 'Las consecuencias concretas de revelar la ruta y la asistencia efectiva al concilio.'),
    'P34-001': ('pendiente', 'Blink relata que por fin salió de Shiaru y despertó fuera del poblado, aunque pasa días perdida buscando Cuicapalli y acaba en Iktan. Esto documenta una salida posterior, pero no explica las lagunas de memoria ni el mecanismo de sus regresos anteriores.', [1, 5], 'La causa de las lagunas de memoria y de sus regresos anteriores a Shiaru.'),
    'P36-003': ('parcial', 'El reencuentro con Eleanor ya documentado resuelve su paradero posterior. En el capítulo 41 Blink relata una salida conseguida de Shiaru y llega a Iktan tras perderse buscando Cuicapalli. No explica el regreso ni la amnesia que motivaron la pregunta.', ['37-001', '38-001', 1, 5], 'La causa del regreso de Blink y de sus lagunas de memoria.'),
    'P39-004': ('parcial', 'No se representa el té de Walulu con Citlali sobre sus marcas. Los problemas de Iktan sí se amplían: se descubre una infiltrada y otros adversarios preparando viales al norte; una voz reclama los cuerpos y Winscore ve un dragón verde. No se resuelve el origen de todas las amenazas ni la conversación de los tatuajes.', ['40-013', '40-016', '40-035', 15, 16, 23, 28, 49, 51], 'El resultado de la conversación con Citlali y las causas completas de las amenazas.'),
    'P39-005': ('pendiente', 'Winscore observa un dragón verde durante la retirada del combate del capítulo 41. No hay identificación retrospectiva de esa criatura con la presencia que observaba la ciudad en el 39. Tampoco se informa del destino de los yuan-ti sepultados en el derrumbe de aquella cueva.', [51], 'La identidad de la presencia del capítulo 39 y el destino de los yuan-ti tras el derrumbe.'),
    'P40-001': ('pendiente', 'La muestra del claro no recibe análisis nuevo. Los adversarios del norte preparan otros recipientes verdes que el grupo considera venenos y Winscore recoge tras el combate. No se identifica al creador de los restos animados ni se demuestra una equivalencia o causalidad entre ambas fuentes.', ['40-016', '40-017', '40-026', '40-035', 29, 51], 'El origen de la animación de los restos y la función causal del veneno.'),
    'P40-003': ('pendiente', 'Winscore ve el dragón verde y Tortas reconoce su olor en Blink. El anciano intenta pronunciar su nombre, sin grafía segura en la transcripción, y el director aclara que no conoce la guarida. No se inspecciona la cueva de la emboscada ni se demuestra identidad con Clodidrax.', ['40-030', '40-033', 51, 54, 55], 'La grafía, la ubicación de la guarida y la relación de identidad con Clodidrax.'),
    'P40-005': ('pendiente', 'Tortas recuerda los primeros bigotes de Naór y reconoce un olor que lleva muchos años percibiendo. La tradición de la ciudad y las bromas sobre su antigüedad no concilian la edad declarada de 77 años con los siglos que le atribuye Walulu.', ['40-011', '40-031', '40-035', 52, 53, 54], 'La edad de Tortas y la historia de su inmovilidad.'),
    'P40-006': ('parcial', 'Walulu confirma que aumentó las precauciones tras el aviso de Leona. La amenaza se concreta en una infiltrada y adversarios localizados al norte, con un combate que termina en victoria local. No se muestra la llegada de hombres, recetas o protecciones a Cuicapalli ni una cura de Eromov; tampoco la eliminación de toda la red.', [15, 16, 19, 23, 28, 38, 46], 'El envío y resultado de la ayuda a Eromov y el alcance restante de la operación contra Iktan.'),
    'P40-007': ('parcial', 'Chopito descubre a Cipo saliendo del agua y Tentacol lo acerca al fuego. Recupera el rojo y las llamas y el director lo señala después en el festival de Iktan. Queda resuelto el paradero posterior, sin que Ilikar sea informado en escena; la procedencia, dueño e historia del fragmento de espada continúan desconocidos.', [8, 9, 14, 24], 'El origen y la historia del fragmento de espada; no se documenta que Ilikar conozca el rescate.'),
}

all_old_ids = []
for path in sorted((ROOT / 'config').glob('seguimiento_preguntas_*.json')):
    if path.name == 'seguimiento_preguntas_41.json':
        continue
    document = read_json(path)
    document['revisado_hasta'] = 41
    for entry in document['preguntas']:
        all_old_ids.append(entry['id'])
        if entry['id'] in tracking_updates:
            state, answer, numbers, pending = tracking_updates[entry['id']]
            entry.update(estado=state, respuesta=answer, referencias=refs(*numbers), pendiente=pending)
        # Cotejo editorial de las preguntas leídas; no se deduce por palabras clave.
        entry['revisado_hasta'] = 41
    write_json(path, document)
assert len(all_old_ids) == 235

new_pending = [
    'La identidad, el paradero y el motivo del retraso del emisario.',
    'La identidad y propósito de la presencia anunciada como «ella».',
    'La causa del dolor, la salida de serpientes y la muerte.',
    'La finalidad de retirar al Anciano, los integrantes restantes y el mando de la operación.',
    'El destino del cautivo vivo y la información que pudiera proporcionar.',
    'La composición de los líquidos y su relación con otras muestras.',
    'El fabricante, proveedor y organización que equipa a los adversarios.',
    'La causa de la excepción de Tentacol a la compulsión.',
    'La grafía, la guarida y la relación de identidad con Clodidrax.',
    'La visita y el método para que Naór respire bajo el agua.',
    'El origen y la función del brillo mágico detectado en el Anciano.',
]
new_answers = [
    ('Naór lleva días esperándolo y pregunta por noticias en la taberna. No aparece durante la sesión ni recibe un nombre o una explicación de su ausencia.', [2, 4]),
    ('La cautiva anuncia que «ella» viene e impedirá descubrir lo que buscan; muere antes de dar un nombre. El dragón observado después no identifica por sí solo esa alusión.', [18, 23, 51]),
    ('El dolor persiste al curar las quemaduras y no se observa un efecto que lo explique. Tras el interrogatorio con agua expulsa serpientes y cae muerta. Ni Chopito ni otra entidad quedan acreditados como causa.', [21, 22, 23]),
    ('La sugerencia pide llevarse la tortuga. El informe conduce a dos sacerdotes y se observa una abominación, derrotada en escena. No se verifica la segunda anunciada ni se reconstruye la finalidad de toda la operación.', [11, 23, 28, 38, 46]),
    ('El superviviente queda registrado y atado para un interrogatorio. La voz exige dejar los cuerpos y el director incluye al vivo en esa expresión; no se narra su traslado, interrogatorio o muerte.', [42, 47, 49, 51]),
    ('Tentacol observa líquido verde a través del familiar; el grupo sospecha veneno y Winscore recoge recipientes. No se muestra análisis ni equivalencia con el envenenamiento de Eromov o la botella de Leona.', [19, 29, 30, 51]),
    ('El director confirma la buena factura de las armas. Los personajes infieren una organización mayor, sin hallar un nombre de taller, proveedor o dirigente.', [47]),
    ('El director exceptúa a Tentacol del sentimiento de obedecer, aunque sí oye la voz. La explicación tentativa sobre Chopito no fija la causa ni una inmunidad general.', [49, 50]),
    ('Winscore observa el dragón y Tortas reconoce su olor. El deletreo incompleto no permite fijar el nombre; el director niega que el monje conozca la guarida. No hay identificación expresa con Clodidrax.', [51, 54, 55]),
    ('Naór expresa el deseo de conocer Perlasal y Tentacol consulta a Chopito. No obtiene un medio de respiración acuática ni comienza la visita.', [10]),
    ('Detectar magia revela brillo en el Anciano durante la vigilancia. No se identifica su origen o función y el pasaje no atribuye esa magia al soporte pétreo.', [24]),
]
entries = []
for i, (question, pending, (answer, numbers)) in enumerate(zip(questions, new_pending, new_answers), 1):
    entries.append(dict(id=f'P41-{i:03d}', capitulo=41, indice=i, pregunta=question,
                        estado='pendiente', respuesta=answer, referencias=refs(*numbers),
                        pendiente=pending, revisado_hasta=41))
write_json(ROOT / 'config/seguimiento_preguntas_41.json', dict(version=1, revisado_hasta=41, preguntas=entries))
write_json(ROOT / 'borradores/41/cotejo_historico.json', dict(
    capitulo=41, preguntas_anteriores=235, preguntas_leidas=all_old_ids,
    actualizaciones_con_texto=sorted(tracking_updates),
    sin_nueva_respuesta=[qid for qid in all_old_ids if qid not in tracking_updates],
    criterio='Cotejo editorial de las preguntas históricas con las lecturas integrales de los tres bloques. Las preguntas sin nueva respuesta conservan su estado y explicación; no se cierran por coincidencias léxicas.',
    cautelas=['Una sola abominación observada.', 'La voz y el dragón se asocian por contexto.',
              'Cipo localizado; fragmento de espada sin origen.', 'Ataque local acreditado; ayuda a Eromov sin desenlace.']))

source_meta = read_json(ROOT / 'config/fuente_xoltacan_41.json')
source_meta['lectura'] = 'Tres bloques completos sin solapamiento; 55 registros, diez etapas de relato y cotejo editorial de las 235 preguntas anteriores. Audio no cotejado.'
source_meta['reparto'] = 'borradores/41/reparto.json'
write_json(ROOT / 'config/fuente_xoltacan_41.json', source_meta)
print('Capítulo 41 integrado: 55 registros, diez etapas, ocho identidades nuevas y once preguntas nuevas.')
