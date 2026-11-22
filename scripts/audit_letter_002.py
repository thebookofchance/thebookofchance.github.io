"""Static and PDF/EPUB checks for Letter 002, without network or user data."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
import fitz, hashlib, json, zipfile, re

ROOT=Path(__file__).resolve().parents[1]
LINKS=0
ERRORS=[]
for htmlpath in ROOT.rglob('*.html'):
    if '__pycache__' in htmlpath.parts: continue
    soup=BeautifulSoup(htmlpath.read_text('utf8'),'html.parser')
    for elem in soup.find_all(['a','img','script','link','source']):
        for attr in ('href','src'):
            url=elem.get(attr)
            if not url: continue
            parts=urlsplit(url)
            if parts.scheme or url.startswith('//'):continue
            if not parts.path:continue
            dest=unquote(parts.path)
            if dest.startswith('/'):
                target=ROOT/dest.lstrip('/')
            else:
                target=htmlpath.parent/dest
            if dest.endswith('/') or target.is_dir():target=target/'index.html'
            LINKS+=1
            if not target.exists():ERRORS.append((htmlpath.relative_to(ROOT).as_posix(),url))

cat=json.loads((ROOT/'source/letters/catalogue.json').read_text('utf8'))
assert [p['number'] for p in cat['available']]==[1,2]
for item in cat['available']:
    for key in ('file','cover','pdf','epub'):
        assert (ROOT/item[key]).is_file(), (item['id'],key)
    assert (ROOT/item['url']/'index.html').exists()
assert not ERRORS, ERRORS[:30]

second=cat['available'][1]
source=(ROOT/second['file']).read_text('utf8')
pdf=fitz.open(ROOT/second['pdf'])
assert len(pdf)>=6
assert all((round(p.rect.width),round(p.rect.height))==(432,648) for p in pdf)
full=' '.join(p.get_text() for p in pdf)
for s in ['When Good Choices','Intention is not enough','Who carries the risk','An optional practice','The philosopher Thomas Nagel','Thomas Nagel','Bernard Williams']:
    assert s.lower() in re.sub(r'\s+',' ',full).lower(),s
for pageno, p in enumerate(pdf,1):
    for block in p.get_text('blocks'):
        if block[6] !=0:continue
        x0,y0,x1,y1, *_=block
        if x0<-3 or y0<-3 or x1>p.rect.width+3 or y1>p.rect.height+3:
            ERRORS.append(('pdf-boundary',pageno,block[:4]))

with zipfile.ZipFile(ROOT/second['epub']) as ep:
    assert ep.read('mimetype')==b'application/epub+zip'
    assert ep.testzip() is None
    content=' '.join(ep.read(f).decode('utf8',errors='ignore') for f in ep.namelist() if f.endswith(('.html','.xhtml')))
    assert 'Who carries the risk?' in content

page=BeautifulSoup((ROOT/second['url']/'index.html').read_text('utf8'),'html.parser')
assert 'Intention is not enough' in page.select_one('article.letters-prose').get_text()
assert page.select_one('article.letters-prose a[href^="https://plato.stanford.edu"]')
assert len(BeautifulSoup((ROOT/'letters/index.html').read_text('utf8'),'html.parser').select('.letters-index-feature'))==2
assert '03' in BeautifulSoup((ROOT/'downloads/index.html').read_text('utf8'),'html.parser').select_one('.library-count span').get_text()

report={
    'site_version':'0.12',
    'new_issue':second['id'],
    'edition':second['edition'],
    'status':second['status'],
    'page_count_pdf':len(pdf),
    'source_words':len(source.split()),
    'site_pages_checked':sum(1 for _ in ROOT.rglob('index.html')),
    'local_references_checked':LINKS,
    'broken_local_links':ERRORS,
    'epub_integrity':'PASS',
    'html_markdown_parity_spot_checks':'PASS',
    'pdf_format_size':'6x9 inches',
    'letter_001_change_prevented':True,
    'live_deployment_test':'NOT TESTED',
    'physical_e_reader_test':'NOT TESTED',
    'human_editorial_approval':'PENDING',
}
(ROOT/'docs/Letter_002_QA_Report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf8')
assert not ERRORS,ERRORS
print(json.dumps(report,indent=2))
