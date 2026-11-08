"""Entrega editorial tras la lectura completa de los índices 0 a 1145."""
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'scripts'))
from construir import validate_fact,write_json,seconds

rows=json.loads((ROOT / 'campanas/xoltacan/revision/borradores/46/bloque_2_segmentos.json').read_text(encoding='utf-8'))
source=ROOT / 'campanas/xoltacan/fuentes/46 - yRdWu0NIldc.es-orig.vtt'
facts=[]


def fact(number,title,start,end,quote_time,text,entities,limitation='',kind='hecho_confirmado'):
    cue=next(s for s in rows if s['inicio'].startswith(quote_time))
    item={'id':f'46-{number:03d}','titulo':title,'tipo':kind,'afirmacion':text,
          'inicio':start,'fin':end,'cita':cue['texto_original'],
          'evidencia_cue':{'inicio':cue['inicio'],'fin':cue['fin'],'texto':cue['texto_original']},
          'entidades':entities,'ambito':'rescate y combate en la aldea caníbal de la cascada',
          'conocedores':[],'conocimiento_personaje':'desconocido',
          'nota_conocimiento':'Acceso de Madame Oghma sin establecer en este pasaje.',
          'confianza':'lectura de subtítulos; audio no cotejado','limitacion':limitation}
    validate_fact(item,source)
    facts.append(item)


fact(101,'Citlali ayuda a Zoltan a abandonar la cueva','00:49:25.319','00:52:32.519','00:50:14.480',
     'Los viajeros quieren salir del olor de la cueva y revisar lo que pueda quedar en las casas. Citlali ayuda a Zoltan a levantarse y lo acompaña del brazo hacia la entrada y después al agua para que pueda limpiarse. Él admite que no sabe cuánto tiempo ha pasado allí; los cadáveres cercanos no le permiten fijarlo con precisión.',
     ['Citlali','Zoltan','Eleanor','Ione','Cueva de los cadáveres ennegrecidos','Aldea caníbal de la cascada'],
     'La broma sobre hacer una barbacoa en la cueva no explica la causa de la muerte o el estado de todos los cadáveres. Zoltan no establece una duración exacta de su encierro.')
fact(102,'Eleanor encuentra una copa dorada distinta de la que ya llevaba','00:52:32.520','00:54:47.639','00:54:30.319',
     'Eleanor entra en la choza grande, que parece corresponder al líder. Encuentra una silla semejante a un trono, pieles, calaveras, cuernos, huesos y cofres. Al pisar el suelo nota pieles humanas de textura gelatinosa. Entre los objetos halla una copa de apariencia dorada con inscripciones y joyas. La compara con otra que ya llevaba y el director aclara que son diferentes: esta es un tesoro para vender.',
     ['Eleanor','Aldea caníbal de la cascada','Copa dorada de la choza del jefe'],
     'La denominación inicial de copa ritual en la tirada de tesoro no demuestra un efecto mágico o un rito ejecutado. La distinción explícita impide fusionarla con la copa anterior de Eleanor.')
fact(103,'Zoltan se baña mientras Citlali espera en la orilla','00:54:47.640','00:56:51.038','00:55:09.280',
     'Zoltan agradece la ayuda de Citlali, se suelta de su brazo y entra de cabeza al agua. Se refresca, se limpia y le ofrece entrar. Citlali rehúsa, se da la vuelta y se cubre los ojos para no verlo mientras está poco vestido. Zoltan bucea por los alrededores y ve algunos peces y una calavera entre los restos, sin detectar nada especialmente extraño.',
     ['Zoltan','Citlali','Aldea caníbal de la cascada'],
     'La observación de una calavera no identifica a la víctima ni añade un hallazgo mágico. El baño ocurre en el agua próxima a la aldea, sin atribuir propiedades curativas a la cascada.')
fact(104,'Citlali consigue una piel para vestir a Zoltan y se presenta','00:56:51.039','00:58:49.439','00:57:33.440',
     'Citlali busca entre las chozas algo con lo que Zoltan pueda vestirse. Encuentra una piel que el director distingue expresamente de las humanas y la deja sobre una roca, todavía evitando mirarlo. Rechaza volver a entrar al agua porque deben seguir hacia sus amigos. Cuando él le pregunta el nombre, se presenta como Citlali y ambos se disponen a darse la mano.',
     ['Citlali','Zoltan','Aldea caníbal de la cascada'],
     'La piel se obtiene como ropa improvisada, sin nombre de animal, valor mágico o vinculación a una víctima humana. Las variantes de reconocimiento de Citlali no crean otra persona.')
