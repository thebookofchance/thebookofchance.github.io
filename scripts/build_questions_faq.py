"""Build editorial FAQ PDF, EPUB and source-aligned web data.
This is a self-contained proof generator; it does not modify the website.
"""
from pathlib import Path
import re, json, html, subprocess, zipfile
import cairosvg
from bs4 import BeautifulSoup
from weasyprint import HTML
from approved_cover_assets import check_cover
import fitz

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'_build_faq'
WORK.mkdir(exist_ok=True)
SOURCE=ROOT/'source/resources/questions-about-chance.md'
PDF=ROOT/'files/resources/Questions_About_Chance_FAQ_Editorial_Proof_v0.3.pdf'
EPUB=ROOT/'files/resources/Questions_About_Chance_FAQ_Editorial_Proof_v0.3.epub'
COVER=ROOT/'assets/resources/questions-about-chance-cover.png'
DATA=ROOT/'source/resources/questions-about-chance.json'
HTML_FRAGMENT=WORK/'questions-about-chance-web-content.html'

# Always use the approved cover artwork, not the older generated SVG.
check_cover('faq')

source=SOURCE.read_text('utf8')
# Extract public content excluding editorial metadata and the separate sources note.
public=source.split('\n## A note on sources, status and authorship\n')[0]
public=public[public.index('## Before the questions'):]

categories=[]
for match in re.finditer(r'^## ([IVX]+)\. (.+)$',public,re.M):
    categories.append({'id':match.group(1).lower(),'title':match.group(2),'offset':match.start()})
qre=list(re.finditer(r'^### (\d+)\. (.+)$',public,re.M))
assert len(qre)==26
questions=[]
for i,m in enumerate(qre):
    start=m.end(); end=qre[i+1].start() if i+1<len(qre) else public.index('## Where can I read further?')
    answer=public[start:end].strip()
    category=next(c for c in reversed(categories) if c['offset']<m.start())
    questions.append({'number':int(m.group(1)),'id':f'q{int(m.group(1)):02d}',
                      'question':m.group(2),'category_id':category['id'],
                      'category':category['title'],'answer_markdown':answer})
assert [q['number'] for q in questions]==list(range(1,27))
DATA.write_text(json.dumps({'title':'Questions About Chance','subtitle':'Twenty-Six Questions About Confluent Humanism and the Fellowship of Chance',
                            'id':'BOC-FAQ-001','edition':'v0.3','status':'author-approved digital edition',
                            'source_documents':['Foundational Identity v1.0-RC2','Identity and Values Charter RC2','A Beginners Guide to Confluent Humanism v0.2','Publications Standard 1.0-RC1'],
                            'categories':[{'id':c['id'],'title':c['title']} for c in categories],
                            'questions':questions},ensure_ascii=False,indent=2)+'\n',encoding='utf8')

# Convert source to HTML for PDF + website prototype.
res=subprocess.run(['pandoc',str(SOURCE),'-f','markdown+smart','-t','html5','--wrap=none'],capture_output=True,text=True,check=True)
soup=BeautifulSoup(res.stdout,'html.parser')
for tag in soup.find_all(['h1','h2','h3']):
    if tag.name=='h1': tag['class']=['faq-title']
    elif tag.name=='h3': tag['class']=['faq-question']
    elif re.match(r'^[IVX]+\.',tag.get_text(' ',strip=True)): tag['class']=['faq-group']
    else: tag['class']=['faq-section']
for hr in soup.find_all('hr'):hr['class']=['faq-rule']
# accessible web fragment, not yet deployed; exclude duplicate beginning cover matter
start=soup.find(id='before-the-questions')
if not start:
    start=next(h for h in soup.find_all('h2') if 'Before the questions' in h.get_text())
parts=[str(start)]
for node in start.next_siblings:
    if getattr(node,'name',None)=='h2' and 'A note on sources' in node.get_text():break
    parts.append(str(node))
HTML_FRAGMENT.write_text(''.join(parts).strip()+'\n',encoding='utf8')

