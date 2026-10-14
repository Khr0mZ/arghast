# Revisión del estilo de los documentos generales

Se han leído y revisado por completo estos nueve documentos:

- `continuidad_16_17.md`
- `continuidad_18_24.md`
- `continuidad_25_31.md`
- `continuidad_32_39.md`
- `MISTERIOS.md`
- `RELACIONES.md`
- `ATLAS.md`
- `FACCIONES.md`
- `TRAMAS.md`

La prosa editorial utiliza ahora español neutro, frases completas y atribuciones explícitas. Se han separado las palabras y los números de los capítulos, añadido artículos y preposiciones, y sustituido las abreviaturas y las instrucciones internas por explicaciones para el lector. No se imita la voz de ningún personaje. Las citas literales, las referencias a registros y los enlaces de fuentes se conservan.

Ejemplos:

- «Naór leonina hija de Camar Taruan nombra reino Atlat en20» pasa a «Naór es la hija leonina de Camar Taruan. En el capítulo 20 llama Atlat a su reino».
- «Dos plantas matan Margaret/Marga, trabajadora de Liz» pasa a «Dos plantas matan a Margaret/Marga, trabajadora de Liz».
- «Curación hiere Patata18/Leona19 y ella pierde arrugas» pasa a una descripción con sujetos y acciones explícitos, sin presentar una hipótesis causal como un hecho.

Se mantiene la distinción entre lo observado, los testimonios, las visiones y las hipótesis. Coyote y Citlali, Naór y Nox, y las diferentes monturas Merlucilla siguen separados. Las dos entradas de Iktan en el atlas se han reunido en una sola, conservando los intentos de viaje y las llegadas documentadas. Se han retirado las notas repetidas sobre el acceso de Oghma de los documentos históricos para que la consulta siga siendo enciclopédica.


## Capítulos 36–39

También se han leído y revisado todos los campos editoriales de los capítulos 36, 37, 38 y 39: los cuatro resúmenes, las listas de misiones, preguntas y notas, y 75 registros con sus títulos, afirmaciones y limitaciones. La receta reproducible es `config/revision_estilo_36_39.json`.

La aplicación mediante `scripts/aplicar_estilo.py` ha preservado los campos de evidencia y sincronizado los borradores. No se han modificado citas, tiempos, identidades de registros, tipos de evidencia ni huellas de las fuentes. Las fichas Markdown y el HTML deben regenerarse con el constructor después de integrar todas las revisiones.

Ejemplo: «Ione vuelve humana, cubierta con saco. Venda herida Ilikar» pasa a «Ione vuelve a ser humana y se cubre con un saco. Venda la herida de Ilikar».
