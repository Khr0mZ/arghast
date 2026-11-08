"""Entrega editorial después de leer todos los segmentos del primer bloque46."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
from construir import validate_fact

rows = json.loads((ROOT / 'campanas/xoltacan/revision/borradores/46/bloque_1_segmentos.json').read_text(encoding='utf-8'))
source = ROOT / 'campanas/xoltacan/fuentes/46 - yRdWu0NIldc.es-orig.vtt'
facts = []

def fact(a, b, anchor, title, statement, names, kind='hecho_confirmado', limit=''):
    cue = rows[anchor]
    item = dict(id=f'46-{len(facts)+1:03d}', titulo=title, tipo=kind,
                afirmacion=statement, inicio=rows[a]['inicio'], fin=rows[b]['fin'],
                cita=cue['texto_original'],
                evidencia_cue=dict(inicio=cue['inicio'], fin=cue['fin'], texto=cue['texto_original']),
                entidades=names, ambito='separación del grupo y rescate en la aldea de la cascada',
                conocedores=[], conocimiento_personaje='desconocido',
                nota_conocimiento='Acceso de Madame Oghma sin establecer en este pasaje.',
                confianza='lectura de subtítulos; audio no cotejado', limitacion=limit)
    validate_fact(item, source)
    facts.append(item)

fact(30,60,46,'Eleanor recuerda la discusión en la playa después de la batalla',
     'Eleanor cuenta que, después del combate contra la Marina, siguieron a Citlali hacia la playa tras oír una explosión. Allí intentó impedir que los presentes se mataran durante una disputa y hubo un disparo. También procuró que el ruido no despertara a Erandy antes de continuar el viaje siguiendo a Cipo.',
     ['Eleanor','Citlali','Ione','Erandy','Cipo','Marina','El Garfio'], 'declaracion_personaje',
     'Es un repaso de lo sucedido entre sesiones. No reconstruye el diálogo entero, autor o blanco exacto del disparo, una entrada al Zampaolas o las noticias completas que recibió Citlali sobre Nox.')
fact(61,84,67,'Ione protege al grupo y permanece más seria',
     'Ione confirma el antecedente de una discusión con Mamá y un disparo. Desde entonces ha intentado guiar y proteger a sus compañeros mientras siguen a Cipo, haciendo guardias e interviniendo cuando encuentran peligros. Se describe más callada y seria, menos risueña que antes de lo ocurrido.',
     ['Ione','Citlali','Cipo','Tripulación del Zampaolas'], 'declaracion_personaje',
     'La recapitulación no atribuye por sí sola cada golpe de la disputa, una reconciliación definitiva o una nueva búsqueda submarina de Nox.')
fact(85,104,98,'Citlali se describe dolida y resentida entre siseos',
     'La jugadora de Citlali recuerda una pelea y describe a su personaje seria y dolida, con un rencor creciente. Los siseos vuelven a seducirla y la dejan emocionalmente inestable.',
     ['Citlali','Entidad serpentina vinculada a Citlali'], 'declaracion_personaje',
     'La descripción de su estado interior se ofrece a la mesa. No implica que todos sus compañeros oigan los siseos o conozcan su contenido, ni revela la identidad o el plan completo del interlocutor serpentino.')
fact(111,166,145,'La estampida separa a tres viajeras del grupo que iba a Iktan',
     'El director reúne como viajeros a Eleanor, Ione, Citlali, Poncelot, Ilikar, Erandy, Cipo, Lunaria y los demás acompañantes. Se dirigían a Iktan siguiendo a Cipo, a quien Ilikar atribuía conocer el camino, pero avanzaron dando vueltas. Una estampida de triceratops los obligó a apartarse y algunos saltaron al río. Eleanor, Ione y Citlali quedaron separadas y llevan horas andando por una senda sin hallar a sus compañeros ni la ciudad.',
     ['Eleanor','Ione','Citlali','Sir Poncelot','Ilikar','Erandy','Cipo','Lunaria','Iktan','Tripulación del Zampaolas'], 'explicacion_director',
     'La dispersión se fija como contexto inicial. No se describe una baja concreta durante la estampida, una llegada a Iktan o una guía deliberadamente engañosa por parte de Cipo.')
fact(167,181,175,'Etley queda con el otro grupo después de la separación',
     'Cuando la jugadora de Citlali reclama la presencia de la cría, el director dice primero que la dejó en Iktan. Ella recuerda que la llevó a la batalla y el director corrige: Etley ha quedado separado con el otro grupo.',
     ['Etley','Citlali','Iktan'], 'explicacion_director',
     'Conservar la corrección final. No se documenta un abandono de Etley en Iktan, su presencia junto a las tres viajeras o una muerte de la cría en esta escena.')
fact(182,246,190,'Ione se detiene y reparte fruta mientras buscan orientarse',
     'Cansada y con dolor de pies, Ione se sienta, añora el barco y reparte frutas entre las compañeras. Citlali le reprocha que se canse pese a parecer ahora más joven ella misma. Confían en que los otros estén con los trillizos y en que Pix pueda rastrearlas. La pirata acaba encontrando un cangrejo muerto en la bota, que retira antes de continuar.',
     ['Ione','Citlali','Eleanor','Pix','Tripulación del Zampaolas','Zampaolas'],
     limit='La confianza en los compañeros y Pix no representa un encuentro o rastreo observado de ese otro grupo. La comparación de aspecto no fija la edad exacta de Citlali.')
fact(247,260,252,'La fruta mejora la agilidad, devuelve daño y concede inspiración',
     'El director asigna los efectos de las frutas: Citlali obtiene ventaja en Acrobacias; quien golpee a Eleanor cuerpo a cuerpo recibe un dado de cuatro de daño; Ione recibe una inspiración para la partida, que perderá si no la usa.',
     ['Citlali','Eleanor','Ione'], 'explicacion_director',
     'Los efectos no demuestran una transformación permanente ni se atribuyen a hechizos nuevos de Eleanor. Se conserva la explicación mecánica dada en la sesión.')
fact(261,307,293,'Citlali evita hablar del rejuvenecimiento e intenta rastrear',
     'Ione pide a Citlali que utilice alguna habilidad para orientarse y pregunta por su rejuvenecimiento. Ella insiste en que no quiere hablar de ello. La pirata recuerda que ya contó cosas en la playa, corta una frase y se muestra triste. Citlali, irritada, empieza a tocar la tierra para buscar un rastro.',
     ['Citlali','Ione','Eleanor'],
     limit='La alusión a lo contado en la playa no reproduce una revelación íntegra. No fija una edad final, un mecanismo o la duración del rejuvenecimiento.')
fact(308,354,333,'Unas plantas muerden a las viajeras y Citlali no encuentra el camino',
     'Al buscar, Citlali distingue huellas de animales cruzadas, pero no una ruta clara. De la tierra aparecen plantas que se ocultan en el camino y saltan a morder a las tres. Tras las salvaciones se aplican dos puntos de daño. El director confirma que Citlali no conoce esa zona y está perdida; ella lo admite ante las compañeras.',
     ['Citlali','Ione','Eleanor'],
     limit='Las huellas no se identifican con los compañeros desaparecidos. La intervención del chat es origen de la complicación en la mesa, sin convertirla en un ataque de un personaje kender de la ficción.')
fact(355,421,408,'El rastreo de Eleanor falla e Ione elige el sur por azar',
     'Eleanor busca vegetación desgastada y señales de un paso frecuente, pero tampoco encuentra una ruta. Ione saca monedas y propone decidir la dirección al azar. Después de resolverlo con un dado de cuatro elige el sur y las otras la siguen, aunque dudan de su orientación. La capitana quiere reunirse cuanto antes con su tripulación y saber qué ha pasado.',
     ['Eleanor','Ione','Citlali','Tripulación del Zampaolas'],
     limit='Las monedas no se identifican con la moneda pirata de Bonnie ni se representa un poder de ese objeto. La elección aleatoria no confirma el rumbo correcto hacia Iktan.')
fact(422,475,442,'El camino elegido las devuelve a la costa',
     'Las tres retroceden durante horas por la ruta que habían seguido y vuelven a acercarse a la costa. Ione pretende repetir la elección con monedas, pero Citlali la detiene. Proponen dirigirse al norte o rastrear de nuevo a los otros, sin certeza de encontrarlos en el mismo lugar y sin saber si siguen cerca los triceratops.',
     ['Ione','Citlali','Eleanor','El Garfio'],
     limit='El retorno a la costa no muestra todavía un reencuentro con la tripulación o con la cría, ni una nueva búsqueda de los restos del Invictus.')
fact(476,510,505,'Citlali toma otra ruta guiándose por sus instintos',
     'Citlali intenta orientarse desde el lugar de partida y recibe una nueva tirada, pero continúa sin estar segura. Su enfado y frustración le impiden recordar bien; decide seguir sus instintos y caminar con aparente confianza. El director distingue el resultado de la tirada de lo que puede saber Eleanor al verla elegir.',
     ['Citlali','Eleanor','Ione'],
     limit='La seguridad exterior no convierte la ruta en una certeza. El fracaso de una tirada no se transmite automáticamente como conocimiento a los otros personajes.')
fact(511,541,527,'Ione no obtiene orientación del mapa que recuerda haber recibido de Nox',
     'Ione intenta servirse de un mapa al reconocer el punto de partida, pero el director niega que haya elaborado uno del Garfio. Ella recuerda un mapa que Nox le regaló, lo llama falso y enseguida corrige ese calificativo. Finalmente continúan tras Citlali sin establecer por ese intercambio el camino a Iktan.',
     ['Ione','Citlali','Nox','El Garfio','Iktan'], 'declaracion_personaje',
     'El recuerdo vacilante no identifica el documento con el mapa de Poncelot o con otro ya catalogado. No se muestra su contenido ni se demuestra su falsedad.')
fact(542,579,546,'Las huellas humanoides atraen a Ione hacia unas ruinas',
     'En la ruta aparecen pisadas claras de humanoides. Citlali prepara la alpargata con prudencia, pero Ione cree que son de su tripulación y corre tras ellas. Eleanor desenfunda espada y escudo sin comprender del todo la iniciativa. Las huellas las conducen entre los árboles hasta antiguas piedras cubiertas de vegetación.',
     ['Citlali','Ione','Eleanor','Tripulación del Zampaolas','Aldea caníbal de la cascada'],
     limit='La atribución de las pisadas a la tripulación es una suposición de Ione. No se confirma un reencuentro al seguirlas ni un arma espiritual manifestada por Eleanor.')
fact(580,609,583,'La aldea junto a la cascada no es Iktan',
     'Tras las ruinas encuentran una aldea junto a un pequeño lago y una cascada, al pie de una pared rocosa. Ione pregunta si es el destino, pero Citlali aclara que no es Iktan y que desconoce quién vive allí. Las otras se acercan mientras la nativa pide cautela.',
     ['Ione','Citlali','Eleanor','Aldea caníbal de la cascada','Iktan'],
     limit='El lugar no recibe nombre propio. Se conserva como aldea descriptiva separada de los poblados caníbales de otras sesiones mientras no exista identificación inequívoca.')
fact(610,639,616,'Una planta libera esporas al avanzar hacia la aldea',
     'Al dar un paso, Ione pisa una pequeña planta con cabezas que libera una nube de esporas. Las viajeras reciben dos puntos de daño y el malestar pasa. La pirata sigue avanzando pese a las advertencias de Citlali.',
     ['Ione','Citlali','Eleanor','Aldea caníbal de la cascada'],
     limit='La planta no demuestra una trampa colocada por los habitantes ni explica lo ocurrido en el poblado. No se fija una enfermedad o efecto duradero.')
fact(640,719,691,'Ione descubre que la piel de una cabaña es humana',
     'Ione entra en el poblado y mira una cabaña con camas, pieles y carne colgada para secarse. Se pone una piel como capa, hasta que el director aclara que es humana. Al reconocerla por el olor, se la quita y la devuelve a su sitio. Pregunta en voz alta si estarán en una aldea caníbal y decide explorar escondiéndose.',
     ['Ione','Citlali','Eleanor','Aldea caníbal de la cascada'],
     limit='No se identifica a la víctima de la piel. El hallazgo no transforma la prenda en un vestigio conservado por Ione ni prueba aún quién mató a los habitantes.')
fact(720,822,753,'Las cabañas están vacías y la exploración conduce a una cueva',
     'Ione se oculta detrás de las cabañas; Citlali avanza vigilando con la alpargata y Eleanor mantiene espada y escudo preparados. Encuentran más carne colgada, que no huele a podrido, pero ninguna persona en las casas. Al reconocer que no son restos de animales comunes, Citlali siente náuseas y recuerdos dolorosos. Ione sube a un tejado, descubre una entrada y se aproxima a la cueva llamando a sus habitantes.',
     ['Ione','Citlali','Eleanor','Aldea caníbal de la cascada'],
     limit='La falta de olor a podrido no permite fechar exactamente la carne. El silencio no prueba que toda la población haya desaparecido ni identifica a los muertos o a los responsables.')
fact(823,869,834,'La cueva contiene cadáveres ennegrecidos y un hombre encadenado',
     'Entran en una cueva húmeda que huele a rancio, podredumbre y chamuscado. Hay cuerpos retorcidos, sin respiración y con la piel ennegrecida de una manera que el director compara con el paso de una gran descarga eléctrica. Al fondo encuentran a un hombre encadenado y cerca de perder el conocimiento, con una gran cicatriz y una mancha oscura en un lado del cuerpo.',
     ['Ione','Citlali','Eleanor','Zoltan','Aldea caníbal de la cascada'],
     limit='El nombre del cautivo se revela después. El aspecto de los cadáveres no identifica por sí solo a quien los mató ni relaciona su causa con la cicatriz del hombre. No se fija el número de muertos, su identidad individual o toda la duración del cautiverio.')
fact(870,943,903,'Ione despierta al cautivo y le retira la venda',
     'Ione se acerca pese al olor, apartando los cuerpos. Le echa agua del odre en la cara y le quita una venda. El hombre abre los ojos, teme que quieran comérselo y pide ayuda con las cadenas. La capitana le asegura que, aunque tiene hambre, no se comería a un humano y prepara Negociación para actuar sobre las uniones.',
     ['Ione','Zoltan','Negociación','Aldea caníbal de la cascada'],
     limit='La referencia a humano procede del diálogo de Ione. El despertar no elimina todas sus debilidades ni demuestra la moralidad o inocencia del cautivo.')
fact(944,999,964,'Eleanor cuestiona el rescate entre las súplicas del prisionero',
     'Citlali se acerca con compasión y pide sacar al hombre de allí. Eleanor plantea que podría haber matado a los cadáveres que lo rodean y advierte que no saben si es bueno. Ione responde que esos muertos podían comérselas. El cautivo insiste en que no quiere que lo devoren y pide al menos comida si lo dejan. El grupo termina permitiendo que la pirata continúe el rescate.',
     ['Citlali','Eleanor','Ione','Zoltan','Aldea caníbal de la cascada'],
     limit='La posible autoría del cautivo es una hipótesis de Eleanor, sin confesión o prueba concluyente en este tramo. Las conversaciones no constituyen una detección mágica de alineamiento o un juicio definitivo.')
fact(1000,1026,1019,'Negociación rompe el soporte de madera y libera al hombre',
     'Ione entrechoca las nudilleras Negociación y golpea las juntas del soporte al que están sujetas las cadenas. El director precisa que se trata de una construcción de madera, y ella elige golpearla porque es más blanda que el metal. La madera termina crujiendo y los brazos del cautivo caen libres.',
     ['Ione','Zoltan','Negociación','Aldea caníbal de la cascada'],
     limit='No se afirma que Ione rompa las cadenas de metal. La broma posterior de ordenar al recién liberado que los mate no se convierte en un ataque ejecutado.')
fact(1027,1050,1049,'El rescatado se presenta como Zoltan y reconoce una deuda con Ione',
     'El hombre estira el cuerpo después del cautiverio, agradece la ayuda de Ione y dice estar en deuda con ella. Admira sus golpes; la capitana le presenta sus armas como Negociación. Tras unas bromas y un comentario de coqueteo, se presenta como Zoltan.',
     ['Zoltan','Ione','Citlali','Eleanor','Negociación'],
     limit='La deuda expresa gratitud, sin un contrato, rango o incorporación formal a la tripulación. Los comentarios sobre otro muerto no identifican por nombre a esa persona ni fijan una relación previa de Zoltan con ella.')
fact(1051,1110,1085,'El nombre y el aspecto de Ione provocan un flash de un cartel',
     'Tras fijarse en Ione y conocer su nombre, Zoltan recibe un pinchazo en la cabeza que lo obliga a hincar la rodilla. Ve durante un instante un cartel borroso, sin poder explicar la imagen o el dolor. Citlali se acerca y lo sostiene para que no caiga por completo y propone sacarlo de la cueva. Él niega haber comido chocolate y confirma que no había comido nada.',
     ['Zoltan','Ione','Citlali','Aldea caníbal de la cascada'],
     limit='La imagen no permite leer el cartel, una recompensa o una acusación ni confirma que Zoltan conozca la historia de Ione. La mención de chocolate es una pregunta corregida y no la causa demostrada del episodio.')
fact(1111,1144,1138,'Una fruta concede a Zoltan resistencia al daño punzante',
     'Le ofrecen a Zoltan una fruta para ayudarlo con el hambre. La descripción vacila entre guayaba y mango, y él la acepta y come. Después de resolver la tirada, el director le concede resistencia al daño punzante y advierte que debe recordarla porque no se aplica automáticamente.',
     ['Zoltan','Ione','Citlali','Eleanor'], 'explicacion_director',
     'No se identifica con certeza a quien entrega la fruta en este intercambio. La broma de los piercing no la convierte en inmunidad; no se demuestra curación del episodio del cartel ni se fija aquí una duración permanente.')

stages = [
    dict(titulo='Separadas después de la playa', referencias=['46-001','46-002','46-003','46-004','46-005'], texto=
         'Los recuerdos del grupo enlazan la batalla con una discusión en la playa. Eleanor intentó evitar que los presentes se mataran y proteger el descanso de Erandy; Ione recuerda un disparo y el conflicto con Mamá. La capitana ha seguido haciendo guardias y protegiendo a sus compañeros, más seria y callada. Citlali se describe dolida, resentida y tentada por los siseos. Después, todos emprendieron el camino a Iktan siguiendo a Cipo, cuya orientación resultó poco segura. Una estampida de triceratops los obligó a huir y a algunos a saltar al río. Ione, Eleanor y Citlali quedaron separadas. Etley siguió con el otro grupo, según la corrección final del director, mientras las tres llevan horas caminando sin encontrar la ciudad ni a sus compañeros.'),
    dict(titulo='Las monedas conducen de vuelta a la costa', referencias=['46-006','46-007','46-008','46-009','46-010','46-011','46-012','46-013','46-014'], texto=
         'Ione detiene la marcha para descansar los pies y repartir fruta. Ella recibe inspiración; Citlali gana agilidad y Eleanor devuelve daño a quien la golpee de cerca. Las preguntas sobre el rejuvenecimiento irritan a Mamá, que no quiere hablar del asunto. Busca huellas, pero solo distingue animales y unas plantas ocultas saltan a morderlas. Eleanor intenta orientarse por el desgaste del terreno y tampoco encuentra un camino claro. Ione decide confiar en el azar: el resultado de unas monedas y un dado la lleva a elegir el sur. Las horas de marcha las devuelven a la costa. Citlali impide repetir la ocurrencia y retoma la búsqueda por intuición, sin estar segura. La discusión sobre un mapa que Ione recuerda haber recibido de Nox tampoco resuelve el rumbo. Al aparecer huellas humanoides, la capitana supone que son de su tripulación y corre a seguirlas; las otras preparan sus armas.'),
    dict(titulo='La aldea silenciosa de la cascada', referencias=['46-015','46-016','46-017','46-018','46-019'], texto=
         'Las pisadas conducen a antiguas piedras cubiertas de vegetación y a una aldea junto a un lago y una cascada. Citlali advierte que no es Iktan y que desconoce a sus habitantes. Ione avanza y otra planta libera esporas que les causan un malestar breve. En una cabaña encuentra camas, carne secándose y pieles. Se pone una a modo de capa hasta reconocer que es humana, y entonces la devuelve a su sitio. Sospechan de un poblado caníbal y exploran con cuidado, pero las casas están vacías. Ione sube a un tejado y encuentra la entrada de una cueva. Dentro huele a podredumbre y chamuscado: los cadáveres retorcidos presentan un ennegrecimiento que recuerda al paso de la electricidad. Al fondo hay un hombre encadenado, con una gran cicatriz y una mancha oscura en el cuerpo, todavía vivo.'),
    dict(titulo='Zoltan y el cartel que no consigue recordar', referencias=['46-020','46-021','46-022','46-023','46-024','46-025'], texto=
         'Ione moja la cara del cautivo y le quita la venda. Él teme que quieran comérselo y les pide que lo liberen. Citlali se compadece, mientras Eleanor duda de su inocencia: quizá sea quien mató a los cuerpos que lo rodean. La sospecha no queda demostrada y terminan permitiendo el rescate. Ione usa Negociación para romper las juntas del soporte de madera, dejando libres sus brazos sin partir el metal de las cadenas. El rescatado agradece la ayuda y se presenta como Zoltan. Al fijarse en la capitana y oír su nombre sufre un dolor de cabeza y un flash fugaz de un cartel ilegible. Citlali lo sostiene y propone salir de allí. Una fruta le sirve de alimento y le concede resistencia al daño punzante, sin explicar todavía el episodio de memoria. Las bromas sobre inmunidad a los piercing no alteran ese efecto.')
]

histories = []
def history(name, kind, title, text, refs, new=False, description='', note=''):
    histories.append(dict(nombre=name,tipo=kind,nueva=new,descripcion=description,nota=note,
                          etapas=[dict(titulo=title,texto=text,referencias=refs)]))

history('Ione','personaje','Una capitana que quiere recuperar a su gente',
        'Ione recuerda una disputa con Citlali y un disparo después de la batalla. Desde entonces procura proteger a los viajeros, más callada que de costumbre. La estampida la separa de la tripulación junto a Eleanor y Mamá. Su intento de orientarse por azar acaba devolviéndolas a la costa. Al encontrar huellas humanoides las atribuye a sus compañeros, pero llega a una aldea con restos humanos y casas vacías. Allí deja de bromear al reconocer una piel humana y continúa la exploración oculta.', ['46-002','46-004','46-006','46-010','46-011','46-013','46-014','46-017','46-018'])
histories[-1]['etapas'].append(dict(titulo='Los puños que liberan a Zoltan',texto=
    'Encuentra al hombre encadenado entre cadáveres y lo despierta con agua. Pese a las dudas de Eleanor, decide ayudarlo. Golpea con Negociación el soporte de madera que sujeta las cadenas y lo libera. Zoltan le agradece la ayuda y reacciona a su nombre y aspecto con una dolorosa imagen borrosa de un cartel. El episodio no demuestra que la capitana explique o comprenda ese recuerdo.',referencias=['46-019','46-020','46-021','46-022','46-023','46-024']))
history('Citlali','personaje','Rencor, desorientación y compasión',
        'La jugadora describe a Citlali todavía dolorida y resentida tras la disputa en la playa, bajo la tentación de los siseos. Su apariencia rejuvenecida provoca preguntas que rechaza. Separada de Etley y de los otros, no encuentra el camino a Iktan y acaba guiándose por sus instintos. Los restos humanos de la aldea le provocan náuseas y recuerdos dolorosos, pero se compadece del cautivo. Cuando Zoltan sufre el flash del cartel, lo sostiene y propone sacarlo de la cueva. El primer tramo no explica el mecanismo del rejuvenecimiento o del dolor de ambos.', ['46-003','46-004','46-005','46-008','46-009','46-012','46-018','46-021','46-024'])
history('Eleanor','personaje','Cautela ante una ayuda incierta',
        'Eleanor recuerda haber mediado en la disputa de la playa e intentado proteger el descanso de Erandy. La estampida la deja con Ione y Citlali. Busca una senda de paso habitual sin encontrarla y sigue a sus compañeras con espada y escudo preparados. En la aldea mantiene la guardia y, al descubrir los cadáveres junto al prisionero, plantea que él pueda ser su autor. El rescate sigue adelante sin que esa hipótesis quede probada. Su prudencia no se presenta como una detección mágica de la naturaleza de Zoltan.', ['46-001','46-004','46-010','46-014','46-018','46-019','46-021','46-022'])
history('Zoltan','personaje','El cautivo entre los cadáveres',
        'Ione, Citlali y Eleanor lo encuentran vivo y encadenado al fondo de la cueva de una aldea caníbal, rodeado de cuerpos ennegrecidos. Tiene el torso descubierto, una gran cicatriz y una mancha oscura en un costado; está débil y hambriento. Ione lo despierta y rompe la madera que sujeta sus cadenas. Aunque Eleanor sospecha que puede haber matado a los pobladores, el tramo no lo confirma. Él agradece el rescate, reconoce una deuda con la capitana y se presenta como Zoltan.', ['46-019','46-020','46-021','46-022','46-023'], True,
        'Hombre rescatado de las cadenas en la cueva de una aldea caníbal, marcado por una gran cicatriz y una mancha oscura lateral.',
        'Nombre Zoltan sin tilde. No identificar como responsable de los cadáveres por mera sospecha ni fijar especie, origen o poderes completos antes de los pasajes que lo indiquen.')
histories[-1]['etapas'].append(dict(titulo='Un cartel borroso y una fruta',texto=
    'Al observar a Ione y oír su nombre sufre un pinchazo que lo obliga a arrodillarse y le trae un flash ilegible de un cartel. No comprende el recuerdo. Citlali lo ayuda a sostenerse y recibe una fruta para comer. La tirada le concede resistencia al daño punzante, sin resolver la imagen, su hambre anterior o la causa del dolor.',referencias=['46-024','46-025']))
history('Etley','personaje','Separado de Citlali, con los otros viajeros',
        'La estampida dispersa al grupo que iba hacia Iktan. El director corrige una primera referencia a que Etley se quedó en la ciudad: la cría viajó a la batalla y ahora está separada con el otro grupo. Citlali continúa en esta escena con Ione y Eleanor, sin que esa separación documente una muerte o un abandono definitivo.', ['46-004','46-005'])
history('Erandy','personaje','El descanso protegido antes de separarse',
        'Eleanor recuerda que intentó evitar que la disputa y los ruidos de la playa despertaran a Erandy. El director la incluye después entre quienes siguieron a Cipo rumbo a Iktan antes de la estampida. La separación deja a su señora con Ione y Citlali. Este repaso confirma su presencia y la preocupación por su descanso, sin describir una recuperación completa del trance o del agotamiento del combate.', ['46-001','46-004'])
history('Cipo','personaje','Una ruta que no conocía con seguridad',
        'Ilikar había asegurado que Cipo conocía el camino a Iktan y los viajeros decidieron seguirlo. El director aclara que tampoco se orientaba bien y que dieron vueltas por la jungla antes de que una estampida los dispersara. Cipo no permanece con las tres protagonistas de la separación. La desorientación no demuestra una intención de engañarlas o una nueva naturaleza de la criatura ígnea.', ['46-002','46-004'])
history('Tripulación del Zampaolas','faccion','El camino y la estampida',
        'Después de la batalla los compañeros parten con Ione hacia Iktan siguiendo a Cipo. Los viajeros y acompañantes se dispersan al paso de una estampida de triceratops y al cruzar el río. La capitana queda con Citlali y Eleanor, mientras confía en que los trillizos y Pix ayuden a los otros. El primer tramo documenta esa separación y su deseo de recuperar a la tripulación, sin volver a reunirla todavía.', ['46-002','46-004','46-006','46-010','46-014'])
history('Negociación','objeto','Romper el soporte, sin partir el metal',
        'Ione prepara las nudilleras para liberar a Zoltan, encadenado en la cueva. Elige golpear las juntas del soporte de madera porque no espera poder romper el metal a puñetazos. Los golpes hacen crujir la construcción y dejan libres los brazos del cautivo. Después le presenta el arma por su nombre y la hace entrechocar entre pequeñas chispas.', ['46-020','46-022','46-023'])
history('Aldea caníbal de la cascada','lugar','Pieles humanas y silencio',
        'Unas huellas humanoides llevan a Ione, Citlali y Eleanor a una aldea junto a un lago, una cascada y una pared rocosa. Las cabañas contienen camas, pieles humanas y carne colgada, pero no encuentran habitantes vivos en ellas. La exploración conduce a una cueva húmeda con cadáveres retorcidos y ennegrecidos como por una descarga. Al fondo rescatan al hombre que se presenta como Zoltan. La sospecha de que mató a los pobladores no queda confirmada en el primer tramo.', ['46-014','46-015','46-017','46-018','46-019','46-020','46-021','46-022','46-023'], True,
        'Aldea de cabañas y restos humanos junto a un lago con cascada, cuya cueva contiene cadáveres chamuscados y al cautivo Zoltan.',
        'Denominación descriptiva sin topónimo pronunciado. Mantener separada de las aldeas caníbales de capítulos anteriores; la cueva puede integrarse en esta ficha sin inventar un nombre propio adicional.')
history('Iktan','lugar','Una llegada que sigue pendiente al perderse',
        'Los compañeros ponen rumbo a Iktan después del encuentro en la playa, pero la guía de Cipo no es segura y una estampida los separa. Ione, Citlali y Eleanor intentan volver al norte y encuentran otra aldea que Mamá descarta como su destino. Su intención de llegar no convierte el poblado de la cascada en parte de la ciudad oculta.', ['46-004','46-009','46-011','46-012','46-015'])

delivery = dict(bloque=1, lectura_completa=True, primer_segmento='c000001', ultimo_segmento='c002289',
    cobertura_lectura=[dict(desde=0,hasta=289),dict(desde=290,hasta=579),dict(desde=580,hasta=869),dict(desde=870,hasta=1144)],
    etapas=stages, afirmaciones=facts,
    misiones=[
        'Encontrar Iktan y reunirse con los compañeros: la estampida separa a Eleanor, Ione y Citlali del resto. Las monedas las devuelven a la costa y las huellas siguientes conducen a una aldea desconocida, sin completar aún la llegada en este tramo (46-004–46-005, 46-009–46-015).',
        'Rescatar al prisionero: Ione despierta al hombre, debate con Eleanor y Citlali y rompe el soporte de madera. Zoltan queda libre y recibe alimento, aunque su pasado y el origen del cartel siguen desconocidos (46-019–46-025).',
        'Comprender el flash de Zoltan: el dolor y un cartel borroso aparecen al conocer a Ione. El primer tramo no muestra su contenido o causa (46-024).'
    ],
    preguntas=[
        '¿Quién mató a los cadáveres de la cueva y qué relación tiene Zoltan con lo ocurrido? El ennegrecimiento recuerda al paso de electricidad y Eleanor sospecha del cautivo, sin una prueba definitiva en este tramo (46-019, 46-021).',
        '¿Qué cartel ve Zoltan al reconocer el aspecto y el nombre de Ione, y qué explica el dolor y ese recuerdo fugaz? La imagen no se lee ni se fija una recompensa o acusación (46-024).',
        '¿De dónde vienen la cicatriz y la mancha oscura de Zoltan y por qué estaba encadenado? Su aparición no reconstruye su origen o el cautiverio (46-019–46-023).'
    ],
    contradicciones=[
        'La primera explicación de que Etley quedó en Iktan se corrige: está con el otro grupo tras la estampida. Conservar esa posición sin fabricar un abandono o una muerte (46-004–46-005).',
        'Los repasos confirman la disputa en la playa y un disparo, sin detallar aquí autor y blanco o el diálogo íntegro. La referencia no permite completar conjeturalmente lo que falta en el vídeo43 (46-001–46-003).',
        'La apariencia joven de Citlali y su irritación están presentes, pero no se explica una edad exacta, duración del efecto o identidad completa del ser serpentino (46-003, 46-006, 46-008).',
        'Las monedas utilizadas para elegir rumbo son ordinarias o no identificadas. No se asigna el hecho a la moneda pirata de Bonnie ni se invoca un poder suyo (46-010–46-011).',
        'La atribución de las huellas a la tripulación es de Ione. El hallazgo conduce a una aldea distinta de Iktan, sin demostrar todavía un rastro verdadero de sus compañeros (46-014–46-015).',
        'Los cadáveres y el ennegrecimiento no prueban por sí solos que Zoltan los matara. El rescate se hace rompiendo el soporte de madera y no las cadenas de metal (46-019, 46-021–46-022).',
        'Zoltan recibe resistencia al daño punzante. Las bromas sobre piercing no equivalen a inmunidad y la fruta no demuestra que cure el dolor o el recuerdo del cartel (46-024–46-025).'
    ],
    nombres_dudosos=[
        'Zoltan/Soltan y variantes identifican al mismo rescatado, presentado por nombre. Se conserva Zoltan sin tilde y no se fija especie o historia personal no expresadas (46-019–46-025).',
        'Ione/Jone/Jon/Jones, Eleanor/Eleonor/Elianor y Citlali/Cildali/Lali corresponden a las tres protagonistas ya catalogadas; Andy/Randy del repaso se vincula a Erandy, su escudera (46-001–46-004).',
        'Cipo, llamado superhéroe ígneo por Ilikar y los compañeros, es la criatura de fuego ya conocida. El apelativo no crea otro guía o una autoridad infalible (46-004).',
        'Aldea caníbal de la cascada es una etiqueta descriptiva de lugar. No equiparar por ambientación o mapa con las aldeas de Nox de otras sesiones ni con Iktan (46-015–46-019).',
        'El mapa que Ione recuerda como regalo de Nox no se identifica inequívocamente con el de Poncelot; el calificativo falso se corrige dentro de la conversación y no permite fijar su naturaleza o contenido (46-013).'
    ],
    continuidad=[
        dict(pregunta_id='P43-005',hechos=['46-001','46-002','46-003','46-004'],nota='El repaso documenta que el grupo de tierra alcanzó la playa y hubo una disputa con Ione y un disparo. No reconstruye el diálogo, el autor/blanco o una entrada al barco; conservar parcial la pregunta sobre qué encontró Citlali al alcanzar el Zampaolas.'),
        dict(pregunta_id='P43-004',hechos=['46-003','46-006','46-008'],nota='Citlali sigue con apariencia rejuvenecida y resentimiento; rechaza explicar el cambio. Este tramo no fija duración o mecanismo; integrar los nuevos drenajes de otros bloques si los hubiera.'),
        dict(pregunta_id='P43-006',hechos=['46-001','46-004'],nota='Eleanor intentó proteger el descanso de Erandy y el director la incluye entre quienes salieron hacia Iktan. No se describe una recuperación completa de su agotamiento o consecuencias del trance.'),
        dict(pregunta_id='P42-006',hechos=['46-002','46-004','46-010','46-011','46-014'],nota='Ione pasa al viaje terrestre hacia Iktan y busca reunirse con la tripulación. No representa una nueva búsqueda de Nox ni un uso inequívoco de la moneda pirata; las monedas del rumbo no se asocian a ella.'),
        dict(pregunta_id='P43-001',hechos=['46-003','46-008'],nota='Se mencionan siseos que tientan a Citlali, sin revelar nombre, plan completo o alcance del ser serpentino.'),
        dict(pregunta_id='P43-002',hechos=['46-003','46-008'],nota='El estado de Citlali no localiza el altar ni demuestra por sí mismo las consecuencias de su activación.'),
        dict(pregunta_id='P40-007',hechos=['46-004'],nota='Cipo acompaña la marcha hacia Iktan y queda fuera del trío separado. El repaso no informa de la procedencia del fragmento de espada.'),
        dict(pregunta_id='P07-002',hechos=['46-004','46-005'],nota='La cría Etley se separa con el otro grupo. No se completa la especie, el precio o el conocimiento del antiguo pacto de venta por parte de Citlali.')
    ],
    historias_entidades=histories)
assert len(rows) == 1145
assert rows[0]['id'] == delivery['primer_segmento'] and rows[-1]['id'] == delivery['ultimo_segmento']
assert sum(r['hasta']-r['desde']+1 for r in delivery['cobertura_lectura']) == len(rows)
(ROOT / 'campanas/xoltacan/revision/borradores/46/entrega_1.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
print(f'Entrega 1: {len(facts)} afirmaciones validadas, {len(stages)} etapas, {sum(len(s["texto"].split()) for s in stages)} palabras y {len(histories)} propuestas de historia.')
