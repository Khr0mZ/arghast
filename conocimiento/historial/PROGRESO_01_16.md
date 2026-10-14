# Progreso de reconstrucción

Objetivo activo: revisar los 39 capítulos disponibles y terminar la base de conocimiento, con evidencia temporal, seguimiento de tramas y distinción de perspectiva. El usuario pidió continuar hasta completarlo, sin aprobaciones por capítulo.

## Estado de trabajo

- Capítulo 1: leído completo, 35 registros con citas verificadas.
- Capítulo 2: leído completo, 29 registros con citas verificadas. Se recuperaron separadamente los pasajes 01:20–01:26 y 02:16–02:22 que se habían truncado en la salida de lectura.
- Capítulo 3: leído completo en cuatro tramos sin truncamiento, 31 registros con citas verificadas.
- Capítulo 4: leído completo en cuatro tramos sin truncamiento, 31 registros con citas verificadas.
- Capítulo 5: leído completo en tramos 0–40, 40–80, 80–120, 120–160 y 160–final sin truncamiento; 33 registros con citas verificadas.
- Capítulo 6: leído completo en tramos 0–40, 40–80, 80–120, 120–160 y 160–final, sin truncamiento; 38 registros con citas verificadas.
- Capítulo 7: leído completo en tramos 0–35, 35–75, 75–115, 115–155 y 155–final; 34 registros con citas verificadas.
- Capítulo 8: leído completo en tramos 0–35, 35–75, 75–115 y 115–final; 27 registros con citas verificadas.
- Capítulo 9: leído completo en tramos 0–35, 35–75, 75–115, 115–155 y 155–final; 33 registros con citas verificadas.
- Capítulo 10: leído completo en tramos 0–35, 35–75, 75–115, 115–155 y 155–final; 27 registros con citas verificadas.
- Capítulo 11: leído completo en tramos 0–35, 35–75, 75–115, 115–155, 155–195 y 195–final; 32 registros con citas verificadas.
- Capítulo 12: leído completo en tramos 0–35, 35–75, 75–115, 115–155 y 155–final; 32 registros con citas verificadas.
- Capítulo 13: leído completo en tramos 0–35, 35–75, 75–115 y 115–final; 26 registros con citas verificadas.
- Capítulo 14: leído completo en tramos 0–35, 35–75, 75–115, 115–155 y 155–final; 25 registros con citas verificadas.
- Capítulo 15: leído completo en tramos 0–40, 40–80, 80–120, 120–160 y 160–final; 22 registros con citas verificadas.
- Capítulo 16: leído completo en tramos 0–40, 40–80, 80–120 y 120–final; 21 registros con citas verificadas.
- Siguiente: leer capítulo 17 desde el inicio. Capítulos 17–39 pendientes de revisión editorial.
- Los 39 capítulos tienen originales y derivados; ningún episodio requiere Whisper por ausencia de VTT.

## Procedimiento de continuación

1. Leer `python scripts/leer.py N --desde MINUTO --hasta MINUTO`, en tramos de aproximadamente 45 minutos; no resumir a partir solo de búsquedas. Si una salida se trunca, volver a leer el tramo faltante.
2. Redactar `borradores/NN.json` siguiendo el esquema de 02.json. Este JSON es una ficha editorial manual compacta, no salida de extracción automática.
3. Ejecutar `python scripts/redactar.py borradores/NN.json`. Localiza cada ancla literal dentro del VTT y genera ficha JSON con hash, cita y cue original.
4. Ejecutar `python scripts/construir.py` para validar todas las fichas y producir los índices Markdown.
5. Actualizar este progreso, añadir contradicciones y resolver pistas con evidencia, sin borrar la versión previa.
6. Al completar los 39, consolidar identidades y relaciones verificadas, tramas resueltas y pendientes, conocimiento de Oghma, comprobar originales, probar reproducibilidad y regenerar `xoltacan_biblioteca.zip` incluyendo borradores y scripts, excluyendo `.venv` y `__pycache__`.

## Evidencias que seguir

- Ione: petición de cadenas y luna llena (01-019, 01-034); camarote destrozado y cadenas rotas (02-003), despierta desnuda en selva (02-007). **Forma licántropa confirmada posteriormente** al transformarse en la excavación (03-024 y descripción del director 03-031). Origen y explicación de los desperfectos no confirmados. Poncelot cree que un mago la maldijo, hipótesis distinta de la adjudicación.
- Nox propone ayuda nocturna a Ayoto por comida (02-023), sin especificar tarea; posible relación con Ione sin confirmar.
- Nox muestra zarpazo vendado (02-019); su autor no confirmado.
- Pirámides de oro: leyenda transmitida por Mamá (01-021); existencia y ubicación pendientes.
- Familia, reliquia y dragoncito de Erendriel: causas, nombres e identidad de reliquia pendientes.
- Tribu destruida de Chochi y tribu adoptiva de Ayoto: nombres y responsables pendientes.
- Ayoto = Tortas, Chochi = nombre posterior, Mamá = Citlali/Coyote, Nox = Naór: NO asumir equivalencias sin fuentes posteriores. Nox es el nombre literalmente presentado en los primeros episodios.
- Oghma y Jivirix: solo contexto del usuario por ahora. Su acceso a los hechos de capítulos 1–2 no está establecido.
- Capítulo 2: pulso adulterado por Nox, monedas y posible reclutamiento disputados; no se confirma membresía ni propiedad de personas.
- Capítulo 3: excavación de Marina descubierta, tres trabajadores abatidos y centinela llevado vivo por Nox (nombre candidato Jack). Objeto de excavación sin averiguar. Cautivo no entregado ni interrogado aún.
- Blink / Blank: hada liberada por Mamá, declara alternar ambos nombres. Procedencia de otro bosque/mundo sin plano identificado. Logra calmar y encantar temporalmente a Ione para retirar al grupo.
- Sir Poncelot: nombre explícitamente corregido por su jugador (03-018); conservar variantes fuente. Gnomo que considera caballo al dinosaurio Merlucilla. Proclamaciones de títulos/proezas y comparación de Mamá con Titania no se convierten en canon literal.
- Citlali: mención directa del director en 03-013 refuerza Mamá = Citlali; Coyote aún no confirmado.
- Merlucilla: muerte relatada entre sesiones por la jugadora de Ione en 04-003; no reescribir el cierre vivo de 03-031. Cadáver y cuerda encontrados después (04-009). Poncelot no participa en el 4; reacción pendiente.
- Hombres de Bonnie: dos cadáveres y superviviente hallados entre ruinas; superviviente auxiliado por Patata y luego muerto en emboscada de dinosaurios (04-013–04-018). Son piratas diferentes de los marines muertos en capítulo 3.
- Collar antiguo: visitante lo toma de cadáver, Ione lo toma después y extrae gemas para compañeros (04-020–04-021); entrega collar vacío a Bonnie, que no la cree y ordena buscar gemas (04-029). Patata entrega su gema a encargada de Sirena Borracha para alojamiento (04-030). No hay tasación ni saldo de deuda confirmado.
- Ione y visitante: acuerdo reservado de futuros tesoros 50/50, tras Detectar pensamientos de él; Nox no está informado (04-022). Bonnie dice a Ione que no hable demasiado con Nox, razón pendiente (04-029).
- Criatura divina translúcida de Mamá, cabeza de jaguar/cuerpo de gorila/cola de mono, aparece por efecto de fruta y quiere soltar a Ione. Mamá insiste en equilibrio. Solo se acredita percepción de Mamá; dios sin nombre (04-024).
- El Garfio: costa con esa forma nombrada por el director (04-001).
- La expedición del 4 NO llega a la mina; vuelve tras persecución de dinosaurio volador (04-025). Termina con intención de buscar a Nox, sin encuentro (04-031).

