"""Exporta las fichas revisadas de Kuroto como lecturas Markdown con fuentes."""
import re
from construir import write
from campanas import KUROTO, build_kuroto


def export(data):
    facts = {fact['id']: fact for fact in data['facts']}
    chapters = {chapter['capitulo']: chapter for chapter in data['chapters']}

    def sources(references):
        links = []
        for key in references:
            fact = facts[key]
            h, m, s = map(float, fact['inicio'].split(':'))
            url = chapters[fact['capitulo']]['url'] + '&t=' + str(int(h*3600+m*60+s)) + 's'
            links.append(f'[{key} · {fact["inicio"]}]({url})')
        return ' · '.join(links)

    def story(history):
        lines = []
        for stage in (history or {}).get('etapas', []):
            lines += ['## '+stage['titulo'], '', stage['texto'], '', 'Fuentes: '+sources(stage['referencias'])+'.', '']
        return lines

    for chapter in data['chapters']:
        if chapter['estado'] != 'revisado':
            continue
        source = 'una transcripción local del audio con Whisper' if chapter.get('fuente_transcripcion') else 'los subtítulos automáticos de YouTube'
        lines = [f'# Kuroto · Capítulo {chapter["capitulo"]}: {chapter["titulo"]}', '',
                 f'Estado: revisado a partir de {source}; sin cotejo completo de cada palabra con el audio.', '']
        from fechas_emision import markdown_dates
        lines += markdown_dates(chapter.get('emision'))
        lines += story(chapter['history'])
        lines += ['## Evidencias', '']
        for key in chapter['registros']:
            fact = facts[key]
            lines += ['### '+key+' · '+fact['titulo'], '', fact['afirmacion'], '',
                      '> '+fact['cita'], '', 'Fuente: '+sources([key])+'.', '', fact.get('limitacion', ''), '']
        write(KUROTO / 'conocimiento/capitulos' / f'{chapter["capitulo"]:03d}.md', '\n'.join(lines))
    index = ['# Kuroto · Índice de la crónica', '',
             f'{len(chapters)} vídeos catalogados; {sum(chapter["transcripcion_disponible"] for chapter in data["chapters"])} transcripciones disponibles; '
             f'{sum(chapter["estado"] == "revisado" for chapter in data["chapters"])} sesiones revisadas.', '',
             '## Fichas con relato', '']
    managed = set()
    for number, entity in enumerate(data['entities'], 1):
        filename = f'{number:03d}-' + re.sub(r'[^\w-]+', '-', entity['name'].lower()).strip('-') + '.md'
        lines = ['# '+entity['name'], '', entity['description'], '',
                 f'Revisión narrativa hasta el capítulo {(entity.get("history") or {}).get("revisado_hasta", "pendiente")}.', '',
                 entity['note'], ''] + story(entity.get('history'))
        write(KUROTO / 'conocimiento/entidades' / filename, '\n'.join(lines))
        managed.add(filename)
        index.append(f'- [{entity["name"]}](entidades/{filename}) · {entity["type"]}')
    # Los alias cambian el orden de las fichas numeradas. Retirar solo exportaciones
    # reconocibles de este generador, para no empaquetar biografías ya sustituidas.
    destination = (KUROTO / 'conocimiento/entidades').resolve()
    for old in destination.glob('*.md'):
        if old.name in managed or not re.fullmatch(r'\d{3,}-.*\.md', old.name):
            continue
        if not old.resolve().is_relative_to(destination):
            raise ValueError('La exportación antigua sale de su directorio: '+str(old))
        if 'Revisión narrativa hasta el capítulo ' in old.read_text(encoding='utf-8'):
            old.unlink()
    index += ['', '## Sesiones', '']
    for number, chapter in chapters.items():
        title = f'{number:03d} · {chapter["titulo"]}'
        if chapter['estado'] == 'revisado':
            index.append(f'- [{title}](capitulos/{number:03d}.md) · revisado')
        elif chapter['transcripcion_disponible']:
            index.append(f'- [{title}](../derivados/{number:03d}/lectura.md) · transcripción; lectura editorial pendiente')
        else:
            index.append(f'- [{title}]({chapter["url"]}) · transcripción pendiente')
    write(KUROTO / 'conocimiento/INDICE.md', '\n'.join(index)+'\n')
    tracking = ['# Kuroto · Preguntas y desenlaces', '',
                f'Revisión hasta el capítulo {data["seguimiento"]["ultimo_capitulo"]}.', '']
    for question in data['seguimiento']['preguntas']:
        tracking += ['## '+question['id']+' · '+question['pregunta'], '',
                     f'Estado: {question["estado"]}. Origen: capítulo {question["capitulo"]}. Revisada hasta {question["revisado_hasta"]}.', '',
                     question['respuesta'], '', question.get('pendiente', ''), '',
                     'Fuentes: '+sources(question['referencias'])+'.', '']
    write(KUROTO / 'conocimiento/SEGUIMIENTO.md', '\n'.join(tracking))


if __name__ == '__main__':
    export(build_kuroto())
