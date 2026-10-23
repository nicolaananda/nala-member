import json
from playwright.sync_api import sync_playwright
from pathlib import Path

with sync_playwright() as p:
    browser=p.chromium.launch()
    for width in [1440,360]:
        page=browser.new_page(viewport={'width':width,'height':900})
        errors=[]; saves=[]; notes={'note':'Catatan tersimpan','bookmarked':True}
        page.on('pageerror',lambda e:errors.append(str(e)))
        lesson={'id':9,'title':'Materi pertama','description':'Latihan','worksheets':[],'progress':{'position':42,'duration':100,'completed':False}}
        course={'id':7,'title':'Kelas QA','accessible':True,'chapters':[{'title':'Bab','lessons':[lesson,{'id':10,'title':'Materi kedua','worksheets':[]}]}]}
        def route(r):
            path=r.request.url.split('/api/member')[-1]
            data={}
            if path=='/checkout-capability':data={'enabled':False,'plans':[]}
            elif path=='/me':data={'member':{'id':1,'name':'QA','email':'qa@example.test'}}
            elif path=='/catalog':data={'courses':[course],'active':True}
            elif path=='/dashboard':data={'continueLearning':[]}
            elif path=='/program/notifications':data={'notifications':[]}
            elif path.startswith('/notes/'):
                if r.request.method=='PUT':notes.update(r.request.post_data_json);saves.append(path)
                data=notes
            elif path.startswith('/progress/'):
                saves.append(path);data={'success':True}
            elif path.startswith('/program/'):
                data={'flags':{},'artworks':[],'courses':[]}
            r.fulfill(content_type='application/json',body=json.dumps(data))
        page.route('https://api.artstudionala.com/**',route)
        page.goto('http://127.0.0.1:41739/portal/')
        page.locator('#dashboard-view').wait_for(state='visible')
        page.get_by_role('button',name='Buka kelas',exact=True).click()
        page.get_by_label('Catatan privat').wait_for()
        page.wait_for_function("document.querySelector('.lesson-notes textarea').value==='Catatan tersimpan'")
        page.get_by_label('Catatan privat').fill('Catatan baru')
        page.get_by_role('button',name='Simpan catatan',exact=True).click()
        page.wait_for_function("document.querySelector('#notice').textContent.includes('Catatan privat tersimpan')")
        assert notes['note']=='Catatan baru' and '/notes/9' in saves
        page.get_by_role('button',name='Materi berikutnya →',exact=True).click()
        assert page.locator('#lesson-content h2').inner_text()=='Materi kedua'
        page.get_by_role('button',name='← Sebelumnya',exact=True).click()
        page.get_by_role('button',name='Tandai materi selesai',exact=True).click()
        page.wait_for_function("document.querySelector('#lesson-content button').textContent.includes('Materi selesai')")
        assert '/progress/9' in saves
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),width
        assert not errors,errors
        Path('/tmp/nala-qa').mkdir(exist_ok=True)
        page.screenshot(path=f'/tmp/nala-qa/learning-{width}.png',full_page=True)
        page.close()
    browser.close()
print('PASS desktop/mobile notes, resume selection, next/previous, completion, overflow and JS errors (API fixtures)')