## Notas de lectura del tramo inicial del capítulo 5

Se conservan como notas del trabajo inicial. La ficha del capítulo 5 ya está cerrada y sus registros validados; consultar `conocimiento/capitulos/05.md` para las conclusiones revisadas y sus límites.

- 00:00–00:02: Nox recapitula que llevó al marine al poblado y habló con él y Bonnie; nombre alterna Jack/Jacky/Jack Jackson/Jackie Johnson. Ione recapitula ocultación de rastros de sus transformaciones en selva. Se trata de actividades entre sesiones.
- 00:02–00:04: visitante prepara trampas para sacar negocio de pieles de reptiles. Erendriel duerme en copas de árboles e investiga alrededores, evitando alojamiento del puerto.
- 00:04–00:08: marine quiere volver con su esposa Lucy; Nox lo presenta como nuevo integrante y exmarine, pero su consentimiento no consta y quiere reunirse con su mujer. Director corrige que Kilzer NO estuvo en la mina del capítulo 3. No atribuirle recuerdos de esa escena.
- 00:08–00:14: el elfo identifica por emblema una relación mercantil/cofradía de Puerto de Espadas. El marine declara que encontraron un collar en las minas. Visitante niega saber del collar, Nox inicialmente le cree y el elfo detecta dudas. Esto añade declaración de procedencia al collar recuperado de piratas, todavía sin excavación presenciada por grupo del 4.
- 00:14–00:18: Ione habla de sus limpiezas en jungla; el marine aclara que vio al lobo, no necesariamente vínculo entre mujer y lobo. Nox lo llama salvoconducto para parlamento. Llega buque de la Marina; el elfo murmura Otra vez no y muestra anillo.
- 00:18–00:25: Bonnie ordena apartar al marine a la selva (director aclara ocultarlo/retenerlo, no matarlo). Dice haber subcontrato con capitana que permite permanecer por diezmo y encarga a Nox e Ione colarse en barco para retirar documentos firmados mientras ella recibe la bronca de capitana. Firma indicada en cartel de Ron. No observar contrato todavía; es encargo y declaración de Bonnie.
- 00:25–00:28: Nox relata romance con mujer que creía llamada Marina y luego descubrió Molly, capitana de Marina; dice que la dejó en isla con pistola al enterarse. Confesión de personaje, no escena pasada presenciada. Relación de Molly con buque se infiere de charla y reacción, validar siguientes pasajes.
- 00:28–00:34: el elfo muestra anillo familiar círculo/X/gema roja, critica imperio y cambia pelo a verde con flores al alterarse. Marine defiende minería para bien del imperio. Nox toma ropa de marine y le entrega la suya; argumenta que no lo llevarán a casa. Ofrece a compañeros oro/documentos como incentivo para infiltrarse. Marine se aleja vestido de pirata; no se muestra su muerte.
- 00:34–00:40: capitana desembarca con escolta, gorro negro/casaca roja. Ione arrastra a Nox con cesta como borracho; capitana los desprecia y sigue a taberna sin reconocerlo explícitamente. Se reúnen en muelle y planean llegar al barco sin que los soldados los vean; idea final de tortugas marinas.
- Para leer nombres y acentos correctamente en consola, usar Python con `-X utf8` en siguientes lecturas.

## Notas de lectura del tramo inicial del capítulo 6

Estas notas se conservan como historial de lectura; la ficha 06 ya está cerrada y validada. Consultar `conocimiento/capitulos/06.md` para las conclusiones y su evidencia.

- 00:00–00:05: nueva tirada de sucesos al dormir cerca del poblado. Blink, Ione y Poncelot reciben obsidianas; visitante pierde cuatro monedas y Chochi encuentra cuatro. Valuaciones de inventario: venta inicialmente mitad del precio indicado, regateo permitido; registrar como mecánica de la mesa, no economía universal. El visitante no sabe quién tomó/perdió su dinero; no llamar ladrón a Chochi solo por transferencia narrada.
- 00:06–00:08: Blink relata molestar a sus dos captores entre sesiones y buscarlos porque desaparecieron hace días. Ione relata que Bonnie halló una gema que Patata entregó a Lizy y le ordena obtener de vuelta las gemas que repartió. Confirma avance de búsqueda anunciada 04-029; no recuperadas aún.
- 00:08–00:10: visitante estudia rutas para huir a otro pueblo, pero no sabe atravesar jungla. Chochi relata que por la apuesta acabó en tripulación de Ione, medita y vuelve al poblado para acostumbrarse. Autorreporte añade resolución parcial de pertenencia que era disputada en 02-026–02-029; no extender a pertenencia del visitante.
- 00:10–00:14: Blink ve a Ione medio metida en pozo de suciedad e intenta sacarla; recuerda episodio de trampa. Ione no recuerda bien la noche previa tras transformación; conservar límites.
- 00:14–00:18: visitante ve a encargada Sirena Borracha con gema idéntica a su gema guardada. Ella dice cliente le pagó; explica que recolectores y Bonnie suministran alimentos y que Bonnie controla entradas/salidas. Declaración de encargada, no lectura administrativa independiente. Chochi se presenta como humano joven, dice que nombre completo solo se reserva para jefes de aldea, no lo revela.
- 00:18–00:24: Poncelot recapitula buscar Merlucilla creyendo que escapó al hallar cuerda rota. No sabe todavía que Ione la comió; no atribuirle ese conocimiento. Encontró a Nox tratando de recuperar lobo y por indicación llevó unos piratas atados al juzgado; él interpreta Sirena Borracha como juzgado y a Liz como jueza. Liz le cobra únicas diez monedas para audiencia con majestad Bonnie y le encarga limpiar lo que él llama mazmorra; sale con cubo y mocho que cree casco/lanza. No hacer de Liz jueza oficial por esa interpretación.
- 00:24–00:30: visitante quita cubo de la cabeza de Poncelot; gnomo cree que levantó maldición. Le pide baño para quitar suciedad. Poncelot ve a Ione atascada en pozo y a Blink tirando del pelo; identifica erróneamente hada como enemigo y ayuda a sacar a Ione.
- 00:30–00:34: Ione dice que acabó así por pelea contra semiorcos del poblado, sin escena representada. Poncelot e Ione van a bañarse; ella dice tener misión secreta de reina del pueblo, guiando su interpretación caballeresca. Blink se esconde en rastas de Ione.
- 00:34–00:40: ambos se desnudan y se bañan en mar, Ione lo presenta como entrenamiento al desnudo; visitante y Chochi reaccionan y desean beber. Chochi confunde mar con lago salado. No concluir que desconoce todos los mares permanentemente.

