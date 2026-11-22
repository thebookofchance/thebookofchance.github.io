from pathlib import Path
import subprocess, json, re, html
from PIL import Image
from io import BytesIO
import cairosvg
import mistune
from weasyprint import HTML

ROOT=Path(__file__).resolve().parents[1]
LETTER=ROOT/'source/letters/001-on-the-people-we-never-meet.md'
META=json.loads((ROOT/'source/letters/catalogue.json').read_text(encoding='utf-8'))['available'][0]
PDF=ROOT/META['pdf']
EPUB=ROOT/META['epub']
COVER=ROOT/META['cover']

# An original restrained variation on the intersecting paths from the approved cover family.
def cover_svg():
    paths=[]
    for i in range(7):
        # gentle mirrored arcs, different entry heights; blue used only in one or two paths
        start=550+i*24
        end=1190-i*25
        middle=840+(i-3)*9
        col='#1e70b8' if i in (1,5) else ('#929b9d' if i%3==0 else '#24313b')
        opacity='0.9' if i in (1,5) else ('0.47' if i%3==0 else '0.78')
        paths.append(f'<path d="M -70,{start} C 280,{start+140} 425,{middle-105} 650,{middle} S 1010,{end-155} 1090,{end}" fill="none" stroke="{col}" stroke-width="{2.1 if i in (1,5) else 1.35}" opacity="{opacity}"/>')
        paths.append(f'<path d="M 1090,{start} C 760,{start+140} 610,{middle-105} 410,{middle} S 120,{end-155} -70,{end}" fill="none" stroke="{col}" stroke-width="{2.1 if i in (1,5) else 1.35}" opacity="{opacity}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1500" viewBox="0 0 1000 1500">
    <rect width="1000" height="1500" fill="#fff"/>
    <text x="500" y="120" fill="#286cb8" font-family="Lato, sans-serif" font-size="24" letter-spacing="6" text-anchor="middle">LETTERS FROM H</text>
    <text x="500" y="205" fill="#69757a" font-family="Lato, sans-serif" font-size="20" letter-spacing="4" text-anchor="middle">NO. 01</text>
    <text x="500" y="330" fill="#1b2933" font-family="Liberation Serif, serif" font-size="64" text-anchor="middle">On the People</text>
    <text x="500" y="425" fill="#1b2933" font-family="Liberation Serif, serif" font-size="64" text-anchor="middle">We Never Meet</text>
    <g>{''.join(paths)}</g>
    <text x="500" y="1290" fill="#394853" font-family="Liberation Serif, serif" font-style="italic" font-size="29" text-anchor="middle">A letter on unseen lives and shared responsibility</text>
    <line x1="451" y1="1380" x2="549" y2="1380" stroke="#286cb8" stroke-width="2"/>
    <text x="500" y="1440" fill="#24313b" font-family="Liberation Serif, serif" font-size="45" text-anchor="middle">H</text>
    </svg>'''

def build():
    PDF.parent.mkdir(parents=True,exist_ok=True)
    COVER.parent.mkdir(parents=True,exist_ok=True)
    source=LETTER.read_text(encoding='utf-8')
    svg=cover_svg()
    svg_path=ROOT/'source/letters/lfh-001-cover.svg'
    svg_path.write_text(svg, encoding='utf-8')
    raw_png=cairosvg.svg2png(bytestring=svg.encode('utf-8'),output_width=1000,output_height=1500)
    image=Image.open(BytesIO(raw_png)).convert('RGB')
    image.save(COVER,'WEBP',quality=91,method=6)
    image.save(COVER.with_suffix('.png'),'PNG',optimize=True)
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
    book_html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>On the People We Never Meet — Letters from H No. 01</title><style>{css}</style></head><body>
    <div class="cover"><img alt="" src="{svg_path.as_uri()}"></div>
    <div class="start"><div class="eyebrow">Letters from H · No. 01</div><h1>On the People We Never Meet</h1><p class="subtitle">A letter on unseen lives and shared responsibility · H</p></div>
    {article}<p class="edition">The Book of Chance · Letters from H · BOC-LFH-001<br>Editorial candidate, version {META["edition"]} · Revised 22 November 2026<br>Free to read and share by linking to the published source. No membership or payment required.</p>
    </body></html>'''
    HTML(string=book_html,base_url=ROOT.as_uri()+'/').write_pdf(str(PDF),metadata={'title':'On the People We Never Meet'})
    epub_css=ROOT/'source/letters/epub-letter.css'
    epub_css.write_text('body{font-family:serif;line-height:1.65;color:#26313b}h1,h2,h3{font-weight:normal}h2{margin-top:1.6em;color:#172633}h3{font-variant:small-caps;color:#286cb8}p{margin:.85em 0}hr{border:0;border-top:1px solid #ccc}\n','utf-8')
    cmd=['pandoc',str(LETTER),'-f','markdown','-t','epub3','--standalone','--metadata=title:On the People We Never Meet','--metadata=author:H','--metadata=lang:en-NZ','--metadata=subtitle:Letters from H · No. 01','--epub-cover-image',str(COVER.with_suffix('.png')),'--css',str(epub_css),'-o',str(EPUB)]
    subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print('LETTER OUTPUTS', PDF.name, EPUB.name, COVER.name)

if __name__=='__main__': build()