fact(105,'Un apretón de manos descarga electricidad sobre Citlali','00:58:49.440','01:01:00.159','00:59:34.559',
     'Al darse la mano, Zoltan todavía está mojado. El director describe una electricidad estática que pasa por el cuerpo de Citlali y le causa dolor. Ella grita y retira la mano. Zoltan también percibe la descarga como algo propio y extraño, pero no sufre el mismo daño ni entiende qué ha ocurrido. Se disculpa, mientras Citlali insiste en no mirarlo hasta que se vista.',
     ['Citlali','Zoltan'],
     'La descarga se desencadena con el contacto, sin intención de herir acreditada. No demuestra que Citlali haya vuelto a drenar vida, que Zoltan conozca el origen del efecto o que el agua lo produzca por sí sola.')
fact(106,'Ione encuentra un collar y acude al grito de Citlali','01:01:00.160','01:03:21.159','01:02:01.440',
     'Ione revisa una choza cercana a la que inspecciona Eleanor para buscar algo útil en la jungla. Encuentra un collar, lo toma y corre al oír los gritos, creyendo que hay una emergencia. Citlali se queja de la poca ropa de Zoltan. El recién rescatado termina apoyado junto a un árbol, mientras ella mantiene los ojos cubiertos por desconfianza.',
     ['Ione','Citlali','Zoltan','Eleanor','Collar hallado por Ione en la aldea caníbal','Aldea caníbal de la cascada'],
     'El hallazgo no establece todavía material, procedencia, precio o magia del collar. No se fusiona con los collares de Blink, Leo o las misiones anteriores.')
fact(107,'Ione descubre al tiranosaurio y no consigue apartar a Zoltan','01:03:21.160','01:06:48.999','01:06:18.000',
     'Ione es la primera en ver movimiento entre los árboles detrás de Zoltan. Los pasos se acercan y aparece un enorme tiranosaurio observando al grupo. Intenta tomar al hombre de la nuca y apartarlo del peligro, pero él interpreta el gesto como una posible agresión y se pone en guardia. Al tocarlo, Ione recibe un chispazo que le recorre el cuerpo y la obliga a soltarlo. El intento de apartarlo fracasa y comienza el combate.',
     ['Ione','Zoltan','Eleanor','Citlali','Tiranosaurios de la aldea caníbal','Aldea caníbal de la cascada'],
     'Zoltan no accede sin reservas a la maniobra de rescate. La descarga no se presenta como un ataque deliberado suyo contra Ione, y el dinosaurio no se identifica con el cañoneado en otra expedición.')
fact(108,'Ione salta entre las palmeras y golpea con Negociación','01:06:49.000','01:10:59.158','01:10:06.320',
     'Ione se lanza hacia la jungla y rebota entre las palmeras para llegar a la boca del tiranosaurio. Gasta inspiración y consigue golpearlo. Intenta empujarlo con el impacto, pero el director rechaza el desplazamiento por la diferencia de tamaño. Al caer vuelve a atacar sus patas y utiliza cargas de Negociación para añadir daño. Después se aparta y lo provoca para que vaya a por ella.',
     ['Ione','Negociación','Tiranosaurios de la aldea caníbal'],
     'El intento de empujar o aturdir con la descripción del primer golpe no se conserva como un desplazamiento o aturdimiento logrado. Las cargas de Negociación son distintas de la inspiración empleada.')
fact(109,'El mordisco hiere a Ione y una barrera eléctrica protege a Zoltan','01:10:59.159','01:12:31.959','01:12:02.760',
     'El tiranosaurio persigue a Ione y la alcanza con un mordisco que causa una herida grave. Con la cola intenta golpear a Zoltan. El hombre se protege instintivamente y de él surgen rayos que forman una pantalla o escudo eléctrico: el coletazo golpea contra esa barrera en vez de alcanzarlo.',
     ['Ione','Zoltan','Tiranosaurios de la aldea caníbal'],
     'Zoltan no entiende todavía cómo produce la defensa. El escudo eléctrico es una manifestación mágica, sin convertirlo en una pieza física recogida o adquirida.')
