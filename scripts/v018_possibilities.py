"""Website v0.18: The Little Book of Possibilities editorial candidate v0.2.

Source-driven integration: online reading, home, library and catalogue.
Keep the accepted cover assets untouched; this script does not generate the PDF/EPUB.
Use via build_site.py or run against an existing v0.17 site with apply_v018(...).
"""
from __future__ import annotations
import html
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

SOURCE = 'source/booklets/the-little-book-of-possibilities.md'
PAGE = 'booklets/the-little-book-of-possibilities/'
PDF = 'files/booklets/The_Little_Book_of_Possibilities_Editorial_Proof_v0.2.pdf'
EPUB = 'files/booklets/The_Little_Book_of_Possibilities_Editorial_Proof_v0.2.epub'
COVER = 'assets/booklets/the-little-book-of-possibilities-cover.webp'
SHARE_IMAGE = 'assets/booklets/the-little-book-of-possibilities-cover.png'
CHAPTER_TITLES = [
    'A Door You Cannot See', 'The Difference Between an Option and a Choice',
    'The Weight of a Starting Place', 'What Tomorrow Does Not Owe Us',
    'Ask Before Opening the Door', 'A Refusal That Keeps Something Whole',
    'The Small Repair', 'Learning Without a Ladder',
    'Fair Rules, Not Only Favours', 'The Possibility of Rest',
    'Lives Beyond the Room', 'Leaving a Key Where Others Can Find It',
]
PART_TITLES = [
    'Part I — Seeing What Is Possible',
    'Part II — Making Room',
    'Part III — Keeping the Future Open',
]


def slug(s: str) -> str:
    s = s.casefold().replace('’', "'")
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def make_article(markdown_source: str, markdown) -> str:
    # The dedicated site table of contents replaces the manuscript's TOC;
    # the note, entire argument, end matter, citations and authorship remain.
    start = markdown_source.index('## A Note on This Edition\n')
    contents = markdown_source.index('## Contents\n', start)
    intro = markdown_source.index('## An Introduction — An Unused Chair\n', contents)
    retained = markdown_source[start:contents].rstrip() + '\n\n' + markdown_source[intro:]
    soup = BeautifulSoup(markdown(retained), 'html.parser')
    seen = set()
    chapters = []
    parts = []
    for heading in soup.find_all(['h1', 'h2', 'h3']):
        raw = heading.get_text(' ', strip=True)
        if heading.name == 'h1' and raw.startswith('Part '):
            heading.name = 'h2'
            heading['class'] = ['conversations-part']
            parts.append(raw)
        elif heading.name == 'h2' and re.match(r'^\d+\.\s', raw):
            heading.name = 'h3'
            heading['class'] = ['conversations-chapter']
            chapters.append(raw)
        elif heading.name == 'h2':
            heading['class'] = ['conversations-note-heading']
        ident = slug(raw)
        if ident in seen:
            raise ValueError('Duplicate manuscript heading: ' + raw)
        seen.add(ident)
        heading['id'] = ident
    assert parts == PART_TITLES, f'Unexpected parts: {parts}'
    assert len(chapters) == 12, f'Expected twelve chapters, found {len(chapters)}'
    for i, name in enumerate(CHAPTER_TITLES, 1):
        assert chapters[i-1] == f'{i}. {name}', f'Unexpected chapter {i}: {chapters[i-1]}'
    for p in soup.find_all('p'):
        if p.get_text(' ', strip=True).startswith('A question to carry:'):
            p['class'] = ['possibilities-question']
    assert len(soup.get_text(' ', strip=True)) > 35000, 'Manuscript seems truncated'
    return str(soup)


def make_toc() -> str:
    rows = ['<li><a href="#an-introduction-an-unused-chair">Introduction · An Unused Chair</a></li>']
    for i, title in enumerate(PART_TITLES):
        rows.append(f'<li class="conversations-toc-part"><a href="#{slug(title)}">{html.escape(title)}</a></li>')
        for j in range(i*4, i*4 + 4):
            heading = f'{j+1}. {CHAPTER_TITLES[j]}'
            rows.append(f'<li><a href="#{slug(heading)}"><span>{j+1:02d}</span> {html.escape(CHAPTER_TITLES[j])}</a></li>')
    rows.append('<li class="conversations-toc-part"><a href="#an-afterword-a-place-at-the-table">Afterword</a></li>')
    rows.append('<li><a href="#a-few-ways-to-begin">A Few Ways to Begin</a></li>')
    rows.append('<li><a href="#further-reading-optional">Further Reading</a></li>')
    return '<ol>' + ''.join(rows) + '</ol>'


