"""v0.20 targeted information architecture refinement.

Execute after v019 on every website rebuild. This module deliberately retains
all publication landing pages, manuscript files, downloads, privacy settings,
form configuration, and editorial-candidate status.
"""
from __future__ import annotations
import html
import json
from pathlib import Path
from bs4 import BeautifulSoup


# The copy below is concise *editorial interface text*, not a new publication.
# File paths, titles and publication metadata come from source catalogues.
TOPICS = {
    'BOC-PAR-001': ('Original fiction · 12 stories', 'fiction stories fortune choice uncertainty shared lives'),
    'BOC-BKL-002': ('Practical philosophy · 12 chapters', 'possibility opportunity conditions agency barriers learning fairness'),
    'BOC-CNV-001': ('Discussion guide · 12 conversations', 'discussion dialogue questions facilitation community disagreement'),
    'BOC-BKL-001': ('Illustrated guide · Five values', 'hope acceptance reflection growth community philosophy values'),
    'BOC-LFH-001': ('Letter 01 · Essay', 'people we never meet strangers responsibility interdependence'),
    'BOC-LFH-002': ('Letter 02 · Essay', 'decisions outcomes moral luck responsibility repair'),
    'BOC-LFH-003': ('Letter 03 · Essay', 'strangers duties helping boundaries generosity'),
    'book-of-chance': ('Foundational work · 12 readings', 'uncertainty fortune dignity agency philosophical readings parables'),
}


def e(x):
    return html.escape(str(x), quote=True)


def publication_cards(root: Path):
    catalogue=json.loads((root/'source/publications.json').read_text('utf8'))
    letters=json.loads((root/'source/letters/catalogue.json').read_text('utf8'))['available']
    originals=catalogue['available']
    assert len(originals)==1 and originals[0]['id']=='book-of-chance'
    original=originals[0]
    first_edition=original['editions'][0]
    books=[{
        'id':original['id'],'title':original['title'],'summary':original['summary'],
        'subtitle':original['subtitle'],'cover':first_edition['cover'],
        'url':'read/','pdf':None,'epub':None,'type':'books',
        'status':'Foundational work',
        'anchor':'foundational-index',
    }]
    for group in ('parables','booklets','conversations'):
        for v in catalogue.get(group,[]):
            books.append({
                'id':v['id'],'title':v['title'],'summary':v['subtitle'],
                'subtitle':v['subtitle'],'cover':v['cover'],'url':v['url'],
                'pdf':v['pdf'],'epub':v['epub'],'type':'books',
                'status':'Editorial candidate',
                'anchor':{'BOC-PAR-001':'parables-of-chance',
                          'BOC-BKL-002':'little-book-of-possibilities',
                          'BOC-BKL-001':'five-values-booklet',
                          'BOC-CNV-001':'conversations-of-chance'}.get(v['id'],''),
            })
    issues=[{
        'id':v['id'],'title':v['title'],'summary':v['summary'],
        'subtitle':'Letters from H · No. '+str(v['number']).zfill(2),
        'cover':v['cover'],'url':v['url'],'pdf':v['pdf'],'epub':v['epub'],
        'type':'letters','status':'Editorial candidate',
        'anchor':'letter-0'+str(v['number']),
    } for v in letters]
    by_id={x['id']:x for x in books+issues}
    assert len(books)==5 and len(issues)==3 and len(by_id)==8
    for item in books+issues:
        for key in ('url','cover'):
            assert (root/item[key]).is_file() if key=='cover' else (root/item[key]).exists(),(item['title'],key)
        for key in ('pdf','epub'):
            if item[key]:assert (root/item[key]).is_file(),(item['title'],key)
        assert item['id'] in TOPICS
    # Home placement: five distinct cards, with links to canonical reading pages.
    home_items=[by_id[k] for k in (
        'BOC-PAR-001','BOC-BKL-002','BOC-CNV-001','BOC-BKL-001','BOC-LFH-003'
    )]
    return books,issues,home_items


def home_card(item):
    code=TOPICS[item['id']][0]
    return f'''<article class="v20-home-card">
      <a class="v20-home-cover" href="{e(item['url'])}" aria-label="Read {e(item['title'])}">
        <img src="{e(item['cover'])}" alt="Cover of {e(item['title'])}" loading="lazy" decoding="async" width="1000" height="1500"></a>
      <div class="v20-home-copy"><span class="v20-type">{e(code)}</span>
        <h3><a href="{e(item['url'])}">{e(item['title'])}</a></h3>
        <p>{e(item['subtitle'])}</p>
        <span class="v20-status">Editorial candidate</span></div></article>'''


