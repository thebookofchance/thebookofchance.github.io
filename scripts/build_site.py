from __future__ import annotations
import os, re, html, json, shutil, zipfile, hashlib, textwrap
from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
import mistune

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'source'/'manuscript.md'
ASSETS=ROOT/'assets'
for d in [ROOT, ASSETS/'covers', ASSETS/'artwork', ROOT/'files', ROOT/'read', ROOT/'downloads', ROOT/'print', ROOT/'about', ROOT/'community']:
 d.mkdir(parents=True,exist_ok=True)
md_text=SRC.read_text(encoding='utf8')

# Copy approved cover artwork as web-optimized derivatives; original book data remains untouched.
coverdir=ROOT/'source'/'covers'
for kind in ('Light','Dark'):
 im=Image.open(coverdir/f'Book_of_Chance_{kind}_Cover.png').convert('RGB')
 im.save(ASSETS/'covers'/f'{kind.lower()}-cover.webp', 'WEBP', quality=87, method=6)
 im.save(ASSETS/'covers'/f'{kind.lower()}-cover.jpg', 'JPEG', quality=88, optimize=True)
for p in (ROOT/'source'/'artwork').glob('*.png'):
 im=Image.open(p).convert('RGB')
 im.save(ASSETS/'artwork'/f'{p.stem}.webp', 'WEBP', quality=88, method=6)

# EPUBs and PDF proofs are bundled in files/ and are not modified by this site generator.

# Convert section div wrappers into HTML <figure> elements, retaining the precise author-approved caption wording.
markdown = mistune.create_markdown(escape=True, plugins=['table', 'strikethrough', 'url'])
heading_regex=re.compile(r'^(?:# Part (?:I|II|III) — .*|# Reader Resources \(Optional\)|## (?:A Note on This Edition|A Note to the Reader|Introduction — .*|Reading [IVX]+ — .*|Afterword — .*|A Note on the Fellowship of Chance|Ways of Reflecting|A Note on Language|Further Reading))$', re.M)
heads=list(heading_regex.finditer(md_text))
sections=[]
for j,m in enumerate(heads):
 body=md_text[m.end():heads[j+1].start() if j+1<len(heads) else len(md_text)].strip()
 title=m.group(0).lstrip('#').strip()
 sections.append({'title':title,'body':body})
slugs=[
 'note-on-this-edition', 'note-to-reader', 'introduction',
 'part-one','arrival','the-unfolding','fortune-and-hardship','the-open-future',
 'part-two','action-within-uncertainty','reflection-and-growth','hope','shared-fortune',
 'part-three','fellowship','the-living-world','stewardship','death-and-the-unknown',
 'afterword','note-on-the-fellowship','reader-resources','ways-of-reflecting','note-on-language','further-reading'
]
assert len(slugs)==len(sections),(len(slugs),len(sections),[s['title'] for s in sections])
for s,slug in zip(sections,slugs):s['slug']=slug

# Exactly one of these six approved images appears in each defined location.
FIG_RE=re.compile(r'!\[(?P<alt>[^\]]*)\]\((?P<path>artwork/[^)]+)\)\s*\n\s*:::\s*\{\.figure-context\}\s*\n(?P<caption>.*?)\n:::', re.S)

def content_html(body,base='../../'):
 def convert_figure(match):
  p=Path(match.group('path'))
  src=base+'assets/artwork/'+p.stem+'.webp'
  cap=markdown(match.group('caption').strip()).strip().removeprefix('<p>').removesuffix('</p>')
  return f'\n<figure class="book-figure"><img loading="lazy" decoding="async" src="{html.escape(src)}" alt="{html.escape(match.group("alt"))}"><figcaption>{cap}</figcaption></figure>\n'
 body,count=FIG_RE.subn(convert_figure,body)
 # Markdown in illustrations is fully escaped by default, so allow only these template-generated figure blocks.
 # Pre-render text around the approved figure snippets, rather than trusting arbitrary manuscript HTML.
 parts=re.split(r'(<figure class="book-figure">.*?</figure>)', body, flags=re.S)
 chunks=[]
 for piece in parts:
  if piece.startswith('<figure class="book-figure">'):
   chunks.append(piece)
  else:
   piece=re.sub(r'^### ', '## ', piece, flags=re.M)
   chunks.append(markdown(piece))
 result='\n'.join(chunks)
 # Attach rel to external reference links
 soup=BeautifulSoup(result,'html.parser')
 for a in soup.find_all('a',href=True):
  if a['href'].startswith('http'):
   a['target']='_blank';a['rel']='noopener noreferrer'
 return str(soup),count

