"""Reproducible editorial build for The Parables of Chance. Does not modify website."""
from pathlib import Path
from io import BytesIO
import re, subprocess, json, zipfile
import cairosvg, fitz
from PIL import Image
from bs4 import BeautifulSoup
from weasyprint import HTML

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'source/parables/the-parables-of-chance.md'
ASSETS=ROOT/'assets/publications'; OUTPUT=ROOT/'files/parables'; WORK=ROOT/'_build_parables'
for d in (ASSETS,OUTPUT,WORK):d.mkdir(parents=True,exist_ok=True)
INK='#26313B'; BLUE='#286CB8'; PAPER='#FBFBFA'; GREY='#68747c'

def cover_svg():
    strands=[]
    for i in range(12):
        y0=745+i*29; y1=825+i*18; bend=(i-5.5)*24
        c2=765+bend*.75
        col=BLUE if i in (2,9) else (INK if i in (0,5,7,11) else '#9099a0')
        opacity='.90' if i in (2,9) else ('.64' if i in (0,5,7,11) else '.40')
        width=3 if i in (2,9) else 1.65
        strands.append(f'<path d="M -52 {y0} C 183 {y0-134+bend*.18:.1f}, 333 {y0+168-bend*.2:.1f}, 504 {830+bend*.3:.1f} S 799 {y1-140+bend*.2:.1f}, 1055 {y1}" fill="none" stroke="{col}" stroke-width="{width}" opacity="{opacity}" stroke-linecap="round"/>')
    for i in range(5):
        y=765+i*47
        strands.append(f'<path d="M 1070 {y-125} C 832 {y-68}, 690 {y+136}, 520 {835+i*15} S 220 {y+170}, -70 {y+85}" fill="none" stroke="{BLUE if i==3 else INK}" stroke-width="{2.3 if i==3 else 1.4}" opacity="{.80 if i==3 else .35}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1500" viewBox="0 0 1000 1500">
<rect width="1000" height="1500" fill="{PAPER}"/>
<text x="500" y="120" text-anchor="middle" font-family="Lato,Liberation Sans,sans-serif" letter-spacing="5.7" font-size="24" fill="{BLUE}">THE BOOK OF CHANCE · STORIES</text>
<text x="500" y="293" text-anchor="middle" font-family="Liberation Serif,Georgia,serif" font-size="94" fill="{INK}">The Parables</text>
<text x="335" y="392" text-anchor="middle" font-family="Liberation Serif,Georgia,serif" font-size="75" font-style="italic" fill="{INK}">of</text>
<text x="571" y="392" text-anchor="middle" font-family="Liberation Serif,Georgia,serif" font-size="98" fill="{INK}">Chance</text>
<text x="500" y="500" text-anchor="middle" font-family="Liberation Serif,Georgia,serif" font-size="29" font-style="italic" fill="{GREY}">Twelve Stories about Fortune, Choice</text>
<text x="500" y="540" text-anchor="middle" font-family="Liberation Serif,Georgia,serif" font-size="29" font-style="italic" fill="{GREY}">and the Lives We Share</text>
<g>{''.join(strands)}</g>
<line x1="433" y1="1328" x2="567" y2="1328" stroke="{BLUE}" stroke-width="2"/>
<text x="500" y="1395" text-anchor="middle" font-family="Liberation Serif,Georgia,serif" font-size="50" fill="{INK}">H</text>
</svg>'''

def build_cover():
    raw=cover_svg().encode()
    (ASSETS/'parables-of-chance-cover.svg').write_bytes(raw)
    png=cairosvg.svg2png(bytestring=raw,output_width=1000,output_height=1500)
    (ASSETS/'parables-of-chance-cover.png').write_bytes(png)
    Image.open(BytesIO(png)).convert('RGB').save(ASSETS/'parables-of-chance-cover.webp','WEBP',quality=93,method=6)

def body_source():
    manuscript=SRC.read_text('utf8')
    assert manuscript.count('## 1. The Wrong Address')==1
    body=manuscript[manuscript.index('## A Note on This Edition'):]
    p=WORK/'body.md';p.write_text(body,encoding='utf8')
    return p

def body_markup(body):
    proc=subprocess.run(['pandoc',str(body),'-f','markdown+smart','-t','html5','--wrap=none'],capture_output=True,text=True,check=True)
    soup=BeautifulSoup(proc.stdout,'html.parser')
    num=0
    for h in soup.find_all(['h1','h2','h3']):
        label=h.get_text(' ',strip=True)
        if re.match(r'^Part (I|II|III) ',label):h['class']=['part-heading']
        elif re.match(r'^\d+\. ',label):
            num+=1; h['class']=['story-heading']
            if num in (1,5,9):h['class'].append('first-in-part')
        elif h.name=='h2':
            h['class']=['section-heading']
            if label=='A Note on Authorship and Status':h['class'].append('author-note-heading')
    assert num==12,num
    for hr in soup.find_all('hr'):hr['class']=['section-rule']
    # Keep the authored contents, but group it for compact editorial-proof typesetting.
    contents=soup.find(lambda x:x.name=='h2' and x.get_text(' ',strip=True)=='Contents')
    if contents:
        wrapper=soup.new_tag('div',attrs={'class':'toc-block'})
        contents.insert_before(wrapper)
        next_node=contents
        while next_node is not None:
            after=next_node.next_sibling
            if getattr(next_node,'name',None)=='hr':
                next_node.extract()
                break
            wrapper.append(next_node.extract())
            next_node=after
    return str(soup)

CSS=r'''
@page{size:6in 9in; margin:.76in .72in .68in .72in;
@top-center{content:"THE PARABLES OF CHANCE";font:7.3pt Lato,Arial,sans-serif;letter-spacing:1.45pt;color:#7b858e;}
@bottom-center{content:counter(page);font:8pt Lato,Arial,sans-serif;color:#7b858e;}}
@page cover{margin:0;@top-center{content:none}@bottom-center{content:none}}
body{font:11.55pt/1.62 "Liberation Serif",Georgia,serif;color:#26313B;margin:0;background:#fff}
.cover{page:cover;width:6in;height:9in;margin:0;break-after:page}
.cover img{width:6in;height:9in;object-fit:cover;display:block}
.title-page{break-after:page;padding-top:1.26in;text-align:center}
.title-page .small{font:8pt/1.5 Lato,Arial,sans-serif;letter-spacing:2pt;text-transform:uppercase;color:#286CB8}
.title-page h1{font:normal 29pt/1.13 "Liberation Serif",serif;color:#172633;margin:37pt 0 15pt}
.title-page .subtitle{font:italic 12.3pt/1.5 "Liberation Serif",serif;color:#68747c}
.title-page .mark{margin-top:2.1in;font-size:19pt;color:#26313b}
.title-page .rule{width:64pt;border-top:1.4pt solid #286CB8;margin:0 auto 17pt}
.title-page .edition{font:8pt/1.6 Lato,sans-serif;color:#68747c;margin-top:31pt}
p{margin:0 0 9.25pt;orphans:3;widows:3}
.toc-block{break-before:page;break-after:page}
.toc-block h2{font:normal 23pt/1.2 "Liberation Serif",serif;margin:0 0 18pt;color:#172633}
.toc-block p{font:700 9pt/1.45 Lato,sans-serif;letter-spacing:.5pt;color:#286CB8;margin:11pt 0 5pt}
.toc-block ol,.toc-block ul{margin:0 0 9pt;padding-left:19pt;font:10.4pt/1.3 "Liberation Serif",serif}
.toc-block li{margin:0 0 2pt}
h1.part-heading{break-before:page;break-after:avoid;font:normal 22.5pt/1.16 "Liberation Serif",serif;margin:19pt 0 13pt;color:#172633}
h1.part-heading+p{font:italic 11pt/1.5 "Liberation Serif",serif;color:#62717a;margin:0 0 18pt}
h2.story-heading{break-before:page;break-after:avoid;font:normal 21pt/1.17 "Liberation Serif",serif;color:#172633;margin:15pt 0 22pt}
h2.story-heading.first-in-part{break-before:auto;margin:26pt 0 22pt}
h2.section-heading{break-before:page;break-after:avoid;font:normal 17.3pt/1.2 "Liberation Serif",serif;color:#172633;margin:18pt 0 17pt}
h2.author-note-heading~p{font-size:10.8pt;line-height:1.48;margin-bottom:7.5pt;}
.section-rule{border:0;border-top:.6pt solid #d5dde1;margin:21pt 0}
ul,ol{padding-left:20pt;margin:0 0 15pt}
li{margin-bottom:6pt;orphans:2;widows:2}
blockquote{margin:16pt 0;padding:6pt 16pt;border-left:2pt solid #286CB8;background:#fafafa}
strong{font-weight:700}
em{font-style:italic}
a{color:#286CB8;text-decoration:none}
'''

def build_pdf(markup):
    cover=(ASSETS/'parables-of-chance-cover.svg').as_uri()
    first=f'''<div class="cover"><img alt="" src="{cover}"></div>
    <div class="title-page"><div class="small">The Book of Chance · Stories and Parables</div>
    <h1>The Parables of Chance</h1>
    <div class="subtitle">Twelve Stories about Fortune, Choice<br>and the Lives We Share</div>
    <div class="rule"></div><div class="mark">H</div>
    <p class="edition">Editorial candidate v0.2.1 · 22 November 2026<br>For author review · Not final or print ready</p></div>'''
    html=f'<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><title>The Parables of Chance — editorial proof v0.2.1</title><style>{CSS}</style></head><body>{first}{markup}</body></html>'
    (WORK/'typeset.html').write_text(html,encoding='utf8')
    out=OUTPUT/'The_Parables_of_Chance_Editorial_Proof_v0.2.1.pdf'
    HTML(string=html,base_url=ROOT.as_uri()+'/').write_pdf(out)
    # WeasyPrint's metadata dictionary is not guaranteed to set the Author field.
    # Apply author, subject and language through PyMuPDF in a second pass.
    temp=out.with_name(out.stem+'-metadata.pdf')
    with fitz.open(out) as doc:
        m=doc.metadata.copy()
        m.update({'title':'The Parables of Chance — editorial proof v0.2.1',
                  'author':'H', 'subject':'Twelve Stories about Fortune, Choice and the Lives We Share',
                  'keywords':'literary fiction, philosophy, chance, editorial candidate',
                  'creator':'The Book of Chance editorial production'})
        doc.set_metadata(m)
        doc.xref_set_key(doc.pdf_catalog(),'Lang','(en-NZ)')
        doc.save(temp,garbage=4,deflate=True)
    temp.replace(out)
    return out

def build_epub(body):
    css=WORK/'epub.css'
    css.write_text('''body{font-family:serif;line-height:1.55;color:#26313B}h1{font-weight:normal;font-size:1.8em;margin:1.4em 0 .7em;page-break-before:always}h2{font-weight:normal;font-size:1.4em;margin:1.3em 0 .7em;page-break-before:always}p{margin:0 0 .75em;text-align:left}li{margin-bottom:.5em}em{font-style:italic}a{color:#286CB8}''',encoding='utf8')
    path=OUTPUT/'The_Parables_of_Chance_Editorial_Proof_v0.2.1.epub'
    cmd=['pandoc',str(body),'-f','markdown+smart','-t','epub3','--standalone',
         '--metadata=title:The Parables of Chance','--metadata=subtitle:Twelve Stories about Fortune, Choice and the Lives We Share',
         '--metadata=author:H','--metadata=lang:en-NZ',
         '--metadata=rights:Editorial review candidate; publication rights and details pending.',
         '--toc','--toc-depth=2','--split-level=1','--epub-title-page=true',
         '--epub-cover-image',str(ASSETS/'parables-of-chance-cover.png'),
         '--css',str(css),'-o',str(path)]
    subprocess.run(cmd,capture_output=True,text=True,check=True)
    assert zipfile.ZipFile(path).testzip() is None
    return path

def verify(pdf,epub):
    with fitz.open(pdf) as doc:
        assert doc.metadata.get('author') == 'H', doc.metadata
        assert doc.xref_get_key(doc.pdf_catalog(),'Lang')[1] == 'en-NZ'
        text='\n'.join(page.get_text() for page in doc)
        count=len(doc)
        assert count>=35,count
        for name in ['The Wrong Address','Two Flood Marks','The Day the Signal Failed','A Quiet Harvest',
            'The Map Without a Bridge','The Unmeasured Salt','The Night of No Stars',"The Five O’Clock Ferry",
            'The Names Left Off','The Path Through the Reeds','The Rules of the Room','What the Tide Keeps']:
            assert name in text, name
        assert tuple(round(d) for d in (doc[0].rect.width,doc[0].rect.height))==(432,648)
    with zipfile.ZipFile(epub) as z:
        assert 'mimetype' in z.namelist()
        assert any(n.endswith('parables-of-chance-cover.png') for n in z.namelist())
    info={'status':'structural proof complete; editorial approval and real-device accessibility tests outstanding',
          'manuscript_words':len(SRC.read_text('utf8').split()),'stories':12,'pdf_pages':count,
          'page_size':'6 x 9 in','edition':'v0.2.1','prepared':'2026-11-22',
          'source':str(SRC.relative_to(ROOT)),'pdf':str(pdf.relative_to(ROOT)),'epub':str(epub.relative_to(ROOT))}
    (ROOT/'docs/Parables_Production_QA_v0.2.1.json').write_text(json.dumps(info,indent=2),encoding='utf8')
    return info

def main():
    # Keep the original v0.1 cover proposal byte-for-byte; it has not been approved.
    assert all((ASSETS/('parables-of-chance-cover.'+x)).is_file() for x in ['svg','png','webp'])
    body=body_source()
    pdf=build_pdf(body_markup(body))
    epub=build_epub(body)
    print(json.dumps(verify(pdf,epub),indent=2))

if __name__=='__main__':main()
