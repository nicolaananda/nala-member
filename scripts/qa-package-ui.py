from pathlib import Path
import json, os
from playwright.sync_api import sync_playwright
BASE=os.environ.get('QA_URL','http://127.0.0.1:43817')
OUT=Path('/root/.hermes/office_workers/artifacts/e92db1bdb9464cdd9e5e79428039152b');OUT.mkdir(parents=True,exist_ok=True)
courses=[{'id':'10','title':'Menggambar Dasar','slug':'menggambar-dasar','category':'Gambar','image_url':'','description':'Dasar','sort_order':1,'status':'published','accessible':True,'chapters':[{'id':'20','title':'Awal','sortOrder':1,'lessons':[{'id':'30','title':'Garis','description':'Latihan','youtubeVideoId':'dQw4w9WgXcQ','sortOrder':1,'isPreview':False,'worksheets':[]}]}]},{'id':'11','title':'Crayon','slug':'crayon','category':'Warna','image_url':'','description':'Warna','sort_order':2,'status':'draft','accessible':False,'chapters':[]}]
plans=[{'id':'1','name':'Paket A','price':30000,'duration_days':30,'status':'active','access_mode':'selected','courses':[{'id':'10','title':'Menggambar Dasar','slug':'menggambar-dasar','status':'published'}]}]
requests=[]
auth={'ok':True}
def handler(route):
 req=route.request; u=req.url
 if not u.startswith('https://api.artstudionala.com/'):
  route.abort();return
 path=u.removeprefix('https://api.artstudionalala.com') if False else u.removeprefix('https://api.artstudionala.com')
 payload={'success':True};status=200
 if path=='/api/admin/me':
  if auth['ok']:payload={'admin':{'email':'admin@test'}}
  else:status,payload=401,{'message':'Sesi berakhir'}
 elif path=='/api/admin/member-program/config':payload={'plans':plans,'flags':[],'vouchers':[]}
 elif path=='/api/admin/member/courses':payload={'courses':courses}
 elif path.startswith('/api/admin/member-program/plans/') and req.method=='PUT':
  body=req.post_data_json;requests.append(body)
  if body['name']=='Gagal':status,payload=500,{'message':'Fixture gagal'}
 elif path=='/api/admin/logout':status,payload=401,{'message':'Keluar'}
 else:
  raise AssertionError('Unexpected API '+req.method+' '+path)
 route.fulfill(status=status,content_type='application/json',body=json.dumps(payload))
def run(width,shot):
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True,executable_path='/root/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome');page=b.new_page(viewport={'width':width,'height':800});page.route('**/*',lambda r: handler(r) if r.request.url.startswith('https://api.artstudionala.com/') else r.continue_())
  page.goto(BASE+'/admin/produk/edit/?id=1');page.get_by_text('Edit produk',exact=True).wait_for();assert page.get_by_label('Menggambar Dasar · Terbit').is_checked();page.get_by_label('Crayon · Draft — pembeli belum dapat membuka').check();page.get_by_label('Nama').fill('Gagal');page.get_by_role('button',name='Simpan produk').click();page.get_by_text('Fixture gagal').wait_for();assert page.get_by_label('Nama').input_value()=='Gagal';page.get_by_label('Nama').fill('Paket AB');page.get_by_role('button',name='Simpan produk').click();page.get_by_text('Produk disimpan.').wait_for();assert requests[-1]['accessMode']=='selected' and requests[-1]['courseIds']==['10','11']
  page.goto(BASE+'/admin/produk/edit/?id=new');page.get_by_text('Tambah produk',exact=True).wait_for();page.get_by_label('Nama').fill('Kosong');page.get_by_label('Harga (IDR)').fill('100');page.get_by_label('Durasi hari').fill('1');page.get_by_role('button',name='Simpan produk').click();page.get_by_text('Pilih minimal satu kursus.').wait_for()
  page.goto(BASE+'/admin/produk/edit/?id=999');page.locator('#state').get_by_text('Produk tidak ditemukan.').wait_for();page.reload();page.locator('#state').get_by_text('Produk tidak ditemukan.').wait_for()
  page.goto(BASE+'/admin/kursus/edit/?id=10');page.get_by_text('Edit kursus',exact=True).wait_for();page.get_by_role('link',name='Garis',exact=True).click();assert '/admin/materi/edit/' in page.url;page.get_by_text('Edit materi',exact=True).wait_for();page.get_by_role('link',name='Menggambar Dasar').click();assert 'id=10' in page.url
  overflow=page.evaluate("({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,widest:[...document.querySelectorAll('*')].map(e=>({tag:e.tagName,cls:e.className||'',right:e.getBoundingClientRect().right})).sort((a,b)=>b.right-a.right)[0]})")
  assert overflow['sw']<=overflow['cw'],overflow;page.screenshot(path=str(OUT/shot),full_page=True)
  page.goto(BASE+'/admin/produk/edit/?id=1');page.get_by_text('Edit produk',exact=True).wait_for();auth['ok']=False;page.reload();page.get_by_text('Sesi berakhir. Masuk kembali dari halaman admin.').wait_for();assert page.locator('#editor').is_hidden();auth['ok']=True;b.close()
run(1440,'package-editor-desktop.png');run(360,'package-editor-mobile.png');print('QA package UI passed')
