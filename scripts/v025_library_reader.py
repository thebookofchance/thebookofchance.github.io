"""v0.25: bookshelf browsing and a local-first, paginated in-browser reader.

Builds reader text from existing HTML pages; never edits canonical manuscripts or
publication exports.  The reader is a presentation layer, not a new edition.
"""
from __future__ import annotations
from pathlib import Path
from urllib.parse import urljoin, urlparse
import html, json, re
from bs4 import BeautifulSoup, NavigableString

BOOKS = [
    ('beginner','A Beginner\'s Guide to Confluent Humanism','Introduction','publications/beginners-guide-to-confluent-humanism/index.html','.v21-guide-article','assets/guides/beginners-guide-to-confluent-humanism-cover.webp'),
    ('book-of-chance','The Book of Chance','Foundational philosophy','read/index.html','MULTI','assets/covers/light-cover.webp'),
    ('parables','The Parables of Chance','Fiction · 12 stories','publications/parables-of-chance/index.html','.parables-article','assets/publications/parables-of-chance-cover.webp'),
    ('five-values','The Five Values','Five complementary values','booklets/the-five-values/index.html','.values-prose','assets/booklets/the-five-values-cover.webp'),
    ('possibilities','The Little Book of Possibilities','Practical philosophy','booklets/the-little-book-of-possibilities/index.html','.possibilities-article','assets/booklets/the-little-book-of-possibilities-cover.webp'),
    ('conversations','Conversations of Chance','Discussion companion','publications/conversations-of-chance/index.html','.conversations-article','assets/publications/conversations-of-chance-cover.webp'),
    ('letter-01','On the People We Never Meet','Letters from H · 01','letters/on-the-people-we-never-meet/index.html','.letters-prose','assets/letters/lfh-001-cover.webp'),
    ('letter-02','When Good Choices Lead to Bad Outcomes','Letters from H · 02','letters/when-good-choices-lead-to-bad-outcomes/index.html','.letters-prose','assets/letters/lfh-002-cover.webp'),
    ('letter-03','What Do We Owe to Strangers?','Letters from H · 03','letters/what-do-we-owe-to-strangers/index.html','.letters-prose','assets/letters/lfh-003-cover.webp'),
]


def E(x): return html.escape(str(x), quote=True)


def rewrite_inline_url(root: Path, page_rel: str, target: str, is_asset=False) -> str:
    if not target or target.startswith(('data:','mailto:','tel:','https://','http://')):return target
    if target.startswith('javascript:'):return ''
    if target.startswith('#'):
        return '../'+page_rel.replace('index.html','')+target
    # resolved against the canonical HTML page; reader lives under /reader/
    full = urljoin('https://thebookofchance.github.io/'+page_rel,target)
    parts=urlparse(full)
    if parts.netloc!='thebookofchance.github.io':return ''
    resolved=parts.path.lstrip('/')
    if is_asset and not (root/resolved).is_file():
        raise AssertionError((page_rel, target, resolved))
    return '../'+resolved+(('?' + parts.query) if parts.query else '')+(('#'+parts.fragment) if parts.fragment else '')


def clean_html(root:Path, page_rel:str, children) -> str:
    fragment=BeautifulSoup('<div></div>','html.parser').div
    for child in children:
        fragment.append(BeautifulSoup(str(child),'html.parser'))
    for tag in fragment.find_all(True):
        if tag.name in ('script','style','iframe','form','button','input','textarea','select','noscript'):
            tag.decompose();continue
        for k in list(tag.attrs):
            if k.lower().startswith('on') or k in ('style','contenteditable','srcset'):
                tag.attrs.pop(k,None)
        if tag.has_attr('src'):
            new=rewrite_inline_url(root,page_rel,str(tag['src']),True)
            if new:tag['src']=new
            else:tag.decompose();continue
        if tag.has_attr('href'):
            new=rewrite_inline_url(root,page_rel,str(tag['href']))
            if new:tag['href']=new;tag['target']='_blank';tag['rel']='noopener noreferrer'
            else:tag.attrs.pop('href',None)
        if tag.name in ('img','svg'):
            tag['loading']='lazy' if tag.name=='img' else None
    return fragment.decode_contents()


