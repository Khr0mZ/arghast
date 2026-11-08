"""Entrega editorial tras leer íntegros los 1437 segmentos del bloque 1."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import validate_fact

rows = json.loads((ROOT / 'campanas/xoltacan/revision/borradores/45/bloque_1_segmentos.json').read_text(encoding='utf-8'))
source = ROOT / 'campanas/xoltacan/fuentes/45 - 30qLJWABsPE.es-orig.vtt'
facts = []

def fact(a, b, anchor, title, statement, names, kind='hecho_confirmado', limit=''):
    cue = rows[anchor]
    item = dict(id=f'45-{len(facts)+1:03d}', titulo=title, tipo=kind,
                afirmacion=statement, inicio=rows[a]['inicio'], fin=rows[b]['fin'],
                cita=cue['texto_original'],
                evidencia_cue=dict(inicio=cue['inicio'], fin=cue['fin'], texto=cue['texto_original']),
                entidades=names, ambito='preparación del viaje a Perlasal y búsqueda del escuadrón',
                conocedores=[], conocimiento_personaje='desconocido',
                nota_conocimiento='Acceso de Madame Oghma sin establecer en este pasaje.',
                confianza='lectura de subtítulos; audio no cotejado', limitacion=limit)
    validate_fact(item, source)
    facts.append(item)

fact(0,72,21,'Los viajeros preparan la salida de Iktan hacia Perlasal',
     'Tentacol relata que ha buscado seguidores cerca de Iktan y hablado con Naór y Leo sobre ir a Perlasal. Naór cuenta sus intentos de superar el miedo al agua con Coyote, Tortas y Triel. Coyote quiere regresar a la ciudad submarina y alejarse de Iktan. Tortas recuerda sus esfuerzos por resolver cómo viajar bajo el agua y los brebajes de Coyote que le recordaron a Ilikar.',
     ['Tentacol','Chopito','Naór','Leo','Coyote','Tortas','Triel','Ilikar','Iktan','Perlasal'], 'declaracion_personaje',
     'Los recuerdos aluden a lo sucedido entre sesiones, sin volver a representar cada práctica. Llamar antiguo alumno a Ilikar no demuestra que Tortas conozca un desenlace de la batalla naval o que Ilikar haya muerto.')
fact(73,99,80,'Iktan está junto al lago llamado Tachan',
     'El director sitúa la ciudad oculta de Iktan junto a un lago al que llama Tachan. La narración se acerca a la zona comercial, con el templo y la herrería, donde un portazo anuncia la discusión a la salida del colegio.',
     ['Iktan','Lago Tachan','Colegio de Iktan'], 'explicacion_director',
     'Tachan es una grafía provisional del nombre oído al recordar el director cómo lo llamó. No se identifica por ese nombre cada lago anterior de la campaña.')
fact(93,141,118,'La directora reprocha a Naór la conducta escolar de Leo',
     'Una directora de aspecto felino y con gafas pide a Naór que no grite ante los niños. Naór defiende que Leo aprende a defenderse, pero la directora le atribuye peleas y una conducta inadecuada con el hámster del colegio. Primero dice que todos lo vieron y luego aclara que ella no fue testigo: se lo contaron los niños. Excluye a Leo de las clases de ese día.',
     ['Naór','Leo','Directora del colegio de Iktan','Colegio de Iktan'], 'declaracion_personaje',
     'El incidente del hámster no se representa directamente ni se convierte en observación propia de la directora. El colegio no se identifica automáticamente con el edificio de la academia de guerreros del capítulo 41.')
fact(142,182,158,'Dos monedas consiguen que Leo permanezca dos horas más',
     'Naór dice que no puede quedarse con Leo y deja dos monedas de oro para negociar. La directora protesta, acepta el dinero y permite dos horas más. Naór promete recoger al niño a las cinco y media y autoriza también a una chica de trenza y pelo azul para hacerlo. La directora recuerda una visita anterior de esa muchacha con otros niños, sin nombrarla aquí.',
     ['Naór','Leo','Directora del colegio de Iktan','Colegio de Iktan'],
     limit='La chica autorizada queda sin identificar en este pasaje; no se equipara por apariencia con Triel, que participa después en el viaje. La permanencia negociada no equivale a una expulsión definitiva ni a una recogida ya realizada.')
fact(183,234,202,'Chopito propone reclutar a Tortas',
     'Mientras Coyote observa parte de la discusión, Tentacol llega con Chopito. El pulpo insiste en marcharse, se atribuye la iniciativa de reclutar por medio del niño y considera a la tortuga un posible súbdito poderoso. Tentacol se acerca a Tortas, que intenta meditar sobre la piedra pese al dolor de cabeza, y siguiendo el consejo del pulpo le echa agua por encima.',
     ['Chopito','Tentacol','Tortas','Naór','Leo','Piedra sagrada de Iktan'],
     limit='Llamarlo semidiosa o súbdito expresa las pretensiones de Chopito. No establece divinidad, subordinación real o una nueva jerarquía de la comunidad.')
fact(235,299,257,'Tortas acepta acompañarlos sin rendir culto a Chopito',
     'Tortas protesta por el agua y escucha la invitación a Perlasal. La mesa aclara que los demás normalmente oyen burbujas cuando habla Chopito; el monje atribuye su respuesta a haber interpretado bien sus gestos. Tentacol transmite la propuesta de unirse y hacerse más fuertes. Tortas decide ir porque recuerda que Bigotitos tiene asuntos allí, sin comprometerse a adorar al pulpo, y comienza a bajar lentamente de la piedra.',
     ['Tortas','Tentacol','Chopito','Naór','Perlasal','Piedra sagrada de Iktan'],
     limit='El intercambio no concede a todos comunicación telepática o habla con animales. La aceptación del viaje no confirma el culto solicitado por Chopito.')
fact(300,328,305,'Coyote evita la discusión y vuelve a ser expulsado de la taberna',
     'Coyote recuerda que insistió en cortejar a la tabernera y acabó expulsado, aunque salió con una cerveza robada. Al ver a Naór intenta pasar inadvertido y volver al local para evitar la discusión del colegio.',
     ['Coyote','Naór','Angelique','El Huevo Emplumado'],
     limit='La tabernera llamada Angelita se vincula provisionalmente a Angelique por la continuidad de esas escenas de Iktan, sin fusionarla con Angélica Thunder. El segundo lanzamiento se representa en 45-011; esta entrada conserva el contexto del intento de esconderse.')
fact(330,385,367,'Naór quiere viajar a Perlasal por la convocatoria de Tutucan',
     'Naór va al templo y conversa con Walulu sobre Leo y su próxima visita a Perlasal. Vincula el viaje con la reunión de Tutucan y explica que ha practicado para soportar el agua. Espera contar con Coyote, que conoce el camino, y con Tentacol, que parece proceder de esas aguas.',
     ['Naór','Walulu','Leo','Coyote','Tentacol','Perlasal','Tutucan','Iktan'], 'declaracion_personaje',
     'El proyecto diplomático no representa una audiencia con el liderazgo de Perlasal, una invitación ya entregada o la celebración del concilio.')
fact(373,413,397,'Walulu ofrece una burbuja de una hora, que no llega a lanzar aquí',
     'Walulu ofrece un conjuro para aguantar aproximadamente una hora bajo el agua, pero duda de que baste para alcanzar Perlasal. Advierte del riesgo si la burbuja se rompe o pasa demasiado tiempo. Naór decide consultar a Coyote y Tortas; la chamana queda disponible si necesitan el hechizo.',
     ['Walulu','Naór','Coyote','Tortas','Perlasal'], 'declaracion_personaje',
     'La propuesta no se convierte en una burbuja aplicada. El grupo obtiene después otro medio de respiración, sin que esta conversación fije cuánto dura ese otro efecto.')
fact(414,430,419,'Naór afirma que ella es la familia de Leo',
     'Naór pide a Walulu que vigile a Leo en el colegio. Cuando la chamana sugiere buscarle una familia de verdad, la princesa vuelve y proclama que ella es su familia y que lo convertirá en un guerrero. Walulu lo acepta en la conversación. A solas, expresa su preocupación recordando que los bichos de una familia que Naór hizo de pequeña murieron.',
     ['Naór','Leo','Walulu','Colegio de Iktan'],
     limit='El recuerdo y la preocupación de Walulu no demuestran que Leo vaya a sufrir el mismo destino ni una evaluación de sus secuelas. La escena no formaliza una adopción ante Eromov o Atlan.')
fact(431,610,575,'El grupo se reúne y Tortas reacciona al año y la hora',
     'Naór sigue el rastro de Coyote y lo recoge al salir otra vez de la taberna, donde han vuelto a echarlo con una botella. Ambos se reúnen con Tentacol, Chopito y Tortas. Hablan de llegar a Perlasal y volver a tiempo por Leo, y Coyote promete un atajo aunque no explica aún la respiración. Tortas pregunta el año y la hora; el director responde 1496 y las diez y cuarenta y tres de la mañana. El monje se ilumina brevemente, se mueve el aire y suena un destello, sin explicar el cambio.',
     ['Naór','Coyote','Tentacol','Chopito','Tortas','Angelique','Perlasal','Leo'],
     limit='La fecha y la hora pertenecen al calendario ficticio. La luz no demuestra un cumpleaños, una edad exacta, ascenso de nivel o conciliación entre los 77 años declarados y los siglos atribuidos a Tortas.')
fact(611,666,631,'Coyote activa la perla dentro del agua y contacta con Maris',
     'Coyote se acerca al agua y sumerge la perla. En su interior aparece un remolino como un mar y después el rostro de Maris. Le pide ayuda para que él y sus compañeros puedan llegar a Perlasal y solicita que vengan sirénidos capaces de facilitarles la respiración.',
     ['Coyote','Perla de comunicación de Coyote','Maris','Perlasal','Lago Tachan'],
     limit='La perla sirve para esta comunicación, sin abrir un portal de transporte. La ruta posterior se recorre nadando con una guía.')
fact(667,689,672,'Maris informa de nuevos ataques, secuestros y el cierre de Perlasal',
     'Maris cuenta que han cerrado Perlasal hace poco porque los Profundos volvieron a atacar y se llevaron a algunos de sus habitantes. Cree que los cautivos están en alguna cueva. Al saber que el grupo se encuentra en Iktan, promete buscar a una sirénida que pueda ayudarlo y le pide a Coyote que tenga cuidado.',
     ['Maris','Coyote','Profundos','Perlasal','Iktan'], 'declaracion_personaje',
     'Las cuevas son una hipótesis de Maris, no una localización ya observada por ella en la llamada. Este relato no identifica al kraken, al dios de los atacantes o a los autores individuales de los secuestros.')
fact(690,779,712,'Triel sale del lago y sus prácticas no le dan respiración acuática',
     'Una figura sale del agua: es Triel, que llevaba tiempo practicando y trae un pez. Naór intenta cogerlo para comerlo. La elfa cree estar cerca de aprender a respirar bajo el agua y explica su método de contener el aire sin soltar burbujas; Tortas lo prueba. Coyote insinúa que permanecer en el agua la transformará y hará olvidar la respiración en tierra, y ella decide salir.',
     ['Triel','Naór','Tortas','Coyote','Lago Tachan'],
     limit='Las manos arrugadas de Triel no prueban una transformación acuática. El consejo de Coyote es una broma o engaño, no una regla confirmada del mundo; las prácticas de apnea no conceden aquí branquias.')
fact(780,816,800,'Llega una guía sirénida enviada por la princesa Maris',
     'Otra figura asciende del agua y se presenta ante Coyote como enviada por la princesa Maris. Él le pide ayuda para respirar. La mujer acepta, pero solicita a cambio que la ayuden a regresar a Perlasal.',
     ['Guía sirénida enviada por Maris','Coyote','Maris','Perlasal'],
     limit='La guía no da su nombre. Llamar princesa a Maris es el tratamiento de esta enviada, sin equipararla por ello con Ivet ni reconstruir una jerarquía política completa.')
fact(817,866,823,'Los besos de la sirénida permiten respirar a Coyote, Naór y Tortas',
     'La guía besa a Coyote y aparecen pequeñas escamas que le permiten respirar bajo el agua. Naór protesta y pregunta por otro método, pero acaba aceptando; siente malestar momentáneo y brotan escamas en su cuello. Tortas recibe también el beso y queda sorprendido. Tentacol dice no necesitarlo. Coyote explica que cambiar de apariencia no le proporciona siempre todas las capacidades del ser imitado.',
     ['Guía sirénida enviada por Maris','Coyote','Naór','Tortas','Tentacol'],
     limit='El efecto permite la respiración representada, sin duración exacta fijada aquí ni una transformación de especie permanente. La explicación sobre sus cambios de forma es de Coyote y no una lista general de todas sus capacidades.')
fact(867,889,881,'Naór hace que Triel reciba el mismo medio de respiración',
     'Naór agarra del tobillo a la sirénida y la acerca a Triel. La guía besa a la elfa, que responde, y también le aparecen escamas. Triel queda incorporada al grupo que se dispone a descender.',
     ['Naór','Triel','Guía sirénida enviada por Maris'],
     limit='Triel participa después en el viaje submarino. No se presume por semejanza que sea la chica de pelo azul autorizada antes a recoger a Leo.')
fact(890,948,908,'La guía pide buscar su escuadrón y Naór se aferra a Tortas',
     'Antes de ir a Perlasal, la guía pide encontrar a sus compañeros, amenazados por la vigilancia de los Profundos. Naór teme sumergirse pese a poder respirar y se aferra al caparazón de Tortas. Tentacol traduce las palabras tranquilizadoras de Chopito. El monje reacciona a una mención de enemigos y el grupo se pone en marcha.',
     ['Guía sirénida enviada por Maris','Profundos','Naór','Tortas','Tentacol','Chopito','Coyote','Triel','Perlasal'],
     limit='Leo permanece en el colegio; una broma de la mesa sobre que se ahoga no lo traslada a la expedición. El temor de Naór no implica pérdida del efecto respiratorio.')
fact(949,1039,958,'El lago conduce por una gruta de corrientes hasta el mar',
     'El grupo sigue a la sirénida por un lago extremadamente profundo. Antes de llegar al fondo entran por una gruta lateral y las fuertes corrientes los impulsan durante un trayecto largo hasta un espacio abierto que parece el mar, con ruinas antiguas bajo el agua. La guía advierte que es una zona controlada por los Profundos. Naór recuerda al fin usar su nueva respiración y Chopito trata de abrirle los ojos; Triel disfruta nadando alrededor.',
     ['Lago Tachan','Iktan','Guía sirénida enviada por Maris','Naór','Tortas','Tentacol','Chopito','Triel','Coyote','Profundos','Ruinas del ataque al escuadrón sirénido'],
     limit='Se narra una conexión física por túneles y corrientes, sin duración precisa o teletransporte. La salida no equivale a haber entrado en Perlasal y las ruinas aún no son el escondite del altar.')
fact(1040,1074,1060,'La guía admite que huyó mientras quedaban compañeros',
     'En unas ruinas, la guía señala dónde atacaron los Profundos y se presenta como la única superviviente. Cuando Tentacol transmite la objeción de Chopito sobre por qué buscan a alguien si todos murieron, ella reconoce que vio caer a dos compañeros y huyó por miedo aunque aún quedaban más. Coyote deja de sonreír y acepta buscarlos; Tortas le ofrece un gesto de apoyo.',
     ['Guía sirénida enviada por Maris','Tentacol','Chopito','Coyote','Tortas','Profundos','Ruinas del ataque al escuadrón sirénido'], 'declaracion_personaje',
     'Su primera afirmación no confirma la muerte de todo el escuadrón. Caer no fija por sí solo el destino final de esos dos; la identidad y el estado de cada desaparecido siguen sin comprobarse.')
fact(1075,1118,1087,'Tentacol encuentra coral roto y señales de armas cortantes',
     'Tentacol examina el fondo de las ruinas y encuentra corales rotos como por el paso de una criatura grande, además de zonas cortadas con algo afilado. Interpreta que hubo combate y avisa al grupo. Chopito se atribuye haberlo entendido y pide prepararse contra los responsables.',
     ['Tentacol','Chopito','Ruinas del ataque al escuadrón sirénido'],
     limit='Los indicios no identifican una especie, arma concreta o individuo responsable. No se equiparan automáticamente con las heridas de un cautivo todavía no encontrado.')
fact(1119,1230,1189,'Coyote reúne a todos para priorizar la búsqueda',
     'Mientras Triel confunde la búsqueda con encontrar Perlasal y Tortas lleva a Naór de un lado a otro, Coyote reúne a los compañeros. Explica que ayudar a la guía a encontrar a su escuadrón es la prioridad y una manera de ser bien recibidos en la ciudad. Deciden permanecer juntos para investigar.',
     ['Coyote','Naór','Tortas','Triel','Tentacol','Guía sirénida enviada por Maris','Perlasal'],
     limit='Ser bien recibidos es la expectativa de Coyote, no una autorización oficial de entrada. Los equívocos del grupo no representan una llegada o visita a Perlasal.')
fact(1231,1268,1264,'Naór detecta un rastro mágico hacia el norte',
     'Naór propone olfatear e identificar lo que no encaja y activa su percepción de la magia. En la zona que Tentacol había examinado, el director describe pequeños restos de magia asociados al uso o transporte de armas mágicas. El rastro forma líneas que se alejan hacia el norte.',
     ['Naór','Tentacol','Ruinas del ataque al escuadrón sirénido'],
     limit='La percepción mágica y la búsqueda mediante olfato se distinguen en la mesa. El rastro no se atribuye por nombre a Maris, a una cautiva o a un arma vista, ni prueba aún el destino de los secuestrados.')
fact(1269,1304,1296,'La guía da cuatro nombres de compañeros desaparecidos',
     'Triel dice haber encontrado gente con cola, aletas y una gran boca dentada; los otros sospechan tiburones y piden agarrarse a Tortas. Antes de salir, Tortas pregunta los nombres de los compañeros de la guía. Ella enumera Alfira, Zamuria, Jariora y María Antonieta.',
     ['Triel','Tortas','Guía sirénida enviada por Maris','Alfira','Zamuria','Jariora','María Antonieta'], 'declaracion_personaje',
     'Las grafías de los nombres son provisionales. La enumeración no identifica a una cautiva posterior con ninguna de esas cuatro personas ni confirma quién sigue vivo. Los peces descritos por Triel no son miembros del escuadrón.')
fact(1305,1344,1325,'Tortas amplifica los nombres mediante su proyección astral',
     'Tortas se ilumina de azul y manifiesta su proyección astral. Propone usar la voz espiritual como un megáfono de seiscientos pies para llamar a los compañeros de la sirénida. El director exige activar las dos capacidades indicadas y narra que el grito resuena por el mar. Los acompañantes quedan sorprendidos y le piden que avise antes de repetirlo.',
     ['Tortas','Guía sirénida enviada por Maris','Alfira','Zamuria','Jariora','María Antonieta','Naór'],
     limit='El grito no contiene una respuesta de los desaparecidos ni los localiza. El alcance es el acordado en esta escena y no demuestra detección automática como un sonar.')
fact(1345,1359,1351,'Se acercan cuatro tiburones y el grupo decide marcharse',
     'Triel vuelve a señalar las figuras y el director muestra cuatro tiburones acercándose. Los viajeros piden agarrarse al caparazón de Tortas y deciden alejarse por el rastro. Tentacol no sube porque puede moverse más deprisa por su cuenta.',
     ['Triel','Tortas','Naór','Coyote','Tentacol','Chopito','Guía sirénida enviada por Maris'],
     limit='La cercanía entre el grito y la llegada no prueba que Tortas haya creado o invocado a los tiburones. No se inicia un combate contra ellos ni se identifican con los compañeros de la guía.')
fact(1360,1436,1381,'Naór impulsa a Tortas y todos escapan de los tiburones',
     'Naór entra en furia, se agarra a Tortas y utiliza sus piernas para impulsarlo hacia el norte por el rastro. Tras una tirada de Atletismo, el director fija la velocidad en sesenta y cinco pies. Tentacol recoge a Chopito y los sigue a gran velocidad. Los tiburones se quedan atrás y una escena humorística los muestra volviéndose entre sí. Naór vuelve a cerrar los ojos mientras mantiene el rastreo; al final se piden percepciones a Coyote y Tortas.',
     ['Naór','Tortas','Tentacol','Chopito','Coyote','Triel','Guía sirénida enviada por Maris'],
     limit='No se representan bajas o heridas del grupo por los tiburones ni se proclama su exterminio. El bloque termina antes de narrar qué descubren Coyote y Tortas con sus percepciones.')

stages = [
    dict(titulo='La salida empieza en el colegio', referencias=['45-001','45-002','45-003','45-004','45-007','45-008','45-009','45-010'], texto=
         'Tentacol y Chopito buscan compañeros para ir a Perlasal, mientras Naór practica para vencer el miedo al agua. Antes de partir debe resolver un problema en el colegio de Iktan, junto al lago Tachan. La directora, una pequeña felina con gafas, le reprocha las peleas de Leo y una conducta con el hámster que conoce por otros niños. Naór defiende a su hijo, pero negocia que permanezca dos horas más dejando dos monedas. Promete recogerlo a las cinco y media y autoriza a una muchacha de trenza y pelo azul si ella no vuelve. La identidad de esa persona no queda fijada en la conversación. Después consulta a Walulu: necesita visitar Perlasal por la convocatoria de Tutucan. La chamana ofrece una burbuja de aproximadamente una hora, quizá insuficiente para llegar. Naór decide buscar otra solución. También insiste ante su amiga en que ella es la familia de Leo, mientras Walulu expresa después sus dudas a solas.'),
    dict(titulo='Un pulpo, una tortuga y una perla', referencias=['45-005','45-006','45-011','45-012','45-013'], texto=
         'Chopito considera que Tortas sería un súbdito valioso y manda a Tentacol acercarse a él. El monje intenta meditar, molesto por un dolor de cabeza, hasta que le echan agua encima. Escucha la propuesta de acompañarlos y acepta porque Bigotitos tiene asuntos en Perlasal; no promete rendir culto al pulpo. Naór recoge a Coyote, expulsado otra vez de la taberna después de insistir en sus cortejos, y reúne al grupo. Tortas pregunta el año y la hora, recibe como respuesta 1496 y las diez y cuarenta y tres y experimenta un breve destello cuyo efecto no se explica. Coyote propone un atajo y sumerge su perla para contactar con Maris. Ella cuenta que los Profundos han atacado de nuevo, secuestrado a varios habitantes y obligado a cerrar la ciudad. Cree que los cautivos están en alguna cueva. Aun así, promete enviar ayuda para que los viajeros puedan respirar.'),
    dict(titulo='Un nuevo medio para respirar', referencias=['45-014','45-015','45-016','45-017','45-018','45-019'], texto=
         'La primera figura que sale del lago es Triel, entusiasmada con sus prácticas de apnea y con un pez en la mano. Sus arrugas no prueban que se esté convirtiendo en un ser acuático, por mucho que Coyote se burle. Después llega una sirénida enviada por la princesa Maris. A cambio de ayuda para regresar y encontrar a su escuadrón, ofrece el medio de respirar: besa a Coyote, Naór y Tortas, que desarrollan escamas en el cuello. Tentacol ya se desenvuelve bajo el agua. Naór hace que Triel reciba también el efecto y la elfa se incorpora al viaje. La princesa, todavía aterrada, se aferra al caparazón de Tortas mientras Tentacol transmite los ánimos de Chopito. Todos siguen a la guía por las profundidades del lago y entran en una gruta lateral. Sus fuertes corrientes los transportan hasta el mar, entre antiguas ruinas. No han llegado aún a Perlasal.'),
    dict(titulo='La verdad de la guía y el rastro del combate', referencias=['45-020','45-021','45-022','45-023'], texto=
         'La guía los lleva al lugar donde atacaron a su escuadrón. Primero afirma que fue la única superviviente, pero la pregunta de Chopito la obliga a corregirse: huyó por miedo cuando vio caer a dos compañeros y todavía quedaban otros. Nadie conoce aún el destino de todos. Coyote deja de bromear y Tortas le ofrece apoyo. Tentacol examina el fondo y encuentra coral roto y cortes de armas, señales de una pelea. Mientras Triel se distrae y Naór sigue abrazada al monje, Coyote reúne al grupo: ayudar a encontrar a los desaparecidos es la prioridad para poder continuar hacia la ciudad. Naór activa su percepción de la magia en la zona dañada y descubre restos asociados a armas mágicas que se alejan hacia el norte. Ese indicio marca una dirección, sin identificar todavía a los responsables o a una víctima.'),
    dict(titulo='Un grito y cuatro tiburones', referencias=['45-024','45-025','45-026','45-027'], texto=
         'Triel señala unos seres con aletas, cola y dientes que confunde con gente de Perlasal. Antes de marcharse, Tortas pregunta los nombres del escuadrón: Alfira, Zamuria, Jariora y María Antonieta. Activa su proyección astral y los grita con una voz amplificada que resuena por el agua. No llega una respuesta. Lo que se acerca son cuatro tiburones, y el grupo decide seguir el rastro sin combatirlos. Naór entra en furia y usa las piernas para impulsar a Tortas como una embarcación, alcanzando la velocidad que resuelve el director. Tentacol toma a Chopito y nada detrás. Los tiburones quedan atrás y la expedición continúa hacia el norte. Naór vuelve a cerrar los ojos mientras mantiene el rastreo; Coyote y Tortas miran al frente, donde el descubrimiento siguiente queda fuera de este primer tramo.')
]

histories = []
def history(name, kind, title, text, refs, new=False, description='', note=''):
    histories.append(dict(nombre=name,tipo=kind,nueva=new,descripcion=description,nota=note,
                          etapas=[dict(titulo=title,texto=text,referencias=refs)]))

history('Tentacol','personaje','Del reclutamiento al rastro submarino',
        'Tentacol intenta reunir seguidores para Chopito y consigue que Tortas acepte viajar con el grupo. Traduce las palabras del pulpo cuando los demás solo oyen burbujas y acompaña a Naór durante su miedo al agua. Puede respirar sin el beso de la guía. En las ruinas descubre coral roto y cortes que sugieren un combate. Después sigue a sus compañeros por el rastro del norte, nadando por su cuenta con Chopito para dejar atrás a los tiburones.', ['45-001','45-005','45-006','45-016','45-018','45-021','45-027'])
history('Chopito','personaje','La ambición de conseguir súbditos',
        'Chopito se atribuye las ideas del reclutamiento y pretende sumar a Tortas como súbdito. El monje acepta acompañarlos, sin rendirle culto. Sus frases normalmente llegan a los otros como burbujas y Tentacol las traduce. Durante el viaje intenta que Naór abra los ojos y cuestiona a la guía cuando se presenta como única superviviente. Interpreta los signos del combate y exige seguir adelante, aunque abandona junto a Tentacol la proximidad de los tiburones. Sus alardes no acreditan divinidad o autoridad sobre los demás.', ['45-005','45-006','45-018','45-019','45-020','45-021','45-027'])
history('Naór','personaje','Leo antes de la misión submarina',
        'Naór discute con la directora del colegio por la conducta atribuida a Leo. Consigue que lo mantengan dos horas más a cambio de dos monedas y promete recogerlo a las cinco y media, autorizando también a una chica de trenza y pelo azul que no se nombra aquí. Ante Walulu reafirma que ella es la familia del pequeño. Su misión para convocar a los dirigentes la lleva entretanto a preparar el viaje a Perlasal: rechaza depender solo de una burbuja de duración incierta y acepta la ayuda de la enviada de Maris.', ['45-003','45-004','45-008','45-009','45-010','45-016'])
histories[-1]['etapas'].append(dict(titulo='Miedo, magia y velocidad bajo el agua', texto=
    'Aunque puede respirar gracias al beso, Naór desciende aferrada a Tortas y con los ojos cerrados. En las ruinas usa su percepción mágica y encuentra un rastro de armas hacia el norte. Cuando llegan tiburones, entra en furia y convierte sus patadas en impulso para el monje y sus pasajeros. La decisión permite continuar la búsqueda sin combatir a los animales, pero todavía no muestra su llegada a Perlasal o el regreso por Leo.', referencias=['45-018','45-019','45-023','45-026','45-027']))
history('Leo','personaje','Un día conflictivo en el colegio',
        'La directora del colegio atribuye a Leo peleas y un incidente con el hámster, sobre el que reconoce no ser testigo directo. Naór lo defiende y negocia que permanezca dos horas más antes de salir hacia Perlasal. Promete recogerlo y autoriza a otra persona si no vuelve. Leo no acompaña la expedición submarina y la escena no confirma una expulsión definitiva o una evaluación de su estado emocional.', ['45-003','45-004','45-010','45-018'])
history('Tortas','personaje','Aprender el camino de las profundidades',
        'Tortas acepta acompañar a Naór y al grupo hacia Perlasal después de la invitación de Tentacol. Su respuesta no lo convierte en adorador de Chopito. Recibe el beso que le permite respirar bajo el agua y lleva a Bigotitos sobre el caparazón. Escucha la confesión de la guía y la apoya. Después manifiesta su proyección astral para llamar a los desaparecidos con voz amplificada. No obtiene respuesta, y cuando llegan cuatro tiburones sirve de transporte mientras Naór impulsa al grupo por el rastro del norte. El breve destello anterior no explica su edad.', ['45-006','45-011','45-016','45-018','45-020','45-024','45-025','45-026','45-027'])
history('Coyote','personaje','Volver a cumplir la promesa de Perlasal',
        'Coyote desea regresar a Perlasal después de sus problemas en Iktan. Naór lo reúne con los demás y él utiliza la perla para contactar con Maris. Al conocer los nuevos secuestros, ofrece ayuda y recibe a la enviada que facilita la respiración. Guía a los compañeros a priorizar la búsqueda del escuadrón antes de aspirar a una buena acogida en la ciudad. La confesión de la sirénida interrumpe sus burlas y el rastro los lleva hacia el norte, después de dejar atrás a los tiburones.', ['45-001','45-007','45-011','45-012','45-013','45-015','45-016','45-020','45-022','45-027'])
history('Maris','personaje','Una nueva petición tras el cierre de la ciudad',
        'Coyote vuelve a contactar con Maris mediante la perla. Ella informa de nuevos ataques de los Profundos, de habitantes llevados por los agresores y del cierre de Perlasal. Sospecha que los cautivos están en cuevas. Aun en esas condiciones busca a una sirénida para ayudar a los viajeros a respirar y les pide precaución. La enviada la llama princesa; el primer tramo no muestra a Maris en persona ni resuelve el secuestro de su pueblo.', ['45-012','45-013','45-015'])
history('Walulu','personaje','Consejo para viajar y preocupación por Leo',
        'Walulu escucha a Naór sobre el colegio y la necesidad de llegar a Perlasal por el concilio de Tutucan. Ofrece un conjuro de respiración de aproximadamente una hora, pero advierte que podría no bastar. Naór busca otro método y pide a su amiga que vigile a Leo. La chamana cuestiona si la crianza es adecuada y luego acepta que Naór se considera su familia; su comentario posterior sobre antiguos bichos muertos expresa preocupación, sin determinar el futuro del niño.', ['45-008','45-009','45-010'])
history('Triel','personaje','Las branquias que no consiguió con la apnea',
        'Triel sale del lago después de practicar la contención del aire y cree estar cerca de aprender a respirar bajo el agua. Coyote la asusta con una transformación imaginaria, pero lo que le concede respiración es el beso posterior de la enviada de Maris. Se incorpora a la expedición y disfruta nadando entre las ruinas. Sus confusiones sobre Perlasal y unas figuras con aletas no identifican a los desaparecidos: se trata de tiburones, que el grupo deja atrás al continuar hacia el norte.', ['45-014','45-017','45-019','45-022','45-024','45-026','45-027'])
history('Angelique','personaje','Otra expulsión de Coyote',
        'La tabernera vuelve a rechazar los cortejos de Coyote y lo expulsa. Él sale con una cerveza y trata de regresar para evitar a Naór, pero una botella se estampa cerca de la puerta y la mujer insiste en que se marche. El episodio conserva la identificación contextual provisional de las escenas anteriores de Iktan, sin unirla por el diminutivo Angelita a Angélica Thunder.', ['45-007','45-011'], note='Mantener separadas las identidades de las taberneras mientras no haya identificación inequívoca.')
history('Perla de comunicación de Coyote','objeto','Contacto desde el lago de Iktan',
        'Coyote introduce la perla en el agua y su interior toma aspecto de un mar con remolino. Allí aparece Maris, que informa del nuevo ataque y busca una enviada capaz de ayudar al grupo. El objeto recupera así su función de contacto: la llegada posterior a las ruinas se hace mediante una guía y túneles físicos, no atravesando un portal abierto en la perla.', ['45-012','45-013','45-015','45-019'])
history('Perlasal','lugar','La ciudad cerrada por nuevos ataques',
        'Maris informa de que Perlasal cerró después de nuevos ataques y secuestros de los Profundos. Naór quiere visitarla para hablar con su liderazgo por la convocatoria de Tutucan, pero los viajeros necesitan primero respiración y ayuda para entrar. Una enviada los conduce hacia el escenario del ataque a su escuadrón. En este primer tramo aún no llegan a la ciudad ni celebran la audiencia.', ['45-008','45-009','45-013','45-015','45-018','45-019','45-022'])
history('Profundos','faccion','Los ataques alcanzan a un nuevo escuadrón',
        'Maris les atribuye nuevos ataques contra Perlasal y el secuestro de habitantes. La enviada señala una zona de ruinas donde su escuadrón fue atacado y admite que huyó mientras quedaban compañeros. Tentacol encuentra signos de lucha y Naór detecta un rastro mágico hacia el norte. Eso orienta la búsqueda, sin que este primer tramo muestre aún a los responsables, sus ritos o el destino de cada desaparecido.', ['45-013','45-018','45-019','45-020','45-021','45-023'])
history('Iktan','lugar','Una ruta acuática desde la ciudad oculta',
        'La preparación del viaje parte de la zona comercial de Iktan, donde el colegio reúne a Naór con la directora y el templo permite su consulta a Walulu. La ciudad queda junto al lago llamado provisionalmente Tachan. Coyote contacta allí con Maris y una enviada conduce al grupo por una gruta profunda que comunica con el mar. Leo permanece en el colegio cuando los viajeros salen.', ['45-002','45-003','45-004','45-008','45-012','45-015','45-018','45-019'])
history('Directora del colegio de Iktan','personaje','Una permanencia negociada para Leo',
        'La directora, una pequeña felina con gafas, pide a Naór que baje la voz ante los alumnos. Atribuye a Leo peleas y una conducta indebida con el hámster, aunque reconoce que la última acusación le llegó por los niños. Pretende dejarlo fuera de clase ese día y termina aceptando dos monedas para mantenerlo dos horas más. Registra que Naór puede enviar a otra chica a recogerlo. El comentario posterior de Walulu puede contener el nombre Musí, cuya lectura no es segura.', ['45-003','45-004','45-008'], True,
        'Directora felina con gafas del colegio de Iktan que discute con Naór sobre Leo y acepta una permanencia adicional de dos horas.',
        'Nombre Musí de lectura provisional en el diálogo de Walulu; mantener denominación descriptiva hasta confirmarlo. No fue testigo directo del incidente del hámster.')
history('Colegio de Iktan','lugar','Las dos horas anteriores al viaje',
        'La directora pretende excluir a Leo de clase por los incidentes que le atribuye, pero Naór negocia dos horas más con dos monedas. El niño permanece allí mientras ella prepara el viaje y autoriza a una chica de trenza y pelo azul para recogerlo. La discusión muestra la vida escolar posterior del pequeño, sin identificar inequívocamente el edificio con la academia de guerreros del capítulo 41.', ['45-002','45-003','45-004','45-010','45-018'], True,
        'Colegio de Iktan donde permanece Leo mientras Naór prepara la visita a Perlasal.',
        'Conservar separado de una identificación arquitectónica o institucional automática con la academia de guerreros mencionada antes.')
history('Lago Tachan','lugar','Corrientes entre Iktan y el mar',
        'El director sitúa Iktan junto al lago llamado Tachan. Triel practica allí la apnea y Coyote usa sus aguas para contactar con Maris a través de la perla. La sirénida enviada por ella aparece desde el lago y guía a los viajeros por sus grandes profundidades. Antes de llegar al fondo entra por una gruta lateral cuyas corrientes los impulsan hasta el mar y unas ruinas.', ['45-002','45-012','45-014','45-015','45-019'], True,
        'Lago junto a Iktan con una gruta profunda de corrientes que conduce hacia el mar.',
        'Grafía provisional del nombre recordado por el director. No equiparar sin cotejo todos los lagos anteriores de Xoltacan con este.')
history('Guía sirénida enviada por Maris','personaje','Ayuda respiratoria y una confesión',
        'La sirénida llega a Iktan por indicación de la princesa Maris y concede mediante besos la respiración acuática a Coyote, Naór, Tortas y Triel. Les pide ayuda para regresar y buscar a su escuadrón. Los guía por las corrientes del lago hasta el lugar del ataque. Primero se presenta como única superviviente, pero admite que huyó tras ver caer a dos compañeros aunque quedaban más. Da cuatro nombres para buscarlos y continúa con los viajeros por el rastro del norte.', ['45-015','45-016','45-017','45-018','45-019','45-020','45-024','45-027'], True,
        'Sirénida anónima enviada por Maris para facilitar la respiración y que solicita ayuda para encontrar a su escuadrón atacado.',
        'Separada de Maris y de la sirena cautiva del altar. No se fija su nombre mediante las bromas posteriores ni se confirma su versión inicial de que todos los otros murieron.')
history('Ruinas del ataque al escuadrón sirénido','lugar','El rastro que parte hacia el norte',
        'Después de atravesar las corrientes, los viajeros alcanzan un fondo marino con ruinas. La guía identifica allí la zona donde su escuadrón fue atacado y confiesa que huyó. Tentacol encuentra coral roto y cortes de armas; Naór reconoce una huella de magia que continúa al norte. El grupo abandona la zona para seguirla al acercarse cuatro tiburones, sin confundir estas ruinas con la llegada a Perlasal.', ['45-019','45-020','45-021','45-023','45-026','45-027'], True,
        'Ruinas submarinas donde la enviada de Maris sitúa el ataque a su escuadrón y comienza el rastro hacia el norte.',
        'Nombre editorial descriptivo; este tramo no demuestra que sean el escondite posterior de los Profundos o las ruinas de otras expediciones.')
for name, spelling in [('Alfira','Alfira'),('Zamuria','Zamuria'),('Jariora','Jariora'),('María Antonieta','María Antonieta')]:
    history(name,'personaje','Un nombre en la búsqueda del escuadrón',
            f'La guía enviada por Maris da el nombre {spelling} cuando Tortas le pregunta por sus compañeros. El monje lo llama con su voz astral junto a los otros desaparecidos, sin recibir una respuesta en este tramo. La enumeración no permite saber si esta persona cayó en el ataque, fue capturada o escapó.', ['45-020','45-024','45-025'], True,
            'Persona del escuadrón desaparecido mencionada por la guía sirénida enviada por Maris.',
            'Grafía provisional. No equiparar por conjetura con la cautiva del altar ni fijar especie, sexo, parentesco o estado actual a partir del nombre.')

delivery = dict(bloque=1, lectura_completa=True, primer_segmento='c000001', ultimo_segmento='c002873',
    cobertura_lectura=[dict(desde=0,hasta=289),dict(desde=290,hasta=579),dict(desde=580,hasta=869),dict(desde=870,hasta=1159),dict(desde=1160,hasta=1436)],
    etapas=stages, afirmaciones=facts,
    misiones=[
        'Llegar a Perlasal por la convocatoria de Tutucan: Naór consulta a Walulu, reúne compañeros y obtiene respiración acuática de la enviada de Maris. El grupo cruza al mar pero aún no visita la ciudad en este bloque (45-008–45-009, 45-012–45-019).',
        'Buscar al escuadrón de la guía: la enviada pide ayuda y corrige su relato inicial para admitir que huyó mientras otros seguían allí. Las ruinas contienen indicios de lucha y un rastro mágico hacia el norte; no hay rescate completado en este primer tramo (45-018–45-025).',
        'Regresar por Leo: Naór negocia dos horas de permanencia y promete recogerlo a las cinco y media. Autoriza a una persona sin nombre en este diálogo, pero no se muestra todavía la recogida (45-004, 45-010–45-011).',
        'Dejar atrás a los tiburones: Naór impulsa a Tortas en furia y Tentacol sigue con Chopito. El grupo se aleja sin combatirlos (45-026–45-027).'
    ],
    preguntas=[
        '¿Qué destino tuvieron Alfira, Zamuria, Jariora y María Antonieta después del ataque? La guía huyó mientras quedaban compañeros y los nombres no identifican a una víctima concreta o a una cautiva posterior (45-020, 45-024–45-025).',
        '¿Qué cambio acompaña al destello de Tortas cuando pregunta el año y la hora? La breve luz no explica por sí sola su edad o sus capacidades (45-011).'
    ],
    contradicciones=[
        'Naór es la princesa leonina y madre adoptiva de Leo; las formas Leona en el diálogo no la fusionan con la harengon de Cuicapalli (45-001, 45-003–45-004).',
        'La directora corrige su afirmación de haber visto el incidente escolar: se lo contaron los niños. La edición no convierte esa acusación en una escena observada directamente (45-003).',
        'La persona de trenza y pelo azul autorizada para recoger a Leo no se nombra aquí. Triel viaja con el grupo y Leo permanece en el colegio; no se los traslada al mar por una broma de la mesa (45-004, 45-017–45-018).',
        'La propuesta de burbuja de Walulu no se lanza. La respiración efectiva llega mediante los besos de otra sirénida, sin duración exacta declarada en este bloque (45-009, 45-015–45-017).',
        'Tortas acepta viajar, sin prometer culto a Chopito. Sus respuestas a las burbujas se presentan como interpretación de gestos, sin conceder habla telepática universal o acreditar divinidad (45-005–45-006).',
        'La guía primero se llama única superviviente y luego admite que huyó mientras aún quedaban compañeros. No confirmar por esa primera frase la muerte del escuadrón ni asociar la cautiva posterior a un nombre sin identificación (45-020, 45-024).',
        'Los signos de corte y el rastro mágico orientan hacia el norte, sin fijar un arma concreta o el olor personal de Maris. La voz amplificada de Tortas no obtiene una respuesta de los desaparecidos (45-021, 45-023, 45-025).',
        'El año 1496 y las diez y cuarenta y tres son referencias ficticias. No datan la grabación ni resuelven la edad de Tortas; el destello no basta para afirmar un cumpleaños o un ascenso mecánico (45-011).'
    ],
    nombres_dudosos=[
        'Tenta/Tentacol y Chopito son las identidades ya catalogadas; los apelativos sapo, señor Calamar o semidiosa no crean nombres propios o especies nuevas (45-001, 45-005–45-006, 45-027).',
        'Lago Tachan es una grafía provisional del nombre pronunciado por el director. La directora del colegio podría recibir el nombre Musí en el diálogo de Walulu, pero se conserva la identidad descriptiva hasta confirmarlo (45-002, 45-003, 45-008).',
        'La tabernera llamada Angelita permanece vinculada contextualmente a Angelique; no se fusiona con Angélica Thunder solo por la semejanza del apelativo (45-007, 45-011).',
        'Guía sirénida enviada por Maris identifica a la aliada anónima. Maris aparece en la comunicación de la perla y no es esa enviada; ninguna se equipara por conjetura con la cautiva del altar (45-012–45-017, 45-020).',
        'Alfira, Zamuria, Jariora y María Antonieta son nombres dados por la guía con grafías provisionales. No fijan parentescos, destinos o identidad de otra sirena vista después (45-024–45-025).',
        'El colegio no se identifica automáticamente con la academia de guerreros de la admisión anterior de Leo, ni las ruinas del ataque con el escondite del altar o con cualquier otro templo submarino (45-003, 45-019–45-021).'
    ],
    continuidad=[
        dict(pregunta_id='P29-001', hechos=['45-013','45-019','45-020','45-021','45-023'],nota='Maris relata nuevos ataques y secuestros; se inspeccionan ruinas de un ataque y aparece un rastro al norte. El bloque no entra todavía en el escondite ni muestra ritos, líderes o kraken; integrar los bloques siguientes antes de resolver.'),
        dict(pregunta_id='P29-003', hechos=['45-008','45-013','45-022'],nota='La nueva expedición pretende entrar y colaborar, pero no visita a Ivet ni identifica su deidad en el primer tramo.'),
        dict(pregunta_id='P41-010', hechos=['45-008','45-009','45-016','45-018','45-019'],nota='Naór sí obtiene un medio efectivo de respiración y comienza el viaje submarino. La llegada a Perlasal no se muestra en este tramo; separar ambas partes de la pregunta.'),
        dict(pregunta_id='P21-004', hechos=['45-003','45-004','45-010'],nota='Leo continúa con Naór y escolarizado. El conflicto y las acusaciones son contexto de crianza, sin aceptación formal de custodia por Eromov o evaluación de secuelas.'),
        dict(pregunta_id='P17-003', hechos=['45-008'],nota='Naór relaciona la visita con Tutucan; no se representa la celebración del concilio ni una nueva invitación ya entregada al liderazgo de Perlasal.'),
        dict(pregunta_id='P40-005', hechos=['45-001','45-011'],nota='Los siglos siguen apareciendo en bromas y Tortas pregunta por el año. El destello no concilia los77 años con los siglos de la tradición.'),
        dict(pregunta_id='P41-008', hechos=['45-005','45-006'],nota='Chopito pretende adoración y recibe traducción de Tentacol, sin explicar la ausencia de compulsión del capítulo41 ni acreditar una protección general.')
    ],
    historias_entidades=histories)
assert len(rows) == 1437
assert rows[0]['id'] == delivery['primer_segmento'] and rows[-1]['id'] == delivery['ultimo_segmento']
assert sum(r['hasta']-r['desde']+1 for r in delivery['cobertura_lectura']) == len(rows)
(ROOT / 'campanas/xoltacan/revision/borradores/45/entrega_1.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
print(f'Entrega 1: {len(facts)} afirmaciones validadas, {len(stages)} etapas, {sum(len(s["texto"].split()) for s in stages)} palabras y {len(histories)} propuestas de historia.')
