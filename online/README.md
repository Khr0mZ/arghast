# Servicio de edición online

La web conserva https://khr0mz.github.io/arghast/. En ese dominio, el editor utiliza
https://arghast-editor.ivan-osorio440384.chatgpt.site/api/editor. En localhost sigue
utilizando el servidor Python del mismo origen. No hay cuentas para los jugadores
ni botones de activación nuevos.

El servicio se aloja en Sites y utiliza su binding R2 `BUCKET`. No necesita procesos
locales, una base de datos externa ni un plan de alojamiento contratado aparte.
El secreto de ejecución `ARGHAST_EDIT_CODE` se configura mediante Sites, fuera del
repositorio. No incluir credenciales de publicación o secretos en los artefactos.

`worker.mjs` conserva el contrato de la API local. `modelo.mjs` valida el contenido
editorial y las asociaciones con las transcripciones. El constructor incorpora
solo los números originales de capítulos; no copia transcripciones, narraciones,
SQLite local ni fuentes al paquete del servicio. Hasta el primer guardado, el
cliente utiliza el contenido editorial publicado en su HTML.

Cada guardado crea una versión completa comprimida y actualiza el puntero de la
campaña mediante una escritura condicional por ETag. Dos jugadores que guardan
desde la misma revisión no pueden sobrescribirse. El historial y las sesiones
se conservan en almacenamiento remoto y sobreviven a nuevas instancias del Worker.
Las transcripciones continúan sirviéndose desde GitHub Pages y nunca se aceptan
como parte del documento editable. CORS permite la web publicada y el propio
servicio; todas las escrituras requieren un código validado en el servidor.

Para preparar una actualización, abrir el proyecto de `hosting.json` mediante la
guía Sites y su helper de fuentes. En un checkout del starter Worker ESM:

```powershell
python scripts/preparar_editor_online.py RUTA_DEL_CHECKOUT
node scripts/probar_editor_online.mjs
```

La prueba utiliza por defecto `.pruebas/editor-online`; ejecuta el Worker con un
almacén de objetos en memoria y ambos documentos reales. No escribe en producción.
Construir y validar con los scripts del starter, sincronizar, empaquetar y desplegar
mediante las herramientas Sites. En Windows usar Git Bash en PATH y
`$env:TAR_OPTIONS = '--force-local'` para que tar acepte las rutas `C:/...`.

Las versiones guardadas quedan separadas de los HTML base. Si se añaden sesiones
a estos últimos, reconciliar primero los cambios con las campañas editadas, igual
que con el servicio local. Para una copia de seguridad se puede descargar cada
versión mediante `/api/editor/document/CAMPANA?revision=REVISION`; la respuesta
incluye el contenido completo y el historial hasta esa versión.
