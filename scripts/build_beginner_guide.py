"""Build reproducible editorial proof of A Beginner's Guide to Confluent Humanism.
The files remain editorial candidates until human approval / accessibility review.
"""
from pathlib import Path
from html import escape
from io import BytesIO
import subprocess, zipfile, re, json
from PIL import Image
import cairosvg
import fitz
from bs4 import BeautifulSoup
from weasyprint import HTML

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'source/guides/beginners-guide-to-confluent-humanism.md'
OUT=ROOT/'files/guides'; OUT.mkdir(exist_ok=True)
TITLE='A Beginner’s Guide to Confluent Humanism'
STEM='A_Beginners_Guide_to_Confluent_Humanism'
COVER_PNG=ROOT/'assets/guides/beginners-guide-to-confluent-humanism-cover.png'
COVER_WEBP=ROOT/'assets/guides/beginners-guide-to-confluent-humanism-cover.webp'
COVER_SVG=ROOT/'assets/guides/beginners-guide-to-confluent-humanism-cover.svg'
PDF=OUT/(STEM+'_Editorial_Proof_v0.2.pdf')
EPUB=OUT/(STEM+'_Editorial_Proof_v0.2.epub')

(ROOT/'_build_beginner_guide').mkdir(parents=True, exist_ok=True)

# Draw twelve open, understated paths. The lines converge momentarily, then
# separate and continue, communicating meaningful influence but not fate.
paths=[]
for i in range(8):
    y=670+i*36
    c='#286CB8' if i in (2,6) else ('#26313B' if i%2 else '#929AA1')
    w=3.1 if i in (2,6) else (1.9 if i%2 else 1.4)
    op='.85' if i in (2,6) else ('.70' if i%2 else '.48')
    # First groups rise, second groups fall; each trajectory remains open.
    if i%2==0:
        d=f'M -60 {y-85} C 200 {y+80} 330 {y-70} 505 {y+12} S 760 {y+110} 1060 {y-55}'
    else:
        d=f'M -60 {y+82} C 220 {y-125} 347 {y+110} 505 {y-12} S 770 {y-100} 1060 {y+55}'
    paths.append(f'<path d="{d}" stroke="{c}" stroke-width="{w}" stroke-opacity="{op}" fill="none" stroke-linecap="round"/>')
