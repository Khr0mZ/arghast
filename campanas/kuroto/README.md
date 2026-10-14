# Kuroto · Campaña de Arghast

[Lista oficial de Lichpol](https://www.youtube.com/playlist?list=PLelQK3I2Q5zymJZ2e2SNmwxsnnFGjBCYb).

El catálogo consultado el 14 de octubre de 2026 contiene 181 vídeos. Sus títulos numeran las sesiones hasta el 182; el 92 no está localizado en esta lista. Los capítulos 169 y 170 se ordenan por su número publicado, conservando también el título original.

`catalogo.json` conserva vídeos, números, títulos, enlaces, duraciones disponibles y la ausencia del 92. `fuentes/lista_reproduccion.json` conserva la instantánea obtenida de YouTube. No se atribuyen acciones a personajes ni se generan resúmenes a partir de esos metadatos.

La descarga del primer capítulo ha fallado con HTTP 429 y una solicitud de autenticación, tanto sin entorno JavaScript como con Node.js. El estado está en `fuentes/estado_descarga.json`. Por ahora hay cero VTT recuperados y cero sesiones revisadas. Esto es un bloqueo de acceso, no una comprobación de que falten subtítulos.

El archivo es independiente del de Xoltacan. Al recuperar fuentes:

1. Conservar los VTT originales como `fuentes/001 - KkZZR81onIw.es-orig.vtt` o la variante disponible, usando el número y el ID del catálogo.
2. Ejecutar `python scripts/importar_kuroto.py --preparar` desde la raíz. El importador registra hashes y genera segmentos y lecturas; no resume.
3. Leer las sesiones y redactar fichas en `conocimiento/capitulos/001.json`, con resumen, estado de revisión, SHA-256 y afirmaciones citadas según el esquema existente. Registrar las identidades revisadas en `conocimiento/entidades.json` y añadir sus relatos editoriales.
4. Regenerar la interfaz con `python scripts/construir_interfaz.py`. El constructor valida las fuentes y mantiene aisladas las evidencias de esta campaña.

Para volver a intentar la descarga pública: `.venv/Scripts/python.exe scripts/importar_kuroto.py --descargar --capitulo 1`. Las cookies, si el usuario aporta una exportación expresamente, deben guardarse fuera del repositorio y pasarse mediante `--cookies`; el importador no abre ni exporta sesiones personales.
