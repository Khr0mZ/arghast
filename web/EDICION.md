# Correcciones de jugadores

La edición compartida utiliza un código, sin cuentas ni aprobación editorial previa. Quien conoce el código puede editar cualquier capítulo o ficha de ambas campañas. El nombre que escribe sirve para atribuir el cambio; no verifica su identidad ni su asistencia a una sesión.

## Revisión local

Desde la raíz del proyecto:

```powershell
python -X utf8 scripts/construir_interfaz.py
$env:ARGHAST_EDIT_CODE = 'showmethemoney'
python -X utf8 scripts/servidor_edicion.py
```

Abrir http://127.0.0.1:8765/ y elegir campaña. Teclear `showmethemoney` fuera de un campo activa la edición con ese código. No hay botón de activación ni formulario para introducirlo. El servicio debe tener configurado ese mismo código. «Salir de edición» solo aparece después de activar el modo y lo cierra.

Tras activar la edición, cada tarjeta de entidad tiene su propio botón «Editar», separado del enlace que abre la ficha. La ficha también lo muestra junto al nombre. Personajes, lugares, facciones y vestigios funcionan igual en ambas campañas. Los capítulos, acontecimientos, preguntas y documentos tienen el mismo acceso junto a su título. Al pulsarlo, los datos se editan directamente sobre el contenido: nombre en su título, descripción en su párrafo e historia en cada etapa, con sus fuentes y controles de orden. Los datos que no se muestran habitualmente aparecen junto a la misma entidad. Todos están disponibles a la vez; no hay diálogo, selector de campo ni editor JSON. Una tarjeta se expande dentro del catálogo para poder editar su historia completa sin navegar a otra página.

«Guardar cambios» y «Cancelar» están en la propia entidad, arriba y al pie. Cancelar restaura la vista anterior sin escribir en el archivo compartido. Guardar exige nombre y motivo y conserva el conjunto de cambios. Los enlaces de navegación y la búsqueda se suspenden mientras hay una edición abierta para evitar perder el borrador; las actualizaciones de otros jugadores no lo sustituyen. Solo se edita una entrada a la vez. Los capítulos, registros, preguntas y documentos utilizan el mismo funcionamiento sobre su contenido. Las listas y etapas tienen controles para añadir, quitar, subir y bajar elementos. Los documentos Misiones y Relaciones conservan su contenido de texto.

Los botones de arriba y abajo tienen exactamente la misma función. «Eliminar entrada» abre un diálogo de advertencia con el nombre y el alcance de la eliminación; Cancelar o Escape cierra el aviso sin marcarla. Confirmar la marca y cambia ambos botones de guardar a «Guardar eliminación». La entrada solo desaparece cuando se guarda. Antes de ese paso se puede pulsar «Deshacer eliminación» o cancelar toda la edición. La edición de contenido continúa en la página; el único diálogo se usa para advertir de una eliminación.

Los tipos de ficha, estados y sesiones se eligen en desplegables con nombres comprensibles. Las referencias se buscan por título o sesión y las entidades por su nombre; se añaden desde la selección, sin copiar identificadores. «Añadir información» permite incorporar un apartado existente que falte o crear uno nuevo: texto, lista, grupo de campos, número o casilla de sí o no. Los grupos permiten añadir, renombrar y quitar sus campos. La información nueva se muestra en la ficha y queda incluida en las versiones guardadas.

«Crear otra entrada» inicia una entrada del mismo tipo en la página, y el historial permite cargar versiones anteriores de la entrada que se está editando. Eliminar un capítulo elimina también sus acontecimientos y misterios; se limpian las referencias a los registros retirados. Las versiones completas de campaña siguen conservadas en la base de datos. Cambiar el nombre de una ficha actualiza las menciones estructuradas y conserva el nombre anterior como alias; cambiar el identificador de un registro actualiza sus referencias. Cambiar el número de capítulo actualiza sus registros y misterios, manteniendo la asociación con su transcripción original.

La única fuente que permanece bloqueada es la transcripción: sus segmentos, texto y archivos no entran en el documento editable. Corregir una cita modifica la cita editorial de la ficha, manteniendo íntegra la transcripción que permite cotejarla. Se conservan también los archivos originales y sus hashes. Los índices y cifras derivados se recalculan; las validaciones impiden guardar referencias rotas, identificadores duplicados o una estructura que el lector no pueda mostrar.

El historial permite cargar una versión anterior de la entrada y guardarla como una corrección nueva. Si dos jugadores parten de la misma versión de una campaña, el segundo guardado se rechaza para que comparen sus cambios, incluso si afectaban a campos diferentes. El borrador permanece en la página para copiarlo antes de recargar. Las correcciones anteriores de texto se incorporan a la nueva edición sin borrar su historial.

Los lectores obtienen las correcciones sin código al abrir la página y cada 30 segundos mientras la pestaña esté visible. La edición caduca a las ocho horas o al salir; recargar o cambiar de campaña requiere introducir el código de nuevo. El código se valida en el servidor, nunca se autoriza un guardado solo porque aparezca el editor.

Las correcciones y su historial se guardan en `.local/edicion/correcciones.sqlite3`, fuera de Git y separadas de los originales. Copiar ese archivo con el servidor detenido para hacer una copia de seguridad. Reiniciar el servidor no pierde correcciones. La primera corrección completa guarda una versión del archivo de campaña; las posteriores parten de esa versión. Si se incorporan nuevas sesiones al HTML base, hay que reconciliarlas con el archivo editado antes de sustituir la base publicada, para no ocultarlas bajo una versión anterior. Esta edición es del contenido de las campañas, no del código, los estilos o las ilustraciones de la web.

## Alcance de esta versión

El servidor escucha solo en este equipo. El HTML abierto con doble clic continúa permitiendo consultar el archivo, pero no guardar correcciones compartidas. La versión de GitHub Pages por sí sola tampoco puede guardarlas: para uso entre jugadores es necesario alojar el servicio con almacenamiento persistente y HTTPS y servir el archivo desde el mismo origen. Esta versión no publica ni configura servicios externos. El código de ejemplo es conocido y debe cambiarse en el servicio si se quiere restringir quién puede editar.

Pruebas:

```powershell
python -X utf8 scripts/test_edicion.py
node scripts/probar_edicion.mjs
node scripts/probar_interfaz.mjs
```
