"""v0.21: Source-driven Beginner's Guide integration into the v0.20 website.

This stage runs after v020_library_refinement on every site rebuild.
Existing publication downloads, all legacy routes, form configuration, and
privacy rules stay unchanged. The guide remains an editorial candidate.
"""
from __future__ import annotations
import html
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

GUIDE_ID = 'BOC-GDE-001'
GUIDE_SLUG = 'beginners-guide-to-confluent-humanism'
GUIDE_URL = 'publications/' + GUIDE_SLUG + '/'
SOURCE = 'source/guides/' + GUIDE_SLUG + '.md'
COVER = 'assets/guides/' + GUIDE_SLUG + '-cover.webp'
COVER_PNG = 'assets/guides/' + GUIDE_SLUG + '-cover.png'
PDF = 'files/guides/A_Beginners_Guide_to_Confluent_Humanism_Editorial_Proof_v0.2.pdf'
EPUB = 'files/guides/A_Beginners_Guide_to_Confluent_Humanism_Editorial_Proof_v0.2.epub'
TITLE = "A Beginner's Guide to Confluent Humanism"
SUBTITLE = 'Chance, Choice and the Lives We Share'


def e(s):
    return html.escape(str(s), quote=True)


def slug(text):
    text = text.casefold().replace('’', "'")
    return re.sub(r'[^a-z0-9]+','-',text).strip('-')


def _build_reader(root, markdown):
    source = (root/SOURCE).read_text('utf8')
    start = source.index('## An invitation, not an entrance exam')
    body = source[start:]
    soup = BeautifulSoup(markdown(body),'html.parser')
    headings = soup.select('h2')
    assert len(headings) == 11, [(h.name,h.get_text(' ',strip=True)) for h in headings]
    seen = set()
    toc = []
    for h in headings:
        name = h.get_text(' ',strip=True)
        hid = slug(name)
        assert hid not in seen, name
        seen.add(hid)
        h['id'] = hid
        h['class'] = ['v21-guide-section', 'v21-guide-endnote' if name.lower()=='a note on this edition' else '']
        h['class'] = [x for x in h['class'] if x]
        if name.lower()=='a note on this edition':
            toc.append((hid, 'Edition note'))
        elif name=='An invitation, not an entrance exam':
            toc.append((hid, 'An invitation'))
        else:
            toc.append((hid,name))
    for h in soup.select('h3'):
        h['class'] = ['v21-guide-subhead']
    for a in soup.find_all('a',href=True):
        if a['href'].startswith('https://'):
            a['rel'] = 'noopener noreferrer'
            a['target'] = '_blank'
    return str(soup), toc


def _toc(toc):
    return '<ol>' + ''.join(f'<li><a href="#{e(href)}">{e(title)}</a></li>' for href,title in toc) + '</ol>'


