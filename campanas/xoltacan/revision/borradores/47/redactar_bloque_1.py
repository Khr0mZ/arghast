"""Entrega editorial del bloque 1, después de leer sus 1028 segmentos completos."""
import hashlib
import importlib.util
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True

ROOT = pathlib.Path(__file__).resolve().parents[5]
BASE = pathlib.Path(__file__).resolve().parent
SEG = json.loads((BASE / 'bloque_1_segmentos.json').read_text(encoding='utf-8'))
QUESTIONS = json.loads((BASE / 'preguntas_bloque_1.json').read_text(encoding='utf-8'))
SOURCE = ROOT / 'campanas/xoltacan/fuentes/47 - yvqhR20m7Zg.es-orig.vtt'
EXPECTED_SHA = 'af82762727aa32ebc82b92459bdc4b039b6b17839c0f994d26f0a5aaf88e983e'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SHA
assert len(SEG) == 1028
md_lines = (BASE / 'bloque_1.md').read_text(encoding='utf-8').splitlines()
assert all(md_lines[i * 2] == f"[{x['inicio']}–{x['fin']}] {x['texto_normalizado']}" for i, x in enumerate(SEG))

facts = []


def fact(number, start, end, quote, title, kind, claim, entities, limitation, witnesses=()):
    cue = SEG[quote]
    facts.append({
        'id': f'47-{number}', 'titulo': title, 'tipo': kind, 'afirmacion': claim,
        'inicio': SEG[start]['inicio'], 'fin': SEG[end]['fin'],
        'cita': cue['texto_original'],
        'evidencia_cue': {'inicio': cue['inicio'], 'fin': cue['fin'], 'texto': cue['texto_original']},
        'entidades': entities, 'ambito': 'regreso de Patata y encuentro en las ruinas del lago de Iktan',
        'conocedores': list(witnesses), 'conocimiento_personaje': 'desconocido',
        'nota_conocimiento': 'Acceso de Madame Oghma sin establecer en este pasaje.',
        'confianza': 'lectura íntegra de subtítulos; audio no cotejado', 'limitacion': limitation,
    })


fact(101, 6, 25, 22, 'Patata encuentra su huerto destruido y el cuerpo de Bonny expuesto', 'explicacion_director',
     'Tras el repaso de Patata sobre su huida de Shiaru, el director concreta que regresó allí en uno de sus viajes, encontró el huerto totalmente destrozado y vio el cuerpo de «Happy» Bonny colgado de la entrada. Lo sitúa después de vuelta en la jungla.',
     ['Patata', 'Shiaru', 'Granja de Patata', '"Happy" Bonny'],
     'Se confirma lo que Patata encontró, sin representar la ejecución ni identificar a quien colgó el cuerpo o destruyó el huerto. La vuelta hacia la jungla se formula como enlace del director.', ['Patata'])
fact(102, 28, 39, 35, 'Tesa combina el cuidado de Leo con la investigación del dragón', 'declaracion_personaje',
     'La jugadora recuerda que Tesa cuida a un conejo maleducado e intenta dedicar sus ratos libres a investigar el encargo de los elfos para encontrar al dragón; también busca tiempo para sus libros y su vino.',
     ['Tesara Queen', 'Leo', 'Dragón verde del bosque de Iktan'],
     'Es una recapitulación de actividad e intención; no demuestra que ya haya encontrado al dragón, realizado la caza o completado una investigación.')
fact(103, 44, 60, 50, 'Tenta sale de Perlasal con Chopito para buscar más súbditos', 'declaracion_personaje',
     'La jugadora sitúa a Tenta y Chopito después de la estancia en Perlasal. Dice que los habitantes conocen a Tenta pero desconfían del pulpo, y que Chopito quiere volver a buscar súbditos leales. El director corrige que van en dirección a Iktan, sin haber llegado todavía.',
     ['Tentacol', 'Chopito', 'Perlasal', 'Iktan'],
     'La reacción de los habitantes y el objetivo de reclutamiento son recapitulación. No se cuantifican los seguidores ni se confirma la divinidad que Chopito se atribuye.')
fact(104, 76, 85, 83, 'Tesa lleva a Leo al colegio y reclama que vuelva su madre', 'hecho_confirmado',
     'En Iktan, Tesa acompaña a Leo de la mano al colegio. Se queja de que lleva tres días con ella y considera que debería hacerse cargo su madre.',
     ['Tesara Queen', 'Leo', 'Colegio de Iktan', 'Iktan'],
     'Más tarde Tesa habla de tres o cuatro días y de cuatro días: no se convierte esa vacilación en una cronología exacta. La madre no aparece ni se la nombra aquí.', ['Tesara Queen', 'Leo'])
fact(105, 86, 107, 99, 'Leo acusa a una mujer de haberle pegado en el colegio', 'declaracion_personaje',
     'Leo amenaza con contar a su madre que una mujer le pegó varias veces. Tesa cree primero que se escapó de los deberes y dice haberlo buscado por la taberna; él replica que estaba en el colegio, que una señora se llevó a su amigo y después le pegó. Ante las preguntas admite de forma evasiva haberla insultado y niega haber intentado robarla.',
     ['Leo', 'Tesara Queen', 'Colegio de Iktan'],
     'El amigo aparece como «Écil» en el VTT. El contexto anterior permite proponer un cotejo con Eztli, pero no asignar aquí inequívocamente ese nombre ni atribuir la agresión a Citlali. Es testimonio de Leo, no una repetición observada del incidente.', ['Leo', 'Tesara Queen'])
fact(106, 108, 128, 109, 'Leo entra en el colegio después de provocar a Tesa', 'hecho_confirmado',
     'Cuando Leo dice que Tesa parece vieja, ella declara que le da un golpe y él agacha las orejas. El niño insiste en que su madre castigará a las dos mujeres, hace un gesto insultante desde la puerta y sale corriendo hacia dentro cuando Tesa saca el látigo. Tesa queda libre para volver a la taberna.',
     ['Leo', 'Tesara Queen', 'Colegio de Iktan'],
     'No se fija el tipo o daño del golpe. Sacar el látigo no prueba que llegue a azotarlo. La frase sobre el tío Johnny pertenece al comentario de Tesa y no desarrolla una nueva historia familiar.', ['Leo', 'Tesara Queen'])
fact(107, 143, 165, 162, 'Angelique tolera a unos clientes nuevos porque pagan bien', 'declaracion_personaje',
     'La taberna de Iktan tiene un ambiente distinto y empieza a oler mal desde una esquina. Tesa pregunta a Angelique por los desconocidos allí sentados. La tabernera los llama nuevos y de mala calaña, pero añade que beben mucho y pagan bien.',
     ['Tesara Queen', 'Angelique', 'Iktan'],
     'No se identifica a esos clientes ni se demuestra que sean los piratas que ocuparon Shiaru. El juicio sobre su carácter es de Angelique.', ['Tesara Queen', 'Angelique'])
fact(108, 170, 244, 210, 'Una joya a cambio de la pista de unas ruinas junto al lago', 'declaracion_personaje',
     'Angelique diferencia unas ruinas junto al lago del antiguo barrio del pueblo que Tesa ya estudia. Para indicarle el camino pide algo bonito, en particular una joya. Tesa promete traerle alguna pieza resultona si la encuentra y le pide que luego le cuente su relación amorosa. Angelique se muestra posesiva respecto a ese hombre y aplaza la conversación.',
     ['Tesara Queen', 'Angelique', 'Ruinas de la orilla del lago de Iktan'],
     'El hombre no recibe nombre en este diálogo: el cortejo anterior no convierte estas palabras en una nueva identificación. La joya es un encargo condicional, sin hallazgo o entrega en este tramo.', ['Tesara Queen', 'Angelique'])
fact(109, 245, 272, 250, 'Angelique da a Tesa el camino hacia las ruinas', 'declaracion_personaje',
     'Angelique indica salir por la puerta norte, seguir el camino y girar a la derecha al ver tres calaveras de personas que, según dice, mataron la semana anterior. Advierte sobre los cocodrilos y sitúa las ruinas junto al lago. Tesa apunta las indicaciones en su libreto y parte.',
     ['Tesara Queen', 'Angelique', 'Iktan', 'Ruinas de la orilla del lago de Iktan'],
     'Es una ruta verbal, sin coordenadas. El segundo giro resulta impreciso en el VTT y la recapitulación de Tesa lo formula a la izquierda. Las tres muertes y su fecha son información atribuida a Angelique, sin identidad o autoría.', ['Tesara Queen', 'Angelique'])
fact(110, 290, 311, 296, 'Tesa encuentra unos muros escasos y empieza a estudiarlos', 'hecho_confirmado',
     'Tesa llega siguiendo las indicaciones en menos de una hora. Las ruinas son tres o cuatro muros caídos junto al lago. Pese a la decepción busca grabados, restos de columnas, estatuas o cualquier detalle que merezca estudio y permanece investigando.',
     ['Tesara Queen', 'Ruinas de la orilla del lago de Iktan'],
     'La enumeración de grabados y estatuas expresa lo que busca, no hallazgos ya adjudicados. No se identifica la cultura, antigüedad o función de los muros.', ['Tesara Queen'])
