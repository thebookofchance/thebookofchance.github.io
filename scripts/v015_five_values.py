"""v0.15 - integrate The Five Values booklet after previously registered releases.
Regenerating the website is idempotent; publishing exports remain unchanged.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import json, html

VALUES=('Hope','Acceptance','Reflection','Growth','Community')


def apply_v015(root:Path, document, markdown, info:dict):
    src=root/'source/booklets/the-five-values.md'
    pdf=root/'files/booklets/The_Five_Values.pdf'
    epub=root/'files/booklets/The_Five_Values.epub'
    cover=root/'assets/booklets/the-five-values-cover.webp'
    assert all(p.is_file() for p in (src,pdf,epub,cover)), 'The Five Values must be published from build_five_values.py first'

    # Readable, freely accessible HTML. PDF/EPUB are optional formats, not gates.
    soup=BeautifulSoup(markdown(src.read_text('utf8')),'html.parser')
    if soup.h1:soup.h1.decompose()
    for p in list(soup.find_all('p',recursive=False))[:4]:
        if 'Hope · Acceptance · Reflection' in p.get_text() or 'A companion to The Book of Chance' in p.get_text() or 'By H · BOC-BKL-001' in p.get_text():p.decompose()
    ids=['intro','hope','acceptance','reflection','growth','community','when-values-conflict','practice','notes']
    heads=soup.find_all('h2')
    assert len(heads)==len(ids),[(h.get_text(),k) for h,k in zip(heads,ids)]
    for head,slug in zip(heads,ids):
        head['id']=slug
        head['class']=['values-chapter-heading']
    for im in soup.find_all('img'):
        assert im.get('src','').startswith('../../assets/booklets/')
        im['loading']='lazy';im['decoding']='async'
        im['class']=['values-illustration']
    for a in soup.find_all('a',href=True):
        if a['href'].startswith('https://'):
            a['target']='_blank';a['rel']='noopener noreferrer'
    article=str(soup)
    nav=''.join(f'<a href="#{v.lower()}"><span>{i:02d}</span><strong>{v}</strong><span class="values-nav-arrow" aria-hidden="true">↘</span></a>' for i,v in enumerate(VALUES,1))
    body=f'''<section class="shell values-hero"><div><a class="back-to-toc" href="../../downloads/">← Back to the Library</a><span class="eyebrow">The Book of Chance · Companion publication 01</span><h1>The Five Values</h1><p class="lead">Hope. Acceptance. Reflection. Growth. Community.</p><p>Five ways of attending to our lives in uncertainty. An illustrated, independently readable introduction by H—open to agreement, criticism and adaptation.</p><div class="button-line"><a href="#start-reading" class="btn btn-primary">Read the booklet ↓</a><a href="../../files/booklets/The_Five_Values.pdf" download class="btn btn-outline">Download PDF ↓</a><a href="../../files/booklets/The_Five_Values.epub" download class="btn btn-outline">Download EPUB ↓</a></div><p class="values-hero-meta">17-page PDF · Illustrated · Free, no membership required · Editorial candidate 1.0-RC1</p></div><div class="values-hero-cover"><img src="../../assets/booklets/the-five-values-cover.webp" width="1000" height="1500" alt="The Five Values by H, white literary cover with five fine charcoal and blue crossing paths"/></div></section>
    <section class="shell values-guide" id="start-reading"><div class="values-guide-intro"><span class="eyebrow">Explore by value</span><h2>Start anywhere.</h2><p>Each value is a question to consider, not a judgement to pass. Read in order, or follow whichever question meets you where you are.</p></div><nav class="values-jump-grid" aria-label="Jump to a value">{nav}</nav></section>
    <div class="shell values-reading-layout"><article class="reading-body values-prose" aria-label="Complete text of The Five Values">{article}</article><aside class="values-side"><span class="eyebrow">This booklet</span><p>A standalone companion to <cite>The Book of Chance</cite>. Each illustrated chapter includes an optional practice and a question to carry.</p><a href="../../files/booklets/The_Five_Values.pdf" class="btn btn-primary" download>PDF edition ↓</a><a href="../../files/booklets/The_Five_Values.epub" class="btn btn-outline" download>EPUB edition ↓</a><a class="text-link" href="../../read/reflection-and-growth/">Read the foundational book's discussion →</a><p class="values-small">Your answers remain yours. There is no sign-up or donation requirement.</p></aside></div>
    <section class="shell values-bottom"><div><span class="eyebrow">Continue exploring</span><h2>Read, reflect, or disagree.</h2><p>Use one question privately, discuss a value with someone you trust, or return to the full twelve readings. There is no required sequence of participation.</p></div><div class="button-line"><a class="btn btn-outline" href="../../reflect/">Explore reflection practices →</a><a class="btn btn-outline" href="../../read/">Read The Book of Chance →</a></div></section>'''
    dest=root/'booklets/the-five-values/index.html';dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(document('The Five Values',body,base='../../',active='downloads',desc='Read The Five Values by H: an illustrated companion exploring Hope, Acceptance, Reflection, Growth and Community, free online and as PDF or EPUB.',extra_head='<link rel="canonical" href="https://thebookofchance.github.io/booklets/the-five-values/">'),encoding='utf8')

    # Insert an obvious publication card in the growing library; no empty future shelves.
    library=root/'downloads/index.html'
    lib=BeautifulSoup(library.read_text('utf8'),'html.parser')
    section=BeautifulSoup('''<section class="values-library-feature" id="five-values-booklet"><div class="values-library-heading"><span class="eyebrow">New companion publication · BOC-BKL-001</span><h2>Five values to live with—not five rules to follow.</h2><p>A concise illustrated guide to Hope, Acceptance, Reflection, Growth and Community. Each chapter includes an original scene, a practical question and an optional exercise. The values are complementary, not a test of worth.</p></div><div class="values-library-card"><img src="../assets/booklets/the-five-values-cover.webp" alt="The Five Values by H — illustrated booklet cover" width="1000" height="1500" loading="lazy"><div><span class="eyebrow">Illustrated booklet · 17-page PDF · Free</span><h3>The Five Values</h3><p>Explore how these values work together when life is uncertain—and what to do when they seem to pull in different directions.</p><div class="button-line"><a class="btn btn-primary" href="../booklets/the-five-values/">Read online →</a><a class="btn btn-outline" href="../files/booklets/The_Five_Values.pdf" download>PDF ↓</a><a class="btn btn-outline" href="../files/booklets/The_Five_Values.epub" download>EPUB ↓</a></div><p class="values-meta">Prepared for editorial approval · Digital access does not require membership</p></div></div></section>''','html.parser').section
    letters=lib.select_one('.letters-feature-library')
    assert letters,'Library insert point missing'
    letters.insert_before(section)
    count=lib.select_one('.library-count')
    if count:
        count.find('span').string='05'
        count.find('small').string='Foundational book + three Letters + The Five Values · Plus journals'
    library.write_text(str(lib),encoding='utf8')

    # Homepage: clear path to new writing, preserving existing feature links.
    home=root/'index.html'
    hs=BeautifulSoup(home.read_text('utf8'),'html.parser')
    card=BeautifulSoup('''<section class="shell values-home-feature section-space"><div><span class="eyebrow">New illustrated companion · by H</span><h2>What do our five values ask of us?</h2><p>Hope, Acceptance, Reflection, Growth and Community are not a checklist. Our new illustrated booklet examines what each one means—and how to balance them when life is complicated.</p><div class="button-line"><a href="booklets/the-five-values/" class="btn btn-primary">Read The Five Values →</a><a href="downloads/#five-values-booklet" class="btn btn-outline">Explore the Library</a></div></div><img src="assets/booklets/the-five-values-cover.webp" alt="Cover of The Five Values, an illustrated companion by H" loading="lazy" width="1000" height="1500"></section>''','html.parser').section
    before=hs.select_one('.letters-home-feature')
    assert before, 'Home insertion point not found'
    before.insert_before(card)
    home.write_text(str(hs),encoding='utf8')

    # Catalogue and sitemap are regenerated from earlier source on each build.
    pub=root/'source/publications.json'
    p=json.loads(pub.read_text('utf8'))
    p['booklets']=[{'id':'BOC-BKL-001','title':'The Five Values','author':'H','series':'The Book of Chance — Companions',
        'subtitle':'Hope · Acceptance · Reflection · Growth · Community','edition':'1.0-RC1',
        'status':'editorial candidate; founder sign-off and live check outstanding',
        'language':'en-NZ','date_prepared':'2026-11-22',
        'source':'source/booklets/the-five-values.md','url':'booklets/the-five-values/',
        'cover':'assets/booklets/the-five-values-cover.webp','pdf':'files/booklets/The_Five_Values.pdf','epub':'files/booklets/The_Five_Values.epub'}]
    pub.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    sitemap=root/'sitemap.xml';sm=sitemap.read_text('utf8')
    url='https://thebookofchance.github.io/booklets/the-five-values/'
    if url not in sm:sm=sm.replace('</urlset>',f'<url><loc>{url}</loc></url>\n</urlset>')
    sitemap.write_text(sm,encoding='utf8')
    info.update({'website_version':'0.15','latest_companion_id':'BOC-BKL-001','companion_page_count_pdf':17,
        'companion_status':'Editorial candidate; approval and deployed verification outstanding',
        'values_booklet':{'online':'booklets/the-five-values/','pdf':'files/booklets/The_Five_Values.pdf','epub':'files/booklets/The_Five_Values.epub'},
        'video_programme':'Deferred until after planned publications'})