## Consecuencias documentadas del capítulo 5

- Lunaria / Luna: kender nueva PJ, no Blink/Blank. Dice ser pequeña y no niña; edad no fijada. Barco abordado y posibles compañeros perdidos según su relato; se suelta y ayuda a Nox por oferta de alojamiento/comida (05-015–05-016).
- Jack / Jackie: el cautivo del 3, apellido oscila Jackson/Johnson, esposa declarada Lucy. Desea volver a casa, no consentir tripulación; Bonnie manda apartarlo de vista de capitana, no matarlo (05-003, 05-007, 05-011). Se aleja vestido de pirata, destino pendiente.
- Molly: capitana actual con relación pasada confesada por Nox (05-009); contrato con Bonnie por diezmo relatado por ella (05-008) y papel firmado encontrado por Nox (05-024). No afirmar anulación legal por sustracción.
- Objetivo documental cumplido y entrega a Bonnie (05-024, 05-030); consecuencias negativas: incendio verdadero por vela del visitante, tras ilusión de fuego de Lunaria (05-028–05-029), explosión vista (05-032), aumento de deuda y trabajos especiales anunciados por Bonnie (05-031). No saldo de deuda, víctimas o hundimiento total confirmados.
- Nota escrita por Nox para Molly queda en compartimento; no se lee texto y Nox lamenta que quizá no la lea tras incendio. Contenido y suerte pendientes (05-024, 05-032).
- Erendriel conserva dos mapas y papeles, carteles de búsqueda de Nox/Ione y pistola tomada de armería. En cierre habla de investigación y familia, nombre preferido mal reconocido, no fijar nuevo alias todavía (05-010, 05-021, 05-023–05-024, 05-033).
- Nox y los piratas conocen misión contractual; compañeros no la conocen aunque ayuden a robar. Ione no sabe inicialmente qué puerta trancó Nox. Solo Lunaria y Erendriel saben que el fuego primero es ilusión; corrección de conocimiento fundamental (05-023, 05-027–05-028).

## Consecuencias documentadas del capítulo 6

- Bonnie localizó gema entregada por Patata a Liz y exige recuperar las demás, según recapitulación de Ione (06-004). No hay entrega final aún.
- Chochi declara haber quedado en tripulación de Ione por apuesta (06-005); no extender al visitante. Nombre completo reservado y humano joven adjudicado por director (06-008).
- Liz / Lizy = encargada de Sirena Borracha por contexto del pago/recapitulación de Poncelot, que interpreta local como juzgado. No convertirla en jueza real.
- Poncelot sigue creyendo que Merlucilla dinosaurio escapó (06-009), sin saber muerte relatada por Ione en 04-003.
- Loro pirata roba monedero de Chochi y lo deja caer al mar; visitante lo rescata y reparte siete monedas a cada uno (06-012–06-013).
- Marina es sirena liberada de botella por Chochi, distinta del alias Marina que Nox daba a Molly. Captura por bandera banana y tesoro declarados por ella; Ione identifica rey pirata Elger Banana, grafía provisional (06-015–06-018).
- Sirena da burbujas de respiración, escolta pasa por ruinas submarinas, rescatan hipocampo de dos tiburones; hipocampo llamado Merlucilla II y se vuelve fluorescente por fruta (06-019–06-024). Princesa es cadáver de tiburón que Ione arrastra, distinto de ambas monturas.
- Señora de Marina la devuelve a tamaño normal y las sirenas intentan matar al grupo para ocultar tesoro; aparecen tres atacantes en total (06-025–06-028).
- Ione transforma, hiere a Chochi con mordisco y garras, él siente malestar tras salvaciones; contagio NO confirmado (06-030). Poncelot rompe burbuja de Ione con mocho y ella huye hacia superficie/selva (06-032 y 06-038).
- Blink hecha pez por Polimorfia, vuelve a hada por concentración rota al golpe de hipocampo (06-031 y 06-034). Intenta estabilizar a Chochi sin éxito; visitante mata última sirena y Poncelot da poción que salva a Chochi antes de completar tres fallos (tenía dos fallidos/una acertada) (06-035–06-036).
- Tres perlas y diez monedas adjudicadas, luego director dice tres perlas y cinco monedas. Discrepancia conservada, no inventar saldo/reparto. Poncelot conserva botín al salir; visitante y Chochi van a médico, Blink busca Ione en selva (06-037–06-038).

## Notas de lectura parcial del capítulo 7

Notas iniciales conservadas como historial. El capítulo 7 ya está leído completo y su ficha validada; consultar `conocimiento/capitulos/07.md`.

- Grupo: Patata, Nox, Mamá, Lunaria y Erendriel; Ione no está jugando en esta sesión.
- 00:00–00:03: Patata busca terreno para granja y vuelve por hacha/materiales. Tirada de sucesos le quita herramientas de cocina; no se identifica ladrón ni dar por culpable a Lunaria por bromas. Nox mantiene a Jack medio secuestrado intentando adaptarlo y ha cedido camarote a Mamá. Descanso malo de Nox, un punto de cansancio/exhaustion.
- 00:03–00:08: Mamá convive con Erendriel y lagartijo, descanso malo; Lunaria merodea entradas por ventanas y pierde tres monedas por tirada; elfo relata que Mamá lo llevó a cenar y mató un dinosaurio, medita en camarote ofrecido por ella. Elfo pierde cuatro monedas; no atribuir robo a Mamá por bromas.
- 00:08–00:10: director recapitula escena entre partidas con pirata/lagartija, gnomo que se lleva montura y pulpo que la come. No inferir muerte del dragoncito; aclarar qué montura en siguientes pasajes. Poncelot fuera de escena buscando nuevo corcel.
- 00:10–00:16: Nox y Lunaria oyen dos piratas hablar de huevo muy valioso en nidos entre ruinas después de un puente. Lunaria se acerca con ruido de distracción, anota indicaciones usando papel/pluma robados al buque. Nox reconoce parte del camino pero pide guía nativa.
- 00:16–00:22: Mamá reconoce puente de madera sobre precipicio, estancia redonda y antiguo templo derrumbado hace años. Nox confunde relato de huevo con Patata (a quien llama limón); él aparece y aclara no estar secuestrado. Se acuerda investigar ruinas igualmente.
- 00:22–00:26: dragoncito de Erendriel está con Mamá; Lunaria le ofrece comida, animal busca a su cuidador. Mamá llama al elfo desde abajo, Nox ofrece llaves del barco. Dragón vivo presente. Nox tira del animal por cola y le da asco, no representar como rescue real.
- 00:26–00:30: Patata propone charla a Nox; este rehúye insinuaciones y le recuerda hablar del collar con Bonnie. Patata aclara que fue Ione quien repartió gemas; Nox se muestra sorprendido y complacido por su iniciativa, pero advierte que Bonnie controla mercancías. No asumir que Nox había planeado el reparto de capítulo 4.
- 00:30–00:35: elfo agradece a Mamá cuidado de dragoncito y pregunta quién lo intentó salvar; ella mira Nox. Él le exige hablar. Nox le apunta abajo con pistola; elfo lleva dos pistolas ocultas. Al final lo llama Jim, pendiente de contexto siguiente; NO normalizar a nombre real confirmado todavía.