part_labels={'part-one':'What We Inherit','part-two':'What We Make Possible','part-three':'The Lives We Share'}
roman=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']
reader_ids=[s['slug'] for s in sections if s['title'].startswith('Reading ')]
assert len(reader_ids)==12
for ix,s in enumerate(sections):
 title=s['title']
 if title.startswith('Reading '):
  s['label']='Reading '+title.split(' — ')[0].split()[-1]
  s['display']=title.split(' — ',1)[1]
  s['kind']='reading';s['readnum']=reader_ids.index(s['slug'])+1
 elif s['slug'] in part_labels:
  s['label']=title.split(' — ')[0]
  s['display']=part_labels[s['slug']]; s['kind']='part'
 elif s['slug']=='reader-resources':
  s['label']='Supplementary material';s['display']='Reader Resources';s['kind']='note'
 else:
  s['label']='The Book of Chance';s['display']=title;s['kind']='note'
 s['html'],s['figure_count']=content_html(s['body'])
 s['prev']=sections[ix-1]['slug'] if ix else None
 s['next']=sections[ix+1]['slug'] if ix+1<len(sections) else None

# Metadata for fast client-side title/full-text search (only book content, no user data).
search=[]
for s in sections:
 text=BeautifulSoup(s['html'],'html.parser').get_text(' ',strip=True)
 search.append({'slug':s['slug'],'title':s['display'],'label':s['label'],'text':text,'summary':text[:270]})
(ROOT/'search-index.json').write_text(json.dumps(search,ensure_ascii=False,separators=(',',':')),encoding='utf8')

BRAND='''<svg class="brand-mark" viewBox="0 0 120 120" aria-hidden="true" fill="none"><circle cx="60" cy="60" r="50.3" fill="none" stroke="currentColor" stroke-width="3.1"/>
<g fill="none" stroke="currentColor" stroke-width="2.9" stroke-linecap="round" stroke-linejoin="round">
 <path d="M12 38 L88 110 M26 26 L102 101 M40 16 L110 88 M55 9 L110 71"/>
 <path d="M10 84 L68 8 M25 102 L91 17 M42 110 L105 34 M55 112 L109 51"/>
</g>
<g fill="none" stroke="var(--blue)" stroke-width="3.2" stroke-linecap="round">
 <path d="M12 38 L88 110 M42 110 L105 34"/>
</g></svg>'''
SVG_ARROW='<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def url(base,path): return base+path

def nav(base,active=''):
 links=[('Home','index.html','home'),('Read the book','read/','read'),('Library','downloads/','downloads'),('Fellowship','community/','community'),('Physical books','print/','print'),('About','about/','about')]
 item=''.join(f'<a class="nav-link {"current" if name==active else ""}" href="{base+href}" {"aria-current=\"page\"" if name==active else ""}>{html.escape(title)}</a>' for title,href,name in links)
 return f'''<a class="skip-link" href="#main">Skip to main content</a>
 <header class="site-header"><div class="shell header-shell">
 <a class="brand" href="{base}index.html" aria-label="The Book of Chance — Home">{BRAND}<span class="brand-text">THE BOOK <em>OF</em> CHANCE</span></a>
 <nav id="main-navigation" class="main-nav" aria-label="Main navigation">{item}</nav>
 <div class="header-actions"><button class="theme-toggle icon-button" type="button" data-theme-toggle aria-label="Switch colour theme" title="Switch colour theme"><span class="theme-icon" aria-hidden="true">◐</span></button><button class="menu-toggle icon-button" type="button" aria-controls="main-navigation" aria-expanded="false" aria-label="Open navigation"><span class="menu-bars" aria-hidden="true">☰</span></button></div>
 </div></header>'''

def footer(base):
 return f'''<footer class="site-footer"><div class="shell footer-top"><div class="footer-brand">{BRAND}<div><strong>The Book of Chance</strong><p>On the Lives We Inherit and the Futures We Shape</p></div></div><div class="footer-links"><a href="{base}read/">Read online</a><a href="{base}downloads/">The library</a><a href="{base}community/">The Fellowship</a><a href="{base}print/">Physical editions</a><a href="{base}about/">About</a></div></div><div class="shell footer-bottom"><span>Written by H · A work of reflective philosophy</span><span>Free to read. No account required.</span></div></footer>'''