fact(110,'Un segundo tiranosaurio llega atraído por un olor','01:12:31.960','01:13:10.119','01:12:46.560',
     'Se oyen nuevos pasos y por otro lado de la jungla aparece un segundo tiranosaurio. El director lo describe olfateando y atraído por un olor. Se acerca corriendo al grupo, que queda amenazado por dos grandes animales.',
     ['Tiranosaurios de la aldea caníbal','Ione','Zoltan','Citlali','Eleanor','Aldea caníbal de la cascada'],
     'No se identifica qué olor lo atrae, ni una relación de pareja o parentesco entre los dinosaurios. Que aparezcan dos no prueba una población o un mando que los dirija.')
fact(111,'Zoltan quita la reacción a un dinosaurio, pero el otro lo muerde','01:13:10.120','01:16:36.638','01:14:56.639',
     'Zoltan intenta canalizar deliberadamente la electricidad mediante un contacto electrizante. Acierta al primer dinosaurio y le impide reaccionar, con lo que decide alejarse. Sin embargo, el segundo sigue pudiendo atacar y tiene alcance suficiente: cuando el hombre sale corriendo, lo alcanza con un mordisco que lo deja muy herido pese al intento de protegerse.',
     ['Zoltan','Ione','Tiranosaurios de la aldea caníbal'],
     'La electricidad retira la reacción a un rival, no a ambos. La discusión de distancia y defensa se resuelve con el segundo mordisco acertado; no se conserva como una retirada sin consecuencias.')
fact(112,'Citlali evoca los dados de Nox al golpear con las chanclas','01:16:36.639','01:18:36.519','01:17:32.120',
     'Citlali combate con sus chanclas. Cuando falla un ataque, la escena se adorna con unos dados que giran alrededor de la alpargata y un canto, al utilizar el recurso de suerte. Ella recuerda que aquellos daditos eran de su Nox. La repetición consigue impactar y continúa golpeando en sus acciones siguientes.',
     ['Citlali','Nox','Tiranosaurios de la aldea caníbal'],
     'La evocación y la representación de la suerte no demuestran el regreso de Nox, un espíritu que intervenga o la aparición de un objeto físico transferido desde él. No se inventa una resurrección por ese recuerdo.')
fact(113,'La transformación de Eleanor infunde miedo a uno de los rivales','01:18:36.520','01:20:51.999','01:19:07.760',
     'Eleanor utiliza su transformación y uno de los tiranosaurios falla la salvación, quedando asustado dentro de su aura y sin poder alejarse en la resolución acordada. La transformación consume su acción. Considera reforzarse con escudo de fe antes de resolver otra opción de su turno.',
     ['Eleanor','Tiranosaurios de la aldea caníbal'],
     'La protección de escudo de fe se plantea, pero el diálogo cambia de opción sin una confirmación verbal inequívoca de su lanzamiento. El impacto posterior no identifica con claridad el arma o efecto empleado. El miedo tiene duración limitada, corregida después, no seis turnos garantizados.')
fact(114,'Ione se cura y adopta una defensa paciente','01:20:52.000','01:22:09.279','01:21:43.600',
     'Muy herida, Ione se lleva una mano al pecho y utiliza una curación para evitar caer con otro ataque. Cambia de posición y decide emplear su acción en una defensa paciente, manteniendo los puños en alto y preparada ante la siguiente acometida.',
     ['Ione','Tiranosaurios de la aldea caníbal'],
     'La curación no fija una recuperación completa. La asignación de acción y acción adicional se corrige en mesa antes de conservar la defensa como resolución del turno.')
fact(115,'Los tiranosaurios siguen atacando a los compañeros','01:22:09.280','01:24:56.879','01:24:04.520',
     'Un tiranosaurio falla el coletazo contra Ione mientras ella se protege y busca después alcanzar a Zoltan. El otro ataca a Citlali, afectado por el miedo de Eleanor, y aun así logra morderla. Una réplica de un compañero alcanza al dinosaurio cuando ataca a un aliado cercano. El coletazo que sigue no consigue impactar.',
     ['Tiranosaurios de la aldea caníbal','Ione','Citlali','Zoltan','Eleanor'],
     'La réplica no tiene hablante inequívocamente identificado en la transcripción de este intervalo y se conserva sin dueño. El intento de mordisco contra Zoltan no permite fijar un resultado adicional con la misma claridad que el ataque a Citlali.')
