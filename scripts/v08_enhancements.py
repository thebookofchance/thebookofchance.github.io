"""v0.8 usability and reflection PDF release. Runs after v07 enhancements."""
from pathlib import Path
import json,re
from bs4 import BeautifulSoup

JOURNAL='files/reflection/The_Reflection_Journal_Fillable.pdf'
SHEETS={
    'chance':('The Reflection of Chance','files/reflection/The_Reflection_of_Chance_Fillable.pdf','A short daily or situational practice','01 · DAILY'),
    'action':('The Act of Possibility','files/reflection/The_Act_of_Possibility_Fillable.pdf','Consider one voluntary, respectful act','02 · ACTION'),
    'week':('A Week of Possibilities','files/reflection/A_Week_of_Possibilities_Fillable.pdf','A thoughtful look across your week','03 · WEEKLY')
}


def once(s,old,new,what):
    n=s.count(old)
    if n!=1:raise AssertionError(f'{what}: expected 1 match, found {n}')
    return s.replace(old,new,1)

def within(s,begin,end,replacement,what):
    i=s.find(begin)
    if i<0:raise AssertionError(f'Missing {what} start')
    j=s.find(end,i+len(begin))
    if j<0:raise AssertionError(f'Missing {what} end')
    return s[:i]+replacement+s[j:]

def edit(root,rel,fn):
    p=root/rel
    raw=p.read_text('utf8')
    revised=fn(raw)
    assert revised!=raw,rel
    p.write_text(revised,'utf8')