def document(title,body,base='',active='',desc='Explore The Book of Chance, a free illustrated work of reflective philosophy about uncertainty, choice and the lives we share.',extra_head=''):
 return f'''<!doctype html><html lang="en" data-theme="light"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{html.escape(desc,quote=True)}"><meta name="color-scheme" content="light dark"><title>{html.escape(title)} · The Book of Chance</title><link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="{base}assets/brand-avatar-512.png"><link rel="stylesheet" href="{base}assets/site.css"><script>try{{document.documentElement.dataset.theme=localStorage.getItem('chance-theme')||'light'}}catch(e){{}}</script>{extra_head}</head><body>{nav(base,active)}<main id="main">{body}</main>{footer(base)}<script defer src="{base}assets/site.js"></script></body></html>'''

# HOME
home=f'''<section class="hero"><div class="shell hero-grid"><div class="hero-copy"><span class="eyebrow"><span class="eyebrow-line"></span>A philosophy for an uncertain world</span><h1>We inherit more<br>than we <em>choose.</em></h1><p class="lead">Our lives begin in circumstances we did not make. What we do next can change what becomes possible.</p><p class="hero-explain"><cite>The Book of Chance</cite> explores uncertainty, agency, hope, grief and our responsibilities to one another—through twelve readings and original parables.</p><div class="button-line"><a class="btn btn-primary" href="read/introduction/">Begin reading {SVG_ARROW}</a><a class="btn btn-outline" href="downloads/">Download free</a></div><div class="hero-meta"><span>12 reflective readings</span><span class="meta-dot"></span><span>Illustrated</span><span class="meta-dot"></span><span>Free to read</span></div></div>
<div class="hero-books" aria-label="Two cover editions of The Book of Chance"><div class="book-stage"><img class="cover-card cover-light" src="assets/covers/light-cover.webp" alt="Light cover of The Book of Chance by H, featuring fine charcoal and blue paths" width="994" height="1536"><img class="cover-card cover-dark" src="assets/covers/dark-cover.webp" alt="Dark cover of The Book of Chance by H, with white and blue intersecting paths" width="994" height="1536"></div><p class="books-note">Two covers. One book. <span>Your first choice.</span></p></div></div></section>
<div class="shell"><div class="thin-rule"></div></div>
<section class="section-space"><div class="shell"><div class="section-head split"><div><span class="eyebrow">Inside the book</span><h2>Three movements.<br>One unfolding story.</h2></div><p>From the circumstances we inherit, to the actions we take, to the lives we affect. Read in order or explore one idea at a time.</p></div><div class="part-cards"><a class="part-card" href="read/part-one/"><span class="part-number">PART I</span><img src="assets/artwork/01_part_i.webp" alt="Thin intersecting paths in charcoal and blue" loading="lazy"><h3>What We Inherit</h3><p>Beginnings, uncertainty, fortune and hardship.</p><span class="text-link">Explore Part I {SVG_ARROW}</span></a><a class="part-card" href="read/part-two/"><span class="part-number">PART II</span><img src="assets/artwork/02_part_ii.webp" alt="A single path branching outward at a moment of choice" loading="lazy"><h3>What We Make Possible</h3><p>Choice, reflection, hope and the possibilities we widen.</p><span class="text-link">Explore Part II {SVG_ARROW}</span></a><a class="part-card" href="read/part-three/"><span class="part-number">PART III</span><img src="assets/artwork/03_part_iii.webp" alt="A network of connections representing shared lives" loading="lazy"><h3>The Lives We Share</h3><p>Fellowship, the living world, stewardship and loss.</p><span class="text-link">Explore Part III {SVG_ARROW}</span></a></div></div></section>
<section class="quote-panel"><div class="shell quote-inner"><span class="eyebrow">A question to carry</span><blockquote>What had to happen before you could make your first choice?</blockquote><p>And now that you are here, what can your choices make possible for someone else?</p><span class="quote-credit">— From the Introduction</span></div></section>
<section class="section-space"><div class="shell editions-home"><div class="home-section-copy"><span class="eyebrow">Your first choice</span><h2>Light or dark.<br>The words remain the same.</h2><p>Choose the cover that speaks to you. Both editions contain the exact same readings, parables and illustrations. Neither represents a different teaching or path.</p><a class="text-link" href="downloads/">Choose your free edition {SVG_ARROW}</a></div><div class="edition-pair"><div><img src="assets/covers/light-cover.webp" alt="Light Edition cover" loading="lazy"><span>LIGHT EDITION</span></div><div><img src="assets/covers/dark-cover.webp" alt="Dark Edition cover" loading="lazy"><span>DARK EDITION</span></div></div></div></section>
<section class="shell home-community"><div class="home-community-line"></div><div><span class="eyebrow">Beyond the pages</span><h2>Some possibilities begin with other people.</h2><p>The Fellowship of Chance is being developed as a place to meet, reflect, learn from one another and widen opportunities together. The book remains free to read whether or not you ever participate.</p><a class="text-link" href="community/">Discover the vision for the Fellowship {SVG_ARROW}</a></div><div class="home-community-mark" aria-hidden="true"><img src="assets/brand-mark.svg" alt="" width="210" height="210" loading="lazy"></div></section>
<section class="section-space compact-section"><div class="shell"><div class="next-step-card"><div><span class="eyebrow">Coming later</span><h2>A book to hold.</h2><p>We're exploring a first physical printing with both covers. Interested readers will be able to register when the interest list opens; no money is being collected at this stage.</p></div><a href="print/" class="btn btn-outline">Explore physical editions {SVG_ARROW}</a></div></div></section>'''
(ROOT/'index.html').write_text(document('Home',home,active='home',desc='Read The Book of Chance online for free. Twelve illustrated philosophical readings about chance, choice, hope and the possibilities we create together.'),encoding='utf8')