fact(111, 312, 350, 324, 'Tenta y Chopito salen por otro punto del lago', 'explicacion_director',
     'Tenta y Chopito emergen del agua cerca de las ruinas. El director recuerda que habían viajado a Perlasal por el lago y unos túneles sumergidos y aclara que el regreso los ha sacado por otra parte de la orilla. Tenta reconoce que no conoce el sitio y teme haberse equivocado de ruta; Chopito se acomoda después en el tarro.',
     ['Tentacol', 'Chopito', 'Perlasal', 'Ruinas de la orilla del lago de Iktan'],
     'El lago no recibe nombre en este bloque. La continuidad con el viaje anterior permite cotejarlo después, sin extender la identidad a todos los lagos de la campaña.', ['Tentacol', 'Chopito'])
fact(112, 327, 345, 339, 'Chopito prefiere repartir sus acólitos entre más lugares', 'declaracion_personaje',
     'Chopito convierte el desvío en una oportunidad: afirma que en Iktan, donde veneraban a una tortuga, ya consiguió algunos acólitos y que ahora conviene buscar otros sitios. Dice que pronto admirarán a un pulpo y propone investigar la jungla para extender sus seguidores.',
     ['Chopito', 'Tentacol', 'Iktan'],
     'Son ambiciones y afirmaciones de Chopito. No prueban la sustitución del culto de Iktan, el número de acólitos ni un poder divino real.', ['Chopito', 'Tentacol'])
fact(113, 352, 403, 401, 'Tesa baja la pistola ante Tenta y Chopito', 'hecho_confirmado',
     'Tesa oye un paso extraño, descubre a Tenta y la apunta con la pistola para preguntarle si es amiga o enemiga. Tenta presenta al pulpo del tarro como su señor y asegura que no será hostil si no se le opone. Tras bromear sobre el proselitismo y preguntar por su objetivo, Tesa baja el arma.',
     ['Tesara Queen', 'Tentacol', 'Chopito'],
     'El parecido con religiones del mundo real forma parte de la conversación humorística; no establece una organización de campaña con esos nombres. Bajar el arma no constituye conversión o juramento.', ['Tesara Queen', 'Tentacol', 'Chopito'])
fact(114, 421, 448, 427, 'Tesa entiende la conversación de Chopito en Aquan', 'hecho_confirmado',
     'Chopito habla a Tenta en Aquan y considera que Tesa, por no conocer más ciudades, sería un recipiente vacío para sus ideas. La jugadora aclara que Tesa entiende Aquan; el director confirma que ha comprendido las palabras. Chopito se sorprende y ordena a Tenta abrazarla como posible discípula.',
     ['Tesara Queen', 'Tentacol', 'Chopito'],
     'La comprensión del idioma sí se confirma; la condición de discípula solo la propone Chopito. El abrazo posterior no demuestra que Tesa la acepte.', ['Tesara Queen', 'Tentacol', 'Chopito'])
fact(115, 454, 497, 483, 'Patata aparece cubierto de barro y hojas', 'hecho_confirmado',
     'Mientras Tenta abraza a Tesa, ambas oyen agitación entre los matorrales. Chopito manda investigar y Tesa vuelve a sacar la pistola. De entre las hojas sale Patata, con barro y vegetación en la armadura; se disculpa por asustarlas y explica que lleva un tiempo huyendo de Shiaru.',
     ['Patata', 'Tesara Queen', 'Tentacol', 'Chopito', 'Shiaru'],
     'La descripción sugiere una marcha fatigosa, pero no fija el número de días ni una persecución activa hasta este punto de la jungla.', ['Patata', 'Tesara Queen', 'Tentacol', 'Chopito'])
fact(116, 521, 530, 526, 'Patata comunica que otros piratas tomaron Shiaru y destruyeron su casa', 'declaracion_personaje',
     'Patata explica a Tesa que Shiaru era un pueblo de piratas gobernado por Bonny, a quien describe como muy peligrosa. Dice que ahora parece muerta, que expulsaron a quienes vivían allí y que hay nuevos piratas. Atribuye su huida a la destrucción de su casa.',
     ['Patata', 'Tesara Queen', 'Tentacol', 'Chopito', 'Shiaru', '"Happy" Bonny', 'Granja de Patata'],
     'El cuerpo visto por Patata está respaldado por el director al inicio. La expulsión general, los ocupantes y la casa son aquí su relato: no se nombra a sus responsables ni se describe el estado de cada habitante o edificio.', ['Patata', 'Tesara Queen', 'Tentacol', 'Chopito'])
fact(117, 503, 546, 538, 'Patata conserva su propia fe y Tesa traduce a Chopito', 'declaracion_personaje',
     'Patata se presenta como clérigo que quiere repartir la palabra de su señor. Chopito le ofrece cobijo a cambio de obediencia; Patata responde que ya tiene su propia diosa. Cuando se aclara que no entiende las burbujas de Aquan, Tesa le traduce que el pulpo quiere ser su amigo, propuesta que acepta.',
     ['Patata', 'Tesara Queen', 'Tentacol', 'Chopito'],
     'El pasaje no da nombre a la diosa ni convierte la amistad en sumisión religiosa. La traducción amistosa de Tesa suaviza la condición de obediencia formulada por Chopito.', ['Patata', 'Tesara Queen', 'Tentacol', 'Chopito'])
fact(118, 547, 575, 556, 'Patata lava su armadura en el lago', 'hecho_confirmado',
     'Patata pregunta dónde puede limpiar la armadura y descansar. Tesa le sitúa Iktan a una hora y Tenta le ofrece el agua del lago del que acaba de salir. El director describe un lago enorme de agua transparente; Patata se acerca y empieza a refrescarse y limpiarse.',
     ['Patata', 'Tesara Queen', 'Tentacol', 'Ruinas de la orilla del lago de Iktan'],
     'La transparencia observada no constituye un análisis de potabilidad o ausencia de veneno. El lavado no identifica la armadura como el equipo confiscado en capítulos antiguos.', ['Patata', 'Tesara Queen', 'Tentacol'])
fact(119, 577, 650, 648, 'Un felino camuflado se presenta como Mlan', 'hecho_confirmado',
     'Tesa descubre entre los árboles una figura bien camuflada con ojos amarillos y le pide que se muestre. El felino sale disimulando como si solo pasara por allí, pregunta por qué están en territorio ajeno y declara que su gente vigila el lugar, aunque la madre tierra pertenece a todos. Se presenta con el nombre transcrito «Mlan».',
     ['Tesara Queen', 'Mlan', 'Ruinas de la orilla del lago de Iktan'],
     'Grafía provisional del nombre, sin audio cotejado. No se fija especie reglada, tribu, rango ni identidad con otro felino conocido. La vigilancia del lugar es declaración suya.', ['Tesara Queen', 'Mlan', 'Tentacol', 'Chopito'])
fact(120, 637, 650, 645, 'Mlan permite que Tesa estudie si no comete sacrilegio', 'declaracion_personaje',
     'Tesa pide permiso para terminar de revisar los muros y tomar sus apuntes antes de marcharse. Mlan acepta mientras no cometa ningún sacrilegio. Ella responde que respeta la historia.',
     ['Tesara Queen', 'Mlan', 'Ruinas de la orilla del lago de Iktan'],
     'El acuerdo expresa sus condiciones de convivencia, sin demostrar autoridad legal exclusiva sobre las ruinas, propiedad o una consagración histórica concreta.', ['Tesara Queen', 'Mlan', 'Tentacol', 'Chopito'])
fact(121, 675, 749, 712, 'El suelo de las ruinas empieza a moverse', 'hecho_confirmado',
     'Durante la conversación se oyen ruidos y las plantas y raíces de alrededor de las ruinas se mueven paulatinamente: unas penetran más en el suelo y otras salen. Patata saca escudo y martillo con forma de patata, Tesa prepara la pistola y Tenta se aparta para proteger a Chopito.',
     ['Tesara Queen', 'Patata', 'Patata Hammer', 'Tentacol', 'Chopito', 'Mlan', 'Ruinas de la orilla del lago de Iktan'],
     'Nadie obtiene una explicación arcana del fenómeno. Las bromas sobre que llegará un hombre topo no incorporan tal criatura a la escena.', ['Tesara Queen', 'Patata', 'Tentacol', 'Chopito', 'Mlan'])
fact(122, 753, 787, 785, 'Las raíces levantan cadáveres y mueven sus cuerpos', 'explicacion_director',
     'Las raíces abren el suelo y sacan manos y cadáveres enterrados. Al levantarse se distingue que las plantas han penetrado en cuerpos y restos humanos y los están moviendo. El director describe un grupo de zombis conducido por esas raíces.',
     ['Tesara Queen', 'Patata', 'Tentacol', 'Chopito', 'Mlan', 'Cadáveres movidos por raíces de las ruinas del lago', 'Ruinas de la orilla del lago de Iktan'],
     'No se identifican los muertos, su número total o el agente último que anima las plantas. El aspecto zombi no demuestra una resurrección personal ni que estos cuerpos sean los mismos del capítulo 40.', ['Tesara Queen', 'Patata', 'Tentacol', 'Chopito', 'Mlan'])
fact(123, 788, 795, 792, 'Chopito entinta el tarro ante los cadáveres', 'declaracion_personaje',
     'Durante la aparición de los muertos se declara que el frasco de Chopito se vuelve negro y que sale algo de tinta, en una reacción interpretada con humor en la mesa.',
     ['Chopito', 'Tentacol'],
     'Reacción de interpretación humorística, sin un efecto ofensivo, veneno o nueva capacidad adjudicados. No se deriva de ella una naturaleza sobrenatural adicional.')
