# Archivos de las campañas de Arghast

Xoltacan y Kuroto comparten esta estructura:

```text
campanas/
  xoltacan/                 kuroto/
    catalogo.json            catalogo.json
    config/                  config/
    fuentes/                 fuentes/
    revision/                revision/
    conocimiento/            conocimiento/
    derivados/               derivados/
    web/                     web/
    publico/                 publico/
```

`catalogo.json` es el catálogo activo de cada campaña. `config/` contiene sus nombres, equivalencias, fechas y reglas editoriales. `fuentes/` conserva los originales y sus metadatos; las fuentes VTT se leen directamente desde esa carpeta. `revision/` mantiene las entregas, los borradores y la procedencia de las revisiones. `conocimiento/` contiene las fichas y el rol escrito. `derivados/` contiene inventarios y lecturas que se pueden regenerar.

La estructura común no mezcla identidades ni evidencias. Los relatos, los identificadores, los mensajes, los hashes de los originales y las paletas siguen perteneciendo a su campaña. Los formatos editoriales existentes se conservan y sus constructores entregan el mismo modelo a la interfaz.

`web/` contiene los estilos, imágenes, tipografías, rótulos y licencias propios de cada campaña. `config/` incluye también su paleta de 16 HEX, duraciones del rol, anuncios de Discord, estimaciones y programación de Twitch. Los avisos ajenos utilizados como contraste conservan su identidad explícita.

`publico/` es el lector independiente generado: `index.html`, `datos.js`, `transcripciones/` y `rol_escrito/`, con `escenas/` y `adjuntos/`. Se puede copiar esa carpeta a otro lugar y abrir su `index.html` sin conexión ni archivos de la otra campaña. Las dos usan el mismo sistema de carga por sesión y por escena.

En la raíz del proyecto, `scripts/`, `web/` y `online/` contienen las herramientas, la interfaz y los servicios comunes. `arghast.html` reúne ambas campañas leyendo sus datos desde sus respectivos directorios; `xoltacan.html` y `kuroto.html` conservan las entradas anteriores, incluidos la consulta y el fragmento de sus enlaces. Los identificadores y las correcciones guardadas del editor se mantienen. [rutas.py](../scripts/rutas.py) declara las ubicaciones.

`python scripts/construir_interfaz.py` regenera los lectores y el visor común. `node scripts/probar_autonomia.mjs` comprueba ambas campañas copiando solo su carpeta pública y rechazando cualquier petición de archivos externa a ella. `python scripts/preparar_publicacion.py` prepara `_site` localmente con los lectores públicos; no publica ni incluye originales privados. Ambos ZIP incorporan los lectores desde sus directorios.

La descarga inicial de Xoltacan se conserva en `xoltacan/fuentes/descarga_inicial/`, y los dos ZIP originales en `xoltacan/fuentes/paquetes_originales/`. Sus catálogos históricos documentan aquella descarga; las incorporaciones actuales se registran en `xoltacan/catalogo.json` mediante `scripts/incorporar.py`.
