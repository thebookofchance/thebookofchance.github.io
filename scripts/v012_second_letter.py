"""Website v0.12: integrate Letters from H No. 02 after source-driven v0.10 page generation.

Retains Letter 001 and all existing art, books, forms and journals without content edits.
"""
import json, html
from pathlib import Path
from bs4 import BeautifulSoup
from build_letters import build_letter_002


def apply_v012(root: Path, document, markdown, info: dict):
    # Do not regenerate a previous issue as a side-effect of rebuilding the site.
    old = json.loads((root/'source/letters/catalogue.json').read_text('utf8'))['available'][1]
    if not all((root/old[k]).is_file() for k in ('pdf', 'epub', 'cover')):
        build_letter_002()
    cat = json.loads((root/'source/letters/catalogue.json').read_text('utf8'))
    assert [e['number'] for e in cat['available']][:2]==[1,2]
    entry = cat['available'][1]
    label = html.escape(entry['title'])
    lead = html.escape(entry['lead'])
    summary = html.escape(entry['summary'])
    essay = BeautifulSoup(markdown((root/entry['file']).read_text('utf8')),'html.parser')
    if essay.h1: essay.h1.decompose()
    p = essay.find('p')
    if p and 'Letters from H · No. 02' in p.get_text(' ',strip=True): p.decompose()
    for link in essay.find_all('a',href=True):
        if link['href'].startswith('https://'):
            link['target']='_blank'
            link['rel']='noopener noreferrer'

    page_body = f'''<div class="shell letters-reading-top"><a class="back-to-toc" href="../">← All Letters from H</a><a class="back-to-toc" href="../../downloads/#letters-from-h">The Library</a></div>
    <header class="shell letters-reading-hero"><span class="eyebrow">Letters from H · No. 02</span><h1>{label}</h1><p class="lead">{lead}</p><p class="letters-meta">By H · Prepared 22 November 2026 · Editorial candidate {html.escape(entry['edition'])}</p></header>
    <div class="shell letters-reading-layout"><article class="reading-body letters-prose" aria-label="Full text of Letter 02">{str(essay)}</article><aside class="letters-side"><span class="eyebrow">This letter</span><p>A complete, freely available essay about choice and responsibility. This is a reflective argument, not an additional foundational teaching.</p><img src="../../{entry['cover']}" alt="Cover of Letter 02, with fine charcoal and blue paths branching from a shared origin" width="1000" height="1500" loading="lazy"><a class="btn btn-primary" href="../../{entry['pdf']}" download>Download PDF ↓</a><a class="btn btn-outline" href="../../{entry['epub']}" download>Download EPUB ↓</a><a class="text-link" href="../../read/action-within-uncertainty/">Related: Action Within Uncertainty ↗</a></aside></div>
    <section class="shell letters-postscript"><div><span class="eyebrow">Continue reading</span><h2>A larger conversation.</h2><p>The first two Letters explore different kinds of responsibility: toward people we never meet, and after decisions whose outcomes we cannot control.</p></div><a class="btn btn-outline" href="../">Explore the series →</a></section>'''
    destination = root/'letters'/entry['slug']/'index.html'
    destination.parent.mkdir(exist_ok=True,parents=True)
    destination.write_text(document(entry['title'],page_body,base='../../',active='downloads',desc=entry['summary'],extra_head=f'<link rel="canonical" href="https://thebookofchance.github.io/{entry["url"]}">'),encoding='utf8')

    # The v0.10 generator creates both issue cards from the series catalogue.
    archive = root/'letters/index.html'
    a = BeautifulSoup(archive.read_text('utf8'),'html.parser')
    foot=a.select_one('.letters-series-foot')
    assert foot and len(a.select('.letters-index-feature'))>=2
    foot.select_one('p').string='A third Letter, What Do We Owe to Strangers?, is planned but not yet published. Each issue will be offered freely when it is ready; no release timetable is promised.'
    archive.write_text(str(a),encoding='utf8')

    library=root/'downloads/index.html'
    b=BeautifulSoup(library.read_text('utf8'),'html.parser')
    section=b.select_one('.letters-feature-library')
    assert section
    head=section.select_one('.letters-library-head')
    head.select_one('.eyebrow').string='The collection · Letters from H'
    head.select_one('p').string='Two complete, free philosophical letters. Each examines a question raised by The Book of Chance and can be read independently.'
    # The main featured card becomes the latest issue. Letter 01 receives its own link below.
    first=section.select_one('.letters-library-card')
    assert first
    feature=BeautifulSoup(f'''<article class="letters-library-card"><img src="../{entry['cover']}" alt="Cover of Letter 02, with fine branching paths" loading="lazy" width="1000" height="1500"><div><span class="eyebrow">No. 02 · Latest letter</span><h3>{label}</h3><p>{summary}</p><div class="button-line"><a class="btn btn-primary" href="../{entry['url']}">Read online →</a><a class="btn btn-outline" href="../{entry['pdf']}" download>PDF ↓</a><a class="btn btn-outline" href="../{entry['epub']}" download>EPUB ↓</a></div><a class="text-link" href="../letters/">Read both Letters →</a></div></article>''','html.parser').article
    first.replace_with(feature)
    # Place a non-redundant link to previous issue below featured card.
    prev = cat['available'][0]
    older = BeautifulSoup(f'''<p class="letters-previous-link"><strong>Also available:</strong> <a href="../{prev['url']}">No. 01 — {html.escape(prev['title'])} →</a></p>''','html.parser').p
    feature.insert_after(older)
    count=b.select_one('.library-count')
    if count:
        count.select_one('span').string='03'
        small=count.select_one('small')
        if small: small.string='The foundational book + two Letters · Plus free journals and worksheets'
    library.write_text(str(b),encoding='utf8')

    homepage=root/'index.html'
    h=BeautifulSoup(homepage.read_text('utf8'),'html.parser')
    feature=h.select_one('.letters-home-feature')
    assert feature
    feature.select_one('.eyebrow').string='New writing · Letters from H / 02'
    feature.select_one('h2').string='What if a careful choice ends badly?'
    feature.select_one('p').string=entry['lead']
    primary=feature.select_one('a.btn')
    assert primary
    primary['href']=entry['url']
    primary.string='Read the second Letter →'
    cover=feature.select_one('img')
    cover['src']=entry['cover']
    cover['alt']='Cover of Letters from H No. 02: When Good Choices Lead to Bad Outcomes'
    homepage.write_text(str(h),encoding='utf8')

    pubpath=root/'source/publications.json'
    pub=json.loads(pubpath.read_text('utf8'))
    pub['letters']={'series':'Letters from H','index':'letters/','issues':[
        {k: e[k] for k in ['id','title','url','pdf','epub','status']} for e in cat['available']
    ]}
    pubpath.write_text(json.dumps(pub,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

    smpath=root/'sitemap.xml'
    sitemap=smpath.read_text('utf8')
    url='https://thebookofchance.github.io/'+entry['url']
    if url not in sitemap:
        sitemap=sitemap.replace('</urlset>',f'<url><loc>{url}</loc></url>\n</urlset>')
    smpath.write_text(sitemap,encoding='utf8')
    info.update({'website_version':'0.12', 'letters_series_available':2,
       'letters_series_status':'Two editorial candidates; H approval and live testing pending',
       'latest_letter_id':entry['id'],'latest_letter_edition':entry['edition']})