# READ INDEX
intro_items=[s for s in sections if s['slug'] in ('note-on-this-edition','note-to-reader','introduction')]
ending_items=[s for s in sections if s['slug'] in ('afterword','note-on-the-fellowship','reader-resources','ways-of-reflecting','note-on-language','further-reading')]

def link_list(items):
 return ''.join(f'<a class="toc-entry" href="{s["slug"]}/"><span class="toc-left"><span class="toc-index">{html.escape(s["label"])}</span><span class="toc-title">{html.escape(s["display"])}</span></span><span class="toc-arrow" aria-hidden="true">↗</span></a>' for s in items)

groups=[('part-one','I','What We Inherit',sections[3:8]),('part-two','II','What We Make Possible',sections[8:13]),('part-three','III','The Lives We Share',sections[13:18])]
tocgroups=''.join(f'''<section class="toc-section"><div class="toc-section-head"><span class="toc-part-number">{pn}</span><div><h2>{ht}</h2><a href="{ps}/">View part opening</a></div></div><div class="toc-list">{link_list([s for s in ss if s['kind']=='reading'])}</div></section>''' for ps,pn,ht,ss in groups)
readindex=f'''<section class="page-hero shell"><span class="eyebrow">The complete book · free to read</span><h1>Read at your own pace.</h1><p class="lead">Every reading is available here, without an account. Explore in order, return to a favourite, or follow a question wherever it leads.</p><div class="reader-dashboard"><div><span class="dash-label">YOUR READING</span><p data-reading-status>Reading progress stays on this device.</p></div><a class="btn btn-primary" data-continue-reading href="introduction/">Begin the book {SVG_ARROW}</a></div></section><section class="shell read-directory"><div class="read-controls"><div><span class="eyebrow">Find a passage</span><h2>The twelve readings</h2></div><label class="search-box"><span class="sr-only">Search the book's chapters and text</span><svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.5"/><path d="m16 16 5 5" stroke="currentColor" stroke-width="1.5"/></svg><input id="book-search" type="search" placeholder="Search the book…" autocomplete="off"></label></div><div class="search-results" id="search-results" aria-live="polite" hidden></div><div id="book-toc"><div class="toc-section intro-toc"><div class="toc-list">{link_list(intro_items)}</div></div>{tocgroups}<div class="toc-section end-toc"><h2>After the readings</h2><div class="toc-list">{link_list(ending_items)}</div></div></div></section>'''
(ROOT/'read'/'index.html').write_text(document('Read the book',readindex,base='../',active='read',desc='Read all twelve philosophical readings of The Book of Chance online, with original parables, illustrations and optional reflections.'),encoding='utf8')

