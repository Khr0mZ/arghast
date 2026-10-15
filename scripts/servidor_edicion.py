"""Archivo local con correcciones compartidas; no modifica las fuentes originales."""
import argparse
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import sqlite3
import threading
import time
from copy import deepcopy
from modelo_edicion import editable, validate
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, unquote, parse_qs

ROOT = Path(__file__).resolve().parents[1]


def catalog(world):
    result = {}
    for campaign in ('xoltacan', 'kuroto'):
        data = world if campaign == 'xoltacan' else world['campaigns'][campaign]
        def add(kind, identity, obj, fields):
            for field in fields:
                if isinstance(obj.get(field), str):
                    result[(campaign, kind, str(identity), field)] = obj[field]
            for i, stage in enumerate((obj.get('history') or {}).get('etapas', [])):
                for field in ('titulo', 'texto'):
                    result[(campaign, kind, str(identity), f'history.etapas.{i}.{field}')] = stage[field]
        for obj in data['chapters']:
            add('capitulo', obj['capitulo'], obj, ['resumen'])
        for obj in data['entities']:
            add('entidad', obj['name'], obj, ['description', 'note'])
        for obj in data['facts']:
            add('registro', obj['id'], obj, ['titulo', 'afirmacion', 'limitacion'])
        for obj in data.get('seguimiento', {}).get('preguntas', []):
            add('pregunta', obj['id'], obj, ['respuesta', 'pendiente'])
        for identity, obj in data.get('documents', {}).items():
            if isinstance(obj, dict):
                add('documento', identity, obj, ['text'])
    return result


