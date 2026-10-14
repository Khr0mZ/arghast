# Revisión editorial de los capítulos 01–19

Se revisó la prosa editorial para utilizar un español neutro, completo y gramatical. Las citas literales de las transcripciones se conservan, aunque contengan errores del reconocimiento de voz o una forma particular de hablar. La voz de los personajes no se imita en las explicaciones de la enciclopedia.

## Alcance y resultado

Los capítulos 01–07 ya tenían afirmaciones redactadas en oraciones completas; se conservaron y se ajustaron únicamente algunos metadatos. Se corrigieron **299 afirmaciones** de los capítulos 08–19, principalmente por omisión de artículos y preposiciones, concordancia y sintaxis. En el capítulo 01 se retiraron la pregunta y la frase del resumen sobre el acceso de Madame Oghma a la información, conforme a la petición de consultar una enciclopedia global.

| Capítulo | Afirmaciones con cambios editoriales |
|---|---:|
| 01–07 | 0 |
| 08 | 20 |
| 09 | 33 |
| 10 | 27 |
| 11 | 32 |
| 12 | 32 |
| 13 | 26 |
| 14 | 25 |
| 15 | 22 |
| 16 | 21 |
| 17 | 23 |
| 18 | 21 |
| 19 | 17 |
| **Total** | **299** |

Se ajustaron también resúmenes y listas de los capítulos 01–08 y 17–19. El agente principal corrigió los resúmenes y las listas 09–16 para evitar ediciones simultáneas. La receta final recoge los valores actuales de los 19 capítulos, incluidos esos cambios.

## Ejemplos

- **10-024:** «Elfo, dragón y Ayoto siguen huyendo» pasa a «El elfo, el dragón y Ayoto siguen huyendo».
- **11-023:** «mientras él invisible» pasa a «mientras él es invisible».
- **16-019:** la acusación de Ayoto se presenta como una afirmación suya, seguida de la negativa de la mujer y de la ausencia de confirmación del director. No se convierte el parecido de una representación gráfica en una identidad o una resurrección.
- **18-009:** «Mamá intenta curar Patata» pasa a «Mamá intenta curar a Patata». Se conserva que el intento le causa dolor y que Mamá pierde algunas arrugas; no se interpreta como una curación exitosa.
- **19-007:** se expresa por separado que Mamá intenta curar, que Leona siente dolor y que Blink observa el rejuvenecimiento. Se mantiene la limitación de que Blink desconoce la causa.

## Validación

Se compararon los 19 archivos de capítulos con una instantánea anterior al cambio. Todos los campos protegidos permanecen idénticos: IDs, tipos, citas, evidencia, tiempos, entidades, conocedores, confianza y hashes de las fuentes. No se añadieron ni eliminaron registros.

En los 18 borradores existentes también permanecen idénticas las columnas protegidas: tiempos, clasificación, entidades, anclas, conocedores y estado del conocimiento. Los cambios de prosa se sincronizaron con los borradores para conservar la reproducibilidad.

Esta comprobación demuestra la conservación estructural de la evidencia. La conservación del significado se revisó mediante lectura de la prosa y, cuando surgió una ambigüedad durante la corrección, consulta de la transcripción: por ejemplo, el camarote modificado de Nox en 09-001. No sustituye una auditoría del audio original.

## Registro de trabajo

Los cambios revisados y la instantánea se encuentran en `derivados/revision_estilo_01_19/`. Las sustituciones son literales y se seleccionaron después de leer los registros; no constituyen una normalización automática de la voz de los personajes.

`scripts/revisar_estilo_01_19.py` conserva el primer pase histórico y está deshabilitado para impedir que restaure una instantánea antigua. La receta final compatible con `scripts/aplicar_estilo.py` es `config/revision_estilo_01_19_final.json`: recoge metadatos y campos editoriales por ID, sin evidencia, tiempos o entidades. No se volvió a aplicar innecesariamente al exportarla. La incorporación habitual de episodios debe seguir los scripts de mantenimiento del proyecto y las revisiones de los borradores actuales.
