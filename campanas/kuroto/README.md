# Kuroto · Campaña de Arghast

[Lista oficial de Lichpol](https://www.youtube.com/playlist?list=PLelQK3I2Q5zymJZ2e2SNmwxsnnFGjBCYb).

**Estado de Kuroto:** 181 vídeos catalogados y **178 sesiones con subtítulos recuperados** mediante el mismo procedimiento que `xoltacan_subtitulos`. Los vídeos 96, 135 y 136 no ofrecen subtítulos manuales ni automáticos según la consulta del 14 de octubre de 2026; el 92 no figura en la lista consultada. **La revisión narrativa llega al capítulo 1**, con 24 evidencias, diez fichas con historia y dos preguntas de seguimiento. Las otras 180 sesiones están pendientes de lectura editorial, tengan o no transcripción. Fuentes y catálogo: `campanas/kuroto/`.

La lista contiene 181 vídeos numerados hasta el 182. Se conserva el hueco del 92 y se ordenan correctamente el 169 y el 170. No se usa el título como evidencia narrativa.

## Recuperación de fuentes

El primer acceso devolvió HTTP 429. La repetición con los argumentos exactos del descargador de Xoltacan sí permitió recuperar las fuentes públicas sin cookies. Se mantienen `--skip-download --write-subs --write-auto-subs --sub-langs es.* --sub-format vtt/best --no-overwrites --ignore-errors`. No se descarga audio ni vídeo. Los fallos de red se distinguen de los vídeos sin subtítulos.

`fuentes/` conserva los VTT es-orig y es tal como se descargaron y su inventario SHA-256. `fuentes/verificaciones_subtitulos.json` guarda las comprobaciones explícitas de los tres vídeos sin subtítulos. `derivados/NNN/lectura.md` y `segmentos.jsonl` son lecturas automáticas del original, sin resumen ni identificación automática de hablantes.

Ejecutar desde la raíz `.venv/Scripts/python.exe scripts/importar_kuroto.py --descargar` permite reanudar sin sobrescribir fuentes existentes. `--capitulo N` limita la petición. `--preparar` registra y comprueba originales aportados y regenera las lecturas. No se abren sesiones personales del navegador.

## Lectura editorial

El capítulo 1 está leído de principio a fin, con cinco etapas narrativas y 24 afirmaciones con cita literal validada dentro de su intervalo. Seis personajes, tres lugares y un objeto tienen su propio relato; sus nombres dudosos permanecen señalados. No se ha confirmado una ficha de facción. Dos preguntas quedan abiertas y requieren cotejar sesiones posteriores.

Las fichas JSON viven en `conocimiento/capitulos/` y `conocimiento/entidades.json`; sus exportaciones Markdown se enlazan desde [el índice](conocimiento/INDICE.md). **El siguiente capítulo a revisar es el 2.** El material recuperado de las demás sesiones todavía no se presenta como canon revisado.

`python scripts/construir_interfaz.py` valida las fuentes, exporta las fichas y genera ambos HTML y `transcripciones/kuroto/*.js`. Esos archivos se abren por sesión, para evitar cargar cientos de transcripciones al entrar. Para usar el HTML local hay que conservar a su lado la carpeta `transcripciones`; los paquetes ZIP la incluyen. GitHub Pages la publica automáticamente.
