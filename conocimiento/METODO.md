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
