import {createRequire} from 'node:module';
import assert from 'node:assert/strict';
// Run with PLAYWRIGHT_PACKAGE pointing to an installed playwright/package.json.
const require=createRequire(process.env.PLAYWRIGHT_PACKAGE||import.meta.url);
const {chromium}=require('playwright');
const browser=await chromium.launch({headless:true});
const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
const course={id:1,title:'Crayon Ceria',description:'Belajar warna',accessible:true,chapters:[{title:'Mulai',lessons:[{id:11,title:'Warna dasar',worksheets:[]},{id:12,title:'Bentuk',worksheets:[]}]}],progress_percent:30,completed_count:1,material_count:2};
const rewards=[{id:1,name:'Squishy',point_cost:50,stock:3,active:true},{id:2,name:'Crayon',point_cost:150,stock:2,active:true}];let redeem=0;
await page.route('**/api/**',async route=>{const path=new URL(route.request().url()).pathname;let x={};
if(path.endsWith('/checkout-capability'))x={enabled:true,plans:[{id:1,name:'Beginner',price:15000,durationDays:30,accessMode:'selected',courses:[{id:1,title:'Crayon Ceria'}]}]};
else if(path==='/api/admin/me')x={admin:{role:'owner',email:'fixture@example.test'}};
else if(path.endsWith('/me'))x={member:{name:'Fixture',email:'fixture@example.test',learning_level:'beginner'}};
else if(path.endsWith('/catalog'))x={courses:[course],active:true};
else if(path.endsWith('/dashboard'))x={courses:[course],overall_progress:30,point_balance:100,reminders:[],latest_artwork:null};
else if(path.endsWith('/points'))x={balance:100,history:[]};
else if(path.endsWith('/rewards'))x={rewards};
else if(path.endsWith('/redemptions')){if(route.request().method()==='POST'){redeem++;x={success:true}}else x={redemptions:[{id:1,reward_name:'Squishy',point_cost:50,status:'requested',created_at:new Date().toISOString()}]}}
else if(path.endsWith('/notifications'))x={notifications:[]};
else if(path.endsWith('/notification-preferences'))x={preferences:{inApp:true,email:true,whatsapp:false}};
else if(path.endsWith('/artworks'))x={artworks:[],enabled:true};
else if(path.includes('/quizzes/'))return route.fulfill({status:404,json:{message:'Tidak ada kuis'}});
else if(path.includes('/notes/'))x={note:'',bookmarked:false};
else if(path.endsWith('/program/plans'))x={plans:[{id:1,name:'Beginner',price:15000,durationDays:30,accessMode:'selected',courses:[{title:'Crayon Ceria'}]}]};
else if(path.endsWith('/config'))x={plans:[],vouchers:[]};
else if(path.endsWith('/orders'))x={orders:[]};
else if(path.endsWith('/courses'))x={courses:[]};
await route.fulfill({json:x});});
await page.goto('http://127.0.0.1:4318/portal/');await page.locator('.dashboard-actions').waitFor();
await page.locator('[data-view=rewards]:visible').first().click();await page.getByText('Kurang 50 poin lagi',{exact:true}).waitFor();
page.on('dialog',d=>{assert.ok(d.message().includes('Saldo setelah penukaran: 50'));d.accept()});await page.getByRole('button',{name:'Tukar Squishy dengan 50 poin',exact:true}).click();await page.waitForTimeout(100);assert.equal(redeem,1);
for(const width of [360,390,768,1280]){await page.setViewportSize({width,height:900});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`member overflow ${width}`)}
await page.locator('[data-view=dashboard]:visible').first().click();await page.getByRole('button',{name:'Lanjutkan',exact:true}).click();await page.locator('.lesson-navigation').waitFor();await page.getByRole('button',{name:'Materi berikutnya →'}).click();await page.locator('#lesson-content h2').filter({hasText:'Bentuk'}).waitFor();
await page.locator('[data-view=dashboard]:visible').first().click();await page.getByRole('button',{name:'Lihat paket & perpanjang'}).click();
await page.getByRole('button',{name:'Beli QRIS',exact:true}).click();await page.locator('#checkout-summary').waitFor();assert.ok((await page.locator('#checkout-summary').innerText()).includes('Crayon Ceria'));await page.locator('#checkout-dialog button.close').first().click();
await page.goto('http://127.0.0.1:4318/admin/');await page.locator('[data-view=rewards]').click();await page.locator('#reward-list .ops-row').first().waitFor();await page.locator('#reward-search').fill('Crayon');await page.waitForTimeout(500);assert.equal(await page.locator('#reward-list .ops-row').count(),1);await page.locator('#reward-queue-tab').click();assert.ok(await page.locator('#reward-queue-panel').isVisible());assert.ok(await page.getByText('Diajukan',{exact:false}).count());
for(const width of [360,390,768,1280]){await page.setViewportSize({width,height:900});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`admin overflow ${width}`)}
assert.deepEqual(errors,[]);await browser.close();console.log('Fixture browser checks passed: redemption confirmation, points shortage, lesson navigation, admin tabs/search and 4 viewport widths; zero page errors.');