fact(124, 799, 807, 804, 'Tesa advierte de un posible vínculo entre las plantas y el dragón verde', 'declaracion_personaje',
     'Tesa dice reconocer a medias estas criaturas por otra ocasión y avisa al grupo de que están controladas por una planta extraña. Añade que esa planta puede obedecer a un dragón verde y que este puede meterse en sus cabezas.',
     ['Tesara Queen', 'Patata', 'Tentacol', 'Chopito', 'Mlan', 'Dragón verde del bosque de Iktan', 'Cadáveres movidos por raíces de las ruinas del lago'],
     'La relación con el dragón se formula como posibilidad y recuerdo de Tesa. No aparece aquí el dragón ni se adjudica una intrusión mental actual. No se establece el nombre Clolgedranx por esta advertencia.', ['Tesara Queen', 'Patata', 'Tentacol', 'Chopito', 'Mlan'])
fact(125, 812, 849, 846, 'Mlan golpea con dos descargas y conserva la distancia', 'hecho_confirmado',
     'El primer turno anterior al de Tesa corresponde al felino recién presentado. Decide tantear al enemigo sin lanzarse de cerca y se adjudican impactos de sus dos descargas mágicas contra un zombi. Después mantiene una posición prudente.',
     ['Mlan', 'Cadáveres movidos por raíces de las ruinas del lago'],
     'La atribución se apoya en la continuidad de turnos y en el comentario de la mesa sobre el felino brujo. Las comparaciones jocosas con personajes de otras partidas no establecen parentescos ni identidades en Xoltacan. No se da por muerto al objetivo.', ['Tesara Queen', 'Patata', 'Tentacol', 'Chopito', 'Mlan'])
fact(126, 854, 887, 868, 'El disparo de Escupefuego provoca una salpicadura que hiere al grupo', 'hecho_confirmado',
     'Tesa prueba su pistola Escupefuego contra las plantas que recubren a los zombis. Impacta en uno más verde, del que salta una salpicadura. El director adjudica seis puntos de daño a los presentes y especifica que Chopito también los recibe. Se confirma el gasto de una carga de Escupefuego.',
     ['Tesara Queen', 'Escupefuego', 'Patata', 'Tentacol', 'Chopito', 'Mlan', 'Cadáveres movidos por raíces de las ruinas del lago'],
     'El director relaciona la adjudicación con una carta del chat: la carta pertenece al procedimiento de mesa, no a una persona o fuerza diegética. Las bromas sobre matar a Chopito no declaran que muera. No se identifica la composición de la salpicadura.', ['Tesara Queen', 'Patata', 'Tentacol', 'Chopito', 'Mlan'])
fact(127, 890, 907, 893, 'El fuego no hace daño extra y Tesa busca ocultarse', 'hecho_confirmado',
     'Tesa pregunta si el fuego de la pistola ha hecho daño adicional. El director responde que ha sido normal; ella descarta esa teoría y se mete entre los matorrales para evitar el peligro e intentar ocultarse. La tirada de sigilo recibe la aceptación del director.',
     ['Tesara Queen', 'Escupefuego', 'Cadáveres movidos por raíces de las ruinas del lago'],
     'No se establece una resistencia universal de todas las plantas o zombis al fuego. La escena solo resuelve este disparo y este intento de ocultación.', ['Tesara Queen', 'Patata', 'Tentacol', 'Chopito', 'Mlan'])
fact(128, 908, 947, 944, 'Tenta invoca un tentáculo de frío y retrocede', 'hecho_confirmado',
     'Tenta recurre al gran maestro Chopito y usa el Tentáculo de las profundidades. Tras resolver un problema de la herramienta de juego, coloca el tentáculo, ataca con él como acción adicional, declara daño de frío y retrocede.',
     ['Tentacol', 'Chopito', 'Cadáveres movidos por raíces de las ruinas del lago'],
     'El fallo del botón es un problema de interfaz y no una pérdida de poderes del personaje. La comparación con un arma espiritual es comentario de la mesa, sin cambiar el nombre de la capacidad. El VTT no precisa aquí una cifra de daño.', ['Tesara Queen', 'Patata', 'Tentacol', 'Chopito', 'Mlan'])
fact(129, 948, 972, 963, 'Las descargas de Tenta empujan y ralentizan', 'hecho_confirmado',
     'Después del tentáculo, Tenta lanza dos descargas. Se adjudican ambos impactos y desplazamientos de diez pies. Declara también una reducción de diez pies de movimiento y recuerda la ralentización del tentáculo. El director aclara que Chopito se desplaza con Tenta y no tiene un turno separado.',
     ['Tentacol', 'Chopito', 'Cadáveres movidos por raíces de las ruinas del lago'],
     'No se calcula una suma definitiva de todas las reducciones de velocidad ni se atribuye cada efecto a todos los enemigos. El tablero no se reconstruye a partir de deícticos como «aquí».', ['Tesara Queen', 'Patata', 'Tentacol', 'Chopito', 'Mlan'])
fact(130, 973, 1004, 995, 'El aura de un zombi envenena a Patata e impide que se cure', 'hecho_confirmado',
     'Un zombi avanza hacia Patata y emplea su acción para acercarse con su aura apestosa. Antes de que Patata se mueva debe superar una salvación de Constitución; obtiene diez y falla. El director lo declara envenenado e incapaz de recuperar puntos de vida hasta el final de su siguiente turno.',
     ['Patata', 'Cadáveres movidos por raíces de las ruinas del lago'],
     'La duración citada corresponde a la imposibilidad de recuperar vida; no se extrapola a una secuela permanente. El bloque no llega a resolver la recuperación posterior de Patata.', ['Patata', 'Tesara Queen', 'Tentacol', 'Chopito', 'Mlan'])
fact(131, 1007, 1024, 1011, 'Patata atemoriza a casi todos los no muertos', 'hecho_confirmado',
     'Patata elige una capacidad cuyo nombre queda transcrito de forma defectuosa como «trundez», coherente con la expulsión de no muertos que se resuelve a continuación. El director dice que todos menos uno empiezan a asustarse. Se revisa el alcance del efecto sobre enemigos fuera de la vista y se acepta que puedan oírlo.',
     ['Patata', 'Cadáveres movidos por raíces de las ruinas del lago'],
     'No se reconstruyen todas las tiradas individuales ni la posición de cada esqueleto: la frase siguiente del VTT sobre quién ha fallado es imprecisa. No se afirma todavía la huida efectiva o destrucción de los afectados.', ['Patata', 'Tesara Queen', 'Tentacol', 'Chopito', 'Mlan'])
fact(132, 1025, 1027, 1027, 'Patata impacta con un ataque de nivel tres al final del tramo', 'hecho_confirmado',
     'Al cerrar este bloque, Patata anuncia un lanzamiento de nivel tres y un ataque. El director confirma que impacta; el combate continúa fuera del corte de lectura.',
     ['Patata', 'Cadáveres movidos por raíces de las ruinas del lago'],
     'El nombre del conjuro y su daño no resultan legibles en estos tres segmentos. Tampoco se adjudica aquí la muerte del objetivo ni el desenlace de la batalla.', ['Patata', 'Tesara Queen', 'Tentacol', 'Chopito', 'Mlan'])

