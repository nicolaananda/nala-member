"""Run against built loopback site; intercept all API writes with in-memory fixtures."""
import os, json
from playwright.sync_api import sync_playwright
BASE=os.environ.get('QA_URL','http://127.0.0.1:43818')
for width in [1440,360]:
 courses=[]; calls=[]; errors=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/root/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome',headless=True)
  page=browser.new_page(viewport={'width':width,'height':900}); page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
  def handler(route):
   r=route.request;path=r.url.split('artstudionala.com',1)[1];method=r.method;body=r.post_data_json if method in ['POST','PUT'] else {};calls.append((method,path,body));out={'success':True}
   if path=='/api/admin/me':out={'admin':{'email':'fixture@example.test'}}
   elif path=='/api/admin/member/courses' and method=='GET':out={'courses':courses}
   elif path=='/api/admin/member/courses' and method=='POST':
    c={**body,'id':'51','image_url':body['imageUrl'],'sort_order':body['sortOrder'],'chapters':[]};courses.append(c);out={'course':c}
   elif path=='/api/admin/member/chapters' and method=='POST':
    ch={'id':'61','title':body['title'],'sortOrder':body['sortOrder'],'lessons':[]};courses[0]['chapters'].append(ch);out={'item':ch}
   elif path=='/api/admin/member/lessons' and method=='POST':
    lesson={**body,'id':'71','worksheets':[]};courses[0]['chapters'][0]['lessons'].append(lesson);out={'item':lesson}
   elif path=='/api/admin/member/worksheets' and method=='POST':courses[0]['chapters'][0]['lessons'][0]['worksheets'].append({'id':'81','title':body['title']})
   elif path=='/api/admin/member/worksheets/81' and method=='DELETE':courses[0]['chapters'][0]['lessons'][0]['worksheets']=[]
   elif path=='/api/admin/member/lessons/71' and method=='DELETE':courses[0]['chapters'][0]['lessons']=[]
   else:errors.append('Unexpected '+method+' '+path);route.abort();return
   route.fulfill(status=200,content_type='application/json',body=json.dumps(out))
  page.route('https://api.artstudionala.com/**',handler)
  page.goto(BASE+'/admin/kursus/edit/?id=new');page.locator('#editor-form [name=title]').fill('Kursus fixture');page.locator('[name=slug]').fill('kursus-fixture');page.locator('#editor-form button[type=submit],#editor-form button:not([type])').last.click();page.wait_for_url('**/admin/kursus/edit/?id=51');page.locator('#editor-title').get_by_text('Edit kursus').wait_for()
  chapter=page.locator('#lesson-links form').last;chapter.locator('[name=title]').fill('Bab fixture');chapter.get_by_role('button',name='Tambah bab').click();page.get_by_role('link',name='+ Materi',exact=True).click();page.wait_for_url('**lesson=new*');page.locator('#editor-form [name=title]').fill('Video fixture');page.locator('[name=youtube]').fill('https://youtu.be/dQw4w9WgXcQ');page.locator('#editor-form button[type=submit],#editor-form button:not([type])').last.click();page.wait_for_url('**lesson=71');page.locator('#worksheet-file').set_input_files({'name':'latihan.pdf','mimeType':'application/pdf','buffer':b'%PDF-1.4 fixture'});page.get_by_role('link',name='latihan',exact=True).wait_for();assert calls[-2][0] in ['POST','GET']
  page.get_by_role('button',name='Hapus PDF',exact=True).click();page.get_by_role('link',name='latihan',exact=True).wait_for(state='detached');assert page.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth');page.locator('#delete-lesson').click();page.wait_for_url('**/admin/kursus/edit/?id=51');assert courses[0]['chapters'][0]['lessons']==[];assert not errors,errors;browser.close()
print('Create course -> chapter -> lesson -> upload/delete PDF -> delete lesson: PASS desktop/mobile (intercepted fixtures)')
