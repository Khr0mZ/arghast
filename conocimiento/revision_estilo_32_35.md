# Revisión del estilo editorial: capítulos 32–35

Se leyeron y reescribieron los resúmenes, las cinco listas editoriales y las 80 afirmaciones de los capítulos 32–35. También se corrigieron las limitaciones que contenían elipsis gramaticales.

Se aplicaron las recetas `borradores/estilo32_35.json` y `borradores/estilo34_35.json` con `scripts/aplicar_estilo.py`. Las fichas y sus borradores están sincronizados.

La aplicación comprueba que permanecen idénticos los IDs, tipos, citas, evidencia VTT, tiempos, entidades, conocedores, estados de conocimiento y confianza. No se cambian las fuentes ni sus SHA. Una comprobación adicional verificó la igualdad de los campos entre fichas y borradores, incluyendo los capítulos 20–29 revisados por este agente: 284 afirmaciones en total.

Ejemplos:

- «Bonnie exige a recién llegadas obediencia y revisión de acciones» pasa a «Bonnie exige obediencia a las recién llegadas y supervisar sus acciones».
- «Mamá toca cuello Winscore, roba dieciocho puntos de vida» pasa a «Mamá toca el cuello de Winscore y le roba dieciocho puntos de vida».
- «Nox sigue pensando visión y culpa» pasa a «Nox sigue pensando en la visión y su culpa».

Se mantienen las diferencias entre testimonios, hechos, interpretaciones, bromas y reglas de la mesa. Las citas no se reescriben.