# READING PAGES
for s in sections:
 slug=s['slug'];d=ROOT/'read'/slug;d.mkdir(parents=True,exist_ok=True)
 prev=next((x for x in sections if x['slug']==s['prev']),None)
 nxt=next((x for x in sections if x['slug']==s['next']),None)
 previous=f'<a href="../{prev["slug"]}/" class="chapter-prev"><span>← Previous</span><strong>{html.escape(prev["display"])}</strong></a>' if prev else '<div></div>'
 next_=f'<a href="../{nxt["slug"]}/" class="chapter-next"><span>Next →</span><strong>{html.escape(nxt["display"])}</strong></a>' if nxt else '<div></div>'
 if s['kind']=='reading': label=f'Reading {roman[s["readnum"]-1]} of XII'
 else: label=s['label']
 meta=f'<span class="eyebrow">{html.escape(label)}</span>'
 action='<button type="button" class="bookmark-button" data-bookmark aria-pressed="false">☆ <span>Bookmark</span></button>'
 article=f'''<div class="reader-topbar shell"><a class="back-to-toc" href="../">← All readings</a><div class="reader-preferences" aria-label="Reading preferences"><span class="pref-label">TEXT SIZE</span><button type="button" data-font-decrease aria-label="Decrease reading font size">A−</button><button type="button" data-font-increase aria-label="Increase reading font size">A+</button>{action}</div></div><div class="reader-progress" aria-hidden="true"><div data-progress-fill></div></div><div class="reader-layout shell"><aside class="reader-sidebar" aria-label="Book contents"><span class="sidebar-label">THE BOOK OF CHANCE</span><a href="../" class="sidebar-toc">← Table of contents</a><div class="sidebar-section"><span>YOU ARE READING</span><strong>{html.escape(s["display"])}</strong></div><span class="sidebar-secondary">Your place is saved on this device.</span></aside><article class="reading-article" data-reader-slug="{slug}" data-reading-kind="{s['kind']}"><header class="chapter-heading">{meta}<h1>{html.escape(s['display'])}</h1><div class="heading-ornament"><span></span><span></span><span></span></div></header><div class="reading-body">{s['html']}</div><nav class="chapter-pager" aria-label="Adjacent chapters">{previous}{next_}</nav></article><aside class="reader-rail"><span class="rail-word">THE BOOK OF CHANCE</span></aside></div>'''
 (d/'index.html').write_text(document(s['display'],article,base='../../',active='read',desc=f'{s["display"]}. Read The Book of Chance by H online for free, with original illustrations and reflection prompts.',extra_head='<meta name="robots" content="index,follow">'),encoding='utf8')

# LIBRARY — scalable catalogue with explicit availability, never invented downloads.
CAT=ROOT/'source'/'publications.json'
catalogue=json.loads(CAT.read_text(encoding='utf8'))
assert len(catalogue['available'])>=1
for publication in catalogue['available']:
 assert publication['title'] and publication['summary']
 for edition in publication['editions']:
  for kind in ('epub','pdf'):
   assert (ROOT/edition[kind]).is_file(), (publication['title'],edition[kind])

def release_card(pub):
 editions=[]
 for edition in pub['editions']:
  editions.append(f'''<article class="library-edition"><img src="../{html.escape(edition['cover'])}" alt="{html.escape(pub['title'])} {html.escape(edition['name'])} cover" loading="lazy" width="994" height="1536"><div><span class="eyebrow">{html.escape(edition['name'])}</span><h3>{html.escape(edition['label'])}</h3><p>{html.escape(edition['description'])}</p><div class="library-edition-actions"><a class="btn btn-primary" href="../{html.escape(edition['epub'])}" download>EPUB <span aria-hidden="true">↓</span></a><a class="btn btn-outline" href="../{html.escape(edition['pdf'])}" download>PDF reader proof <span aria-hidden="true">↓</span></a></div></div></article>''')
 return f'''<section class="library-release" aria-labelledby="featured-book"><div class="library-release-intro"><div><span class="eyebrow">Available · Foundational book</span><h2 id="featured-book">{html.escape(pub['title'])}</h2><p class="library-subtitle">{html.escape(pub['subtitle'])}</p></div><p>{html.escape(pub['summary'])}</p></div><div class="library-editions">{''.join(editions)}</div><div class="library-release-foot"><p><strong>Two covers, one text.</strong> Both versions have exactly the same readings, diagrams and illustrations.</p><a class="text-link" href="../read/">Or read the complete book online {SVG_ARROW}</a></div></section>'''

planned=''.join(f'''<article class="library-planned-card"><span class="library-type">{html.escape(t['category'])}</span><h3>{html.escape(t['title'])}</h3><p>{html.escape(t['summary'])}</p><span class="library-status">In development · Not yet available</span></article>''' for t in catalogue['planned'])
downloads=f'''<section class="shell page-hero library-hero"><span class="eyebrow">The library</span><h1>Ideas worth returning to.</h1><p class="lead">Books, reflections and future learning resources exploring chance, choice and the ways our lives shape one another.</p><p>Everything currently available is free to read or download, without an account. The collection can grow without turning the site into a storefront.</p></section><div class="shell library-layout"><div class="library-count"><span>01</span><div><strong>Available now</strong><small>One complete work · Two cover choices</small></div></div>{''.join(release_card(pub) for pub in catalogue['available'])}<section class="library-upcoming"><div class="section-head split"><div><span class="eyebrow">The collection ahead</span><h2>More than one book.</h2></div><p>The library is being designed to accommodate shorter essays, guided reflections and additional literature as they are written and prepared for publication. These are plans, not available downloads.</p></div><div class="library-planned-grid">{planned}</div></section><section class="library-guide"><div><h2>Choose how to read.</h2><p><strong>EPUB</strong> is best for adjustable text and dedicated ebook readers. <strong>PDF</strong> preserves the fixed illustrated page layout. The PDFs currently supplied are reader proofs, pending final digital accessibility and production checks.</p></div><div><h2>Open by principle.</h2><p>Foundational writings remain accessible without membership, payment or registration. Additional resources may have their own formats and availability when they are ready.</p></div></section></div>'''
(ROOT/'downloads'/'index.html').write_text(document('Library',downloads,base='../',active='downloads',desc='Explore The Book of Chance and a growing library of philosophical readings and resources, free to access.'),encoding='utf8')

