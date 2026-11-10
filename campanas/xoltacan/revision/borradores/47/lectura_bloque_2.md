# Lectura editorial completa: capítulo 47, bloque 2

Responsabilidad exclusiva: **00:45:29.000–01:34:05.709**, segmentos **c002057–c004113**; **1.028 segmentos**. Se han leído íntegros `bloque_2.md`, los 1.028 objetos de `bloque_2_segmentos.json` y las 95 preguntas completas de `preguntas_bloque_2.json`. No se ha cotejado audio.

Fuente conservada: `campanas/xoltacan/fuentes/47 - yvqhR20m7Zg.es-orig.vtt`.

SHA-256 comprobado: `af82762727aa32ebc82b92459bdc4b039b6b17839c0f994d26f0a5aaf88e983e`.

## Cobertura de las lecturas

Índices de segmentos basados en cero, extremos incluidos. Ninguna salida de los tramos contabilizados quedó truncada.

| Archivo | Tramos leídos completos |
|---|---|
| `bloque_2.md` | Líneas 1–522, 523–1.044, 1.045–1.566 y 1.567–2.055; segmentos 0–260, 261–521, 522–782 y 783–1.027 |
| `bloque_2_segmentos.json` | Objetos 0–259, 260–519, 520–779 y 780–1.027; se mostraron id, inicio, fin y texto original de cada objeto |
| `preguntas_bloque_2.json` | Objetos completos 0–19, 20–39, 40–59, 60–79 y 80–94, con pregunta, respuesta anterior, pendientes, estado, referencias y hash |

Los 1.028 `texto_normalizado` son idénticos a `texto_original`; se comprobó esa igualdad para todos y se indicó en cada salida compacta del JSON. También se verificó que el Markdown completo reproduce, en el mismo orden, los intervalos y textos originales de los 1.028 registros. Los identificadores saltan de c004007 a c004011 porque así los produce la eliminación de arrastres del parser; no falta un registro del bloque.

La primera lectura masiva de contexto/preguntas excedió el límite de salida y **no se contó como cobertura**. Fue sustituida por los cinco tramos íntegros señalados arriba. La comparación inicial construida desde una tubería de PowerShell tuvo un separador Unicode alterado; se repitió usando `\u2013` y dio igualdad íntegra. Ninguna escritura editorial utiliza esa tubería para texto español: el script y este registro se crearon mediante `apply_patch`, y el JSON se serializa como UTF-8.

Contexto consultado: `AGENTS.md`, `conocimiento/continuidad_46.md`, las fichas pertinentes de `config/entidades.json`, `revision/borradores/47/identidades_contexto.json`, el formato de `revision/borradores/46/entrega_2.json` y `validate_fact`/`parse_vtt` de `scripts/construir.py`.

## Escenas y material entregado

1. **00:45:29–00:54:45:** continuación de la expulsión de Patata, ataque y veneno de Mictlan, disparos de apoyo de Tesara, tentáculo y rayos de Tentacol, ataques fallidos contra el felino y avance desigual de los muertos.
2. **00:54:45–01:11:15:** intrusión compartida con dos elfos pálidos, remates de enemigos que se levantan, aclaración de sacar a los elfos de la ciudad, interpretación de rescate de Chopito, ataques a distancia y daño radiante.
3. **01:11:15–01:19:33:** recompensa prometida, caída de los últimos muertos, raíces que reúnen los cuerpos en una masa, amenaza, reconocimiento de la voz por Tesara y rama que rebota en la presencia invisible.
4. **01:19:33–01:30:27:** maldiciones y empujones contra la masa, Patata evita quedar envuelto aunque recibe daño, Mictlan dispara desde lejos, Tesara descubre que la presencia cambió de sitio, ofensiva final de Patata, cadáveres inertes y raíces que se retiran.
5. **01:30:27–01:34:05:** comprobación del estado de los compañeros, Tesara sigue escondida y detecta otro hueco enfrente, Tentacol corre a buscar a los elfos y Patata ofrece ayuda al felino y pregunta su nombre.

`entrega_2.json` contiene 30 afirmaciones **47-201–47-230**, cinco etapas continuas, ocho historias de entidad, cuatro misiones, cinco preguntas nuevas, cuatro relaciones y 95 cotejos individualizados de preguntas anteriores. Los hechos conservan intervalos y citas exactas; la petición de rescate se atribuye a Chopito, las promesas y amenazas a la voz y las reglas al director cuando corresponde.

No hay novedad directa que cierre los pendientes de las 95 preguntas asignadas. Cada una tiene su motivo específico y conserva su estado previo. La animación actual no demuestra una alianza entre el dragón, los sacerdotes y Hoja Caída de P30-005; las señales compartidas no identifican a todos los controladores de visiones anteriores. P15-006 requiere la corrección contextual de nombre Zarynth con su fuente externa: este dragón del bosque no se convierte en el compañero de Aerendriel.

## Identidades y continuidad para integrar

- **Mictlan**: nombre confirmado por el coordinador tras leer completa la escena escrita posterior `x-1531013198478708756`. Bloque 1 registra su presentación como «Mlan» y este bloque ofrece MD, Mlan, «mi clan» y Mic. Las citas mantienen el original; solo se normaliza la identidad. No se trasladan sucesos posteriores al capítulo.
- Se armonizan con bloque 1 **Ruinas de la orilla del lago de Iktan** y **Cadáveres movidos por raíces de las ruinas del lago**. La masa posterior es una etapa de la misma ficha colectiva.
- El director confirma que Tesara reconoce **la misma voz** de su experiencia anterior con los elfos. En este bloque no se pronuncia Clolgedranx; el coordinador integra el nombre y la relación de identidades mediante el contexto completo y el rol conservado.
- Los destinatarios de la orden son dos elfos pálidos que Tesara llama gemelos. No se pronuncian sus nombres en este tramo. El coordinador coteja su identificación con Eldrath y Tryel.
- El relato del disparo antiguo de Tesara termina aquí «le disparé al»; el blanco no se completa en el bloque.
- La presencia nunca se muestra directamente. Tesara sigue presiones y huecos de la vegetación, y distingue su movimiento mientras los demás ven los cuerpos. Destruir la masa no prueba la muerte del dragón o la extinción del encantamiento.
- El corte llega antes de resolver la ayuda de Patata, el estado final de Mictlan y la búsqueda que Tentacol acaba de iniciar. Deben integrarse con bloque 3.

Se excluyen como lore las bromas de posesión de Patata, los ruidos de cocina, el supuesto hackeo de Foundry, una bola de fuego que no se lanza, una red que no inmoviliza al dragón y una supuesta visión verdadera que el director no confirma. Se permite tirar para recargar tinta, pero el resultado no se anuncia aquí.

## Verificación local

El script `redactar_bloque_2.py` genera exclusivamente `entrega_2.json`. Ejecuta `validate_fact` para las 30 afirmaciones; comprueba hash, extremos, pertenencia a este intervalo, igualdad completa entre Markdown y registros, las 95 preguntas sin omisiones ni repeticiones y referencias internas de etapas/historias. Coteja además cada segmento leído y cada cue citado contra `parse_vtt` aplicado al original.

No se han modificado fuentes, archivos compartidos, campañas ajenas o índices de capítulos. No se ha publicado, desplegado, realizado commit ni push.