def split_article(root:Path, page_rel:str, selector:str):
    doc=BeautifulSoup((root/page_rel).read_text('utf8'),'html.parser')
    article=doc.select_one(selector)
    assert article, (page_rel,selector)
    chunks=[];cur=[];name='Opening';anchor=''
    # Split only at section headings; preserve their full HTML text.
    # Letters, the introductory guide and the Five Values use H2 as sections.
    # Story collections have H3 chapters beneath H2 part dividers.
    stop_tags=('h2','h3') if any(x in page_rel for x in ('parables-of-chance','conversations-of-chance','the-little-book-of-possibilities')) else ('h2',)
    for node in article.find_all(recursive=False):
        if node.name in stop_tags:
            if cur and BeautifulSoup(''.join(str(c) for c in cur),'html.parser').get_text(' ',strip=True):
                chunks.append({'title':name,'source':'../'+page_rel.replace('index.html','')+('#'+anchor if anchor else ''),'html':clean_html(root,page_rel,cur)})
            name=node.get_text(' ',strip=True)
            anchor=node.get('id','')
            cur=[node]
        else:
            cur.append(node)
    if cur:
        chunks.append({'title':name,'source':'../'+page_rel.replace('index.html','')+('#'+anchor if anchor else ''),'html':clean_html(root,page_rel,cur)})
    return [s for s in chunks if BeautifulSoup(s['html'],'html.parser').get_text(' ',strip=True)]


def multi_main_book(root:Path):
    doc=BeautifulSoup((root/'read/index.html').read_text('utf8'),'html.parser')
    anchors=[]
    for a in doc.select('#book-toc .toc-entry, #book-toc .toc-section-head a'):
        rel=a.get('href')
        if not rel or not re.fullmatch(r'[a-z0-9-]+/',rel):continue
        slug=rel.strip('/')
        if slug not in anchors:anchors.append(slug)
    # preserve authored ordering, including introduction, parts and afterword
    sections=[]
    for slug in anchors:
        rel='read/'+slug+'/index.html'
        page=BeautifulSoup((root/rel).read_text('utf8'),'html.parser')
        el=page.select_one('.reading-body');head=page.select_one('.chapter-heading h1')
        assert el and head,slug
        sections.append({'title':head.get_text(' ',strip=True),'source':'../read/'+slug+'/','html':clean_html(root,rel,list(el.children))})
    assert len(sections)==24, len(sections)
    return sections


def build_reader_data(root:Path):
    data={};total_chars=0
    for ident,title,kind,page,selector,cover in BOOKS:
        assert (root/cover).is_file(),cover
        chunks=multi_main_book(root) if selector=='MULTI' else split_article(root,page,selector)
        assert len(chunks)>=4,(ident,len(chunks))
        # Readable content is extracted from verified already-published HTML.
        for c in chunks:
            assert len(BeautifulSoup(c['html'],'html.parser').get_text(' ',strip=True))>18,(ident,c['title'])
        data[ident]={'id':ident,'title':title,'kind':kind,'cover':'../'+cover,
                     'original':'../'+page.replace('index.html',''),'sections':chunks}
        total_chars+=sum(len(x['html']) for x in chunks)
    assert len(data)==9
    out=root/'assets/reader-books-data.js'
    out.write_text('/* Generated from canonical website literature; content is unchanged. */\nwindow.BOC_READER_BOOKS = '+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+';\n',encoding='utf8')
    return data,total_chars


def insert_after(parent,target,node):
    target.insert_after(node)


