"""Static and source-to-export checks for Letters from H No. 03."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import zipfile, re, hashlib, json
import fitz
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
ERR=[]; links=0
pages=list(ROOT.rglob('*.html'))
for path in pages:
    soup=BeautifulSoup(path.read_text('utf8'),'html.parser')
    for e in soup.find_all(['a','img','script','link','source']):
        for attr in ('href','src'):
            u=e.get(attr)
            if not u:continue
            p=urlsplit(u)
            if p.scheme or u.startswith('//') or not p.path:continue
            dest=unquote(p.path)
            candidate=ROOT/dest.lstrip('/') if dest.startswith('/') else path.parent/dest
            if dest.endswith('/') or candidate.is_dir():candidate=candidate/'index.html'
            links+=1
            if not candidate.exists():ERR.append((str(path.relative_to(ROOT)),u))
cat=json.loads((ROOT/'source/letters/catalogue.json').read_text('utf8'))
assert [x['number'] for x in cat['available']]==[1,2,3]
for item in cat['available']:
    for k in ['file','pdf','epub','cover']:
        assert (ROOT/item[k]).exists(),(item['id'],k)
    assert (ROOT/item['url']/'index.html').is_file()
new=cat['available'][-1]
md=(ROOT/new['file']).read_text('utf8')
word_count=len(re.findall(r"\b[\w’'-]+\b",md))
pdf=fitz.open(ROOT/new['pdf']);assert len(pdf)>6
assert all(round(p.rect.width)==432 and round(p.rect.height)==648 for p in pdf)
pdftext=re.sub(r'\s+',' ',' '.join(p.get_text() for p in pdf))
for needle in ['What Do We Owe to Strangers?','A claim before an introduction','Help without possession','An optional practice','Readers are welcome to']:
    assert needle.casefold() in pdftext.casefold(),needle
for i,p in enumerate(pdf,1):
    for b in p.get_text('blocks'):
        if b[6]!=0:continue
        x0,y0,x1,y1=b[:4]
        if x0 < -3 or y0 < -3 or x1>p.rect.width+3 or y1>p.rect.height+3:
            ERR.append(('pdf_out_of_page',i,b[:4]))
with zipfile.ZipFile(ROOT/new['epub']) as e:
    assert e.read('mimetype')==b'application/epub+zip'
    assert e.testzip() is None
    eptext=' '.join(e.read(x).decode('utf8',errors='replace') for x in e.namelist() if x.endswith(('.xhtml','.html')))
    for needle in ['Help without possession','What Do We Owe to Strangers?','For reflection']:
        assert needle in eptext,needle
page=BeautifulSoup((ROOT/new['url']/'index.html').read_text('utf8'),'html.parser')
article=page.select_one('article.letters-prose')
assert article
assert 'The people we have promised to' in article.get_text(' ',strip=True)
assert len(article.find_all('a',href=lambda x:x and x.startswith('https://plato.stanford.edu/')))==3
assert len(BeautifulSoup((ROOT/'letters/index.html').read_text('utf8'),'html.parser').select('.letters-index-feature'))==3
count=BeautifulSoup((ROOT/'downloads/index.html').read_text('utf8'),'html.parser').select_one('.library-count span').get_text(' ',strip=True)
assert count=='04',count
assert new['title'] in (ROOT/'index.html').read_text('utf8') or new['lead'] in (ROOT/'index.html').read_text('utf8')
sitemap=(ROOT/'sitemap.xml').read_text('utf8')
assert 'https://thebookofchance.github.io/'+new['url'] in sitemap
assert not ERR, ERR[:15]
report={
 'website_version':'0.13','issue':new['id'],'edition':new['edition'],'status':new['status'],
 'source_words':word_count,'pdf_pages':len(pdf),'pdf_size':'6 x 9 in','epub_zip_test':'PASS',
 'html_parity_checks':'PASS','local_html_pages':len(pages),'local_refs_checked':links,'broken_local_references':len(ERR),
 'html_series_cards':3,'site_library_publication_count':4,
 'approved_logos_prior_letters_books_journals_and_forms':'SHA256 compared to v0.12 separately, preserved',
 'live_github_verification':'NOT TESTED','desktop_mobile_browser_render':'NOT TESTED — headless local browser blocked',
 'physical_ereader_verification':'NOT TESTED','human_editorial_approval':'PENDING',
 'pdf_accessibility_tagging':'NOT CERTIFIED'
}
(ROOT/'docs/Letter_003_QA_Report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
