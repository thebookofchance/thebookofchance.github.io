"""Website v0.16 — integrate Conversations of Chance with the established editorial site.
Run through scripts/build_site.py after v015_five_values, or call apply_v016
against an up-to-date website root. This never overwrites forms-config.js.
"""
from __future__ import annotations
import html
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

CONVERSATION_TITLES = [
    'The Starting Line', 'The Road Not Taken', 'When Good Choices Fail',
    'Is Tomorrow Already Written?', 'A Small Measure of Influence',
    'The Story We Tell Ourselves', 'A Hope Without a Guarantee',
    'What Can We Pass On?', 'A Place Without a Price',
    'Beyond the Human Circle', 'Who Holds the Keys?',
    'At the Edge of What We Know',
]
READING_SLUGS = [
    'arrival','the-unfolding','fortune-and-hardship','the-open-future',
    'action-within-uncertainty','reflection-and-growth','hope','shared-fortune',
    'fellowship','the-living-world','stewardship','death-and-the-unknown'
]
PART_LABELS=['Part I — What We Inherit','Part II — What We Make Possible','Part III — The Lives We Share']
PDF='files/conversations/Conversations_of_Chance_Editorial_Proof_v0.1.pdf'
EPUB='files/conversations/Conversations_of_Chance_Editorial_Proof_v0.1.epub'
SOURCE='source/conversations/conversations-of-chance.md'
PAGE='publications/conversations-of-chance/'

def slug(text:str)->str:
    text=text.casefold().replace('’',"'")
    return re.sub(r'[^a-z0-9]+','-',text).strip('-')

def _make_article(md:str, markdown):
    # Exclude the cover leaf and duplicated manuscript contents; site TOC replaces it.
    start=md.index('## A Note on This Edition')
    contents=md.index('## Contents',start)
    intro=md.index('## An Invitation to Conversation',contents)
    relevant=md[start:contents].rstrip()+'\n\n'+md[intro:]
    soup=BeautifulSoup(markdown(relevant),'html.parser')
    seen=set(); conversations=0
    for h in soup.find_all(['h1','h2','h3']):
        label=h.get_text(' ',strip=True)
        if label.startswith('Part ') and h.name=='h1':
            h.name='h2';h['class']=['conversations-part']
        elif label.startswith('Conversation ') and h.name=='h2':
            h.name='h3';h['class']=['conversations-chapter'];conversations+=1
        elif label.startswith('Alongside ') and h.name=='h3':
            h.name='h4';h['class']=['conversations-reading-ref']
            assert conversations>0
            parent=h.parent
            # Link the original text, not just the abstract reference.
            link=soup.new_tag('p',attrs={'class':'conversations-original-link'})
            anchor=soup.new_tag('a',href='../../read/'+READING_SLUGS[conversations-1]+'/')
            anchor.string='Read the corresponding Book of Chance reading →'
            link.append(anchor)
            h.insert_after(link)
        else:
            if h.name=='h2':h['class']=['conversations-note-heading']
        ident=slug(label)
        if ident in seen: raise ValueError('Duplicate heading slug: '+ident)
        seen.add(ident)
        h['id']=ident
    assert conversations==12, f'Expected twelve chapters, got {conversations}'
    # Keep user-supplied text escaped by the project's standard mistune engine.
    assert len(soup.get_text(' ',strip=True))>30000, 'Manuscript appears truncated'
    return str(soup)

def _toc_list():
    rows=[]
    for part_ix,part in enumerate(PART_LABELS):
        rows.append(f'<li class="conversations-toc-part"><a href="#{slug(part)}">{html.escape(part)}</a></li>')
        for j in range(part_ix*4,part_ix*4+4):
            title=CONVERSATION_TITLES[j]
            rows.append(f'<li><a href="#{slug("Conversation "+str(j+1)+" — "+title)}"><span>{j+1:02d}</span> {html.escape(title)}</a></li>')
    return '<ol>'+''.join(rows)+'</ol>'

