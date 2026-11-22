"""Build PDF and EPUB exports for Conversations of Chance.

This creates a publication-style PDF that includes the dedicated cover, and an
EPUB that uses the same cover asset.
"""
from pathlib import Path
import subprocess, zipfile, re
from bs4 import BeautifulSoup
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source/conversations/conversations-of-chance.md'
PDF = ROOT / 'files/conversations/Conversations_of_Chance_Editorial_Proof_v0.1.pdf'
EPUB = ROOT / 'files/conversations/Conversations_of_Chance_Editorial_Proof_v0.1.epub'
COVER_PNG = ROOT / 'assets/publications/conversations-of-chance-cover.png'
COVER_SVG = ROOT / 'assets/publications/conversations-of-chance-cover.svg'
WORK = ROOT / '_build_conversations'
WORK.mkdir(parents=True, exist_ok=True)


def markdown_to_html(md_text: str) -> str:
    src = WORK / 'conversations_body.md'
    src.write_text(md_text, encoding='utf8')
    res = subprocess.run([
        'pandoc', str(src), '-f', 'markdown+smart', '-t', 'html5', '--wrap=none'
    ], capture_output=True, text=True, check=True)
    return res.stdout


def build_pdf() -> int:
    text = SOURCE.read_text('utf8')
    start = text.index('## A Note on This Edition\n')
    body_md = text[start:]
    html = markdown_to_html(body_md)
    soup = BeautifulSoup(html, 'html.parser')

    for hr in soup.find_all('hr'):
        hr['class'] = ['conv-divider']
    for h in soup.find_all(['h1', 'h2', 'h3']):
        label = h.get_text(' ', strip=True)
        if h.name == 'h1':
            h['class'] = ['conv-part-heading']
        elif h.name == 'h2' and label.startswith('Conversation '):
            h['class'] = ['conv-session-heading']
        elif h.name == 'h2':
            h['class'] = ['conv-section-heading']
        elif h.name == 'h3':
            h['class'] = ['conv-reading-link']
    for p in soup.find_all('p'):
        txt = p.get_text(' ', strip=True)
        if txt == '— H':
            p['class'] = ['conv-signoff']
        if txt.startswith('Editorial record'):
            p['class'] = ['conv-editorial-record']

    css = '''
    @page { size: 6in 9in; margin: .78in .72in .74in .72in;
      @top-center{content:"CONVERSATIONS OF CHANCE";font-family:Lato,Arial,sans-serif;font-size:7pt;letter-spacing:1.4pt;color:#77848d;}
      @bottom-center{content:counter(page);font-family:Lato,Arial,sans-serif;font-size:8pt;color:#77848d;}
    }
    @page cover { margin:0; @top-center{content:none} @bottom-center{content:none} }
    body{font:11.1pt/1.58 "Liberation Serif",Georgia,serif;color:#26313b;margin:0;background:white}
    .cover{page:cover;break-after:page;margin:0;width:6in;height:9in}
    .cover img{width:6in;height:9in;object-fit:cover;display:block}
    .title-page{break-after:page;padding:.1in 0 0 0}
    .eyebrow{font:700 8pt Lato,Arial,sans-serif;letter-spacing:1.8pt;color:#286cb8;text-transform:uppercase;margin:0 0 14pt}
    h1.page-title{font:normal 25pt/1.08 "Liberation Serif",Georgia,serif;color:#172633;margin:0 0 10pt}
    .subtitle{font:italic 12pt/1.45 "Liberation Serif",Georgia,serif;color:#62717b;margin:0 0 16pt}
    .front-meta,.front-note{font-size:10.1pt;line-height:1.6;color:#51606a;margin:0 0 12pt}
    .front-rule{border:0;border-top:.8pt solid #d8dee2;margin:18pt 0 16pt}
    p{margin:0 0 11pt;orphans:3;widows:3}
    ul,ol{margin:0 0 14pt 1.25em;padding:0} li{margin:0 0 7pt}
    h1.conv-part-heading{font:normal 18pt/1.15 "Liberation Serif",Georgia,serif;color:#172633;margin:32pt 0 15pt;break-before:page}
    h2.conv-session-heading{font:normal 17pt/1.16 "Liberation Serif",Georgia,serif;color:#172633;margin:26pt 0 10pt;break-before:page}
    h2.conv-section-heading{font:normal 15.5pt/1.2 "Liberation Serif",Georgia,serif;color:#172633;margin:26pt 0 10pt;break-after:avoid}
    h3.conv-reading-link{font:700 8.3pt/1.55 Lato,Arial,sans-serif;letter-spacing:1.25pt;color:#286cb8;text-transform:uppercase;margin:0 0 12pt;break-after:avoid}
    strong{font-weight:700} em{font-style:italic}
    blockquote{margin:14pt 0 16pt;padding:0 0 0 14pt;border-left:2pt solid #d5dce0;color:#41505a}
    .conv-divider{border:0;border-top:1pt solid #d7dddf;margin:22pt 0}
    .conv-signoff{font-style:italic}
    .conv-editorial-record{font-size:9.2pt;line-height:1.55;color:#5d6a72;border-top:.7pt solid #dce2e5;padding-top:10pt;margin-top:18pt}
    a{color:#286cb8;text-decoration:none}
    cite{font-style:italic}
    '''

    title_page = f'''<div class="cover"><img alt="" src="{COVER_SVG.as_uri()}"></div>
    <div class="title-page"><div class="eyebrow">The Book of Chance · Discussion companion 01</div>
    <h1 class="page-title">Conversations of Chance</h1>
    <p class="subtitle">Twelve Discussions for an Uncertain Life · H</p>
    <p class="front-meta">Editorial proof v0.1 · Prepared 22 November 2026</p>
    <hr class="front-rule">
    <p class="front-note">A discussion companion to <cite>The Book of Chance</cite>. This edition is designed for private reading, informal discussion and editorial review. It includes twelve stand-alone conversations, an open ending, a one-page host's reference and authorship notes.</p>
    <p class="front-note">The thought experiments are fictional and are included to help readers examine ideas rather than to report events. No registration, donation or membership is required to read or share the publication links.</p>
    </div>'''
    page = f'<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><title>Conversations of Chance — editorial proof</title><style>{css}</style></head><body>{title_page}{str(soup)}</body></html>'
    HTML(string=page, base_url=ROOT.as_uri() + '/').write_pdf(str(PDF))
    info = subprocess.run(['pdfinfo', str(PDF)], capture_output=True, text=True, check=True).stdout
    m = re.search(r'^Pages:\s+(\d+)', info, flags=re.M)
    return int(m.group(1))