def apply_v021(root:Path, document, markdown, info:dict):
    for x in (SOURCE,COVER,COVER_PNG,PDF,EPUB):
        assert (root/x).is_file(), 'Missing Beginner Guide source or asset: '+x
    art,toc = _build_reader(root, markdown)
    navigation = _toc(toc)
    hero = f'''<section class="shell v21-guide-hero">
      <div class="v21-guide-intro"><a class="back-to-toc" href="../../downloads/">← Back to the Library</a>
      <span class="eyebrow">The Book of Chance · Introductory guides</span>
      <h1>A Beginner's Guide<br>to Confluent Humanism</h1><p class="lead">{e(SUBTITLE)}</p>
      <p>New to Confluent Humanism? Start here. This short introduction explores chance, meaningful choice, five values and the proposed Fellowship—without asking you to agree, sign up or donate.</p>
      <div class="button-line"><a href="#v21-guide-text" class="btn btn-primary">Read the guide ↓</a>
       <a href="../../{PDF}" class="btn btn-outline" download>Download PDF ↓</a>
       <a href="../../{EPUB}" class="btn btn-outline" download>Download EPUB ↓</a></div>
      <p class="v21-guide-meta">By H · 13-page PDF · Free to read · Revised editorial candidate v0.2</p>
      </div>
      <img class="v21-guide-cover" src="../../{COVER}" alt="A Beginner's Guide to Confluent Humanism by H, literary cover with crossing blue and charcoal paths" width="1000" height="1500">
    </section>'''
    body = hero + f'''<div class="shell v21-guide-preamble"><strong>Begin without commitment.</strong>
      The guide introduces the philosophy while clearly distinguishing its beliefs from scientific findings and its proposed community from services that are already operating.</div>
    <details class="shell v21-guide-mobile-toc"><summary>Jump to a section</summary>{navigation}</details>
    <div class="shell v21-guide-layout" id="v21-guide-text">
      <aside class="v21-guide-toc" aria-label="Guide contents"><strong>In this guide</strong><p>Read in order or start with a question.</p>{navigation}</aside>
      <article class="v21-guide-article" aria-label="Complete text of A Beginner's Guide to Confluent Humanism">{art}</article>
    </div>
    <section class="shell v21-guide-after"><div><span class="eyebrow">Your next reading</span><h2>One beginning. Many possible paths.</h2><p>If you would like to explore further, the Library contains the foundational book, companions, original stories and reflection resources. You can follow whichever subject interests you.</p></div><a class="btn btn-outline" href="../../downloads/#publication-catalogue">Explore the Library →</a></section>'''
    dest=root/GUIDE_URL/'index.html';dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(document(TITLE,body,base='../../',active='downloads',desc='A free introduction by H to Confluent Humanism, its five values, meaningful choice, uncertainty and the proposed Fellowship of Chance.',og_image=COVER_PNG,extra_head='<link rel="canonical" href="https://thebookofchance.github.io/'+GUIDE_URL+'"><meta name="robots" content="noindex,follow">'),encoding='utf8')

    # Catalogue data is the source of truth, with existing publications left untouched.
    catalogue_file=root/'source/publications.json'
    catalogue=json.loads(catalogue_file.read_text('utf8'))
    catalogue['guides']=[{
        'id':GUIDE_ID,'title':TITLE,'subtitle':SUBTITLE,'author':'H',
        'series':'The Book of Chance — Introductory guides','edition':'v0.2',
        'status':'approved for website staging; independent review and accessibility checks outstanding',
        'language':'en-NZ','date_prepared':'2026-11-22','source':SOURCE,
        'url':GUIDE_URL,'cover':COVER,'pdf':PDF,'epub':EPUB,
        'pages_pdf':13,'sections':9
    }]
    catalogue_file.write_text(json.dumps(catalogue,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

    # After the v0.20 stage has built its compact grid, add the guide as the first
    # item (Start here) and swap a homepage promo rather than lengthen the page.
    hp=root/'index.html';home=BeautifulSoup(hp.read_text('utf8'),'html.parser')
    home_grid=home.select_one('.v20-home-grid');assert home_grid,'v0.20 homepage grid missing'
    for prior in home.select('.v21-guide-hero-link'):prior.decompose()
    for prior in home_grid.select('.v21-guide-home-card'):prior.decompose()
    for card in home_grid.select('.v20-home-card'):
        if 'What Do We Owe to Strangers?' in card.get_text(' ',strip=True):card.decompose()
    new_card=BeautifulSoup(f'''<article class="v20-home-card v21-guide-home-card">
      <a class="v20-home-cover" href="{GUIDE_URL}" aria-label="Read {e(TITLE)}"><img src="{COVER}" alt="Cover of {e(TITLE)}" loading="lazy" decoding="async" width="1000" height="1500"></a>
      <div class="v20-home-copy"><span class="v20-type">Start here · Introductory guide</span>
      <h3><a href="{GUIDE_URL}">{e(TITLE)}</a></h3><p>{e(SUBTITLE)}</p>
      <span class="v20-status">Editorial candidate · Free</span></div></article>''','html.parser').article
    home_grid.insert(0,new_card)
    hero_copy=home.select_one('.hero-copy')
    assert hero_copy,'Original hero missing'
    bridge=BeautifulSoup(f'<p class="v21-guide-hero-link">New to these ideas? <a href="{GUIDE_URL}">Start with the short beginner’s guide →</a></p>','html.parser').p
    hero_copy.append(bridge)
    discover=home.select_one('.v20-home-discover')
    if discover:
        for s in discover.select('span'):
            if 'Browse all eight' in s.get_text():s.string='Browse all nine publications, journals and worksheets.'
    home_file_text=str(home).replace('Browse all eight publications','Browse all nine publications')
    hp.write_text(home_file_text,encoding='utf8')

    library_file=root/'downloads/index.html';lib=BeautifulSoup(library_file.read_text('utf8'),'html.parser')
    grid=lib.select_one('[data-library-group="books"] .v20-catalogue-grid')
    assert grid,'v0.20 book catalogue not found'
    for elem in grid.select('#beginners-guide'):elem.decompose()
    summary='A welcoming introduction to chance, meaningful choice, five values and the Fellowship in development.'
    topics='beginner newcomers first start philosophy confluent humanism chance choice five values faith religion belief fellowship guide introduction'
    guide_card=BeautifulSoup(f'''<article class="v20-catalogue-card v21-guide-catalogue-card" id="beginners-guide" data-library-item data-category="books" data-search="{e((TITLE+' '+SUBTITLE+' '+summary+' '+topics).casefold())}">
      <a class="v20-catalogue-cover" href="../{GUIDE_URL}" aria-label="Read {e(TITLE)}"><img src="../{COVER}" loading="lazy" decoding="async" width="1000" height="1500" alt="Cover of {e(TITLE)}"></a>
      <div class="v20-catalogue-copy"><span class="v20-type">Start here · 13-page introductory guide</span>
        <h4><a href="../{GUIDE_URL}">{e(TITLE)}</a></h4><p>{e(summary)}</p><span class="v20-status">Revised editorial candidate</span>
        <div class="v20-catalogue-actions"><a href="../{GUIDE_URL}" class="v20-card-read">Read online →</a>
        <a href="../{PDF}" class="v20-card-download" download aria-label="Download {e(TITLE)} as PDF">PDF ↓</a>
        <a href="../{EPUB}" class="v20-card-download" download aria-label="Download {e(TITLE)} as EPUB">EPUB ↓</a></div></div></article>''','html.parser').article
    grid.insert(0,guide_card)
    label=lib.select_one('.v20-catalogue-head>p')
    if label:label.string='Nine books and essays, from a short introduction to original fiction. Find something by its title, question or theme.'
    heading=lib.select_one('[data-library-group="books"] .v20-group-heading p')
    if heading:heading.string='Six works in different forms, including a short place to start.'
    libcount=lib.select_one('.library-count')
    if libcount:
        libcount.select_one('span').string='09'
        libcount.select_one('small').string='One foundational book · five guides, companions / story collections · three Letters · Plus journals'
    for value,newval in [('all','9'),('books','6')]:
        btn=lib.select_one(f'[data-library-filter="{value}"]')
        assert btn
        span=btn.find('span');assert span
        span.string=newval
    results=lib.select_one('[data-library-result]')
    if results:results.string='Showing all 9 publications'
    shortcut=lib.select_one('.section-shortcuts');assert shortcut
    first=shortcut.find('a',href='#featured-book')
    if first:
        a=lib.new_tag('a',href='#beginners-guide');a.string='Start here';first.insert_before(a)
    notice=lib.select_one('.v20-catalogue-note')
    if notice:notice.string='All publications can be read without an account. The Beginner’s Guide and other companion titles and Letters remain editorial candidates, with final review and accessibility checks outstanding.'
    library_file.write_text(str(lib),encoding='utf8')

    # Do not list editorial candidates as indexed releases before sign-off.
    sitemap=root/'sitemap.xml'
    if sitemap.is_file():
        s=sitemap.read_text('utf8')
        s=re.sub(r'<url>\s*<loc>https://thebookofchance.github.io/'+re.escape(GUIDE_URL)+r'</loc>\s*</url>\s*','',s)
        sitemap.write_text(s,encoding='utf8')
    info.update({
        'website_version':'0.21','library_index_count':9,
        'introductory_guide':{'id':GUIDE_ID,'source':SOURCE,'url':GUIDE_URL,'cover':COVER,'pdf':PDF,'epub':EPUB,'pdf_pages':13},
        'guide_status':'Approved for website staging; independent human review, accessibility and live deployment checks pending',
        'sitemap_publication_gate':'Noindex on the guide until formal release approval',
        'video_programme':'Deferred; site introduction integrated'
    })
