from pathlib import Path
import re, shutil, subprocess, html, zipfile, hashlib, json
from bs4 import BeautifulSoup
from weasyprint import HTML
import fitz

R=Path(__file__).resolve().parents[1]
W=R/'_build_book'
W.mkdir(parents=True,exist_ok=True)
NEW=R/'source'
ART=NEW/'artwork'
outmd=NEW/'manuscript.md'
new=outmd.read_text(encoding='utf-8')
assert len(list(ART.glob('*.png')))==6
captions={
 '01_part_i.png':('What we inherit','Each path enters a world already shaped by other lives.'),
 '02_part_ii.png':('Where choice begins','Our decisions take place within conditions we inherit.'),
 '03_part_iii.png':('Lives in relation','As paths cross and recross.'),
 '04_meanings.png':('Reading the distinctions','These four meanings answer different questions.'),
 '05_values.png':('Values in conversation','The five values are complementary, not ranked.'),
 '06_ripple.png':('An influence, not a promise','An act of help may lead to a connection.'),
}
body=new[new.index('## A Note on This Edition\n'):]
bodymd=W/'contextual_body_v014.md';bodymd.write_text(body,encoding='utf-8')
res=subprocess.run(['pandoc',str(bodymd),'-f','markdown+smart+fenced_divs','-t','html5','--wrap=none'],capture_output=True,text=True,check=True)
soup=BeautifulSoup(res.stdout,'html.parser')
heads=soup.find_all(re.compile('^h[1-3]$'))
contents=[]
for h in heads:
    title=h.get_text(' ',strip=True)
    if h.name=='h1' and title.startswith('Part '):h['class']=['part-heading'];contents.append(('part',h))
    elif h.name=='h1' and title.startswith('Reader Resources'):h['class']=['resources-heading'];contents.append(('part',h))
    elif h.name=='h2' and title.startswith('Reading '):h['class']=['chapter-heading'];contents.append(('chapter',h))
    elif h.name=='h2' and title.startswith('Afterword'):h['class']=['front-heading','afterword-heading'];contents.append(('front',h))
    elif h.name=='h2' and (title.startswith('A Note') or title.startswith('Introduction')):h['class']=['front-heading'];contents.append(('front',h))
    elif h.name=='h2' and title in ('Ways of Reflecting','Further Reading'):h['class']=['appendix-heading'];contents.append(('appendix',h))
    elif h.name=='h3':h['class']=['section-heading']
for hr in soup.find_all('hr'):hr['class']=['prose-divider']
for h in soup.select('h3.section-heading'):
    if h.get_text(' ',strip=True)=='For reflection':
        h['class'].append('reflection-heading');li=h.find_next_sibling()
        if li and li.name in ('ul','ol'):li['class']=['reflection-list']
    if h.get_text(' ',strip=True).lower() in ['the two gardens','the missed bus','the crossing','the page and the hand','the lantern','the waiting room','the open door','the empty chair','the shared well']:
        h['class'].append('parable-heading')

# Each image has one following authored, editable, semantic context block.
for img in list(soup.find_all('img')):
    name=Path(img['src']).name
    assert name in captions,name
    fig=img.parent if img.parent.name=='figure' else img
    context=fig.find_next_sibling()
    assert context and 'figure-context' in context.get('class',[]),(name,str(context)[:140])
    img['src']=(ART/name).as_uri()
    wrapper=soup.new_tag('section',attrs={'class':'part-plate' if name in ['01_part_i.png','02_part_ii.png','03_part_iii.png'] else 'diagram-plate','role':'group'})
    if name in ['01_part_i.png','02_part_ii.png','03_part_iii.png']:
        heading=fig.find_previous_sibling('h1')
        assert heading and 'part-heading' in heading.get('class',[]),name
        heading.wrap(wrapper)
        wrapper.append(fig.extract())
    else:fig.wrap(wrapper)
    context['class']=['figure-context','caption-block']
    wrapper.append(context.extract())
    wrapper['aria-label']=captions[name][0]

css=(R/'source/book-print-base.css').read_text(encoding='utf-8')
css+='''
/* Contextual illustrated edition: the image is larger/higher; editable sharp text is below. */
@page illustrated { size:5.5in 8.5in; margin:0;
 @top-left{content:none;} @top-right{content:none;} @bottom-left{content:none;} @bottom-right{content:none;} }
.part-plate,.diagram-plate{page:illustrated; break-before:page; break-after:page; width:5.5in;height:8.48in;overflow:hidden;position:relative;box-sizing:border-box;margin:0;padding:0;background:white}
.part-plate{break-before:right}
.part-plate h1.part-heading{position:absolute;top:0;left:0;width:0;height:0;min-height:0;overflow:hidden;font-size:0;line-height:0;padding:0;margin:0;page:auto;break-before:auto;break-after:auto}
.part-plate figure,.diagram-plate figure {margin:0;padding:0;display:block;position:absolute;top:.06in;left:.11in;width:5.28in;height:6.43in;}
.part-plate img,.diagram-plate img {display:block;width:5.28in;height:6.43in;object-fit:contain;margin:0;padding:0;}
.part-plate figcaption,.diagram-plate figcaption {display:none}
.figure-context.caption-block{position:absolute;top:6.61in;left:.73in;right:.68in;border-top:.55pt solid #a9b2bb;padding-top:.17in;margin:0;color:#333b41;}
.figure-context.caption-block p{font-family:"Gentium Book Plus",serif;font-size:9.2pt;line-height:1.32;text-align:left;margin:0;orphans:2;widows:2;hyphens:none;}
.figure-context.caption-block strong{font-family:"EB Garamond",serif;font-style:italic;font-size:10.2pt;font-weight:600;color:#262e35;}
'''
toc=[]
for kind,h in contents:
    cls={'part':'toc-part','chapter':'toc-chapter','front':'toc-front','appendix':'toc-appendix'}[kind]
    title=h.get_text(' ',strip=True)
    toc.append(f'<p class="toc-entry {cls}"><a href="#{h["id"]}">{html.escape(title)}</a></p>')

