"""Run from any location: python scripts/audit_v07.py (requires playwright and chromium)."""
from pathlib import Path
from bs4 import BeautifulSoup
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import threading, json, zipfile, subprocess, hashlib, xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
issues=[]; refs=0
pages=sorted(root.rglob('index.html'))
for f in pages:
    s=BeautifulSoup(f.read_text(encoding='utf8'),'html.parser')
    if len(s.select('main h1'))!=1: issues.append(f'{f.relative_to(root)} bad h1 count')
    for tag in s.select('[href], [src]'):
        href=tag.get('href') or tag.get('src')
        if not href or href.startswith(('https:','http:','mailto:','tel:','data:','javascript:')): continue
        uri,_,fragment=href.partition('#')
        target=(f.parent/uri.split('?')[0]).resolve() if uri else f
        if target.is_dir():target/='index.html'
        if not target.exists(): issues.append(f'BROKEN {f.relative_to(root)}: {href}')
        if fragment and target.exists() and target.suffix=='.html':
            to_soup=BeautifulSoup(target.read_text(encoding='utf8'),'html.parser')
            if not to_soup.find(id=fragment):issues.append(f'BROKEN ANCHOR {f.relative_to(root)}: {href}')
        refs+=1
    for img in s.find_all('img'):
        if img.get('alt') is None:issues.append(f'NO ALT {f.relative_to(root)}')
for f in root.glob('files/*.epub'):
    with zipfile.ZipFile(f) as z:
        if z.testzip():issues.append('Corrupt EPUB '+f.name)
try:
    ET.parse(root/'sitemap.xml')
except Exception as e: issues.append('Sitemap not XML: '+str(e))
for p in ['assets/site.js','assets/reflect.js','assets/forms-config.js']:
    result=subprocess.run(['node','--check',str(root/p)],capture_output=True,text=True)
    if result.returncode:issues.append('JS '+p+' '+result.stderr)
assert (root/'assets/forms-config.js').read_text().count('fellowshipEndpoint')==1
assert len(pages)==33,len(pages)
assert len(list((root/'read').glob('*/index.html')))==24
report={'website_version':'0.7','html_pages':len(pages),'local_links_and_assets_checked':refs,'issues':issues,'browser_test':'not attempted','browser_screenshots':[],'live_form_submissions_tested':False,'production_deployment_checked':False}

class Quiet(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(root),**kw)
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Quiet)
threading.Thread(target=server.serve_forever,daemon=True).start()
origin=f'http://127.0.0.1:{server.server_port}'
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
        report['browser_test']='started'
        for label,w,h in [('desktop',1440,900),('tablet',820,1000),('mobile',390,844)]:
            page=browser.new_page(viewport={'width':w,'height':h},accept_downloads=True)
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            for segment in ['community/','reflect/','focus/','downloads/','']:
                page.goto(origin+'/'+segment,wait_until='domcontentloaded',timeout=15000)
                page.wait_for_timeout(150)
                overflow=page.evaluate('document.documentElement.scrollWidth-window.innerWidth')
                if overflow>3:issues.append(f'{label} overflow {segment}: {overflow}px')
                if errors:issues+=['JS '+label+': '+x for x in errors];errors.clear()
                if segment in ['community/','reflect/','focus/'] and label in ['desktop','mobile']:
                    filename=f'preview_v07_{label}_{segment.rstrip("/")}.png'
                    out=root.parent/filename
                    page.screenshot(path=str(out),full_page=True,animations='disabled')
                    report['browser_screenshots'].append(str(out))
                if segment=='community/':
                    assert page.locator('a[href="#community-interest"].btn-primary').count()==1
                    assert page.locator('.work-icon-art svg').count()==3
                if segment=='reflect/':
                    assert page.locator('.reflection-field textarea').count()==5
                    page.locator('#reflection-answer-1').fill('This is a browser interaction test')
                    with page.expect_download() as download_event:
                        page.locator('#reflection-download').click()
                    download=download_event.value
                    saved=root.parent/(label+'_v07_reflection_check.txt')
                    download.save_as(str(saved))
                    if 'This is a browser interaction test' not in saved.read_text():issues.append('Reflection download did not contain answer')
                    saved.unlink()
                    page.locator('#reflection-clear').click()
                    if page.locator('#reflection-answer-1').input_value():issues.append('Reflection clear failed')
                    page.locator('#reflection-mode').select_option('action')
                    if 'Whose possibilities' not in page.locator('.reflection-field label').first.inner_text():issues.append('Reflection template selection failed')
                if segment=='downloads/':
                    if page.locator('.library-resource-grid a[download]').count()!=3:issues.append('Downloadable templates missing')
            if label=='mobile':
                page.goto(origin+'/community/',wait_until='domcontentloaded')
                page.locator('.menu-toggle').click()
                if not page.locator('.main-nav').is_visible():issues.append('mobile menu not working')
            page.close()
        browser.close()
        report['browser_test']='passed' if not issues else 'completed with issues'
except Exception as e:
    report['browser_test']='blocked: '+repr(e)
    print('Browser test unavailable:',repr(e))
finally:
    server.shutdown()
report['issues']=issues
out=root.parent/'Book_of_Chance_Website_v0.7_QA.json'
out.write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report,indent=2)[:7000]);print('REPORT',out)
if issues:raise SystemExit(1)
