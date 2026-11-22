"""Refined journals / publication-series expansion. Applied after v0.8 overlays."""
from pathlib import Path
import json
from bs4 import BeautifulSoup


def between(s,head,tail,replacement,why):
    a=s.find(head)
    if a<0:raise AssertionError('Missing start for '+why)
    b=s.find(tail,a+len(head))
    if b<0:raise AssertionError('Missing end for '+why)
    return s[:a]+replacement+s[b:]

def once(s,a,b,why):
    if s.count(a)!=1:raise AssertionError(f'{why} expected one match, got {s.count(a)}')
    return s.replace(a,b,1)

def edit(root,rel,fn):
    p=root/rel
    original=p.read_text('utf8');updated=fn(original)
    if updated==original:raise AssertionError('No update '+rel)
    assert BeautifulSoup(updated,'html.parser').find('main')
    p.write_text(updated,'utf8')

MAIN='files/reflection/The_Reflection_Journal_Fillable.pdf'
DARK='files/reflection/The_Reflection_Journal_Dark_Fillable.pdf'
DAILY='files/reflection/The_Daily_Reflection_Journal_Fillable.pdf'
POSS='files/reflection/The_Possibility_Journal_Fillable.pdf'


def library(s):
    new='''<section class="journal-series" id="reflection-journal" aria-labelledby="series-title"><div class="journal-series-heading"><div><span class="eyebrow">The Book of Chance · Companion publications</span><h2 id="series-title">A journal for the life you're living.</h2></div><p>Four free fillable PDFs across three complementary journals. Begin with the complete companion, or choose a focused practice. None requires membership or a daily commitment.</p></div>
    <div class="journal-edition-pair"><article class="journal-edition"><img src="../assets/journals/reflection-light.webp" alt="Light Edition cover of The Reflection Journal" loading="lazy" width="605" height="907"><div><span class="eyebrow">The complete companion · Light Edition</span><h3>The Reflection Journal</h3><p>48 pages combining daily reflection, acts of possibility, weekly review, a Turning of Chance and open writing space.</p><p class="journal-detail">Same interior as the Dark Edition. Fillable PDF · 6 × 9 in.</p><a class="btn btn-primary" href="../files/reflection/The_Reflection_Journal_Fillable.pdf" download>Download Light Edition · PDF ↓</a></div></article>
    <article class="journal-edition"><img src="../assets/journals/reflection-dark.webp" alt="Dark Edition cover of The Reflection Journal" loading="lazy" width="605" height="907"><div><span class="eyebrow">The complete companion · Dark Edition</span><h3>A different opening, the same reflections.</h3><p>The same 48-page journal in a charcoal cover, matching the two-edition idea of <cite>The Book of Chance</cite>.</p><p class="journal-detail">Same interior as the Light Edition. Fillable PDF · 6 × 9 in.</p><a class="btn btn-outline" href="../files/reflection/The_Reflection_Journal_Dark_Fillable.pdf" download>Download Dark Edition · PDF ↓</a></div></article></div>
    <div class="journal-focused-heading"><span class="eyebrow">Focused companions · Different purposes, not just new covers</span><h3>Choose a practice to return to.</h3></div>
    <div class="journal-focused-grid"><article class="journal-focused"><img src="../assets/journals/daily.webp" alt="The Daily Reflection Journal cover" loading="lazy" width="605" height="907"><div><span class="eyebrow">01 · Personal reflection</span><h4>The Daily Reflection Journal</h4><p>40 pages for noticing circumstance and choice, with fourteen full entries, two weekly reviews and open pages. No streaks, scores or requirement to write every day.</p><a class="btn btn-outline" href="../files/reflection/The_Daily_Reflection_Journal_Fillable.pdf" download>Download Daily Journal · PDF ↓</a></div></article>
    <article class="journal-focused"><img src="../assets/journals/possibility.webp" alt="The Possibility Journal cover" loading="lazy" width="605" height="907"><div><span class="eyebrow">02 · Care and contribution</span><h4>The Possibility Journal</h4><p>40 pages for thoughtful acts of support: twelve guided opportunities, three follow-up reviews and open pages. Consent and personal boundaries are built in.</p><a class="btn btn-outline" href="../files/reflection/The_Possibility_Journal_Fillable.pdf" download>Download Possibility Journal · PDF ↓</a></div></article></div>
    <p class="journal-series-footer">All journals are free, private by default, and editable with compatible PDF readers. Some mobile or browser viewers cannot save form fields; we recommend downloading a copy and testing a short entry. Physical editions are ideas under development, not products currently for sale. <a href="../reflect/">Prefer to write online?</a></p></section>'''
    s=between(s,'<section class="library-journal" id="reflection-journal">','<section class="shell library-resources" id="practice-guides">',new,'library journal feature')
    s=once(s,'<a href="#reflection-journal">Reflection Journal</a>','<a href="#reflection-journal">Journals</a>','library anchors')
    return s

