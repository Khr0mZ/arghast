"""Integra las revisiones de identidades sin promover cada etiqueta a una ficha."""
from pathlib import Path
from construir import ROOT, read_json, write_json


def main():
    path = ROOT / 'config/entidades.json'
    backup = ROOT / 'config/historial/entidades_antes_revision.json'
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(path.read_bytes())
    people = read_json(ROOT / 'config/revision_personajes.json')
    others = read_json(ROOT / 'config/revision_otras_entidades.json')
    groups = people['grupos'] + others['grupos']
    # Son menciones cuya identidad no está resuelta, no personas nuevas acreditadas.
    for group in groups:
        if group['nombre'] in ('Tórtola de las órdenes', 'Angelique'):
            group['visible'] = False
    additions = [
        dict(nombre='Collar de Blink', tipo='objeto', etiquetas=['Collar de Blink', 'Collar serpiente de charca'],
             referencias=['19-014','25-021','28-010'],
             descripcion='Collar obtenido por Blink en la charca y relacionado con las voces y las incursiones de los hombres serpiente.',
             nota='Blink lo guarda en una fruta en el capítulo 19, lo revela en el 25 y lo abandona en el templo en el 28. Es distinto del collar de gemas de la misión de Bonnie.'),
        dict(nombre='Mapa de Poncelot', tipo='objeto', etiquetas=['Mapa Slaz del cofre (grafía provisional)','Mapa de Poncelot (destino Ezlat provisional)'],
             referencias=['20-014','25-019','26-015','28-001'],
             descripcion='Mapa obtenido por Poncelot y usado para llegar a la pirámide de la expedición de los capítulos 26 y 28.',
             nota='Slaz y Ezlat son lecturas o recuerdos del destino del mismo mapa. La grafía del lugar sigue sin fijarse; no son dos mapas por esa variación.'),
    ]
    groups.extend(additions)
    all_facts = {fact['id']: fact for chapter in sorted((ROOT / 'conocimiento/capitulos').glob('*.json'))
                 for fact in read_json(chapter)['afirmaciones']}
    # Entradas singulares conocidas que no requieren agrupar alias.
    singletons = {
        'Xoltacan': ('lugar', 'Isla en la que transcurre la campaña.'),
        'Shiaru': ('lugar', 'Poblado costero bajo la autoridad de Bonnie.'),
        'Tutucan': ('lugar', 'Ciudad elegida para reunir el concilio de líderes.'),
        'Perlasal': ('lugar', 'Población submarina de sirénidos visitada por los viajeros.'),
        'El Bocado del Jaguar': ('lugar', 'Taberna de Cuicapalli, donde Tacha prepara el banquete del cocodrilo.'),
        'Forja del Águila de Sangre': ('lugar', 'Forja de Cuicapalli donde se ofrecen armas y armaduras.'),
        'Cabaña del Sueño': ('lugar', 'Establecimiento de Cuicapalli vinculado al sabio y sus tatuajes.'),
        'Humo del Paso de los Muertos': ('lugar', 'Establecimiento de alquimia de Cuicapalli.'),
        'La Madriguera': ('lugar', 'Alojamiento de Cuicapalli con servicios de sastrería.'),
        'El Huevo Emplumado': ('lugar', 'Taberna de Iktan visitada por los viajeros.'),
        'Granja de Patata': ('lugar', 'Granja de Patata situada junto al camino cercano a Shiaru.'),
        'Cueva de la Hoja Caída': ('lugar', 'Cueva investigada en relación con el envenenamiento de Eromov.'),
        'Templo de los nawals': ('lugar', 'Ruinas donde el grupo encontró un diario y a una mujer que se transformaba en pantera.'),
        'Templo de Lares (grafía provisional)': ('lugar', 'Templo investigado por encargo de Eromov, ocupado por hombres serpiente.'),
        'Tribu de la Hoja Caída': ('faccion', 'Nombre con el que se presentan las visitantes relacionadas con la investigación del veneno.'),
        'Profundos (opresores de Perlasal)': ('faccion', 'Grupo al que Maris atribuye los secuestros y los rituales de los merros.'),
        'Yuan-ti': ('faccion', 'Hombres serpiente presentes en templos e incursiones de la campaña.'),
        'Nawals (grafía provisional)': ('faccion', 'Tradición o grupo relacionado con los rituales de transformación.'),
        'Patata Hammer (martillo de Patata)': ('objeto', 'Martillo obtenido por Patata después de que se rompiera su espada.'),
        'Collar antiguo de oro con gemas': ('objeto', 'Collar encontrado durante la búsqueda de los piratas enviados por Bonnie.'),
        'Collar de plata de Leo': ('objeto', 'Collar de Leo usado por Naór durante el combate de la cueva de lobos.'),
        'Brújula de deseos de Nox': ('objeto', 'Brújula cuya dirección cambia según el deseo de Nox.'),
        'Moneda pirata de Bonnie': ('objeto', 'Moneda que Bonnie utiliza durante la defensa de Shiaru.'),
        'Moneda negra del mercante': ('objeto', 'Moneda obtenida del marinero de la boca cosida en el mercante maldito.'),
        'Diario de capitán del mercante': ('objeto', 'Diario que relata la enfermedad de la hija del capitán y una negociación con una entidad.'),
        'Relicario de gema negra': ('objeto', 'Relicario vinculado a la maldición del mercante y a la marca de Patata.'),
        'Diálogo (bate de Ione)': ('objeto', 'Bate de Ione, distinto de sus armas de puño.'),
        'Espada azul de escamas de Triel': ('objeto', 'Espada de Triel descrita como hecha con escamas azules de dragón.'),
        'Pociones de Arwen': ('objeto', 'Pociones mencionadas y utilizadas por los viajeros durante la campaña.'),
    }
    used = {label for group in groups for label in group['etiquetas']}
    for label, (kind, description) in singletons.items():
        mentions = [fid for fid,fact in all_facts.items() if label in fact['entidades']]
        if label in used or not mentions:
            continue
        name = label.replace(' (grafía provisional)', '').replace(' (opresores de Perlasal)', '')
        if name == 'Patata Hammer (martillo de Patata)': name = 'Patata Hammer'
        if name == 'Diálogo (bate de Ione)': name = 'Diálogo'
        groups.append(dict(nombre=name,tipo=kind,etiquetas=[label],referencias=mentions[:3],
                           descripcion=description,nota='Entrada documentada en los registros citados.'))
    # El cadáver pertenece a la biografía de Erendriel, no crea un segundo personaje.
    erendriel = next(group for group in groups if group['nombre']=='Erendriel')
    if 'Cuerpo de Erendriel exhibido' not in erendriel['etiquetas']:
        erendriel['etiquetas'].append('Cuerpo de Erendriel exhibido')
    erendriel['referencias'] = list(dict.fromkeys([*erendriel['referencias'],'16-004','29-003']))
    updates_path = ROOT / 'config/actualizaciones_catalogo.json'
    if updates_path.exists():
        for updated in read_json(updates_path)['grupos']:
            position = next((i for i,group in enumerate(groups) if group['nombre']==updated['nombre']), None)
            if position is None:
                groups.append(updated)
            else:
                groups[position].update(updated)
    exclusions = others.get('exclusiones', [])
    # Las propuestas se conservan sin convertirlas en identidades aprobadas.
    result = dict(criterio='Una ficha por identidad revisada. Las etiquetas de extracción permanecen en las fuentes y no crean automáticamente personas, objetos o lugares.',
                  grupos=groups,exclusiones=exclusions,propuestas_dudosas=people['propuestas_dudosas'])
    claimed = {}
    for group in groups:
        for reference in group['referencias']:
            if reference not in all_facts:
                raise ValueError('Referencia inexistente: '+reference)
        for label in group['etiquetas']:
            if label in claimed and claimed[label]!=group['nombre']:
                raise ValueError('Etiqueta en dos grupos: '+label)
            claimed[label] = group['nombre']
    write_json(path,result)
    print(f'Catálogo: {len(groups)} fichas revisadas; {len(claimed)} etiquetas agrupadas; {len(exclusions)} etiquetas de revisión separadas.')


if __name__=='__main__':
    main()
