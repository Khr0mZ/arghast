# Método de reconstrucción

## Evidencia

Cada afirmación lleva un identificador estable, capítulo, intervalo del vídeo, cita literal de los subtítulos y enlace al minuto. El constructor comprueba que esa cita aparece dentro del intervalo del VTT original. Esta comprobación valida la localización textual, no la interpretación ni la fidelidad al audio. La confianza es una valoración editorial sobre la lectura de los subtítulos, no una probabilidad calculada.

- `hecho_confirmado`: acción o resultado adjudicado y narrado explícitamente en la sesión. Confirmado respecto a los subtítulos, pendiente de audio si hay dudas.
- `declaracion_personaje`: afirmación, intención, relato o creencia de un personaje. No demuestra por sí sola que el mundo sea así.
- `explicacion_director`: exposición del director, diferenciada de la escena y de los trasfondos presentados por jugadores.
- `especulacion_jugadores`: teoría o interpretación de la mesa, sin adjudicación confirmatoria.
- `desconocido`: pregunta abierta; no se completa con conocimientos generales de D&D ni con episodios aún no revisados.

Los trasfondos presentados por jugadores se registran como declaraciones atribuidas, salvo confirmación posterior. Bromas, comentarios sobre otros mundos o campañas y hipótesis no se convierten en lugares, muertes ni parentescos del canon. Los hablantes no se identifican automáticamente.

## Conocimiento de personajes

Actualización de alcance solicitada por el usuario: el resultado es una **enciclopedia global de Xoltacan**, sin vista ni filtro de conocimiento de Oghma. Los campos históricos de conocimiento se conservan en JSON por compatibilidad, pero no limitan búsquedas o documentos. Ámbito y testigos ayudan a atribuir conversaciones, no excluyen información de la enciclopedia.

El campo histórico `conocimiento_personaje` se conserva en JSON por compatibilidad con fichas iniciales. No se usa para excluir información ni generar una vista personal: la enciclopedia incluye todo lo documentado, con atribución de escenas y testimonios.

El campo `ambito` distingue presentación en la mesa, escena pública y conversación privada. `conocedores` solo enumera destinatarios o testigos explícitos; una lista vacía significa sin determinar, no nadie. Tampoco se da por sabido a todo el grupo lo que ve el espectador al cambiar de escena. Personajes presentes, personajes ausentes y jugadores son conjuntos distintos.

## Nombres e integridad

La prosa de la enciclopedia se redacta en español natural, con frases completas y tono neutral. No reproduce la forma de hablar de los personajes. Las citas literales y las transcripciones conservan el texto reconocido, incluidos sus errores, para permitir su comprobación.

El catálogo público se construye a partir de identidades revisadas en `config/entidades.json`, con tipo, descripción y referencias. Las variantes confirmadas conducen a una sola ficha. Las etiquetas de extracción que describen acciones, reglas o visiones no generan personajes. Cuando una equivalencia no está demostrada, se conserva la duda en la fuente sin inventar una identidad ni fusionar personas por parecido. Las etiquetas originales permanecen en los datos y siguen disponibles para la búsqueda.

Los VTT y TXT descargados se conservan byte a byte. Los SHA-256 abarcan todas las variantes; el primer inventario establece la referencia local. No constituye una prueba de cómo eran antes de ese inventario.

Cada segmento derivado conserva `texto_original` y `texto_normalizado`. Solo se sustituyen alias confirmados con límites de palabra y se registra cada cambio. La equivalencia Choltacán → Xoltacan procede del usuario. Otros parecidos no se sustituyen en masa. Variantes como Sitlali pueden usarse en una ficha como identidad candidata, indicando la base contextual y conservando la cita original. No se deduce que Citlali sea Coyote solo porque el usuario escribió Citlali/Coyote.

El parser elimina únicamente líneas de arrastre exactamente iguales a las del cue anterior cuando los cues son contiguos (hasta 21 ms). No elimina frases similares, tartamudeos ni repeticiones entre escenas. El VTT íntegro permite verificar cualquier pérdida accidental de esa limpieza. Los tiempos del texto derivado corresponden al inicio del cue, no necesariamente al instante exacto de cada palabra.

