import assert from 'node:assert/strict';
import fs from 'node:fs';
const member=fs.readFileSync('src/pages/portal.astro','utf8'),admin=fs.readFileSync('src/pages/admin.astro','utf8'),css=fs.readFileSync('src/styles.css','utf8');
for(const text of ['Kurang ${','Saldo setelah penukaran','checkout-summary','lesson-navigation','Coba lagi','dashboard-actions'])assert.ok(member.includes(text),text);
for(const text of ['reward-search','reward-status-filter','redemption-status-filter','reward-catalog-panel','reward-queue-panel','Lanjut ke karya berikutnya'])assert.ok(admin.includes(text),text);
assert.ok(css.includes('prefers-reduced-motion'));
assert.ok(css.includes(':focus-visible'));
console.log('Six-area UX contracts OK');
