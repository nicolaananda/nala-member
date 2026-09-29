import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
const [portal, admin, css] = await Promise.all(['src/pages/portal.astro', 'src/pages/admin.astro', 'src/styles.css'].map(path => readFile(path, 'utf8')));
const source = portal + admin + css;
for (const marker of ['Beginner', 'Intermediate', 'Advanced', 'Pilih kelas', 'lesson-upload', '/api/admin/member-program/artworks', 'Simpan feedback', 'prefers-reduced-motion']) assert.ok(source.includes(marker), `missing ${marker}`);
console.log('redesign source assertions: 8 passed');
