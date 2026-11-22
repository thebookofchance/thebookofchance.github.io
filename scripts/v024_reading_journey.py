"""Guided Reading Journey v0.24 — source-driven, no user data collection.

Runs after v023 on every website rebuild.  Uses exact links to previously
published online text and does not edit any literature, download, or status.
"""
from __future__ import annotations
import html
import json
from pathlib import Path
import re
from urllib.parse import urldefrag, unquote
from bs4 import BeautifulSoup

DATA = 'source/resources/guided-reading-journey.json'
ROUTE = 'journey/'


def escape(s):
    return html.escape(str(s), quote=True)


def verified_routes(root, data):
    # Re-check all internal destinations and anchors, and reject duplicates.
    assert data['edition'] == 'v0.1'
    routes = data['paths']
    ids = set()
    for route in routes:
        rid = route['id']
        assert rid not in ids and rid.replace('-', '').isalnum(), rid
        ids.add(rid)
        assert len(route['steps']) == 3, rid
        for step in route['steps']:
            p, anchor = urldefrag(step['href'])
            assert not p.startswith('/') and '://' not in p and '..' not in p
            dest = (root/p)
            if dest.is_dir():
                dest = dest/'index.html'
            assert dest.is_file(), (rid, step['title'], str(dest))
            if anchor:
                parsed=BeautifulSoup(dest.read_text(encoding='utf8'),'html.parser')
                assert parsed.find(id=unquote(anchor)), (rid, step['title'], anchor)
    assert len(routes) == 8
    return routes


def path_selector(item, index):
    slug='path-'+item['id']
    return f'''<a class="v24-choice" href="#{escape(slug)}" data-journey-choice="{escape(slug)}" aria-controls="{escape(slug)}">
        <span class="v24-choice-top"><span class="v24-choice-index">{index:02d}</span><span class="v24-choice-line" aria-hidden="true"></span></span>
        <span class="v24-choice-title">{escape(item['title'])}</span>
        <span class="v24-choice-prompt">{escape(item['prompt'])}</span>
        <span class="v24-choice-link">Explore this path <span aria-hidden="true">↗</span></span>
      </a>'''


def path_panel(item):
    name=escape(item['title'])
    key='path-'+item['id']
    steps=[]
    for n, step in enumerate(item['steps'],1):
        steps.append(f'''<li class="v24-stop" data-journey-stop>
          <div class="v24-stop-top"><span class="v24-stop-number" aria-hidden="true">{n:02d}</span><div>
            <span class="v24-stop-kind">{escape(step['stage'])} · {escape(step['type'])}</span>
            <h3>{escape(step['title'])}</h3>
            <p class="v24-stop-source">{escape(step['source'])}</p>
          </div></div>
          <p class="v24-stop-reason">{escape(step['why'])}</p>
          <div class="v24-stop-actions"><a class="v24-stop-read" href="../{escape(step['href'])}" target="_blank" rel="noopener">Open the reading <span aria-hidden="true">↗</span><span class="sr-only"> (opens in a new tab)</span></a>
          <label class="v24-check"><input type="checkbox" data-journey-check aria-label="Mark {escape(step['title'])} as explored"><span>Explored</span></label></div>
        </li>''')
    return f'''<section id="{escape(key)}" class="v24-route" data-journey-panel aria-labelledby="{escape(key)}-title">
        <div class="v24-route-head"><div><span class="eyebrow">A reading journey · Three suggested stops</span>
          <h2 id="{escape(key)}-title" tabindex="-1">{name}</h2>
          <p>{escape(item['description'])}</p></div>
          <a class="v24-back" href="#choose-a-path" data-journey-back>← Choose another theme</a></div>
        <div class="v24-progress" data-journey-progress><div><span class="v24-progress-caption">Your progress (this page only)</span>
          <strong data-journey-progress-text>0 of 3 explored</strong></div>
          <button type="button" data-journey-reset>Reset this path</button></div>
        <ol class="v24-steps">{''.join(steps)}</ol>
        <aside class="v24-reflection"><span class="eyebrow">An optional reflection</span><p>{escape(item['reflection'])}</p>
          <small>This is a question to think about, not a form. Nothing needs to be written or shared.</small></aside>
      </section>'''