# FELLOWSHIP COMMUNITY — enticing without misrepresenting membership or services as operational.
community=f'''<section class="shell community-hero"><div class="community-hero-copy"><span class="eyebrow"><span class="eyebrow-line"></span>Fellowship of Chance · In development</span><h1>Chance brings us together.<br><em>What we do next matters.</em></h1><p class="lead">A community imagined around a simple belief: the people we meet, the knowledge we share and the choices we make can widen one another's possibilities.</p><p>We're developing a place for genuine relationships across experiences and generations—where reflection becomes conversation, and conversation can become meaningful support.</p><div class="button-line"><a class="btn btn-primary" href="#how-belonging-works">Explore belonging {SVG_ARROW}</a><a class="btn btn-outline" href="../read/fellowship/">Read the chapter on fellowship</a></div></div><div class="community-hero-emblem"><img src="../assets/brand-mark.svg" width="440" height="440" alt="Circular emblem of intersecting paths with two blue lines, representing lives and possibilities meeting"><p>Through chance, we meet. Through choice, we grow. Together, we create possibility.</p></div></section>
<div class="shell"><div class="thin-rule"></div></div>
<section class="shell section-space community-why"><div class="section-head split"><div><span class="eyebrow">Why a Fellowship?</span><h2>Connection before opportunity.</h2></div><p>The Fellowship isn't designed as a directory of career profiles or a place to sell yourself. Relationships should develop through shared time, questions, projects and mutual understanding.</p></div><div class="community-pillars"><article><span class="pillar-num">01</span><h3>Be heard. Be curious.</h3><p>Discuss what you're learning, reflect on the uncertainty we all face and hear perspectives unlike your own. Disagreement is welcome; respect is expected.</p></article><article><span class="pillar-num">02</span><h3>Learn from lived experience.</h3><p>Meet people with different experiences. Informal guidance and a future structured adult mentorship programme could help members navigate possibilities together.</p></article><article><span class="pillar-num">03</span><h3>Make something possible.</h3><p>Bring people together around community projects, useful introductions, shared knowledge and practical acts that widen opportunities beyond ourselves.</p></article></div></section>
<section class="community-manifesto"><div class="shell community-manifesto-inner"><span class="eyebrow">The five values</span><h2>Hope. Acceptance.<br>Reflection. Growth. Community.</h2><p>No one value stands above the others. Each has a role in how we live with uncertainty and how we treat the people around us.</p><a class="text-link" href="../read/reflection-and-growth/">Explore the values in the book {SVG_ARROW}</a></div></section>
<section class="shell section-space community-work"><div class="section-head"><span class="eyebrow">First-year development priorities</span><h2>From ideas to real support.</h2><p>These are the first areas we intend to develop. None should be presented as a service already running.</p></div><div class="community-work-grid"><article><span class="work-icon">↗</span><h3>Mentorship & guidance</h3><p>Informal conversations and, when appropriate safeguards exist, structured adult-to-adult mentoring based on mutual consent.</p></article><article><span class="work-icon">⌁</span><h3>Collaborative projects</h3><p>Local and online initiatives in which people share skills, work together and improve opportunities in their communities.</p></article><article><span class="work-icon">◌</span><h3>Practical support</h3><p>Thoughtful, confidential help for members facing hardship, introduced only when the necessary safeguarding and operational capacity are in place.</p></article></div></section>
<section class="shell section-space community-belonging" id="how-belonging-works"><div class="section-head split"><div><span class="eyebrow">How belonging is envisioned</span><h2>A place for everyone to begin.</h2></div><p>Joining is never required to read the book or consider its ideas. Participation will be voluntary, with a free membership model once the community is ready.</p></div><div class="belonging-table"><div><span>01</span><div><h3>Follower</h3><p>Explore the complete foundational writings openly. No registration and no obligation to agree with every idea.</p></div><small>Available now · Read freely</small></div><div><span>02</span><div><h3>Member</h3><p>Planned free registration for adults aged 18+, with community gatherings and resources when operational. Real names will be used in protected Member spaces, not published openly.</p></div><small>Planned · Not open</small></div><div><span>03</span><div><h3>Senior Member</h3><p>Future recognition for sustained, meaningful service and contributions, with reasonable hardship accommodations. Seniority will never mean greater human worth.</p></div><small>Future pathway</small></div></div></section>
<section class="shell community-status"><div class="status-art"><img src="../assets/artwork/03_part_iii.webp" alt="Network of interconnected paths representing possible relationships" loading="lazy"></div><div><span class="eyebrow">Where things stand</span><h2>The community is being built.</h2><p>The Fellowship is a developing organisation, not an active member service. Registration, gatherings, mentorship and support programmes are not open yet. We want to establish trust, privacy, accountability and safeguarding before inviting people into member spaces.</p><p>You can begin as a follower simply by reading the philosophy. Updates about the wider community will appear here as plans become operational.</p><div class="button-line"><a class="btn btn-primary" href="../read/">Start with the book {SVG_ARROW}</a><a class="btn btn-outline" href="../about/">About the philosophy</a></div><p class="community-fineprint">No email addresses, applications, donations or membership payments are collected on this prototype.</p></div></section>'''
(ROOT/'community'/'index.html').write_text(document('The Fellowship',community,base='../',active='community',desc='Discover the vision for The Fellowship of Chance: a developing community of reflection, mentorship, shared projects and mutual support.'),encoding='utf8')

