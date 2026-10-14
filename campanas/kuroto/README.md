# Kuroto · Campaña de Arghast

**Estado de Kuroto:** 181 vídeos catalogados; 181 transcripciones (178 de YouTube y 3 locales). 181 sesiones con relato revisado, 2092 evidencias y 1257 fichas con historia. Revisión continua hasta el capítulo 182; 0 sesiones pendientes. La lectura de los bloques está completada; la versión permanece en local para revisión, sin publicación autorizada.

## Revisión local

Abrir `kuroto.html` desde la raíz del proyecto para entrar directamente en Kuroto. Abrir `arghast.html` para elegir campaña. Conservar la carpeta `transcripciones` junto a los HTML para consultar los subtítulos sin servidor. Los capítulos y las fichas usan la misma presentación narrativa de Xoltacan.

No publicar, desplegar ni subir cambios sin que el usuario confirme que ha revisado y aprobado esta versión. La autorización de despliegues anteriores no se reutiliza. La configuración local de Pages solo admite ejecución manual.

## Estructura y contenido

- `catalogo.json`: 181 vídeos de la [lista oficial](https://www.youtube.com/playlist?list=PLelQK3I2Q5zymJZ2e2SNmwxsnnFGjBCYb). Se conserva la numeración hasta el 182 y la ausencia del 92; se ordenan correctamente el 169 y el 170.
- `fuentes/`: originales VTT es-orig y es conservados sin alteraciones, inventario SHA-256, incidencias y verificaciones de idiomas. Se recuperaron los subtítulos de 178 vídeos con el descargador de Xoltacan. Los capítulos 96, 135 y 136, sin subtítulos de YouTube, se transcribieron localmente a partir del audio; su procedencia figura en `transcripciones_locales.json`.
- `derivados/NNN/lectura.md` y `segmentos.jsonl`: lecturas de los subtítulos, sin inventar resúmenes ni identificar hablantes automáticamente.
- `conocimiento/capitulos/`: fichas JSON revisadas y sus relatos Markdown; cada afirmación tiene intervalo, cita literal, tipo y entidades.
- `conocimiento/entidades.json` y `conocimiento/entidades/`: identidades y relatos de personajes, lugares, facciones y objetos, con evidencia y alcance de revisión.
- `conocimiento/SEGUIMIENTO.md` y `seguimiento.json`: preguntas de origen, respuestas posteriores, referencias y asuntos pendientes.
- `conocimiento/MISIONES.md`, `RELACIONES.md`, `ATLAS.md`, `FACCIONES.md`, `MISTERIOS.md` y `METODO.md`: vistas de consulta de la misma crónica.
- [Índice de lectura](conocimiento/INDICE.md).

Las historias conservan los acontecimientos de cada sesión y las fichas reúnen su evolución posterior. El seguimiento distingue las preguntas resueltas de las tramas que siguen abiertas al terminar el epílogo. Cada cierre enlaza las evidencias que lo justifican.

## Continuación

**Lectura completada de las 181 sesiones disponibles.** Consultar [REVISION.md](REVISION.md) para el catálogo y la procedencia de cada sesión.

`python scripts/construir_interfaz.py` valida fuentes e historias, exporta Markdown y regenera los tres HTML y los archivos por sesión en `transcripciones/kuroto/`. `python -m unittest discover -s scripts -p 'test_*.py'` comprueba los constructores. La verificación en navegador es local: `node scripts/probar_interfaz.mjs`.
