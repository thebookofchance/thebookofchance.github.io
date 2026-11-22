"""Website v0.19 — The Parables of Chance v0.2.1.

Source-driven, idempotent HTML reader and library/home integration.
Does not regenerate PDF, EPUB, or approved artwork; does not edit forms-config.
"""
from __future__ import annotations
import html, json, re
from pathlib import Path
from bs4 import BeautifulSoup

SOURCE='source/parables/the-parables-of-chance.md'
PAGE='publications/parables-of-chance/'
PDF='files/parables/The_Parables_of_Chance_Editorial_Proof_v0.2.1.pdf'
EPUB='files/parables/The_Parables_of_Chance_Editorial_Proof_v0.2.1.epub'
COVER='assets/publications/parables-of-chance-cover.webp'
SHARE_IMAGE='assets/publications/parables-of-chance-cover.png'
PARTS=['Part I — What Arrives Unasked','Part II — The Turns We Take','Part III — What Remains Between Us']
STORIES=['The Wrong Address','Two Flood Marks','The Day the Signal Failed','A Quiet Harvest',
    'The Map Without a Bridge','The Unmeasured Salt','The Night of No Stars',
    "The Five O'Clock Ferry",'The Names Left Off','The Path Through the Reeds',
    'The Rules of the Room','What the Tide Keeps']
NOTES=['Before the Stories','A Note on Reading Parables','Twelve Questions to Keep','A Note on Authorship and Status']


def slug(s:str)->str:
    s=s.casefold().replace('’',"'")
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')


def make_article(source:str, markdown)->str:
    # Exclude only duplicated manuscript contents/cover. The complete prose and end matter remain.
    note=source.index('## A Note on This Edition\n')
    contents=source.index('## Contents\n',note)
    body=source.index('## Before the Stories\n',contents)
    retained=source[note:contents].strip()+'\n\n'+source[body:]
    soup=BeautifulSoup(markdown(retained),'html.parser')
    observed=[];part_titles=[]; ids=set()
    for h in soup.find_all(['h1','h2','h3']):
        raw=h.get_text(' ',strip=True)
        if h.name=='h1' and raw.startswith('Part '):
            h.name='h2';h['class']=['conversations-part','parables-part'];part_titles.append(raw)
        elif h.name=='h2' and re.fullmatch(r'\d+\.\s.+',raw):
            h.name='h3';h['class']=['conversations-chapter','parables-story'];observed.append(raw)
        elif h.name=='h2':
            h['class']=['conversations-note-heading']
        ident=slug(raw)
        assert ident not in ids,('duplicate heading',ident)
        ids.add(ident);h['id']=ident
    assert part_titles==PARTS,(part_titles,PARTS)
    assert observed==[f'{i}. {title}' for i,title in enumerate(STORIES,1)],observed
    assert len(soup.get_text(' ',strip=True))>60000,'Manuscript appears incomplete'
    return str(soup)


def make_toc():
    items=['<li><a href="#before-the-stories">Before the Stories</a></li>']
    for pi,part in enumerate(PARTS):
        items.append(f'<li class="conversations-toc-part"><a href="#{slug(part)}">{html.escape(part)}</a></li>')
        for si in range(pi*4,pi*4+4):
            title=STORIES[si]
            items.append(f'<li><a href="#{slug(str(si+1)+". "+title)}"><span>{si+1:02d}</span> {html.escape(title)}</a></li>')
    items.append('<li class="conversations-toc-part"><a href="#a-note-on-reading-parables">After the stories</a></li>')
    for note in NOTES[1:]:
        items.append(f'<li><a href="#{slug(note)}">{html.escape(note)}</a></li>')
    return '<ol>'+''.join(items)+'</ol>'


