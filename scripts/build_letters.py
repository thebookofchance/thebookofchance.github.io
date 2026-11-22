from pathlib import Path
import subprocess, json, re, html
from PIL import Image
from io import BytesIO
import cairosvg
import mistune
from weasyprint import HTML
from approved_cover_assets import check_cover
from pdf_release_metadata import set_pdf_info

ROOT=Path(__file__).resolve().parents[1]
LETTER=ROOT/'source/letters/001-on-the-people-we-never-meet.md'
META=json.loads((ROOT/'source/letters/catalogue.json').read_text(encoding='utf-8'))['available'][0]
PDF=ROOT/META['pdf']
EPUB=ROOT/META['epub']
COVER=ROOT/META['cover']

# Approved cover art is verified by `check_cover` during each build.
# Legacy procedural cover generators were deliberately retired in v0.30.

def build():
    PDF.parent.mkdir(parents=True,exist_ok=True)
    COVER.parent.mkdir(parents=True,exist_ok=True)
    source=LETTER.read_text(encoding='utf-8')
    # Reuse approved, hash-verified Letter 01 cover. No generated SVG is written.
    check_cover('letter-01')
    # Convert the canonical Markdown using the same rule-based renderer as the website.
    md=mistune.create_markdown(escape=True,plugins=['table','strikethrough','url'])
    article=md(source)
    article=re.sub(r'<h1>.*?</h1>','',article,count=1,flags=re.S)
    article=re.sub(r'<p><em>Letters from H · No. 01</em></p>','',article,count=1)
    article=article.replace('<hr />','<hr>')
    css='''
      @page{size:6in 9in;margin:0.80in 0.72in 0.73in 0.72in;
        @top-center{content:"LETTERS FROM H  ·  NO. 01";font-family:Lato,sans-serif;font-size:7pt;letter-spacing:1.4pt;color:#77848d;}
        @bottom-center{content:counter(page);font-family:Lato,sans-serif;font-size:8pt;color:#77848d;}}
      @page cover{margin:0;@top-center{content:none}@bottom-center{content:none}}
      body{font:11.4pt/1.61 'Liberation Serif',Georgia,serif;color:#26313b;margin:0;background:white}
      .cover{page:cover;break-after:page;margin:0;width:6in;height:9in}
      .cover img{width:6in;height:9in;object-fit:cover;display:block}
      h1{font:normal 24pt/1.18 'Liberation Serif',serif;color:#172633;margin:0 0 15pt}
      .eyebrow{font:700 8pt Lato,sans-serif;letter-spacing:1.8pt;color:#286cb8;text-transform:uppercase;margin-bottom:15pt}
      .subtitle{font:italic 11.5pt/1.5 'Liberation Serif',serif;color:#62717b;margin:0 0 27pt}
      .start{margin-top:8pt}
      .start::after{content:'';display:block;border-bottom:.7pt solid #d6dce0;margin:0 0 24pt}
      p{margin:0 0 11pt;orphans:3;widows:3}
      h2{font:normal 16pt/1.18 'Liberation Serif',serif;margin:26pt 0 12pt;color:#172633;break-after:avoid}
      h3{font:700 8.5pt/1.5 Lato,sans-serif;letter-spacing:1.3pt;margin:22pt 0 12pt;color:#286cb8;text-transform:uppercase;break-after:avoid}
      ul{padding-left:18pt;margin-bottom:15pt}li{margin-bottom:9pt;orphans:2;widows:2}
      strong{font-weight:bold} em{font-style:italic}
      hr{border:0;border-top:1pt solid #d7dddf;margin:22pt 0}
      .edition{font:8pt/1.65 Lato,sans-serif;color:#6d797f;border-top:.6pt solid #dee3e5;padding-top:10pt;margin-top:20pt}
      a{color:#286cb8}
    '''
    book_html=f'''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><title>On the People We Never Meet — Letters from H No. 01</title><style>{css}</style></head><body>
    <div class="cover"><img alt="Cover: On the People We Never Meet by H" src="{COVER.with_suffix('.png').as_uri()}"></div>
    <div class="start"><div class="eyebrow">Letters from H · No. 01</div><h1>On the People We Never Meet</h1><p class="subtitle">A letter on unseen lives and shared responsibility · H</p></div>
    {article}<p class="edition">The Book of Chance · Letters from H · BOC-LFH-001<br>Editorial candidate, version {META["edition"]} · Revised 22 November 2026<br>Free to read and share by linking to the published source. No membership or payment required.</p>
    </body></html>'''
    HTML(string=book_html,base_url=ROOT.as_uri()+'/').write_pdf(str(PDF), pdf_variant='pdf/ua-1')
    set_pdf_info(PDF,'On the People We Never Meet','Letters from H · No. 01')
    epub_css=ROOT/'source/letters/epub-letter.css'
    epub_css.write_text('body{font-family:serif;line-height:1.65;color:#26313b}h1,h2,h3{font-weight:normal}h2{margin-top:1.6em;color:#172633}h3{font-variant:small-caps;color:#286cb8}p{margin:.85em 0}hr{border:0;border-top:1px solid #ccc}\n','utf-8')
    cmd=['pandoc',str(LETTER),'-f','markdown','-t','epub3','--standalone','--metadata=title:On the People We Never Meet','--metadata=author:H','--metadata=lang:en-NZ','--metadata=subtitle:Letters from H · No. 01','--epub-cover-image',str(COVER.with_suffix('.png')),'--css',str(epub_css),'-o',str(EPUB)]
    subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print('LETTER OUTPUTS', PDF.name, EPUB.name, COVER.name)

