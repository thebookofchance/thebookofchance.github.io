"""Reproducible illustrator, typesetter and EPUB packager for The Five Values.

Editorial candidate only. Run intentionally following any manuscript revision;
normal site rebuilds do not overwrite existing PDF and EPUB publications.
"""
from pathlib import Path
from io import BytesIO
import html, os, re, subprocess
import mistune
import cairosvg
from PIL import Image
from weasyprint import HTML
from approved_cover_assets import check_cover
from pdf_release_metadata import set_pdf_info

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'files/booklets'
ART=ROOT/'assets/booklets'
SOURCE=ROOT/'source/booklets/the-five-values.md'
PAPER='#FAFAF7'; WHITE='#FFFFFF'; CHAR='#26313B'; INK='#172633'; BLUE='#286CB8'; GRAY='#9EACB5'; LT='#D6DEE2'


def svg_wrap(content,w=960,h=420):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{WHITE}"/>{content}</svg>'

def path(d,color=CHAR,width=2.4,opacity=1,dash=None):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'

def circle(x,y,r,color=CHAR,fill='white',width=2):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="{width}"/>'

def render_art():
    ART.mkdir(exist_ok=True,parents=True)
    diagrams={}
    # Hope: an unexpectedly available route, not guaranteed success.
    diagrams['hope']=''.join([
        path('M 30 360 C 155 306 205 130 380 170 S 660 265 930 122',CHAR,2.5,.67),
        path('M 30 290 C 165 325 250 350 400 264 S 670 100 930 260',CHAR,2.5,.57),
        path('M 30 225 C 177 200 215 280 380 315 S 655 370 930 330',GRAY,2.3,.78),
        path('M 30 346 C 165 272 208 220 360 203 S 660 107 930 73',BLUE,4,.94),
        circle(360,203,6,BLUE,BLUE,1),
    ])
    # Acceptance: boundary + accessible detour, with the obstruction remaining evident.
    diagrams['acceptance']=''.join([
        path('M 28 205 L 407 205',CHAR,2.8),path('M 550 205 L 930 205',CHAR,2.8),
        path('M 407 94 L 407 310',CHAR,3,.55),path('M 550 94 L 550 310',CHAR,3,.55),
        path('M 28 205 C 230 205 360 205 400 205 C 420 205 430 365 480 365 C 540 365 539 205 565 205 S 800 205 930 205',BLUE,3.7),
        path('M 428 92 L 530 92',GRAY,2),path('M 428 312 L 530 312',GRAY,2),
        circle(480,365,5,BLUE,BLUE,1)
    ])
    # Reflection: open orbits, not a closed loop or spiral of rumination.
    r=''
    for j in range(5):
        rr=55+j*30
        r+=path(f'M {480-rr} 210 C {480-rr} {210-rr*1.08} {480+rr*.7} {210-rr*1.05} {480+rr} 210 C {480+rr*1.08} {210+rr*.68} {480-rr*.5} {210+rr*1.1} {480-rr*.65} {210+rr*.38}', BLUE if j==2 else CHAR,3 if j==2 else 2,.9 if j==2 else .55)
    diagrams['reflection']=r+path('M 480 210 C 555 215 623 253 675 306',BLUE,3.2)+circle(480,210,8,BLUE,WHITE,2.8)
    # Growth: equal-height variations, each takes different branching form rather than ranking.
    growth=''
    for j,x in enumerate((128,300,472,644,816)):
        yy=282
        growth+=path(f'M {x} 354 Q {x-10*(j%2)} 306 {x} {yy} Q {x+16*(j%2)} 230 {x} 166',CHAR,2.7,.75)
        opts=[(x-45,125,x+20,98),(x-28,152,x+55,133),(x-60,175,x+36,112),(x-38,118,x+25,149),(x-55,135,x+50,118)]
        xl,yl,xr,yr=opts[j]
        growth+=path(f'M {x} 212 Q {x-18} 165 {xl} {yl}', BLUE if j in (1,4) else CHAR,2.8,.8)
        growth+=path(f'M {x} 188 Q {x+20} 140 {xr} {yr}', BLUE if j in (0,3) else CHAR,2.8,.8)
        growth+=circle(xl,yl,4,BLUE if j in (1,4) else CHAR,WHITE,2)
        growth+=circle(xr,yr,4,BLUE if j in (0,3) else CHAR,WHITE,2)
    diagrams['growth']=growth
    # Community: independent nodes can connect and keep their distinctness.
    coords=[(100,135),(240,235),(347,95),(460,286),(510,160),(645,95),(700,280),(825,170),(880,325)]
    edges=[(0,1),(1,2),(1,3),(2,4),(3,4),(4,5),(4,6),(5,7),(6,7),(6,8)]
    comp=''
    for k,(a,b) in enumerate(edges):
        xa,ya=coords[a];xb,yb=coords[b]
        comp+=path(f'M {xa} {ya} Q {(xa+xb)/2} {(ya+yb)/2 + (21 if k%2 else -19)} {xb} {yb}', BLUE if k in (2,7) else CHAR,3.3 if k in (2,7) else 2.0,1 if k in (2,7) else .53)
    for idx,(x,y) in enumerate(coords):comp+=circle(x,y,7,BLUE if idx in (3,7) else CHAR,WHITE,2.2)
    diagrams['community']=comp
    # Five equal streams towards an open central space; no one value rules the others.
    center=(480,210);import math
    comp=''
    for j in range(5):
        angle=2*math.pi*(j/5)-math.pi/2
        x=center[0]+174*math.cos(angle);y=center[1]+174*math.sin(angle)
        inner_x=center[0]+68*math.cos(angle);inner_y=center[1]+68*math.sin(angle)
        cx=center[0]+108*math.cos(angle+.13);cy=center[1]+108*math.sin(angle+.13)
        comp+=path(f'M {x:.1f} {y:.1f} Q {cx:.1f} {cy:.1f} {inner_x:.1f} {inner_y:.1f}', BLUE if j==0 else CHAR,3 if j==0 else 2.4,.88)
        comp+=circle(x,y,6,BLUE if j==0 else CHAR,WHITE,2)
    comp+=circle(480,210,38,LT,'white',1.9)
    diagrams['values-in-conversation']=comp
    for name,content in diagrams.items():
        svg=svg_wrap(content)
        (ART/f'{name}.svg').write_text(svg,encoding='utf8')
        cairosvg.svg2png(bytestring=svg.encode('utf8'),write_to=str(ART/f'{name}.png'),output_width=1600,output_height=700)
    return diagrams


