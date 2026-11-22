"""Independent source-to-PDF/EPUB build for Letters from H No. 03.

Do not call this on routine website rebuilds once assets exist: intentionally avoid
silently revising previously produced publications.
"""
from pathlib import Path
import json, re, subprocess
from io import BytesIO
from PIL import Image
from weasyprint import HTML
from approved_cover_assets import check_cover
from pdf_release_metadata import set_pdf_info
import cairosvg, mistune

ROOT=Path(__file__).resolve().parents[1]

def build_letter_003():
    item=next(x for x in json.loads((ROOT/'source/letters/catalogue.json').read_text('utf8'))['available'] if x['number']==3)
    path=ROOT/item['file']
    pdf=ROOT/item['pdf']
    epub=ROOT/item['epub']
    cover=ROOT/item['cover']
    svgpath=ROOT/'source/letters/lfh-003-cover.svg'
    pdf.parent.mkdir(parents=True,exist_ok=True)
    cover.parent.mkdir(parents=True,exist_ok=True)

    # Preserve approved Letter 03 cover; no fallback to old generated artwork.
    check_cover('letter-03')
    markdown=mistune.create_markdown(escape=True,plugins=['table','strikethrough','url'])
    article=markdown(path.read_text('utf8'))
    article=re.sub(r'<h1>.*?</h1>','',article,count=1,flags=re.S)
    article=re.sub(r'<p><em>Letters from H · No. 03</em></p>','',article,count=1)
    article=article.replace('<hr />','<hr>')
    css='''
      @page{size:6in 9in;margin:.80in .72in .73in .72in;
        @top-center{content:"LETTERS FROM H  ·  NO. 03";font-family:Lato,sans-serif;font-size:7pt;letter-spacing:1.4pt;color:#77848d;}
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
    from html import escape
    page=f'''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><title>{escape(item['title'])} — Letters from H No. 03</title><style>{css}</style></head><body>
        <div class="cover"><img alt="Cover: What Do We Owe to Strangers by H" src="{cover.with_suffix('.png').as_uri()}"></div>
        <div class="start"><div class="eyebrow">Letters from H · No. 03</div><h1>{escape(item['title'])}</h1><p class="subtitle">{escape(item['subtitle'])} · H</p></div>
        {article}<p class="edition">The Book of Chance · Letters from H · BOC-LFH-003<br>Editorial candidate, version {escape(item['edition'])} · Prepared 22 November 2026<br>Free to read or download without membership or payment. Share a link to the original source.</p></body></html>'''
    HTML(string=page,base_url=ROOT.as_uri()+'/').write_pdf(str(pdf),pdf_variant='pdf/ua-1')
    set_pdf_info(pdf,item['title'],'Letters from H · No. 03')
    epubcss=ROOT/'source/letters/epub-letter.css'
    subprocess.run(['pandoc',str(path),'-f','markdown','-t','epub3','--standalone',
        '--metadata=title:'+item['title'],'--metadata=author:H','--metadata=lang:en-NZ',
        '--metadata=subtitle:Letters from H · No. 03','--epub-cover-image',str(cover.with_suffix('.png')),
        '--css',str(epubcss),'-o',str(epub)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print('Letter 003 built',pdf.name,epub.name,cover.name)

if __name__=='__main__':
    build_letter_003()