## Cronología y contradicciones

Se lee cada capítulo completo antes de cerrar su ficha. Tras autorización del usuario, los pendientes se revisan en bloques paralelos, en orden dentro de cada bloque; después se cruzan revelaciones, referencias y contradicciones entre bloques. La cronología publicada se ordena por número de capítulo y tiempo del vídeo. Ese orden no demuestra el orden temporal entre grupos West Marches. El calendario interno queda sin fijar mientras no haya fechas o relaciones temporales explícitas. Flashbacks y presentaciones se distinguen del presente de la aventura.

Si un episodio posterior discrepa, se añade una afirmación nueva y una contradicción con ambas referencias. No se reescribe el testimonio anterior para encajar. Una corrección explícita del director se conserva junto a la versión corregida. Las aclaraciones del mismo episodio se registran también.

Estas observaciones forman parte de las notas de cada capítulo o identidad. No constituyen una categoría del mundo de Xoltacan ni una sección principal de la interfaz.

## Fechas de emisión y publicación

Las fichas distinguen el directo original de Twitch, la publicación posterior en YouTube y la fecha del aviso de Discord. Las correspondencias se cotejan por campaña, número y título, con variantes editoriales explícitas. Un enlace Twitch en la descripción promocional de YouTube no constituye un aviso de directo. Los títulos contradictorios y los avisos repetidos en días distintos quedan pendientes; no se rellena un capítulo por frecuencia semanal o proximidad a una subida.

Las fechas civiles se muestran en Europe/Madrid. El timestamp de la tarjeta y la hora del mensaje se conservan separados: el bot puede anunciar un vídeo días después de publicarse. Si falta el timestamp del vídeo y no hay metadatos independientes, se muestra «Aviso de YouTube». La apertura del directo de Twitch no demuestra la hora exacta de inicio del rol. Este calendario civil no fija fechas del mundo ficticio; las escenas escritas conservan sus fuentes y lectura editorial propias. El cotejo completo está en [Fechas de emisión y publicación](EMISIONES.md).

Los originales del canal de anuncios permanecen en el archivo privado local, con las respuestas JSON y sus SHA-256. El índice público conserva únicamente las evidencias de fechas y enlaces de Discord. Se puede verificar su integridad con `python scripts/fechas_emision.py --originales RUTA_DEL_ARCHIVO`.

Se conservan el intervalo inclusivo entre anuncios de referencia, los posibles días, los supuestos y la confianza cualitativa de las estimaciones. Por indicación del usuario se adoptan 22 fechas asumidas para la cronología: cuatro de Xoltacan y dieciocho de Kuroto. Todos los capítulos catalogados tienen un día elegido. Se guarda la aceptación y la procedencia previa sin convertirlas en fechas acreditadas por los avisos. Kuroto 55 y 56 adoptan conjuntamente el 9 y 10 de octubre de 2024 según el calendario: se conserva el aviso del 55 fechado el día 10 y se explican las dos rotulaciones presuntamente anteriores. Los avisos de Zaland o Campaña III utilizados para el contraste conservan su campaña original. El orden de capítulos se usa como hipótesis del orden de emisión, sin trasladarlo al calendario ficticio. Aceptar un día no fija una hora ni un corte exacto para el rol escrito.

Los calendarios del canal de información documentan programación prevista. Se leen las imágenes completas y se conservan los originales, sus hashes y las fechas de publicación y edición del mensaje. La programación se coteja con los avisos de directo: una fecha prevista no acredita realización y una hora prevista no acredita inicio real. Las indicaciones de subidas de YouTube del lateral permanecen separadas. Los cambios entre calendarios y los avisos con título anterior se conservan como discrepancias. Véase el [cotejo de programación](PROGRAMACION_TWITCH.md).

## Rol escrito de Discord