fact(116,'Un rayo de Zoltan alcanza a ambos dinosaurios antes de teletransportarse','01:24:56.880','01:28:53.399','01:28:17.560',
     'Zoltan ve a los dos dinosaurios alineados y prepara un rayo más potente. Se le eriza el pelo y aparecen chispas a su alrededor. La descarga alcanza a ambos, que fallan sus salvaciones y reciben daño. Después utiliza un paso brumoso para teletransportarse y salir de la zona inmediata del peligro.',
     ['Zoltan','Tiranosaurios de la aldea caníbal'],
     'Las repeticiones del lanzamiento para colocar y configurar el efecto son ajustes de interfaz: no se convierten en varios rayos ejecutados o en una pérdida definitiva de todos sus espacios de conjuro. No se describe una muerte todavía.')
fact(117,'Citlali usa una chancla cargada, pero el animal resiste el empuje','01:28:53.400','01:31:03.559','01:30:20.320',
     'Citlali elige una de sus chanclas con cargas y ataca a distancia a uno de los tiranosaurios pese a tener un enemigo cerca. Acierta, pero la criatura supera la fuerza necesaria para resistir el intento de empujarla. Continúa con un golpe normal a otro blanco cercano y falla el intento adicional.',
     ['Citlali','Tiranosaurios de la aldea caníbal'],
     'La broma de llamarla Nike no es un nombre propio canónico del arma. El intento de empujar diez pies no se resuelve como un desplazamiento logrado.')
fact(118,'Eleanor continúa el combate cuerpo a cuerpo','01:31:03.560','01:31:53.799','01:31:23.560',
     'Eleanor emplea su turno en atacar a los tiranosaurios con sus dos ataques. El segundo falla según la resolución verbal del director, mientras sus compañeros preparan las acciones siguientes.',
     ['Eleanor','Tiranosaurios de la aldea caníbal'],
     'La transcripción no verbaliza con la misma claridad el resultado del primer golpe ni una muerte atribuible a este turno. Se evita inventar un golpe divino o un daño concreto.')
fact(119,'Ione aturde a un tiranosaurio y el otro supera la salvación','01:31:53.800','01:36:21.118','01:33:20.960',
     'Ione se aproxima para golpear por debajo de la barbilla y consigue aplicar un golpe aturdidor a uno de los tiranosaurios. Cambia de posición y golpea al otro, esta vez con los puños normales porque ha agotado las cargas de Negociación. El segundo animal supera la salvación. El director aclara que el miedo de Eleanor ya ha terminado. Ione se aparta: el rival aturdido pierde su acción, pero el otro continúa intentando morder y golpear con la cola.',
     ['Ione','Negociación','Eleanor','Tiranosaurios de la aldea caníbal'],
     'No se conservan dos aturdimientos por la forma plural de una recapitulación: el segundo superó expresamente la salvación. Las cargas agotadas no implican la destrucción de Negociación. Los blancos y efectos de las acometidas finales no se verbalizan suficientemente para asignarles nuevas heridas concretas.')
fact(120,'El segundo rayo de Zoltan mata a uno y deja al otro muy herido','01:36:21.119','01:37:36.149','01:37:25.040',
     'Zoltan prepara otro rayo y lo alinea contra los dos tiranosaurios. El que está aturdido falla automáticamente la salvación en la resolución de mesa y el otro también la falla. El director confirma que uno muere y el otro queda bastante herido.',
     ['Zoltan','Ione','Tiranosaurios de la aldea caníbal'],
     'La confirmación distingue una muerte y un superviviente herido, sin fijar inequívocamente cuál de los dos animales es el muerto por su posición anterior. La acción adicional anunciada después se integra con la continuación de la sesión.')


def stage(title,text,*refs):
    return {'titulo':title,'texto':text,'referencias':list(refs)}


