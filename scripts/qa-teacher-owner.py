import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [360,1440]:
  page=b.new_page(viewport={'width':width,'height':900});errors=[];saved=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   path=r.request.url.split('/api/admin')[-1]
   if path=='/me':data={'admin':{'role':'owner'}}
   elif path=='/member/courses':data={'courses':[{'id':7,'title':'Kelas QA'}]}
   elif path=='/member/teachers':
    if r.request.method=='PUT':saved.append(r.request.post_data_json);data={'success':True}
    else:data={'teachers':[]}
   else:raise AssertionError(path)
   r.fulfill(content_type='application/json',body=json.dumps(data))
  page.route('https://api.artstudionala.com/**',route)
  page.goto('http://127.0.0.1:41739/admin/pengajar/')
  page.get_by_label('Email',exact=True).fill('teacher@example.test')
  page.locator('[name=password]').fill('test-teacher-password')
  page.get_by_label('Kelas QA').check()
  page.get_by_role('button',name='Simpan pengajar').click()
  page.wait_for_function("document.querySelector('#status').textContent.includes('Tersimpan')")
  assert saved[0]['courses']==['7']
  assert page.locator('[name=password]').input_value()==''
  assert not errors,errors
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.close()
 b.close()
print('PASS owner teacher management desktop/mobile (fixture API)')