class ArchiveServer(ThreadingHTTPServer):
    def __init__(self, address, root, database, code):
        self.root = Path(root).resolve()
        html = (self.root / 'arghast.html').read_text(encoding='utf-8')
        world = json.loads(re.search(r'<script id="xoltacan-data" type="application/json">(.*?)</script>', html, re.S)[1])
        self.fields = catalog(world)
        self.original = {campaign:editable(world if campaign == 'xoltacan' else world['campaigns'][campaign]) for campaign in ('xoltacan','kuroto')}
        self.code_hash = hashlib.sha256(code.encode()).digest()
        self.sessions = {}
        self.attempts = {}
        self.lock = threading.Lock()
        self.db = sqlite3.connect(database, check_same_thread=False)
        self.db.execute('CREATE TABLE IF NOT EXISTS edits (revision INTEGER PRIMARY KEY, campaign TEXT, kind TEXT, identity TEXT, field TEXT, value TEXT, author TEXT, reason TEXT, created REAL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS documents (revision INTEGER PRIMARY KEY AUTOINCREMENT, campaign TEXT, content TEXT, author TEXT, reason TEXT, created REAL)')
        self.db.commit()
        super().__init__(address, Handler)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass  # No registrar códigos ni contenido de las correcciones.

    def respond(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)

    def rows(self):
        return [dict(zip(('revision', 'campaign', 'kind', 'identity', 'field', 'value', 'author', 'reason', 'created'), row))
                for row in self.server.db.execute('SELECT * FROM edits ORDER BY revision')]

    def documents(self, campaign):
        return [dict(zip(('revision','campaign','author','reason','created'), row)) for row in self.server.db.execute('SELECT revision,campaign,author,reason,created FROM documents WHERE campaign=? ORDER BY revision', (campaign,))]

    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        if path == '/api/editor':
            with self.server.lock:
                rows = self.rows()
            return self.respond(200, {'edits': rows})
        if path.startswith('/api/editor/document/'):
            campaign = path.rsplit('/',1)[-1]
            if campaign not in self.server.original:
                return self.respond(404, {'error':'Campaña desconocida.'})
            with self.server.lock:
                history = self.documents(campaign)
                query = parse_qs(urlsplit(self.path).query)
                latest_revision = history[-1]['revision'] if history else 0
                if query.get('since') == [str(latest_revision)]:
                    return self.respond(200, {'unchanged':True})
                if 'revision' in query:
                    selected = next((r for r in history if str(r['revision'])==query['revision'][0]), None)
                    if not selected:
                        return self.respond(404, {'error':'Versión no disponible.'})
                    saved = self.server.db.execute('SELECT content FROM documents WHERE revision=? AND campaign=?',(selected['revision'],campaign)).fetchone()[0]
                    return self.respond(200, {'content':json.loads(saved)})
                # Migrar las correcciones de texto anteriores sin perder su historial.
                current = deepcopy(self.server.original[campaign])
                groups = {'capitulo':current['chapters'],'entidad':current['entities'],'registro':current['facts'],'pregunta':current['seguimiento']['preguntas']}
                for row in self.rows():
                    if row['campaign'] != campaign:
                        continue
                    identity_field = {'capitulo':'capitulo','entidad':'name','registro':'id','pregunta':'id'}.get(row['kind'])
                    obj = current['documents'].get(row['identity']) if row['kind']=='documento' else next((o for o in groups.get(row['kind'],[]) if str(o[identity_field])==row['identity']), None)
                    if obj is not None:
                        parts = row['field'].split('.')
                        for part in parts[:-1]:
                            obj = obj[int(part)] if isinstance(obj,list) else obj[part]
                        obj[parts[-1]] = row['value']
                if history:
                    saved = self.server.db.execute('SELECT content FROM documents WHERE revision=?',(latest_revision,)).fetchone()[0]
                    current = json.loads(saved)
                return self.respond(200, {'content':current,'revision':latest_revision,'history':[{k:v for k,v in r.items() if k!='content'} for r in history]})
        # Solo servir los artefactos públicos, nunca el repositorio o SQLite.
        if path == '/':
            path = '/arghast.html'
        target = (self.server.root / path.lstrip('/')).resolve()
        allowed = path in ('/arghast.html', '/xoltacan.html', '/kuroto.html') or (path.startswith('/transcripciones/') and target.suffix in ('.json','.js'))
        if not allowed or not target.is_relative_to(self.server.root) or not target.is_file():
            return self.respond(404, {'error': 'Recurso no disponible.'})
        self.send_response(200)
        self.send_header('Content-Type', {'.html':'text/html; charset=utf-8','.json':'application/json; charset=utf-8','.js':'text/javascript; charset=utf-8'}[target.suffix])
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(target.read_bytes())

    def do_POST(self):
        # JSON y origen propio evitan escrituras desde otras páginas.
        origin = self.headers.get('Origin')
        if origin and origin != 'http://' + self.headers.get('Host', ''):
            return self.respond(403, {'error': 'Origen no permitido.'})
        if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
            return self.respond(415, {'error': 'Se requiere JSON.'})
        try:
            length = int(self.headers.get('Content-Length', 0))
            if not 0 < length <= 15000000:
                raise ValueError()
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError()
        except (ValueError, UnicodeError):
            return self.respond(400, {'error': 'Solicitud no válida.'})
        path = urlsplit(self.path).path
        with self.server.lock:
            now = time.time()
            if path == '/api/editor/unlock':
                ip = self.client_address[0]
                attempts = [t for t in self.server.attempts.get(ip, []) if t > now - 60]
                self.server.attempts[ip] = attempts
                if len(attempts) >= 10:
                    return self.respond(429, {'error': 'Espera un minuto antes de volver a intentarlo.'})
                attempts.append(now)
                code = body.get('code')
                if not isinstance(code, str) or not hmac.compare_digest(hashlib.sha256(code.encode()).digest(), self.server.code_hash):
                    return self.respond(403, {'error': 'Código incorrecto.'})
                self.server.sessions = {k: v for k, v in self.server.sessions.items() if v > now}
                token = secrets.token_urlsafe(32)
                self.server.sessions[token] = now + 8 * 3600
                return self.respond(200, {'token': token})
            token = self.headers.get('Authorization', '').removeprefix('Bearer ')
            if self.server.sessions.get(token, 0) <= now:
                return self.respond(401, {'error': 'Introduce el código para activar la edición.'})
            if path == '/api/editor/lock':
                self.server.sessions.pop(token, None)
                return self.respond(200, {'ok': True})
            if path == '/api/editor/save-document':
                campaign = body.get('campaign')
                if not isinstance(campaign,str) or campaign not in self.server.original:
                    return self.respond(400, {'error':'Campaña desconocida.'})
                author, reason = body.get('author'), body.get('reason')
                if not all(isinstance(v,str) and v.strip() for v in (author,reason)) or len(author)>100 or len(reason)>1000:
                    return self.respond(400, {'error':'Escribe tu nombre y el motivo del cambio.'})
                history = self.documents(campaign)
                revision = history[-1]['revision'] if history else 0
                if body.get('revision') != revision:
                    return self.respond(409, {'error':'Otro jugador ha guardado cambios en esta campaña. Copia tu borrador, cierra y vuelve a abrir el editor para comparar.'})
                try:
                    content = validate(body.get('content'), self.server.original[campaign])
                except (ValueError,TypeError,KeyError,RecursionError) as error:
                    return self.respond(400, {'error':str(error) or 'Contenido no válido.'})
                self.server.db.execute('INSERT INTO documents (campaign,content,author,reason,created) VALUES (?,?,?,?,?)',(campaign,json.dumps(content,ensure_ascii=False),author.strip(),reason.strip(),now))
                self.server.db.commit()
                return self.respond(200, {'ok':True})
            if path != '/api/editor/save':
                return self.respond(404, {'error': 'Ruta no disponible.'})
            if isinstance(body.get('campaign'),str) and self.documents(body['campaign']):
                return self.respond(409, {'error':'Esta campaña ya utiliza el editor completo. Recarga la página antes de editar.'})
            key = tuple(body.get(k) for k in ('campaign', 'kind', 'identity', 'field'))
            if not all(isinstance(k, str) for k in key) or key not in self.server.fields:
                return self.respond(400, {'error': 'Campo no editable.'})
            value, author, reason = (body.get(k) for k in ('value', 'author', 'reason'))
            if not all(isinstance(v, str) and v.strip() for v in (value, author, reason)) or len(value) > 100000 or len(author) > 100 or len(reason) > 1000:
                return self.respond(400, {'error': 'Completa el texto, tu nombre y el motivo con las longitudes permitidas.'})
            previous = self.server.db.execute('SELECT revision FROM edits WHERE campaign=? AND kind=? AND identity=? AND field=? ORDER BY revision DESC LIMIT 1', key).fetchone()
            revision = previous[0] if previous else 0
            if body.get('revision') != revision:
                return self.respond(409, {'error': 'Otro jugador ha cambiado este campo. Copia tu borrador, cierra y vuelve a abrir la edición para comparar.'})
            self.server.db.execute('INSERT INTO edits (campaign,kind,identity,field,value,author,reason,created) VALUES (?,?,?,?,?,?,?,?)', (*key, value, author.strip(), reason.strip(), now))
            self.server.db.commit()
            return self.respond(200, {'edits': self.rows()})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    code = os.environ.get('ARGHAST_EDIT_CODE')
    if not code:
        parser.error('Define ARGHAST_EDIT_CODE con el código compartido antes de iniciar.')
    state = ROOT / '.local/edicion'
    state.mkdir(parents=True, exist_ok=True)
    server = ArchiveServer(('127.0.0.1', args.port), ROOT, state / 'correcciones.sqlite3', code)
    print(f'Archivo editable local: http://127.0.0.1:{args.port}/', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        server.db.close()


if __name__ == '__main__':
    main()