## Validación existente

Seis pruebas de parser/normalización/citas en `scripts/test_construir.py`. Se verificó identidad byte a byte de los 156 originales contra el ZIP de descarga y estabilidad de mtimes en ejecución incremental. No se ha cotejado todo el audio; `revisado` significa lectura editorial de subtítulos, no verificación audiovisual ni extracción exhaustiva.

## Consecuencias documentadas de capítulos 7–8

- Nox declara Jim Hawkins como nombre, Capitán Nox como apelativo (07-009). Naór sigue sin equivalencia demostrada.
- El elfo y dragoncito quedan inconscientes, pero sobreviven tras curaciones (07-017–07-020). No son muertes definitivas.
- Mamá recoge huevo para criar; Nox promete a Bonnie entregar la futura criatura para venta bajo amenaza, sin consentimiento ni conocimiento acreditado de Mamá (07-023 y 07-033).
- Nox pregunta a Mamá por parecido de ruinas con sus propios tatuajes de espalda; ella no identifica relación. El elfo copia símbolos sin entender (07-025–07-026).
- Jack vuelve a aparecer en taberna; cautivo nuevo del nido es otro pirata (07-032). Patata atribuye mayoría de gemas a Ione, contradictorio con reparto representado del 4 (07-029).
- Lunaria recibe inmunidad al alcohol por 21 días en el 7, no en el 5; gana cinco monedas en apuesta (07-014 y 07-034).
- Capítulo 8: el elfo pide ser llamado Salazor, dos veces; conservar variantes previas sin borrar la fuente (08-007 y 08-011).
- Un pirata herido declara matanza en templo; Kilzer le roba diez monedas y Tlachka lo lleva a Gobs, médico que empieza a serrar sin desenlace mostrado (08-008–08-010).
- Ayoto se une y guía al templo tras engaño telepático de Blink como dios Sol (08-014–08-016). Cinco panteras derrotadas; criatura bípeda cambia de forma y al morir revierte a mujer, explícitamente muerta (08-017 y 08-022–08-023).
- Salazor conserva diario en Terran sin traducir. Ayoto entrega mortero a Pinky; ella no reconoce nawal. No se consulta a Mamá ausente (08-021, 08-024 y 08-026).
- Día alterado a noche por carta; después de ocho horas de descanso siguen volviendo de noche. Encuentros del regreso resumidos, sin heridas mecánicas adicionales (08-025).
- Kilzer termina con espada rota, recuerda otra guardada sin sustitución mostrada; loro escapa conservando bolsa (08-027).

## Consecuencias documentadas del capítulo 9

- Grupo Nox, Lunaria, Ione, Mamá y Axi. Axi parece continuidad de Chochi por saludo, heridas y mordida relatada; identificación contextual pendiente de declaración inequívoca (09-004 y 09-020). Se hace pirata al interpretar abandono de su dios tras casi muerte; no abandono divino confirmado.
- Ione relata un día en forma de bestia y recuperación dolorosa después de sirenas. Reproche de Axi por mordida y temor de Ione no confirman contagio (09-002, 09-007 y 09-020).
- Mamá relata visión al tomar mano de Nox entre sesiones, contenido no descrito. Tatuaje propio escuece cuando Nox la cura. Tatuajes de espalda de Nox son otros; conexión no resuelta (09-003, 09-028 y 09-031).
- Nox cambia mapas con joven aprendiz sin nombre inequívoco; joven llama a Baps, no asumir que sea él. Mapa recibido lleva a templo con símbolos de serpientes; mapa entregado por Nox no abierto (09-009 y 09-018).
- Axi queda rezagado por desconexión antes de jardín y combate final; vuelve con grupo, sin conocimiento automático de escenas ausentes (09-023 y 09-030).
- Agua en canales de altar no funciona; sangre de Mamá sí abre paso. Requisito nativo que dice Nox es mentira, aclarada por director (09-019 y 09-021).
- Ione activa veneno al tocar puerta; criatura de primera tumba abatida. Planta atrapa a Nox y compañeras lo liberan; Ione guarda hojas olorosas sin consumo mostrado (09-019 y 09-022–09-024).
- Tres guardianes salen tras tomar copa; dicen ellos tienen que volver y vosotros sois traidores, sin explicación histórica confirmada. Derrotados; Pinky finge muerte y Lunaria le roba cinco monedas (09-026–09-029).
- Director limita reclamación de Bonnie: botín nuevo propio, deuda de Nox/Ione por taberna y gemas de encargo específicas. Liz conserva gema de Patata, sin recuperación (09-031–09-032).
- Ventas: obsidiana de Ione seis, collar de Nox 27, copa de Lunaria adjudicación final 170, cimitarra veinte y cadáver una moneda. Ropa regalada a Nox, dos pociones de Lunaria y herramientas de Nox; no saldo agregado seguro (09-032–09-033).
- Inmunidad al alcohol recordada como semana en 9 frente a 21 días del 7, discrepancia conservada. Huevo sigue cuidado sin eclosionar (09-008 y 09-033).

## Notas de lectura parcial del capítulo 10

Notas iniciales conservadas como historial. Capítulo 10 ya leído completo y ficha validada; consultar `conocimiento/capitulos/10.md`.

- Grupo Patata, Erendriel/Salazor con dragoncito, Blink, Axi y Ayoto. Ayoto inicialmente dirigido por director al faltar su jugador, que llega hacia 00:27. No interpretar ausencia de conexión como ausencia del personaje de barca.
- 00:01–00:03: Patata relata que kender le pidió ayudar a Mamá con huevo; construye nido y mecanismo para calor/sol, vuelve a talar. Cuenta cinco árboles frente a tres previos y muchos pendientes, no granja acabada. Tirada le da cansancio por ruido del alojamiento.
- 00:03–00:04: elfo intenta estudiar dibujos del libro de nawal sin leer idioma; evita doctor. Intenta recapitular ausencia del mono, director corrige que aún no sabe eso. Broma de deber cinco monedas por no tener dinero no se consolida como deuda.
- 00:04–00:07: Blink vive a veces en vigía del barco y comparte espacio alternadamente con loro; visita casa de selva, recoge brillantes. Relata dormir bajo huevo y calentarlo con su nido. Tirada le da perla. Axi relata ciclo de borrachera/resaca, pierde poción de vida por tirada; no asumir hurto de Bonnie por bromas de caja fuerte.
- 00:08–00:11: de noche en Shiaru, Ayoto desmenuza pantera junto al pozo, Axi tirado de resaca. Pix sale con basura y la vierte al agua; mayoría ve desaparecer al mono, bolsa cae. Blink no ve por percepción. Patata mira agua sin identificar qué pasó; solo sombras y mono ausente.
- 00:11–00:14: elfo habla a Blink de monstruo grande del puerto, especula alimentación por Pix y propone tener contenta Bonnie. Blink se entera por charla, no atribuir visión directa del incidente.
- 00:14–00:18: Bonnie se presenta Happy Bonnie a Patata, lo interroga sobre gema de alojamiento; él admite origen de Ione. Bonnie apunta pistola y afirma gema suya, llama a Nox inútil que usa. Dice Ron de Bonnie abarca todo lo que ven, no solo taberna; es declaración de poder, no mapa de jurisdicción formal.
- 00:18–00:22: Patata informa desaparición de Pix. Bonnie le obliga a buscarlo en bote, amenaza patatas fritas si no va y promete agradecimiento/posible pago si vuelve. Obliga a Axi con cimitarra al cuello y pide al elfo rastrear y llevar al grandote. Ordena volver con mono vivo. Blink se había escondido, Bonnie no la ve.
- 00:22–00:26: Blink se presenta a Patata y hablan de Chimy, mago zanahoria, solo mención sin aparición. Axi confundido acepta seguir a Patata. Elfo intenta rastrear salida del mono desde agua sin éxito. Suben los cinco a barca, Ayoto rema y dragoncito bajo capa del elfo.
- 00:26–00:30: navegan al norte de Shiaru hasta zona pantanosa llamada Ruki Peten (grafía provisional). Aguas poco profundas permiten caminar o barca. Blink encuentra marcas recientes de criaturas con pelos de mono entre ellas; no son huellas de mono. Más adelante siguen las marcas.
- 00:30: elfo pide objeto pendiente del capítulo 8, especifica pergamino truco, director reconoce no haberlo añadido y lo apunta. Aclara objeto descrito ambiguamente en 08-019, pero aún sin conjuro determinado.
- 00:31–00:35: naturaleza indica marcas de bestia de dos patas, humanoide en forma pero no necesariamente persona, varias criaturas sin número firme. Hipótesis de comerse mono no comprobada. Llegan a encuentro, jugadores reconocen posibles atacantes previos; continuar desde 35 para identidad y desenlace.