stages=[
    stage('Aire limpio, ropa y tesoros',
          'Citlali ayuda a Zoltan a levantarse y salir del hedor de la cueva. Él no sabe cuánto tiempo ha pasado entre aquellos cadáveres. Mientras lo acompaña hacia el agua para limpiarse, Eleanor inspecciona la choza mayor: hay un trono de pieles, calaveras, cuernos y un suelo cubierto de piel humana. Entre los cofres encuentra una copa dorada con inscripciones y joyas, distinta de la que ya llevaba y destinada al intercambio como tesoro. Zoltan se baña y bucea sin hallar nada especial. Citlali espera dándole la espalda, busca una piel que no sea humana para vestirlo y se presenta. Cuando se dan la mano, la humedad que él conserva descarga electricidad sobre ella. Citlali grita y se aparta; Zoltan percibe el chispazo sin entenderlo. Ione encuentra un collar en otra choza y acude pensando que alguien necesita ayuda.',
          '46-101','46-102','46-103','46-104','46-105','46-106'),
    stage('Un rescate interrumpido por los dientes',
          'Ione ve los árboles moverse detrás de Zoltan y descubre un enorme tiranosaurio. Intenta apartarlo de la nuca, pero el hombre interpreta el gesto como una amenaza y otra descarga obliga a soltarlo. La pirata se lanza al combate, salta entre las palmeras para golpear la boca y aterriza atacando las patas con Negociación. No consigue empujarlo por su tamaño. Lo provoca para atraerlo y el animal responde con un mordisco que la deja muy herida. Su cola busca a Zoltan, pero él se cubre instintivamente y forma una barrera eléctrica que contiene el golpe. Otro tiranosaurio llega olfateando desde la jungla. Zoltan consigue impedir la reacción del primero con un contacto eléctrico y trata de salir, pero el segundo lo alcanza con un mordisco durante la retirada.',
          '46-107','46-108','46-109','46-110','46-111'),
    stage('Miedo, curación y una línea de relámpagos',
          'Citlali entra en la lucha con sus chanclas. Al repetir un golpe fallido mediante la suerte, unos dados giran alrededor de la alpargata en la descripción y ella recuerda a Nox. Eleanor se transforma e infunde miedo a uno de los animales, que queda limitado por su aura. Ione se cura, cambia de posición y adopta una defensa paciente que le permite evitar un coletazo. El otro dinosaurio consigue morder a Citlali pese al miedo. Zoltan aprovecha que ambos enemigos están alineados: su pelo se eriza, las chispas lo rodean y descarga un rayo contra los dos. Los alcanza y después utiliza un paso brumoso para ponerse a salvo de sus bocas.',
          '46-112','46-113','46-114','46-115','46-116'),
    stage('Un animal cae bajo el segundo rayo',
          'Citlali vuelve a utilizar una chancla cargada, pero el tiranosaurio aguanta el empuje que pretendía desplazarlo. Eleanor sigue atacando mientras Ione busca otra oportunidad. La pirata golpea bajo la barbilla de uno y logra aturdirlo. Después se mueve hacia el otro y continúa con los puños: las cargas de Negociación se han agotado y ese rival resiste el segundo intento de aturdimiento. El miedo provocado por Eleanor también termina. El animal todavía activo sigue acometiendo, pero Zoltan prepara otro rayo que atraviesa a los dos. Ninguno evita la descarga y el director confirma que uno muere, mientras el otro queda muy herido. El combate aún exige resolver qué harán con el superviviente.',
          '46-117','46-118','46-119','46-120')
]

histories=[]


def history(name,kind,title,text,refs,new=False,description='',note=''):
    histories.append({'nombre':name,'tipo':kind,'nueva':new,'descripcion':description,'nota':note,
                      'etapas':[stage(title,text,*refs)]})


history('Ione','personaje','Negociación contra los tiranosaurios',
        'Ione registra una choza y encuentra un collar antes de acudir a los gritos de Citlali. Es la primera en advertir al tiranosaurio e intenta apartar a Zoltan, pero el contacto eléctrico lo impide. Se lanza entre las palmeras para golpearlo y utiliza Negociación, recibiendo a cambio un mordisco grave. Se cura y adopta una defensa paciente. Más tarde aturde a uno de los animales y continúa a puño limpio cuando se agotan las cargas de su arma; el otro resiste su intento.',
        ['46-106','46-107','46-108','46-109','46-114','46-119'])
