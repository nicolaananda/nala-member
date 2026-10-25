import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {readFile} from 'node:fs/promises';

const files=['src/pages/admin.astro','src/pages/admin/operasional.astro'];
const current=await Promise.all(files.map(file=>readFile(new URL(`../${file}`,import.meta.url),'utf8')));
const baseline=files.map(file=>execFileSync('git',['show',`origin/main:${file}`],{encoding:'utf8'}));
const endpoints=s=>new Set(s.match(/\/api\/[A-Za-z0-9_?=&${}./:-]+/g)||[]);
for(let i=0;i<files.length;i++) for(const endpoint of endpoints(baseline[i])) assert(endpoints(current[i]).has(endpoint),`${files[i]} lost endpoint ${endpoint}`);
const joined=current.join('\n'),css=await readFile(new URL('../src/styles.css',import.meta.url),'utf8');
for(const token of ['<details class="admin-menu">','aria-label="Buka menu navigasi"','role="status"','aria-live="polite"','role="tablist"','<dialog']) assert(joined.includes(token),`Missing structure/a11y token: ${token}`);
for(const token of ['min-height:44px','@media(max-width:799px)','@media(max-width:600px)','@media(max-width:380px)','overflow-x:hidden']) assert(css.includes(token),`Missing responsive rule: ${token}`);
const editorial=css.slice(css.indexOf('/* Admin editorial system'),css.indexOf('/* Artstudio Nala parent theme'));
assert(!editorial.includes('linear-gradient('),'Editorial admin system must not use generic gradients');
console.log(`PASS admin structure, ${[...endpoints(baseline.join('\n'))].length} endpoint patterns, a11y, responsive selectors`);