## Consecuencias documentadas del capítulo 10

- Expedición obligada a rescatar a Pix vivo; cinco aventureros y dragón navegan al norte de Shiaru hacia Ruki Peten. Bonnie solo vio cuatro porque Blink estaba escondida (10-008–10-009).
- Dos cocodrilos abatidos; Axi toma diente. Blink obtiene mondadientes de nivel cinco, permite recuperar conjuro. Elfo pide pergamino de truco pendiente del 8, sin conjuro preciso (10-011–10-012 y 10-017).
- Elfo capturado al acercarse solo a poblado de hombres lagarto; compañeros no presencian captura. Guardias detectan a Patata, Axi y dragón y ordenan retirada en dracónico, solo Axi/dragón comprenden. Ayoto/Blink inicialmente ocultos (10-013–10-015).
- Jabalina hiere Axi, después insulta y comienza combate; guardia llama refuerzos. Numerosos defensores y cocodrilos cercan al grupo (10-015–10-016).
- Elfo se desata y teletransporta fuera de jaula, escapa sin recuperar armas. Ayoto y dragón también huyen. Patata sigue combatiendo para no abandonar a Axi; Blink intenta control y telequinesis (10-017–10-022).
- Axi cae varias veces y una carta lo levanta temporalmente; eso no es resurrección. Finalmente Patata y Blink también caen. Director confirma los tres vivos y enjaulados al cierre, sin personajes nuevos de momento (10-019–10-023 y 10-027).
- Elfo y Ayoto vuelven a Shiaru sin Pix o compañeros. Ayoto llama poblado Ciudad de la Luna y estima más de sesenta; son sus palabras, sin nombre oficial o censo confirmado (10-024–10-025).
- Bonnie ordena a Ayoto volver con Nox/Ione y traer al elfo; mata pirata de ejemplo para imponer amenaza. No segunda expedición iniciada, Pix no localizado (10-026–10-027).

## Consecuencias documentadas del capítulo 11

- Grupo Ione, Mamá, Kilzer y Poncelot; Nox se incorpora en pantano. Ione recibe informe de Nox y recluta bajo amenaza a Kilzer; encargo de bufón/reina para Poncelot adapta su interpretación caballeresca (11-001, 11-006–11-007 y 11-011).
- Mamá relata visión de sí misma dejando bebé en cofre y prometiendo volver. Relata juramento de Nox por maldición de no mentir, sin texto mecánico ni sanción probada (11-003).
- Poncelot sigue creyendo que Merlucilla I escapó. Vende tres perlas por sesenta y obsidiana por ocho, da catorce a Kilzer. Diez monedas submarinas retomadas frente a cinco al cierre del 6, discrepancia sin resolver (11-004–11-005 y 11-008).
- Nox dice usar ritual Comprender lenguajes y anotaciones en libro Terran; no identificarlo con diario del elfo sin fuente. Fruta lo hace invisible toda sesión, objetos nuevos siguen visibles (11-011, 11-013–11-014).
- Hombres lagarto inteligentes, organizados y eficientes según saber adjudicado a Mamá; no intrínsecamente malvados por comer caídos. Nox oye conversación de guardias sobre Fred comido, sin datos extra de identidad (11-013 y 11-016).
- Infiltración rota por transformación de Ione al olor de sangre; Nox mata guardia e incendia puente y choza. Kilzer protege Mamá, Poncelot calma y monta a Ione (11-017–11-021).
- Nox usa libro con glifo y Inmovilizar persona adjudicados sin revisar todas reglas, mata combatiente grande y recoge Pix atado de altar (11-022–11-023). No sacrificio de mono realizado.
- Nox roba de Pix moneda plateada con calavera; director la asocia a cinco monedas de cinco reyes piratas (11-024). No ascenso de Nox al trono por tenerla.
- Abren jaulas, sacan Patata/Axi y botella de Blink, recuperan caja con solo parte de equipo y arco para Axi. Incendio avanza; vuelven a Shiaru. Ione humana de nuevo por trato de Poncelot, sin memoria completa (11-025–11-027).
- Nox roba una obsidiana/gema a Kilzer, director corrige que conserva otra. Da a Bonnie Pix, moneda y gema; ella ve invisible y lleva anillo negro de espadas llamado Cuchillas Negras. Cita a las nueve en muelle, no conversación realizada (11-028–11-029).
- Poncelot lleva dos heridos a médico; Mamá lleva a Blink al barco e intenta abrir/reanimar, resolución pendiente. Kilzer discute pago con Ione sin cobrar (11-030).
- Nox propone casino con licencia invisible y cuatro monedas/cinco por ciento; Kilzer exige verificar al verlo antes de cerrar. Al final Nox obtiene gema de Liz por inspiración, recuento tres/dos/una conserva contradicción y referencias a rol externo (11-031–11-032).

## Notas de lectura parcial del capítulo 12

Notas iniciales conservadas como historial. Capítulo 12 leído completo y ficha validada; consultar `conocimiento/capitulos/12.md`.