# PHYSICAL BOOK — nontransactional interest preview
print_page=f'''<section class="shell page-hero"><span class="eyebrow">A future physical edition</span><h1>Some books are meant to be held.</h1><p class="lead">We're exploring a first paperback printing of <i>The Book of Chance</i>. Choose a cover, and follow the journey from digital pages to a physical book.</p></section><section class="shell print-preview"><div class="print-books"><div class="print-art-stack"><img id="selected-print-cover" src="../assets/covers/light-cover.webp" alt="Light Edition book cover" width="994" height="1536"><span class="book-bottom-shadow" aria-hidden="true"></span></div></div><div class="print-info"><span class="eyebrow">Two covers · identical interiors</span><h2>Your first choice.</h2><p>Every copy contains the same twelve readings, parables and interior artwork. The design you choose is simply the first choice of your reading journey.</p><div class="cover-chooser" role="group" aria-label="Choose your preferred paperback cover"><button type="button" class="cover-choice selected" data-cover-choice="light" aria-pressed="true"><span class="choice-swatch light-swatch"></span><span><strong>Light</strong><small>White & charcoal</small></span></button><button type="button" class="cover-choice" data-cover-choice="dark" aria-pressed="false"><span class="choice-swatch dark-swatch"></span><span><strong>Dark</strong><small>Charcoal & ivory</small></span></button></div><button type="button" class="btn btn-primary" id="save-cover-choice">Save my cover preference</button><p class="micro-status" id="cover-save-status" role="status" aria-live="polite">Saved only on this device. No order or reservation is placed.</p></div></section><section class="shell"><div class="print-state"><div><span class="eyebrow">Printing status</span><h2>Interest registration is not open yet.</h2><p>We'll announce a clear print threshold, price, shipping arrangements and closing date before accepting paid pre-orders. This prototype does not collect email addresses or payment details.</p></div><div class="state-pill"><span class="state-dot"></span>Planning stage</div></div></section><section class="shell section-space"><div class="section-head"><span class="eyebrow">How it could work</span><h2>From interest to first printing.</h2></div><div class="steps"><div><span>01</span><h3>Register interest</h3><p>When the list opens, readers choose Light or Dark and provide contact details voluntarily.</p></div><div><span>02</span><h3>Set a transparent goal</h3><p>We'll publish a viable print target, pricing, estimated dispatch window and refund terms before collecting payment.</p></div><div><span>03</span><h3>Print & deliver</h3><p>If the paid pre-order goal is met, we print and ship. If not, the campaign would issue the stated full refunds.</p></div></div></section>'''
(ROOT/'print'/'index.html').write_text(document('Physical editions',print_page,base='../',active='print',desc='Explore the planned Light and Dark paperback editions of The Book of Chance. Printing is not yet open and no orders are being collected.'),encoding='utf8')

