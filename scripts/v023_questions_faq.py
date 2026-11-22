"""v0.23 -- Source-driven, public-facing FAQ reader integration.

Runs after v0.21. Does not open membership, collect input, change interest
forms, release the FAQ for indexing, or alter the main publication counts.
"""
from __future__ import annotations
import html, json, re
from pathlib import Path
from bs4 import BeautifulSoup

SLUG='questions-about-chance'
ROUTE='questions/'
SRC='source/resources/questions-about-chance.md'
DATA='source/resources/questions-about-chance.json'
COVER='assets/resources/questions-about-chance-cover.webp'
COVER_PNG='assets/resources/questions-about-chance-cover.png'
PDF='files/resources/Questions_About_Chance_FAQ_Editorial_Proof_v0.3.pdf'
EPUB='files/resources/Questions_About_Chance_FAQ_Editorial_Proof_v0.3.epub'
TITLE='Questions About Chance'

def e(s):return html.escape(str(s),quote=True)


def apply_v023(root:Path, document, markdown, info:dict):
    for p in (SRC,DATA,COVER,COVER_PNG,PDF,EPUB):
        assert (root/p).is_file(), f'Missing FAQ component: {p}'
    data=json.loads((root/DATA).read_text('utf8'))
    assert data['edition']=='v0.3' and len(data['questions'])==26
    assert len(data['categories'])==5
    assert [q['number'] for q in data['questions']]==list(range(1,27))
    canonical=(root/SRC).read_text('utf8')
    assert 'Foundational Identity v1.0-RC1' not in canonical
    assert not re.search(r'\bRNG\b',canonical,re.I)
    start=canonical.index('## Before the questions')
    pre=canonical[start:canonical.index('## I. Starting with the basics')]
    # Intro contains both the heading and introduction text.
    pre_html=markdown(pre)
    for attr in ('title','subtitle','id','edition'):
        assert data[attr]

    buttons=['<button type="button" class="v23-faq-filter" data-faq-filter="all" aria-pressed="true">All questions <span>26</span></button>']
    for cat in data['categories']:
        n=sum(q['category_id']==cat['id'] for q in data['questions'])
        buttons.append(f'<button type="button" class="v23-faq-filter" data-faq-filter="{e(cat["id"])}" aria-pressed="false">{e(cat["title"])} <span>{n}</span></button>')
    groups=[]
    for i,cat in enumerate(data['categories']):
        qq=[q for q in data['questions'] if q['category_id']==cat['id']]
        questions=[]
        for q in qq:
            question=e(q['question'])
            answer=markdown(q['answer_markdown'])
            questions.append(f'''<details class="v23-faq-question" id="{e(q['id'])}" data-faq-question data-category="{e(cat['id'])}" data-search="{e((q['question']+' '+q['answer_markdown']+' '+cat['title']).casefold())}">
                <summary><span class="v23-number" aria-hidden="true">{q['number']:02d}</span><span class="v23-faq-qtitle">{question}</span><span class="v23-plus" aria-hidden="true"></span></summary>
                <div class="v23-faq-answer">{answer}</div></details>''')
        groups.append(f'''<section class="v23-faq-group" id="category-{e(cat['id'])}" data-faq-group>
        <div class="v23-group-heading"><span class="eyebrow">Theme {i+1:02d}</span><h2>{e(cat['title'])}</h2><span>{len(qq)} questions</span></div>
        {''.join(questions)}</section>''')
    more=canonical[canonical.index('## Where can I read further?'):canonical.index('## A note on sources, status and authorship')]
    # The end note is public but accessible without needing to parse internal references.
    more_html=markdown(more)
    hero=f'''<section class="shell v23-faq-hero">
      <div class="v23-faq-hero-copy"><a class="back-to-toc" href="../downloads/">← Back to the Library</a>
      <span class="eyebrow">The Book of Chance · Reader resources</span><h1>Questions<br>About Chance</h1>
      <p class="lead">Twenty-six questions about Confluent Humanism and the Fellowship of Chance.</p>
      <p>No belief, membership or account is required. Explore the challenging questions as well as the familiar ones. These answers explain a developing philosophy and proposed community, not a guarantee of services.</p>
      <div class="button-line"><a class="btn btn-primary" href="#faq-search">Explore the questions ↓</a>
      <a class="btn btn-outline" href="../{PDF}" download>Download PDF ↓</a>
      <a class="btn btn-outline" href="../{EPUB}" download>Download EPUB ↓</a></div>
      <p class="v23-faq-status">By H · 26 questions · 5 themes · Free · Revised editorial candidate v0.3</p></div>
      <img class="v23-faq-cover" src="../{COVER}" width="1000" height="1500" alt="Approved Questions About Chance cover, with a question-mark motif in flowing blue and charcoal lines" loading="eager">
    </section>'''
    body=hero+f'''<div class="shell v23-faq-intro">{pre_html}</div>
    <section class="shell v23-faq-explorer" id="faq-explorer" aria-labelledby="v23-explore-title">
      <header class="v23-explore-head"><div><span class="eyebrow">Find a question</span><h2 id="v23-explore-title">An open conversation.</h2></div><p>Search the wording of a question or an answer, or browse by theme. Everything is searched locally in your browser; no information is sent or saved.</p></header>
      <label for="faq-search" class="v23-search-label">Search questions and answers</label>
      <div class="v23-search-wrap"><span aria-hidden="true">⌕</span><input id="faq-search" type="search" autocomplete="off" placeholder="Try 'free will', 'prayer', 'donations' or 'H'" aria-describedby="faq-search-help"><button type="button" id="faq-clear" class="v23-clear" hidden>Clear</button></div>
      <p id="faq-search-help" class="v23-search-help">No account or tracking. Open a question to read its full answer.</p>
      <div class="v23-filter-bar" role="group" aria-label="Filter by FAQ theme">{''.join(buttons)}</div>
      <p class="v23-results" id="faq-results" role="status" aria-live="polite">Showing all 26 questions</p>
      <div class="v23-faq-groups">{''.join(groups)}</div>
      <p class="v23-no-results" id="faq-empty" hidden>No questions match your search. Try a different word or select All questions.</p>
    </section>
    <section class="shell v23-faq-more" aria-label="Read further">{more_html}<p class="v23-editorial-note">This is an editorial candidate, not a statement that the proposed Council, membership or support programmes exist. The cover is a concept pending final approval; independent human reading, accessibility and live checks remain outstanding.</p></section>'''
    out=root/ROUTE/'index.html';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(document(TITLE,body,base='../',active='downloads',desc='Clear answers to 26 questions about chance, free will, faith, ethical responsibility and the proposed Fellowship of Chance.',og_image=COVER_PNG,extra_head='<link rel="canonical" href="https://thebookofchance.github.io/questions/"><meta name="robots" content="noindex,follow"><script defer src="../assets/faq.js?v=0.23"></script>'),encoding='utf8')

    pub=root/'source/publications.json'
    catalog=json.loads(pub.read_text('utf8'))
    catalog['reader_resources']=[{'id':'BOC-FAQ-001','title':TITLE,'subtitle':data['subtitle'],'edition':'v0.3','author':'H','status':'editorial candidate, approved for website staging only','url':ROUTE,'cover':COVER,'pdf':PDF,'epub':EPUB,'source':SRC,'questions':26,'themes':5}]
    pub.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

    def make_snippet(href):
        return BeautifulSoup(f'<a class="v23-faq-inline" href="{href}">Have a question? Explore 26 answers about chance, belief and the Fellowship →</a>','html.parser').a

    # One quiet discovery link on the homepage; no sixth promotion or new navbar tab.
    hp=root/'index.html'; home=BeautifulSoup(hp.read_text('utf8'),'html.parser')
    foot=home.select_one('.v20-collection-foot')
    assert foot,'Homepage collection footer not found'
    foot.insert_after(make_snippet('questions/'))
    hp.write_text(str(home),encoding='utf8')

    library=root/'downloads/index.html';lib=BeautifulSoup(library.read_text('utf8'),'html.parser')
    catalogue=lib.select_one('#publication-catalogue');assert catalogue
    teaser=BeautifulSoup('''<aside id="questions-about-chance" class="v23-faq-teaser" aria-labelledby="v23-faq-teaser-title"><div><span class="eyebrow">Public reader resource · Editorial candidate</span><h2 id="v23-faq-teaser-title">Questions are part of the reading.</h2><p>Curious about faith, free will, giving or the proposed Fellowship? Explore clear answers to twenty-six questions—including the difficult ones.</p></div><a class="btn btn-outline" href="../questions/">Browse Questions About Chance →</a></aside>''','html.parser').aside
    catalogue.insert_after(teaser)
    shortcuts=lib.select_one('.section-shortcuts')
    if shortcuts:
        first=shortcuts.find('a',href='#publication-catalogue')
        a=lib.new_tag('a',href='#questions-about-chance');a.string='Questions'
        if first:first.insert_after(a)
        else:shortcuts.append(a)
    library.write_text(str(lib),encoding='utf8')

    about=root/'about/index.html';soup=BeautifulSoup(about.read_text('utf8'),'html.parser')
    ph=soup.select_one('.page-hero')
    assert ph
    ph.append(BeautifulSoup('<p class="v23-about-faq">Have questions about the philosophy, faith or the future Fellowship? <a href="../questions/">Read Questions About Chance →</a></p>','html.parser').p)
    about.write_text(str(soup),encoding='utf8')

    guide=root/'publications/beginners-guide-to-confluent-humanism/index.html';g=BeautifulSoup(guide.read_text('utf8'),'html.parser')
    following=g.select_one('.v21-guide-after');assert following
    following.append(BeautifulSoup('<a class="v23-guide-faq" href="../../questions/">More questions? Explore the FAQ →</a>','html.parser').a)
    guide.write_text(str(g),encoding='utf8')

    # Explicitly noindex during editorial staging. No sitemap entry added.
    sitemap=root/'sitemap.xml'
    if sitemap.exists():
        old=sitemap.read_text('utf8')
        old=re.sub(r'<url>\s*<loc>https://thebookofchance.github.io/questions/?</loc>\s*</url>\s*','',old)
        sitemap.write_text(old,encoding='utf8')
    info.update({'website_version':'0.23','faq_resource':{'id':'BOC-FAQ-001','url':ROUTE,'source':SRC,'pdf':PDF,'epub':EPUB,'questions':26,'themes':5},'faq_status':'Revised editorial candidate v0.3, staged noindex; cover and final release approval pending','resources_stage':'Questions About Chance FAQ staged; next guided reading journey'})