def render_cover():
    """Retain the approved series cover; never regenerate an old design."""
    return check_cover('five-values')


def build():
    DEST.mkdir(parents=True,exist_ok=True)
    render_art();check_cover('five-values')
    md=SOURCE.read_text('utf8')
    h=mistune.create_markdown(escape=True,plugins=['table','strikethrough','url'])(md)
    # Remove cover material, which has been typeset more deliberately as the PDF cover/intro.
    h=re.sub(r'^<h1>.*?</h1>', '',h,flags=re.S)
    h=re.sub(r'^\s*<p><em>Hope.*?</p>','',h,flags=re.S)
    h=re.sub(r'^\s*<p><em>A companion.*?</p>','',h,flags=re.S)
    # This markdown body will also be embedded directly in the website from the source file.
    h=h.replace('<h2>','<h2 class="booklet-section">')
    # wrap inline illustrations to avoid page split; add aria text by mistune.
    h=re.sub(r'<p>(<img [^>]+>)</p>',r'<figure>\1</figure>',h)
    cover=(ART/'the-five-values-cover.png').as_uri()
    # EPUB illustrations source links are relative to SOURCE; PDF base URL handles them.
    css=r'''
      @page{size:6in 9in;margin:.78in .70in .73in .70in;
       @top-center{content:"THE FIVE VALUES  ·  H";font:8pt Lato,sans-serif;letter-spacing:1.4pt;color:#78858D;}
       @bottom-center{content:counter(page);font:8.2pt Lato,sans-serif;color:#78858D;}}
      @page cover{margin:0;@top-center{content:none}@bottom-center{content:none}}
      body{font:10.85pt/1.49 'Liberation Serif',Georgia,serif;color:#26313B;margin:0;background:white;}
      .cover{page:cover;width:6in;height:9in;margin:0;break-after:page}
      .cover img{width:100%;height:100%;display:block}
      .opening{font-size:10pt;color:#7b858e;letter-spacing:1.6pt;text-transform:uppercase;font-family:Lato,sans-serif;margin:2pt 0 11pt}
      p{margin:0 0 8.7pt;orphans:3;widows:3}
      h2.booklet-section{font:normal 20pt/1.15 'Liberation Serif',serif;color:#172633;margin:23pt 0 14pt;break-after:avoid;}
      h2.booklet-section:nth-of-type(1){font-size:24pt;margin-top:18pt}
      h2.booklet-section:not(:first-of-type){break-before:page;margin-top:5pt}
      blockquote{margin:17pt 2pt 21pt;padding:14pt 16pt;background:#FAFAF7;border-left:2pt solid #286CB8;font:italic 10.5pt/1.65 'Liberation Serif',serif}
      blockquote p{margin:0}
      figure{margin:12pt 0 12pt;break-inside:avoid}
      figure img{max-width:100%;max-height:102pt;object-fit:contain;display:block;margin:auto}
      em{font-style:italic}strong{font-weight:bold}
      h2+p em{font:italic 11.5pt 'Liberation Serif',serif;color:#596B78}
      ol,ul{padding-left:18pt;margin:8pt 0 16pt}li{margin:0 0 9pt;orphans:2;widows:2}
      li::marker{color:#286CB8}a{color:#286CB8}
      .closing{border-top:1pt solid #CED8DC;margin-top:24pt;padding-top:12pt;font:8.2pt/1.6 Lato,sans-serif;color:#64747d}
    '''
    pdfpage=f'''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><title>The Five Values — H</title><style>{css}</style></head><body><div class="cover"><img alt="The Five Values cover" src="{cover}"/></div><div class="opening">The Book of Chance · Companion 01</div>{h}</body></html>'''
    pdf_path=DEST/'The_Five_Values.pdf'
    HTML(string=pdfpage,base_url=SOURCE.parent.as_uri()+'/').write_pdf(str(pdf_path),pdf_variant='pdf/ua-1')
    set_pdf_info(pdf_path,'The Five Values','Hope, Acceptance, Reflection, Growth and Community')
    css_epub=ROOT/'source/booklets/booklet-epub.css'
    css_epub.write_text('body { font-family: serif; line-height: 1.6; color: #26313B; } h1,h2 { color:#172633; } h2 { margin-top: 2em; } blockquote { border-left: 2px solid #286CB8; padding-left: 1em; } img { max-width: 100%; height: auto; }',encoding='utf8')
    epub_path=DEST/'The_Five_Values.epub'
    cmd=['pandoc',str(SOURCE),'-f','markdown','-t','epub3','--standalone',
      '--metadata=title:The Five Values','--metadata=author:H','--metadata=lang:en-NZ',
      '--metadata=description:Five values for living thoughtfully within uncertainty, a companion to The Book of Chance.',
      '--metadata=rights:Free public reading and download. Contact publisher for republication permissions.',
      '--epub-cover-image',str(ART/'the-five-values-cover.png'),
      '--resource-path',str(SOURCE.parent)+os.pathsep+str(ROOT),
      '--css',str(css_epub),'-o',str(epub_path)]
    result=subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if result.stderr.strip():print('Pandoc messages:',result.stderr[:900])
    print('built',pdf_path,pdf_path.stat().st_size,epub_path,epub_path.stat().st_size)

if __name__=='__main__':build()
