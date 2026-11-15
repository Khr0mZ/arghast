"""Conserva la procedencia y reparte la lectura íntegra del capítulo 48."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[5]
FOLDER=Path(__file__).parent
sys.path.insert(0,str(ROOT/'scripts'))
from construir import read_json,sha,parse_vtt,normalize
from datos_publicos import load_public_world
from subtitulos import texto_desde_vtt


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    newline='\r\n' if path.exists() and b'\r\n' in path.read_bytes() else '\n'
    path.write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+'\n').replace('\n',newline).encode('utf-8'))


def main():
    proof=ROOT/'.local/capitulo48';proof.mkdir(parents=True,exist_ok=True)
    if not (proof/'baseline.json').exists():
        world=load_public_world(ROOT)
        originals={p.relative_to(ROOT).as_posix():sha(p) for c in ('xoltacan','kuroto')
            for sub in ('fuentes','conocimiento/rol_escrito') for p in (ROOT/'campanas'/c/sub).rglob('*')
            if p.is_file() and not p.name.startswith('48 - FYarBX28XfI.')}
        save(proof/'baseline.json',dict(originales=originals,
            kuroto_sha256=hashlib.sha256(json.dumps(world['campaigns']['kuroto'],ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
            escenas_antes=world['writtenRole']['scenes'],estadisticas_rol=world['writtenRole']['stats']))
        save(FOLDER/'seguimiento_antes.json',world['seguimiento']['preguntas'])
    info=ROOT/'campanas/xoltacan/fuentes/48 - FYarBX28XfI.info.json';meta=read_json(info)
    assert meta['id']=='FYarBX28XfI' and meta['channel_id']=='UCWJ11LdxIuDJpbknXpSPgeg'
    for p in sorted(info.parent.glob('48 - FYarBX28XfI.*.vtt')):
        if not p.with_suffix('.txt').exists():p.with_suffix('.txt').write_bytes(texto_desde_vtt(p).encode('utf-8'))
    path=ROOT/'campanas/xoltacan/catalogo.json';catalog=read_json(path)
    episode=dict(capitulo=48,id=meta['id'],titulo='Una Guarida Apestosa',url=meta['webpage_url'])
    matches=[e for e in catalog['episodios'] if e['capitulo']==48 or e['id']==episode['id']]
    assert not matches or matches==[episode]
    if not matches:catalog['episodios'].append(episode);save(path,catalog)
    path=ROOT/'campanas/xoltacan/config/emisiones.json';dates=read_json(path)
    dates['capitulos']['48']=dict(video_id=meta['id'],twitch=dict(estado='documentada',fecha='2026-07-29',
        fuentes=['1532095200023937216'],criterio='campana_numero_y_titulo',
        nota='La tarjeta conservada identifica campaña, capítulo y título; no fija el comienzo exacto del rol.',
        variantes=None,fechas_candidatas=['2026-07-29']),youtube=dict(estado='publicacion_documentada',fecha='2026-11-15',
        fecha_aviso=None,fuentes=[],origen_fecha='metadatos_youtube',archivo_metadatos=info.relative_to(ROOT).as_posix(),
        sha256_metadatos=sha(info),publicacion_reportada_utc=datetime.fromtimestamp(meta['timestamp'],timezone.utc).isoformat()))
    save(path,dates)
    path=ROOT/'campanas/xoltacan/config/duraciones_rol.json';durations=read_json(path)
    durations['fuentes']['xoltacan48']=dict(archivo=info.relative_to(ROOT).as_posix(),sha256=sha(info))
    durations['campanas']['xoltacan']['48']=dict(video_id=meta['id'],segundos=meta['duration'],fuente='xoltacan48');save(path,durations)
    source=info.parent/'48 - FYarBX28XfI.es-orig.vtt';segments=parse_vtt(source)
    names=read_json(ROOT/'campanas/xoltacan/config/nombres.json')['alias_confirmados']
    for s in segments:s['texto_normalizado']=normalize(s['texto_original'],names)
    questions=read_json(FOLDER/'seguimiento_antes.json')
    split=dict(capitulo=48,fuente=source.relative_to(ROOT).as_posix(),sha256=sha(source),total_segmentos=len(segments),bloques=[])
    for i in range(3):
        rows=segments[len(segments)*i//3:len(segments)*(i+1)//3];qs=questions[len(questions)*i//3:len(questions)*(i+1)//3]
        save(FOLDER/f'bloque_{i+1}_segmentos.json',rows);save(FOLDER/f'preguntas_bloque_{i+1}.json',qs)
        (FOLDER/f'bloque_{i+1}.md').write_bytes(('\n\n'.join(f'[{r["inicio"]}–{r["fin"]}] {r["texto_normalizado"]}' for r in rows)+'\n').encode('utf-8'))
        split['bloques'].append(dict(bloque=i+1,inicio=rows[0]['inicio'],fin=rows[-1]['fin'],segmentos=len(rows),
            palabras=sum(len(r['texto_original'].split()) for r in rows),primer_segmento=rows[0]['id'],ultimo_segmento=rows[-1]['id'],
            preguntas_asignadas=[q['id'] for q in qs]))
    save(FOLDER/'reparto.json',split)
    groups=read_json(ROOT/'campanas/xoltacan/config/entidades.json')['grupos']
    save(FOLDER/'identidades_contexto.json',dict(grupos=groups,criterio='Catálogo local vigente; conservar variantes originales en las citas y no fusionar por semejanza.'))
    save(ROOT/'campanas/xoltacan/revision/fuente_xoltacan_48.json',dict(
        **{k:meta[k] for k in ('id','title','duration','upload_date','channel','channel_id','webpage_url')},
        capitulo=48,recuperado_el='2026-11-15',herramienta='yt-dlp',version=meta['_version']['version'],
        estado_revision='pendiente',lectura='Descargado y repartido; pendiente de lectura íntegra e integración editorial.',
        originales={p.relative_to(ROOT).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(info.parent.glob('48 - FYarBX28XfI.*'))},
        reparto='borradores/48/reparto.json'))
    print(json.dumps(split,ensure_ascii=False))


if __name__=='__main__':main()