# For PDF, keep the end matter but don't repeat markdown title leaf.
start_note=next(h for h in soup.find_all('h2') if 'Before the questions' in h.get_text())
print_body=str(start_note)+''.join(str(node) for node in start_note.next_siblings)
css='''
@page{size:6in 9in;margin:.78in .7in .72in .7in;
 @top-center{content:"QUESTIONS ABOUT CHANCE · H";font:7.4pt Lato,sans-serif;color:#74828a;letter-spacing:1.3pt;}
 @bottom-center{content:counter(page);font:8pt Lato,sans-serif;color:#74828a;}}
@page cover{margin:0;@top-center{content:none}@bottom-center{content:none}}
html,body{font:10.65pt/1.51 "Liberation Serif",Georgia,serif;color:#26313B;margin:0}
.cover{page:cover;width:6in;height:9in;break-after:page}
.cover img{width:6in;height:9in;display:block}
.opening{margin-top:12pt;font:700 8pt Lato,sans-serif;color:#286CB8;letter-spacing:1.6pt}
p{margin:0 0 9pt;orphans:3;widows:3}
.faq-section{font:normal 18pt/1.15 "Liberation Serif",Georgia,serif;color:#172633;margin:28pt 0 13pt;break-after:avoid}
.faq-group{font:normal 18pt/1.15 "Liberation Serif",Georgia,serif;color:#172633;margin:24pt 0 12pt;break-before:page;break-after:avoid}
.faq-question{font:normal 13pt/1.22 "Liberation Serif",Georgia,serif;color:#172633;margin:21pt 0 9pt;break-after:avoid;}
.faq-question::first-letter{color:#286CB8}
h3.faq-question + p{margin-top:0}
strong{font-weight:bold}em{font-style:italic}
a{color:#286CB8;text-decoration:none}
.faq-rule{border:0;border-top:.7pt solid #d7dfe2;margin:21pt 0}
.faq-section:last-of-type{break-before:page}
'''
cover_url=COVER.as_uri()
page=f'''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><title>Questions About Chance — Digital Edition</title><style>{css}</style></head><body><div class="cover"><img src="{cover_url}" alt="Cover: Questions About Chance by H"/></div><div class="opening">THE BOOK OF CHANCE · PUBLIC READER RESOURCES</div>{print_body}</body></html>'''
HTML(string=page,base_url=ROOT.as_uri()+'/').write_pdf(str(PDF),pdf_variant='pdf/ua-1')
with fitz.open(PDF) as pdf:
    pdf.set_metadata({'title':'Questions About Chance — Digital Edition v0.3','author':'H','subject':'Twenty-Six Questions About Confluent Humanism and the Fellowship of Chance','keywords':'Confluent Humanism, Fellowship of Chance, FAQ, chance, ethics'})
    pdf.save(str(WORK/'_pdf_tmp.pdf'),garbage=4,deflate=True)
(WORK/'_pdf_tmp.pdf').replace(PDF)

# EPUB cover/title page and native navigation.
EPUBCSS=WORK/'_epub.css'
EPUBCSS.write_text('''body{font-family:serif;line-height:1.55;color:#26313B}h1,h2{font-weight:normal;color:#172633}h2{margin-top:2em;page-break-before:always}h3{font-size:1.12em;font-weight:normal;margin-top:1.5em;color:#172633;page-break-after:avoid}p{margin-bottom:.85em}a{color:#286CB8}''',encoding='utf8')
subprocess.run(['pandoc',str(SOURCE),'-f','markdown+smart','-t','epub3','--standalone',
                '--toc','--toc-depth=2','--split-level=2',
                '--metadata=title:Questions About Chance','--metadata=subtitle:Twenty-Six Questions About Confluent Humanism and the Fellowship of Chance',
                '--metadata=author:H','--metadata=lang:en-NZ',
                '--metadata=rights:Free public reading and download; republication requires permission.',
                '--epub-cover-image',str(COVER),'--css',str(EPUBCSS),'-o',str(EPUB)],capture_output=True,text=True,check=True)
with zipfile.ZipFile(EPUB) as z:
    assert z.testzip() is None
    assert any('cover' in n.lower() for n in z.namelist())
print('PDF', PDF.stat().st_size,'EPUB',EPUB.stat().st_size,'QA',len(questions))
