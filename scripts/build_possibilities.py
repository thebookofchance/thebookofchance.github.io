"""Produce the editorial candidate for The Little Book of Possibilities.

Uses the existing The Book of Chance literary cover language and typeset approach;
this does not update website content or assert editorial approval.
"""
from pathlib import Path
import re, json, subprocess, zipfile, hashlib
from xml.sax.saxutils import escape
from PIL import Image
import cairosvg
from weasyprint import HTML
from bs4 import BeautifulSoup
import fitz

ROOT = Path(__file__).resolve().parents[1]
S = ROOT/'source/booklets/the-little-book-of-possibilities.md'
DEST = ROOT/'files/booklets'
DEST.mkdir(parents=True,exist_ok=True)
ART = ROOT/'assets/booklets'
WORK = ROOT/'_build_possibilities'
WORK.mkdir(parents=True,exist_ok=True)
TITLE = 'The Little Book of Possibilities'
SUBTITLE = 'On Small Openings and the Conditions We Create'
COVER = 'the-little-book-of-possibilities-cover'
PDF = DEST/'The_Little_Book_of_Possibilities_Editorial_Proof_v0.2.pdf'
EPUB = DEST/'The_Little_Book_of_Possibilities_Editorial_Proof_v0.2.epub'

BLUE='#286CB8'; INK='#26313B'; MUTED='#68747c'; LIGHT='#d8dfe2'; GREY='#929da4'

def p(d, color=INK, w=1.7, opacity=1):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round"/>'


def verify_approved_cover():
    # Exact accepted v0.1 cover assets from publication QA; never regenerate them.
    expected={
       '.svg':'d016e2e9d12a154853cc59ba9c6f3f41349ea989f77f07125405edff4b9eead7',
       '.png':'3552fa6ba5c85c7957f7ab1280b8859d4a61862c52b76b3a132bf2f566d2e99c',
       '.webp':'214ce2ce0fb79434e2f54cfec96315afcdd798faec190c218708c5bb4b00fa3f',
    }
    for ext, accepted_hash in expected.items():
       path=ART/f'{COVER}{ext}'
       assert path.is_file(), 'Approved cover asset missing: '+str(path)
       assert hashlib.sha256(path.read_bytes()).hexdigest()==accepted_hash, 'Approved cover changed: '+str(path)

