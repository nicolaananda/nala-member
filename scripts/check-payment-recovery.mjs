import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

const source=await readFile(new URL('../src/pages/portal.astro',import.meta.url),'utf8');
assert.match(source,/o\.status==='pending'.*Buat pembayaran baru/);
assert.match(source,/Jangan bayar pesanan lama dan pesanan baru sekaligus/);
assert.match(source,/pay\(plan\.id,fresh\)/);
console.log('pending payment recovery check passed');