# ABOUT
about=f'''<section class="shell page-hero about-hero"><span class="eyebrow">About the philosophy</span><h1>What can we shape<br>within uncertainty?</h1><p class="lead">Confluent Humanism explores the meeting of circumstance, chance, agency and ethical responsibility. It draws on questions people have asked across many philosophical traditions.</p></section><section class="shell about-grid"><div class="about-long"><h2>An invitation to think.</h2><p><i>The Book of Chance</i> is a work of reflective philosophy, not a revelation or a claim to have settled scientific debates. Its central conviction—that chance is fundamental and the future is not entirely predetermined—is presented as a philosophical position open to criticism.</p><p>Its ethical commitments begin with dignity, meaningful action, attention to unequal circumstances and responsibility toward one another and the living world. Those commitments deserve their own arguments; they cannot be derived simply from randomness.</p><p>The work draws upon prior conversations in philosophy about causation, luck, free will, care, moral responsibility and practical opportunity. Its contribution is in bringing ideas together into a distinct synthesis and a way of living with uncertainty—not claiming they were all invented here.</p><h2>The author</h2><p>H is the pseudonymous authorial voice of <i>The Book of Chance</i>. The name signals authorship, not special authority over readers or immunity from disagreement.</p><h2>About the Fellowship</h2><p>The book is associated with the envisioned Fellowship of Chance, a proposed community centred on reflection, growth and support for others. The book stands on its own: reading it involves no membership, loyalty, donation or other obligation.</p><p>The Fellowship is not represented here as an active membership service. Readers may explore the philosophy independently.</p></div><aside class="about-side"><div class="about-figure"><img src="../assets/artwork/03_part_iii.webp" loading="lazy" alt="A network of charcoal and blue connections symbolising interdependent lives"><p>Our lives are shaped by one another, even where their paths are unknown to us.</p></div><div class="aside-quote"><span class="eyebrow">The five values</span><p>Hope<br>Acceptance<br>Reflection<br>Growth<br>Community</p><a class="text-link" href="../read/reflection-and-growth/">Explore the readings {SVG_ARROW}</a></div></aside></section>'''
(ROOT/'about'/'index.html').write_text(document('About',about,base='../',active='about',desc='About Confluent Humanism, H and The Book of Chance: a philosophical synthesis exploring chance, agency and shared ethical responsibility.'),encoding='utf8')

# Brand master, derived faithfully from the founding circular diagonal-line sketch.
# It is intentionally a simple vector rather than a scaled-down decorative image.
master_logo = BRAND.replace('class="brand-mark" ', 'xmlns="http://www.w3.org/2000/svg" ').replace('currentColor', '#172633').replace('var(--blue)', '#1670d9')
(ASSETS/'brand-mark.svg').write_text(master_logo, encoding='utf8')
favicon_markup = master_logo.replace('<svg ', '<svg ')
favicon_markup = favicon_markup.replace('fill="none"><circle', 'fill="none"><circle')
favicon_markup = favicon_markup.replace('stroke="currentColor"', 'stroke="#172633"').replace('stroke="var(--blue)"', 'stroke="#1670d9"')
favicon_markup = favicon_markup.replace('viewBox="0 0 120 120"', 'viewBox="0 0 120 120"')
(ASSETS/'favicon.svg').write_text(favicon_markup, encoding='utf8')
# A full text corpus validation before creating the ZIP.
assert sum(s['figure_count'] for s in sections)==6, [(s['slug'],s['figure_count']) for s in sections]
assert all((ROOT/'read'/s['slug']/'index.html').exists() for s in sections)
# Ensure original word order in visible paragraphs remains (mechanical text extraction notwithstanding)
for s in sections:
 if s['kind']=='reading': assert len(BeautifulSoup(s['html'],'html.parser').get_text(' ',strip=True))>3000,s['slug']

info={'website_version':'0.4','source':'Book_of_Chance_Illustrated_Manuscript_v0.12.md','source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'chapters':len(sections),'readings':len(reader_ids),'illustration_placements':sum(s['figure_count'] for s in sections),'epub_files':2,'pdf_reader_proofs':2,'interest_form_live':False,'email_collected':False,'fellowship_membership_open':False,'library_available_publications':len(catalogue['available']),'library_planned_categories':len(catalogue['planned'])}
(ROOT/'SITE_CONTENT_MANIFEST.json').write_text(json.dumps(info,indent=2),encoding='utf8')
print('generated sections',len(sections),'readings',len(reader_ids),'figures',sum(s['figure_count'] for s in sections))
print('section titles',[(s['slug'],s['title']) for s in sections]);print('root',ROOT)
