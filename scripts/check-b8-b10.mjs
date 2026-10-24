import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const source=await readFile(new URL('../src/pages/portal.astro',import.meta.url),'utf8');
for(const feature of ['gallery','paths','badges','certs']){
  assert.match(source,new RegExp(`data-program="${feature}"`),`${feature} navigation missing`);
  assert.match(source,new RegExp(`name==='${feature}'`),`${feature} frontend handler missing`);
}
for(const route of ['/program/gallery','/program/learning-paths','/program/badges','/program/certificates'])assert.ok(source.includes(route),`${route} API integration missing`);
console.log('PASS B8-B10 member frontend routes');
