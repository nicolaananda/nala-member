from pathlib import Path
import json, re
from playwright.sync_api import sync_playwright

import os
BASE = os.environ.get("ADMIN_QA_URL", "http://127.0.0.1:41732/admin/")
OUT = Path("/root/.hermes/office_workers/artifacts/5d4d93726ab04c169984b648b23b5b03")
OUT.mkdir(parents=True, exist_ok=True)
plans = [{"id": 1, "name": "Studio Bulanan", "price": 150000, "duration_days": 30, "status": "active"}]
course = {"id": 7, "title": "Cat Air Dasar", "slug": "cat-air-dasar", "category": "Lukis", "image_url": "", "description": "Dasar cat air", "sort_order": 1, "status": "published", "chapters": [{"id": 8, "title": "Persiapan", "sortOrder": 1, "lessons": [{"id": 9, "title": "Alat", "youtubeVideoId": "dQw4w9WgXcQ", "description": "Pilih kuas", "sortOrder": 1, "isPreview": False, "worksheets": []}]}]}
orders = [
    {"order_id":"MEMBER-PENDING1","member_id":3,"member_name":"Nala","member_email":"nala@example.test","plan_name":"Studio Bulanan","amount":150000,"duration_days":30,"status":"pending","created_at":"2026-01-02T03:04:00Z","expires_at":"2026-01-03T03:04:00Z","paid_at":None,"archived_at":None},
    {"order_id":"MEMBER-PAID01","member_id":3,"member_name":"Nala","member_email":"nala@example.test","plan_name":"Studio Bulanan","amount":150000,"duration_days":30,"status":"paid","created_at":"2026-01-01T03:04:00Z","expires_at":None,"paid_at":"2026-01-01T03:10:00Z","archived_at":None}
]
requests = []

def body(req):
    try: return req.post_data_json
    except: return None

def run(viewport, shot):
    errors=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True, executable_path="/root/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome")
        page=browser.new_page(viewport=viewport)
        page.on("console", lambda m: errors.append(f"console {m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        def route(r):
            req=r.request; url=req.url; path=url.removeprefix("https://api.artstudionala.com")
            requests.append((req.method,path,body(req)))
            status=200; payload={"success":True}
            if path == "/api/admin/me": payload={"email":"admin@example.test"}
            elif path == "/api/admin/member-program/config": payload={"plans":plans}
            elif path.startswith("/api/admin/member/courses") and req.method == "GET": payload={"courses":[course]}
            elif path.startswith("/api/admin/member/orders?"):
                q=path.split("?",1)[1]
                assert "failed" not in q
                payload={"orders":orders,"total":25,"page":1,"limit":20}
            elif path.startswith("/api/admin/member/members?"): payload={"members":[{"id":3,"name":"Nala","email":"nala@example.test","membership_expires_at":"2026-03-01T03:04:00Z"}],"total":1,"page":1,"pageSize":50}
            elif path.startswith("/api/admin/member/members/3?"):
                payload={"account":{"id":3,"name":"Nala","email":"nala@example.test","membership_expires_at":"2026-03-01T03:04:00Z"},"orders":[orders[0]],"accessHistory":[{"source_type":"admin_grant","days_delta":7,"previous_expires_at":"2026-02-22T03:04:00Z","resulting_expires_at":"2026-03-01T03:04:00Z","reason":"Bonus","actor":"admin@example.test","created_at":"2026-01-02T03:04:00Z"}]}
            elif path == "/api/admin/member/lessons/9" and req.method == "PUT":
                if body(req)["title"] == "Gagal simpan": status,payload=500,{"message":"Fixture menolak simpan"}
                else:
                    course["chapters"][0]["lessons"][0].update({"title":body(req)["title"],"youtubeVideoId":body(req)["youtubeVideoId"],"description":body(req)["description"],"sortOrder":body(req)["sortOrder"],"isPreview":body(req)["isPreview"]})
            r.fulfill(status=status,content_type="application/json",body=json.dumps(payload))
        page.route("https://api.artstudionala.com/**",route)
        page.goto(BASE,wait_until="networkidle")
        if not page.locator("#app").is_visible(): raise AssertionError({"url":page.url,"errors":errors,"requests":requests[-5:],"html":page.locator("body").inner_text()[:500]})
        page.get_by_role("button",name="Kursus",exact=True).click(); page.get_by_role("button",name="Buka kursus").click()
        assert page.locator("details.material").count()==1 and not page.locator("details.material").get_attribute("open")
        page.locator("details.chapter > summary").click(); page.locator("details.material > summary").click()
        lesson=page.locator("details.material form"); lesson.locator('[name="title"]').fill("Gagal simpan"); lesson.locator('[name="youtube"]').fill("https://youtu.be/dQw4w9WgXcQ?t=2"); lesson.get_by_role("button",name="Simpan").click(); page.wait_for_timeout(100)
        assert lesson.locator('[name="title"]').input_value()=="Gagal simpan"
        lesson.locator('[name="title"]').fill("Alat baru"); lesson.get_by_role("button",name="Simpan").click(); page.wait_for_timeout(150)
        assert any(x[1]=="/api/admin/member/lessons/9" and x[2]["youtubeVideoId"]=="dQw4w9WgXcQ" for x in requests)
        assert page.get_by_text("Alat baru",exact=True).count()>=1
        page.get_by_role("button",name="Pesanan",exact=True).click(); page.get_by_label("Status pesanan").select_option("denied"); page.get_by_role("button",name="Terapkan").click(); page.wait_for_timeout(100)
        page.get_by_role("button",name="Detail").nth(1).click(); assert page.get_by_role("button",name="Batalkan & arsipkan").is_disabled(); page.locator("dialog[open] .icon.close").click()
        page.get_by_role("button",name="Detail").first.click(); assert page.get_by_role("button",name="Batalkan & arsipkan").is_enabled(); page.locator("dialog[open] .icon.close").click()
        page.get_by_role("button",name="Member",exact=True).click(); page.get_by_role("button",name="Detail").click(); page.locator("#member-detail").get_by_text("Riwayat akses").wait_for(); detail=page.locator("#member-detail").inner_text(); assert "Penambahan admin" in detail and "+7 hari" in detail, detail; assert page.get_by_role("button",name="Pesanan arsip").count()==1
        assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
        page.screenshot(path=str(OUT/shot),full_page=True)
        page.get_by_role("button",name="Produk",exact=True).click(); page.get_by_role("button",name="+ Tambah produk",exact=True).click(); page.get_by_label("Nama").fill("Rahasia"); page.locator("dialog[open] .icon.close").click(); page.locator("#plan-q").fill("private"); page.get_by_role("button",name="Keluar").click(); page.wait_for_timeout(100)
        assert page.locator("#app").is_hidden() and page.locator("#plan-q").input_value()=="" and page.locator("#plan-form [name=name]").input_value()=="" and page.locator("#order-detail").inner_text()=="" and page.locator("#order-title").inner_text()==""
        assert not [e for e in errors if e != 'console error: Failed to load resource: the server responded with a status of 500 (Internal Server Error)'], errors
        assert errors.count('console error: Failed to load resource: the server responded with a status of 500 (Internal Server Error)') == 1, errors
        browser.close()

run({"width":1440,"height":1000},"admin-desktop.png")
run({"width":360,"height":800},"admin-mobile-360.png")
print("Playwright intercepted fixture QA passed")
