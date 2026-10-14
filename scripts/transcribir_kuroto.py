"""Genera fuentes de transcripción local para vídeos sin subtítulos de YouTube.

No redacta fichas ni marca capítulos como revisados. El audio y los modelos se
guardan en .pruebas; la procedencia y los hashes acompañan cada VTT generado.
"""
import argparse
import hashlib
import importlib.metadata
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from construir import ROOT, write_json, read_json
from campanas import KUROTO


def timestamp(value):
    milliseconds = round(value * 1000)
    hours, remainder = divmod(milliseconds, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    seconds, fraction = divmod(remainder, 1000)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}.{fraction:03d}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capitulos', nargs='+', type=int, default=[96, 135, 136])
    parser.add_argument('--modelo', default='turbo')
    parser.add_argument('--dispositivo', choices=['cuda', 'cpu'], default='cuda')
    args = parser.parse_args()
    cache = ROOT / '.pruebas/modelos_whisper'
    cache.mkdir(parents=True, exist_ok=True)
    os.environ['HF_HOME'] = str(ROOT / '.pruebas/huggingface')
    # Bibliotecas NVIDIA aisladas dentro de este entorno; no modifica el sistema.
    handles = []
    library_dirs = sorted({dll.parent for dll in (Path(sys.prefix) / 'Lib/site-packages/nvidia').rglob('*.dll')})
    for directory in library_dirs:
        if hasattr(os, 'add_dll_directory'):
            handles.append(os.add_dll_directory(str(directory)))
    os.environ['PATH'] = os.pathsep.join(str(directory) for directory in library_dirs) + os.pathsep + os.environ.get('PATH', '')
    from faster_whisper import WhisperModel, BatchedInferencePipeline
    compute = 'int8_float16' if args.dispositivo == 'cuda' else 'int8'
    print(f'Cargando Whisper {args.modelo} en {args.dispositivo}, {compute}.', flush=True)
    model = WhisperModel(args.modelo, device=args.dispositivo, compute_type=compute,
                         download_root=str(cache), cpu_threads=4)
    pipeline = BatchedInferencePipeline(model=model)
    episodes = {episode['capitulo']: episode for episode in read_json(KUROTO / 'catalogo.json')['episodios']}
    provenance_path = KUROTO / 'fuentes/transcripciones_locales.json'
    provenance = read_json(provenance_path) if provenance_path.exists() else {}
    for number in args.capitulos:
        episode = episodes[number]
        target = KUROTO / 'fuentes' / f'{number:03d} - {episode["id"]}.es-local.vtt'
        if target.exists():
            if str(number) not in provenance or provenance[str(number)]['vtt_sha256'] != hashlib.sha256(target.read_bytes()).hexdigest():
                raise ValueError('VTT local existente sin procedencia verificable: ' + str(target))
            print(f'{number}: transcripción existente conservada.', flush=True)
            continue
        audio_files = [path for path in (ROOT / '.pruebas/audio_kuroto').glob(episode['id']+'.*')
                       if path.suffix in ('.webm', '.m4a', '.opus', '.mp3', '.wav')]
        if len(audio_files) != 1:
            raise ValueError(f'{number}: se necesita exactamente un audio completo en .pruebas/audio_kuroto')
        audio = audio_files[0]
        print(f'{number}: transcribiendo {audio.name}.', flush=True)
        segments, info = pipeline.transcribe(str(audio), batch_size=8, language='es',
                                            beam_size=5, vad_filter=True,
                                            condition_on_previous_text=False)
        temporary = target.with_suffix('.vtt.tmp')
        count = 0
        with temporary.open('w', encoding='utf-8', newline='\n') as output:
            output.write('WEBVTT\nKind: captions\nLanguage: es\n\n')
            for segment in segments:
                text = ' '.join(segment.text.split()).replace('-->', '→')
                if not text:
                    continue
                count += 1
                output.write(f'{count}\n{timestamp(segment.start)} --> {timestamp(segment.end)}\n{text}\n\n')
                if count % 100 == 0:
                    output.flush()
                    print(f'{number}: {count} segmentos; audio hasta {timestamp(segment.end)}.', flush=True)
        if not count:
            raise ValueError(f'{number}: Whisper no ha producido texto; no se registra la fuente')
        record = {'tipo': 'transcripcion_local_audio', 'video_id': episode['id'], 'url': episode['url'],
                  'fecha_utc': datetime.now(timezone.utc).isoformat(), 'modelo': args.modelo,
                  'motor': 'faster-whisper', 'version_motor': importlib.metadata.version('faster-whisper'),
                  'idioma': 'es', 'beam_size': 5, 'vad_filter': True, 'condition_on_previous_text': False,
                  'dispositivo': args.dispositivo, 'compute_type': compute,
                  'audio_sha256': hashlib.sha256(audio.read_bytes()).hexdigest(),
                  'audio_archivo_local': audio.relative_to(ROOT).as_posix(),
                  'vtt': target.relative_to(KUROTO).as_posix(),
                  'vtt_sha256': hashlib.sha256(temporary.read_bytes()).hexdigest(),
                  'segmentos': count, 'duracion_audio_segundos': info.duration,
                  'nota': 'Generada localmente del audio. No es una pista de subtítulos publicada por YouTube; pendiente de revisión editorial.'}
        temporary.replace(target)
        provenance[str(number)] = record
        write_json(provenance_path, provenance)
        print(f'{number}: VTT y procedencia conservados; {count} segmentos.', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