def reflect(s):
    new='''<section class="journal-feature journal-feature-v09" id="reflection-journal"><div class="shell journal-feature-inner"><div class="journal-feature-book"><img src="../assets/journals/reflection-light.webp" alt="The Reflection Journal, Light Edition cover" width="605" height="907" loading="lazy"></div><div class="journal-copy"><span class="eyebrow">Book of Chance companions · Free fillable PDFs</span><h2>Return to a page that's yours.</h2><p>Our redesigned 48-page Reflection Journal brings together daily, action and weekly practices, with a longer Turning of Chance and open writing space. Its Light and Dark covers belong alongside the two editions of the book.</p><p>Prefer a narrower focus? The Daily Reflection Journal and Possibility Journal each have their own guided prompts—not just different covers.</p><div class="button-line"><a class="btn btn-primary" href="../files/reflection/The_Reflection_Journal_Fillable.pdf" download>Download the complete journal · PDF ↓</a><a class="btn btn-outline" href="../downloads/#reflection-journal">See all journal editions</a></div><p class="journal-note">The fillable PDFs stay on your device. A compatible PDF reader is recommended for saving entries. Digital downloads are free; physical journals are not yet available.</p></div></div></section>'''
    return between(s,'<section class="journal-feature" id="reflection-journal">','<section class="shell section-space" id="reflection-guides">',new,'reflect journal')

def home(s):
    return once(s,'fillabe 28-page journal','fillable 48-page journal','old home label') if 'fillabe 28-page journal' in s else once(s,'fillab'+ 'le 28-page journal','fillable 48-page journal','home journal length')

def apply_v09(root:Path,info:dict):
    edit(root,'downloads/index.html',library)
    edit(root,'reflect/index.html',reflect)
    edit(root,'index.html',home)
    catalogue=root/'source/publications.json';data=json.loads(catalogue.read_text('utf8'))
    extra=[
     {'id':'reflection-journal','title':'The Reflection Journal — Light Edition','kind':'Free fillable journal PDF','file':MAIN},
     {'id':'reflection-journal-dark','title':'The Reflection Journal — Dark Edition','kind':'Free fillable journal PDF','file':DARK},
     {'id':'daily-reflection-journal','title':'The Daily Reflection Journal','kind':'Free fillable journal PDF','file':DAILY},
     {'id':'possibility-journal','title':'The Possibility Journal','kind':'Free fillable journal PDF','file':POSS}
    ]
    data['resources']=[e for e in data['resources'] if e.get('id') not in {'reflection-journal','reflection-journal-dark','daily-reflection-journal','possibility-journal'}]
    data['resources']=extra+data['resources'];catalogue.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n','utf8')
    info.update({'website_version':'0.9','journal_titles':3,'journal_digital_editions':4,'reflection_journal_pages':48,'physical_journals_available':False,'journal_files':[MAIN,DARK,DAILY,POSS]})