def apply_v025(root:Path,document,info:dict):
    data,total_chars=build_reader_data(root)
    page_body='''<section class="v25-reader-shell shell" aria-label="Website eReader" id="reader-app">
      <div class="v25-reader-top"><a class="v25-back" href="../downloads/">← Back to the Library</a>
      <span class="v25-reader-name">THE BOOK OF CHANCE · READING ROOM</span><a class="v25-path-link" href="../journey/">Reading paths ↗</a></div>
      <header class="v25-reader-header"><div class="v25-reader-cover"><img data-reader-cover src="../assets/covers/light-cover.webp" width="994" height="1536" alt="Cover of the selected publication" /></div>
      <div class="v25-reader-intro"><span class="eyebrow">A quieter way to read</span><h1 data-reader-title>Reading room</h1><p data-reader-kind>Choose a book from the Library, or begin with the foundational book.</p>
      <div class="v25-reader-tools"><label>Choose a publication <select data-reader-book aria-label="Select publication"></select></label>
      <a href="../read/" data-reader-original>Open original web edition ↗</a></div></div></header>
      <div class="v25-reader-stage"><aside class="v25-reader-aside" aria-label="Book contents" data-reader-aside>
      <div class="v25-aside-title"><h2>Contents</h2><button type="button" data-reader-toggle aria-expanded="true" aria-controls="v25-toc">Hide</button></div>
      <nav id="v25-toc" data-reader-toc aria-label="Sections in this book"></nav></aside>
      <div class="v25-reader-panel"><div class="v25-reading-toolbar"><button class="v25-contents-toggle" type="button" data-reader-toggle aria-expanded="true" aria-controls="v25-toc">Contents ☰</button>
      <span data-reader-section-caption>Choose a section</span><div class="v25-size-tools" aria-label="Text size"><button type="button" data-reader-smaller aria-label="Decrease text size">A−</button><button type="button" data-reader-larger aria-label="Increase text size">A+</button></div></div>
      <div class="v25-paper" id="v25-paper"><div class="v25-paper-viewport" data-reader-viewport><article class="v25-page-flow" data-reader-flow aria-label="Current reading"></article></div>
      <div class="v25-page-line"><span data-reader-page-status aria-live="polite">Preparing pages…</span><span data-reader-location>Stored only on this device</span></div></div>
      <div class="v25-reading-actions"><button type="button" data-reader-prev>← Previous page</button><span data-reader-count>Page 1 of 1</span><button type="button" data-reader-next>Next page →</button></div>
      <div class="v25-reader-footer"><p>Page numbers depend on your screen and text size. Original editions and downloads remain available; some companions are still editorial candidates.</p><button data-reader-clear type="button">Forget my reading place</button></div>
      </div></div><noscript><p>The interactive reader needs JavaScript. All books remain available in the <a href="../downloads/">Library</a> as ordinary web pages and downloadable editions.</p></noscript>
      <div class="v25-reader-error" data-reader-error hidden role="alert">This reader could not start. You can still use the <a href="../downloads/">Library</a> to read online or download a book.</div>
    </section><script defer src="../assets/reader-books-data.js"></script><script defer src="../assets/reader.js"></script>'''
    reader=root/'reader';reader.mkdir(exist_ok=True)
    reader_html=document('Reading Room',page_body,base='../',active='downloads',desc='Read The Book of Chance and its companion writings in a paginated online reading room with chapter navigation and text-size controls.',extra_head='<meta name="robots" content="noindex,follow"><link rel="canonical" href="https://thebookofchance.github.io/reader/">')
    (reader/'index.html').write_text(reader_html,encoding='utf8')
    # Add book actions to the library, while retaining all original read/download links.
    lp=root/'downloads/index.html'
    soup=BeautifulSoup(lp.read_text('utf8'),'html.parser')
    hero=soup.select_one('.library-hero');assert hero
    portal=BeautifulSoup('''<section class="shell v25-library-portal" aria-label="Choose how to explore the library">
       <div class="v25-library-portal-copy"><span class="eyebrow">Your reading room</span><h2>Where will you begin?</h2><p>Follow a question through the library, or open a book and read page by page—without an account.</p></div>
       <div class="v25-library-portal-actions"><a href="../journey/" class="btn btn-primary">Explore reading paths →</a><a href="../reader/?book=book-of-chance" class="btn btn-outline">Open the eReader →</a></div>
       </section>''','html.parser').section
    hero.insert_after(portal)
    prevpromo=soup.select_one('#reading-journeys')
    if prevpromo:prevpromo.decompose()
    cards=soup.select('.v20-catalogue-card')
    assert len(cards)==9,len(cards)
    refs={'beginners-guide':'beginner','foundational-index':'book-of-chance','parables-of-chance':'parables','five-values-booklet':'five-values',
          'little-book-of-possibilities':'possibilities','conversations-of-chance':'conversations','letter-01':'letter-01','letter-02':'letter-02','letter-03':'letter-03'}
    for card in cards:
        key=refs[card.get('id')]
        cover=card.select_one('.v20-catalogue-cover') or card.select_one('img')
        link=cover if cover and cover.name=='a' else cover.find_parent('a') if cover else None
        # Keep cover click semantics unchanged; add a plainly labelled eReader action.
        actions=card.select_one('.v20-catalogue-actions');assert actions
        e=soup.new_tag('a',href='../reader/?book='+key)
        e['class']=['v25-reader-action'];e.string='Read in eReader ↗'
        actions.insert(0,e)
        card['data-reader-id']=key
    # Make the whole catalogue a distinctive library space; covers unchanged.
    collection=soup.select_one('#publication-catalogue');assert collection
    collection['class']=list(collection.get('class',[]))+['v25-library-shelves']
    # Reorder quick-shortcuts to lead with finding a reading path.
    shortcuts=soup.select_one('nav.section-shortcuts')
    if shortcuts:
        j=shortcuts.select_one('a[href="../journey/"]')
        if j: j.extract();shortcuts.find('span').insert_after(j)
    lp.write_text(str(soup),encoding='utf8')
    # Keep the site hero; place reading path directly in the primary CTAs.
    hp=root/'index.html';home=BeautifulSoup(hp.read_text('utf8'),'html.parser')
    actions=home.select_one('.hero-copy .button-line')
    assert actions
    anchor=home.new_tag('a',href='journey/');anchor['class']=['btn','btn-outline','v25-primary-path'];anchor.string='Find a reading path →'
    first=actions.find('a');first.insert_after(anchor)
    # add eReader as an explicit secondary route in the home book collection.
    homebooks=home.select_one('#explore-library');assert homebooks
    intro=homebooks.select_one('.section-head') or homebooks.select_one('header')
    if intro:
        l=home.new_tag('a',href='reader/?book=beginner');l['class']=['v25-home-ereader'];l.string='Or open a book in the eReader ↗';intro.append(l)
    hp.write_text(str(home),encoding='utf8')
    css=root/'assets/site.css'
    base_css=css.read_text('utf8')
    marker='/* v0.25 – Reading Room & Library shelving:'
    if marker in base_css:base_css=base_css.split(marker,1)[0].rstrip()+'\n'
    css.write_text(base_css+'\n'+(root/'source/resources/v025-reader-styles.css').read_text('utf8'),encoding='utf8')
    # This is a duplicate-content reading interface, intentionally noindex.
    # Remove it if prior regeneration added the route to the sitemap.
    sm=root/'sitemap.xml'
    if sm.is_file():
        lines=sm.read_text('utf8').splitlines(keepends=True)
        sm.write_text(''.join(line for line in lines if 'https://thebookofchance.github.io/reader/' not in line),encoding='utf8')
    # Document exact build/release status; don't change candidate flags or manuscript text.
    info['website_version']='0.25'
    info['library_available_publications']=9
    info['reading_room']={'path':'reader/','books':9,'sections':sum(len(x['sections']) for x in data.values()),'storage':'local reading place only','new_publications':0}
    info['cover_changes']=0
    (root/'SITE_CONTENT_MANIFEST.json').write_text(json.dumps(info,indent=2),encoding='utf8')