history('Citlali','personaje','Cuidar al rescatado y recordar la suerte de Nox',
        'Citlali ayuda a Zoltan a salir de la cueva, lo acompaña al agua y busca una piel para que se vista. Su pudor la mantiene con los ojos apartados, pero al presentarse y darle la mano recibe una dolorosa descarga de origen eléctrico. Durante la acometida de los tiranosaurios combate con sus chanclas. El recurso de suerte evoca unos dados y el recuerdo de Nox, sin mostrar su regreso. Recibe un mordisco y continúa intentando golpear y desplazar a los animales.',
        ['46-101','46-103','46-104','46-105','46-112','46-115','46-117'])
history('Eleanor','personaje','La copa del jefe y el aura de miedo',
        'Eleanor inspecciona la choza mayor de la aldea y encuentra una copa dorada con joyas e inscripciones. La compara con la que llevaba y comprueba que son objetos distintos. Al llegar los tiranosaurios se transforma e infunde miedo a uno, limitándolo durante parte del combate. Después continúa atacando. El miedo termina conforme a la corrección de la mesa, sin prolongarse durante todos los turnos que se habían supuesto.',
        ['46-102','46-107','46-113','46-118','46-119'])
history('Zoltan','personaje','Una electricidad que aún no comprende',
        'Tras salir de la cueva con ayuda de Citlali, Zoltan se baña y acepta la ropa que ella encuentra. El apretón de manos desencadena electricidad dolorosa para la anciana; después ocurre algo semejante cuando Ione intenta apartarlo del tiranosaurio. No entiende todavía esos efectos. Ante el coletazo forma instintivamente una barrera de rayos. Intenta controlar la electricidad con un contacto que impide reaccionar a un enemigo, aunque el segundo lo muerde al alejarse. Muy herido, descarga dos rayos contra ambos dinosaurios y se teletransporta para protegerse. El último rayo mata a uno y deja al otro herido.',
        ['46-101','46-103','46-104','46-105','46-107','46-109','46-111','46-116','46-120'],True,
        'Hombre rescatado de la cueva que manifiesta una electricidad que todavía no sabe explicar.',
        'Nombre presentado como Zoltan. Sus variantes de transcripción no crean identidades distintas; la descarga por contacto y la barrera instintiva no demuestran origen, linaje o patrón determinados.')
history('Negociación','objeto','Cargas agotadas entre las palmeras',
        'Ione emplea las cargas de Negociación al golpear al tiranosaurio después de saltar entre las palmeras. El arma añade daño a sus ataques, sin superar por ello la limitación de tamaño que impide empujarlo. Más tarde agota las cargas disponibles y continúa con los puños normales para intentar aturdir a los animales. El gasto de recursos no implica que las nudilleras desaparezcan o queden destruidas.',
        ['46-108','46-119'])
history('Tiranosaurios de la aldea caníbal','personaje','Dos depredadores atraídos hacia los viajeros',
        'Un enorme tiranosaurio aparece detrás de Zoltan mientras los viajeros registran la aldea. Ione se enfrenta a él y recibe una grave mordedura. Otro llega después siguiendo un olor no identificado. Ambos atacan con dientes y cola; ni la protección eléctrica, el miedo ni los intentos de retirada evitan todos los golpes. Un primer rayo de Zoltan los hiere y otro, tras el aturdimiento de uno, mata a un animal y deja al otro muy dañado.',
        ['46-107','46-108','46-109','46-110','46-111','46-113','46-115','46-116','46-117','46-119','46-120'],True,
        'Dos grandes tiranosaurios que atacan a los viajeros junto a la aldea de la cascada.',
        'Ficha colectiva descriptiva sin nombres individuales, sexo o relación familiar confirmados. No se los identifica con dinosaurios de expediciones anteriores por pertenecer a la misma especie.')
history('Aldea caníbal de la cascada','lugar','Botín entre casas y una amenaza desde la jungla',
        'Los viajeros salen de la cueva de cadáveres y revisan las chozas. La mayor contiene una silla de apariencia señorial, huesos, calaveras, piel humana y una copa dorada; en otra Ione encuentra un collar. El agua cercana permite a Zoltan limpiarse y Citlali consigue una piel no humana para vestirlo. Los movimientos de los árboles anuncian la llegada de dos tiranosaurios, que convierten el registro y el descanso en un combate peligroso.',
        ['46-101','46-102','46-103','46-104','46-106','46-107','46-110'],True,
        'Aldea de chozas próxima a la cascada donde el grupo registra restos de ocupación caníbal y sufre el ataque de dos tiranosaurios.',
        'Nombre editorial descriptivo. No se fusiona con aldeas visitadas en capítulos anteriores sin una identificación expresa.')
