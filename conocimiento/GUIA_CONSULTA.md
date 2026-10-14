# Consultar la biblioteca

El índice general enlaza capítulos, cronología, entidades, relaciones, misiones, preguntas y contradicciones. La consulta abarca toda la enciclopedia sin filtro de conocimiento de Oghma. Las fichas de entidades agrupan toda su evolución registrada sin fusionar automáticamente grafías parecidas.

## Pregunta verificable

Para responder una consulta, buscar primero fichas revisadas. Citar identificador de registro, capítulo y minuto; abrir VTT si una precisión no está en la ficha. Distinguir acción adjudicada, declaración escuchada y teoría. Si no existe evidencia, decir «no consta en las fuentes revisadas», sin rellenar el vacío.

Ejemplo de instrucciones para un chat que tenga estos archivos:

> Usa esta enciclopedia de Aventuras en Xoltacan. Responde objetivamente, con capítulo, minuto e identificador de evidencia. Conserva contradicciones y fechas de revelación. No conviertas declaraciones de personajes o especulaciones en hechos. Consulta toda la información documentada de Xoltacan, sin restringirla al conocimiento de un personaje.

## Búsqueda local

Desde raíz del proyecto:

```powershell
python -X utf8 scripts/consultar.py "Tutucan"
python -X utf8 scripts/consultar.py "collar" --capitulo 9
python -X utf8 scripts/consultar.py "casino" --personaje Axi
python -X utf8 scripts/consultar.py "Jivirix"
python -X utf8 scripts/consultar.py "Marina" --tipo declaracion_personaje --json
```

Todos los términos de consulta deben aparecer en un mismo registro. Se ignoran mayúsculas y acentos, y se incluyen las equivalencias editoriales documentadas en `config/entidades.json`. No se infieren alias por semejanza. Si no hay resultados, probar grafías de nombres dudosos o buscar en VTT con `rg`.

`--personaje` permite localizar escenas con destinatarios/testigos explícitos del campo `conocedores`; es opcional y parcial. Una lista vacía no acredita ignorancia. La consulta normal incluye todos los registros, también escenas privadas o privilegiadas de espectadores. Una declaración escuchada sigue sin demostrar su contenido.

## Transportar y mantener

Los archivos locales no son memoria automática de otros chats. Aportar índice y fichas pertinentes o el paquete de biblioteca en el contexto donde se consultarán. Mantener originales y fuentes con citas para poder comprobar respuestas.

La incorporación de nuevos episodios prepara transcripciones e inventario automáticamente. La revisión interpretativa sigue siendo necesaria: una descarga nueva no puede aparecer como capítulo revisado sin lectura. Después ejecutar `construir.py`; las vistas y búsquedas incluirán la ficha nueva.

```powershell
python -X utf8 scripts/construir.py
python -X utf8 scripts/auditar.py --exigir-completo --comparar-zip
```

La auditoría valida citas y hashes; no sustituye la revisión semántica ni el cotejo de audio para un nombre dudoso.