def build_epub() -> None:
    epub_css = WORK / 'conversations_epub.css'
    epub_css.write_text('''html{font-family:serif;line-height:1.5;color:#23272b}body{margin:4%}h1{font-weight:normal;font-size:1.65em;line-height:1.14;margin:1.55em 0 .75em;page-break-before:always}h2{font-weight:normal;font-size:1.28em;line-height:1.2;margin:1.35em 0 .6em;page-break-after:avoid}h3{font-size:.9em;letter-spacing:.04em;text-transform:uppercase;color:#285f9a;margin:0 0 .8em}p{margin:0 0 .78em;text-align:left;orphans:2;widows:2}blockquote{margin:1em 4%;padding-left:.8em;border-left:1px solid #aaa}li{margin-bottom:.4em}a{color:inherit}img{max-width:100%;height:auto;display:block;margin:.8em auto}hr{border:none;border-top:1px solid #cdd4d8;margin:1.4em 0}cite{font-style:italic}''', encoding='utf8')
    subprocess.run([
        'pandoc', str(SOURCE), '-f', 'markdown+smart', '-t', 'epub3', '--standalone',
        '--toc', '--toc-depth=2', '--split-level=1', '--epub-title-page=true',
        '--metadata=title:Conversations of Chance', '--metadata=subtitle:Twelve Discussions for an Uncertain Life',
        '--metadata=author:H', '--metadata=lang:en-NZ', '--metadata=rights:Editorial proof; public review edition.',
        '--epub-cover-image', str(COVER_PNG), '--css', str(epub_css), '-o', str(EPUB)
    ], capture_output=True, text=True, check=True)
    assert zipfile.ZipFile(EPUB).testzip() is None


def main():
    PDF.parent.mkdir(parents=True, exist_ok=True)
    EPUB.parent.mkdir(parents=True, exist_ok=True)
    pages = build_pdf()
    build_epub()
    print(f'Built {PDF.name} ({pages} pages) and {EPUB.name}')


if __name__ == '__main__':
    main()