def library_card(item):
    label,topics=TOPICS[item['id']]
    terms=' '.join([item['title'],item['subtitle'],item['summary'],topics])
    linkread=f'<a href="../{e(item["url"])}" class="v20-card-read">Read online <span aria-hidden="true">→</span></a>'
    if item['id']=='book-of-chance':
        actions=(linkread+'<a href="#featured-book" class="v20-card-download">View Light / Dark editions ↑</a>')
    else:
        actions=(linkread+
            f'<a href="../{e(item["pdf"])}" class="v20-card-download" download aria-label="Download {e(item["title"])} as PDF">PDF ↓</a>'+
            f'<a href="../{e(item["epub"])}" class="v20-card-download" download aria-label="Download {e(item["title"])} as EPUB">EPUB ↓</a>')
    return f'''<article class="v20-catalogue-card" id="{e(item['anchor'])}" data-library-item data-category="{e(item['type'])}" data-search="{e(terms.casefold())}">
      <a class="v20-catalogue-cover" href="../{e(item['url'])}" aria-label="Read {e(item['title'])}"><img src="../{e(item['cover'])}" loading="lazy" decoding="async" width="1000" height="1500" alt="Cover of {e(item['title'])}"></a>
      <div class="v20-catalogue-copy"><span class="v20-type">{e(label)}</span>
        <h4><a href="../{e(item['url'])}">{e(item['title'])}</a></h4>
        <p>{e(item['summary'])}</p>
        <span class="v20-status">{e(item['status'])}</span>
        <div class="v20-catalogue-actions">{actions}</div></div></article>'''


