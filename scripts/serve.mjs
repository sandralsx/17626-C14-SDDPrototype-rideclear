import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const root = fileURLToPath(new URL('../frontend/', import.meta.url));
const port = Number(process.env.PORT || 4173);
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
const allowed = new Set(['index.html', 'styles.css', 'domain.js', 'store.js', 'app.js']);
const server = http.createServer(async (request, response) => {
  const name = new URL(request.url, 'http://localhost').pathname.slice(1) || 'index.html';
  if (!allowed.has(name)) { response.writeHead(404); response.end('Not found'); return; }
  try {
    const data = await readFile(path.join(root, name));
    response.writeHead(200, { 'Content-Type': `${types[path.extname(name)]}; charset=utf-8`, 'Cache-Control': 'no-store' });
    response.end(data);
  } catch { response.writeHead(500); response.end('Unable to read application asset'); }
});
server.listen(port, '127.0.0.1', () => console.log(`RideClear V2: http://127.0.0.1:${port}`));