def reflect_edit(s):
    shortcuts='''<nav class="shell section-shortcuts" aria-label="On this page"><span>On this page</span><a href="#choose-a-practice">Choose a practice</a><a href="#reflection-workspace">Write online</a><a href="#reflection-journal">The journal</a><a href="#reflection-guides">PDF worksheets</a></nav>'''
    s=once(s,'<section class="shell weekly-practice"',shortcuts+'<section class="shell weekly-practice"','reflect shortcuts')
    s=once(s,'<section class="shell section-space reflect-intro">','<section class="shell section-space reflect-intro" id="choose-a-practice">','reflect anchors')
    cards='''<div class="reflection-options" role="group" aria-label="Choose one reflection practice">'''
    symbols = {
        'chance':'<circle cx="30" cy="30" r="22" stroke="currentColor" stroke-width="1.4"/><path d="M6 35 44 8M14 53 54 20M8 18l37 36" stroke="#286cb8" stroke-width="1.6"/>',
        'action':'<circle cx="16" cy="43" r="5" stroke="currentColor" stroke-width="1.5"/><circle cx="44" cy="15" r="5" stroke="currentColor" stroke-width="1.5"/><circle cx="47" cy="46" r="5" stroke="currentColor" stroke-width="1.5"/><path d="M20 39 40 19M24 42h18" stroke="#286cb8" stroke-width="1.6"/>',
        'week':'<circle cx="30" cy="30" r="23" stroke="currentColor" stroke-width="1.4"/><circle cx="30" cy="30" r="13" stroke="#286cb8" stroke-width="1.5"/><path d="M30 6v13M30 41v13M6 30h13M41 30h13" stroke="currentColor" stroke-width="1.3"/>'
    }
    for k,(title,href,subtitle,index) in SHEETS.items():
        if k=='chance':text='Notice circumstance, choice, learning and what might become possible.'
        elif k=='action':text='Explore an appropriate way to help someone, with consent and within your means.'
        else:text='Look back at the unexpected, the choices you made and what to carry forward.'
        cards+=f'''<button class="practice-card" type="button" data-pick-template="{k}" aria-label="Use {title} in the private writing workspace"><span class="practice-index">{index}</span><span class="practice-card-symbol" aria-hidden="true"><svg viewBox="0 0 60 60" fill="none">{symbols[k]}</svg></span><strong>{title}</strong><span class="practice-card-description">{text}</span><span class="practice-card-cta">Start this practice <span aria-hidden="true">↗</span></span></button>'''
    # The untouched end marker closes the grid.
    s=within(s,'<div class="reflection-options">','</div></section>',cards,'reflection practice tiles')
    s=once(s,'<button type="button" class="btn btn-primary" id="reflection-download">Download my reflection (.txt)</button><button type="button" class="btn btn-outline" id="reflection-print">Print or save as PDF</button>','<button type="button" class="btn btn-primary" id="reflection-print">Save / print as PDF</button><a class="btn btn-outline" id="reflection-blank-pdf" href="../'+SHEETS['chance'][1]+'" download>Download blank fillable PDF</a>','reflection editor actions')
    s=once(s,'Nothing is automatically saved. Download a copy before closing the page if you want to keep it.','Nothing is automatically saved. Use <strong>Save / print as PDF</strong> to keep your typed responses, or download a blank fillable worksheet to write in a PDF reader.','privacy use copy')
    s=once(s,'<section class="shell section-space" id="reflection-guides">','<section class="shell section-space" id="reflection-guides">','guide anchor exists') if False else s
    journal='''<section class="journal-feature" id="reflection-journal"><div class="shell journal-feature-inner"><div class="journal-cover" aria-label="The Reflection Journal cover"><span>THE BOOK OF CHANCE</span><div class="journal-cover-mark" aria-hidden="true"><svg viewBox="0 0 190 190" fill="none"><circle cx="95" cy="95" r="72" stroke="#286cb8" stroke-width="1.4"/><path d="M10 133 127 16M32 154 150 36M54 176 175 55M19 61 130 172" stroke="#26313b" stroke-width="1.5"/></svg></div><h3>The Reflection<br>Journal</h3><small>BY H · A BOOK OF CHANCE COMPANION</small></div><div class="journal-copy"><span class="eyebrow">New · Free fillable journal</span><h2>One place for the questions you return to.</h2><p>A complete 28-page companion bringing together all three reflection practices. Designed with the same editorial language as the book, and arranged as a repeatable journal rather than disconnected templates.</p><ul><li>Three organised sections: daily, action and weekly.</li><li>Editable text boxes in compatible PDF readers.</li><li>6 × 9-inch interior layout suitable for future print development.</li></ul><div class="button-line"><a class="btn btn-primary" href="../files/reflection/The_Reflection_Journal_Fillable.pdf" download>Download the free journal · PDF ↓</a><a class="btn btn-outline" href="#reflection-guides">Individual worksheets</a></div><p class="journal-note">The PDF can be filled and saved locally. Some browser PDF viewers have limited support for saving form fields; a desktop PDF reader is recommended. A future printed edition would require production proofing and is not available for purchase.</p></div></div></section>'''
    s=once(s,'<section class="shell section-space" id="reflection-guides">',journal+'<section class="shell section-space" id="reflection-guides">','reflect journal insert')
    s=once(s,'Three ready-to-use text templates can be printed, edited or kept privately. They require no login, account, application or internet connection after downloading.','Download individual themed PDF worksheets. Each contains editable answer fields for compatible PDF readers and can also be printed and completed by hand. No registration required.','reflect guide copy')
    dl='''<div class="practice-downloads">'''
    for k,(name,href,desc,index) in SHEETS.items():
        dl+=f'<a class="pdf-download-card" href="../{href}" download><span>{index} · FILLABLE PDF</span><strong>{name}</strong><em>{desc}</em><small>Download PDF worksheet <b aria-hidden="true">↓</b></small></a>'
    # The untouched end marker closes the grid.
    s=within(s,'<div class="practice-downloads">','</div><div class="prompt-archive">',dl,'reflect PDF downloads')
    # The search-and-replace above preserves the closing marker; it must still exist exactly once.
    s=once(s,'<script defer src="../assets/reflect.js?v=0.7"></script>','<script defer src="../assets/reflect.js?v=0.8"></script>','reflection js cache')
    return s


