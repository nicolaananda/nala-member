import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
const [portal, admin, css] = await Promise.all(['src/pages/portal.astro', 'src/pages/admin.astro', 'src/styles.css'].map(path => readFile(path, 'utf8')));
const source = portal + admin + css;
for (const marker of ['Beginner', 'Intermediate', 'Advanced', 'Pilih Kelas', 'member-home-head', 'course-price', 'lesson-upload', '/api/admin/member-program/artworks', 'Terbitkan evaluasi', 'prefers-reduced-motion']) assert.ok(source.includes(marker), `missing ${marker}`);
assert.ok(!portal.includes("String(c.learningLevel||'').toLowerCase()===selectedLevel.toLowerCase()"), 'level choice must not hide purchasable courses');
console.log('member dashboard source assertions: 10 passed');
