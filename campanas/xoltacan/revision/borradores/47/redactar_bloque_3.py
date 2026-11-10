"""Entrega editorial local del bloque 3. No modifica las fuentes."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
S = json.loads((HERE / 'bloque_3_segmentos.json').read_text(encoding='utf-8'))
P = json.loads((HERE / 'preguntas_bloque_3.json').read_text(encoding='utf-8'))
SOURCE = ROOT / 'campanas/xoltacan/fuentes/47 - yvqhR20m7Zg.es-orig.vtt'
EXPECTED_SHA = 'af82762727aa32ebc82b92459bdc4b039b6b17839c0f994d26f0a5aaf88e983e'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SHA
assert len(S) == 1028
assert all(s['texto_original'] == s['texto_normalizado'] for s in S)
md = '\n\n'.join(f"[{s['inicio']}–{s['fin']}] {s['texto_normalizado']}" for s in S)
assert md.strip() == (HERE / 'bloque_3.md').read_text(encoding='utf-8').strip()

F = []
FELINO = 'Mictlan'
DRAGON = 'Clolgedranx'
ELFOS = 'Hermanos elfos buscados por el dragón'

def fact(num, titulo, tipo, texto, a, b, q, entidades, limitacion):
    cue = S[q]
    F.append(dict(id=f'47-{num}', titulo=titulo, tipo=tipo, afirmacion=texto,
        inicio=S[a]['inicio'], fin=S[b]['fin'], cita=cue['texto_original'],
        evidencia_cue={k: cue[k] for k in ('inicio', 'fin')} | {'texto': cue['texto_original']},
        entidades=entidades, ambito='encuentro con el dragón y regreso a Iktan',
        conocedores=[], conocimiento_personaje='desconocido',
        nota_conocimiento='No se establece el acceso de Madame Oghma a estos sucesos o conversaciones.',
        confianza='lectura completa de subtítulos automáticos; audio no cotejado', limitacion=limitacion))

fact(301, 'Patata desaparece durante la curación y vuelve a ser visible', 'hecho_confirmado',
    'Mientras Patata está curando al felino, una magia que el director describe como salida de los zombis vuelve invisible a toda criatura dentro de treinta pies; en la escena afecta a Patata. El director aclara que procede de una carta de la mesa. Más adelante Patata vuelve a aparecer y se precisa una duración de un minuto.',
    0, 211, 10, ['Patata', FELINO],
    'No atribuir la invisibilidad a una técnica aprendida de Patata, al dragón o a una curación fallida. El minuto es duración declarada del efecto; la conversación ocupa más tiempo de grabación. La curación venía del bloque anterior y este tramo no fija su cantidad.')
fact(302, 'La presencia invisible susurra junto al oído de Tesara', 'hecho_confirmado',
    'Tesara, escondida en la vegetación, escucha junto a su oído una voz que comenta sus pistolitas. El director confirma que la criatura es invisible, que las hojas se han movido a su alrededor y que ella nota su aliento. La criatura se comporta como si la oliera y califica el hallazgo de interesante.',
    25, 55, 41, ['Tesara Queen', DRAGON],
    'La escena identifica después a la presencia como el dragón que se muestra. Las bromas de comprar leche o de memes no son encargos narrativos. No afirmar que los demás ven ya al dragón.')
fact(303, 'Tesara falla el latigazo y sale de la maleza', 'hecho_confirmado',
    'Tesara intenta golpear con el látigo la dirección de la voz y falla. Tras corregir la reacción de movimiento que pretendía usar, se destraba y sale treinta pies de la vegetación. Tropieza, cae de culo, toma la pistola y avisa a los demás de que hay un dragón escondido allí.',
    65, 162, 158, ['Tesara Queen', DRAGON],
    'El latigazo no hiere a la criatura. La retirada válida es la acción adicional de destrabarse y el movimiento de treinta pies; la reacción de quince pies propuesta antes se corrige. No se adjudica un disparo.')
fact(304, 'Chopito abofetea a Tesara y cuestiona su alarma', 'hecho_confirmado',
    'Tentacol se arrodilla junto a Tesara y abre el recipiente de Chopito. El pulpo sale, se acerca a la cara de ella y le da un guantazo para hacerla reaccionar. Reprocha que, cuando deben ir a buscar a los elfos, ella se meta en historias de dragones. Tesara insiste en que la voz pertenece a un dragón verde invisible.',
    163, 180, 170, ['Tentacol', 'Chopito', 'Tesara Queen', DRAGON],
    'La incredulidad del pulpo es su postura, no una refutación del encuentro. El aviso de Tesara de cocinarlo a la gallega es una amenaza verbal, sin daño consumado o muerte del pulpo.')
fact(305, 'Tesara defiende a los elfos y recuerda una emboscada anterior', 'declaracion_personaje',
    'Tesara pide que no se fíen del dragón porque quiere acabar con dos amigos suyos. Explica que lo conoce de un ataque anterior: les sacó un ejército de zombis mientras se ocultaba y jugaba con sus mentes. Ante la mención del dragón verde se ofrece protección contra venenos para quienes permanezcan cerca.',
    192, 261, 234, ['Tesara Queen', DRAGON, ELFOS],
    'El relato del ataque anterior conserva atribución a Tesara. La promesa de protección contra venenos no demuestra inmunidad, duración o una salvación ya superada; el hablante de esa oferta no está rotulado en el VTT y queda sin atribuir.')
fact(306, 'Las raíces inmovilizan al grupo', 'hecho_confirmado',
    'Cuando Tesara trata de observar dónde sigue la criatura, nota raíces entre los dedos, en el brazo y bajo el cuerpo. También rodean los pies del felino, Patata y Tentacol. Tras las salvaciones de fuerza, el director declara que todos quedan atrapados y no logran moverse haciendo fuerza.',
    262, 296, 293, ['Tesara Queen', FELINO, 'Patata', 'Tentacol', DRAGON],
    'No convertir el efecto en daño físico, muerte o control mental. El contexto lo relaciona con la aparición del dragón, sin que se verbalice aquí un conjuro de nombre determinado.')
fact(307, 'El dragón se muestra y exige a los elfos', 'hecho_confirmado',
    'La vegetación se agita y el dragón deja de estar invisible. Aparece enroscado entre las ramas con la cola y baja de los árboles con movimientos ágiles, silenciosos para su tamaño. Mientras el grupo está atrapado exige que le lleven a los elfos; amenaza con comerse a cada uno y añadirlos a su hueste de muertos.',
    300, 329, 317, [DRAGON, 'Tesara Queen', FELINO, 'Patata', 'Tentacol', ELFOS],
    'La amenaza y la hueste son palabras del dragón. En este pasaje no devora a nadie, no convierte al grupo en muertos ni exhibe un nuevo ejército materializado.')
fact(308, 'La recompensa ofrecida alcanza los deseos de los viajeros', 'declaracion_personaje',
    'El dragón avanza alrededor de los viajeros con su cuerpo serpentino y promete recompensarlos con aquello que desean si le llevan a los elfos.',
    333, 349, 346, [DRAGON, ELFOS],
    'Es una oferta intimidatoria, sin pago, pacto aceptado o demostración de poder conceder cualquier deseo. No definir su especie de bestiario solo por el cuerpo serpentino.')
fact(309, 'Chopito rechaza que le ofrezcan Perlasal', 'declaracion_personaje',
    'Chopito anima mentalmente a Tentacol a negociar. Tentacol pregunta qué puede ofrecer una criatura cuyos dominios parecen limitarse al bosque. El dragón observa al pulpo, le brillan los ojos y dice tener magia poderosa y poder ofrecerle Perlasal. Chopito rechaza que le vendan lo que considera suyo; el dragón replica que entonces sus súbditos no lo respetan.',
    350, 385, 376, ['Chopito', 'Tentacol', DRAGON, 'Perlasal'],
    'Ni la oferta ni la reivindicación del pulpo prueban soberanía efectiva, posesión o control del dragón sobre Perlasal. Los ojos brillantes no explican por sí solos qué magia realiza.')
fact(310, 'El dragón declara que alguien paga por los elfos', 'declaracion_personaje',
    'Preguntado por qué busca a los elfos, el dragón afirma que a él también le han ofrecido una recompensa y que alguien los quiere. Ante el comentario de que una gran sierpe no debería estar al mando de nadie, responde que siempre hay una sierpe más grande.',
    386, 398, 389, [DRAGON, ELFOS],
    'No se nombra al interesado, su especie o su organización. La metáfora de una sierpe mayor no prueba que el contratante sea un dragón, una serpiente o la entidad vinculada a Citlali.')
fact(311, 'El ultimátum da una semana y amenaza a la ciudad', 'declaracion_personaje',
    'El dragón anuncia que enviará su hueste de no muertos a destruir la ciudad si agota su paciencia sin recibir a los elfos. Tras la negativa de Tesara y la amenaza personal contra Oliver, fija un plazo de una semana.',
    399, 429, 429, [DRAGON, ELFOS, 'Iktan', 'Tesara Queen'],
    'La destrucción sigue siendo una amenaza condicional. No ha transcurrido el plazo dentro de este bloque ni se narra el asalto o la entrega de los elfos.')
fact(312, 'El dragón nombra a Oliver, hermano de Tesara', 'declaracion_personaje',
    'Tesara se niega a entregar a sus amigos. El dragón pone la zarpa sobre ella a modo de jaula, sin aplastarla; le brillan los ojos y afirma que Oliver será suyo. Ella pregunta cómo sabe nada de su hermano. La criatura responde que ella misma se lo dice.',
    407, 427, 422, [DRAGON, 'Tesara Queen', 'Oliver'],
    'La respuesta de Tesara identifica a Oliver como su hermano. No demuestra dónde está él, que esté capturado, una invasión mental de mecanismo conocido o que ella haya comunicado voluntariamente la información al dragón.')
fact(313, 'La criatura se retira invisible y los viajeros deciden volver', 'hecho_confirmado',
    'El dragón se interna otra vez en la jungla con movimientos sigilosos y se vuelve invisible; la vegetación que aparta aún permite seguir su volumen. Tesara le grita una amenaza de represalia. Chopito la consuela diciendo que la criatura se marca un farol, y el grupo empieza a plantear el regreso para descansar y encontrar a los hermanos.',
    430, 470, 442, [DRAGON, 'Tesara Queen', 'Chopito', ELFOS],
    'La afirmación del pulpo de ser más poderoso es una fanfarronada. No prueba que el dragón mienta, que haya sido derrotado o que otra persona le arranque la piel. No se explica con precisión cómo termina el agarre de las raíces.')
fact(314, 'Tesara sostiene la confianza en sus compañeros elfos', 'declaracion_personaje',
    'Tesara explica que los buscados son dos hermanos elfos, compañeros con quienes combatió contra la criatura al llegar a Iktan. Dice que se salvaron mutuamente y los considera raros pero buenas personas que quieren matar al dragón. El felino cuestiona si la utilizaron y mantiene su desconfianza; Chopito elogia la capacidad del dragón para sembrar dudas.',
    471, 533, 475, ['Tesara Queen', FELINO, 'Chopito', ELFOS, DRAGON],
    'Las sospechas del felino no prueban traición. Los reconocimientos «el Dream/Eldrin» y «Miriam» se conservan como problema nominal pendiente; este bloque no basta para imponer identidad con Eldrath y Tryel.')
fact(315, 'Tesara guía el regreso a Iktan', 'hecho_confirmado',
    'Los viajeros siguen a Tesara de vuelta a Iktan, ciudad de plantas y colores que algunos aún no conocían. Ella señala la taberna y las ruinas junto al lago y se apresura a buscar a los elfos. Patata y el felino la siguen, este último porque desconfía de ella.',
    534, 556, 537, ['Tesara Queen', FELINO, 'Patata', 'Tentacol', 'Iktan', 'El Huevo Emplumado'],
    'No se fija cuánto dura el camino ni una nueva ruta secreta revelada. La llegada a la ciudad no equivale a encontrar a los elfos.')
fact(316, 'Tentacol y Chopito imitan la meditación de Tortas', 'hecho_confirmado',
    'Tentacol se queda con Chopito junto a Tortas para imitar su postura de meditación, en lugar de entrar con los demás en la taberna. El director los sitúa junto al anciano mientras el otro grupo entra.',
    557, 581, 577, ['Tentacol', 'Chopito', 'Tortas', 'Iktan'],
    'Las bromas sobre contagiarse una maldición por una encuesta no constituyen una maldición diegética confirmada. No se acredita entrenamiento concluido, nuevo poder o autorización formal como discípulos.')
fact(317, 'Patata encuentra a los piratas en la taberna de Iktan', 'hecho_confirmado',
    'Patata reconoce en la taberna a los piratas que frecuentaban la de Shiaru. Al preguntar por la capitana, ellos responden que los echaron del pueblo y tuvieron que venir hasta allí. Le dan cerveza, que prueba y aprecia, y comentan que están agotando las existencias de la encargada.',
    582, 637, 599, ['Patata', 'Tripulación del Zampaolas', 'Ione', 'Angelique', 'El Huevo Emplumado', 'Shiaru'],
    'El motivo de la salida de Shiaru es testimonio de los piratas; no identifica quién gobierna ahora ni una nueva inspección del puerto. La descripción de estar en idéntica posición con las mismas botellas es humor de continuidad, no una duplicación o bucle mágico.')
fact(318, 'Angelique informa de la salida de la elfa y del entrenamiento de su hermano', 'declaracion_personaje',
    'Tesara dice a la encargada que el dragón los ha emboscado y pide localizar a los hermanos. Angelique cuenta que la muchacha salió hace días diciendo que iba a entrenar para bucear, acompañada por el pulpo, la leona y otros. Del hermano afirma que lo vio entrenando esa mañana y que suele estar fuera. Añade que la patrulla aún no ha vuelto; su conjetura de que se habrán ahogado no se confirma.',
    638, 710, 666, ['Tesara Queen', 'Angelique', ELFOS, 'El Huevo Emplumado'],
    'Son noticias y conjeturas de Angelique, sin escena actual de los hermanos o de la patrulla. Las referencias a un pulpo y una leona no autorizan identificar a cada integrante. «Andrea» es un reconocimiento del trato de Tesara, sin crear otra tabernera ni fijarlo como alias confirmado.')
fact(319, 'Tesara y el felino llevan el aviso a Walulu', 'hecho_confirmado',
    'Tras explicar en la taberna que el dragón ha amenazado con la caída de la ciudad, Tesara decide avisar primero a Walulu. Patata permanece con su cerveza; el felino acompaña a la historiadora porque no se fía de ella. Encuentran a Walulu preparando pastas de plantas y medicinas, y Tesara le expone el ultimátum de una semana por los elfos.',
    679, 779, 778, ['Tesara Queen', FELINO, 'Patata', 'Walulu', 'Iktan', DRAGON],
    'La audiencia es sobre el dragón. No confundirla con la consulta pendiente de Citlali e Ione sobre la maldición o dar aquella misión por resuelta.')
fact(320, 'Walulu remite a un antiguo ritual tras el ataque del dragón', 'declaracion_personaje',
    'Walulu reconoce el asunto del dragón que persiguen los hermanos y que atacó a la elfa. Al escuchar la amenaza contra Iktan, sonríe y muestra un gran libro de historias antiguas y relatos de sus dirigentes. Explica que hace ciento veinte años, después del ataque del dragón, el antiguo líder realizó con otros miembros de las tribus un ritual protector. Mira hacia las ruinas al hablar de aquel desastre. Afirma que la protección se hizo contra la magia especial de los dragones y les impide entrar en la ciudad.',
    758, 815, 801, ['Walulu', DRAGON, 'Iktan', 'Libro histórico mostrado por Walulu', ELFOS],
    'Es explicación histórica de Walulu apoyada en el libro, no una visión o reconstrucción del ataque. No se da el nombre del antiguo líder, la fecha absoluta, los ingredientes o un texto íntegro del rito. El VTT reconoce el nombre como «Glendra Drax» y «Colgenrax»; la grafía de catálogo debe resolverla la coordinación.')
fact(321, 'La protección dracónica no detiene por sí sola a la hueste', 'declaracion_personaje',
    'Walulu responde que el dragón no puede acceder de ninguna manera, tampoco sobrevolar la ciudad para llenarla de veneno: la considera protegida de la presencia e invasión de dragones. Ante los no muertos admite que la protección no los detiene, pero confía en la guardia. Razona que el dragón pide sacar a los elfos porque él no puede entrar y que permanecer en Iktan los mantiene seguros frente a él.',
    816, 848, 823, ['Walulu', DRAGON, 'Iktan', ELFOS, 'Guardia de Iktan'],
    'La seguridad es valoración de Walulu; no equivale a invulnerabilidad universal ni a una victoria ya conseguida sobre los muertos. No trasladar el alcance del rito a serpientes, infiltradores o todas las amenazas mágicas.')
fact(322, 'Walulu informa de varias guaridas dispersas', 'declaracion_personaje',
    'Cuando Tesara pregunta cómo encontrar y matar a la criatura, Walulu advierte que derrotar a un dragón no es fácil. Dice que algunos guardias han encontrado diferentes guaridas y cree que el dragón las está dispersando por toda la jungla, lo que dificultará rastrearlo.',
    849, 865, 864, ['Walulu', DRAGON, 'Guardia de Iktan'],
    'No da coordenadas o una guarida inspeccionada por los protagonistas. No se identifica automáticamente ninguna con la cueva de una emboscada anterior, ni se narran nuevos refugios fundados ante la cámara.')
fact(323, 'Walulu acepta estudiar una estrategia contra el dragón', 'declaracion_personaje',
    'Tesara se ofrece a ocuparse del rastreo y pide a Walulu una manera de matar al dragón, una debilidad o una estrategia. Walulu promete estudiar los libros antiguos y acepta hablar con los elfos si los ve. Al final de la audiencia vuelve a los estantes y empieza a buscar pergaminos de antiguas historias.',
    866, 914, 875, ['Tesara Queen', 'Walulu', DRAGON, ELFOS, 'Libro histórico mostrado por Walulu'],
    'Se inicia una búsqueda documental, sin resultado, debilidad revelada o expedición de caza consumada. La invitación a avisar a los elfos no demuestra que Walulu llegue a encontrarlos.')
fact(324, 'El felino prefiere entregar a los elfos y Walulu los acoge', 'declaracion_personaje',
    'Invitado a añadir algo, el felino insiste en que sería más fácil entregar a los elfos. Walulu afirma que son bienvenidos y estarán seguros mientras permanezcan en Iktan; sostiene que la guardia podrá hacer frente a las huestes de muertos. La objeción del felino sobre la seguridad del pueblo la deja pensativa.',
    883, 900, 891, [FELINO, 'Walulu', ELFOS, 'Iktan', 'Guardia de Iktan'],
    'No se aprueba una entrega o sacrificio. La reacción pensativa de Walulu no revoca explícitamente su acogida ni confirma que vaya a cambiar de bando.')
fact(325, 'Walulu quiere hablar con Naór y pide compañía para una reunión futura', 'declaracion_personaje',
    'Walulu pregunta si Naór ha vuelto y dice que necesita hablar con ella. Tesara responde que lleva días cuidando del niño que le dejó. Walulu plantea reunirlos cuando regrese y pide que los acompañen; Tesara acepta contar con ella.',
    901, 914, 907, ['Walulu', 'Naór', 'Tesara Queen', 'Leo'],
    'La reunión queda futura; no se muestra el regreso de Naór ni se declara aquí el destino o la lista completa de convocados. La identificación del niño con Leo procede de su continuidad como menor dejado por Naór, sin convertir la frase en filiación biológica. El numeral del cuidado se corta en «Llevo tr»: no se fija una cifra de días.')
fact(326, 'Tesara y el felino discrepan sobre el sacrificio por un bien mayor', 'declaracion_personaje',
    'Al salir, Tesara pregunta al felino por su inclinación a sacrificar gente. Él defiende un sacrificio por un bien mayor, observa que nadie ha demostrado que los elfos sean útiles y sostiene que los dioses requieren sacrificios. Tesara replica que la vida no debe entregarse como moneda y que no merece servir a dioses que exigen vidas.',
    915, 933, 925, ['Tesara Queen', FELINO, ELFOS],
    'Son posiciones de los interlocutores, no una regla objetiva de todos los dioses o culturas de Xoltacan. No se realiza un sacrificio ni se vincula esa doctrina al rito de los Profundos sin pruebas.')
fact(327, 'La imitación de Tortas se presenta como una apariencia de piedra', 'hecho_confirmado',
    'De vuelta a la taberna, Tesara y el felino ven a Tortas meditando. Tentacol se ha dado con prestidigitación apariencia de roca y Chopito se coloca encima imitando al anciano; añaden la broma de una barba o bigote largo. El director confirma la composición de la escena.',
    934, 954, 949, ['Tentacol', 'Chopito', 'Tortas', 'Tesara Queen', FELINO],
    'La apariencia de roca se explica mediante prestidigitación: no acredita petrificación, aprendizaje de un nuevo estado corporal o maldición compartida. La imitación no explica la edad o el brillo mágico anterior de Tortas.')
fact(328, 'Angelique cuenta a Patata su encuentro con Zoltan', 'declaracion_personaje',
    'Patata intenta cortejar a la encargada, que deriva la conversación hacia un recién llegado de torso desnudo, herida y chispas. Dice que estuvo con él el día anterior, promete presentárselo y finalmente lo nombra Zoltan. Lo describe mientras Patata sigue en la taberna; Tesara y el felino regresan de hablar con Walulu y Chopito continúa la imitación de Tortas en el cierre.',
    955, 1027, 990, ['Patata', 'Angelique', 'Zoltan', 'Tesara Queen', FELINO, 'Tentacol', 'Chopito', 'Tortas', 'El Huevo Emplumado'],
    'No se representa una nueva aparición de Zoltan ni la presentación prometida. La expresión «ayer» pertenece al testimonio de Angelique; no sirve por sí sola para cerrar un calendario. Las comparaciones de mesa con otros personajes o campañas no incorporan sus identidades a Xoltacan.')

def refs(*nums):
    return [f'47-{n}' for n in nums]

ETAPAS = [
    dict(titulo='La voz al oído y la alarma de Tesara', texto='Patata está curando al felino cuando una magia salida de los zombis lo vuelve invisible. El director explica que es un efecto de una carta de la mesa y más tarde le devuelve la visibilidad. En la maleza, Tesara escucha la voz del dragón junto a su oído y nota el aliento de la criatura. Intenta alcanzarla con el látigo, pero falla. Se destraba, sale de la vegetación a trompicones y cae de culo antes de apuntar con la pistola hacia el escondite. Chopito sale del frasco que abre Tentacol, la abofetea y le reprocha esas historias de dragones cuando deberían buscar a los elfos. Ella insiste: se trata de un dragón verde que ya los emboscó con zombis y jugó con sus mentes. Quiere impedir que sus nuevos compañeros se fíen de una voz que amenaza a dos amigos suyos.', referencias=refs(301,302,303,304,305)),
    dict(titulo='La aparición y el precio de los elfos', texto='Antes de que puedan decidir qué hacer, unas raíces se enredan en los brazos y las piernas de Tesara, el felino, Patata y Tentacol. Todos quedan inmovilizados. La vegetación se mueve y el dragón se muestra, enroscado entre las ramas; baja con una agilidad silenciosa y comienza a rodearlos. Exige que le lleven a los elfos y amenaza con devorarlos y sumarlos a su hueste. También ofrece satisfacer sus deseos. Chopito anima a negociar, pero rechaza la propuesta de recibir Perlasal porque lo considera ya suyo. El dragón responde que sus súbditos no lo respetan. Al explicar su interés por los elfos, afirma que alguien le ha prometido a él una recompensa y alude a una sierpe mayor. Tesara se niega a entregar a sus amigos. La criatura forma una jaula con su zarpa, la mira con ojos brillantes y nombra a Oliver. Ella revela en su respuesta que es su hermano, sin comprender cómo lo sabe. El dragón les concede una semana y amenaza con mandar a sus muertos contra Iktan. Después se interna invisible en la jungla; aún se distingue el movimiento de la vegetación a su paso.', referencias=refs(306,307,308,309,310,311,312,313)),
    dict(titulo='La confianza discutida y la vuelta a la ciudad', texto='Chopito trata de tranquilizar a Tesara y llama farol a las amenazas, sin que la escena pruebe que tenga razón. Los viajeros quieren descansar y encontrar a los hermanos. Tesara explica que combatieron juntos al llegar a Iktan y que se salvaron mutuamente. El felino no comparte esa confianza: pregunta si los elfos la utilizaron y duda de que sean preferibles al dragón. La historiadora los defiende como compañeros y buenas personas. Finalmente guía el regreso a la ciudad de plantas y colores. Nada más llegar corre a la taberna a buscarlos. Patata y el felino la siguen; Tentacol y Chopito se quedan con Tortas e imitan su meditación.', referencias=refs(313,314,315,316)),
    dict(titulo='Las noticias incompletas de la taberna', texto='Patata reconoce en la taberna a los piratas de Shiaru. Cuentan que los echaron del pueblo y que tuvieron que refugiarse allí. Le ofrecen cerveza y comentan que están agotando las reservas de la encargada. Tesara pregunta con urgencia por los hermanos elfos. Angelique dice que la muchacha salió hace días para aprender a bucear con una patrulla y que aún no han regresado. La posibilidad de un ahogamiento es una conjetura suya. Del hermano sabe que entrenaba esa mañana, pero no puede localizarlo ahora. Cuando los visitantes explican que el dragón ha amenazado con destruir la ciudad si no recibe a los elfos, la tabernera propone avisar a Walulu. Tesara decide llevar el aviso y el felino la acompaña por desconfianza. Patata se queda con su cerveza.', referencias=refs(317,318,319)),
    dict(titulo='El libro, las ruinas y la protección de Iktan', texto='Walulu los recibe mientras prepara medicinas con plantas. La amenaza del dragón le provoca una sonrisa que sorprende a Tesara. La dirigente abre un gran libro de historias de Iktan y explica que, hace ciento veinte años, tras el ataque del dragón al que vincula con las ruinas, un antiguo líder y otros miembros de las tribus hicieron un ritual de protección. Según ella, ningún dragón puede entrar en la ciudad, ni siquiera sobrevolarla para rociarla de veneno. La protección tiene un límite decisivo: los no muertos no quedan excluidos. Para ellos confía en la guardia. Walulu razona que la exigencia de sacar a los elfos demuestra precisamente la incapacidad del dragón para ir a por ellos dentro de Iktan. Tesara pide una debilidad o una estrategia para matarlo. La dirigente informa de varias guaridas dispersas por la jungla y acepta consultar los libros antiguos, aunque todavía no ofrece una solución. El felino insiste en que entregarle a los elfos sería más fácil; Walulu mantiene que son bienvenidos. Quiere hablar con Naór cuando vuelva y solicita que acompañen una futura reunión. Tesara acepta, tras quejarse de que lleva días cuidando al niño que Naór le dejó. Walulu vuelve a sus estantes y empieza a buscar pergaminos.', referencias=refs(319,320,321,322,323,324,325)),
    dict(titulo='Los sacrificios y el cierre entre compañeros', texto='De vuelta a la taberna, Tesara discute con el felino sobre el valor de la vida. Él justifica un sacrificio por un bien mayor y considera que los dioses necesitan ofrendas; ella se opone a entregar vidas como monedas. No alcanzan un acuerdo ni entregan a los elfos. En el camino ven a Tortas y la imitación de Tentacol y Chopito: el viajero parece una roca mediante prestidigitación y el pulpo se ha colocado encima como el anciano. Dentro, Patata intenta cortejar a Angelique, que termina hablándole del recién llegado Zoltan, su herida y sus chispas. Promete presentárselo. El capítulo cierra con los visitantes de regreso en Iktan, una semana de plazo por delante y la investigación de Walulu recién iniciada.', referencias=refs(326,327,328)),
]

H = []
def history(nombre, tipo, descripcion, nota, titulo, texto, *nums, nueva=False):
    H.append(dict(nombre=nombre, tipo=tipo, nueva=nueva, descripcion=descripcion, nota=nota,
        etapas=[dict(titulo=titulo, texto=texto, referencias=refs(*nums))]))

history('Tesara Queen','personaje','','Tesa es abreviatura confirmada. No se identifica a los elfos solo por los reconocimientos del VTT.',
    'De la emboscada a la defensa de los compañeros',
    'Tesara intenta herir a la voz invisible, falla y sale de la maleza para advertir a los demás. Se opone a entregar a los hermanos y recibe una amenaza que nombra a Oliver, a quien reconoce como su hermano. Guía el regreso a Iktan y busca a los elfos, pero recibe solo noticias incompletas. Lleva el ultimátum a Walulu, pide una estrategia contra el dragón y acepta acompañar una reunión cuando vuelva Naór. Al regresar discute con el felino porque rechaza sacrificar vidas como moneda.',302,303,304,305,311,312,314,315,318,319,323,325,326)
history(FELINO,'personaje','Viajero felino del grupo, cuyo nombre se reconoce en el VTT como Mlan, Miklan, Mic o «mi clan».',
    'Grafía Mictlan respaldada por la escena posterior x-1531013198478708756, leída íntegra por el coordinador (36 mensajes), que rotula al personaje. Esta nota de identidad no traslada la escena futura al vídeo ni pretende que este agente la haya leído.',
    'La utilidad y el sacrificio',
    'Recibe la curación de Patata antes de que este se vuelva invisible. Las raíces lo inmovilizan junto a los demás y presencia la exigencia del dragón. Cuestiona la confianza de Tesara en los hermanos y la sigue a la taberna y a la audiencia con Walulu porque no se fía de ella. Prefiere entregar a los elfos por la seguridad del pueblo y, al salir, defiende el sacrificio por un bien mayor. La historiadora rechaza esa posición.',301,306,307,314,315,319,324,326,nueva=True)
history('Patata','personaje','','La oferta de protección contra venenos queda sin atribuir por falta de hablante rotulado.',
    'La invisibilidad y el reencuentro pirata',
    'Patata queda invisible durante la curación del felino por un efecto temporal adjudicado a una carta y luego reaparece. Las raíces lo atrapan mientras el dragón exige a los elfos. Sigue a Tesara hasta Iktan, reconoce a los piratas desplazados desde Shiaru y prueba una cerveza que aprecia. Permanece en la taberna durante la visita a Walulu y corteja a Angelique, que termina describiéndole a Zoltan y promete presentárselo.',301,306,307,315,317,328)
history('Tentacol','personaje','','La roca del cierre es apariencia mediante prestidigitación, sin petrificación acreditada.',
    'Negociar antes de imitar al maestro',
    'Tentacol abre el frasco para que Chopito salga a hablar con Tesara. Queda atrapado por las raíces, pregunta al dragón qué recompensa podría ofrecer y escucha la propuesta sobre Perlasal. Al volver a Iktan se queda con Tortas y el pulpo para imitar la meditación. En el cierre se muestra como una roca sobre la que se coloca Chopito.',304,306,309,316,327)
history('Chopito','personaje','','Sus pretensiones sobre Perlasal y de ser más poderoso que el dragón son declaraciones, no soberanía o superioridad confirmadas.',
    'La negociación que no entrega a los elfos',
    'Chopito abofetea a Tesara para que reaccione y cuestiona su relato sobre el dragón. Anima mentalmente a Tentacol a negociar; rechaza Perlasal como recompensa porque lo considera suyo. Tras la retirada de la criatura consuela a Tesara y la acusa de marcarse un farol. Ya en Iktan imita a Tortas desde encima de Tentacol con apariencia de piedra.',304,309,313,314,316,327)
history(DRAGON,'personaje','','Grafía Clolgedranx confirmada por el usuario, aplicada por coordinación al interlocutor que Walulu nombra Colgenrax/Glendra Drax y enlaza con el encargo de los hermanos y la barrera de Iktan. Mantener documentado el puente respecto de la etiqueta histórica Dragón verde del bosque de Iktan. No es Zarynth.',
    'Una semana para cobrar una recompensa',
    'La criatura invisible se acerca a Tesara, juega con su miedo y se muestra cuando todos quedan enredados en raíces. Exige a los hermanos elfos, amenaza con devorar al grupo y ofrece recompensas. Dice que alguien le pagará por ellos; nombra a Oliver y da una semana antes de enviar a su hueste contra la ciudad. Se retira otra vez invisible. Walulu lo relaciona con un ataque antiguo tras el que se protegió Iktan e informa de varias guaridas dispersas por la jungla.',302,303,305,306,307,308,309,310,311,312,313,320,321,322)
history('Oliver','personaje','Hermano de Tesara nombrado como objetivo de la amenaza del dragón.',
    'La relación fraterna se acredita por la respuesta de Tesara; no se fijan ubicación, edad, cautiverio o pasado. Cotejar menciones históricas antes de crear ficha definitiva.',
    'El nombre que la criatura conoce',
    'El dragón mira a Tesara con los ojos brillantes y declara que Oliver será suyo. Ella pregunta cómo sabe algo de su hermano. La criatura afirma que ella misma se lo dice, sin explicar un mecanismo ni mostrar a Oliver.',312,nueva=True)
history(ELFOS,'personaje','Pareja de hermanos elfos a los que el dragón exige entregar.',
    'Agrupador provisional para coordinación, no necesariamente ficha nueva definitiva. El VTT da Miriam para la muchacha y Eldrin/el Dream para el varón. No fusionar con Tryel/Eldrath por intuición.',
    'Buscados para una recompensa',
    'Tesara los considera compañeros que se salvaron mutuamente ante la criatura. El dragón dice que un tercero los quiere y pide su entrega. En Iktan Angelique informa de que la muchacha partió con una patrulla para bucear y de que el hermano entrenaba esa mañana, sin localizarlos ahora. Walulu explica que la ciudad los protege frente al dragón y se opone a expulsarlos.',305,307,310,311,314,318,320,321,324)
history('Walulu','personaje','','La explicación del ritual y las guaridas es su testimonio; conservar esta modalidad.',
    'La protección que no alcanza a todos los atacantes',
    'Walulu recibe el aviso y muestra en un libro el antecedente del ritual protector realizado hace ciento veinte años tras el ataque del dragón. Sostiene que Iktan impide su entrada, pero reconoce que los muertos deben contenerse con la guardia. Se compromete a estudiar una estrategia y empieza a buscar pergaminos. Mantiene la acogida de los elfos frente a la propuesta del felino y pide hablar con Naór cuando vuelva.',319,320,321,322,323,324,325)
history('Angelique','personaje','','Continuidad nominal explícita en el cierre («Angelic») y tabernera felina de Iktan. No convertir el reconocimiento Andrea en una identidad nueva ni acreditar su matrimonio por el coqueteo.',
    'Las noticias de la taberna',
    'Angelique atiende a los visitantes mientras los piratas consumen sus reservas. No cree al principio la excusa de Tesara sobre el dragón y le reprocha no traer los objetos que esperaba. Informa de la salida de la elfa y el entrenamiento del hermano, sin darles un paradero actual comprobado. Tras escuchar el ultimátum sugiere avisar a Walulu. Más tarde describe a Patata el encuentro anterior con Zoltan y promete presentarlos.',317,318,319,328)
history('Tortas','personaje','','La imitación del cierre no aclara su edad, su brillo previo o una maldición.',
    'El modelo de la meditación',
    'Tortas permanece en su sitio de Iktan meditando. Tentacol y Chopito se colocan junto a él para imitarlo, hasta componer la apariencia de un anciano sobre una roca. El tramo no muestra que Tortas enseñe una técnica nueva o se incorpore a la audiencia con Walulu.',316,327)
history('Iktan','lugar','','La relación del desastre antiguo con el dragón se atribuye a Walulu y al libro que muestra.',
    'La ciudad bajo el ultimátum',
    'Tesara devuelve a los viajeros a la ciudad, entre la taberna, el lago y las ruinas. La amenaza de una hueste contra Iktan conduce a la audiencia con Walulu. La dirigente explica la protección dracónica nacida del ataque de hace ciento veinte años y confía en su guardia para contener a los muertos. Acoge a los elfos y empieza a buscar una estrategia mientras el plazo de una semana sigue abierto.',311,315,317,318,319,320,321,323,324)
history('El Huevo Emplumado','lugar','','Nombre de continuidad de la taberna de Iktan; no se pronuncia de nuevo en este tramo.',
    'Refugio y noticias incompletas',
    'La taberna aloja a los piratas desplazados de Shiaru y recibe a Patata, Tesara y el felino. Allí se habla de las salidas de los hermanos y de la amenaza del dragón antes de avisar a Walulu. Patata permanece bebiendo y conversando con Angelique; la historiadora y el felino regresan al cierre.',315,317,318,319,328)
history('Tripulación del Zampaolas','faccion','','No se distribuyen los parlamentos colectivos entre piratas individuales sin identificación en el VTT.',
    'Expulsados de Shiaru según su relato',
    'Patata reconoce a los piratas de Shiaru en la taberna de Iktan. Le cuentan que los echaron del pueblo y que tuvieron que desplazarse hasta allí. Le ofrecen cerveza y comentan que están agotando el suministro de la encargada, sin describir en este tramo el nuevo gobierno o un regreso organizado.',317)
history('Guardia de Iktan','faccion','Guardia local en la que Walulu confía para contener las huestes de muertos.',
    'Función colectiva en testimonio de Walulu; sin nombres individuales, número o victoria nueva confirmados.',
    'Defensa frente a la hueste y noticias de guaridas',
    'Walulu asegura que la guardia ha mantenido bajo control el problema de los muertos y cree que podrá contener la amenaza. Atribuye a algunos guardias el hallazgo de diferentes guaridas del dragón por la jungla. No se representa esa exploración ni un nuevo combate de la guardia.',321,322,324,nueva=True)
history('Libro histórico mostrado por Walulu','objeto','Gran libro sobre historias antiguas y dirigentes de Iktan que Walulu abre durante la audiencia.',
    'Denominación descriptiva sin título propio pronunciado. No equivale al diario Terran ni a una receta de Parroter.',
    'La consulta sobre el ritual protector',
    'Walulu busca una entrada del volumen y la muestra al explicar el ritual del antiguo líder tras el ataque del dragón. Después acepta estudiar los libros antiguos y busca pergaminos para hallar una estrategia. No se transcribe el contenido completo del volumen ni se entrega a los viajeros.',320,323,nueva=True)
history('Zoltan','personaje','','Solo mencionado y descrito por Angelique; no aparece actuando en este bloque.',
    'La descripción que recibe Patata',
    'Angelique cuenta a Patata que ha llegado un hombre de torso desnudo, herida y chispas con quien estuvo el día anterior. Lo nombra Zoltan y promete presentárselo. Su testimonio amplía la circulación del nombre, sin explicar las marcas, la electricidad o el pasado del recién llegado.',328)
history('Naór','personaje','','La reunión futura no prueba su regreso ni se identifica automáticamente con el concilio de Tutucan.',
    'Una conversación a la vuelta',
    'Walulu quiere hablar con Naór y pregunta si ha vuelto. Tesara lamenta llevar días cuidando al niño que le dejó. La dirigente plantea reunirlos cuando regrese y obtiene el compromiso de Tesara de acompañarlos, sin que la reunión llegue a celebrarse.',325)

MISSION = [
    'Salir del encuentro con el dragón: después del fallo del látigo y de quedar inmovilizados, los viajeros reciben el ultimátum. La criatura se retira y el grupo vuelve a Iktan; no la derrotan ni pactan la entrega de los elfos (47-303, 47-306–47-315).',
    'Encontrar y avisar a los hermanos elfos: Tesara los busca en la taberna. Angelique solo ofrece noticias de la patrulla de la muchacha y del entrenamiento del hermano. Walulu acepta hablar con ellos si los ve; no se representa el contacto (47-314, 47-318, 47-323).',
    'Defender Iktan del ultimátum: el dragón da una semana y amenaza con mandar muertos. Walulu explica la barrera contra dragones, acoge a los elfos y confía en la guardia frente a la hueste. La defensa y el desenlace del plazo siguen pendientes (47-311, 47-320–47-324).',
    'Hallar una estrategia contra la criatura: Tesara propone encargarse del rastreo y solicita una debilidad. Walulu informa de varias guaridas y empieza la consulta de libros y pergaminos. No se obtiene todavía la respuesta ni se inicia la caza (47-322–47-323).',
    'Hablar con Naór cuando regrese: Walulu quiere reunirlos y solicita compañía; Tesara acepta. La vuelta de Naór, el destino y la reunión no se muestran en el tramo (47-325).',
    'Imitar a Tortas: Tentacol y Chopito permanecen junto al anciano y reproducen su meditación mediante una apariencia de roca y barba. No se acredita aprendizaje terminado o una capacidad nueva (47-316, 47-327).',
]
NEW = [
    dict(id_provisional='P47-B3-01', pregunta='¿Quién ofrece al dragón una recompensa por los hermanos elfos y con qué propósito? La alusión a una sierpe mayor no identifica al contratante.', estado='pendiente', respuesta='El dragón dice que alguien los quiere y que le han prometido un pago; no proporciona nombre o plan.', referencias=refs(310), pendiente='La identidad del interesado, los términos y el motivo del encargo.'),
    dict(id_provisional='P47-B3-02', pregunta='¿Qué hará el dragón cuando venza la semana y cómo responderán Iktan y sus guardias a la hueste? La protección dracónica no excluye a los muertos.', estado='pendiente', respuesta='Walulu confía en su guardia y protege la permanencia de los elfos, pero el plazo no se resuelve en el bloque.', referencias=refs(311,321,324), pendiente='La ejecución o retirada del ultimátum y el resultado de la defensa.'),
    dict(id_provisional='P47-B3-03', pregunta='¿Dónde está Oliver y cómo obtiene el dragón la información sobre el hermano de Tesara? Nombrarlo y decir que será suyo no prueba su captura.', estado='pendiente', respuesta='Tesara reconoce el parentesco al preguntar cómo lo sabe; la criatura responde que ella se lo dice.', referencias=refs(312), pendiente='El paradero de Oliver y el origen y mecanismo del conocimiento del dragón.'),
    dict(id_provisional='P47-B3-04', pregunta='¿Qué estrategia o debilidad encontrará Walulu en los libros y cómo localizarán las guaridas dispersas del dragón?', estado='pendiente', respuesta='Walulu promete estudiar y empieza a buscar pergaminos. No presenta el resultado.', referencias=refs(322,323), pendiente='La información obtenida y su aplicación en una caza efectiva.'),
    dict(id_provisional='P47-B3-05', pregunta='¿Qué reunión quiere organizar Walulu al regreso de Naór y a dónde pide que los acompañen?', estado='pendiente', respuesta='Walulu pide hablar con Naór y Tesara acepta acompañarlos, sin que el tramo precise destino, lista completa o fecha.', referencias=refs(325), pendiente='La convocatoria concreta y su celebración.'),
]

# Cada entrada conserva la pregunta previa íntegra: las observaciones se limitan al bloque leído.
UPDATES = {
 'P31-001': ('avance_parcial', 'parcial', 'Walulu vincula el ataque del dragón que discuten con el desastre de las ruinas y muestra un libro: tras él se hizo una protección hace ciento veinte años. El VTT vuelve a deformar el nombre; el uso de la grafía del usuario y la relación con Clolgedranx requieren integración de identidades.', refs(320), 'La equivalencia nominal exacta y los detalles históricos del ataque; no tratar el testimonio como inspección del pasado.'),
 'P31-002': ('avance_sin_cierre', 'parcial', 'Se observan invisibilidad, acercamiento a Tesara y raíces que inmovilizan al grupo. El dragón conoce el nombre de Oliver y Walulu dice que manipula a quienes entran en su territorio. No se explica el mecanismo completo ni se rompe de forma permanente.', refs(302,306,312,321), 'El mecanismo, alcance y neutralización permanente de la influencia.'),
 'P31-004': ('sin_cambio_en_el_bloque', 'pendiente', 'Walulu habla de un líder de hace ciento veinte años, sin identificarlo con su padre o explicar el altercado de su muerte.', refs(320), 'Las circunstancias y responsables de la muerte de su padre.'),
 'P31-005': ('mencion_sin_respuesta', 'pendiente', 'Tesara guía a nuevos viajeros hasta Iktan y Walulu plantea hablar con Naór. No se menciona un castigo por revelar la ruta ni se identifica la futura reunión con el concilio de Tutucan.', refs(315,325), 'Consecuencias concretas de revelar la ruta y asistencia efectiva al concilio.'),
 'P39-003': ('avance_parcial', 'parcial', 'Walulu explica el impedimento: un ritual tras el ataque de hace ciento veinte años protege Iktan de la entrada de dragones. La conversación se refiere a la criatura que busca a los hermanos. No fija por sí sola la identidad de la pareja anónima del 39 o un diagnóstico nuevo de la muchacha.', refs(318,320,321), 'Integrar la identidad de los elfos y la continuidad nominal del dragón; queda pendiente el diagnóstico de la elfa anónima.'),
 'P39-004': ('avance_sin_cierre', 'parcial', 'El problema de Iktan se amplía con el ultimátum contra la ciudad y las limitaciones de la protección. La audiencia de Tesara y el felino trata del dragón, sin realizar la consulta de Citlali e Ione sobre tatuajes.', refs(311,319,320,321), 'La conversación con Citlali y las causas completas de las amenazas.'),
 'P39-005': ('mencion_sin_respuesta', 'pendiente', 'El dragón invisible se muestra ante este grupo y luego se retira. No identifica retrospectivamente la presencia del capítulo 39 ni informa de los yuan-ti sepultados.', refs(302,307,313), 'La identidad de aquella presencia y el destino de los yuan-ti tras el derrumbe.'),
 'P40-001': ('avance_sin_cierre', 'pendiente', 'El dragón llama suya a una hueste de muertos y amenaza con enviarla. Tesara le atribuye la emboscada con zombis. No se representa la animación de los restos del claro ni se analiza la función causal de su veneno.', refs(305,307,311), 'El origen demostrado de la animación y la función causal del veneno.'),
 'P40-002': ('sin_cambio_en_el_bloque', 'pendiente', 'Las raíces y plantas del encuentro se mueven, pero no se inspecciona la contaminación del lago y del claro ni se verifica la recuperación de la vegetación.', refs(306,313), 'La extensión del daño y recuperación de la vegetación del claro y del lago.'),
 'P40-003': ('avance_parcial', 'parcial', 'Walulu informa de diferentes guaridas halladas por guardias y dispersas por la jungla. La conversación histórica aporta una conexión contextual con la criatura nombrada de varias formas, sin una guarida localizada o identificación de la cueva anterior.', refs(320,322), 'La localización de las guaridas, la relación con la cueva de la emboscada y la integración nominal con Clolgedranx.'),
 'P40-004': ('mencion_sin_respuesta', 'pendiente', 'Tesara solicita una estrategia para matar al dragón. No intervienen Ione o Poncelot ni se revelan las preguntas que Eldrath quería hacerle; tampoco se ejecuta la caza.', refs(323), 'La información concreta de Eldrath y el reclutamiento y ejecución de su expedición.'),
 'P40-005': ('sin_cambio_en_el_bloque', 'pendiente', 'El dato de ciento veinte años se refiere al ritual de un dirigente antiguo. Tortas medita y es imitado, sin una explicación de sus cifras de edad.', refs(316,320,327), 'La conciliación de la cronología personal de Tortas.'),
 'P40-006': ('mencion_sin_respuesta', 'parcial', 'La amenaza del dragón y la preparación contra su hueste añaden un frente local, sin identificarse como toda la operación del festival. La audiencia no trata la llegada de expertos o la evolución de Eromov.', refs(311,321,324), 'La llegada de los expertos, recuperación de Eromov y alcance restante de la operación anterior.'),
 'P41-004': ('mencion_sin_respuesta', 'pendiente', 'La búsqueda de los elfos y la amenaza de muertos no se vinculan expresamente con la orden de retirar a Tortas o el mando de los sacerdotes del norte.', refs(310,311,316), 'La finalidad de retirar al Anciano, los integrantes restantes y el mando de aquella operación.'),
 'P41-008': ('sin_cambio_en_el_bloque', 'pendiente', 'Tentacol negocia y Chopito se comunica mentalmente con él, pero no se explica la excepción a la compulsión del capítulo 41.', refs(309), 'La causa de la excepción de Tentacol a aquella compulsión.'),
 'P41-009': ('avance_parcial', 'parcial', 'Walulu habla de la criatura en relación con el ataque antiguo y explica que los guardias encontraron varias guaridas. No ofrece posición concreta o inspección; la grafía del usuario y su equivalencia con el dragón descriptivo deben integrar las fuentes históricas.', refs(320,322), 'La ubicación de guaridas y la integración inequívoca de identidad con Clolgedranx.'),
 'P41-011': ('sin_cambio_en_el_bloque', 'pendiente', 'La prestidigitación explica la apariencia de roca de Tentacol en la imitación. No explica el brillo anterior de Tortas ni lo atribuye a la piedra sagrada.', refs(327), 'El origen y función del brillo mágico detectado en el Anciano.'),
 'P42-003': ('mencion_sin_respuesta', 'pendiente', 'Los piratas dicen a Patata que los echaron de Shiaru y por eso están en Iktan. No identifican al gobernante ni añaden una escena de las consecuencias del disparo contra Bonny.', refs(317), 'Las consecuencias posteriores del disparo y el gobierno de Shiaru.'),
 'P45-002': ('sin_cambio_en_el_bloque', 'pendiente', 'La discusión del felino con Tesara sobre dioses y sacrificios expresa sus posiciones. No identifica al dios de los Profundos ni explica su resurrección o el papel de las sirenas.', refs(326), 'La identidad del dios y los requisitos y eficacia del rito de los Profundos.'),
 'P45-005': ('mencion_sin_respuesta', 'pendiente', 'La reunión futura de Walulu con Naór no contiene una respuesta de Ivet ni la confirmación de su asistencia a Tutucan.', refs(325), 'La decisión definitiva de Ivet y eventual asistencia.'),
 'P45-009': ('sin_cambio_en_el_bloque', 'pendiente', 'Tortas sigue meditando y Tentacol y Chopito lo imitan. No se explica el destello que siguió a la pregunta por la fecha y hora.', refs(316,327), 'El sentido de aquella manifestación.'),
 'P46-003': ('mencion_sin_respuesta', 'pendiente', 'Angelique describe a Zoltan con una herida y torso desnudo. No explica el origen de la cicatriz o mancha ni las circunstancias de su cautiverio.', refs(328), 'El pasado, las marcas y los responsables y motivos del encierro.'),
 'P46-004': ('mencion_sin_respuesta', 'pendiente', 'Angelique vuelve a mencionar chispazos de su encuentro con Zoltan. No hay una demostración nueva de control, un origen o condiciones de su electricidad.', refs(328), 'El origen, condiciones, límites y dominio estable de sus capacidades.'),
 'P46-006': ('sin_cambio_en_el_bloque', 'pendiente', 'Patata reconoce a los piratas y les pregunta por la capitana, pero esta conversación no localiza al novato o aclara su identidad.', refs(317), 'La identidad, paradero y circunstancias de la desaparición del novato.'),
 'P46-007': ('sin_cambio_en_el_bloque', 'pendiente', 'Los piratas explican su desplazamiento a Iktan, pero no ejecutan el plan de Ione de buscar apoyos o recuperar el puerto.', refs(317), 'Los apoyos, expedición, situación del puerto y resultado del plan.'),
 'P46-008': ('mencion_sin_respuesta', 'pendiente', 'Tesara dice que lleva días cuidando al niño que Naór le dejó; el numeral se corta en «tr». No se representa la reunión de madres, el encuentro con Naór o la evolución escolar con Eztli.', refs(325), 'La reunión de madres, el regreso de Leo y la convivencia escolar.'),
}
COTEJO=[]
for p in P:
    if p['id'] in UPDATES:
        resultado, estado, obs, rr, pendiente = UPDATES[p['id']]
    else:
        resultado, estado = 'sin_cambio_en_el_bloque', p['estado']
        obs = 'La lectura íntegra de 01:34:05.719–02:20:12.399 no aporta respuesta nueva al asunto concreto de esta pregunta. Límite cotejado: ' + (p.get('pendiente') or 'Su resolución anterior se conserva; este tramo no la modifica.')
        rr, pendiente = [], p.get('pendiente','')
    COTEJO.append(dict(id=p['id'], pregunta_previa=p['pregunta'], estado_previo=p['estado'],
        sha256_pregunta=p['sha256_pregunta'], resultado=resultado, estado_propuesto=estado,
        observacion_bloque=obs, referencias=rr, pendiente=pendiente,
        alcance='Solo bloque 3 del capítulo 47; no declara ausencia en el capítulo completo.'))

COVER=[]
for a,b in [(0,179),(180,359),(360,539),(540,719),(720,899),(900,1027)]:
    COVER.append(dict(desde_indice=a,hasta_indice=b,primer_segmento=S[a]['id'],
        ultimo_segmento=S[b]['id'],inicio=S[a]['inicio'],fin=S[b]['fin']))

D=dict(bloque=3, capitulo=47, titulo='Cadáveres', lectura_completa=True,
    primer_segmento=S[0]['id'],ultimo_segmento=S[-1]['id'],cobertura_lectura=COVER,
    fuente_sha256=EXPECTED_SHA,segmentos_leidos=1028,
    equivalencia_markdown_json='Verificada íntegramente: los 1028 textos originales y normalizados son iguales y forman exactamente bloque_3.md.',
    cobertura_preguntas=[dict(desde_indice=a,hasta_indice=b,primera=P[a]['id'],ultima=P[b]['id']) for a,b in [(0,17),(18,37),(38,56),(57,76),(77,94)]],
    etapas=ETAPAS, afirmaciones=F,historias_entidades=H,misiones=MISSION,
    preguntas=[x['pregunta'] for x in NEW],seguimiento_nuevo=NEW,cotejo_preguntas_asignadas=COTEJO,
    dudas_y_puentes=[
        'Mictlan: nombre reconocido en los bloques como Mlan/Miklan/Mic/mi clan. El coordinador ha leído completos los 36 mensajes de la escena posterior x-1531013198478708756 y confirma la grafía por rótulo. La entrega usa ese canónico con nota de respaldo, sin trasladar los sucesos posteriores al vídeo.',
        'Los elfos son llamados Miriam y Eldrin/el Dream. El coordinador confirma Eldrath y Tryel mediante lectura íntegra de los 80 mensajes posteriores de x-1530576387507753053: Tessa usa esas variantes ante personajes rotulados, él asume la amenaza contra él y su hermana y Tryel interviene. El relato del vídeo conserva la pareja descriptiva; integrar identidades con fuente posterior separada.',
        'Walulu nombra al dragón del diálogo como Glendra Drax/Colgenrax. Coordinación aplica la grafía del usuario Clolgedranx por el puente del encargo de los hermanos y la barrera de Iktan del 39; se añade la relación testimonial con ruinas. Documentar el puente histórico respecto de Dragón verde del bosque de Iktan, sin confundir con Zarynth.',
        'El ataque a las ruinas y el ritual protector de hace ciento veinte años aparecen como relato de Walulu apoyado en un libro. Puede avanzar P31-001 y P39-003, conservando su condición testimonial.',
        'Oliver es hermano de Tesara por respuesta explícita. No está capturado ni presente en escena. Cotejar cualquier ficha histórica antes de crear duplicado.',
        'La voz que ofrece protección contra venenos en 01:44:45.639–01:44:52.910 carece de hablante rotulado. La oferta se conserva sin atribución nominal; no usar poderes genéricos para asignarla.',
        'La salida y falta de regreso de la patrulla son noticias de Angelique; el ahogamiento es solo su hipótesis. No sustituir el resultado de la expedición acuática del capítulo 45 por esa conjetura.',
        'El bloque empieza durante la curación del felino y el combate ya cerrado; no vuelve a narrar el daño previo ni confirma por sí solo su cantidad.',
        'El ofrecimiento de reunión al regreso de Naór no precisa destino o convocados completos y no equivale automáticamente al concilio de Tutucan. Enlazar con planes de los otros bloques.',
        'El cuidado del niño lleva días, pero el numeral se corta en «Llevo tr» y no se fija como tres. El ayer de Angelique y las dos semanas de jungla de Patata son declaraciones contextuales, no un calendario absoluto certificado.',
        'La apariencia de roca de Tentacol y la barba del pulpo se sitúan en una imitación con prestidigitación. Las bromas sobre maldiciones, memes y personajes de otras campañas no se incorporan como hechos de Xoltacan.',
        'Madame Oghma no recibe acceso atestiguado a estas conversaciones; conocimiento_personaje permanece desconocido.'
    ])

sys.path.insert(0,str(ROOT/'scripts'))
from construir import validate_fact
for f in F:
    validate_fact(f,SOURCE)
    cue=f['evidencia_cue']
    assert any(s['inicio']==cue['inicio'] and s['fin']==cue['fin'] and s['texto_original']==cue['texto'] for s in S)
assert len({f['id'] for f in F})==len(F)
assert {p['id'] for p in P}=={p['id'] for p in COTEJO}
known={f['id'] for f in F}
for item in ETAPAS:
    assert set(item['referencias']) <= known
for h in H:
    for e in h['etapas']:
        assert set(e['referencias']) <= known
(HERE/'entrega_3.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

notes = '''# Lectura editorial del bloque 3 del capítulo 47

Se han leído íntegros los 1028 segmentos c004115–c006169, desde 01:34:05.719 hasta 02:20:12.399. El audio no está cotejado. Se ha verificado el SHA-256 del VTT original: `af82762727aa32ebc82b92459bdc4b039b6b17839c0f994d26f0a5aaf88e983e`.

Los textos originales y normalizados son idénticos en los 1028 segmentos. Se ha comprobado por código que el Markdown completo es exactamente la unión ordenada de esos textos con sus intervalos. La lectura humana se realizó sobre todos los textos con IDs e intervalos en seis tramos sin truncamiento: 0–179, 180–359, 360–539, 540–719, 720–899 y 900–1027. Así se cubren completos el Markdown y el JSON sin releer contenido idéntico.

Las 95 preguntas asignadas, de P31-001 a P46-008, se han leído completas, incluidos respuestas previas, referencias, pendientes y límites, en los tramos 0–17, 18–37, 38–56, 57–76 y 77–94. La entrega contiene un cotejo individual de las 95. Sus conclusiones de ausencia se limitan a este bloque.

Se han leído AGENTS.md, continuidad_46.md e identidades_contexto.json y consultado el catálogo de entidades para identidades, separaciones y grafías. Las citas y evidencia_cue se extraen literalmente de texto_original. Todas las afirmaciones pasan validate_fact contra el VTT original; también se verifican IDs únicos, coincidencia exacta de las cues y referencias internas.

## Recorrido íntegro

- 01:34:05.719–01:41:36.145: Patata desaparece durante la curación; la criatura invisible susurra a Tesara; falla el látigo y se retira; Chopito la abofetea y cuestiona su alarma.
- 01:41:36.155–01:45:47.229: Tesara defiende a los elfos y relata el ataque anterior; Patata reaparece; se ofrece protección contra venenos; las raíces empiezan a atraparlos.
- 01:45:47.239–01:54:52.350: todos quedan inmovilizados; se muestra el dragón; recompensa, Perlasal, contratante desconocido, ultimátum, Oliver y retirada invisible; Chopito minimiza la amenaza.
- 01:54:52.360–02:02:28.390: discusión sobre la confianza en los hermanos y regreso a Iktan; Tentacol y Chopito imitan a Tortas; Patata encuentra a los piratas y bebe cerveza.
- 02:02:28.400–02:07:10.669: Angelique da noticias incompletas de los elfos; hipótesis de ahogamiento; deciden avisar a Walulu; discusión de Tesara y el felino sobre el tacto.
- 02:07:10.679–02:14:38.549: audiencia; libro y ritual de hace 120 años; ruinas; protección contra dragones y límite ante muertos; guaridas, investigación prometida y propuesta rechazada de entrega de los elfos.
- 02:14:38.559–02:20:12.399: futura reunión con Naór; discusión sobre sacrificios; imitación mediante prestidigitación; Angelique describe a Zoltan; regreso y despedida.

## Precauciones de integración

El coordinador ha confirmado por fuentes posteriores leídas íntegras la grafía Mictlan (x-1531013198478708756, 36 mensajes) y a los hermanos Eldrath/Tryel (x-1530576387507753053, 80 mensajes). Este agente no atribuye esas lecturas al bloque: usa el canónico Mictlan con nota y conserva la pareja descriptiva en el relato del vídeo. Clolgedranx se aplica por coordinación al nombre deformado que da Walulu y al puente contextual del encargo y la barrera de Iktan; debe mantenerse documentada su relación con la etiqueta histórica del dragón verde. El parentesco de Oliver sí tiene respuesta explícita de Tesara. El ritual y las guaridas son testimonios de Walulu; la amenaza no se ejecuta, la oferta no se acepta y el plazo no se cumple dentro de este tramo. La roca de Tentacol no prueba petrificación. Las bromas y las comparaciones con otras campañas quedan fuera del relato factual.
'''
(HERE/'lectura_bloque_3.md').write_text(notes,encoding='utf-8')
print(f'{len(F)} afirmaciones validadas; {len(H)} historias; {len(COTEJO)} preguntas cotejadas; {len(ETAPAS)} etapas.')