def make_body(article: str, toc: str) -> str:
    return f'''<section class="shell conversations-hero possibilities-hero">
      <div class="conversations-hero-text"><a class="back-to-toc" href="../../downloads/">← Back to the Library</a>
      <span class="eyebrow">The Book of Chance · Companion 02</span>
      <h1>The Little Book<br>of Possibilities</h1>
      <p class="lead">On Small Openings and the Conditions We Create</p>
      <p>An independent companion exploring the conditions that make opportunities genuinely possible. Twelve chapters about fairness, permission, cooperation, learning and our power to open—or close—doors for one another.</p>
      <div class="button-line"><a class="btn btn-primary" href="#possibilities-text">Begin reading ↓</a>
      <a class="btn btn-outline" href="../../{PDF}" download>Download PDF ↓</a>
      <a class="btn btn-outline" href="../../{EPUB}" download>Download EPUB ↓</a></div>
      <p class="conversations-status">12 chapters · 42-page PDF reader proof · Free · Editorial candidate v0.2, awaiting manuscript approval</p>
      </div><div class="possibilities-cover-art"><img src="../../{COVER}" alt="The Little Book of Possibilities by H, approved cover with fine charcoal and blue branching paths" width="1000" height="1500" loading="eager"></div>
    </section>
    <div class="shell conversations-lead"><p><strong>A possibility is more than a promise.</strong> This book distinguishes options that are merely imaginable from those people can realistically use. Its scenes are fictional; none claims a guaranteed outcome, a service that is already operating, or an obligation to participate. Read in order or begin wherever a question interests you.</p>
    <details class="conversations-mobile-contents"><summary>Explore the twelve chapters</summary>{toc}</details></div>
    <div class="shell conversations-layout" id="possibilities-text">
      <aside class="conversations-toc" aria-label="Book contents"><strong>Contents</strong><p>Read in order or follow a theme.</p>{toc}</aside>
      <article class="conversations-article possibilities-article" aria-label="Complete text of The Little Book of Possibilities">{article}</article>
    </div>
    <section class="shell conversations-after"><div><span class="eyebrow">After the last page</span><h2>A small opening may be enough to begin.</h2><p>Continue with the foundational readings or explore another independent companion. Your reflection need not become a public pledge or a measure of worth.</p></div>
    <div class="button-line"><a class="btn btn-outline" href="../../read/">Read The Book of Chance →</a><a class="btn btn-outline" href="../../downloads/">Back to the Library →</a></div></section>'''


def local_document_from_template(root: Path, title: str, body: str, desc: str, extra_head: str) -> str:
    """One-time integration aid, not used by the normal build_site.py pipeline."""
    template = BeautifulSoup((root/'publications/conversations-of-chance/index.html').read_text('utf8'), 'html.parser')
    main = template.select_one('main#main')
    assert main is not None
    main.clear()
    fragment = BeautifulSoup(body, 'html.parser')
    for node in list(fragment.contents):
        main.append(node.extract())
    template.title.string = f'{title} · The Book of Chance'
    template.select_one('meta[name="description"]')['content'] = desc
    template.select_one('meta[property="og:title"]')['content'] = f'{title} · The Book of Chance'
    template.select_one('meta[property="og:description"]')['content'] = desc
    template.select_one('meta[property="og:image"]')['content'] = 'https://thebookofchance.github.io/' + SHARE_IMAGE
    canonical = template.select_one('link[rel="canonical"]')
    canonical['href'] = 'https://thebookofchance.github.io/' + PAGE
    if not template.select_one('meta[name="robots"]'):
        tag = template.new_tag('meta', attrs={'name':'robots','content':'noindex,follow'})
        template.head.append(tag)
    return str(template)


