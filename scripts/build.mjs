import { mkdir, copyFile, readdir, stat } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const root = fileURLToPath(new URL('../', import.meta.url));
const files = ['index.html', 'styles.css', 'domain.js', 'store.js', 'app.js'];
await mkdir(path.join(root, 'dist'), { recursive: true });
for (const name of files) {
  await copyFile(path.join(root, 'frontend', name), path.join(root, 'dist', name));
}
const assets = await readdir(path.join(root, 'dist'));
// The Sites packager adds its hosting metadata here after a successful build.
if (assets.some(name => !files.includes(name) && name !== '.openai')) throw new Error('Unexpected public asset in dist.');
const total = (await Promise.all(files.map(name => stat(path.join(root, 'dist', name)))))
  .reduce((sum, x) => sum + x.size, 0);
console.log(`Built ${files.length} static application assets (${total} bytes). No source interviews are public assets.`);