def make_body(article,toc,pages):
    return f'''<section class="shell conversations-hero parables-hero">
      <div class="conversations-hero-text"><a class="back-to-toc" href="../../downloads/">← Back to the Library</a>
      <span class="eyebrow">The Book of Chance · Stories and Parables · BOC-PAR-001</span>
      <h1>The Parables<br>of Chance</h1>
      <p class="lead">Twelve Stories about Fortune, Choice and the Lives We Share</p>
      <p>Ordinary lives meet uncertainty in unexpected ways. Twelve original fictional stories about the circumstances we inherit, the turns we take, and what remains between us. Each story can be read in its own right—without a prescribed lesson.</p>
      <div class="button-line"><a class="btn btn-primary" href="#parables-text">Begin reading ↓</a>
      <a class="btn btn-outline" href="../../{PDF}" download>Download PDF ↓</a>
      <a class="btn btn-outline" href="../../{EPUB}" download>Download EPUB ↓</a></div>
      <p class="conversations-status">12 stories · {pages}-page PDF reader proof · Free · Final copyedit candidate v0.2.1</p>
      </div><div class="parables-cover-art"><img src="../../{COVER}" alt="The Parables of Chance by H, a literary cover of intersecting charcoal and blue paths" width="1000" height="1500" loading="eager"></div>
    </section>
    <div class="shell conversations-lead parables-intro"><p><strong>Fiction, not a test of belief.</strong> The people and incidents in these stories are invented. Their endings do not promise rewards for virtue or prove a theory of chance. Readers may question any choice or simply enjoy the stories. No membership, payment or personal disclosure is required.</p>
    <details class="conversations-mobile-contents"><summary>Explore all twelve stories</summary>{toc}</details></div>
    <div class="shell conversations-layout" id="parables-text"><aside class="conversations-toc" aria-label="Story contents"><strong>Contents</strong><p>Begin anywhere.</p>{toc}</aside>
      <article class="conversations-article parables-article" aria-label="Complete text of The Parables of Chance">{article}</article></div>
    <section class="shell conversations-after"><div><span class="eyebrow">After the last story</span><h2>Not every ending settles its question.</h2><p>Return to a story, carry its question with you, or explore the foundational readings. No particular interpretation is required.</p></div>
      <div class="button-line"><a class="btn btn-outline" href="../../read/">Read The Book of Chance →</a><a class="btn btn-outline" href="../../downloads/">Back to the Library →</a></div></section>'''


