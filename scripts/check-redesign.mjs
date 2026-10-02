import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
const [portal, admin, css] = await Promise.all(['src/pages/portal.astro', 'src/pages/admin.astro', 'src/styles.css'].map(path => readFile(path, 'utf8')));
const source = portal + admin + css;
for (const marker of ['Beginner', 'Intermediate', 'Advanced', 'Pilih Kelas', 'member-home-head', 'course-price', 'lesson-upload', '/api/admin/member-program/artworks', 'Terbitkan evaluasi', 'prefers-reduced-motion']) assert.ok(source.includes(marker), `missing ${marker}`);
assert.ok(!portal.includes("String(c.learningLevel||'').toLowerCase()===selectedLevel.toLowerCase()"), 'level choice must not hide purchasable courses');
for (const marker of ['id="checkout-dialog"', 'Kode voucher (opsional)', "'/program/vouchers/redeem'", "if(!code)return pay(planId,button)"]) assert.ok(portal.includes(marker), `missing checkout voucher step: ${marker}`);
for (const marker of ["e.status===401", "['dashboard','account','orders','program']", "b.disabled=!currentCourse?.accessible", "Alamat pembayaran tidak aman", "await loadSnap();const x=await req('/orders'", "await loadOrders();say('Selesaikan QRIS"]) assert.ok(portal.includes(marker), `missing portal hardening: ${marker}`);
console.log('member dashboard source assertions: 20 passed');
