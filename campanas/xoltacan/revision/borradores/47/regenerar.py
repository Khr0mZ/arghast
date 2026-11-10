"""Regenera las vistas tras la integración; los originales permanecen intactos."""
from preparar import ROOT
from construir import read_json, render_dossier, render_indexes, validate_fact
from rutas import episodios
from historias import load_chapter_histories
from seguimiento import build_tracking, render_tracking
from fechas_emision import load_dates
from organizar import render_views
from construir_interfaz import main as build_interface


def main():
    episodes = episodios()
    folder = ROOT / 'campanas/xoltacan/conocimiento/capitulos'
    dossiers = {ep['capitulo']:read_json(folder / f'{ep["capitulo"]:02d}.json') for ep in episodes}
    facts = {f['id']:{**f, 'capitulo':n} for n,d in dossiers.items() for f in d['afirmaciones']}
    histories = load_chapter_histories([dict(capitulo=n, resumen=d['resumen'], estado=d['estado_revision'])
                                       for n,d in dossiers.items()], facts)
    source = ROOT / 'campanas/xoltacan/fuentes/47 - yvqhR20m7Zg.es-orig.vtt'
    for fact in dossiers[47]['afirmaciones']:
        validate_fact(fact, source)
    tracking = build_tracking()
    emissions = load_dates('xoltacan', episodes)
    for episode in episodes:
        n = episode['capitulo']
        render_dossier(episode, dossiers[n], tracking, histories[n], emissions[n])
    render_indexes(read_json(ROOT / 'campanas/xoltacan/derivados/inventario.json'))
    render_tracking(tracking)
    render_views()
    build_interface()
    print('47 capítulos y todas sus vistas regenerados; las 90 citas nuevas se han vuelto a validar.')


if __name__ == '__main__':
    main()