cover=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1500" width="1000" height="1500">
<rect width="1000" height="1500" fill="#FBFBFA"/>
<text x="500" y="118" font-family="Liberation Sans,Lato,sans-serif" font-size="25" letter-spacing="5.5" text-anchor="middle" fill="#286CB8">THE BOOK OF CHANCE · INTRODUCTORY GUIDES</text>
<text x="500" y="294" font-family="Liberation Serif,Georgia,serif" font-size="73" text-anchor="middle" fill="#26313B">A Beginner’s Guide</text>
<text x="500" y="381" font-family="Liberation Serif,Georgia,serif" font-size="56" font-style="italic" text-anchor="middle" fill="#26313B">to</text>
<text x="500" y="471" font-family="Liberation Serif,Georgia,serif" font-size="71" text-anchor="middle" fill="#26313B">Confluent Humanism</text>
<g>{''.join(paths)}</g>
<text x="500" y="1170" font-family="Liberation Serif,Georgia,serif" font-size="30" text-anchor="middle" font-style="italic" fill="#586773">Chance, Choice and the Lives We Share</text>
<line x1="430" y1="1340" x2="570" y2="1340" stroke="#286CB8" stroke-width="2.2"/>
<text x="500" y="1410" font-family="Liberation Serif,Georgia,serif" font-size="49" text-anchor="middle" fill="#26313B">H</text>
</svg>'''
COVER_SVG.write_text(cover,encoding='utf8')
img=Image.open(BytesIO(cairosvg.svg2png(bytestring=cover.encode('utf8'),output_width=1000,output_height=1500))).convert('RGB')
img.save(COVER_PNG,'PNG',optimize=True)
img.save(COVER_WEBP,'WEBP',quality=92,method=6)

# Convert markdown into HTML. Skip typeset cover-leaf text (not the author's content).
res=subprocess.run(['pandoc',str(SRC),'-f','markdown+smart','-t','html5','--wrap=none'],check=True,capture_output=True,text=True)
soup=BeautifulSoup(res.stdout,'html.parser')
# Cover leaf title/subtitle/byline/candidate fields are repeated in a compact colophon.
first=soup.find('h1')
if first: first.decompose()
if soup.find('h2') and soup.find('h2').get_text(strip=True)=='Chance, Choice and the Lives We Share':
    soup.find('h2').decompose()
first_hr=soup.find('hr')
if first_hr:
    for p in list(first_hr.find_previous_siblings()):
        if p.name=='p':p.decompose()
    first_hr.decompose()
for h in soup.select('h2'):
    h['class']=['chapter'] if re.match(r'^\d+\.',h.get_text(' ',strip=True)) else ['section']
for h in soup.select('h3'):h['class']=['subsection']
for h in soup.select('h2.section'):
    if h.get_text(' ',strip=True).lower()=='a note on this edition':h['class']=['section','colophon']
for hr in soup.select('hr'):hr['class']=['section-separator']
for a in soup.find_all('a',href=True):
    if a['href'].startswith('https://'):a['rel']='noopener'
html=str(soup)
css='''
@page { size:6in 9in; margin:.76in .73in .75in .73in;
@top-center{content:"CONFLUENT HUMANISM  ·  AN INTRODUCTION";font:7pt Lato,"Liberation Sans",sans-serif;letter-spacing:1.15pt;color:#64747d;}
@bottom-center{content:counter(page);font:8pt Lato,"Liberation Sans",sans-serif;color:#64747d}}
@page cover{margin:0;@top-center{content:none}@bottom-center{content:none}}
body{font:10.65pt/1.49 "Liberation Serif",Georgia,serif;color:#26313B;background:white;margin:0}
.cover{page:cover;break-after:page;width:6in;height:9in;display:block;position:relative;margin:0}
.cover img{width:6in;height:9in;object-fit:cover;display:block}
.opening{padding:4pt 0 13pt;border-bottom:.7pt solid #CBD5D9;margin:0 0 18pt;}
.opening .label{font:700 8pt Lato,"Liberation Sans",sans-serif;letter-spacing:1.25pt;color:#286CB8;text-transform:uppercase;margin:0 0 12pt}
.opening h1{font:400 25pt/1.12 "Liberation Serif",Georgia,serif;color:#172633;margin:0 0 8pt}
.opening .subtitle{font:italic 12pt/1.3 "Liberation Serif",Georgia,serif;color:#60717B;margin:0 0 10pt}
.opening .meta{font:8.3pt/1.5 "Liberation Sans",Arial,sans-serif;color:#68747C;margin:0}
p{margin:0 0 9pt;orphans:3;widows:3;hyphens:none}
h2.chapter,h2.section{font:400 16.5pt/1.13 "Liberation Serif",Georgia,serif;margin:24pt 0 12pt;color:#172633;break-after:avoid}
h2.chapter{margin-top:26pt}h2.section{margin-top:23pt}
h2.colophon{break-before:page;margin-top:48pt}
h3.subsection{font:700 9pt/1.32 "Liberation Sans",Arial,sans-serif;letter-spacing:.7pt;text-transform:uppercase;color:#286CB8;margin:18pt 0 8pt;break-after:avoid}
strong{font-weight:700}em{font-style:italic}
ul,ol{padding-left:18pt;margin:2pt 0 12pt}li{margin-bottom:6pt;orphans:2;widows:2}
a{color:#286CB8;text-decoration:underline}
.section-separator{border:none;border-top:.7pt solid #CCD6DB;margin:22pt 0}
.end-note{font-size:8.8pt;line-height:1.52;color:#56646D}
.last-words{font:italic 12pt/1.52 "Liberation Serif",Georgia,serif;color:#26313B;text-align:center;margin:15pt 0}
'''
front='''<section class="opening"><div class="label">The Book of Chance · Introductory Guides</div>
<h1>A Beginner's Guide<br>to Confluent Humanism</h1><p class="subtitle">Chance, Choice and the Lives We Share</p>
<p class="meta">By H · BOC-GDE-001 · Editorial candidate v0.2 · 22 November 2026</p></section>'''
source='<html lang="en-NZ"><head><meta charset="utf-8"><title>'+escape(TITLE)+'</title><style>'+css+'</style></head><body><div class="cover"><img src="'+COVER_SVG.as_uri()+'" alt=""></div>'+front+html+'</body></html>'
( ROOT/'_build_beginner_guide/_guide_typeset.html').write_text(source,encoding='utf8')
HTML(string=source,base_url=ROOT.as_uri()+'/').write_pdf(str(PDF))
with fitz.open(PDF) as pdf:
    md=pdf.metadata
    md.update({'title':TITLE,'author':'H','subject':'Introductory guide to Confluent Humanism — editorial candidate v0.2','keywords':'The Book of Chance, Confluent Humanism, Fellowship of Chance, beginner guide'})
    pdf.set_metadata(md)
    tmp=ROOT/'_build_beginner_guide/_guide_meta.pdf'
    pdf.save(str(tmp),garbage=4,deflate=True)
tmp.replace(PDF)

css_epub=ROOT/'_build_beginner_guide/_guide_epub.css'
css_epub.write_text('''html{font-family:serif;line-height:1.58;color:#26313B}body{margin:5%}h1,h2{font-weight:normal;color:#172633}h2{font-size:1.5em;margin:1.6em 0 .7em;page-break-after:avoid}h3{font-size:1.03em;color:#286CB8;margin:1.2em 0 .6em}p{margin:0 0 .84em}li{margin-bottom:.5em}a{color:#286CB8}hr{border:0;border-top:1px solid #CBD5D9;margin:1.5em 0}''',encoding='utf8')
subprocess.run(['pandoc',str(SRC),'-f','markdown+smart','-t','epub3','--standalone','--toc','--toc-depth=2',
 '--split-level=1','--epub-title-page=true',
 '--metadata=title:A Beginner\'s Guide to Confluent Humanism','--metadata=subtitle:Chance, Choice and the Lives We Share',
 '--metadata=author:H','--metadata=lang:en-NZ',
 '--metadata=description:An introduction to Confluent Humanism, chance, meaningful choice, five values and the proposed Fellowship of Chance.',
 '--metadata=rights:Free access intended. Editorial candidate. Republication rights pending.',
 '--epub-cover-image',str(COVER_PNG),'--css',str(css_epub),'-o',str(EPUB)],capture_output=True,text=True,check=True)
with zipfile.ZipFile(EPUB) as epub:
    assert epub.testzip() is None
print(json.dumps({'pdf':str(PDF),'epub':str(EPUB),'pages':len(fitz.open(PDF)),'word_count':len(SRC.read_text('utf8').split()),'files':[str(p) for p in (COVER_SVG,COVER_PNG,COVER_WEBP)]},indent=2))
