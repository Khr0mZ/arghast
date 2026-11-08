# Xoltacan · Campaña de Arghast

El catálogo activo está en `catalogo.json`. La campaña comparte la [estructura común](../README.md) con Kuroto:

- `config/`: nombres, entidades, historias, seguimiento de preguntas y fechas de emisión.
- `fuentes/`: VTT, TXT y metadatos originales, sin alterar sus bytes. `descarga_inicial/` conserva el material de la descarga original y `paquetes_originales/` los ZIP aportados al principio.
- `revision/`: procedencia por capítulo, revisiones editoriales y `borradores/` con las lecturas completas y sus entregas.
- `conocimiento/`: fichas JSON, lecturas Markdown y escenas originales del rol escrito.
- `derivados/`: inventario de originales, segmentos y lecturas regenerables.
- `web/`: estilos, ilustraciones, rótulos y licencias de Xoltacan.
- `publico/`: lector independiente, datos, transcripciones y rol con sus adjuntos.

Desde la raíz del proyecto, `python scripts/construir.py` reconstruye Xoltacan y la web de Arghast. `python scripts/auditar.py --exigir-completo --comparar-zip` verifica cobertura, citas y conservación de los originales. `scripts/incorporar.py` registra nuevos episodios en el catálogo activo; recuperar subtítulos sigue sin equivaler a revisar una sesión.

Abrir [publico/index.html](publico/index.html) para consultar Xoltacan. Esa carpeta se puede copiar completa y usar sin conexión. El visor común `arghast.html` y la entrada compatible `xoltacan.html` siguen disponibles en la raíz. Las rutas y los identificadores de la web se mantienen.