def apply_v018(root: Path, document, markdown, info: dict):
    for p in [SOURCE, PDF, EPUB, COVER, SHARE_IMAGE]:
        assert (root/p).is_file(), f'Missing required file: {p}'
    manuscript = (root/SOURCE).read_text('utf8')
    article = make_article(manuscript, markdown)
    toc = make_toc()
    body = make_body(article, toc)
    desc = 'The Little Book of Possibilities by H: twelve free chapters exploring practical opportunities, fairness and how we widen possibilities together.'
    page = root/PAGE/'index.html'
    page.parent.mkdir(parents=True, exist_ok=True)
    if document is None:
        html_page = local_document_from_template(root, 'The Little Book of Possibilities', body, desc, '')
    else:
        html_page = document('The Little Book of Possibilities', body, base='../../', active='downloads', desc=desc,
            extra_head='<link rel="canonical" href="https://thebookofchance.github.io/booklets/the-little-book-of-possibilities/"><meta name="robots" content="noindex,follow">',
            og_image=SHARE_IMAGE)
    page.write_text(html_page, encoding='utf8')

    # Library: add a real publication card and preserve other editions.
    libfile = root/'downloads/index.html'
    lib = BeautifulSoup(libfile.read_text('utf8'), 'html.parser')
    existing = lib.select_one('#little-book-of-possibilities')
    if existing:
        existing.decompose()
    section = BeautifulSoup(f'''<section class="possibilities-library-feature" id="little-book-of-possibilities">
      <div class="possibilities-library-heading"><span class="eyebrow">New companion · BOC-BKL-002</span><h2>A little room can change what happens next.</h2>
      <p><cite>The Little Book of Possibilities</cite> considers the difference between a choice we can imagine and an opportunity we can actually reach. Twelve accessible chapters explore fair access, rest, consent, shared knowledge and everyday actions.</p></div>
      <div class="possibilities-library-card"><img src="../{COVER}" width="1000" height="1500" loading="lazy" alt="The Little Book of Possibilities by H — approved companion cover">
      <div><span class="eyebrow">Companion 02 · 12 chapters · 42-page PDF proof</span><h3>The Little Book of Possibilities</h3>
      <p class="possibilities-library-subtitle">On Small Openings and the Conditions We Create</p>
      <p>A short literary work on how we can widen possibilities without pretending to control every outcome.</p>
      <div class="button-line"><a class="btn btn-primary" href="../{PAGE}">Read online →</a>
      <a class="btn btn-outline" download href="../{PDF}">PDF ↓</a><a class="btn btn-outline" download href="../{EPUB}">EPUB ↓</a></div>
      <p class="possibilities-meta">Cover approved · Manuscript v0.2 is an editorial candidate, not a final release</p></div></div></section>''', 'html.parser').section
    anchor = lib.select_one('#conversations-of-chance')
    assert anchor is not None, 'Cannot locate v0.17 library insertion point'
    anchor.insert_before(section)
    count = lib.select_one('.library-count')
    assert count and count.select_one('small')
    count.find('span').string = '07'
    count.select_one('small').string = 'Foundational book + three Letters + three companion titles · Plus journals'
    shortcuts = lib.select_one('.section-shortcuts')
    assert shortcuts is not None
    if not shortcuts.select_one('a[href="#little-book-of-possibilities"]'):
        a = lib.new_tag('a', href='#little-book-of-possibilities')
        a.string = 'Possibilities'
        before = shortcuts.select_one('a[href="#conversations-of-chance"]')
        if before:
            before.insert_before(a)
        else:
            shortcuts.append(a)
    libfile.write_text(str(lib), encoding='utf8')

    # Homepage: use the approved cover in the same editorial layout as companion releases.
    homepage = root/'index.html'
    home = BeautifulSoup(homepage.read_text('utf8'), 'html.parser')
    previous = home.select_one('.possibilities-home-feature')
    if previous:
        previous.decompose()
    feature = BeautifulSoup(f'''<section class="shell possibilities-home-feature section-space">
      <div><span class="eyebrow">The next companion · by H</span><h2>What makes a possibility real?</h2>
      <p>A doorway can look open while the way towards it remains out of reach. This twelve-chapter book explores the conditions that turn opportunities into usable choices—and the thoughtful actions that can make room for others.</p>
      <div class="button-line"><a class="btn btn-primary" href="{PAGE}">Read The Little Book of Possibilities →</a><a class="btn btn-outline" href="downloads/#little-book-of-possibilities">Explore the Library</a></div>
      <p class="possibilities-meta">Free online, PDF and EPUB · Manuscript editorial candidate v0.2</p></div>
      <img src="{COVER}" alt="The Little Book of Possibilities by H — illustrated companion cover" width="1000" height="1500" loading="lazy"></section>''','html.parser').section
    before = home.select_one('.conversations-home-feature')
    assert before is not None, 'Cannot locate current homepage companion'
    before.insert_before(feature)
    homepage.write_text(str(home), encoding='utf8')

    # Catalogue: preserve the already-released work and append a new editorial candidate.
    catfile = root/'source/publications.json'
    cat = json.loads(catfile.read_text('utf8'))
    books = [entry for entry in cat.get('booklets',[]) if entry.get('id') != 'BOC-BKL-002']
    books.append({
        'id':'BOC-BKL-002', 'title':'The Little Book of Possibilities',
        'subtitle':'On Small Openings and the Conditions We Create', 'author':'H',
        'series':'The Book of Chance — Companions', 'edition':'v0.2',
        'status':'editorial candidate; cover approved; manuscript author sign-off and live check outstanding',
        'language':'en-NZ', 'date_prepared':'2026-11-22',
        'source':SOURCE, 'url':PAGE, 'cover':COVER, 'pdf':PDF, 'epub':EPUB,
        'chapters':12, 'pdf_pages':42,
    })
    cat['booklets'] = books
    catfile.write_text(json.dumps(cat, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    info.update({
        'website_version':'0.18', 'library_available_publications':7,
        'publications_represented_in_library':7,
        'latest_companion_id':'BOC-BKL-002',
        'possibilities_status':'Editorial candidate v0.2; cover approved; author approval, accessibility and live checks pending',
        'possibilities':{'online':PAGE, 'pdf':PDF, 'epub':EPUB, 'source':SOURCE, 'cover':COVER, 'chapters':12, 'pdf_pages':42},
        'video_programme':'Deferred until planned publications completed',
    })


if __name__ == '__main__':
    import mistune
    root=Path(__file__).resolve().parents[1]
    metadata={}
    apply_v018(root,None,mistune.create_markdown(escape=True,plugins=['table','strikethrough','url']),metadata)
    print('Integrated The Little Book of Possibilities:',metadata['website_version'])