if __name__=='__main__': build()


# Letter 002 is built independently so subsequent updates never regenerate or silently
# revise the approved/candidate files for Letter 001. Shared house colours and type
# system are inherited; all body text comes exclusively from the canonical Markdown.
def build_letter_002():
    import json, re
    from io import BytesIO
    from PIL import Image
    from weasyprint import HTML
    import cairosvg, mistune, subprocess

    item = next(x for x in json.loads((ROOT/'source/letters/catalogue.json').read_text('utf8'))['available'] if x['number']==2)
    path = ROOT/item['file']
    pdf = ROOT/item['pdf']
    epub = ROOT/item['epub']
    cover = ROOT/item['cover']
    svgpath = ROOT/'source/letters/lfh-002-cover.svg'
    pdf.parent.mkdir(parents=True, exist_ok=True)
    cover.parent.mkdir(parents=True, exist_ok=True)

    # Preserve approved Letter 02 cover; never regenerate an older variant.
    check_cover('letter-02')
    md = mistune.create_markdown(escape=True, plugins=['table','strikethrough','url'])
    article = md(path.read_text('utf8'))
    article = re.sub(r'<h1>.*?</h1>','',article,count=1,flags=re.S)
    article = re.sub(r'<p><em>Letters from H · No. 02</em></p>','',article,count=1)
    article = article.replace('<hr />','<hr>')
    css = '''
    @page{size:6in 9in;margin:.80in .72in .73in .72in;
      @top-center{content:"LETTERS FROM H  ·  NO. 02";font-family:Lato,sans-serif;font-size:7pt;letter-spacing:1.4pt;color:#77848d;}
      @bottom-center{content:counter(page);font-family:Lato,sans-serif;font-size:8pt;color:#77848d;}}
    @page cover{margin:0;@top-center{content:none}@bottom-center{content:none}}
    body{font:11.4pt/1.61 'Liberation Serif',Georgia,serif;color:#26313b;margin:0;background:white}
    .cover{page:cover;break-after:page;margin:0;width:6in;height:9in}
    .cover img{width:6in;height:9in;object-fit:cover;display:block}
    h1{font:normal 24pt/1.18 'Liberation Serif',serif;color:#172633;margin:0 0 15pt}
    .eyebrow{font:700 8pt Lato,sans-serif;letter-spacing:1.8pt;color:#286cb8;text-transform:uppercase;margin-bottom:15pt}
    .subtitle{font:italic 11.5pt/1.5 'Liberation Serif',serif;color:#62717b;margin:0 0 27pt}
    .start{margin-top:8pt}
    .start::after{content:'';display:block;border-bottom:.7pt solid #d6dce0;margin:0 0 24pt}
    p{margin:0 0 11pt;orphans:3;widows:3}
    h2{font:normal 16pt/1.18 'Liberation Serif',serif;margin:26pt 0 12pt;color:#172633;break-after:avoid}
    h3{font:700 8.5pt/1.5 Lato,sans-serif;letter-spacing:1.3pt;margin:22pt 0 12pt;color:#286cb8;text-transform:uppercase;break-after:avoid}
    ul{padding-left:18pt;margin-bottom:15pt}li{margin-bottom:9pt;orphans:2;widows:2}
    strong{font-weight:bold}em{font-style:italic}
    hr{border:0;border-top:1pt solid #d7dddf;margin:22pt 0}
    .edition{font:8pt/1.65 Lato,sans-serif;color:#6d797f;border-top:.6pt solid #dee3e5;padding-top:10pt;margin-top:20pt}
    a{color:#286cb8}
    '''
    source_html=f'''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><title>{item['title']} — Letters from H No. 02</title><style>{css}</style></head><body>
    <div class="cover"><img alt="Cover: When Good Choices Lead to Bad Outcomes by H" src="{cover.with_suffix('.png').as_uri()}"></div>
    <div class="start"><div class="eyebrow">Letters from H · No. 02</div><h1>{item['title']}</h1><p class="subtitle">{item['subtitle']} · H</p></div>
    {article}<p class="edition">The Book of Chance · Letters from H · BOC-LFH-002<br>Editorial candidate, version {item['edition']} · Prepared 22 November 2026<br>Free to read or download without membership or payment. Share a link to the original source.</p></body></html>'''
    HTML(string=source_html,base_url=ROOT.as_uri()+'/').write_pdf(str(pdf),pdf_variant='pdf/ua-1')
    set_pdf_info(pdf,item['title'],'Letters from H · No. 02')
    css_path=ROOT/'source/letters/epub-letter.css'
    subprocess.run(['pandoc',str(path),'-f','markdown','-t','epub3','--standalone',
        '--metadata=title:'+item['title'],'--metadata=author:H','--metadata=lang:en-NZ',
        '--metadata=subtitle:Letters from H · No. 02','--epub-cover-image',str(cover.with_suffix('.png')),
        '--css',str(css_path),'-o',str(epub)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print('LETTER 002 GENERATED', pdf, epub, cover)
