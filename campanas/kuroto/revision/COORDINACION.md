# Coordinación de la revisión paralela

El usuario ha pedido expresamente un enjambre y ha prohibido publicar sin su revisión y aprobación. No hacer git push, desplegar ni activar Pages. Todos los resultados actuales son locales.

## Reparto exclusivo

- `/root/kuroto_004_062`: 004–048. Conserva `lote_004_062.json`.
- `/root/kuroto_063_122`: 063–122, saltando 92 e incluyendo 96 local. Conserva `lote_063_122.json` y añade `lote_116_122.json`.
- `/root/kuroto_123_182`: 123–165, incluyendo 135/136 locales. Conserva `lote_123_182.json`.
- Coordinador `/root`: 049–062 y 166–182, además de integración. Lotes separados `lote_049_062.json`, `lote_166_168.json` y `lote_169_182.json`.

El coordinador se suma como cuarto lector para acelerar el trabajo. El reparto se ha ajustado por carga restante después de completar 049–057, porque la integración consume parte de su tiempo. Ningún lector había empezado los rangos reasignados. No se resume por muestreo. Cada lector debe leer íntegramente sus fuentes antes de marcar una ficha revisada y mantener sus lotes incrementalmente.

## Fuentes adicionales recuperadas

Los audios de96/135/136 se descargaron en `.pruebas/audio_kuroto/` y se transcribieron íntegramente con faster-whisper1.2.1, modelo turbo, GPU. Hay VTT `.es-local.vtt`, procedencia, hash del audio y parámetros en `fuentes/transcripciones_locales.json`. `importar_kuroto.py --preparar` ya registró los359 VTT y sus derivados. Son181 sesiones con fuente, no181 sesiones revisadas.

El92 no figura tampoco en los507 vídeos del catálogo público del canal consultado. No usar el92 de La Guerra de Brunami, que es otra campaña.

## Integración

`scripts/integrar_kuroto.py --integrar` parte de `base_003.json`, valida los lotes, sus fuentes, citas, relatos, horizontes y entidades, y reconstruye `conocimiento/entidades.json`, `seguimiento.json` e `integracion.json`.

El constructor solo muestra como revisadas las fichas incluidas en `integracion.json`, de modo que escribir un JSON durante el trabajo de un lector no lo incorpora prematuramente a la interfaz. Los cambios de identidad se documentan en `identidades_confirmadas.json` y `IDENTIDADES.md`.

Sir/Sirt/Sirth se ha conciliado como el mismo clérigo de la muerte por contraste de ambos lectores. Es distinto de Shiru (cervan, herrero y panadero). El artífice negociador de Liber se ha identificado como Guxi y el drow bardo como Gelbreak, por continuidad contrastada entre los lectores. Véase `IDENTIDADES.md`.

`scripts/construir_interfaz.py` actualiza vistas, exporta fichas y genera `arghast.html`, `xoltacan.html`, `kuroto.html` y transcripciones por sesión. `vistas_kuroto.py` mantiene estadísticas, método y `REVISION.md` a partir de lo efectivamente integrado.

## Continuación del coordinador

1. Mantener lectores trabajando hasta completar sus rangos; si terminan un turno con su bloque incompleto, reactivarlos con `followup_task` para continuar desde el primer no revisado, sin repetir lecturas hechas.
2. Integrar periódicamente; los errores de cobertura o de referencias se devuelven al dueño del lote. No suplirlos con contenido inventado.
3. Cotejar propuestas de alias y respuestas entre bloques. Especial atención a universidad/nekomata, estatua, promesas de reparación, tratamientos de sangre, esferas, deudas y pactos.
4. Al cerrar los bloques, pulir historias por arcos coherentes y redactar una visión conjunta de las relaciones y tramas, apoyada por las evidencias entregadas.
5. Ejecutar pruebas de datos e interfaz local y regenerar paquetes. Entregar la versión local para revisión; no publicar sin confirmación expresa.

## Cierre de la lectura

Los cuatro lectores han completado las 181 transcripciones disponibles. Las fichas de capítulo reúnen 122.417 palabras de relato y 2.092 evidencias; el integrador valida las citas contra los originales. El capítulo 92 sigue ausente de las fuentes, sin renumerar el resto.

Los cotejos finales se conservan por responsable en `cotejos_*.json`. Una entrada puede estar auditada hasta el epílogo y seguir pendiente: `requiere_actualizacion=false` expresa que no quedan sesiones de este catálogo por cotejar, no que la pregunta tenga una respuesta definitiva. El integrador prioriza el cotejo de mayor alcance y no modifica las historias de capítulos anteriores con revelaciones futuras.

`arcos_relaciones.json` reúne nueve síntesis narrativas de vínculos, con sus evidencias, antes de las escenas por sesión. Las historias de las fichas conservan las etapas y las fuentes de cada bloque.