def apply_v019(root:Path,document,markdown,info:dict):
    for p in (SOURCE,PDF,EPUB,COVER,SHARE_IMAGE):
        assert (root/p).is_file(),f'Missing source / download: {p}'
    text=(root/SOURCE).read_text('utf8')
    article=make_article(text,markdown);toc=make_toc()
    # Count is based on actual built PDF, never hand-assumed.
    import fitz
    with fitz.open(root/PDF) as pdf:
        pages=len(pdf)
        assert pdf.metadata.get('author')=='H','Final author metadata missing'
    desc='Read The Parables of Chance by H: twelve original free stories exploring fortune, choice, shared responsibility and the lives we inherit.'
    pagefile=root/PAGE/'index.html';pagefile.parent.mkdir(parents=True,exist_ok=True)
    body=make_body(article,toc,pages)
    pagefile.write_text(document('The Parables of Chance',body,base='../../',active='downloads',desc=desc,
        extra_head='<link rel="canonical" href="https://thebookofchance.github.io/publications/parables-of-chance/"><meta name="robots" content="noindex,follow">',
        og_image=SHARE_IMAGE),encoding='utf8')
    libfile=root/'downloads/index.html';lib=BeautifulSoup(libfile.read_text('utf8'),'html.parser')
    prior=lib.select_one('#parables-of-chance')
    if prior:prior.decompose()
    section=BeautifulSoup(f'''<section class="parables-library-feature" id="parables-of-chance">
       <div class="parables-library-heading"><span class="eyebrow">New fiction collection · BOC-PAR-001</span>
       <h2>Twelve stories. No single answer.</h2><p>Stories of misplaced connections, difficult choices, unexpected loss and the lives that continue beyond our own. <cite>The Parables of Chance</cite> explores the philosophy through original fiction, allowing readers to reach their own conclusions.</p></div>
       <div class="parables-library-card"><img src="../{COVER}" alt="The Parables of Chance by H — literary collection cover" loading="lazy" width="1000" height="1500">
       <div><span class="eyebrow">Stories and Parables · 12 stories · {pages}-page PDF proof</span><h3>The Parables of Chance</h3>
       <p class="parables-library-subtitle">Twelve Stories about Fortune, Choice and the Lives We Share</p>
       <p>An original collection of philosophical fiction. Read independently, discuss with others, or simply enjoy the stories.</p>
       <div class="button-line"><a class="btn btn-primary" href="../{PAGE}">Read online →</a><a class="btn btn-outline" href="../{PDF}" download>PDF ↓</a><a class="btn btn-outline" href="../{EPUB}" download>EPUB ↓</a></div>
       <p class="parables-meta">Copyedited v0.2.1 · Editorial candidate pending final publication gates</p></div></div></section>''','html.parser').section
    anchor=lib.select_one('#little-book-of-possibilities')
    assert anchor is not None,'v0.18 Library publication missing'
    anchor.insert_before(section)
    count=lib.select_one('.library-count')
    assert count and count.select_one('small')
    count.find('span').string='08'
    count.select_one('small').string='Foundational book + three Letters + four additional publications · Plus journals'
    shortcuts=lib.select_one('.section-shortcuts')
    assert shortcuts,'Library shortcuts unavailable'
    if not shortcuts.select_one('a[href="#parables-of-chance"]'):
        a=lib.new_tag('a',href='#parables-of-chance');a.string='Parables'
        before=shortcuts.select_one('a[href="#little-book-of-possibilities"]')
        if before:before.insert_before(a)
        else:shortcuts.append(a)
    libfile.write_text(str(lib),encoding='utf8')
    homefile=root/'index.html';home=BeautifulSoup(homefile.read_text('utf8'),'html.parser')
    prior=home.select_one('.parables-home-feature')
    if prior:prior.decompose()
    feature=BeautifulSoup(f'''<section class="shell parables-home-feature section-space">
       <div><span class="eyebrow">A new collection of stories · by H</span>
       <h2>What stories stay with us after the ending?</h2>
       <p>Ordinary people, uncertain outcomes and the unexpected ways one life meets another. Twelve original parables that stand on their own, with questions worth carrying rather than answers to memorise.</p>
       <div class="button-line"><a class="btn btn-primary" href="{PAGE}">Read The Parables of Chance →</a><a class="btn btn-outline" href="downloads/#parables-of-chance">Explore the Library</a></div>
       <p class="parables-meta">Free online, PDF and EPUB · Editorial candidate v0.2.1</p></div>
       <img src="{COVER}" alt="The Parables of Chance by H — original fiction collection cover" loading="lazy" width="1000" height="1500"></section>''','html.parser').section
    anchor=home.select_one('.possibilities-home-feature')
    assert anchor,'v0.18 homepage feature missing'
    anchor.insert_before(feature)
    homefile.write_text(str(home),encoding='utf8')
    catfile=root/'source/publications.json';cat=json.loads(catfile.read_text('utf8'))
    cat['parables']=[{
        'id':'BOC-PAR-001','title':'The Parables of Chance',
        'subtitle':'Twelve Stories about Fortune, Choice and the Lives We Share',
        'author':'H','series':'The Book of Chance — Stories and Parables',
        'edition':'v0.2.1','status':'final copyedit candidate; external review, accessibility and live checks outstanding',
        'language':'en-NZ','date_prepared':'2026-11-22','source':SOURCE,'url':PAGE,
        'cover':COVER,'pdf':PDF,'epub':EPUB,'stories':12,'pdf_pages':pages,
    }]
    catfile.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    info.update({'website_version':'0.19','library_available_publications':8,'publications_represented_in_library':8,
        'latest_story_id':'BOC-PAR-001','parables_status':'Final copyedit candidate v0.2.1; external and author sign-off, accessibility and live checks outstanding',
        'parables':{'online':PAGE,'pdf':PDF,'epub':EPUB,'cover':COVER,'source':SOURCE,'stories':12,'pdf_pages':pages},
        'video_programme':'Deferred until the publication programme and release gates are complete'})