- Grupo Blink, Nox, Ione, Axi y Erendriel; Mamá no juega. No misión conocida por personajes al principio, director lo recuerda a quienes hablan de misión prevista.
- 00:00–00:02: Blink relata estar consciente pero recuperándose en barco, cerca de Mamá/huevo y sin moverse mucho; busca ropa. No pierde objeto al no tener nada por tirada. Nox relata conversación interesante con Bonnie, sin contenido completo, nervioso por fuerte al sur del Garfio. Tirada le resta tres de vida.
- 00:02–00:04: Ione relata cita breve con Kilzer, mono interfería y casi degüella por no pagar monedas, al final pagó y mono se fue. Relato entre sesiones sin cantidad o causa contractual completas. Tirada Ione encuentra cuatro de oro.
- 00:04–00:07: Axi despierta en enfermería sin equipo y con dolor, tirada da cansancio. Elfo relata hablar con Nox y Bonnie, ayudar y recibir piercing en oreja y haber salvado vida; Nox le dio dinero y arma. Robó ropa de convalecientes. Bromas de sarna y venérea no consolidar como enfermedad formal sin adjudicación clara; tirada da dos de oro.
- 00:08–00:10: Nox hace runas/ritual en libro que dice le dio Erendriel; refuerza posible relación con diario Terran del 8, aclarado a 00:27. Ione recoge tanga colgado. Blink busca agua dulce en pozo pero hay sangre y pantera ya medio podrida; va hacia ropa pero no roba tanga al verse pasando entre Nox/Ione.
- 00:11–00:15: elfo tiene punta de una oreja perdida, director lo confirma, no solo piercing. Abre taberna y Bonnie dispara rozando otra oreja; le queda una semana y amenaza que no habrá más orejas. No tarea precisa aún en estos minutos. Encuentra dieciséis de oro bajo mostrador, dueño no confirmado. Dragoncito sigue vivo bajo capa.
- 00:16–00:20: Blink pregunta por rescate y cosas; Ione agradece Nox/Kilzer/gnomo y admite no recordar todo. Palillo de Blink está con Pix por memoria adjudicada a Nox y elfo; Ione no recuerda. Blink conoce ubicación por diálogo, no recupera palillo aún. Agradece descanso en barco y está más recuperada.
- 00:21–00:24: elfo habla de tema con Jacki y plazo de semana. Intenta devolver ocho de oro a Nox por lo prestado; Nox rechaza, recuerda diez por ciento de lo que traiga a Bonnie y de misiones, pide equiparse. Elfo se plantea comprar arco, no compra vista todavía.
- 00:24–00:27: Nox presenta Jacki, quiere verlo reunido con Lucy. Propone barco hacia Puerto de Espadas para gestiones cobrando a lista de nombres y volver con ganancias para ser libre, lista no leída. Marine cree posible volver a fuerte para zarpar, Nox insiste que lo matarían por traidor; amenaza hipotética, no sentencia comprobada. Elfo muestra anillo y apoya advertencia sin que marine lo reconozca. No viaje iniciado ni libertad consumada.
- 00:27–00:29: director identifica escrituras antiguas como diario del nawal. Empieza con rutinas y rituales a dioses animales; escritura luego fuerte/agresiva, cada vez menos palabras, termina en garabatos. Interpretan pérdida de esencia humana progresiva. No texto completo, autor o deidades nombradas; no atribuir rituales a hombres serpiente solo por comentario de Nox.
- 00:29–00:32: Jacki declara Fuerte Aurora casi terminado al llegar, pocos muros/cosas pendientes y expediciones más arriba. Quiere avisar compañeros, Nox lo disuade con amenaza. Nox cree Molly dirige fuerte, no confirmado en esos minutos. Busca Mingo/Mango y tercero no reconocido; cree vivos, sin ubicación comprobada. Estos piratas no identificados con captores de Blink por pregunta sola.
- 00:32–00:35: quieren recopilar información de excavaciones y marina, no combate de entrada. Blink recuerda por historia ruinas/campamento con hombres azules y humo al sur de casa/árbol, además de minas anteriores. Puede guiar cerca de casa y después orientarse. Plan de expedición no desenlace aún.

## Consecuencias documentadas del capítulo 12

- Libro que usa Nox recibido de Erendriel, escrituras identificadas explícitamente por director como diario del nawal. Rutinas y rituales a dioses animales pasan a letras agresivas, menos palabras y garabatos: pérdida de humanidad interpretada por fuente, no nombres/receta completa (12-004 y 12-008).
- Nox y elfo proponen Jack embarcar hacia Puerto de Espadas para gestiones, ver a Lucy y volver con dinero para ser libre. No lista o barco vistos ni viaje iniciado. Jack dice Aurora casi terminado y con expediciones; Nox cree Molly manda, sin inspección (12-007–12-009).
- Campamento explorado al sur de árbol de Blink es ruinas distintas del fuerte. Nox disfrazado como Jack Jackson logra aceptación provisional como marine; Pinky lo reconoce (12-010 y 12-015–12-016).
- Pix tiene mondadientes de Blink sin devolución vista; arco comprado por elfo, Axi recibe cerbatana/dardos/abrigo y hace arco con penalidad. Diferencia frente a arco recogido para él en 11, sin inventar pérdida intermedia (12-005, 12-011 y 12-014).
- Ione siente transformación por adrenalina pero conserva control, no se vuelve lobo en este capítulo (12-015). Palabra papaya acordada para aviso/cadenas (12-011).
- Cuatro presos: mujer tatuada, hombre tigre, pirata familiar de Shiaru y hombre pintado mordiendo barrotes. Sin nombres, filiación o delitos (12-017).
- Ione/Blink reducen primer guardia y lo dejan inconsciente; otro intenta despertarlo después, no muerte. Segundo agarre es detectado, combate (12-018 y 12-020).
- Pinky crece plantas tras cobrar diez, luego chocolate de Mamá la hace alucinar cuatro horas. Quema capitán y Nox; Nox acaba transformándola en oveja y recupera dinero (12-019, 12-023 y 12-026–12-027, 12-030).
- Jaulas de mujer/pirata/hombre tigre abiertas. Mujer ayuda y sale herida con Ione; pirata huye y cae por disparos, sin recuperación; cuarto preso no abierto explícitamente. No atribuir liberación de todos por plural del cierre (12-023–12-025 y 12-028).
- Capitán tiene exclamación de muerte al fuego pero sigue actuando y Nox lo noquea sin matar; queda vivo con carta en pecho. Interrogatorio/leer mente solo propuestos (12-026–12-027 y 12-032).
- Nox obtiene nueve de oro, copa ritual y mapa de varios puntos de Marina, lo muestra/da a Blink. Sin coordenadas, nombres de puntos o contenido de carta leído (12-029–12-032).
- Elfo obtiene cinco de oro, Blink perla y cuatro por carta; no munición final exacta. Ione evacua heridos/refugiados, elfo avisa y restantes vuelven con Pinky oveja guiada por brócoli ilusorio (12-028 y 12-031–12-032).

## Notas de lectura parcial del capítulo 13

Notas iniciales conservadas como historial. Capítulo 13 leído completo y ficha validada; consultar `conocimiento/capitulos/13.md`.