stages = [
    {'titulo': 'Lo que queda de Shiaru y los caminos pendientes', 'referencias': ['47-101', '47-102', '47-103'],
     'texto': 'Patata ya no tiene el refugio que había cultivado en Shiaru. El director concreta que, al volver en uno de sus viajes, encontró el huerto destrozado y el cuerpo de «Happy» Bonny colgado de la entrada. Da media vuelta hacia la jungla, sin un destino claro. En otro frente, Tesa sigue cuidando a Leo mientras intenta atender el encargo de los elfos sobre el dragón. Tenta y Chopito, por su parte, han salido de Perlasal en busca de más seguidores para el pulpo. La jugadora sitúa su avance hacia Iktan; el director aclara que aún no han llegado.'},
    {'titulo': 'Tesa deja a Leo en el colegio', 'referencias': ['47-104', '47-105', '47-106'],
     'texto': 'Tesa lleva a Leo de la mano al colegio de Iktan y se lamenta de que su madre lleve varios días sin hacerse cargo de él. El niño quiere denunciarle que una mujer lo golpeó y que Tesa no lo defendió. Ella recuerda haberlo dejado haciendo los deberes y haberlo buscado por la taberna; Leo insiste en que estaba en el colegio, donde la señora se llevó a su amigo antes de pegarle. No da una identificación inequívoca de ninguno de los dos en esta conversación. La disputa empeora cuando llama vieja a Tesa: ella le da un golpe, él agacha las orejas y vuelve a amenazar con la llegada de su madre. Desde la puerta todavía le dedica un gesto insultante. Tesa saca el látigo y Leo corre hacia dentro. Por fin puede dejarlo e intentar disfrutar de una mañana tranquila.'},
    {'titulo': 'Angelique ofrece unas ruinas y pide una joya', 'referencias': ['47-107', '47-108', '47-109', '47-110'],
     'texto': 'La tranquilidad de la taberna trae un olor desagradable desde una mesa de desconocidos. Angelique reconoce que parecen de mala calaña, pero le compensa lo que beben y pagan. La charla acaba llevando a las notas históricas de Tesa y a unas ruinas cercanas al lago, distintas del barrio antiguo que ya conoce. Tesa pregunta cómo llegar. Angelique quiere una joya bonita a cambio; ella promete buscar algo si lo encuentra y pide que después le cuente quién es ese hombre por el que se muestra tan posesiva. El nombre no sale. Tesa apunta una ruta que parte por la puerta norte, pasa por tres calaveras y exige cuidado con los cocodrilos. En menos de una hora alcanza el lago, pero las supuestas ruinas resultan ser tres o cuatro muros caídos. Aun decepcionada, busca grabados, columnas o estatuas y se queda estudiando el lugar.'},
    {'titulo': 'Tenta y Chopito salen del agua', 'referencias': ['47-111', '47-112', '47-113', '47-114'],
     'texto': 'Tenta y Chopito emergen del lago por un punto distinto de aquel por el que iniciaron el trayecto sumergido a Perlasal. Tenta teme haber confundido la ruta. Chopito lo considera una oportunidad: sostiene que Iktan ya tiene algunos acólitos suyos y que ahora les conviene repartir seguidores entre más lugares. Se instala en el tarro y manda explorar. Tesa oye su paso húmedo, se vuelve y apunta a la recién llegada. Quiere saber si son hostiles; Tenta presenta al pulpo como su señor y no ofrece enemistad mientras no se le opongan. Tesa termina bajando la pistola y le indica el camino de Iktan, pero Tenta busca nuevos territorios. Chopito comenta en Aquan que la ignorancia de la humana deja sitio para sus ideas. La sorpresa es suya cuando Tesa revela que entiende el idioma y el director confirma la comprensión. Lejos de desistir, la toma por una posible discípula y ordena a Tenta abrazarla. Ella la abraza y Tesa intenta apartarse con delicadeza, sin aceptar ninguna conversión.'},
    {'titulo': 'Patata pide agua y cuenta la caída de su casa', 'referencias': ['47-115', '47-116', '47-117', '47-118'],
     'texto': 'Un movimiento entre los matorrales interrumpe el abrazo. Chopito exige que investiguen y Tesa vuelve a empuñar la pistola. Aparece Patata cubierto de barro y hojas en la armadura. Se disculpa por el susto y se presenta como clérigo. Al explicar por qué huye de Shiaru, cuenta que Bonny parece muerta, que unos nuevos piratas expulsaron a sus habitantes y que le destruyeron la casa. Tesa se compadece. Chopito ofrece cobijo bajo su obediencia, pero Patata ya tiene su propia diosa. Además, no entiende Aquan: Tesa le traduce que el pulpo quiere ser su amigo y él acepta esa amistad. Lo que necesita de inmediato es limpiarse y descansar. Le indican que Iktan está a una hora; mientras tanto se acerca al lago de agua transparente para lavarse la armadura.'},
    {'titulo': 'El vigilante de ojos amarillos', 'referencias': ['47-119', '47-120'],
     'texto': 'Tesa distingue otra presencia, esta vez bien escondida entre los árboles: unos ojos amarillos la observan. La llama antes de tener que sacar otra vez el arma. El felino sale como si solo estuviera de paso y reprocha al grupo que ocupe territorio ajeno. Cuando Tesa pregunta si las ruinas son suyas, responde que la madre tierra pertenece a todos y que su gente se limita a vigilarla. Su nombre queda como «Mlan» en la transcripción. Tesa pide terminar los apuntes y promete marcharse; él lo permite mientras no cometa sacrilegio. Patata concluye el lavado y recibe indicaciones para llegar a Iktan. La conversación sobre quién resulta más extraño sirve de tregua breve entre los viajeros.'},
    {'titulo': 'Los cadáveres que levantan las raíces', 'referencias': ['47-121', '47-122', '47-123', '47-124'],
     'texto': 'El suelo interrumpe la tregua. Las raíces se hunden o afloran lentamente alrededor de los muros, como si la tierra cobrara vida. Patata prepara el escudo y su martillo con forma de patata; Tesa echa mano de la pistola y Tenta retrocede protegiendo a Chopito, que insiste en ser quien da las órdenes. Las bromas de la mesa sobre hombres topo no se materializan. Lo que sale del suelo son manos y cadáveres: las plantas han penetrado en los restos y los levantan y manejan. Los muertos se vuelven hacia los presentes mientras el frasco de Chopito se oscurece de tinta en una reacción humorística. Tesa cree reconocer el peligro y advierte que los controla una planta extraña; añade que puede obedecer a un dragón verde capaz de entrar en sus cabezas. Es su advertencia, sin aparición del dragón ni ataque mental demostrado en ese instante.'},
    {'titulo': 'El fuego no resuelve el avance', 'referencias': ['47-125', '47-126', '47-127', '47-128', '47-129', '47-130', '47-131', '47-132'],
     'texto': 'Mlan tantea la amenaza desde lejos y golpea con dos descargas. Tesa prueba Escupefuego contra la vegetación que recubre a los zombis. Acierta a uno más verde y una salpicadura hiere a los presentes: el director fija seis puntos de daño y recuerda expresamente a Chopito. La adjudicación se vincula a una carta del chat, sin convertirla en una fuerza del mundo. La carga de la pistola se consume y el fuego hace daño normal; Tesa abandona esa teoría y busca cubrirse entre los matorrales. Tenta invoca el Tentáculo de las profundidades, ataca con frío y se retira. Después impacta con dos descargas que empujan, y se comentan las reducciones de movimiento de sus ataques. Un zombi, sin embargo, se acerca a Patata con un aura apestosa. El clérigo falla la salvación de Constitución y queda envenenado, sin poder recuperar vida hasta el final de su siguiente turno. Responde con una capacidad de expulsión de no muertos: todos menos uno muestran temor, aunque aún no se representa su retirada. Su siguiente ataque, anunciado a nivel tres, impacta justo cuando termina el tramo. La batalla sigue abierta en el corte.'},
]


def history(name, kind, description, note, title, text, refs, new=False):
    return {'nombre': name, 'tipo': kind, 'nueva': new, 'descripcion': description, 'nota': note,
            'etapas': [{'titulo': title, 'texto': text, 'referencias': refs}]}