CSS = r'''
@page { size: 6in 9in; margin:.76in .74in .73in .74in;
  @top-center{content:"THE LITTLE BOOK OF POSSIBILITIES";font-family:Lato,Liberation Sans,Arial,sans-serif;font-size:7.0pt;letter-spacing:1.1pt;color:#78848c;}
  @bottom-center{content:counter(page);font-family:Lato,Liberation Sans,Arial,sans-serif;font-size:8pt;color:#78848c;}}
@page cover{margin:0;@top-center{content:none}@bottom-center{content:none}}
@page titlepage{margin:.76in .78in;@top-center{content:none}@bottom-center{content:none}}
body{font-family:"Liberation Serif",Georgia,serif;font-size:10.8pt;line-height:1.51;color:#26313B;background:#fff;margin:0}
p{margin:0 0 8.8pt;orphans:3;widows:3;hyphens:auto}
.cover{page:cover;break-after:page;margin:0;width:6in;height:9in}.cover img{width:6in;height:9in;display:block;object-fit:cover}
.titlepage{page:titlepage;break-after:page;padding:1.15in .16in .2in}
.titlepage .kicker{font-family:Lato,Liberation Sans,Arial,sans-serif;font-size:8pt;letter-spacing:1.5pt;color:#286CB8;text-transform:uppercase;margin-bottom:28pt}
.titlepage h1{font-size:31pt;font-weight:400;line-height:1.11;color:#172633;margin:0 0 21pt}
.titlepage .subtitle{font-size:13pt;line-height:1.4;font-style:italic;color:#586b74}
.titlepage .byline{font-size:21pt;margin-top:56pt;color:#26313B}
.titlepage .status{border-top:.7pt solid #b8c1c7;padding-top:15pt;margin-top:45pt;font:8.5pt/1.65 Lato,Liberation Sans,sans-serif;color:#64727a}
section.main-content h1{font-size:20pt;line-height:1.22;font-weight:400;color:#172633;margin:28pt 0 17pt;break-before:page;break-after:avoid}
section.main-content h1:first-child{break-before:auto}
section.main-content h2{font-size:17.8pt;font-weight:400;line-height:1.2;color:#172633;margin:29pt 0 16pt;break-after:avoid}
section.main-content h2.chapter{break-before:page;margin:22pt 0 16pt;font-size:22pt}
section.main-content h2.section-break{break-before:page}
section.main-content h3{font-size:10.2pt;color:#286CB8;font-family:Lato,Arial,sans-serif;letter-spacing:.5pt;margin:20pt 0 8pt;break-after:avoid}
section.main-content .part-note{font-style:italic;color:#68747c;font-size:12pt;line-height:1.5;margin-bottom:15pt}
section.main-content strong{font-weight:700}
section.main-content em{font-style:italic}
section.main-content .question{border-left:2pt solid #286CB8;padding:2pt 0 2pt 11pt;font-style:italic;margin:16pt 0 18pt;break-inside:avoid;color:#435766}
section.main-content hr{border:0;border-top:.65pt solid #d8dfe2;margin:20pt 0}
section.main-content ul,section.main-content ol{padding-left:19pt;margin:7pt 0 18pt}
section.main-content li{margin-bottom:7pt;orphans:2;widows:2}
section.main-content a{color:#286CB8}
section.main-content .intro-h{font-size:19pt;margin-top:20pt}
section.main-content .front-head{font-size:15pt;margin:12pt 0}
section.main-content .contents-head{break-before:page}
section.main-content .toc-compact{font-size:9.5pt;line-height:1.25}
section.main-content .toc-compact p{margin-bottom:4pt}
section.main-content .toc-compact ol,section.main-content .toc-compact ul{margin:3pt 0 9pt;padding-left:16pt}
section.main-content .toc-compact li{margin-bottom:2pt}
section.main-content .front-head+ p{margin-top:8pt}
section.main-content .editorial-end{margin-top:10pt;color:#65757e;font-size:9.5pt}
'''