def apply_v016(root:Path, document, markdown, info:dict):
    src=root/SOURCE
    assert all((root/p).is_file() for p in [SOURCE,PDF,EPUB]),'Conversations source and files must be copied to their expected paths'
    md=src.read_text('utf8')
    article=_make_article(md,markdown)
    toc=_toc_list()
    body=f'''<section class="shell conversations-hero">
      <div class="conversations-hero-text"><a class="back-to-toc" href="../../downloads/">← Back to the Library</a>
        <span class="eyebrow">The Book of Chance · Discussion companion 01</span>
        <h1>Conversations<br>of Chance</h1>
        <p class="lead">Twelve Discussions for an Uncertain Life</p>
        <p>Questions for individuals, friends and future gatherings. Explore twelve thoughtful dilemmas about the lives we inherit and the possibilities we shape. You may disagree, read privately or simply follow a question that interests you.</p>
        <div class="button-line"><a class="btn btn-primary" href="#conversations-text">Begin reading ↓</a><a class="btn btn-outline" href="../../{PDF}" download>Download PDF ↓</a><a class="btn btn-outline" href="../../{EPUB}" download>Download EPUB ↓</a></div>
        <p class="conversations-status">12 conversations · 48-page PDF proof · Free · Editorial candidate v0.1 — not a final release</p>
      </div>
      <div class="conversations-cover" aria-label="Conversations of Chance, twelve discussions for an uncertain life, H">
        <div class="conversations-cover-top">THE BOOK OF CHANCE <span>·</span> COMPANIONS</div>
        <div class="conversations-cover-symbol" aria-hidden="true"><img src="../../assets/brand-mark.svg?v=5" alt="" width="94" height="94"/></div>
        <span class="conversations-cover-number">12 conversations</span>
        <strong>Conversations<br><i>of</i> Chance</strong>
        <span class="conversations-cover-sub">Twelve Discussions<br>for an Uncertain Life</span>
        <span class="conversations-cover-author">H</span>
      </div>
    </section>
    <div class="shell conversations-lead"><p><strong>A book that makes room for disagreement.</strong> Each conversation corresponds to one of the twelve foundational readings. Each includes an imagined dilemma, questions, an optional private reflection and a practical invitation. No group, registration, payment or personal disclosure is required.</p><details class="conversations-mobile-contents"><summary>Explore all twelve conversations</summary>{toc}</details></div>
    <div class="shell conversations-layout" id="conversations-text"><aside class="conversations-toc" aria-label="Conversation contents"><strong>Contents</strong><p>Follow a theme or read in order.</p>{toc}</aside>
    <article class="conversations-article" aria-label="Complete text of Conversations of Chance">{article}</article></div>
    <section class="shell conversations-after"><div><span class="eyebrow">Continue the reading</span><h2>One answer need not end the conversation.</h2><p>Every session can begin with a question from the book. The discussions are invitations to think together, not tests of belief, achievement or belonging.</p></div><div class="button-line"><a class="btn btn-outline" href="../../read/">Explore the foundational readings →</a><a class="btn btn-outline" href="../../downloads/">Return to the Library →</a></div></section>
    '''
    d=root/PAGE/'index.html';d.parent.mkdir(parents=True,exist_ok=True)
    # The earlier v0.16 stand-alone proof used noindex, retained for this unapproved editorial candidate.
    d.write_text(document('Conversations of Chance',body,base='../../',active='downloads',
        desc='Twelve thoughtful discussions for an uncertain life: a free conversation companion by H to The Book of Chance, with online reader, PDF and EPUB.',
        extra_head='<link rel="canonical" href="https://thebookofchance.github.io/publications/conversations-of-chance/"><meta name="robots" content="noindex,follow">'),encoding='utf8')

    # Library - keep the published presentation intact and add a dedicated feature.
    library=root/'downloads/index.html';lib=BeautifulSoup(library.read_text('utf8'),'html.parser')
    old=lib.select_one('#conversations-of-chance')
    if old:old.decompose()
    sec=BeautifulSoup(f'''<section class="conversations-library-feature" id="conversations-of-chance">
    <div class="conversations-library-type"><span class="eyebrow">New companion · BOC-CNV-001</span><span class="conversations-library-count" aria-hidden="true">12</span></div>
    <div class="conversations-library-content"><div><h2>Twelve questions worth discussing.</h2><p>What does it mean to make a fair choice when our starting conditions differ? What can hope ask of us when nothing is guaranteed? And how can a group disagree well? <cite>Conversations of Chance</cite> offers twelve original scenarios and guided discussions that follow the twelve readings of <cite>The Book of Chance</cite>.</p><p class="conversations-library-meta">By H · Complete online · 48-page PDF proof · EPUB · Editorial candidate</p>
    <div class="button-line"><a class="btn btn-primary" href="../{PAGE}">Read online →</a><a class="btn btn-outline" href="../{PDF}" download>PDF ↓</a><a class="btn btn-outline" href="../{EPUB}" download>EPUB ↓</a></div></div>
    <div class="conversations-library-quote"><span>FROM THE DISCUSSIONS</span><p>“A useful unresolved question is a result.”</p><small>— H</small></div></div></section>''','html.parser').section
    before=lib.select_one('#five-values-booklet')
    assert before, 'v0.15 Library feature missing; refusing to overwrite'
    before.insert_before(sec)
    count=lib.select_one('.library-count')
    assert count and count.find('small'),'v0.15 library count missing'
    count.find('span').string='06'
    count.find('small').string='Foundational book + three Letters + The Five Values + Conversations of Chance · Plus journals'
    shortcuts=lib.select_one('.section-shortcuts')
    assert shortcuts,'Library quick links missing'
    if not shortcuts.find('a',href='#conversations-of-chance'):
        a=lib.new_tag('a',href='#conversations-of-chance');a.string='Conversations';
        anchor=shortcuts.find('a',href='#featured-book')
        if anchor:anchor.insert_after(a)
        else:shortcuts.append(a)
    library.write_text(str(lib),encoding='utf8')

    # Homepage – newest companion without displacing the accepted brand and original releases.
    hp=root/'index.html';s=BeautifulSoup(hp.read_text('utf8'),'html.parser')
    prior=s.select_one('.conversations-home-feature')
    if prior:prior.decompose()
    feature=BeautifulSoup(f'''<section class="shell conversations-home-feature section-space">
        <div><span class="eyebrow">A new conversation companion · by H</span><h2>What happens when we ask better questions together?</h2><p>Twelve discussions on chance, choices, shared responsibility and the lives we shape. Start on your own, or bring a scenario to friends. You need not agree with every answer—or share anything personal.</p><div class="button-line"><a class="btn btn-primary" href="{PAGE}">Explore Conversations of Chance →</a><a class="btn btn-outline" href="downloads/#conversations-of-chance">Browse the Library</a></div><p class="conversations-home-meta">Free online, PDF and EPUB · Editorial candidate for review</p></div>
        <div class="conversations-home-graphic" aria-hidden="true"><span>THE BOOK OF CHANCE · COMPANIONS</span><strong>12</strong><div class="conversations-graphic-lines"></div><p>QUESTIONS FOR AN UNCERTAIN LIFE</p></div>
    </section>''','html.parser').section
    anchor=s.select_one('.values-home-feature');assert anchor,'Homepage v0.15 Five Values feature missing'
    anchor.insert_before(feature)
    hp.write_text(str(s),encoding='utf8')

    # Catalogue includes statuses that do NOT claim institutional services or approval.
    catfile=root/'source/publications.json';pub=json.loads(catfile.read_text('utf8'))
    pub['conversations']=[{'id':'BOC-CNV-001','title':'Conversations of Chance',
        'subtitle':'Twelve Discussions for an Uncertain Life','author':'H',
        'series':'The Book of Chance — Companions','edition':'v0.1',
        'status':'editorial candidate; founder approval and live testing outstanding',
        'language':'en-NZ','date_prepared':'2026-11-22',
        'source':SOURCE,'url':PAGE,'pdf':PDF,'epub':EPUB,'sessions':12}]
    catfile.write_text(json.dumps(pub,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    # Do not add an unapproved noindex candidate to the public-facing sitemap.
    info.update({'website_version':'0.16','latest_discussion_id':'BOC-CNV-001',
        'conversations_status':'Editorial candidate; H approval and live deployment testing outstanding',
        'conversations':{'online':PAGE,'pdf':PDF,'epub':EPUB,'source':SOURCE,'sessions':12},
        'publications_represented_in_library':6,
        'video_programme':'Deferred until planned publications are completed'})
