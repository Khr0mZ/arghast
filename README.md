# Arghast · Archivo de campañas

**[Revisar la versión local](arghast.html)** · [Versión online anterior](https://khr0mz.github.io/arghast/) · [Estado del despliegue](https://github.com/Khr0mZ/arghast/actions/workflows/pages.yml)

El mundo se llama **Arghast**. **Xoltacan** y **Kuroto** son campañas distintas que se eligen desde una portada común o desde el selector de la barra lateral. Las búsquedas, fichas, capítulos y evidencias pertenecen exclusivamente a la campaña elegida. La selección forma parte de la URL (`?campana=xoltacan` o `?campana=kuroto`) y se conserva al navegar o compartir un enlace.

Cada ámbito conserva su identidad visual: Arghast usa mar gris azulado y ocres del mapa; Xoltacan combina sombras, oliva, azules, caliza y los acentos amarillo y rojo; Kuroto usa crema, turquesa, rosa cerezo y marrón, siguiendo muestras de las portadas aportadas. Los botones, la navegación y los paneles cambian de estilo con la campaña.

Los fondos abarcan toda el área de contenido. Arghast conserva el mapa oficial `arghast.webp` como fondo, con sus colores originales y capas de contraste mediante CSS. El original permanece intacto; `web/assets/arghast-mapa-oficial.webp` es la versión optimizada, con la misma resolución. Arghast, Xoltacan y Kuroto tienen ilustraciones verticales exclusivas para sus drawers. Las campañas tienen además fondos de contenido distintos de las portadas: un cenote selvático para Xoltacan y un jardín entre brumas para Kuroto. Las cinco imágenes se generan con imagegen y se integran sin conexión; sus prompts, originales y versiones WebP constan en [el registro de generación](web/assets/fondos-exclusivos.generacion.json).

Abrir **`arghast.html`** con doble clic para consultar el mismo archivo sin servidor. Conservar a su lado **`transcripciones/`** para los subtítulos de Kuroto y **`rol_escrito/`** para las escenas de Discord y sus adjuntos; los paquetes ZIP incluyen ambas. `xoltacan.html` se conserva como entrada compatible al archivo unificado. **`kuroto.html`** abre directamente Kuroto con los mismos componentes de capítulos y fichas; **`arghast.html`** permite elegir campaña. El contenido de Xoltacan mantiene sus 42 capítulos revisados, 1115 registros, 161 fichas de entidades y sus relatos.

**Estado de Kuroto:** 181 vídeos catalogados; 181 transcripciones (178 de YouTube y 3 locales). 181 sesiones con relato revisado, 2092 evidencias y 1257 fichas con historia. Revisión continua hasta el capítulo 182; 0 sesiones pendientes. La lectura de los bloques está completada; la versión permanece en local para revisión, sin publicación autorizada.

La publicación requiere que el usuario revise y apruebe expresamente la versión local. El flujo `.github/workflows/pages.yml` se ejecuta manualmente desde Actions, comprueba los datos, regenera la interfaz y publica `arghast.html` como `index.html`. No hacer `git push` ni ejecutar el despliegue antes de esa confirmación. El cambio de flujo permanece local hasta que se autorice su subida.

Para continuar la incorporación de Kuroto, usar `.venv/Scripts/python.exe scripts/importar_kuroto.py --descargar`. El importador conserva los VTT, verifica hashes y se detiene si YouTube limita las solicitudes. `--capitulo 1` permite limitar un intento; `--preparar` registra subtítulos aportados en la carpeta de fuentes. No se leen cookies del navegador. Una exportación aportada explícitamente puede indicarse con `--cookies RUTA`, guardándola fuera del repositorio. La lectura editorial y las citas siguen siendo necesarias después de recuperar los subtítulos; no se simulan mediante extracción de nombres o palabras clave.

El archivo revisado de Xoltacan reconstruye la campaña de Lichpol con buscador, capítulos, personajes, atlas, facciones, misiones, relaciones y misterios, con citas y enlaces al minuto. También puedes consultar su [índice Markdown](conocimiento/INDICE.md).

El HTML integra los 42 capítulos, 1115 registros y transcripciones de Xoltacan. Las 181 transcripciones de Kuroto se abren por sesión desde `transcripciones/kuroto/`, sin cargar todo el archivo al entrar en la portada. Permite buscar en registros o dentro de una transcripción, filtrar evidencias y leer el contexto de una cita. Con el HTML, las transcripciones y el archivo de rol disponibles localmente se pueden leer las fuentes conservadas sin conexión; los vídeos y los enlaces a Discord requieren Internet. La interfaz se regenera con `python scripts/construir_interfaz.py`; el proceso general de Xoltacan, `python scripts/construir.py`, también la actualiza.

Las fichas públicas se construyen con el catálogo revisado de identidades: las variantes confirmadas comparten ficha, y personajes, lugares, facciones y objetos tienen un tipo explícito. Las etiquetas originales siguen disponibles en la búsqueda. Las cautelas sobre transcripción y testimonios se consultan en las notas de cada capítulo. La prosa editorial utiliza español neutral; las citas literales conservan el reconocimiento original.

Las dos campañas comparten los términos Crónicas, Acontecimientos, Personajes, Lugares, Facciones y Vestigios, además de Misiones, Misterios y desenlaces y Relaciones. Vestigios reúne los objetos con historia: armas, artefactos, embarcaciones y otras pertenencias. Cada ficha vuelve a su sección. Lugares incluye el contexto geográfico del atlas y Facciones el contexto político.

Las portadas comparten estructura, accesos y etiquetas. **Leer historia** es la acción principal y abre la lectura continua; «Seguir los misterios» lleva al seguimiento de preguntas en ambas campañas. El catálogo permanece en Crónicas → Capítulos y los vídeos se abren desde cada ficha. El vocabulario común se define en `sections` dentro de `web/app.js`; los estilos y fondos siguen siendo propios de cada campaña.

Los 94 personajes incluyen **Su historia en Xoltacan**, un relato editorial dividido en etapas que conecta sus orígenes, aventuras y evolución hasta el capítulo 42. Cada etapa enlaza sus registros y minutos; después del relato se conservan las evidencias completas. Los personajes de aparición breve tienen una historia proporcional a lo documentado. Las mismas historias se incluyen en las fichas Markdown de `conocimiento/entidades/`.

Los **28 lugares**, las **8 facciones** y los **27 objetos** tienen también relatos propios: historia y acontecimientos de cada lugar, intereses y evolución de cada facción, y origen, usos y recorrido de cada objeto. Los registros quedan después del relato. Sus textos editoriales se conservan en `config/historias_lugares.json`, `config/historias_facciones.json` y `config/historias_objetos.json`, con referencias y horizonte de revisión.

Los **42 capítulos** abren en **Relato de la sesión**. Sus resúmenes revisados se conservan íntegros, separados en etapas con títulos y citas de esa misma sesión mediante `config/relatos_capitulos.json`. Las otras pestañas dan acceso a acontecimientos, misiones, preguntas y transcripción. Las divisiones se validan para no cortar frases, alterar el resumen ni incorporar referencias de capítulos posteriores. La construcción general regenera también esta presentación en las fichas Markdown.

Las historias de personajes se editan en `config/historias_personajes.json` y `config/historias_personajes_complementarias.json`; no se generan concatenando menciones. El constructor comprueba cobertura de todas las identidades canónicas, duplicados, referencias y horizonte de revisión mediante `scripts/historias.py`. Para revisar nuevos capítulos, actualizar la prosa, las referencias y `revisado_hasta` después de leer las fuentes, y definir las etapas de los nuevos resúmenes. Las entidades nuevas requieren su entrada editorial. Ejecutar `python scripts/construir.py` para regenerar todas las vistas Markdown y HTML.

**Misterios y desenlaces** coteja individualmente las 253 preguntas históricas de Xoltacan con los capítulos posteriores. Cada entrada conserva la pregunta original, el estado (resuelta, parcial o pendiente), la explicación y los registros que aportan la respuesta. Se puede buscar, filtrar por estado y consultar las citas y minutos. Cada capítulo incluye el mismo seguimiento junto a sus preguntas. La versión Markdown está en [SEGUIMIENTO.md](conocimiento/SEGUIMIENTO.md).

La revisión editorial se conserva en `config/seguimiento_preguntas_*.json`. `python scripts/seguimiento.py --exigir-completo` valida la cobertura, las referencias y la coincidencia de cada pregunta con su texto original; el constructor regenera JSON, Markdown y HTML. Los nuevos episodios producen entradas sin revisar y marcan las respuestas anteriores para cotejo: no se cierra una trama automáticamente por encontrar palabras parecidas. Cambiar una pregunta invalida su revisión anterior para evitar asociaciones erróneas.

Los borradores contienen la revisión vigente. `config/revision_editorial_vigente.json` reúne también los cambios editoriales de los 39 capítulos y puede aplicarse con `python scripts/aplicar_estilo.py config/revision_editorial_vigente.json`; este comando comprueba que los campos de evidencia no cambien. Después se regenera la biblioteca con el constructor. Las recetas anteriores se conservan como historial y no deben aplicarse sobre una revisión posterior.

## Fechas originales de emisión

Las fichas y las tarjetas de ambas campañas separan **Directo en Twitch**, **Publicación en YouTube** y **Aviso de YouTube** cuando el anuncio no documenta la publicación exacta. Xoltacan tiene fecha para **sus 42 capítulos: 38 documentadas y 4 asumidas**; Kuroto, para **sus 181 capítulos: 163 documentadas y 18 asumidas**. Todos los capítulos catalogados tienen un día de emisión elegido. El cotejo de información y anuncios adopta Kuroto 49 el 24/09/2024, el 56 el 10/10/2024 y el 134 el 02/07/2025. La reconstrucción conjunta de los capítulos 55 y 56 sitúa el 55 el 09/10/2024, conservando el aviso literal del día 10. El capítulo 41 de Xoltacan se emitió en Twitch el 3 de julio de 2026 y se publicó en YouTube el 20 de octubre.

Consultar el [cotejo de todas las fechas](conocimiento/EMISIONES.md), con enlaces a los anuncios. Los originales completos de Discord permanecen en local y se verifican por SHA-256. La interfaz integra las fechas desde `config/emisiones_xoltacan.json` y `campanas/kuroto/revision/emisiones.json`; `config/fuentes_anuncios_discord.json` conserva las evidencias de procedencia. Se muestran fechas civiles en Europe/Madrid, independientes del calendario ficticio del mundo y del comienzo exacto del rol dentro de cada directo.

Las [estimaciones de origen y sus decisiones](conocimiento/ESTIMACIONES_EMISIONES.md) se conservan en `config/estimaciones_emisiones.json`, con sus intervalos, fuentes, confianza y supuestos. Los 22 días asumidos figuran en los archivos de emisiones con fecha elegida y registro de la aceptación; la corrección del 55 conserva también la correspondencia previa. La interfaz muestra el día y explica su procedencia en «Fuentes de las fechas», incluidos los avisos de otras campañas utilizados para contrastar títulos arrastrados. Esos avisos conservan su identidad y no se convierten en pruebas directas de Kuroto. Los informes se regeneran mediante `python scripts/fechas_emision.py --informe-emisiones --informe-estimaciones --informe-programacion`. Aceptar el día no fija la hora ni un corte exacto para asignar escenas escritas.

El [cotejo de programación y emisiones](conocimiento/PROGRAMACION_TWITCH.md) incorpora la lectura completa de 193 mensajes y la revisión visual de 43 calendarios seleccionados para los casos estudiados. `config/programacion_twitch.json` conserva sus fuentes y hashes. La fecha y hora previstas permanecen separadas de la fecha adoptada; los cambios de programa y títulos contradictorios siguen visibles. Xoltacan 38 adopta el 15/06/2026 y el 40 el 02/07/2026. Kuroto 55 conserva la advertencia y la explicación de su corrección conjunta con el 56.

## Rol escrito de Discord

La continuación de las descargas utiliza **`.local/discord/sincronizacion_rol.json`**, un registro privado de la última sincronización completa y del último ID y fecha de mensaje de cada canal o hilo. Se inicializa verificando los hashes de la exportación existente, sin conexión ni nuevas descargas; conserva su fecha real de finalización: **20/10/2026 a las 17:26:05 en Madrid (15:26:05 UTC)**. La fecha del último mensaje se guarda por separado, pues puede ser anterior a la comprobación. La inicialización no actualiza artificialmente la fecha de sincronización.

En PowerShell, `powershell -NoProfile -ExecutionPolicy Bypass -File ./scripts/sincronizar_rol_discord.ps1 -Accion estado` consulta el registro sin usar credenciales; la política indicada solo afecta a ese proceso. Cambiar `estado` por `sincronizar` busca novedades con el token DPAPI local, que solo viaja por stdin. La entrada anterior `.local/discord/descargar_rol.ps1` utiliza también esta continuación. Para recuperar el registro desde un archivo conservado, si aún no existe, usar `-Accion inicializar`; no reemplaza un registro existente. El token solo puede abrirlo la cuenta de Windows que lo guardó.

Cada ejecución vuelve a enumerar los canales y los hilos activos y archivados accesibles, descarga el historial completo únicamente de los hilos nuevos y recorre los existentes desde los mensajes recientes hasta el punto guardado. También comprueba los **100 mensajes previos por hilo**, configurables con `-Ventana`, para detectar ediciones y ausencias recientes. Los adjuntos ya verificados se reutilizan por ID y hash. Esto no detecta ediciones o borrados fuera de esa ventana: para comprobarlos hace falta una revisión más amplia. Los originales anteriores no se sobrescriben ni se eliminan por una ausencia.

Los incrementos se guardan en `.local/discord/fuentes/rol_incremental/`, con las respuestas originales y sus hashes, una copia del registro anterior, los mensajes combinados por campaña y un informe de novedades. El registro solo avanza mediante reemplazo atómico al completar correctamente todos los hilos y adjuntos; si falla, el siguiente intento parte del último éxito. Un bloqueo local impide ejecuciones simultáneas. Si un proceso se cierra de forma forzada, comprobar que ya no está ejecutándose antes de retirar `.local/discord/sincronizacion_rol.lock`. El puntero de la exportación editorial original y sus ZIP permanecen conservados: los incrementos tienen su propio historial. Las novedades quedan en `pendientes_revision`; descargarlas no las convierte en escenas revisadas ni las publica. `python -m unittest discover -s scripts -p "test_sincronizar_rol_discord.py"` comprueba este flujo sin conectarse a Discord. El recorrido sigue la [paginación oficial de mensajes de Discord](https://docs.discord.com/developers/resources/message#get-channel-messages).

La exportación privada conserva **25.412 mensajes de 19 hilos**: 6.243 de Xoltacan y 19.169 de Kuroto, incluidos sus hilos de reglas. Contiene **154 adjuntos**, dos de ellos anidados en mensajes reenviados, y los audios originales de **28 notas de voz** junto con sus transcripciones automáticas. Los JSON originales y cada archivo descargado conservan hashes. Las exportaciones completas por campaña permanecen en el archivo privado local.

La lectura íntegra de **25.408 mensajes de rol**, repartidos en 715 unidades de revisión, produce **924 escenas: 304 de Xoltacan y 620 de Kuroto**. Cada escena incluye **relato editorial y texto original completo**, evidencias enlazadas a sus mensajes y los adjuntos conservados. Los cuatro mensajes de reglas permanecen en las exportaciones privadas. Se consulta desde **Crónicas → Escenas**, entre las tarjetas de capítulos o en las interacciones anteriores y posteriores a cada sesión. Las fichas de personajes enlazan sus escenas. Misiones, Misterios y desenlaces, Relaciones y Nombres incluyen 17 informes de hilo con sus propias fuentes y alcance temporal; los cotejos distinguen las respuestas comprobadas de lo que sigue sin aclararse en esas fuentes.

Crónicas ofrece un único selector de vista: **Leer historia**, **Capítulos** y **Escenas**. «Leer historia» (`#lectura`) reúne los relatos completos de capítulos y escenas en una lectura continua, respetando sus intervalos y sin repetir entradas. Empieza con seis relatos y añade bloques al acercarse al final, conservando el texto ya abierto y la posición de lectura. Las fuentes quedan plegadas y cada relato enlaza la ficha o los mensajes completos. Los enlaces `#lectura/capitulo/41` y `#lectura/rol/ID` permiten empezar desde un punto concreto; las fechas asumidas y las escenas posteriores al catálogo conservan sus avisos. No se cargan los mensajes originales para leer los relatos. La carga automática utiliza IntersectionObserver y dispone también de detección por desplazamiento y cambio de tamaño.

El botón flotante **Saltar a** permanece accesible durante la lectura. Abre un índice con buscador de capítulos, escenas y personajes participantes, incluyendo relatos que aún no se han mostrado. Elegir una entrada empieza la lectura desde ese punto. Escape o el botón de cierre recogen el índice; el buscador conserva el foco mientras se filtra y el control se oculta al abrir el menú lateral en móvil.

La posición utiliza las fechas de Twitch y las horas de referencia, con el final estimado a partir de la duración del vídeo de YouTube. El rol posterior a ese final se coloca después del capítulo; el cercano al inicio previsto permanece antes para admitir retrasos. Los cierres tardíos y el contexto no desplazan el diálogo. Los días asumidos, las retrospectivas y los directos sin vídeo conservan sus cautelas; esta ordenación no establece un calendario ficticio exacto.

El corpus editorial se conserva separado por campaña en `conocimiento/rol_escrito/` y `campanas/kuroto/conocimiento/rol_escrito/`. Sus manifests verifican las fichas y los adjuntos. `scripts/rol_escrito.py` valida la separación y genera **`rol_escrito/`**, con los mensajes de cada escena y sus archivos para lectura sin conexión. Mantener esa carpeta junto al HTML; ambos paquetes ZIP la incluyen. Las fuentes de duración están en `config/duraciones_rol.json`, contrastadas por identificador de vídeo y hash con los metadatos conservados.

Después de reconstruir la interfaz, `python -m unittest discover -s scripts -p "test_*.py"` comprueba los datos y cortes temporales. `node scripts/probar_rol.mjs` verifica las escenas reales y su navegación en Edge, además de la prueba general `node scripts/probar_interfaz.mjs`. La construcción y la revisión se hacen en local; la exportación o lectura no autoriza una publicación.

## Material disponible

Hay 42 capítulos catalogados, 84 VTT y 84 TXT conservados: dos variantes españolas por episodio (`es-orig` y `es`). Ningún episodio carece de subtítulos en este catálogo. Los subtítulos son automáticos y no prueban que todas las palabras del audio estén reconocidas correctamente. El inventario registra inicio, final, tamaño, variantes y SHA-256. No se han cotejado todas las duraciones con el vídeo ni verificado el audio.

El ZIP inicial de 6 KB contiene catálogo y descargador; el ZIP de transcripciones de aproximadamente 23 MB contiene las descargas. Se conservan ambos. El descargador inicial distingue solo `sin_subtitulos_o_error`: ese estado no permite concluir que falta una pista de YouTube. Se usa una sola variante por episodio para la lectura, dando preferencia a `es-orig`, y se conservan todas las variantes originales.

## Estructura

```text
xoltacan_subtitulos/           catálogo, descargador y originales conservados
  subtitulos/                 VTT y TXT originales; no editar
config/
  nombres.json                alias confirmados y nombres aportados por el usuario
  entidades.json              equivalencias editoriales con criterio y fuentes
  episodios_nuevos.json        episodios adicionales, creado cuando se añadan
scripts/
  construir_interfaz.py        genera los HTML y las transcripciones de Kuroto por sesión
  construir.py                inventario, derivados e índices incrementales
  incorporar.py               registro y descarga de nuevos episodios
  leer.py                     lectura integral por intervalos, sin resumen automático
  redactar.py                 convierte fichas editoriales compactas y localiza citas
  organizar.py                fichas enciclopédicas por entidad
  consultar.py                búsqueda global con tipos de evidencia y referencias
  auditar.py                  cobertura, citas, hashes y comparación con descarga ZIP
  empaquetar.py               ZIP completo o compacto, con verificación de entradas
borradores/                   fichas editoriales compactas, conservadas para reproducir la revisión
web/                          plantilla visual y aplicación JavaScript de la interfaz
xoltacan.html                 enciclopedia interactiva lista para abrir
derivados/
  originales_sha256.json      comprobación de integridad de TODOS los originales
  inventario.json             disponibilidad y estado de revisión por episodio
  01/ … 42/                   segmentos JSONL, lectura Markdown y cambios de nombres
conocimiento/
  INDICE.md                   capítulos y estado de revisión
  CRONOLOGIA.md               acontecimientos ordenados por episodio/minuto
  ENTIDADES.md                apariciones verificables de personajes y lugares
  FICHAS.md y entidades/      fichas con evolución documentada bajo cada etiqueta
  NOMBRES.md                  equivalencias, grafías provisionales y separaciones
  RELACIONES.md              vínculos acreditados, fechados y sus límites
  ATLAS.md y FACCIONES.md     regiones, lugares, organizaciones e intereses atribuidos
  MISIONES.md                 encargos, objetivos, resultados y consecuencias
  PREGUNTAS.md                misterios y tramas sin resolución documentada
  MISTERIOS.md                estado actual, resoluciones posteriores y preguntas restantes
  CONTRADICCIONES.md          discrepancias conservadas
  TRAMAS.md                   seguimiento editorial de pistas y resoluciones entre episodios
  PROGRESO.md                 estado de lectura y punto exacto de continuación
  CONTEXTO_USUARIO.md         información del usuario, separada de los vídeos
  METODO.md                   criterio de evidencia y atribución de declaraciones
  GUIA_CONSULTA.md             instrucciones y ejemplos de consulta verificable
  capitulos/01.json, 01.md     ficha editable estructurada y documento generado
```

## Ejecutar

Desde la raíz, con Python 3.10 o superior:

```powershell
python scripts/construir.py
```

No necesita Internet, API, créditos ni dependencias externas. Conserva los originales, detecta cambios o desapariciones mediante hashes y regenera únicamente los derivados cuyo origen, reglas o código han cambiado. `--reconstruir` recalcula los derivados; no permite ignorar cambios en originales. Los índices y fichas Markdown se generan desde las fichas JSON: editar el JSON, no el Markdown generado.

La versión utilizada en la descarga inicial está fijada en `requirements-descarga.txt`. Para reproducir ese entorno: `python -m pip install -r requirements-descarga.txt`. Si YouTube cambia y exige otra versión, actualizarla deliberadamente y anotar la versión utilizada. Las pruebas de limpieza y validación de citas se ejecutan con `python scripts/test_construir.py`.

Para registrar un nuevo episodio (sustituir los valores de ejemplo por los reales):

```powershell
.\.venv\Scripts\python.exe scripts/incorporar.py --capitulo 42 --url "https://www.youtube.com/watch?v=ID_DE_VIDEO" --titulo "Título real" --descargar
```

El ejemplo usa un identificador ficticio y no se ejecuta literalmente. Para reintentar todos los episodios que no tengan VTT válido:

```powershell
.\.venv\Scripts\python.exe scripts/incorporar.py --descargar
```

La descarga requiere conexión y `yt-dlp` instalado. No descarga vídeos ni audio. La incorporación prepara automáticamente inventario, segmentos y entrada pendiente en el índice. La lectura interpretativa y validación de hechos requieren revisión: el programa no inventa resúmenes ni simula una revisión con palabras clave. El siguiente episodio a revisar es el primero marcado pendiente, en orden numérico.

## Consultar desde ChatGPT

En este proyecto, el agente puede leer el índice y buscar en Markdown o en los originales con `rg`. En otro chat es necesario adjuntar los archivos relevantes o un paquete; crear estos archivos no conecta automáticamente todos los chats a esta carpeta. Para respuestas sobre el canon, buscar primero fichas revisadas y después comprobar los pasajes originales. Las transcripciones pendientes sirven para localizar evidencia, no como hechos ya contrastados.

Ejemplos locales:

```powershell
rg -n -i "Bonnie|pirámides|cadenas" conocimiento derivados/01/lectura.md
rg -n -i "Oghma|Jivirix" derivados -g lectura.md
python -X utf8 scripts/consultar.py "Tutucan"
python -X utf8 scripts/consultar.py "Jivirix"
python -X utf8 scripts/consultar.py "casino" --personaje Axi
```

Los 42 capítulos disponibles se han leído completos y cuentan con fichas estructuradas: 1115 registros de acontecimientos, declaraciones y explicaciones con citas temporales. La reconstrucción cubre el material publicado de este catálogo; las tramas abiertas se mantienen con su seguimiento actualizado al capítulo 42. El estado de cada capítulo figura en el índice.

Las búsquedas de nombres pueden fallar por reconocimiento de voz; una ausencia en la búsqueda no prueba una ausencia en la sesión. Las fichas seleccionan acontecimientos relevantes y no sustituyen el diálogo original ni un cotejo de audio.

El archivo reúne enciclopedias de Xoltacan y Kuroto bajo el mundo Arghast. Cada campaña conserva su canon y sus identidades. En Xoltacan no se filtra por conocimiento de Oghma. Las declaraciones, escenas privadas y datos del director se incluyen con su atribución y límites.

Para generar paquetes después de construir y auditar:

```powershell
python -X utf8 scripts/empaquetar.py
python -X utf8 scripts/empaquetar.py --solo-conocimiento
```

El paquete completo incluye originales y herramientas; el compacto contiene la enciclopedia, documentación y lecturas Markdown de los episodios para que funcionen los enlaces de consulta. Para VTT/TXT originales y reproducir el procesamiento, usar el completo. Cada entrada se comprueba contra el archivo local antes de sustituir el ZIP previo.

Las portadas oficiales aportadas (`Xoltacan.png` y `Kuroto.png` (versiones sin número de episodio)) se muestran completas tanto en el selector como en cada inicio, separadas de los textos y botones. `lichpol.jpg` identifica el sidebar. Los originales se conservan intactos; las copias WebP y sus hashes figuran en `web/assets/imagenes-aportadas.procedencia.json`.

Las paletas se definen en `web/paletas.css` y se apoyan en el [muestreo por regiones](web/assets/paletas-muestreo.json) de las portadas y el mapa. Los materiales ilustrados, las veladuras y los distintos acentos sustituyen los bloques de color plano; el papel se reserva principalmente para los relatos largos. Los drawers se alinean a la derecha y las barras de desplazamiento son finas en todas las vistas. La interfaz usa nombres y acciones directos, sin lemas; se conservan los relatos y fuentes de las fichas.

Los paneles de portada, cifras, accesos y catalogos usan materiales ilustrados exclusivos: jade tallado y bronce en Xoltacan, laca azul y ondas doradas en Kuroto. Los colores de interfaz se limitan a las paletas oficiales aportadas por el usuario; las texturas se conservan como ilustraciones decorativas. Los relatos largos conservan superficies de lectura calidas. Originales, prompts y WebP: `web/assets/materiales-paneles.generacion.json`.

Las paletas autoritativas son los 16 HEX de cada campaña aportados por el usuario, guardados en `config/paletas_campanas.json`. Xoltacan usa sombras y oliva, azules de cielo, caliza, amarillo y rojo del título; Kuroto combina crema, turquesa, coral y marrón. Los bordes son comunes dentro de cada campaña y los colores se asignan por función, sin arcoíris por categoría. Se conservan los materiales ilustrados.

Las texturas activas se editaron con las paletas HEX aportadas: `web/assets/xoltacan-panel-paleta.webp` usa piedra oscura, oliva y caliza con vetas azul gris; `web/assets/kuroto-panel-paleta.webp` usa laca turquesa, incrustaciones crema y flores coral. Se conserva el relieve de las versiones anteriores. Prompts, archivos de referencia y hashes: `web/assets/materiales-paneles-paleta.generacion.json`.

Cada topbar tiene una textura horizontal exclusiva de su vista. Arghast suma un panel de atlas con brujula, piedra azul y ocres, y cifras calculadas desde las campanas disponibles. El mapa oficial sigue siendo el fondo. Originales, prompts y archivos optimizados: `web/assets/cabeceras-atlas.generacion.json`.

Tipografía de campañas: **Karate** (Gary D. Jessey, freeware) en Kuroto y **Ambystoma Mexicanum** (Chequered Ink) en Xoltacan, aplicadas al sidebar, la topbar, botones, pestañas, accesos y encabezados de sección. Ambystoma usa rótulos PNG transparentes con el texto original accesible y seleccionable; la licencia gratuita no comercial restringe incrustar el OTF extraíble, que no se distribuye. Los gráficos adoptan el color del control mediante máscaras CSS, conservan las tildes y se incrustan para uso sin conexión. `scripts/generar_rotulos.py --fuente RUTA` regenera los rótulos con una copia local de la fuente y Pillow; la construcción ordinaria utiliza los PNG guardados. Karate usa Kaisei Tokumin como apoyo para los caracteres españoles ausentes. Los relatos y los nombres dinámicos de Xoltacan mantienen Macondo/Georgia; Arghast y su nombre en el sidebar usan **IM Fell English SC 400**, de Igino Marini (OFL), también aplicada a la topbar y los controles de Arghast. Fuentes OFL y freeware, procedencia y licencias en `web/assets/fonts/`, `web/assets/rotulos-xoltacan.procedencia.json` y `web/assets/xoltacan-titulo.licencia.html`. Estilos en `web/tipografia.css` y `web/rotulos.css`.

El **capítulo 40, El Festival del Anciano de Piedra** (publicado el 18/10/2026), está incorporado con lectura íntegra en tres bloques, 42 registros citados, ocho etapas de relato y ocho fichas nuevas. El seguimiento de preguntas queda cotejado hasta el 40, incluyendo el paradero de Triel y el origen declarado por Ilikar. Se conservan los testimonios incompatibles sobre la edad de Tortas y las cautelas sobre las identidades de los dragones y de los elfos del capítulo 39. Véanse [la continuidad](conocimiento/continuidad_40.md) y [la procedencia y hashes](config/fuente_xoltacan_40.json).

El **capítulo 41, Serpientes en Iktan** (publicado en YouTube el 20/10/2026), está incorporado con lectura íntegra en tres bloques, 55 registros citados, diez etapas de relato y ocho fichas nuevas. Las 235 preguntas anteriores se han cotejado y se añaden once: 246 en total. Cipo queda localizado; la advertencia de Leona se concreta en la infiltración. Se conserva la incertidumbre sobre «ella», el cautivo, los venenos y el nombre del dragón. Véanse [la continuidad](conocimiento/continuidad_41.md) y [la procedencia y hashes](config/fuente_xoltacan_41.json). Esta incorporación permanece en local para revisión, sin publicación autorizada.

El **capítulo 42, Batalla en el Arrecife del Garfio** (directo del 09/07/2026; publicado en YouTube el 25/10/2026), está incorporado con lectura íntegra en tres bloques sin solapamiento, 72 evidencias, trece etapas y ocho fichas nuevas. Las 246 preguntas anteriores están cotejadas y se añaden siete: 253 en total. El Zampaolas vuelve a navegar, Nox libera a Pinky y llegan los cuatro reyes restantes. Se conservan el desenlace del Invictus, la despedida del director y los límites de la búsqueda y del disparo final. Véanse [la continuidad](conocimiento/continuidad_42.md) y [la procedencia con hashes](config/fuente_xoltacan_42.json). Versión local para revisión, sin publicación autorizada.