histories = [
    history('Patata', 'personaje', 'Agricultor y clérigo que pierde su casa y huerto de Shiaru.',
            'Patatamán y las variantes del VTT se normalizan a la identidad ya catalogada; no se asigna nombre a su diosa.',
            'Del huerto destruido a los cadáveres del lago',
            'Vuelve a Shiaru y encuentra su huerto arrasado y el cuerpo de Bonny colgado de la entrada. Huye hacia la jungla y llega embarrado a las ruinas del lago, donde cuenta a Tesa la expulsión por nuevos piratas y la destrucción de su casa. Acepta la amistad con Chopito pero conserva su propia fe. Después de lavar la armadura, prepara sus armas contra los cadáveres movidos por raíces. El aura de uno lo envenena y le impide recuperar vida durante el intervalo adjudicado. Su expulsión atemoriza a casi todos los enemigos y su siguiente ataque impacta antes del corte.',
            ['47-101', '47-115', '47-116', '47-117', '47-118', '47-121', '47-130', '47-131', '47-132']),
    history('Tesara Queen', 'personaje', 'Historiadora de Puerto de Espadas, llamada Tesa, que cuida temporalmente a Leo.',
            'Se usa la identidad configurada Tesara Queen, sin crear otra persona por Tesa o los errores César/Tesam del VTT.',
            'Una mañana de estudios que acaba en combate',
            'Tesa alterna la investigación del dragón con el cuidado de Leo, del que se queja al llevarlo al colegio. Acuerda con Angelique buscar una joya y va a estudiar unas ruinas junto al lago. Su cautela la hace apuntar a los recién llegados, pero baja el arma al hablar con Tenta y Chopito. Revela que entiende Aquan y comprende los planes de conversión del pulpo sin aceptarlos. Se compadece de Patata, pide permiso al vigilante Mlan y vuelve a sus apuntes. Cuando se alzan los muertos advierte de un posible vínculo de las plantas con el dragón verde. Su prueba de fuego no hace daño extra, provoca la salpicadura adjudicada y termina buscando sigilo.',
            ['47-102', '47-104', '47-105', '47-106', '47-108', '47-110', '47-113', '47-114', '47-116', '47-120', '47-124', '47-126', '47-127']),
    history('Leo', 'personaje', 'Niño harengon a cargo de Tesa mientras espera a su madre.',
            'La madre invocada no se nombra en este tramo; mantener su continuidad familiar según las fuentes previas. El amigo «Écil» requiere cotejo con Eztli.',
            'Una queja que no consigue la defensa de Tesa',
            'Leo acusa a una mujer de haberle pegado en el colegio después de llevarse a su amigo. También reprocha a Tesa que no lo protegiera y amenaza con contárselo a su madre. Tesa duda de su conducta y él responde con una burla sobre su edad. Tras recibir un golpe, agacha las orejas pero todavía se despide con un gesto insultante. Corre al interior del colegio cuando ella saca el látigo.',
            ['47-104', '47-105', '47-106']),
    history('Angelique', 'personaje', 'Encargada de la taberna de Iktan que proporciona a Tesa el camino de unas ruinas.',
            'Conservar la continuidad editorial ya establecida de Angelique; este diálogo no identifica por nombre a su hombre.',
            'Una indicación a cambio de algo bonito',
            'Acepta a unos clientes nuevos por lo mucho que consumen y pagan, pese al juicio negativo sobre ellos. Sugiere a Tesa salir a otras ruinas junto al lago y pide una joya bonita a cambio de indicarle el camino. Su actitud posesiva despierta la curiosidad de la historiadora; acuerdan hablar luego. Le da una ruta desde la puerta norte, con las calaveras y los cocodrilos como referencias, y vuelve a sus asuntos.',
            ['47-107', '47-108', '47-109']),
    history('Tentacol', 'personaje', 'Viajera acuática llamada Tenta en el diálogo, compañera y devota de Chopito.',
            'Se mantiene Tentacol como identidad catalogada; el diálogo usa femenino, sin fijar especie reglada.',
            'Un camino desviado que trae nuevos compañeros',
            'Sale de Perlasal con Chopito buscando más lugares para sus seguidores y emerge por una orilla distinta de la esperada. Ante Tesa defiende la autoridad de su señor y obedece la orden de abrazarla como posible discípula. Participa en el encuentro con Patata y protege el tarro cuando el suelo se mueve. En combate coloca el Tentáculo de las profundidades, declara daño de frío y añade dos descargas que empujan a los adversarios y reducen su movilidad.',
            ['47-103', '47-111', '47-112', '47-113', '47-114', '47-115', '47-121', '47-128', '47-129']),
    history('Chopito', 'personaje', 'Pulpo transportado por Tenta en un tarro, con ambiciones de ampliar su culto.',
            'Ni sus títulos de señor y maestro ni los supuestos acólitos prueban divinidad o mando sobre una facción identificada.',
            'Dos intentos de reclutamiento y seis puntos de daño',
            'Prefiere buscar seguidores en más lugares antes que concentrarlos en Iktan. Intenta aprovechar la supuesta ignorancia de Tesa, pero descubre que entiende sus comentarios en Aquan. Ordena a Tenta abrazarla y más tarde ofrece cobijo a Patata bajo obediencia, sin conseguir una conversión. Ante el despertar de los muertos su tarro se oscurece de tinta en una reacción humorística. También recibe los seis puntos de daño de la salpicadura. Su acompañamiento no le concede un turno independiente del de Tenta.',
            ['47-112', '47-114', '47-117', '47-123', '47-126', '47-129']),
    history('Mlan', 'personaje', 'Felino de ojos amarillos que vigila las ruinas y combate con descargas mágicas.',
            'Nombre provisional «Mlan» según c001297 y c001303. No se asigna una tribu ni se fusiona con otros felinos.',
            'El vigilante se queda a combatir',
            'Observa camuflado al grupo antes de que Tesa lo descubra. Sale fingiendo que solo pasaba y pregunta por su presencia en territorio ajeno. Dice que su gente vigila el lugar y permite la investigación mientras no haya sacrilegio. Cuando las raíces sacan cadáveres decide tantearlos desde la distancia y acierta dos descargas, sin que este tramo muestre la destrucción del objetivo.',
            ['47-119', '47-120', '47-125'], True),
    history('"Happy" Bonny', 'personaje', 'Dirigente pirata cuyo cuerpo encuentra Patata colgado en la entrada de Shiaru.',
            'Se aplica la grafía corregida por el usuario; la cita conserva Bonnie. El bloque no representa cómo murió ni quién colgó el cuerpo.',
            'El cuerpo expuesto en Shiaru',
            'La concreción inicial del director añade el hallazgo de Patata al destino de Bonny: al regresar encuentra su cuerpo colgado de la entrada del poblado. Patata transmite luego a Tesa que la antigua gobernante parece muerta y que otros piratas ocupan Shiaru. La información amplía las consecuencias de su caída, sin identificar ejecutores o resolver deudas pendientes.',
            ['47-101', '47-116']),
    history('Shiaru', 'lugar', 'Poblado costero que Patata encuentra bajo el dominio de nuevos piratas.',
            'La situación general procede del relato de Patata; no se adjudica el destino de cada antiguo habitante.',
            'Un regreso sin hogar',
            'La vuelta de Patata muestra el huerto destrozado y a Bonny colgada en la entrada. Él cuenta después que nuevos piratas expulsaron a quienes vivían allí y que destruyeron su casa, motivo de su marcha a la jungla. El pasaje no establece quién gobierna ahora, cómo se repartió el poder ni qué edificios continúan en pie.',
            ['47-101', '47-116']),
    history('Granja de Patata', 'lugar', 'Casa y cultivo de Patata en el entorno de Shiaru.',
            'Mantener la identidad ya catalogada del asentamiento de Patata. El estado del huerto está confirmado por el director y el de la casa relatado por su dueño.',
            'El cultivo perdido',
            'Patata encuentra el huerto totalmente destrozado durante su regreso a Shiaru. Más tarde cuenta que huyó después de que los nuevos ocupantes destruyeran su casa. Su búsqueda inmediata de agua y descanso expresa la pérdida de su refugio, sin que se acuerde todavía reconstruirlo o recuperarlo.',
            ['47-101', '47-116', '47-118']),
    history('Colegio de Iktan', 'lugar', 'Colegio al que Tesa lleva a Leo durante el cuidado temporal del niño.',
            'No se equipara automáticamente con la academia de guerreros ni se identifica aquí al personal docente.',
            'Un nuevo día para Leo',
            'Tesa deja a Leo en su puerta mientras él se queja de una agresión anterior ocurrida, según su versión, allí mismo. Tras una disputa y un gesto insultante, el niño entra corriendo cuando ella saca el látigo. La llegada permite a Tesa dedicar tiempo a sus propios estudios.',
            ['47-104', '47-105', '47-106']),
    history('Ruinas de la orilla del lago de Iktan', 'lugar', 'Tres o cuatro muros caídos junto al lago al que llega Tesa desde la puerta norte de Iktan.',
            'Nombre editorial descriptivo. No fusionar con el barrio antiguo, las ruinas del nido del capítulo 7, el templo de los nawals o el claro del capítulo 40 sin cotejo adicional.',
            'Un lugar de estudio que oculta cadáveres',
            'Angelique indica a Tesa cómo llegar a unas ruinas diferentes del barrio que ya ha estudiado. El trayecto tarda menos de una hora y concluye ante pocos muros. Allí coinciden la historiadora, Tenta y Chopito, Patata y el vigilante Mlan. La investigación queda interrumpida cuando las raíces se mueven, abren el suelo y extraen cadáveres que pasan a manejar. Su origen y su relación exacta con el dragón quedan abiertos en este bloque.',
            ['47-108', '47-109', '47-110', '47-111', '47-115', '47-119', '47-120', '47-121', '47-122', '47-124'], True),
    history('Cadáveres movidos por raíces de las ruinas del lago', 'personaje', 'Grupo de cuerpos y restos levantados y movidos por plantas en las ruinas.',
            'Ficha colectiva descriptiva de los adversarios presentes, sin convertir el fenómeno en una facción ni identificar estos cuerpos con otros no muertos anteriores.',
            'Raíces, salpicaduras y un aura de veneno',
            'Las raíces extraen los restos enterrados y los mueven desde dentro. Uno de los zombis más verdes salpica cuando Tesa le dispara y el daño alcanza al grupo y a Chopito; el fuego de ese disparo no produce daño extra. Otro se acerca a Patata con un aura apestosa, lo envenena y bloquea temporalmente su curación. La respuesta de expulsión hace temer a casi todos y el combate continúa al corte.',
            ['47-122', '47-126', '47-127', '47-130', '47-131', '47-132'], True),
    history('Dragón verde del bosque de Iktan', 'personaje', 'Dragón que Tesa relaciona de forma posible con las plantas que manejan a los muertos.',
            'Conservar separado de Clolgedranx hasta evidencia explícita. La advertencia no certifica su presencia o control actual.',
            'La explicación que teme Tesa',
            'El encargo de los elfos sigue ocupando los ratos libres de Tesa. Al reconocer parcialmente el comportamiento de los cadáveres, advierte que las plantas podrían obedecer a un dragón verde capaz de entrar en sus cabezas. El grupo no lo ve ni recibe una intrusión mental adjudicada durante este tramo.',
            ['47-102', '47-124']),
    history('Escupefuego', 'objeto', 'Pistola de Tesa con una carga de fuego utilizada contra un zombi cubierto de plantas.',
            'Nombre tomado de la declaración repetida en la escena. No se fija daño total, capacidad de cargas ni poderes fuera del uso observado.',
            'Una prueba de fuego sin ventaja',
            'Tesa la elige por la vegetación de los enemigos. El disparo impacta, consume una carga y hace daño normal, sin confirmar la vulnerabilidad al fuego que ella esperaba. Del zombi alcanzado salta la salpicadura que el director adjudica a todos, incluida la mención expresa de Chopito.',
            ['47-126', '47-127'], True),
    history('Patata Hammer', 'objeto', 'Martillo de Patata con forma de patata.',
            'Identificación contextual con el arma ya catalogada; su nombre propio no se vuelve a pronunciar aquí.',
            'Preparado ante el movimiento del suelo',
            'Patata lo saca junto con el escudo cuando las raíces empiezan a moverse alrededor de las ruinas. Esta preparación confirma su uso como equipo actual, sin resolver el inventario de los objetos que perdió en antiguos cautiverios.',
            ['47-121']),
    history('Piratas ocupantes de Shiaru', 'faccion', 'Nuevos piratas a los que Patata atribuye la ocupación del poblado y la expulsión de habitantes.',
            'Denominación colectiva descriptiva basada solo en su testimonio. No se identifica capitán, bandera, alianza ni relación con los clientes nuevos de Iktan.',
            'Los ocupantes vistos a través de la huida de Patata',
            'Patata cuenta que, después de la caída de Bonny, hay otros piratas en Shiaru y que echaron a quienes estaban allí. Incluye la destrucción de su casa entre las razones por las que salió corriendo. El pasaje no permite repartir esas acciones entre individuos concretos o atribuirlas a todos los presentes en el ataque anterior.',
            ['47-116'], True),
]