- Grupo Patata, Kilzer, Nox, Lunaria y Ayoto; Ione/Mamá/Blink/elfo no juegan. No transportar conocimiento del campamento del 12 a este grupo sin diálogo.
- 00:00–00:03: Patata recapitula despertar desnudo y sin cosas en médico, hablar con Bonnie para trato que devolviera parte; dice vender alma en broma/metáfora, sin pacto sobrenatural demostrado. Tirada encuentra tres monedas. Kilzer relata cita con Ione y semana tranquila; tirada da corte, autor desconocido, broma de enano no prueba. Nox relata cerrar venta con Liz y repartir ganancias a compañeros, sin cantidades, y espera que nota del capitán llegue; descanso le da cansancio.
- 00:03–00:06: Lunaria recopila pinturas y pinta casco del barco sin pedir autorización; tiene cansancio y encuentra mapa de tesoro. Ayoto busca información de mujer que se llevó nawal y artefacto/mechero para abuela; director reconoce pendiente colocarla. Identidad de quien se llevó cuerpo no fijada en este inicio. Ayoto pierde dos monedas; teorías de que son tres de Patata no transferencia demostrada.
- 00:06–00:10: pantera en pozo tras semanas está seca, medio huesos, olor horrible y sangre en pozo. Ayoto desuella restos. Patata cree armadura devuelta, director corrige que solo espada, escudo y amuleto, sin armadura. Kilzer va al bar; Nox/Luna cansados organizan objetos hallados y cerveza.
- 00:11–00:14: Kilzer intenta evitar grupo, chillido de pianista por carta de audiencia lo deja sordo un minuto. Patata roba tres de oro a Ayoto por juego de manos y se pincha con algo afilado sin identificar en bolsillo, por carta. Va a forja para vestirse.
- 00:15–00:18: Lunaria lleva a Kilzer a barra y le roba mientras sordo; director adjudica inicialmente una moneda, pero jugador aclara que Luna no busca dinero y se sustituye por cola de puma/pantera. No sumar moneda y cola como robo simultáneo. Nox come crema de cucaracha del desierto para cansancio; se representa sin extraer receta real o poderes universales.
- 00:18–00:24: sordera de Kilzer termina. Nox muestra licencia con espacio para firma, Kilzer empieza a leer y ahora ve que existe papel. Al llamarla guardadora de cosas ajenas Luna se ofende, no acepta ladrona y lanza papel por viento; Nox/Kilzer lo recuperan. No contenido legal completo, emisor, licencia válida o acuerdo cerrado todavía. Jacki intenta ver papel porque le recuerda pluma/imágenes, sin explicación completa.
- 00:24–00:29: Patata compra cobertura barata moldeada por herrero para cuerpo de patata y se cura totalmente dedo. Ayoto interpreta desnudez previa de Patata como saludo al sol, se desnuda y entra al bar. Pide cabeza/piel de pantera como capucha/capa; no curtida y olor fuerte. Director corrige que tras semanas ya seca, frente a decir sangrando primero.
- 00:29–00:32: ilusión de sol de Luna al hombro de Kilzer hace Ayoto creer bendición; al mirar de cerca queda ciego un minuto por carta. No intervención divina verdadera. Jacki llama Nox, con ayuda de Ojo ausente y Baps dibujó mapa del Garfio con puntos de extracción recordados de Marina. Dibujos y etiquetas defectuosos, no mapa de precisión. Nox da moneda de oro para ronda.
- 00:32–00:35: Nox/Luna comparan croquis de Jacki con mapa de tesoro nuevo de Lunaria, descifran punto y marcan cruces con cartografía. Nox mete mapa/croquis en botella y se lo lanza a cabeza a Jacki, lo deja inconsciente. Baps aparta cuerpo. Nox golpea accidentalmente cuello de Kilzer y se anuncia silencio un período (continuar desde 35 para duración y consecuencias). No muerte de Jacki adjudicada.

## Consecuencias documentadas del capítulo 13

- Silencio de Kilzer y ceguera de Ayoto duran un minuto y terminan; Ayoto da capa a Pix, división de piel poco clara. Jacki queda inconsciente por botella de Nox, no muerte (13-008–13-009).
- Licencia visible de casino y reparto declarado por Nox 35 Bonnie/15 Nox/50 Kilzer; diferencia con cinco por ciento discutido en 11. Local sin visitar o abrir, beneficios no recibidos (13-006 y 13-011).
- Nox da herramientas de pintor a Luna y mapas guían a punto elegido por Ayoto. Carta hace dormir Nox; Ayoto roba sombrero y Kilzer seis monedas, dado de carta explota y despierta Nox (13-010 y 13-012).
- Templo de noche/sol/luna no identificación oficial: fallan lecturas, engaño de sol ilusorio fracasa y carta oscurece. Tres abren portón. Patata pone Luz a Ayoto, sin bendición divina probada (13-014–13-015).
- Cuatro plantas derrotadas, Patata encerrado con daño ácido se libera matando planta; Nox arranca Kilzer de raíces; Ayoto agarrado por última liberado al morir (13-015–13-020). Inmunidad veneno solo Kilzer, no ácido; fuego daña, cura por carta aparte.
- Ayoto toma lianas y dos semillas, sin cultivo o escudo modificado. Altar visible sin tesoro, Luna no halla hierba de Pinky (13-021).
- Nox comprende jaguar/águila/serpiente, Ayoto ofrece asociaciones culturales variables. Ritual/danza hace brillar águila y plataforma baja a sótano de cajas; no solo peso (13-022–13-024).
- Ayoto tres monedas antiguas, Patata jade indicado cien de oro, Luna obsidiana. Ocho monedas se sustituyen por nueva tirada sin resultado inequívoco, no sumar. Botín de todos no plenamente anunciado (13-025).
- Luna usa una carga de Paso brumoso arriba; plataforma vacía no sube. Terminan en templo, sin regreso o salida del sótano de todos mostrados (13-026).

## Notas de lectura parcial del capítulo 14

Notas iniciales conservadas como historial. Capítulo 14 leído completo y ficha validada; consultar `conocimiento/capitulos/14.md`.

