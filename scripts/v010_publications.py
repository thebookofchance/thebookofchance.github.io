"""The Book of Chance v0.10: source-driven Letters from H catalogue and reading pages.
Called by build_site.py AFTER v0.9 enhancements. No live services or private form configuration touched.
"""
from pathlib import Path
import json, html
from bs4 import BeautifulSoup
from build_letters import build as build_letter_assets

LETTER_TITLE='On the People We Never Meet'


def apply_v010(root: Path, document, md, info: dict):
    # Do not mutate a previously produced Letter merely by rebuilding the website.
    # Rebuild the issue deliberately with build_letters.py after an editorial change.
    required=[root/'files/letters/Letters_from_H_01_On_the_People_We_Never_Meet.pdf',
              root/'files/letters/Letters_from_H_01_On_the_People_We_Never_Meet.epub',
              root/'assets/letters/lfh-001-cover.webp']
    if not all(x.is_file() for x in required):
        build_letter_assets()
    metadata_path=root/'source/letters/catalogue.json'
    catalogue=json.loads(metadata_path.read_text('utf-8'))
    entry=catalogue['available'][0]
    letter_md=(root/entry['file']).read_text('utf-8')
    # Use the same project markdown renderer used for The Book of Chance.
    article_markup=md(letter_md)
    # The page gives the heading its own accessible hero; avoid a duplicate h1 and metadata.
    soup=BeautifulSoup(article_markup,'html.parser')
    if soup.h1: soup.h1.decompose()
    first=soup.find('p')
    if first and 'Letters from H · No. 01' in first.get_text():first.decompose()
    article_markup=str(soup)
    topic=html.escape(LETTER_TITLE)
    summary=html.escape(entry['summary'])

    letter_body=f'''<div class="shell letters-reading-top"><a class="back-to-toc" href="../">← All Letters from H</a><a class="back-to-toc" href="../../downloads/#letters-from-h">The Library</a></div>
    <header class="shell letters-reading-hero"><span class="eyebrow">Letters from H · No. 01</span><h1>{topic}</h1><p class="lead">A letter on unseen lives and shared responsibility.</p><p class="letters-meta">By H · Revised 22 November 2026 · Editorial candidate {html.escape(entry["edition"])}</p></header>
    <div class="shell letters-reading-layout"><article class="reading-body letters-prose" aria-label="Full text of Letter 01">{article_markup}</article><aside class="letters-side"><span class="eyebrow">This letter</span><p>A standalone essay that extends themes in <cite>The Book of Chance</cite>. No account, donation or Fellowship membership is required.</p><img src="../../{entry['cover']}" alt="White literary cover with crossing black and blue paths and the title On the People We Never Meet" loading="lazy" width="1000" height="1500"><a class="btn btn-primary" href="../../{entry['pdf']}" download>Download PDF ↓</a><a class="btn btn-outline" href="../../{entry['epub']}" download>Download EPUB ↓</a><a class="text-link" href="../../read/shared-fortune/">Related: Shared Fortune ↗</a></aside></div>
    <section class="shell letters-postscript"><div><span class="eyebrow">Keep reading</span><h2>More letters will follow.</h2><p>Each Letter will explore one philosophical question in full, with care for uncertainty, dignity and the people our choices touch.</p></div><a class="btn btn-outline" href="../">Explore the series →</a></section>'''
    letter_page=root/'letters'/entry['slug']/'index.html'
    letter_page.parent.mkdir(parents=True,exist_ok=True)
    letter_page.write_text(document(topic,letter_body,base='../../',active='downloads',desc=summary,extra_head=f'<link rel="canonical" href="https://thebookofchance.github.io/letters/{entry["slug"]}/">',og_image=entry['cover'].replace('.webp','.png')),encoding='utf-8')

    entries=''.join(f'''<article class="letters-index-feature"><img src="../{e['cover']}" alt="Literary cover for {html.escape(e['title'])}, with intersecting charcoal and blue paths" width="1000" height="1500" loading="lazy"><div><span class="eyebrow">Letter {e['number']:02d} · Free to read</span><h2>{html.escape(e['title'])}</h2><p>{html.escape(e['summary'])}</p><div class="button-line"><a class="btn btn-primary" href="{e['slug']}/">Read the letter →</a><a class="btn btn-outline" href="../{e['pdf']}" download>PDF ↓</a><a class="btn btn-outline" href="../{e['epub']}" download>EPUB ↓</a></div></div></article>''' for e in catalogue['available'])
    archive=f'''<section class="shell page-hero letters-index-hero"><span class="eyebrow">The library · Short-form philosophical literature</span><h1>Letters from H.</h1><p class="lead">Questions worth examining in their own right.</p><p>These occasional essays extend themes from <cite>The Book of Chance</cite>. They are invitations to think, not instructions to believe, and each stands alone.</p></section><div class="shell letters-index-list">{entries}<div class="letters-series-foot"><span class="eyebrow">The series continues, one letter at a time</span><p>The next planned question is <em>When Good Choices Lead to Bad Outcomes</em>. It is not published yet. There is no registration requirement or publication schedule to keep up with.</p><a href="../downloads/" class="text-link">Browse the rest of the Library →</a></div></div>'''
    index=root/'letters'/'index.html'
    index.parent.mkdir(parents=True,exist_ok=True)
    index.write_text(document('Letters from H',archive,base='../',active='downloads',desc='Read Letters from H: free standalone philosophical essays related to The Book of Chance.'),encoding='utf-8')

    # Prominent placement in the Library before journals, which remain available and unchanged.
    library=root/'downloads/index.html'
    l_soup=BeautifulSoup(library.read_text('utf-8'),'html.parser')
    new_section=BeautifulSoup(f'''<section class="letters-feature-library" id="letters-from-h"><div class="letters-library-head"><span class="eyebrow">New collection · Letters from H</span><h2>Questions that deserve their own pages.</h2><p>A series of free, independently readable essays by H. The first Letter considers the people we never meet but whose choices touch our lives.</p></div><article class="letters-library-card"><img src="../{entry['cover']}" alt="Letters from H No. 01 cover with intersecting paths" loading="lazy" width="1000" height="1500"><div><span class="eyebrow">No. 01 · A philosophical letter</span><h3>{topic}</h3><p>{summary}</p><div class="button-line"><a class="btn btn-primary" href="../letters/{entry['slug']}/">Read online →</a><a class="btn btn-outline" href="../{entry['pdf']}" download>PDF ↓</a><a class="btn btn-outline" href="../{entry['epub']}" download>EPUB ↓</a></div><a class="text-link" href="../letters/">About the Letters series →</a></div></article></section>''','html.parser').section
    target=l_soup.select_one('.journal-series') or l_soup.select_one('.library-upcoming')
    assert target, 'Library insertion point unavailable'
    target.insert_before(new_section)
    for card in l_soup.select('.library-planned-card'):
        if 'Reflections from H' in card.get_text(' ',strip=True):card.decompose()
    count=l_soup.select_one('.library-count')
    if count:
        count.find('span').string='02'  # foundational book and first Letter; journals are additional resources
        small=count.find('small')
        if small:small.string='Foundational book + first Letter · Free journals and worksheets'
    library.write_text(str(l_soup),encoding='utf-8')

    # One clear editorial placement on the homepage; no new top-level menu crowding.
    home=root/'index.html'
    h_soup=BeautifulSoup(home.read_text('utf-8'),'html.parser')
    card=BeautifulSoup(f'''<section class="shell letters-home-feature section-space"><div><span class="eyebrow">New writing · Letters from H / 01</span><h2>We are part of lives we never see.</h2><p>Who makes our ordinary days possible? And what might we leave behind for people whose names we will never know?</p><a class="btn btn-outline" href="letters/{entry['slug']}/">Read the first Letter →</a><a class="text-link" href="letters/">Explore the collection →</a></div><img src="{entry['cover']}" alt="Cover of Letters from H: On the People We Never Meet" loading="lazy" width="1000" height="1500"></section>''','html.parser').section
    community=h_soup.select_one('.home-community')
    assert community, 'Homepage insertion point unavailable'
    community.insert_before(card)
    home.write_text(str(h_soup),encoding='utf-8')

    # Clean up “planned” placeholders now that issue 1 actually exists.
    pubpath=root/'source/publications.json'
    pub=json.loads(pubpath.read_text('utf-8'))
    pub['planned']=[p for p in pub['planned'] if p.get('title')!='Reflections from H']
    pub['letters']={'series':'Letters from H','index':'letters/','issues':[{'id':entry['id'],'title':entry['title'],'url':entry['url'],'pdf':entry['pdf'],'epub':entry['epub'],'status':entry['status']}]} 
    pubpath.write_text(json.dumps(pub,ensure_ascii=False,indent=2)+'\n','utf-8')

    # Add a path to the footer of every generated HTML page through its source generator?
    # Keep the primary nav at seven items for narrow screens. Linkable collection is visible
    # from the homepage and the Library; interior page footer stays unmodified.

    # Update sitemap only once per route, using the same origin as the site's canonical links.
    smpath=root/'sitemap.xml'
    sm=smpath.read_text('utf-8')
    for path in ('letters/','letters/'+entry['slug']+'/'):
        loc='https://thebookofchance.github.io/'+path
        if loc not in sm: sm=sm.replace('</urlset>',f'<url><loc>{loc}</loc></url>\n</urlset>')
    smpath.write_text(sm,'utf-8')

    # This is an editorial candidate pending human author approval and a live website check.
    info.update({'website_version':'0.11','letters_series_available':1,'letters_series_status':'First issue editorial candidate; author/live review pending','letters_publication':entry['id'],'publication_standard':'docs/Publications_Standard_v1.0_RC1.md'})
