# Interfaz local de Xoltacan

La interfaz ahora es el archivo de **Arghast**, con portada de campañas y selector entre Xoltacan y Kuroto. El constructor genera `../arghast.html` y conserva `../xoltacan.html` como entrada compatible al mismo contenido. `arghast.css` añade la portada, el selector y el tema de Kuroto. La consulta `campana` de la URL selecciona el archivo activo; las rutas, búsquedas, entidades y transcripciones se resuelven solo dentro de él.

`../scripts/campanas.py` integra el archivo revisado de Xoltacan con el catálogo independiente de Kuroto. Los títulos de vídeo no producen hechos. El estado de recuperación y revisión de Kuroto se muestra expresamente mientras faltan sus fuentes. `ARGHAST_TEST_URL=https://khr0mz.github.io/arghast/` permite ejecutar la prueba de navegador contra el despliegue público.

Abrir `../xoltacan.html` con doble clic. Es un archivo autónomo: diseño, aplicación, capítulos, evidencias y transcripciones están integrados. No utiliza CDN, servidor, cuentas ni API. Los enlaces a vídeos sí requieren Internet.

Fuentes de la interfaz:

- `plantilla.html`: estructura y estilos base adaptables.
- `selva.css`: tema de isla selvática, portada y navegación de exploración.
- `codice.css`: contenido como códice de rol: pergaminos, emblemas, controles de jade y bronce, pestañas y citas ornamentadas. Se integra después del tema selvático.
- `assets/xoltacan-selva.webp`: paisaje generado, integrado como imagen de datos en el HTML final para funcionar sin conexión.
- `app.js`: búsqueda, navegación, filtros, fichas, citas y contexto.
- `../scripts/construir_interfaz.py`: empaqueta datos y código en el HTML final.

La construcción general regenera también la interfaz. Para actualizar solo HTML:

```powershell
python -X utf8 scripts/construir_interfaz.py
```

Comprobaciones reales de navegador:

```powershell
node scripts/probar_interfaz.mjs
```

La prueba utiliza Chrome o Edge local en modo sin ventana y un perfil nuevo dentro de `.pruebas/interfaz/`. Comprueba archivo local, búsqueda, filtros, citas, contexto, transcripciones, documentos, teclado y diseño móvil; guarda capturas de escritorio/móvil y cierra el navegador al terminar. No utiliza el perfil personal del navegador.

El HTML se genera desde las fichas revisadas y lecturas derivadas; no modifica las transcripciones originales. Los JSON históricos de conocimiento personal no se usan para filtrar información de la interfaz.

El paisaje es una ambientación artística de la isla, no un mapa canónico. Su procedencia y el prompt se conservan en `assets/imagen-procedencia.json`.

Todas las fichas muestran primero un relato por etapas y después sus registros. Los personajes tienen su historia; los lugares, sus acontecimientos; las facciones, sus intereses y evolución; y los objetos, su origen y recorrido. La prosa editorial procede de `../config/historias_*.json`; cada etapa conserva referencias navegables al registro original y su minuto. `../scripts/historias.py` valida cobertura de todas las identidades canónicas, referencias y horizonte de revisión.

Los capítulos abren en la pestaña `Relato de la sesión`. `../config/relatos_capitulos.json` define títulos, comienzos de etapa y citas locales; el constructor conserva íntegro el resumen revisado de cada capítulo. Acontecimientos, misiones, preguntas y transcripción siguen disponibles en pestañas independientes. Para regenerar también los capítulos Markdown, ejecutar la construcción general: `python scripts/construir.py`.

`python scripts/test_historias.py` comprueba cobertura, integridad de los resúmenes y errores editoriales detectables. La prueba de navegador verifica los relatos de todas las categorías, sus citas y las fichas a 320 y 768 píxeles, y guarda capturas de escritorio y móvil.