history('Copa dorada de la choza del jefe','objeto','Un tesoro distinto del anterior',
        'Eleanor encuentra la copa en la choza grande entre cofres, huesos y pieles. Su superficie parece dorada y tiene inscripciones y joyas. La compara con otra copa que ya llevaba, pero el director las distingue y describe esta como tesoro para vender. No se revela el significado de sus inscripciones ni se ejecuta con ella un ritual.',
        ['46-102'],True,
        'Copa de apariencia dorada con inscripciones y joyas que Eleanor recoge de la choza mayor.',
        'Objeto nuevo y explícitamente diferente de la copa anterior de Eleanor. Una etiqueta de la tabla de tesoro no demuestra por sí sola poderes rituales.')
history('Collar hallado por Ione en la aldea caníbal','objeto','El hallazgo antes de los gritos',
        'Mientras Eleanor revisa la choza mayor, Ione busca objetos útiles en una casa cercana y encuentra un collar. Lo toma y sale corriendo al oír los gritos de Citlali, dejando su examen para después. El momento del hallazgo no aporta todavía un origen, material o poder.',
        ['46-106'],True,
        'Collar encontrado por Ione al registrar una choza de la aldea próxima a la cascada.',
        'Se conserva separado de los collares de Blink, Leo y las expediciones antiguas. Su valoración posterior debe enlazarse con el resto de esta misma sesión.')

