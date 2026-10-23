"""Built UI + real isolated Express/PostgreSQL; transport rewrites only, no API fixtures."""
import json, time, os
from pathlib import Path
from playwright.sync_api import sync_playwright
access=json.loads(Path('/tmp/nala-lms-preview-access.json').read_text());BASE=os.environ.get('LMS_QA_URL','http://127.0.0.1:41739');API=BASE if os.environ.get('LMS_QA_URL') else access['api']
with sync_playwright() as p:
 browser=p.chromium.launch()
 for width in [360,1440]:
  tag=str(width)+'-'+str(time.time_ns())
  context=browser.new_context(viewport={'width':width,'height':900});page=context.new_page();errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
  def forward(route):
   request=route.request
   response=context.request.fetch(API+request.url.split('artstudionala.com',1)[1],method=request.method,headers={'Origin':BASE,'Content-Type':'application/json'},data=request.post_data,fail_on_status_code=False)
   route.fulfill(response=response)
  if not os.environ.get('LMS_QA_URL'):page.route('https://api.artstudionala.com/**',forward)
  def api(path,method='GET',data=None):
   return context.request.fetch(API+path,method=method,headers={'Origin':BASE},data=data)
  assert api('/api/admin/login','POST',{'email':'owner@example.test','password':access['password']}).status==200
  page.goto(BASE+'/admin/kursus/edit/?id=new');page.locator('#editor-form [name=title]').fill('Integrated '+tag);page.locator('[name=slug]').fill('integrated-'+tag);page.locator('[name=status]').select_option('published');page.locator('#editor-form button[type=submit],#editor-form button:not([type])').last.click();page.wait_for_url('**/admin/kursus/edit/?id=*');page.locator('#editor-title').get_by_text('Edit kursus').wait_for()
  chapter=page.locator('#lesson-links form').last;chapter.locator('[name=title]').fill('Bab integrasi');chapter.get_by_role('button',name='Tambah bab').click();page.get_by_role('link',name='+ Materi',exact=True).click();page.wait_for_url('**lesson=new*');page.locator('#editor-form [name=title]').fill('Materi integrasi');page.locator('[name=youtube]').fill('https://youtu.be/dQw4w9WgXcQ');page.locator('#editor-form button[type=submit],#editor-form button:not([type])').last.click();page.wait_for_function("!location.search.includes('lesson=new')")
  page.locator('#editor-title').get_by_text('Edit materi').wait_for();page.locator('#worksheet-file').set_input_files({'name':'integrasi.pdf','mimeType':'application/pdf','buffer':b'%PDF-1.4 isolated fixture'});page.get_by_role('link',name='integrasi',exact=True).wait_for()
  courses=api('/api/admin/member/courses').json()['courses'];course=next(c for c in courses if c['slug']=='integrated-'+tag);lesson=course['chapters'][0]['lessons'][0];assert lesson['worksheets']
  teacher='teacher'+str(width)+'@example.test'
  assert api('/api/admin/member/teachers','PUT',{'email':teacher,'password':access['password'],'enabled':True,'courses':[course['id']]}).status==200
  assert api('/api/admin/member-program/flags/artwork','PUT',{'enabled':True}).status==200
  assert api('/api/admin/logout-all','POST',{}).status==200
  assert api('/api/admin/me').status==401
  assert api('/api/admin/login','POST',{'email':teacher,'password':access['password']}).status==200
  assert len(api('/api/admin/member/courses').json()['courses'])==1
  assert api('/api/admin/member/members').status==403
  assert api('/api/admin/member-program/config').status==403
  page.goto(BASE+'/admin/');page.get_by_text('Integrated '+tag,exact=True).first.wait_for()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert api('/api/member/login','POST',{'email':'learner@example.test','password':access['password']}).status==200
  import base64, io
  from PIL import Image
  image=io.BytesIO();Image.new('RGB',(2,2),'red').save(image,format='PNG')
  uploaded=api('/api/member/program/artworks','POST',{'courseId':course['id'],'lessonId':lesson['id'],'title':'Integrasi evaluasi','base64':base64.b64encode(image.getvalue()).decode()});assert uploaded.status==201,uploaded.text()
  page.goto(BASE+'/admin/');page.locator('#courses-view').wait_for(state='visible');page.locator('[data-view=evaluations]').click();page.get_by_label('Nilai (0–100)').fill('88');page.get_by_label('Masukan untuk murid').fill('Warna bagus, lanjutkan latihan');page.get_by_role('button',name='Terbitkan evaluasi').click();page.get_by_text('Evaluasi tersimpan. Murid menerima notifikasi di portal.').wait_for()
  works=api('/api/member/program/artworks').json()['artworks'];assert next(a for a in works if a['id']==uploaded.json()['artwork']['id'])['score']==88

  page.goto(BASE+'/portal/');page.locator('#dashboard-view').wait_for(state='visible');page.locator('[data-view=catalog]').click();page.locator('#search').fill('Integrated '+tag);page.get_by_role('button',name='Buka kelas',exact=True).click();page.get_by_label('Catatan privat').fill('Catatan integrasi');page.get_by_role('button',name='Simpan catatan',exact=True).click();page.wait_for_function("document.querySelector('#notice').textContent.includes('Catatan privat tersimpan')");page.get_by_role('button',name='Tandai materi selesai',exact=True).click();page.wait_for_function("document.querySelector('#lesson-content button').textContent.includes('Materi selesai')");assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not errors,errors
  page.screenshot(path='/tmp/nala-lms-integrated-'+str(width)+'.png',full_page=True)
  context.close()
 browser.close()
print('PASS actual PostgreSQL authoring, PDF, teacher provisioning/login/scope, durable logout, learner login; desktop/mobile')