def make_pdf():
    text=S.read_text('utf8')
    begin=text.index('## A Note on This Edition')
    content=text[begin:]
    # semantic header levels retained. Markdown supports sections with strong and italics.
    mdfile=WORK/'_book_body.md'
    mdfile.write_text(content,encoding='utf8')
    out=subprocess.run(['pandoc',str(mdfile),'-f','markdown+smart','-t','html5','--wrap=none'],text=True,capture_output=True,check=True).stdout
    soup=BeautifulSoup(out,'html.parser')
    for hr in soup.find_all('hr'):
        # A part heading already signals the transition. Suppress a dangling
        # horizontal rule that could otherwise create a blank page.
        next_block = hr.find_next_sibling()
        if next_block and next_block.name == 'h1':
            hr.decompose()
        else:
            hr['class']=['interlude-rule']
    for h in soup.find_all(['h1','h2']):
        name=h.get_text(' ',strip=True)
        if h.name=='h2' and re.match(r'^\d+\. ',name): h['class']=['chapter']
        elif h.name=='h2' and name in ['A Note on This Edition','Contents'] : h['class']=['front-head']
        elif h.name=='h2':h['class']=['section-break']
        if h.name=='h2' and name=='Contents':h['class']=['front-head','contents-head']
    # Keep the preliminary Contents compact and on one page, avoiding a dangling
    # last few items on a second Contents page.
    _contents = next((h for h in soup.find_all('h2') if h.get_text(' ',strip=True)=='Contents'), None)
    if _contents:
        _toc=soup.new_tag('div',attrs={'class':'toc-compact'})
        for _sib in list(_contents.next_siblings):
            if getattr(_sib,'name',None)=='hr':break
            _toc.append(_sib.extract())
        _contents.insert_after(_toc)
    for h in soup.find_all('h1'):
        nx=h.find_next_sibling('p')
        if nx and nx.find('em') and nx.get_text(strip=True).startswith(('Before we can widen','The most useful','An opening is more durable')):
            nx['class']=['part-note']
    for ptag in soup.find_all('p'):
        if ptag.get_text(' ',strip=True).startswith('A question to carry:') or ptag.get_text(' ',strip=True).startswith('**A question to carry:**'):
            ptag['class']=['question']
        if 'Editorial and Authorship Record' in (ptag.find_previous('h2').get_text(' ',strip=True) if ptag.find_previous('h2') else ''):
            ptag['class']=['editorial-end']
    title=f'''<div class="cover"><img alt="" src="{(ART/f'{COVER}.svg').as_uri()}"></div>
<div class="titlepage"><p class="kicker">The Book of Chance · Companion collection</p><h1>The Little Book<br>of Possibilities</h1><p class="subtitle">On Small Openings and the Conditions We Create</p><p class="byline">H</p><p class="status">Editorial reader’s proof v0.2 · Prepared 22 November 2026<br>For author review. This is not a final release or print-ready interior.<br>Copyright, imprint, ISBN and publication rights remain to be confirmed.</p></div>'''
    html=f'<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><title>{escape(TITLE)}</title><style>{CSS}</style></head><body>{title}<section class="main-content">{str(soup)}</section></body></html>'
    HTML(string=html,base_url=ROOT.as_uri()+'/').write_pdf(str(PDF),metadata={'title':TITLE,'author':'H','subject':SUBTITLE})
    with fitz.open(PDF) as _document:
        metadata = _document.metadata
        metadata.update({'title': TITLE, 'author':'H','subject':SUBTITLE + ' — editorial proof v0.2','keywords':'The Book of Chance; Confluent Humanism; possibilities; editorial candidate'})
        _document.set_metadata(metadata)
        _tmp=PDF.with_suffix('.meta.pdf')
        _document.save(_tmp,garbage=4,deflate=True)
    _tmp.replace(PDF)
    print('PDF',PDF)


def make_epub():
    css=WORK/'The_Little_Book_of_Possibilities_Ebook.css'
    css.write_text('''body{font-family:serif;line-height:1.55;color:#26313B}h1{font-weight:400;font-size:1.75em;margin:1.7em 0 .7em;break-before:page}h2{font-weight:400;font-size:1.45em;margin:1.6em 0 .7em;break-after:avoid}p{margin:.4em 0 1em}li{margin-bottom:.6em}blockquote{border-left:2px solid #286CB8;padding-left:1em}a{color:#286CB8}img{max-width:100%;height:auto}''',encoding='utf8')
    cmd=['pandoc',str(S),'-f','markdown+smart','-t','epub3','--standalone','--toc','--toc-depth=2','--split-level=1',
         '--epub-cover-image',str(ART/f'{COVER}.png'),
         '--metadata=title:'+TITLE,'--metadata=subtitle:'+SUBTITLE,'--metadata=author:H','--metadata=lang:en-NZ',
         '--metadata=rights:Editorial candidate, publication details pending.',
         '--metadata=edition:v0.2', '--metadata=description:Editorial candidate v0.2 — substantively revised 22 November 2026.',
         '--css',str(css),'-o',str(EPUB)]
    subprocess.run(cmd,capture_output=True,text=True,check=True)
    assert zipfile.ZipFile(EPUB).testzip() is None
    print('EPUB',EPUB)

if __name__=='__main__':
    # Cover approved by H at v0.1 and deliberately NOT regenerated.
    verify_approved_cover()
    make_pdf()
    make_epub()
