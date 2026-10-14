# Arghast · Archivo de campañas

**[Abrir la enciclopedia online](https://khr0mz.github.io/arghast/)** · [Estado del despliegue](https://github.com/Khr0mZ/arghast/actions/workflows/pages.yml)

El mundo se llama **Arghast**. **Xoltacan** y **Kuroto** son campañas distintas que se eligen desde una portada común o desde el selector de la barra lateral. Las búsquedas, fichas, capítulos y evidencias pertenecen exclusivamente a la campaña elegida. La selección forma parte de la URL (`?campana=xoltacan` o `?campana=kuroto`) y se conserva al navegar o compartir un enlace.

Abrir **`arghast.html`** con doble clic para consultar el mismo archivo sin servidor. Conservar a su lado la carpeta **`transcripciones/`** para abrir los subtítulos de Kuroto; los paquetes ZIP la incluyen. `xoltacan.html` se conserva como entrada compatible al archivo unificado. El contenido de Xoltacan mantiene sus 39 capítulos revisados, 946 registros, 137 fichas de entidades y sus relatos.

**Estado de Kuroto:** 181 vídeos catalogados y **178 sesiones con subtítulos recuperados** mediante el mismo procedimiento que `xoltacan_subtitulos`. Los vídeos 96, 135 y 136 no ofrecen subtítulos manuales ni automáticos según la consulta del 14 de octubre de 2026; el 92 no figura en la lista consultada. **La revisión narrativa llega al capítulo 1**, con 24 evidencias, diez fichas con historia y dos preguntas de seguimiento. Las otras 180 sesiones están pendientes de lectura editorial, tengan o no transcripción. Fuentes y catálogo: `campanas/kuroto/`.

GitHub Pages se actualiza automáticamente al subir cambios a `main`. El flujo `.github/workflows/pages.yml` comprueba los datos, regenera la interfaz y publica `arghast.html` como `index.html`. También puede ejecutarse manualmente desde Actions.

Para continuar la incorporación de Kuroto, usar `.venv/Scripts/python.exe scripts/importar_kuroto.py --descargar`. El importador conserva los VTT, verifica hashes y se detiene si YouTube limita las solicitudes. `--capitulo 1` permite limitar un intento; `--preparar` registra subtítulos aportados en la carpeta de fuentes. No se leen cookies del navegador. Una exportación aportada explícitamente puede indicarse con `--cookies RUTA`, guardándola fuera del repositorio. La lectura editorial y las citas siguen siendo necesarias después de recuperar los subtítulos; no se simulan mediante extracción de nombres o palabras clave.

El archivo revisado de Xoltacan reconstruye la campaña de Lichpol con buscador, capítulos, personajes, atlas, facciones, misiones, relaciones y misterios, con citas y enlaces al minuto. También puedes consultar su [índice Markdown](conocimiento/INDICE.md).

El HTML integra los 39 capítulos, 946 registros y transcripciones de Xoltacan. Las 178 transcripciones de Kuroto se abren por sesión desde `transcripciones/kuroto/`, sin cargar todo el archivo al entrar en la portada. Permite buscar en registros o dentro de una transcripción, filtrar evidencias y leer el contexto de una cita. Con el HTML y la carpeta de transcripciones disponibles localmente, solo abrir el vídeo requiere Internet. La interfaz se regenera con `python scripts/construir_interfaz.py`; el proceso general de Xoltacan, `python scripts/construir.py`, también la actualiza.

Las fichas públicas se construyen con el catálogo revisado de identidades: las variantes confirmadas comparten ficha, y personajes, lugares, facciones y objetos tienen un tipo explícito. Las etiquetas originales siguen disponibles en la búsqueda. Las cautelas sobre transcripción y testimonios se consultan en las notas de cada capítulo. La prosa editorial utiliza español neutral; las citas literales conservan el reconocimiento original.

La navegación ofrece cuatro secciones independientes: Personajes, Lugares, Facciones y Objetos. Cada ficha vuelve a su sección. Lugares incluye el contexto geográfico del atlas y Facciones incluye el contexto político, sin otro catálogo general que repita sus contenidos. El buscador superior permite consultar todo el archivo.

Los 81 personajes incluyen **Su historia en Xoltacan**, un relato editorial dividido en etapas que conecta sus orígenes, aventuras y evolución hasta el capítulo 39. Cada etapa enlaza sus registros y minutos; después del relato se conservan las evidencias completas. Los personajes de aparición breve tienen una historia proporcional a lo documentado. Las mismas historias se incluyen en las fichas Markdown de `conocimiento/entidades/`.

Los **25 lugares**, las **8 facciones** y los **23 objetos** tienen también relatos propios: historia y acontecimientos de cada lugar, intereses y evolución de cada facción, y origen, usos y recorrido de cada objeto. Los registros quedan después del relato. Sus textos editoriales se conservan en `config/historias_lugares.json`, `config/historias_facciones.json` y `config/historias_objetos.json`, con referencias y horizonte de revisión.

Los **39 capítulos** abren en **Relato de la sesión**. Sus resúmenes revisados se conservan íntegros, separados en etapas con títulos y citas de esa misma sesión mediante `config/relatos_capitulos.json`. Las otras pestañas dan acceso a acontecimientos, misiones, preguntas y transcripción. Las divisiones se validan para no cortar frases, alterar el resumen ni incorporar referencias de capítulos posteriores. La construcción general regenera también esta presentación en las fichas Markdown.

Las historias de personajes se editan en `config/historias_personajes.json` y `config/historias_personajes_complementarias.json`; no se generan concatenando menciones. El constructor comprueba cobertura de todas las identidades canónicas, duplicados, referencias y horizonte de revisión mediante `scripts/historias.py`. Para revisar nuevos capítulos, actualizar la prosa, las referencias y `revisado_hasta` después de leer las fuentes, y definir las etapas de los nuevos resúmenes. Las entidades nuevas requieren su entrada editorial. Ejecutar `python scripts/construir.py` para regenerar todas las vistas Markdown y HTML.

**Preguntas y desenlaces** coteja individualmente las 228 preguntas históricas con los capítulos posteriores. Cada entrada conserva la pregunta original, el estado (resuelta, parcial o pendiente), la explicación y los registros que aportan la respuesta. Se puede buscar, filtrar por estado y consultar las citas y minutos. Cada capítulo incluye el mismo seguimiento junto a sus preguntas. La versión Markdown está en [SEGUIMIENTO.md](conocimiento/SEGUIMIENTO.md).

La revisión editorial se conserva en `config/seguimiento_preguntas_*.json`. `python scripts/seguimiento.py --exigir-completo` valida la cobertura, las referencias y la coincidencia de cada pregunta con su texto original; el constructor regenera JSON, Markdown y HTML. Los nuevos episodios producen entradas sin revisar y marcan las respuestas anteriores para cotejo: no se cierra una trama automáticamente por encontrar palabras parecidas. Cambiar una pregunta invalida su revisión anterior para evitar asociaciones erróneas.

Los borradores contienen la revisión vigente. `config/revision_editorial_vigente.json` reúne también los cambios editoriales de los 39 capítulos y puede aplicarse con `python scripts/aplicar_estilo.py config/revision_editorial_vigente.json`; este comando comprueba que los campos de evidencia no cambien. Después se regenera la biblioteca con el constructor. Las recetas anteriores se conservan como historial y no deben aplicarse sobre una revisión posterior.

## Material disponible

Hay 39 capítulos catalogados, 78 VTT y 78 TXT originales: dos variantes españolas por episodio (`es-orig` y `es`). Ningún episodio carece de subtítulos en este catálogo. Los subtítulos son automáticos y no prueban que todas las palabras del audio estén reconocidas correctamente. El inventario registra inicio, final, tamaño, variantes y SHA-256. No se han cotejado todas las duraciones con el vídeo ni verificado el audio.

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
  01/ … 39/                   segmentos JSONL, lectura Markdown y cambios de nombres
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
.\.venv\Scripts\python.exe scripts/incorporar.py --capitulo 40 --url "https://www.youtube.com/watch?v=ID_DE_VIDEO" --titulo "Título real" --descargar
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

Los 39 capítulos disponibles se han leído completos y cuentan con fichas estructuradas: 946 registros de acontecimientos, declaraciones y explicaciones con citas temporales. La reconstrucción cubre el material publicado de este catálogo; las tramas abiertas al capítulo 39 permanecen abiertas. El estado de cada capítulo figura en el índice.

Las búsquedas de nombres pueden fallar por reconocimiento de voz; una ausencia en la búsqueda no prueba una ausencia en la sesión. Las fichas seleccionan acontecimientos relevantes y no sustituyen el diálogo original ni un cotejo de audio.

El alcance final solicitado es una enciclopedia global de Xoltacan. No se filtra por conocimiento de Oghma. Las declaraciones, escenas privadas y datos del director se incluyen con su atribución y límites.

Para generar paquetes después de construir y auditar:

```powershell
python -X utf8 scripts/empaquetar.py
python -X utf8 scripts/empaquetar.py --solo-conocimiento
```

El paquete completo incluye originales y herramientas; el compacto contiene la enciclopedia, documentación y lecturas Markdown de los episodios para que funcionen los enlaces de consulta. Para VTT/TXT originales y reproducir el procesamiento, usar el completo. Cada entrada se comprueba contra el archivo local antes de sustituir el ZIP previo.