before=f'''<div class="title-page"><div class="book-title">The Book<br>of Chance</div><div class="book-subtitle">On the Lives We Inherit<br>and the Futures We Shape</div><div class="rule"></div><div class="title-author">H</div><div class="proof-stamp">ILLUSTRATED READER’S PROOF &nbsp; · &nbsp; editorial revision v0.14</div></div>
<div class="verso"><h2>Illustrated proof edition</h2><p>This is an author-review proof of the illustrated manuscript with six images and typeset explanatory captions. This revision clarifies the argument for an open future while preserving its philosophical uncertainty.</p><p>Illustrations are conceptual aids, not empirical evidence. The book acknowledges its debts to wider philosophical traditions in Further Reading.</p><p>Edition prepared: 22 November 2026. Author byline: H. Copyright, imprint, ISBN and publication details remain pending. This proof is not a final printer-certified interior.</p></div>
<div class="toc-page"><h2>Contents</h2>{''.join(toc)}</div>'''
full=f'<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"/><title>The Book of Chance — Contextual Illustrated Proof</title><style>{css}</style></head><body>{before}{str(soup)}</body></html>'
(W/'contextual_print_v014.html').write_text(full,encoding='utf-8')
pdf=W/'book_interior_v014.pdf'
print('Generating PDF...',flush=True)
HTML(string=full,base_url=str(NEW)).write_pdf(str(pdf))

# Ebook: preserve caption blocks as real selectable text after figures.
ebooklines=[]
for line in body.splitlines():
    if line.startswith('### '):line='## '+line[4:]
    elif line.startswith('## '):line='# '+line[3:]
    ebooklines.append(line)
ebookbody=W/'contextual_epub_body_v014.md'
ebookbody.write_text('\n'.join(ebooklines)+'\n',encoding='utf-8')
epub_css=W/'contextual_ebook_v014.css'
epub_css.write_text('''html{font-family:serif;line-height:1.47;color:#23272b}body{margin:4%}h1{font-weight:normal;font-size:1.8em;line-height:1.14;margin:1.6em 0 .75em;page-break-before:always}h2{font-weight:normal;font-size:1.3em;line-height:1.2;margin:1.4em 0 .6em;page-break-after:avoid}p{margin:0 0 .76em;text-align:left;orphans:2;widows:2}blockquote{margin:1em 4%;padding-left:.8em;border-left:1px solid #aaa}blockquote p{font-style:italic}li{margin-bottom:.4em}a{color:inherit}img{max-width:100%;height:auto;display:block;margin:.8em auto}figure{page-break-inside:avoid;margin:.8em 0 .2em}figure img{max-width:100%}figcaption{font-size:.8em;color:#555}.figure-context{border-top:1px solid #a9b2bb;margin:.35em 3% 1.4em;padding:.55em 0 .1em;color:#383f48;font-size:.93em;line-height:1.4}.figure-context p{margin:0;text-align:left}.figure-context strong{font-style:italic}a[href^="http"]{overflow-wrap:anywhere}''',encoding='utf-8')
meta=W/'contextual_epub_metadata_v014.yaml'
meta.write_text('''title: The Book of Chance
subtitle: On the Lives We Inherit and the Futures We Shape
author: H
lang: en-NZ
rights: Contextual illustrated reader's proof; publication details pending.
''',encoding='utf-8')
# Keep the approved cover images and the same revised body in both editions.
for kind in ('Light','Dark'):
    cover=NEW/'covers'/f'Book_of_Chance_{kind}_Cover.png'
    epubout=R/'files'/f'The_Book_of_Chance_{kind}.epub'
    print('Generating revised EPUB',kind,flush=True)
    cmd=['pandoc',str(ebookbody),'-f','markdown+smart+fenced_divs','-t','epub3','--standalone','--toc','--toc-depth=1','--split-level=1',
         '--epub-title-page=true','--epub-cover-image',str(cover),'--css',str(epub_css),'--metadata-file',str(meta),'-o',str(epubout)]
    subprocess.run(cmd,cwd=NEW,capture_output=True,text=True,check=True)
    assert zipfile.ZipFile(epubout).testzip() is None
    # Prefix the already illustrated interior with the matching original cover.
    pdfout=R/'files'/f'The_Book_of_Chance_{kind}_PDF_Reader_Proof.pdf'
    with fitz.open() as result, fitz.open(str(pdf)) as interior:
        first=result.new_page(width=interior[0].rect.width,height=interior[0].rect.height)
        first.insert_image(first.rect,filename=str(cover),keep_proportion=True)
        result.insert_pdf(interior)
        result.save(str(pdfout),garbage=4,deflate=True)
    print('Created',pdfout.name, len(fitz.open(pdfout)), 'pages',flush=True)

print('Book editions complete')