def library_edit(s):
    quick='''<nav class="shell section-shortcuts" aria-label="Browse the library"><span>Browse</span><a href="#featured-book">The book</a><a href="#reflection-journal">Reflection Journal</a><a href="#practice-guides">Worksheets</a><a href="../reflect/">Write online</a></nav>'''
    s=once(s,'<div class="shell library-layout">',quick+'<div class="shell library-layout">','library shortcut nav')
    journal='''<section class="library-journal" id="reflection-journal"><div class="library-journal-copy"><span class="eyebrow">Available now · Companion publication</span><h2>The Reflection Journal</h2><p>A 28-page fillable PDF companion to <cite>The Book of Chance</cite>. Three practices organised into a repeatable journal, with room to write and return to your reflections.</p><p><strong>Free digital edition.</strong> Open in a compatible PDF reader, enter your answers and save your own copy. The 6 × 9-inch interior is also a starting point for a possible future printed journal.</p><div class="button-line"><a class="btn btn-primary" href="../files/reflection/The_Reflection_Journal_Fillable.pdf" download>Download journal · PDF ↓</a><a class="btn btn-outline" href="../reflect/">Explore the practices</a></div><small>Not a printed book offer. Print design and binding must be validated before any physical edition.</small></div><div class="library-journal-art" aria-hidden="true"><div class="mini-journal"><span>THE BOOK OF CHANCE</span><strong>The<br>Reflection<br>Journal</strong><svg viewBox="0 0 160 120" fill="none"><circle cx="81" cy="58" r="49" stroke="#286cb8"/><path d="M23 106 104 13M46 115 123 30M57 10 141 96" stroke="#26313b"/></svg><i>H</i></div></div></section>'''
    s=once(s,'<section class="shell library-resources" id="practice-guides">',journal+'<section class="shell library-resources" id="practice-guides">','library journal insert')
    s=once(s,'Three concise guides translate the book\'s questions into small private practices. No account, payment or commitment is needed.','Individual fillable PDF sheets for a single reflection. Edit them in a PDF reader or print them to complete by hand; all are free.','library worksheet description')
    cards='''<div class="library-resource-grid">'''
    for k,(name,href,desc,index) in SHEETS.items():
        cards+=f'<a class="library-resource-card" href="../{href}" download><span>{index} / FILLABLE PDF</span><h3>{name}</h3><p>{desc}. Editable fields and a print-friendly layout.</p><strong class="resource-card-cta">Download PDF worksheet <span aria-hidden="true">↗</span></strong></a>'
    # The untouched end marker closes the grid.
    s=within(s,'<div class="library-resource-grid">','</div><div class="library-tool-link">',cards,'library worksheets')
    return s


def home_edit(s):
    addon='''<a class="home-practice-card" href="downloads/#reflection-journal"><span class="card-overline">NEW · FREE PDF JOURNAL</span><h3>Keep your reflections.</h3><p>Download a thoughtfully designed, fillable 28-page journal with three repeatable practices.</p><span class="text-link">Explore the Reflection Journal ↗</span></a>'''
    return once(s,'</div></section><section class="shell home-community">',addon+'</div></section><section class="shell home-community">','home journal feature')


def privacy_edit(s):
    return once(s,'You can choose to download or print your own writing.','You can print or save the online reflection as a PDF using your browser. Separately, the downloadable fillable PDF worksheets and journal are files that you edit and save on your own device.','privacy pdf clarification')


def apply_v08(root:Path,manifest:dict):
    # Dependency-free static experience. Formspree config and logo remain unmodified.
    edit(root,'reflect/index.html',reflect_edit)
    edit(root,'downloads/index.html',library_edit)
    edit(root,'index.html',home_edit)
    edit(root,'privacy/index.html',privacy_edit)
    manifest.update({'website_version':'0.8','reflection_journal_pages':28,'fillable_pdf_resources':4,
      'website_reflection_export':'browser print/save as PDF','paperback_sales_active':False})
    catalog=root/'source/publications.json'
    data=json.loads(catalog.read_text('utf8'))
    data['resources']=[{'id':k,'title':title,'kind':'Fillable PDF worksheet','file':href} for k,(title,href,_,_) in SHEETS.items()]
    data['resources'].insert(0,{'id':'reflection-journal','title':'The Reflection Journal','kind':'Free fillable journal PDF','file':JOURNAL})
    catalog.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf8')