missions = [
    'Investigar el dragón por encargo de los elfos: Tesa lo mantiene como objetivo y recuerda un posible vínculo de las plantas con un dragón verde; estudiar los muros no produce todavía un hallazgo arqueológico o una localización nueva del dragón en este bloque (47-102, 47-110, 47-124).',
    'Cuidar a Leo mientras regresa su madre: Tesa lo lleva al colegio y lo deja dentro, pero la madre sigue ausente en esta escena y no se resuelve el cuidado posterior (47-104–47-106).',
    'Conseguir una joya para Angelique: Tesa acepta de forma condicional traer algo bonito si lo encuentra a cambio de la ruta a las ruinas; el bloque termina sin hallazgo o entrega adjudicados (47-108–47-110).',
    'Ampliar los seguidores de Chopito: Tenta y el pulpo exploran nuevos lugares; los acercamientos a Tesa y Patata no prueban conversiones, y Patata mantiene su diosa (47-103, 47-112–47-114, 47-117).',
    'Encontrar descanso después de huir de Shiaru: Patata consigue agua para lavarse y recibe indicaciones hacia Iktan, pero el combate le impide completar aquí la llegada o acordar refugio (47-115–47-118, 47-130).',
    'Superar a los cadáveres de las raíces: se inicia el combate y Patata logra atemorizar a casi todos, pero la amenaza continúa al corte de las 00:45:28.990 (47-121–47-132).',
]
new_tracking = [
    {'id': 'P47-101', 'pregunta': '¿Quién manda a las raíces que sacan y mueven los cadáveres? ¿Obedecen ahora al dragón verde que menciona Tesa?', 'estado': 'pendiente', 'respuesta': 'El director confirma que las plantas mueven los cuerpos. El vínculo con el dragón es la posibilidad expresada por Tesa, sin presencia o control actual demostrados en este bloque.', 'referencias': ['47-122', '47-124'], 'pendiente': 'Agente último, propósito del despertar y relación causal probada con el dragón.'},
    {'id': 'P47-102', 'pregunta': '¿Quién es Mlan y qué gente vigila con él las ruinas del lago?', 'estado': 'parcial', 'respuesta': 'Se presenta con ese nombre provisional, afirma que su gente vigila el lugar y permite a Tesa estudiar sin sacrilegio. Combate con dos descargas.', 'referencias': ['47-119', '47-120', '47-125'], 'pendiente': 'Grafía confirmada, pueblo o afiliación e historia de la vigilancia.'},
    {'id': 'P47-103', 'pregunta': '¿Quién colgó el cuerpo de Bonny en la entrada de Shiaru y quiénes son sus nuevos ocupantes?', 'estado': 'parcial', 'respuesta': 'El director confirma que Patata vio el cuerpo colgado; Patata habla de nuevos piratas y de expulsión de habitantes. No identifica al responsable de cada acción.', 'referencias': ['47-101', '47-116'], 'pendiente': 'Autoría de la exhibición del cuerpo, identidad y mando de los ocupantes y destino individual de los desplazados.'},
    {'id': 'P47-104', 'pregunta': '¿Encontrará Tesa la joya prometida a Angelique y qué le contará la tabernera sobre su relación?', 'estado': 'pendiente', 'respuesta': 'Pactan que Tesa llevará alguna pieza bonita si la encuentra y aplazan la charla amorosa.', 'referencias': ['47-108', '47-109'], 'pendiente': 'Hallazgo, entrega y conversación posterior; no declarar fracaso por el corte de este bloque.'},
    {'id': 'P47-105', 'pregunta': '¿Qué estudiará Tesa en estas ruinas y a qué cultura o función pertenecen los muros?', 'estado': 'pendiente', 'respuesta': 'Llega a tres o cuatro muros caídos y busca inscripciones o restos significativos. El encuentro y el combate interrumpen la escena antes de un hallazgo identificado.', 'referencias': ['47-110', '47-119', '47-122'], 'pendiente': 'Resultados concretos, contexto histórico e identificación del lugar sin mezclar ruinas anteriores.'},
    {'id': 'P47-106', 'pregunta': '¿Conseguirán vencer a los muertos de las raíces y recuperará Patata su capacidad de curarse?', 'estado': 'pendiente', 'respuesta': 'Patata queda envenenado y con bloqueo temporal de recuperación de vida, atemoriza a casi todos los no muertos e impacta después con un ataque de nivel tres. La batalla continúa fuera del bloque.', 'referencias': ['47-130', '47-131', '47-132'], 'pendiente': 'Desenlace del combate, bajas, botín y recuperación de Patata, a integrar con el bloque siguiente.'},
]

