# Auditoría de cierre del catálogo 1–39

Resultado de `python -X utf8 scripts/auditar.py --exigir-completo --comparar-zip`:

- 39 capítulos catalogados, 39 revisados y ninguno pendiente.
- 946 registros con citas localizadas en el intervalo del VTT original y fuente SHA-256 correspondiente.
- 156 originales íntegros; los 156 coinciden byte a byte con el ZIP de descarga inicial.
- Identificadores únicos y referencias editoriales existentes, incluidas las de documentos de continuidad, atlas y misterios.
- Enlaces locales de la enciclopedia y README comprobados.
- Veinte pruebas aprobadas: seis de limpieza/normalización/localización, cuatro de búsqueda, cinco de catálogo y cinco de seguimiento de preguntas. Se comprueban identidades distintas, variantes unificadas, clasificación de objetos, referencias, cierres respaldados y actualización tras incorporar episodios.

## Revisión editorial y de la interfaz

Se revisó la prosa editorial de los 39 capítulos y de los documentos generales para corregir artículos, preposiciones, concordancias y frases telegráficas. Las citas y los campos de evidencia se conservaron. Las fichas compactas de trabajo están sincronizadas con los capítulos, y las recetas de revisión permiten aplicar los cambios por identificador sin tocar citas, tiempos o fuentes.

El catálogo público contiene 137 identidades revisadas, clasificadas como personajes, lugares, facciones u objetos. Las variantes confirmadas comparten una ficha y sus apariciones se deduplican. Naór y Nox, Citlali y Coyote, Eldrat y Erendriel y las cinco monturas de Poncelot permanecen separados. El reconocimiento del capítulo 33 permite vincular a los tripulantes buscados Mingo, Mango y el tercero con el trío de hipopótamos Mingo, Mango y Mungo. Los casos pendientes de identificación no se fusionan por semejanza.

La interfaz integra las cautelas editoriales en las notas de cada capítulo y elimina la categoría principal de contradicciones. Las citas llevan la etiqueta de texto literal. Se aprobaron 52 comprobaciones en Edge desde el archivo local, incluidas búsquedas, filtros, equivalencias, transcripciones, fuentes, seguimiento individual de preguntas, navegación y visualización móvil. La navegación distingue Personajes, Lugares, Facciones y Objetos, sin un catálogo general duplicado; se comprueba que cada sección contenga solo su tipo y que las fichas regresen a su sección. Las capturas se inspeccionaron para comprobar la presentación.

## Seguimiento individual de preguntas

Se cotejaron las 228 preguntas históricas con los capítulos posteriores hasta el 39: 15 resueltas, 53 parciales y 160 pendientes. No queda ninguna pregunta sin revisar. Cada entrada conserva su texto original y un identificador estable; las respuestas enlazan registros con evidencias y minutos. Se exige una referencia posterior para marcar una pregunta como resuelta o parcial. Las pistas que no contestan ninguna parte se conservan con estado pendiente.

Las preguntas compuestas solo se cierran cuando se responde a todo lo preguntado. Los casos parciales indican qué se sabe y qué falta. La revisión es editorial: la validación automática comprueba cobertura, identidad textual, referencias y coherencia estructural, pero no certifica por sí sola la interpretación. Las recetas de los tres bloques se conservan en `config/seguimiento_preguntas_*.json`; el constructor produce [SEGUIMIENTO.md](SEGUIMIENTO.md), JSON y HTML. Incorporar capítulos marca los cotejos anteriores para actualización y las preguntas nuevas como sin revisar.

Distribución de registros: 715 acciones/resultados confirmados respecto a subtítulos, 170 declaraciones de personajes, 60 explicaciones de director y una especulación registrada como tal. Las hipótesis y límites de interpretación también se conservan en las notas de cada registro y preguntas de capítulo.

Los capítulos 18–24, 25–31 y 32–39 se leyeron en bloques paralelos autorizados; la integración conserva número de episodio, minuto y momento de revelación. Se contrastaron custodia de objetos, identidades, relaciones y resolución de preguntas antiguas.

Esta auditoría comprueba evidencia textual, integridad y cobertura declarada; no certifica fidelidad de reconocimiento de voz, interpretación perfecta ni cotejo audiovisual. Grafías y nombres que requieren audio siguen provisionales. No se inventan respuestas para las tramas abiertas al cierre de 39.

Para reproducir o ampliar:

```powershell
python -X utf8 scripts/construir.py
python -X utf8 scripts/seguimiento.py --exigir-completo
python -X utf8 -m unittest discover -s scripts -p "test_*.py" -v
node scripts/probar_interfaz.mjs
python -X utf8 scripts/auditar.py --exigir-completo --comparar-zip
python -X utf8 scripts/empaquetar.py
python -X utf8 scripts/empaquetar.py --solo-conocimiento
```

Los paquetes se generan después de esta comprobación. El empaquetador verifica nombres, CRC y bytes de todas las entradas frente a archivos locales antes de sustituir el ZIP anterior. Este informe corresponde al catálogo 1–39; tras añadir episodios, actualizar también informe, continuidad y estado de misterios.