def apply_v024(root:Path, document, info:dict):
    data=json.loads((root/DATA).read_text(encoding='utf8'))
    routes=verified_routes(root,data)
    path_cards=''.join(path_selector(item,i) for i,item in enumerate(routes,1))
    panels=''.join(path_panel(item) for item in routes)
    body=f'''<section class="shell v24-hero" aria-labelledby="journey-title"><div class="v24-hero-copy">
        <a class="back-to-toc" href="../downloads/">← Back to the Library</a>
        <span class="eyebrow">The Book of Chance · A guide through the writings</span>
        <h1 id="journey-title">Find a path<br><em>into the questions.</em></h1>
        <p class="lead">You don't have to start at the beginning.</p>
        <p>Choose a theme that interests you. Each path connects three free readings—from philosophy to stories and questions. Follow one, explore several, or simply browse the library.</p>
        <div class="button-line"><a class="btn btn-primary" href="#choose-a-path">Choose a theme ↓</a>
        <a class="btn btn-outline" href="../downloads/">Browse every publication →</a></div>
        <p class="v24-hero-note">No quiz. No account. No personal answers are collected. You can change paths whenever you like.</p>
      </div><div class="v24-hero-art" aria-hidden="true">
        <img class="v24-cover v24-cover-left" src="../assets/booklets/the-five-values-cover.webp" alt="" loading="eager" width="1000" height="1500">
        <img class="v24-cover v24-cover-main" src="../assets/covers/light-cover.webp" alt="" loading="eager" width="994" height="1536">
        <img class="v24-cover v24-cover-right" src="../assets/publications/parables-of-chance-cover.webp" alt="" loading="eager" width="1000" height="1500">
      </div></section>
      <section class="shell v24-chooser" id="choose-a-path" aria-labelledby="choose-path-heading">
        <div class="v24-chooser-head"><div><span class="eyebrow">A place to begin</span>
          <h2 id="choose-path-heading">Which question draws you in?</h2></div>
          <p>There is no correct choice and no ranking. Select a theme to see three specific places to begin reading.</p></div>
        <div class="v24-choices">{path_cards}</div>
      </section>
      <div class="shell v24-route-region" data-journey-root>
        <div class="v24-choose-hint"><span class="eyebrow">Your next step</span><h2>Choose any path above.</h2>
          <p>We'll show the selected readings here. You can always return to choose another path.</p></div>
        {panels}
      </div>
      <section class="shell v24-outro"><span class="eyebrow">Keep exploring</span>
        <h2>A journey doesn't need an ending.</h2><p>These routes are invitations to read and question, not personal diagnoses or promises of good fortune. Some companion texts are still editorial candidates. You are welcome to disagree with any of them.</p>
        <div class="v24-outro-links"><a href="../questions/">Questions About Chance →</a>
          <a href="../reflect/">Try a private reflection →</a><a href="../downloads/">The full Library →</a></div>
      </section>'''
    out=root/ROUTE/'index.html'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(document('Guided Reading Journey',body,base='../',active='downloads',
        desc='Explore The Book of Chance through eight guided themes, each linking three free readings. No account, quiz or personal answers required.',
        extra_head='<link rel="canonical" href="https://thebookofchance.github.io/journey/"><meta name="robots" content="noindex,follow"><script defer src="../assets/journey.js?v=0.24"></script>'),encoding='utf8')

    # Add a single low-pressure route into the tool from the curated collection.
    home_path=root/'index.html'
    home=BeautifulSoup(home_path.read_text(encoding='utf8'),'html.parser')
    foot=home.select_one('.v20-collection-foot');assert foot
    link=BeautifulSoup('<a class="v24-journey-inline" href="journey/">Not sure what to read? Follow a guided reading path →</a>','html.parser').a
    foot.insert_after(link)
    home_path.write_text(str(home),encoding='utf8')

    # Place this before the FAQ box so newcomers have a choice of next steps.
    lib_path=root/'downloads/index.html'
    lib=BeautifulSoup(lib_path.read_text(encoding='utf8'),'html.parser')
    faq=lib.select_one('#questions-about-chance');assert faq
    promo=BeautifulSoup('''<aside class="v24-library-promo" id="reading-journeys" aria-labelledby="reading-journeys-title"><div>
       <span class="eyebrow">Find your way through the library</span><h2 id="reading-journeys-title">Begin with a question.</h2>
       <p>Not sure what to read first? Pick an interest and follow three suggested readings through the collection. No account or quiz needed.</p></div>
       <a class="btn btn-outline" href="../journey/">Explore reading paths →</a></aside>''','html.parser').aside
    faq.insert_before(promo)
    shortcuts=lib.select_one('.section-shortcuts'); assert shortcuts
    catalog_shortcut=shortcuts.find('a',href='#publication-catalogue')
    a=lib.new_tag('a',href='#reading-journeys');a.string='Reading paths'
    if catalog_shortcut:catalog_shortcut.insert_after(a)
    else:shortcuts.append(a)
    lib_path.write_text(str(lib),encoding='utf8')

    # Links from the most relevant existing welcoming resources.
    guide_path=root/'publications/beginners-guide-to-confluent-humanism/index.html'
    guide=BeautifulSoup(guide_path.read_text(encoding='utf8'),'html.parser')
    after=guide.select_one('.v21-guide-after'); assert after
    a=guide.new_tag('a',href='../../journey/');a['class']='v24-guide-link';a.string='Choose a guided reading path →'
    after.append(a)
    guide_path.write_text(str(guide),encoding='utf8')

    faq_path=root/'questions/index.html'
    faq=BeautifulSoup(faq_path.read_text(encoding='utf8'),'html.parser')
    more=faq.select_one('.v23-faq-more');assert more
    link=faq.new_tag('p');link['class']='v24-faq-link'; a=faq.new_tag('a',href='../journey/');a.string='Explore a guided reading path →';link.append(a); more.append(link)
    faq_path.write_text(str(faq),encoding='utf8')

    reader_path=root/'read/index.html'
    reader=BeautifulSoup(reader_path.read_text(encoding='utf8'),'html.parser')
    hero=reader.select_one('.page-hero')
    if hero:
        p=reader.new_tag('p');p['class']='v24-reader-link';a=reader.new_tag('a',href='../journey/');a.string='Prefer to follow a theme? Try a guided reading path →';p.append(a);hero.append(p)
    reader_path.write_text(str(reader),encoding='utf8')

    # Editorial candidate tool, so keep its new route out of the public sitemap for now.
    sitemap=root/'sitemap.xml'
    if sitemap.exists():
        xml=sitemap.read_text(encoding='utf8')
        xml=re.sub(r'<url>\s*<loc>https://thebookofchance\.github\.io/journey/?</loc>\s*</url>\s*', '', xml)
        sitemap.write_text(xml, encoding='utf8')

    # A reader resource, not a tenth book; no changes to publication statuses.
    cat=root/'source/publications.json'
    catalogue=json.loads(cat.read_text(encoding='utf8'))
    catalogue['guided_reading_journey']={
        'id':'BOC-RES-JOURNEY-001','title':'Guided Reading Journey','url':ROUTE,
        'source':DATA,'status':'Website staging candidate; review and live verification pending',
        'paths':len(routes),'steps_per_path':3,'collects_personal_data':False
    }
    cat.write_text(json.dumps(catalogue,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    info.update({'website_version':'0.24','guided_reading_journey':{
        'url':ROUTE,'source':DATA,'themes':len(routes),'steps_per_path':3,
        'search_or_quiz':'None','progress':'Temporary browser-page state only',
        'status':'Staged noindex; release checks to follow'},
        'library_index_count':9,'literature_approval_status':'Not changed; separate review phase to follow'})
