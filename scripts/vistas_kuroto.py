"""Vistas de consulta de la prosa ya revisada; no extrae ni inventa canon."""
from collections import Counter
from construir import ROOT, write, write_json, read_json
from campanas import KUROTO


def refresh(data):
    chapters = data['chapters']
    reviewed = [chapter for chapter in chapters if chapter['estado'] == 'revisado']
    available = [chapter for chapter in chapters if chapter['transcripcion_disponible']]
    local = [chapter for chapter in available if chapter.get('fuente_transcripcion')]
    counts = Counter(entity['type'] for entity in data['entities'])
    progress = data.get('revision') or {}
    through = progress.get('revision_continua_hasta', max((chapter['capitulo'] for chapter in reviewed), default=0))
    complete = len(reviewed) == len(chapters)
    scope = (f'Las {len(chapters)} sesiones disponibles tienen relato revisado, con numeración hasta el capítulo 182. '
             'No se dispone del vídeo ni de la transcripción del capítulo 92.' if complete else
             f'{len(reviewed)} de {len(chapters)} sesiones con relato revisado. '
             f'Revisión continua desde el inicio hasta el capítulo {through}; '
             'los otros capítulos revisados pueden pertenecer a bloques posteriores. '
             f'{len(chapters)-len(reviewed)} sesiones pendientes de lectura editorial.')

    def document(key, title, filename, text):
        content = '# '+title+'\n\n'+scope+'\n\n'+text.strip()+'\n'
        write(KUROTO / 'conocimiento' / filename, content)
        data['documents'][key] = {'title': title, 'text': content}

    def references(ids):
        return ' · '.join(ids)

    for kind, key, title, filename in [('lugar','atlas','Lugares de Kuroto','ATLAS.md'),
                                        ('faccion','facciones','Facciones de Kuroto','FACCIONES.md')]:
        lines = ['Estas vistas reúnen la presentación y el último tramo de los relatos de las fichas. '
                 'Cada ficha conserva su historia completa y sus fuentes.', '']
        for entity in data['entities']:
            if entity['type'] != kind:
                continue
            stages = entity['history']['etapas']
            selected = [stages[0], stages[-1]] if len(stages)>1 else stages
            lines += ['## '+entity['name'], '', entity['description'], '']
            for stage in selected:
                lines += ['### '+stage['titulo'], '', stage['texto'], '', 'Fuentes: '+references(stage['referencias'])+'.', '']
            if entity['note']:
                lines += [entity['note'], '']
        document(key, title, filename, '\n'.join(lines))

    missions = []
    for chapter in reviewed:
        if not chapter['misiones']:
            continue
        missions += [f'## Capítulo {chapter["capitulo"]}: {chapter["titulo"]}', '']
        for mission in chapter['misiones']:
            missions += [mission, '']
        missions += ['Fuentes del capítulo: '+references(chapter['registros'])+'.', '']
    document('misiones','Misiones de Kuroto','MISIONES.md','\n'.join(missions))

    by_name = {entity['name']:entity for entity in data['entities']}
    relations = ['Las siguientes escenas describen interacciones documentadas entre personajes o facciones. '
                 'Compartir una escena no se convierte automáticamente en una alianza, parentesco o pertenencia permanente.', '']
    synthesis_path = KUROTO / 'revision/arcos_relaciones.json'
    if synthesis_path.exists():
        known = {fact['id'] for fact in data['facts']}
        for arc in read_json(synthesis_path):
            if not arc['referencias'] or not set(arc['referencias']) <= known:
                raise ValueError('Síntesis de relaciones sin evidencias integradas: ' + arc['titulo'])
            relations += ['## '+arc['titulo'], '', arc['texto'], '', 'Fuentes: '+references(arc['referencias'])+'.', '']
        relations += ['## Escenas documentadas por sesión', '']
    for chapter in reviewed:
        selected = [fact for fact in data['facts'] if fact['capitulo']==chapter['capitulo'] and
                    sum(by_name[name]['type'] in ('personaje','faccion') for name in fact['entidades'])>=2]
        if not selected:
            continue
        relations += [f'## Capítulo {chapter["capitulo"]}: {chapter["titulo"]}', '']
        for fact in selected:
            relations += ['### '+fact['titulo'], '', fact['afirmacion'], '', 'Fuente: '+fact['id']+'.', '']
    document('relaciones','Relaciones de Kuroto','RELACIONES.md','\n'.join(relations))

    mysteries = []
    labels={'resuelta':'Resuelta','parcial':'Parcial','pendiente':'Pendiente','sin_revisar':'Interpretación sin revisar'}
    for question in data['seguimiento']['preguntas']:
        mysteries += ['## '+question['pregunta'], '', labels[question['estado']]+f' · Revisión de esta entrada hasta el capítulo {question["revisado_hasta"]}.', '',
                      question['respuesta'], '', question.get('pendiente',''), '', 'Fuentes: '+references(question['referencias'])+'.', '']
    document('misterios','Preguntas y desenlaces de Kuroto','MISTERIOS.md','\n'.join(mysteries))

    names = ['Las variantes de búsqueda no equivalen por sí solas a una identidad confirmada. '
             'Las cautelas conservan la distinción entre nombres de personajes, jugadores y lecturas inciertas.', '']
    for entity in data['entities']:
        if entity['note'] or len(entity['aliases'])>1:
            names += ['## '+entity['name'], '', 'Variantes documentadas: '+', '.join(entity['aliases'])+'.', '', entity['note'], '']
    document('nombres','Nombres y cautelas de Kuroto','NOMBRES.md','\n'.join(names))

    method = f'''## Archivo y revisión

Kuroto y Xoltacan son campañas diferentes del mundo Arghast. Comparten interfaz y tipos de ficha, manteniendo separados capítulos, identidades y evidencias. La presencia de un nombre o lugar parecido no permite trasladar hechos entre ambas campañas sin contraste.

El catálogo de la lista oficial contiene {len(chapters)} vídeos numerados hasta el 182. El vídeo 92 no se ha localizado ni en la lista ni en los 507 vídeos del catálogo público del canal consultado el 14 de octubre de 2026. Un anuncio de Twitch documenta el directo del episodio 92 el 13 de marzo de 2025; no se dispone de su vídeo ni de su transcripción y no se marca como sesión revisada.

Hay {len(available)} transcripciones disponibles: {len(available)-len(local)} proceden de pistas de YouTube y {len(local)} se generaron localmente del audio con Whisper. Los capítulos 96, 135 y 136 no ofrecen subtítulos manuales ni automáticos en YouTube; su procedencia local se identifica en la lectura. Los VTT conservan hashes; las fuentes locales registran además modelo, parámetros y hash del audio.

La revisión contiene {len(data['facts'])} evidencias y {len(data['entities'])} fichas con historia: {counts['personaje']} personajes, {counts['lugar']} lugares, {counts['faccion']} facciones y {counts['objeto']} objetos. Los relatos se redactan después de leer las transcripciones completas; tener subtítulos no equivale a haber revisado una sesión.

## Relatos, citas y conocimiento

Cada etapa de un relato remite a evidencias. Las citas literales se validan dentro de sus intervalos de fuente. Los capítulos no toman revelaciones de sesiones posteriores para explicar lo que sus personajes sabían entonces. Las historias de entidades indican su propio alcance de revisión.

Las declaraciones conservan su atribución. Las teorías y las bromas no se convierten en hechos del mundo; se distinguen los nombres de jugadores de las identidades de personajes. Las grafías dudosas siguen señaladas y los alias no se fusionan por parecido. Los errores del reconocimiento automático requieren contraste con el audio cuando afectan a la interpretación.

Las {len(data['seguimiento']['preguntas'])} preguntas se cotejan con evidencias posteriores, manteniendo el origen y la respuesta. No se cierra un misterio por falta de menciones. El estado de cada entrada indica hasta dónde llega su cotejo. {'Todas las entradas están cotejadas hasta el epílogo del capítulo 182; las preguntas pendientes o parciales conservan lo que sigue sin respuesta en el catálogo disponible.' if not data['seguimiento']['por_actualizar'] else str(data['seguimiento']['por_actualizar'])+' entradas necesitan cotejar las sesiones posteriores.'}

## Fechas de emisión y publicación

Cada capítulo distingue el directo original de Twitch, la publicación posterior en YouTube y el aviso de Discord. Se cotejan campaña, número y título; los títulos contradictorios y los avisos repetidos en días distintos quedan pendientes. Las tarjetas de YouTube sin marca temporal solo acreditan que el vídeo estaba disponible cuando se anunció. El enlace Twitch de la descripción promocional de YouTube no convierte el aviso en un directo.

Las fechas civiles se muestran en Europe/Madrid. Se conserva por separado la hora del aviso y la marca temporal de su tarjeta. La apertura del directo no fija el comienzo exacto de la partida, especialmente en los directos mixtos 72–74 con Diceland. Esta cronología civil no establece fechas del calendario ficticio; las escenas de rol escrito conservan su propia lectura y fuentes.

La cronología de Kuroto tiene fecha para sus 181 capítulos catalogados: 163 documentadas y 18 asumidas, con estimaciones de origen, fuentes y discrepancias conservadas. El cotejo de información y anuncios adopta el 49 el 24 de septiembre de 2024, el 56 el 10 de octubre de 2024 y el 134 el 2 de julio de 2025. Los avisos rotulados Zaland o Campaña III se conservan como contradicciones; no se reclasifican como pruebas directas de Kuroto. Los títulos repetidos pueden ser continuaciones, intentos cancelados o avisos sin actualizar. Aceptar un día no fija una hora ni un corte exacto para el rol escrito. El orden de capítulos se usa como hipótesis de orden de emisión.

Los calendarios de información se conservan como programación prevista, con lectura visual completa, hashes y marcas de publicación y edición. Se muestran separados del aviso de directo y de las subidas de YouTube. Un plan puede cambiar: Kuroto 12 pasa del 2 al 7 de mayo entre calendarios. Kuroto 55 y 56 adoptan el 9 y 10 de octubre como hipótesis conjunta del calendario y de dos avisos con títulos anteriores. El aviso literal del 55 del día 10 y la antigua correspondencia se conservan en el registro de corrección. Las inferencias no se confirman entre sí ni modifican el canon narrativo.

## Preparación local

Las entregas de los bloques se integran tras comprobar hashes, citas, relatos, horizontes de revisión y cobertura de entidades. Los cambios permanecen en local. No se publica ni se hace git push sin aprobación expresa del usuario sobre la versión revisada.
'''
    from rol_escrito import ROLE_METHOD
    document('metodo','Fuentes y método de Kuroto','METODO.md',method + '\n' + ROLE_METHOD)
    status = (f'**Estado de Kuroto:** {len(chapters)} vídeos catalogados; {len(available)} transcripciones '
              f'({len(available)-len(local)} de YouTube y {len(local)} locales). '
              f'{len(reviewed)} sesiones con relato revisado, {len(data["facts"])} evidencias y '
              f'{len(data["entities"])} fichas con historia. Revisión continua hasta el capítulo {through}; '
              f'{len(chapters)-len(reviewed)} sesiones pendientes. '
              + ('La lectura de los bloques está completada; la versión permanece en local para revisión, sin publicación autorizada.' if complete else
              'La revisión se realiza en bloques paralelos y todos los cambios permanecen en local, sin publicación autorizada.'))
    for path in (ROOT / 'README.md', KUROTO / 'README.md'):
        if path.exists():
            lines = path.read_text(encoding='utf-8').splitlines()
            lines = [status if line.startswith('**Estado de Kuroto:**') else line for line in lines]
            next_pending = next((chapter['capitulo'] for chapter in chapters if chapter['estado'] != 'revisado'), None)
            checkpoint = ('**Lectura completada de las 181 sesiones disponibles.** Consultar [REVISION.md](REVISION.md) para el catálogo y la procedencia de cada sesión.' if complete else
                          f'**Primer capítulo pendiente desde el inicio: {next_pending}.** La lectura continúa en bloques paralelos; consultar [REVISION.md](REVISION.md) para distinguir las sesiones efectivamente integradas.')
            lines = [checkpoint if line.startswith(('**El siguiente capítulo que debe leerse completo', '**Primer capítulo pendiente desde el inicio:', '**Lectura completada de las')) else line for line in lines]
            write(path, '\n'.join(lines)+'\n')
    write_json(KUROTO / 'fuentes/estado_fuentes.json', {
        'videos_catalogados':len(chapters), 'transcripciones_youtube':len(available)-len(local),
        'transcripciones_locales':[chapter['capitulo'] for chapter in local],
        'capitulos_sin_fuente':[chapter['capitulo'] for chapter in chapters if not chapter['transcripcion_disponible']],
        'fuentes_conservadas':True,
        'nota':'La generación de transcripciones locales no equivale a una revisión narrativa.'})
    lines = ['# Estado de la revisión de Kuroto', '', scope, '',
             'Los bloques se han leído en paralelo y se integran tras validar sus evidencias. '
             + ('La lectura de las sesiones disponibles está completada. No se publica automáticamente.' if complete else
                'Un capítulo pendiente de integración puede estar todavía en revisión. No se publica automáticamente.'), '',
             '| Capítulo | Sesión | Fuente | Revisión |', '|---|---|---|---|']
    for chapter in chapters:
        source = 'Audio transcrito localmente' if chapter.get('fuente_transcripcion') else 'Subtítulos YouTube' if chapter['transcripcion_disponible'] else 'Pendiente'
        lines.append(f'| {chapter["capitulo"]} | {chapter["titulo"].replace("|", "/")} | {source} | {chapter["estado"]} |')
    write(KUROTO / 'REVISION.md', '\n'.join(lines)+'\n')
    return scope
