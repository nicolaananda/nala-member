import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [360,1440]:
  page=b.new_page(viewport={'width':width,'height':900}); errors=[];calls=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   path=r.request.url.split('/api/admin')[-1];calls.append(path)
   if path=='/me':data={'admin':{'email':'teacher@example.test','role':'teacher'}}
   elif path=='/member/courses':data={'courses':[]}
   elif path=='/member-program/artworks':data={'artworks':[]}
   else:raise AssertionError('Forbidden teacher API requested: '+path)
   r.fulfill(content_type='application/json',body=json.dumps(data))
  page.route('https://api.artstudionala.com/**',route)
  page.goto('http://127.0.0.1:41739/admin/')
  page.locator('#courses-view').wait_for(state='visible')
  assert page.locator('[data-view=orders]').is_hidden()
  assert page.locator('[data-view=members]').is_hidden()
  assert page.locator('.admin-summary').is_hidden()
  page.locator('[data-view=evaluations]').click();page.get_by_text('Belum ada karya untuk dievaluasi.').wait_for()
  assert not errors,errors
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.close()
 b.close()
print('PASS teacher browser routing desktop/mobile, no financial API calls')
