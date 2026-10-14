"""Une revisiones por pregunta y genera seguimiento sin alterar las fuentes."""
import argparse
import hashlib
import re
from collections import Counter
from construir import ROOT, KB, read_json, write_json, write

STATES = {'resuelta':'Resuelta', 'parcial':'Parcialmente resuelta',
          'pendiente':'Pendiente', 'sin_revisar':'Sin revisar'}


def build_tracking(chapters=None, review_files=None):
    if chapters is None:
        chapters = [read_json(p) for p in sorted((KB / 'capitulos').glob('*.json'))]
    facts = {f['id']: f for chapter in chapters for f in chapter['afirmaciones']}
    latest = max((c['capitulo'] for c in chapters), default=0)
    expected = {f'P{c["capitulo"]:02d}-{i:03d}': (c['capitulo'], i, question)
                for c in chapters for i, question in enumerate(c.get('preguntas', []), 1)}
    if review_files is None:
        review_files = sorted((ROOT / 'config').glob('seguimiento_preguntas_*.json'))
    reviews = {}
    for path in review_files:
        review = read_json(path)
        for entry in review['preguntas']:
            qid = entry['id']
            if qid in reviews:
                raise ValueError('Pregunta revisada dos veces: ' + qid)
            if qid not in expected:
                raise ValueError('Pregunta que ya no existe: ' + qid)
            n, index, question = expected[qid]
            if (entry['capitulo'], entry['indice'], entry['pregunta']) != (n, index, question):
                raise ValueError('La pregunta cambió; revisar su seguimiento: ' + qid)
            if entry['estado'] not in STATES or entry['estado'] == 'sin_revisar':
                raise ValueError('Estado editorial inválido: ' + qid)
            horizon = entry.get('revisado_hasta', review['revisado_hasta'])
            if not isinstance(horizon, int) or not n <= horizon <= latest:
                raise ValueError('Cobertura de revisión inválida: ' + qid)
            if not entry['respuesta'].strip():
                raise ValueError('Falta explicación de la revisión: ' + qid)
            if entry['estado'] == 'resuelta' and entry.get('pendiente', '').strip():
                raise ValueError('Pregunta cerrada con partes pendientes: ' + qid)
            if entry['estado'] != 'resuelta' and not entry.get('pendiente', '').strip():
                raise ValueError('Falta describir lo pendiente: ' + qid)
            refs = entry['referencias']
            if len(refs) != len(set(refs)) or any(ref not in facts for ref in refs):
                raise ValueError('Referencia duplicada o inexistente: ' + qid)
            if any(int(ref.split('-')[0]) > horizon for ref in refs):
                raise ValueError('Referencia fuera de la revisión: ' + qid)
            if entry['estado'] in ('resuelta', 'parcial') and not any(
                    int(ref.split('-')[0]) > n for ref in refs):
                raise ValueError('La respuesta requiere evidencia posterior: ' + qid)
            reviews[qid] = {**entry, 'revisado_hasta':horizon}
    questions = []
    for qid, (n, index, text) in expected.items():
        default = {'id':qid, 'capitulo':n, 'indice':index, 'pregunta':text,
                   'estado':'sin_revisar', 'respuesta':'Todavía no se ha cotejado esta pregunta con capítulos posteriores.',
                   'referencias':[], 'pendiente':'Revisar las fuentes posteriores.', 'revisado_hasta':n}
        entry = {**reviews.get(qid, default)}
        entry['sha256_pregunta'] = hashlib.sha256(text.encode('utf-8')).hexdigest()
        entry['referencias_origen'] = list(dict.fromkeys(re.findall(r'\b\d{2}-\d{3}\b', text)))
        entry['requiere_actualizacion'] = entry['revisado_hasta'] < latest
        questions.append(entry)
    return {'version':1, 'ultimo_capitulo':latest, 'preguntas':questions,
            'estados':dict(Counter(q['estado'] for q in questions)),
            'por_actualizar':sum(q['requiere_actualizacion'] for q in questions)}


def reference_link(fid, facts):
    fact = facts[fid]
    minute = fact.get('evidencia_cue', {}).get('inicio', fact['inicio']).split('.')[0]
    return f'[{fid} · {minute}](capitulos/{int(fid.split("-")[0]):02d}.md)'


def render_tracking(tracking=None):
    tracking = tracking or build_tracking()
    facts = {f['id']:f for p in (KB / 'capitulos').glob('*.json')
             for f in read_json(p)['afirmaciones']}
    write_json(KB / 'seguimiento_preguntas.json', tracking)
    lines = ['# Preguntas y respuestas posteriores', '',
             'Cada entrada conserva la pregunta de su sesión y la vincula con evidencias posteriores. '
             'Una respuesta parcial no cierra las partes que siguen desconocidas. '
             'Los minutos corresponden a las anclas de los subtítulos.', '',
             ' · '.join(f'{STATES[state]}: {tracking["estados"].get(state, 0)}' for state in STATES), '',
             f'Catálogo revisado hasta el capítulo {tracking["ultimo_capitulo"]}. '
             f'Entradas que requieren revisión tras nuevos capítulos: {tracking["por_actualizar"]}.', '']
    for q in tracking['preguntas']:
        lines += [f'## {q["id"]} · {STATES[q["estado"]]}', '', q['pregunta'], '',
                  f'Origen: [capítulo {q["capitulo"]:02d}](capitulos/{q["capitulo"]:02d}.md). '
                  f'Cotejada hasta el capítulo {q["revisado_hasta"]}.', '', q['respuesta'], '']
        if q['referencias']:
            lines += ['Evidencia posterior: ' + ' · '.join(reference_link(fid, facts) for fid in q['referencias']), '']
        if q['pendiente']:
            lines += ['**Sigue pendiente:** ' + q['pendiente'], '']
        if q['requiere_actualizacion']:
            lines += ['**Revisar los capítulos añadidos después de este cotejo.**', '']
    write(KB / 'SEGUIMIENTO.md', '\n'.join(lines))
    return tracking


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exigir-completo', action='store_true')
    args = parser.parse_args()
    tracking = render_tracking()
    if args.exigir_completo and (tracking['estados'].get('sin_revisar') or tracking['por_actualizar']):
        raise ValueError('Quedan preguntas o capítulos posteriores sin cotejar')
    print(f'{len(tracking["preguntas"])} preguntas: {tracking["estados"]}; por actualizar: {tracking["por_actualizar"]}.')


if __name__ == '__main__':
    main()
