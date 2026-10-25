import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';

const pages = [
  'src/pages/index.astro', 'src/pages/portal.astro', 'src/pages/galeri.astro',
  'src/pages/verifikasi.astro', 'src/pages/reset-password.astro', 'src/pages/admin.astro',
  'src/pages/admin/operasional.astro', 'src/pages/admin/pengajar.astro',
  'src/pages/admin/kursus/edit.astro', 'src/pages/admin/materi/edit.astro',
  'src/pages/admin/produk/edit.astro', 'public/admin-editor.js'
];
const endpointPattern = /(?:\/api\/[A-Za-z0-9_?=&/${}.:'`+-]+|req(?:uest)?\(\s*[`'"][^`'"]+|fetch\(\s*[`'"][^`'"]+)/g;
const actionPattern = /(?:method\s*:\s*['"](?:POST|PUT|PATCH|DELETE)['"]|\.onsubmit\s*=|addEventListener\(\s*['"]submit['"])/g;
const extract = (source, pattern) => [...source.matchAll(pattern)].map(x => x[0]).sort();
let endpointCount = 0, actionCount = 0;
for (const file of pages) {
  const current = readFileSync(file, 'utf8');
  const baseline = execFileSync('git', ['show', `origin/main:${file}`], { encoding: 'utf8' });
  const oldEndpoints = extract(baseline, endpointPattern), newEndpoints = extract(current, endpointPattern);
  const oldActions = extract(baseline, actionPattern), newActions = extract(current, actionPattern);
  for (const endpoint of oldEndpoints) if (!(file==='src/pages/admin.astro'&&endpoint.includes('/api/admin/login'))) assert(newEndpoints.includes(endpoint), `${file}: endpoint hilang: ${endpoint}`);
  const removedUnifiedLogins=file==='src/pages/admin.astro'?2:0;
  assert(newActions.length >= oldActions.length-removedUnifiedLogins, `${file}: action berkurang ${oldActions.length} → ${newActions.length}`);
  if (file.endsWith('.astro')) {
    assert.match(current, /<html lang="id">/, `${file}: bahasa dokumen wajib ada`);
    assert.match(current, /<meta name="viewport"/, `${file}: viewport wajib ada`);
    assert.match(current, /<(main|body)[ >]/, `${file}: struktur halaman tidak valid`);
  }
  endpointCount += oldEndpoints.length;
  actionCount += oldActions.length;
}
const css = readFileSync('src/styles.css', 'utf8');
for (const width of ['360', '430', '600', '799']) assert(css.includes(width), `Selector responsif ${width}px tidak ditemukan`);
assert.match(css, /min-height:44px/, 'Target sentuh 44px tidak ditemukan');
assert.match(css, /:focus-visible/, 'Focus keyboard tidak ditemukan');
assert.match(css, /prefers-reduced-motion/, 'Reduced motion tidak ditemukan');
assert.match(css, /overflow-x:hidden/, 'Proteksi overflow horizontal tidak ditemukan');
console.log(`UI contract OK: ${pages.length - 1} halaman, ${endpointCount} pola endpoint, ${actionCount} action dipertahankan.`);
