"""Auditoría reproducible de integridad, cobertura y evidencias del proyecto."""
import argparse
import json
import re
import zipfile
from collections import Counter
from construir import ROOT, KB, BUILD, SOURCES, read_json, sha, validate_fact
from catalogo import load_catalog
from seguimiento import build_tracking


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exigir-completo', action='store_true', help='Falla si queda algún capítulo catalogado sin revisión.')
    parser.add_argument('--comparar-zip', action='store_true', help='Compara originales con ZIP de descarga inicial, cuando existe.')
    args = parser.parse_args()
    episodes = read_json(SOURCES / 'episodios.json')
    extra = ROOT / 'config/episodios_nuevos.json'
    if extra.exists():
        episodes += read_json(extra)
    baseline = read_json(BUILD / 'originales_sha256.json')
    for relative, expected in baseline.items():
        path = ROOT / relative
        if not path.exists() or sha(path) != expected['sha256'] or path.stat().st_size != expected['bytes']:
            raise ValueError('Original modificado o desaparecido: ' + relative)
    reviewed, pending, total = [], [], 0
    categories = Counter()
    metadata_references, fact_ids = [], set()
    for ep in sorted(episodes, key=lambda row: row['capitulo']):
        n = ep['capitulo']
        path = KB / 'capitulos' / f'{n:02d}.json'
        if not path.exists():
            pending.append(n)
            continue
        dossier = read_json(path)
        meta = read_json(BUILD / f'{n:02d}' / 'meta.json')
        source = ROOT / meta['fuente']
        if dossier['fuente_sha256'] != sha(source):
            raise ValueError(f'Ficha {n:02d} corresponde a otra fuente')
        if dossier.get('capitulo') != n:
            raise ValueError(f'Número de ficha inconsistente: {path}')
        facts = dossier.get('afirmaciones', [])
        if not facts:
            raise ValueError(f'Ficha vacía: {n:02d}')
        ids = [fact['id'] for fact in facts]
        fact_ids.update(ids)
        for key in ('resumen', 'misiones', 'preguntas', 'contradicciones', 'nombres_dudosos'):
            text = json.dumps(dossier.get(key, ''), ensure_ascii=False)
            metadata_references.extend((n, key, ref) for ref in re.findall(r'\b\d{2}-\d{3}\b', text))
        if len(set(ids)) != len(ids) or any(not fact_id.startswith(f'{n:02d}-') for fact_id in ids):
            raise ValueError(f'Identificadores duplicados o de otro capítulo: {n:02d}')
        for fact in facts:
            validate_fact(fact, source)
            cue = fact.get('evidencia_cue')
            if cue and fact['cita'] not in cue['texto']:
                raise ValueError('Ancla no contenida en cue guardado: ' + fact['id'])
            categories[fact['tipo']] += 1
        total += len(facts)
        (reviewed if dossier.get('estado_revision') == 'revisado' else pending).append(n)
    compared = 0
    _, catalog, _ = load_catalog()
    for name, group in catalog.items():
        for reference in group.get('referencias', []):
            if '-' in reference and reference not in fact_ids:
                raise ValueError('Referencia de identidad inexistente: ' + name + ' ' + reference)
    if args.exigir_completo:
        bad = [(n, key, ref) for n, key, ref in metadata_references if ref not in fact_ids]
        if bad:
            raise ValueError('Referencias editoriales inexistentes: ' + repr(bad))
        missing_links = []
        for document in [ROOT / 'README.md', *KB.rglob('*.md')]:
            content = document.read_text(encoding='utf-8')
            bad_ids = [ref for ref in re.findall(r'\b\d{2}-\d{3}\b', content) if ref not in fact_ids]
            if bad_ids:
                raise ValueError('Referencias inexistentes en documento ' + str(document) + ': ' + repr(sorted(set(bad_ids))))
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
                target = target.strip().strip('<>').split('#', 1)[0]
                if not target or re.match(r'^[a-zA-Z]+://', target):
                    continue
                if not (document.parent / target).resolve().exists():
                    missing_links.append((document.relative_to(ROOT).as_posix(), target))
        if missing_links:
            raise ValueError('Enlaces locales inexistentes: ' + repr(missing_links[:30]))
    archive_path = ROOT / 'xoltacan_transcripciones_01-39.zip'
    if args.comparar_zip:
        if not archive_path.exists():
            raise ValueError('No existe ZIP inicial de transcripciones')
        with zipfile.ZipFile(archive_path) as archive:
            names = {name.rsplit('/', 1)[-1]: name for name in archive.namelist() if not name.endswith('/')}
            for relative in baseline:
                path = ROOT / relative
                if path.name not in names:
                    # Episodios futuros no estuvieron en descarga inicial.
                    continue
                if archive.read(names[path.name]) != path.read_bytes():
                    raise ValueError('Original difiere de ZIP inicial: ' + relative)
                compared += 1
        if not compared:
            raise ValueError('ZIP no contiene originales comparables')
    tracking = build_tracking()
    if args.exigir_completo and (tracking['estados'].get('sin_revisar',0) or tracking['por_actualizar']):
        raise ValueError('Quedan preguntas históricas o capítulos posteriores sin cotejar')
    result = {'capitulos_catalogados': len(episodes), 'revisados': len(reviewed),
              'pendientes': pending, 'registros': total, 'originales_integros': len(baseline),
              'originales_identicos_zip': compared, 'tipos_evidencia': dict(categories),
              'preguntas_cotejadas':len(tracking['preguntas']), 'estados_preguntas':tracking['estados'],
              'limite': 'Valida evidencia textual y cobertura declarada; no certifica audio ni interpretación.'}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.exigir_completo and pending:
        raise ValueError('Quedan capítulos pendientes de revisión: ' + ', '.join(map(str, pending)))


if __name__ == '__main__':
    main()