delivery={'bloque':2,'lectura_completa':True,'primer_segmento':'c002291','ultimo_segmento':'c004581',
          'cobertura_lectura':[{'desde_indice':0,'hasta_indice':289},{'desde_indice':290,'hasta_indice':579},{'desde_indice':580,'hasta_indice':869},{'desde_indice':870,'hasta_indice':1145}],
          'etapas':stages,'afirmaciones':facts,'historias_entidades':histories,
          'misiones':[
              'Salir del refugio y atender a Zoltan: Citlali lo ayuda a caminar, lo acompaña al baño y le busca ropa. Las descargas de contacto abren una nueva incertidumbre sobre sus capacidades (46-101, 46-103–46-105).',
              'Aprovechar el registro de la aldea: Eleanor obtiene una copa distinta de la anterior e Ione recoge un collar. La presencia de pieles y huesos no identifica por sí sola a todos los antiguos ocupantes o víctimas (46-102, 46-106).',
              'Sobrevivir a los tiranosaurios: los cuatro viajeros resisten mordiscos y coletazos con curación, defensa, miedo, electricidad y aturdimiento. Un dinosaurio muere al segundo rayo de Zoltan y el otro sigue vivo y herido en esta fase (46-107–46-120).'
          ],
          'preguntas':[
              '¿Qué origen tiene la electricidad de Zoltan y cómo aprenderá a controlar las descargas involuntarias? El contacto hiere a dos compañeras y su barrera surge sin que él la comprenda (46-105, 46-107, 46-109, 46-111).',
              '¿Qué tiempo y circunstancias exactas rodean el encierro de Zoltan y los cadáveres de la cueva? Él no sabe fijar cuánto ha permanecido allí (46-101).',
              '¿Qué significan las inscripciones de la copa y cuál es su procedencia? Se encuentra como tesoro distinto de otra copa previa, sin un rito o una lectura completa (46-102).',
              '¿Qué ocurrirá con el tiranosaurio superviviente y qué destino tendrá el collar de Ione? Son propuestas que deben cotejarse con el desenlace de esta misma sesión antes de dejarse como asuntos pendientes (46-106, 46-120).'
          ],
          'contradicciones':[
              'La nueva copa de Eleanor es expresamente distinta de la que ya llevaba. La etiqueta de copa de rituales en la tabla de tesoro no acredita un efecto mágico o un rito ejecutado (46-102).',
              'Citlali encuentra para Zoltan una piel que no es humana, aunque el suelo de la choza mayor sí contiene piel humana. No se convierten en la misma prenda o víctima (46-102, 46-104).',
              'La descarga sobre Citlali y la que obliga a Ione a soltar a Zoltan no se presentan como ataques deliberados contra sus compañeras. El poder defensivo también sorprende al propio Zoltan (46-105, 46-107, 46-109).',
              'Ione quiere empujar al primer tiranosaurio y Citlali intenta desplazar a otro, pero ambos intentos se rechazan o resisten. No se conservan como movimientos conseguidos (46-108, 46-117).',
              'Los dados evocan a Nox al usar la suerte de Citlali. La descripción no demuestra su regreso físico o espiritual ni transfiere un objeto de su cadáver a la anciana (46-112).',
              'El miedo de Eleanor tiene un final corregido y un rival supera el segundo intento de aturdimiento. La recapitulación plural no se usa para mantener a los dos dinosaurios inmovilizados o asustados de forma indefinida (46-113, 46-119).',
              'Las repeticiones y ajustes de los rayos son manejo de la interfaz. El bloque muestra dos descargas efectivas sobre ambos dinosaurios, de las que la segunda mata a uno y deja al otro herido (46-116, 46-120).',
              'El comentario de que un drow maneja al tiranosaurio es una broma sobre el director de juego y no una prueba de control mental por un personaje del mundo (46-115).'
          ],
          'nombres_dudosos':[
              'Zoltan es el nombre presentado; Zoltán, Zortán, Toltan, Solta y variantes de reconocimiento se integran por la continuidad del rescatado y sus efectos eléctricos (46-101, 46-103–46-107, 46-109, 46-111, 46-116, 46-120).',
              'Citlali, Sitlali y Mamá son la misma persona. Ione y Eleanor son dos compañeras distintas: la primera usa Negociación y la segunda inspecciona la choza del jefe e infunde miedo (46-102, 46-104, 46-106, 46-108, 46-113).',
              'Los dos tiranosaurios carecen de nombres y no se identifica su sexo o parentesco. No se fusionan con un ejemplar atacado por cañones en otra expedición (46-107, 46-110, 46-120).',
              'Nike y las deformaciones de alpargata son bromas o variantes de las chanclas de Citlali. No fijan aquí un nombre propio nuevo de arma, mientras Negociación sí conserva su identidad catalogada (46-108, 46-112, 46-117, 46-119).',
              'La aldea de la cascada, su cueva de cadáveres y los tesoros reciben etiquetas descriptivas. No se les asignan topónimos o relaciones con otros asentamientos por semejanza (46-101–46-106).'
          ],
          'continuidad':[
              {'pregunta_id':'P42-001','nota':'La evocación de Nox durante el recurso de suerte no aporta un cuerpo recuperado, una supervivencia o una escena posterior al estallido; se mantiene como recuerdo de Citlali.','referencias':['46-112']},
              {'pregunta_id':'P42-006','nota':'Ione combate junto a Citlali y Eleanor y utiliza Negociación. Este bloque no muestra el uso de la moneda de Bonnie, nuevas órdenes a la tripulación o una localización de Nox.','referencias':['46-106','46-108','46-114','46-119']},
              {'pregunta_id':'P43-003','nota':'Citlali llama suyo a Nox al evocar los dados, pero no se reconstruyen los años entre Amaru y la vida adulta del pirata. Zoltan no se identifica con él por bromas de parecido.','referencias':['46-101','46-112']},
              {'pregunta_id':'P43-004','nota':'La descarga sufrida por Citlali tiene una explicación eléctrica ligada al contacto con Zoltan. No se atribuye aquí a su absorción vital o a una activación de los símbolos del ser serpentino.','referencias':['46-105','46-112','46-117']}
          ]}

assert len(rows)==1146 and rows[0]['id']=='c002291' and rows[-1]['id']=='c004581'
assert len(facts)==20
assert all(seconds(f['inicio'])<=seconds(f['evidencia_cue']['inicio'])<=seconds(f['fin']) for f in facts)
write_json(ROOT / 'campanas/xoltacan/revision/borradores/46/entrega_2.json',delivery)
print(f'Entrega 2: {len(facts)} evidencias validadas, {len(stages)} etapas, {len(histories)} historias; '+str(sum(len(s['texto'].split()) for s in stages))+' palabras de relato.')