Las [interacciones de rol escrito](rol_escrito/INDICE.md) conservan el texto original completo y un relato editorial redactado después de leer todas sus fuentes. Las lecturas se reparten por hilos o bloques sin solapamiento; sus subescenas conservan una cobertura comprobada de los mensajes, sin duplicarlos ni perder los marcadores y el contexto. Las imágenes se inspeccionan; las notas de voz conservan su audio y una transcripción automática local, identificada como tal y susceptible de errores de nombres.

Las escenas se ordenan respecto a los directos originales de Twitch. En horario de Madrid, el final se estima sumando la duración del vídeo de YouTube a la hora de referencia de la tarjeta o, en su ausencia, del calendario. El rol anterior al final estimado se coloca antes de la sesión, admitiendo retrasos; el posterior se coloca después. Ese corte operativo no certifica horas reales: la edición del vídeo, los retrasos y las fechas asumidas limitan su precisión. Sin hora o duración suficiente se conserva la orientación por día y se explica la incertidumbre. Un FIN publicado tarde permanece con la conversación que cierra.

Las retrospectivas explícitas, los sueños, los recuerdos y las visiones conservan su condición. Si no existe un ancla inequívoca para recolocar una retrospectiva, se mantiene su fecha de publicación y la nota de lectura. Las acciones suelen escribirse en negrita y los pensamientos en cursiva, pero el contexto también puede identificar cartas, telepatía o acciones en cursiva. Se conserva el formato literal y se señalan las excepciones; un pensamiento no pasa a ser conocimiento de otros personajes.

Los originales privados incluyen las respuestas JSON, los metadatos de los hilos y sus adjuntos, con SHA-256. La enciclopedia incorpora el texto de la escena, fechas, referencias y adjuntos conservados, sin los perfiles de autores ni las credenciales del bot. Los mensajes reenviados se identifican aparte. Las fuentes y las identidades de Xoltacan y Kuroto permanecen separadas, incluso cuando una escena recuerda otra isla o un mismo jugador escribe varios personajes.

Los informes por hilo enlazan identidades, arcos, relaciones y cuestiones pendientes con sus mensajes exactos. Cada cuestión conserva el contexto de sus fuentes y los cotejos enlazan las respuestas halladas en otras escenas; la ausencia de cotejo no demuestra que siga abierta después de otros capítulos. Las interacciones posteriores al último vídeo incorporado se presentan como posteriores al catálogo, con referencias a directos conocidos, sin inventar capítulos revisados.

## Mantenimiento

Cada pregunta histórica tiene un identificador estable, su texto original y una revisión vinculada a registros posteriores. El estado `resuelta` requiere una respuesta a todo lo preguntado; `parcial` conserva expresamente la parte desconocida y `pendiente` no presupone una resolución fuera de las fuentes. Los testimonios y visiones mantienen su atribución incluso cuando aportan una respuesta. La validación exige evidencias posteriores para los estados resuelto y parcial y rechaza revisiones cuyo texto original haya cambiado.

Al incorporar capítulos, el seguimiento señala los cotejos anteriores que necesitan actualizarse y crea entradas sin revisar para nuevas preguntas. La aparición de palabras semejantes no cambia automáticamente el estado de una trama. El cotejo editorial se guarda en las recetas de `config/seguimiento_preguntas_*.json`; las salidas JSON, Markdown y HTML se regeneran con el constructor.

1. Registrar el episodio y recuperar VTT; errores de red se investigan antes de declarar ausencia.
2. Construir inventario y derivados; comprobar integridad.
3. Leer el siguiente episodio pendiente de principio a fin; preparar ficha JSON y citas.
4. Revisar nombres, resultados, consecuencias, acceso al conocimiento y preguntas abiertas.
5. Ejecutar el constructor para validar citas y actualizar índices.
6. Conservar dudas y revisar relaciones con los episodios ya documentados.

`revisado` significa que se leyó todo el episodio y se redactó una selección estructurada de hechos relevantes; no garantiza extracción exhaustiva de cada detalle. No implica audio cotejado ni revisión externa. Los episodios sin ficha permanecen pendientes aunque su transcripción ya esté preparada.
