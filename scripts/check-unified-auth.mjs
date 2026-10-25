import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

const read=path=>readFile(new URL(path,import.meta.url),'utf8');
const [login,portal,admin,index]=await Promise.all([
  read('../src/pages/login.astro'),read('../src/pages/portal.astro'),
  read('../src/pages/admin.astro'),read('../src/pages/index.astro')
]);
assert.match(login,/fetch\(API\+path,\{credentials:'include'/);
assert.match(login,/call\('\/api\/auth\/login',\{method:'POST'/);
assert.match(login,/new Set\(\['\/portal','\/admin\/','\/admin\/\?view=evaluations'\]\)/);
assert.match(login,/\['\/api\/admin\/me','admin'\],\['\/api\/member\/me','learner'\]/);
assert.doesNotMatch(admin,/id="login-form"/);
assert.match(admin,/location\.replace\('\/login\?next='/);
assert.match(portal,/location\.replace\('\/login\?next=%2Fportal'\)/);
assert.match(index,/href="\/login"/);
console.log('PASS unified authentication entry, probes, and redirects');