- Grupo Patata, Ayoto y Blink con dos nuevos personajes elfos hermanos: Eldrat/Eldrash/Eldrad y Triel/Tyriel (grafías provisionales). Primera narración por voz invitada, director Pol participa apoyando; conservar adjudicaciones de ambos sin atribuir todo a mismo hablante.
- 00:00–00:03: vista privilegiada del espectador en sala oscura de parto: nacen dos bebés, niña y hermano después vistos creciendo, ayudándose espalda contra espalda en pelea y planificando hurtos adolescentes. Identificados contextualmente con hermanos de escena siguiente, sin madre, padre, ciudad o fecha narrados. No conocimiento directo de otros PJ por verlo espectador.
- 00:03–00:12: horas antes de escena actual de Shiaru, hermanos cruzan lago/tronco de jungla; Eldrat salta al ver cocodrilo, advierte Triel, ella lo alimenta con raciones. Eldrat ve dos panteras acechando por crítico. Escena conjunta sin tracker: dagas moradas hacen dolor sin sangre, Triel espada azul de escamas electrifica. Disputan bajas; Eldrat remata pantera de hermana y otra salta sobre ambos cuando ella usa hermano de escudo, la matan con dagas. No muertes de hermanos ni licantropía por broma.
- 00:12–00:16: Shiaru nocturna, Blink observa dos piratas familiares que buscaba, jugando con su mondadientes. Mira Pix, no lo tiene; no asumir nombres de captores aún hasta voz inequívoca, pregunta por continuidad. Pix cobra a Nelli/Nelly y Baton (grafías provisionales) por bebida; figuras diferentes de dos que juegan palillo salvo prueba. Blink roba palillo con mano de mago invisible, 60 pies, aprovechando estornudo y lo limpia con Prestidigitación. Arma recuperada efectivamente.
- 00:16–00:21: Patata lleva jade del sótano, herrero gestual no logra trato y pasa a Liz. Ella sospecha problema como gema anterior, dice pureza permitiría revender por 80–90, ofrece 35 y acaba 50. Añade servicio una noche con Melisa y Juana al acuerdo, no sexualidad explícita o encuentro consumado en escena. Patata vende jade por 50 de oro, no cien del valor indicado. Habla granja futura y alimentos, Liz remite a Bonnie; no suministro o granja acabados.
- 00:21–00:26: hermanos llegan a Shiaru tras semanas perdidos en selva. Eldrat come fruta guardada y brazos se alargan hasta suelo; Triel lanza resto a Patata para comprobar realidad. Patata advierte peligro del puerto/jungla y los guía a supuesto sastre que es posada/Liz. Hablan de dríadas, mosquito de ilusiones, sin historia completa de captura o identidad de monstruo. Se reconocen como elfos, no piratas según ellos. Patata los ve y les habla, por tanto conoce recién llegados por escena, no pasado de parto.
- 00:26–00:30: Blink pide a Patata comprar mochila al evitar local cerrado de desconocida, él invita a ir detrás. Hermanos compran dos ropas iguales negras tras rechazar servicios de posada; dinero en mesa y compra permitida, sin precio total claro. Aún no compra de mochila de Blink mostrada en primer tramo. No asignar a Liz oficio único de sastre oficial por confusión de jugador.
- 00:30–00:33: Ayoto da al loro sombrero robado a Nox, buscando amistad con loro y Pix. Loro lo lleva a nido en palmera; no devolución a Nox. Piratas se aglomeran en muelle con linterna porque viene bote solo con bulto que creen mujer, sin remero visible. Ayoto no ve oscuridad, no identifica ocupante, va a taberna a avisar. Llegada no resuelta todavía.
- 00:33–00:35: Eldrat habla mentalmente con Triel de quedarse porque dinero agotado tras ropa. Preguntan Patata dónde ganar: responde jungla con tesoros y peligros, recuerda propios veinte lagartos sin precisar censo. No expedición acordada ni conocimiento de cautiverio por haber visto capítulo anterior.

## Consecuencias documentadas del capítulo 14

- Nuevos hermanos elfos Eldrat/Triel distintos de Erendriel. Pasado de infancia/adolescencia visto en narración privilegiada, no sabido por otros PJ. Escena de dos panteras horas antes de puerto (14-001–14-002).
- Mondadientes de Blink recuperado efectivamente, mochila aplazada. Jade de Patata vendido cincuenta, no cien, y servicios prometidos sin encuentro realizado. Sombrero de Nox entregado al loro (14-003–14-006).
- Mujer blanca de bote pide rescate de padre/tripulación mercante; intenta beso evitado, toca Patata y desaparece. Mancha negra aparece. Blink lee leyenda en mente pirata, con precedentes de sacrificios y escape, no diagnóstico completo (14-007–14-009).
- Bonnie expulsa Patata hasta resolver, cinco parten sin Nox. Bonnie no acuerda recompensa comercial aún a hermanos (14-010).
- Mercante en ruinas con muertos en bucles, algunos reaccionan atacando. Hermanos roban llaves al cepo, grupo brújula de camarero y campana del grande; Eldrat moneda negra de marinero que talla traidor (14-011–14-014 y 14-017–14-020).
- Blink lee diario: hija enferma, cura buscada en Xoltacan, entidad de precio dudoso y objetos rituales con relicario. Habla espectro con cara de aparición, que niega salir por padre; contradicción sin resolver (14-015–14-016).
- Patata y Ayoto envenenados durante bebida/combate. Runas de muerte vistas por Triel pero identificadas por narrador, no por ella. No maldición nueva comprobada de Eldrat por frase del marinero (14-017–14-020).
- Cofre abierto con llave por mano de mago; gema corrupta no misma causa que mundo de Blink. Juntar objetos revela capitán, primera fase lleva a cubierta y segunda amenaza hundir barco en dos rondas (14-021–14-023).
- Triel rompe relicario que porta Ayoto: marinero sonríe y desaparece, capitán grita por hija y desaparece con tripulación. Niebla devuelve grupo, sanos y sin veneno, Patata sin mancha. No resurrección humana o destino de almas vistos (14-024–14-025).
- Pago discutido sin dinero intercambiado; Bonnie convoca Patata y hermanos para escena pendiente (14-025).

## Consecuencias documentadas del capítulo 15

- Granja ya construida parcialmente junto al camino de Shiaru, cultivos y estatua, con permiso de Bonnie a cambio de aportaciones. Plantas aún creciendo, no ingresos de cosecha (15-003–15-004). Casino en construcción por recapitulación de Kilzer, sin abrir (15-001).
- Patata declara diosa agrícola Chanrea por grafía fuente y que le dio forma; no normalización externa sin apoyo. Dos piratas arrastrados desde granja por sombras, arma de hueso hallada (15-003 y 15-007).
- Patata entrega cinco de excursión a Bonnie y ella manda investigar/eliminar amenaza, incluso exterminar si tribu caníbal; orden de Bonnie, no valoración neutral. Grupo de seis con dragón sigue rastros al sur y encuentra restos de piratas (15-004–15-005 y 15-010).
- Axi compra flechas/armadura ligera. Espada de Triel reconocida como escamas azules de dragón, no madre exacta. Tarin aparece como candidato de nombre del dragón, no consolidado (15-005–15-006 y 15-012).
- Frutas temporales: Eldrat no miente, Axi inmune armas pero luego envenenado, elfo/dragón resistencia no mágico. Estegosauro herbívoro evitado sin combate (15-008–15-009 y 15-015).
- Poblado distinto de tribu del preso pintado del 12, aunque Axi/Kilzer recuerdan primer ataque del 2. Triel disfrazada, Axi dispara por error fallando; Patata/dragón la reconocen después (15-010 y 15-016).
- Crecimiento espinoso y Espíritus guardianes frenan rivales; Kilzer derribado recibe cura de Triel sin saber origen y ayuda Patata. Jefe de hachas se levanta por rabia/habilidad, Eldrat remata; no resurrección confirmada (15-012–15-017).
- Botín: Patata moneda antigua/siete, Axi obsidiana/nueve; bolsa veintitrés pasa Kilzer→Eldrat por robo y vuelve en regreso. Eldrat copa ritual nueva. Elfo copia tatuajes sin saber poder; miasma de carta doce de daño. Patata/Axi una poción cada uno en hoyo (15-018–15-020).
- Bonnie recibe pierna y paga cincuenta; Patata ofrece treinta a compañeros que no saben total. Reparto finalmente cuatro partes de siete y medio, intento de seis y medio corregido (15-020 y 15-022).
- Bonnie dice Jack acaba de irse tras dos semanas y retiene al elfo por envío tarde; dos piratas lo llevan tras puerta, sin ejecución/mutilación mostradas. Dragón va al barco a buscar abuela, no encuentro visto (15-021–15-022).