# Cotejo individual tras la lectura completa de las 94 preguntas asignadas.
observations = {
    'P01-001': 'Ione y su noche de las cadenas no se reconstruyen en este bloque.',
    'P01-002': 'Las ruinas nuevas no aportan símbolos del mapa de Nox ni de aquella armadura.',
    'P01-003': 'El cuerpo expuesto es el de Bonny; no se tratan las muertes anteriores de los hijos de Citlali.',
    'P01-004': 'Los muros junto al lago no se identifican como las pirámides de oro de la leyenda.',
    'P01-005': 'No se habla de la familia, reliquia o reparación de Aerendriel.',
    'P01-006': 'El dragón de la advertencia es el verde del bosque, no el dragoncito de Aerendriel. La corrección de nombre Zarynth es contexto del usuario y no evidencia nueva de este bloque.',
    'P01-007': 'La exposición del cuerpo de Bonny y la ocupación de Shiaru añaden contexto a su caída, pero no cifran deudas, descuentos o liquidaciones.',
    'P01-008': 'Los días que Tesa lleva con Leo no fechan el accidente inicial de Ione.',
    'P02-001': 'No se reconstruyen el camarote, las cadenas rotas o el recorrido de Ione.',
    'P02-002': 'La muerte de Bonny no identifica al autor del antiguo zarpazo de Nox ni su enfado de entonces.',
    'P02-003': 'La gente de Mlan no recibe nombre o relación con la masacre de la tribu de Chochi.',
    'P02-004': 'No se mencionan la tribu adoptiva o la expulsión de Ayoto.',
    'P02-005': 'Los cadáveres actuales no se identifican con aquella emboscada y no aparece ese dinosaurio.',
    'P02-006': 'El bloque no detalla el antiguo encargo nocturno de Nox a Ayoto.',
    'P02-007': 'No se retoma el pulso, la liquidación de monedas o el reclutamiento de sus participantes.',
    'P03-001': 'La investigación de Tesa en unos muros no se vincula a la excavación de la Marina.',
    'P03-002': 'Las raíces que mueven muertos no explican el bosque ni el tránsito de Bling desde el plano feérico.',
    'P03-003': 'No se desarrolla el origen, control o cura de la licantropía de Ione.',
    'P03-004': 'No aparece Jack ni se modifica su destino ya documentado; no identificarlo con nuevos desconocidos.',
    'P03-005': 'El nombre provisional de Mlan y las ruinas no aportan el importe o acusación del cartel de Nox.',
    'P03-006': 'No se representa un juramento o incorporación de Poncelot.',
    'P03-007': 'Las bromas sobre animales o comida no identifican la especie o madre de Merlucilla I.',
    'P04-001': 'El hallazgo del cuerpo de Bonny no explica su antigua prohibición de hablar con Nox o su saber sobre gemas.',
    'P04-002': 'La joya solicitada por Angelique no se identifica como el collar antiguo de las minas.',
    'P04-003': 'El encargo de una joya nueva no retoma el inventario ni las entregas de aquellas gemas.',
    'P04-004': 'Las pretensiones religiosas de Chopito no identifican a la presencia que habló a Citlali sobre el equilibrio.',
    'P04-005': 'No hay intervención de Jack ni información nueva sobre su antiguo cautiverio.',
    'P04-006': 'Poncelot no conoce o reacciona aquí a la muerte de Merlucilla I.',
    'P04-007': 'No aparece o se identifica el pergamino mágico tomado del pirata.',
    'P04-008': 'No se revisa la duración de la segunda cola ni los efectos de frutas del capítulo 4.',
    'P05-001': 'La ocupación de Shiaru no revela cláusulas, copias o consecuencias jurídicas del contrato Bonny–Molly.',
    'P05-002': 'No se recupera la nota de Nox ni se confirma su lectura por Molly.',
    'P05-003': 'Las noticias actuales de Shiaru no dan el balance de supervivientes del buque incendiado.',
    'P05-004': 'La caída de Bonny aporta contexto posterior, pero no fija deuda o trabajo anunciado a Kilzer.',
    'P05-005': 'No se muestran Jack, Lucy o los cobros de Puerto de Espadas.',
    'P05-006': 'El libreto de indicaciones de Tesa es otro documento; no se leen los mapas de Aerendriel.',
    'P05-007': 'No se reconstruye la historia amorosa de Nox y Molly; la charla de Angelique es otra relación.',
    'P05-008': 'No se explica el nombre de familia ni el uso alterno de Aerendriel y Salazor.',
    'P06-001': 'El envenenamiento actual de Patata no diagnostica el contagio de Axi tras el mordisco.',
    'P06-002': 'No se representa otro retorno de Ione o se modifica la recuperación ya documentada.',
    'P06-003': 'El daño y veneno de Patata no completan las antiguas consultas de Chochi y Kilzer.',
    'P06-004': 'La joya pedida por Angelique no concilia las monedas del huevo ni el reparto de perlas.',
    'P06-005': 'Los nuevos piratas de Shiaru no se identifican con captores de Bling o presos de Poncelot.',
    'P06-006': 'No se representa la recuperación o devolución del lote de gemas reclamado por Bonny.',
    'P06-007': 'Patata no da nombre o bandera a los ocupantes, por lo que no se atribuyen a Elger Banana.',
    'P06-008': 'Tenta procede del agua, pero no es Marina ni revela el hechizo que reducía a la sirena.',
    'P06-009': 'No se comunica a Poncelot la muerte de su primera Merlucilla.',
    'P07-001': 'La advertencia sobre entrar en cabezas no descifra el mapa o tatuajes de Nox.',
    'P07-002': 'El amigo «Écil» del relato de Leo no fija especie, precio o conocimiento del pacto sobre Eztli.',
    'P07-003': 'El cuerpo de Bonny añade una consecuencia posterior de su caída, sin mostrar que ejecutara aquella amenaza por la cría.',
    'P07-004': 'No se identifica a la pirata pequeña fugitiva con ningún personaje de este encuentro.',
    'P07-005': 'No se retoma el cautivo del nido ni un interrogatorio suyo.',
    'P07-006': 'Los muros que estudia Tesa son nuevas ruinas descriptivas, sin conexión probada con la copia de símbolos del nido.',
    'P07-007': 'La destrucción de casa y huerto de Patata es otro episodio y no identifica al autor del antiguo hurto de herramientas.',
    'P07-008': 'Chopito es el pulpo actual; ninguna de sus bromas identifica la montura que comió otro pulpo.',
    'P07-009': 'No se explica el origen del alias Nox ni de su título de capitán.',
    'P08-001': 'El nuevo felino no se identifica con la mujer nawal muerta del templo.',
    'P08-002': 'No se lee el diario Terran ni se identifica a su autor.',
    'P08-003': 'Las raíces que mueven cadáveres no prueban el mecanismo de transformación de la mujer del templo.',
    'P08-004': 'Los muertos nuevos no se identifican con el antiguo paciente de Gobs.',
    'P08-005': 'No se identifican los nuevos clientes u ocupantes con los captores de Bling ni con las huellas antiguas.',
    'P08-006': 'Las descargas mágicas actuales no identifican o utilizan aquel pergamino de truco.',
    'P08-007': 'No se representa la reparación o sustitución de la espada de Kilzer.',
    'P09-001': 'No se fecha ni se explica el cambio nominal de Chochi a Axi.',
    'P09-002': 'No se reconstruye la visión de Citlali al tomar la mano de Nox.',
    'P09-003': 'La salpicadura del zombi no se relaciona con el escozor de los tatuajes al curar a Citlali.',
    'P09-004': 'La vigilancia que Mlan declara no identifica a los antiguos guardianes ni su acusación de traición.',
    'P09-005': 'El libreto de Tesa no se identifica con el mapa entregado al aprendiz.',
    'P09-006': 'Las raíces actuales y los matorrales de sigilo no se identifican con las hojas perfumadas de Ione.',
    'P09-007': 'No hay confesión o escena que identifique al ladrón de la hierba de Ione.',
    'P09-008': 'No se trata la inmunidad al alcohol de Lunaria ni sus duraciones discordantes.',
    'P09-009': 'El veneno de Patata no aporta diagnóstico sobre la mordedura de Ione a Axi.',
    'P10-001': 'No se retoma la captura de Pix o el motivo de su secuestro.',
    'P10-002': 'La gente de Mlan y los muros del lago no se identifican con la aldea de hombres lagarto.',
    'P10-003': 'Patata vuelve a actuar, pero el bloque no cambia el desenlace ya resuelto del cautiverio ni identifica aquí a Axi o Bling.',
    'P10-004': 'No se localizan las armas originales confiscadas a Aerendriel.',
    'P10-005': 'La batalla nueva de las raíces no modifica la aceptación ya documentada de aquella expedición de rescate.',
    'P10-006': 'Ningún lanzamiento actual se vincula al pergamino de truco del capítulo 10.',
    'P11-001': 'No se localiza el cofre ni se reconstruye el rescate y crianza de Amaru.',
    'P11-002': 'La obediencia que pide Chopito no explica la mecánica del juramento antiguo de Nox.',
    'P11-003': 'Tesa toma apuntes propios, sin leer o ampliar aquí el diario del nawal.',
    'P11-004': 'La exposición del cuerpo de Bonny no establece el poder, custodia o sucesión política de las monedas.',
    'P11-005': 'La caída de Bonny no explica su afiliación a las Cuchillas Negras o cómo vio a Nox invisible.',
    'P11-006': 'No se reconstruye la antigua conversación concertada entre Bonny y Nox en el muelle.',
    'P11-007': 'La joya futura de Angelique no concilia el número y custodia de las gemas antiguas.',
    'P11-008': 'Patata conserva armadura, escudo y martillo y los utiliza, pero eso no prueba la restitución íntegra de los bienes confiscados.',
    'P11-009': 'La actividad y el veneno actuales de Patata no completan el diagnóstico de secuelas de su antiguo cautiverio o del de Axi y Bling.',
    'P11-010': 'El respeto exigido por Mlan no modifica el resultado ya resuelto de las represalias de Ras Racor.',
    'P11-011': 'La expulsión de habitantes de Shiaru da contexto de pérdida de hogares, pero no adjudica el estado del casino, su apertura o sus cuentas.',
    'P12-001': 'No se precisan los términos del antiguo compromiso de Aerendriel con Bonny o la ejecución de su castigo.',
    'P12-002': 'No se identifica un objetivo nuevo del mapa de excavaciones de Molly o de la Marina.',
    'P12-003': 'La afirmación de expulsión general no localiza individualmente a Mingo, Mango y Mungo ni modifica su rescate anterior.',
    'P12-004': 'Mlan no se identifica como el preso pintado, Button o Nelli por su aspecto felino.',
    'P12-005': 'No se identifica ningún cadáver actual con el pirata abatido al escapar del campamento de la Marina.',
}
assert set(observations) == {q['id'] for q in QUESTIONS}
context_refs = {
    'P01-007': ['47-101', '47-116'], 'P02-002': ['47-101'], 'P04-001': ['47-101'],
    'P05-001': ['47-101', '47-116'], 'P05-004': ['47-101', '47-116'],
    'P07-002': ['47-105'], 'P07-003': ['47-101'], 'P07-007': ['47-101', '47-116'],
    'P11-004': ['47-101'], 'P11-005': ['47-101'], 'P11-008': ['47-118', '47-121'],
    'P11-009': ['47-130'], 'P11-011': ['47-116'], 'P12-003': ['47-116'],
}
cotejo = [{
    'id': q['id'], 'sha256_pregunta': q['sha256_pregunta'], 'pregunta': q['pregunta'],
    'estado_previo': q['estado'], 'estado_propuesto_desde_bloque': q['estado'],
    'resultado': 'contexto_sin_resolucion' if q['id'] in context_refs else 'sin_aporte_en_bloque',
    'observacion': observations[q['id']], 'referencias': context_refs.get(q['id'], []),
    'requiere_actualizacion': False,
    'alcance': 'Solo bloque 1: 00:00:00.280–00:45:28.990; no es una declaración de ausencia en el capítulo completo.',
} for q in QUESTIONS]

