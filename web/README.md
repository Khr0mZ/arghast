# Interfaz local de Xoltacan

La edición de jugadores por código se explica en [EDICION.md](EDICION.md). La web publicada utiliza el servicio online de Sites y guarda las correcciones sin ejecutar nada en local. Para revisar cambios en localhost se conserva el servidor Python; el HTML abierto con doble clic permite consultar el archivo.

La interfaz ahora es el archivo de **Arghast**, con portada de campañas y selector entre Xoltacan y Kuroto. El constructor genera `../arghast.html` y conserva `../xoltacan.html` como entrada compatible al mismo contenido. `arghast.css` añade la portada, el selector y el tema de Kuroto. La consulta `campana` de la URL selecciona el archivo activo; las rutas, búsquedas, entidades y transcripciones se resuelven solo dentro de él.

`../scripts/campanas.py` integra el archivo revisado de Xoltacan con el catálogo independiente de Kuroto. Los títulos de vídeo no producen hechos. Ambas campañas conservan sus relatos revisados y sus evidencias. `ARGHAST_TEST_URL=https://khr0mz.github.io/arghast/` permite ejecutar la prueba de navegador contra el despliegue público.

Abrir `../arghast.html` con doble clic para elegir campaña. Cada lector independiente está en `../campanas/<campaña>/publico/index.html`: su carpeta `publico/` contiene todos los datos, transcripciones, escenas y adjuntos que necesita. Se puede copiar completa a otro lugar y consultar sin servidor. Los enlaces a vídeos sí requieren Internet.

Fuentes de la interfaz:

- `plantilla.html`: estructura y estilos base adaptables.
- `selva.css`: tema de isla selvática, portada y navegación de exploración.
- `codice.css`: contenido como códice de rol: pergaminos, emblemas, controles de jade y bronce, pestañas y citas ornamentadas. Se integra después del tema selvático.
- `../campanas/<campaña>/web/assets/`: imágenes, fuentes y licencias propias, integradas como datos en el lector para funcionar sin conexión.
- `../campanas/<campaña>/web/estilos/`: reglas visuales específicas. Los marcadores de los CSS compartidos conservan su posición para recomponer exactamente el orden original.
- `app.js`: búsqueda, navegación, filtros, fichas, citas y contexto.
- `../scripts/construir_interfaz.py` y `compilar_web.py`: generan el visor común y los lectores con sus datos y recursos.

La construcción general regenera también la interfaz. Para actualizar solo HTML:

```powershell
python -X utf8 scripts/construir_interfaz.py
```

Las fichas muestran historia, rol escrito, registros e identificación en apartados visibles, con un índice «Saltar a». El seguimiento escrito de misiones, misterios y relaciones, las evidencias y las notas de voz también se leen sin desplegarlos. Solo los justificantes de fechas y las opciones de edición conservan desplegables. Las vistas de crónicas distinguen la lectura continua, los capítulos y las escenas; los catálogos de lugares y facciones enlazan sus documentos de contexto en una vista propia. «Fuentes y método» deja de ser una página de la interfaz; se conserva el documento de archivo y las citas permanecen junto a los contenidos.

Comprobaciones reales de navegador:

```powershell
node scripts/probar_interfaz.mjs
node scripts/probar_autonomia.mjs
node scripts/probar_carga.mjs
```

La prueba utiliza Chrome o Edge local en modo sin ventana y un perfil nuevo dentro de `.pruebas/interfaz/`. Comprueba archivo local, búsqueda, filtros, citas, contexto, transcripciones, documentos, teclado y diseño móvil; guarda capturas de escritorio/móvil y cierra el navegador al terminar. No utiliza el perfil personal del navegador.

`carga.js` y `carga.css` muestran el indicador antes de cargar los datos y ocultan la interfaz hasta completar el primer render y las fuentes. Cada campaña aporta sus colores y tipografía en `web/estilos/carga.css`: Karate en Kuroto y rótulos accesibles de Ambystoma en Xoltacan. Arghast usa IM Fell English SC. La prueba de carga retiene las respuestas de datos para comprobar las fuentes realmente dibujadas, las paletas, las transiciones por enlace y selector, el móvil, movimiento reducido y la recuperación de un error.

El HTML se genera desde las fichas revisadas y lecturas derivadas; no modifica las transcripciones originales. Los JSON históricos de conocimiento personal no se usan para filtrar información de la interfaz.

El paisaje es una ambientación artística de la isla, no un mapa canónico. Su procedencia y el prompt se conservan en `../campanas/xoltacan/web/assets/imagen-procedencia.json`.

Todas las fichas muestran primero un relato por etapas y después sus registros. Los personajes tienen su historia; los lugares, sus acontecimientos; las facciones, sus intereses y evolución; y los objetos, su origen y recorrido. La prosa editorial de Xoltacan procede de `../campanas/xoltacan/config/historias_*.json`; cada etapa conserva referencias navegables al registro original y su minuto. `../scripts/historias.py` valida cobertura de todas las identidades canónicas, referencias y horizonte de revisión.

Los capítulos abren en la pestaña `Relato de la sesión`. `../campanas/xoltacan/config/relatos_capitulos.json` define títulos, comienzos de etapa y citas locales; el constructor conserva íntegro el resumen revisado de cada capítulo. Acontecimientos, misiones, preguntas y transcripción siguen disponibles en pestañas independientes. Para regenerar también los capítulos Markdown, ejecutar la construcción general: `python scripts/construir.py`.

`python scripts/test_historias.py` comprueba cobertura, integridad de los resúmenes y errores editoriales detectables. La prueba de navegador verifica los relatos de todas las categorías, sus citas y las fichas a 320 y 768 píxeles, y guarda capturas de escritorio y móvil.