def apply_v020(root:Path,info:dict):
    books,letters,home_items=publication_cards(root)
    home_file=root/'index.html';home=BeautifulSoup(home_file.read_text('utf8'),'html.parser')
    # Remove five separate promotional strips, preserving hero, original book,
    # reflection, Fellowship and physical-book interest content.
    for selector in ('.parables-home-feature','.possibilities-home-feature',
                     '.conversations-home-feature','.values-home-feature','.letters-home-feature',
                     '.v20-home-library'):
        for elem in home.select(selector):elem.decompose()
    home_markup='''<section class="shell section-space v20-home-library" id="explore-library">
      <div class="v20-collection-head"><div><span class="eyebrow">The growing collection</span>
        <h2>Different ways into the same questions.</h2></div>
        <p>Stories, practical companions and Letters from H. Follow whatever interests you; each work can be read on its own.</p></div>
      <div class="v20-home-grid">'''+''.join(home_card(v) for v in home_items)+'''
        <a class="v20-home-discover" href="downloads/"><span class="v20-type">The full library</span>
        <strong>Find your next reading.</strong><span>Browse all eight publications, journals and worksheets.</span>
        <b>Explore the Library →</b></a></div>
      <p class="v20-collection-foot">Companion publications and Letters are editorial candidates; independent review and final release checks are still outstanding. All reading is free and requires no account.</p>
    </section>'''
    anchor=home.select_one('.home-community');assert anchor,'Homepage Fellowship block missing'
    anchor.insert_before(BeautifulSoup(home_markup,'html.parser').section)
    home_file.write_text(str(home),encoding='utf8')

    lib_file=root/'downloads/index.html';lib=BeautifulSoup(lib_file.read_text('utf8'),'html.parser')
    # Keep the foundational two-edition showcase and the existing journals,
    # worksheets and reader guidance. Collapse only the repeated promotions.
    for sel in ('#parables-of-chance','#little-book-of-possibilities',
                '#conversations-of-chance','#five-values-booklet','#letters-from-h',
                '#publication-catalogue'):
        for section in lib.select(sel):section.decompose()
    featured=lib.select_one('.library-release');assert featured,'Foundational editions missing'
    # The original placeholder for planned further readings no longer helps
    # visitors navigate the now-complete initial literature collection.
    planned=lib.select_one('.library-upcoming')
    if planned:planned.decompose()
    markup='''<section class="v20-catalogue" id="publication-catalogue" aria-labelledby="v20-catalogue-title">
      <header class="v20-catalogue-head"><div><span class="eyebrow">Browse the writing</span>
      <h2 id="v20-catalogue-title">A shelf of possibilities.</h2></div>
      <p>Eight books and essays, from foundational philosophy to original fiction. Find something by its title, question or theme.</p></header>
      <div class="v20-catalogue-toolbar"><div class="v20-catalogue-filters" role="group" aria-label="Filter publications">
      <button type="button" data-library-filter="all" aria-pressed="true">All <span>8</span></button>
      <button type="button" data-library-filter="books" aria-pressed="false">Books <span>5</span></button>
      <button type="button" data-library-filter="letters" aria-pressed="false">Letters <span>3</span></button></div>
      <label class="v20-catalogue-search" for="library-search"><span class="sr-only">Search publications by title or topic</span>
        <svg aria-hidden="true" width="17" height="17" viewBox="0 0 24 24" fill="none"><circle cx="10.5" cy="10.5" r="6.5" stroke="currentColor" stroke-width="1.7"/><path d="m15.5 15.5 5 5" stroke="currentColor" stroke-linecap="round" stroke-width="1.7"/></svg>
        <input type="search" id="library-search" placeholder="Search titles or themes" autocomplete="off"></label></div>
      <p class="v20-results" data-library-result aria-live="polite" aria-atomic="true">Showing all 8 publications</p>
      <section class="v20-catalogue-group" data-library-group="books" aria-labelledby="v20-books-title"><div class="v20-group-heading"><h3 id="v20-books-title">Books &amp; companions</h3><p>Five works in different forms.</p></div><div class="v20-catalogue-grid">'''+''.join(library_card(v) for v in books)+'''</div></section>
      <section class="v20-catalogue-group" id="letters-from-h" data-library-group="letters" aria-labelledby="v20-letters-title"><div class="v20-group-heading"><h3 id="v20-letters-title">Letters from H</h3><p>Three independent philosophical essays. <a href="../letters/">Visit the Letters archive →</a></p></div><div class="v20-catalogue-grid">'''+''.join(library_card(v) for v in letters)+'''</div></section>
      <p data-library-empty class="v20-catalogue-empty" hidden>No matching publications. Try a different title or theme, or clear the search.</p>
      <p class="v20-catalogue-note">All publications can be read without an account. Companion titles and Letters remain editorial candidates, not independently approved final releases.</p>
    </section>'''
    featured.insert_after(BeautifulSoup(markup,'html.parser').section)
    # Category navigation includes Letters and The Five Values through the index.
    shortcuts=lib.select_one('.section-shortcuts');assert shortcuts,'Library shortcuts missing'
    shortcuts.clear()
    for title,href in [
        ('Browse',''),('The book','#featured-book'),('All publications','#publication-catalogue'),
        ('Letters','#letters-from-h'),('Journals','#reflection-journal'),
        ('Worksheets','#practice-guides'),('Write online','../reflect/')
    ]:
        tag=lib.new_tag('span' if title=='Browse' else 'a')
        tag.string=title
        if title!='Browse':tag['href']=href
        shortcuts.append(tag)
    # Announce correct collection count while avoiding claims of final release.
    lib_count=lib.select_one('.library-count')
    if lib_count:
        lib_count.find('span').string='08'
        lib_count.select_one('small').string='One foundational book · four companions / story collections · three Letters · Plus journals'
    head=lib.head
    assert head
    script=lib.new_tag('script',src='../assets/library.js')
    script['defer']=''
    head.append(script)
    lib_file.write_text(str(lib),encoding='utf8')
    # Earlier generators can reintroduce candidate routes into the sitemap on
    # rebuild. Keep v0.19's intentional noindex / sitemap publication gate.
    sitemap=root/'sitemap.xml'
    if sitemap.exists():
        xml=sitemap.read_text('utf8')
        for route in ('booklets/the-little-book-of-possibilities/',
                      'publications/conversations-of-chance/',
                      'publications/parables-of-chance/'):
            tag='<url><loc>https://thebookofchance.github.io/'+route+'</loc></url>'
            xml=xml.replace('  '+tag+'\n','').replace(tag,'')
        sitemap.write_text(xml,encoding='utf8')
    info.update({'website_version':'0.20','library_index_count':8,
       'library_categories':['Books','Letters','Journals','Worksheets'],
       'library_search':'Local catalogue title and topic filter; no remote service',
       'home_publication_promotions':'Consolidated into one cover-led collection grid',
       'editorial_release_gate':'Unchanged; noindex on pending editorial candidates preserved',
       'video_programme':'Not started; site refinement only'})