delivery = {
    'bloque': 1, 'lectura_completa': True, 'primer_segmento': SEG[0]['id'], 'ultimo_segmento': SEG[-1]['id'],
    'cobertura_lectura': [{'desde': start, 'hasta': end, 'primer_segmento': SEG[start]['id'], 'ultimo_segmento': SEG[end]['id'], 'segmentos': end - start + 1} for start, end in [(0, 256), (257, 513), (514, 770), (771, 1027)]],
    'segmentos_leidos': 1028, 'fuente_sha256': EXPECTED_SHA, 'audio_cotejado': False,
    'etapas': stages, 'afirmaciones': facts, 'historias_entidades': histories, 'misiones': missions,
    'preguntas': [f"{q['pregunta']} {q['respuesta']} ({', '.join(q['referencias'])})." for q in new_tracking],
    'seguimiento_nuevo': new_tracking, 'cotejo_preguntas_asignadas': cotejo,
    'dudas': [
        'Nombre Mlan: presentación c001297 (00:28:54.000) y repetición c001303. Conservar provisional; las formas Mik/M antes son reconocimiento defectuoso o tratamiento de mesa.',
        'Amigo de Leo «Écil»: c000199. Cotejar con la recogida de Eztli por Citlali en el capítulo 46; este bloque no nombra a la agresora y no prueba por sí solo la identidad.',
        'El lago no se nombra en el bloque. Su conexión sumergida con Perlasal puede enlazar con Lago Tachan, pero no universalizar la identidad de todas las orillas o ruinas.',
        'Tesa llama al elfo gruñón «Eldream» (00:08:54.440); encaja en el encargo anterior de los elfos, pero no se crea otra identidad ni se atribuye una orden nueva inequívoca a Eldrath.',
        'Ruta de Angelique: segundo giro poco claro en original (00:11:10.240); Tesa recapitula izquierda. No inventar coordenadas o un trazado de mapa.',
        'Conjuro de Patata al corte: el VTT solo permite nivel tres, ataque e impacto, sin nombre o daño. Su capacidad previa transcrita «trundez» se interpreta por la respuesta como expulsión de no muertos, conservando limitación.',
    ],
    'contradicciones': [
        'Tesa dice primero tres días con Leo y después tres/cuatro y cuatro: diferencia de expresión sin fecha exacta conciliada.',
        'La frase de resolución de expulsión dice todos menos uno atemorizados y después menciona de modo confuso un esqueleto que ha fallado: conservar resultado general sin fabricar un recuento de tiradas.',
    ],
    'nombres_dudosos': ['Mlan', 'Écil (amigo de Leo; posible Eztli)', 'Eldream (mención al elfo gruñón)'],
    'posibles_puentes': [
        'Bloque 2 empieza después del impacto de Patata. Integrar desenlace, enemigos restantes, recuperación de veneno, efectos de expulsión y posible botín sin cerrar aquí esos arcos.',
        'Relacionar la advertencia de Tesa con los cadáveres y el dragón de capítulos 31/40, sin identificar cuerpos ni responsables por similitud de vegetación.',
        'El cuerpo colgado de Bonny amplía las consecuencias posteriores al capítulo 43 y puede actualizar preguntas de esa etapa asignadas a otro bloque; las deudas antiguas de este reparto permanecen sin cuantía.',
        'Distinguir los desconocidos de la taberna de Iktan de los ocupantes de Shiaru: no hay vínculo probado.',
        'La joya de Angelique y su relación pendiente pueden retomarse después; no dar por fallido el encargo por ausencia de entrega en este intervalo.',
    ],
}

# Grafía resuelta por el coordinador mediante lectura completa de una escena posterior.
# No se importan sus sucesos al vídeo: solo su identificación del personaje.
def canonical_prose(text):
    return re.sub(r'(?<!«)\bMlan\b(?!»)', 'Mictlan', text)


for item in facts:
    item['entidades'] = ['Mictlan' if name == 'Mlan' else name for name in item['entidades']]
    item['conocedores'] = ['Mictlan' if name == 'Mlan' else name for name in item['conocedores']]
    item['titulo'] = canonical_prose(item['titulo'])
    item['afirmacion'] = canonical_prose(item['afirmacion'])
facts[18]['limitacion'] = 'El VTT presenta «Mlan» sin audio cotejado. El coordinador confirma la grafía Mictlan por lectura íntegra de la escena escrita posterior x-1531013198478708756 (36 mensajes). Solo se importa esa identificación; no sus acciones posteriores. No se fija especie reglada, tribu o rango. La vigilancia del lugar es declaración suya.'
for stage in stages:
    stage['texto'] = canonical_prose(stage['texto'])
for item in histories:
    item['nombre'] = canonical_prose(item['nombre'])
    for stage in item['etapas']:
        stage['texto'] = canonical_prose(stage['texto'])
histories[6]['nota'] = 'Mictlan es la grafía confirmada por el coordinador al leer completa la escena posterior x-1531013198478708756. El VTT de este bloque conserva «Mlan» en c001297 y c001303. Se usa esa escena solo para la identidad, sin trasladar sus acciones al capítulo 47; no se asigna una tribu ni se fusionan otros felinos.'
for item in cotejo:
    item['observacion'] = canonical_prose(item['observacion'])
new_tracking[1]['pregunta'] = '¿Quién es Mictlan y qué gente vigila con él las ruinas del lago?'
new_tracking[1]['respuesta'] = 'Se presenta con el nombre transcrito «Mlan» y el coordinador confirma Mictlan mediante rol escrito posterior. Afirma que su gente vigila el lugar, permite a Tesa estudiar sin sacrilegio y combate con dos descargas.'
new_tracking[1]['pendiente'] = 'Pueblo o afiliación e historia de la vigilancia; la grafía se resuelve mediante la fuente escrita cotejada por el coordinador.'
delivery['preguntas'] = [f"{q['pregunta']} {q['respuesta']} ({', '.join(q['referencias'])})." for q in new_tracking]
delivery['dudas'][0] = 'La presentación «Mlan» de c001297 y repetición c001303 quedan vinculadas a Mictlan por la escena posterior x-1531013198478708756, leída íntegra por el coordinador (36 mensajes). Conservar citas originales. La tribu y el rango no quedan fijados.'
delivery['nombres_dudosos'] = ['Écil (amigo de Leo; posible Eztli)', 'Eldream (mención al elfo gruñón)']
delivery['identidad_resuelta_por_coordinador'] = {'nombre': 'Mictlan', 'variantes_vtt': ['Mlan', 'Mik', 'mi clan'], 'fuente_escrita': 'x-1531013198478708756', 'alcance': 'Solo identificación del personaje; sin importar acciones posteriores a este capítulo.'}

sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('construir_revision_bloque1', ROOT / 'scripts/construir.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
for item in facts:
    module.validate_fact(item, SOURCE)
    assert item['cita'] == item['evidencia_cue']['texto']
    assert item['inicio'] <= item['evidencia_cue']['inicio'] <= item['evidencia_cue']['fin'] <= item['fin']
all_ids = {f['id'] for f in facts}
for stage in stages:
    assert set(stage['referencias']) <= all_ids
for entity in histories:
    for stage in entity['etapas']:
        assert set(stage['referencias']) <= all_ids
(BASE / 'entrega_1.json').write_text(json.dumps(delivery, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
ledger = '''# Lectura completa del bloque 1 del capítulo 47

Responsabilidad exclusiva: 00:00:00.280–00:45:28.990, 1028 segmentos sin solapamiento con los demás bloques.

Se leyeron íntegros `bloque_1.md` y los textos originales correspondientes en `bloque_1_segmentos.json`, en cuatro salidas controladas sin truncar:

| Índices inclusivos | Segmentos | Total |
| --- | --- | ---: |
| 0–256 | c000001–c000513 | 257 |
| 257–513 | c000515–c001027 | 257 |
| 514–770 | c001029–c001541 | 257 |
| 771–1027 | c001543–c002055 | 257 |

Total: 1028/1028. Los identificadores impares reflejan la segmentación ya preparada; no representan saltos de lectura. Se comprobó que cada línea del bloque Markdown coincide con su segmento normalizado y se conservaron las variantes originales para las citas. La lectura mostró las diferencias Choltacan/Choltacán → Xoltacan; no se usaron esas normalizaciones como citas.

También se leyeron completas las 94 preguntas asignadas en cuatro tramos 0–23, 24–47, 48–71 y 72–93, incluidos respuesta previa, estado, pendientes y hash. Cada una recibe observación individual en la entrega, siempre limitada a este bloque. No se declara la ausencia de respuestas en el resto del capítulo.

Contexto cotejado: AGENTS.md, continuidad_46.md, identidades_contexto.json, entradas pertinentes de config/entidades.json y su criterio de identidades. Se consultó el formato de la entrega anterior y la función validate_fact, sin copiar su relato o afirmaciones. Bonny se rotula con la grafía autorizada por el usuario, manteniendo Bonnie en la cita VTT. El coordinador confirmó Mictlan mediante lectura íntegra de la escena posterior x-1531013198478708756 (36 mensajes): se aplica solo a la identidad y se conserva «Mlan» en las citas. El amigo «Écil» y el elfo «Eldream» se registran para integración, sin mezclar identidades.

Fuente original conservada: `47 - yvqhR20m7Zg.es-orig.vtt`. SHA-256 comprobado antes de escribir: `af82762727aa32ebc82b92459bdc4b039b6b17839c0f994d26f0a5aaf88e983e`.

La entrega contiene ocho etapas de relato, 32 afirmaciones, 17 historias de entidades, seis misiones, seis preguntas nuevas provisionales y los 94 cotejos. Las 32 citas proceden literalmente de texto_original y pasan validate_fact contra el VTT original; se verifican además los intervalos de sus cues y las referencias del relato y las historias.

El audio no está cotejado. No se han publicado cambios ni realizado commit o push. El coordinador debe integrar el desenlace del combate desde el bloque siguiente y resolver los puentes de continuidad antes de dar el capítulo por revisado.
'''
(BASE / 'lectura_bloque_1.md').write_text(ledger, encoding='utf-8')
print(json.dumps({'segmentos_leidos': len(SEG), 'afirmaciones_validadas': len(facts), 'etapas': len(stages), 'historias_entidades': len(histories), 'preguntas_cotejadas': len(cotejo), 'preguntas_nuevas': len(new_tracking), 'sha256_fuente': EXPECTED_SHA}, ensure_ascii=False))
