"""Source-driven integration of Letters from H No. 03 into the static site.

Must run after v010_publications and v012_second_letter. Does not mutate previous
letter source or PDF/EPUB assets. Re-running build_site is safe.
"""
from pathlib import Path
import json,html
from bs4 import BeautifulSoup
from build_letter_003 import build_letter_003


def apply_v013(root:Path, document, markdown, info:dict):
    cat=json.loads((root/'source/letters/catalogue.json').read_text('utf8'))
    assert [p['number'] for p in cat['available']]==[1,2,3]
    item=cat['available'][2]
    if not all((root/item[k]).is_file() for k in ('pdf','epub','cover')):
        build_letter_003()

    label=html.escape(item['title'])
    lead=html.escape(item['lead'])
    summary=html.escape(item['summary'])
    rendered=BeautifulSoup(markdown((root/item['file']).read_text('utf8')),'html.parser')
    if rendered.h1:rendered.h1.decompose()
    first=rendered.find('p')
    if first and 'Letters from H · No. 03' in first.get_text(' ',strip=True): first.decompose()
    for a in rendered.find_all('a',href=True):
        if a['href'].startswith('https://'):
            a['target']='_blank'
            a['rel']='noopener noreferrer'

    body=f'''<div class="shell letters-reading-top"><a class="back-to-toc" href="../">← All Letters from H</a><a class="back-to-toc" href="../../downloads/#letters-from-h">The Library</a></div>
    <header class="shell letters-reading-hero"><span class="eyebrow">Letters from H · No. 03</span><h1>{label}</h1><p class="lead">{lead}</p><p class="letters-meta">By H · Prepared 22 November 2026 · Editorial candidate {html.escape(item['edition'])}</p></header>
    <div class="shell letters-reading-layout"><article class="reading-body letters-prose" aria-label="Full text of Letter 03">{rendered}</article><aside class="letters-side"><span class="eyebrow">This letter</span><p>The third standalone Letter examines fairness, particular commitments and the reasonable limits of helping people we do not know. Free to read without membership or donation.</p><img src="../../{item['cover']}" alt="Cover of Letter 03, with fine charcoal and blue paths crossing and continuing independently" width="1000" height="1500" loading="lazy"><a class="btn btn-primary" href="../../{item['pdf']}" download>Download PDF ↓</a><a class="btn btn-outline" href="../../{item['epub']}" download>Download EPUB ↓</a><a class="text-link" href="../when-good-choices-lead-to-bad-outcomes/">← Previous: When Good Choices Lead to Bad Outcomes</a><a class="text-link" href="../../read/shared-fortune/">Related: Shared Fortune ↗</a></aside></div>
    <section class="shell letters-postscript"><div><span class="eyebrow">The opening collection</span><h2>Three questions. More ways to think.</h2><p>These first three Letters explore unseen interdependence, decisions under uncertainty, and our obligations to strangers. They remain independent essays rather than compulsory teachings.</p></div><a class="btn btn-outline" href="../">Read the collection →</a></section>'''
    dst=root/item['url']/'index.html'
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_text(document(item['title'],body,base='../../',active='downloads',desc=item['summary'],extra_head=f'<link rel="canonical" href="https://thebookofchance.github.io/{item["url"]}">'),encoding='utf8')

    archive=root/'letters/index.html'
    arch=BeautifulSoup(archive.read_text('utf8'),'html.parser')
    features=arch.select('.letters-index-feature')
    assert len(features)==3, 'Expected three distinct series cards'
    foot=arch.select_one('.letters-series-foot')
    assert foot
    foot.select_one('p').string='The first three Letters are prepared as editorial candidates. The next planned publication is The Five Values, an introductory illustrated booklet. Further Letters may follow occasionally; no fixed schedule is promised.'
    archive.write_text(str(arch),encoding='utf8')

    library=root/'downloads/index.html'
    soup=BeautifulSoup(library.read_text('utf8'),'html.parser')
    section=soup.select_one('.letters-feature-library')
    assert section
    section.select_one('.letters-library-head .eyebrow').string='The opening collection · Letters from H'
    section.select_one('.letters-library-head p').string='Three complete, free-to-read philosophical essays. Explore unseen connections, responsible choices and the limits of our duties to strangers.'
    older=section.select_one('.letters-previous-link')
    if older:older.decompose()
    prev=cat['available'][1]
    prev0=cat['available'][0]
    featured=section.select_one('.letters-library-card')
    assert featured
    fresh=BeautifulSoup(f'''<article class="letters-library-card"><img src="../{item['cover']}" alt="Cover of Letter 03, intersecting paths" loading="lazy" width="1000" height="1500"><div><span class="eyebrow">No. 03 · Latest letter</span><h3>{label}</h3><p>{summary}</p><div class="button-line"><a class="btn btn-primary" href="../{item['url']}">Read online →</a><a class="btn btn-outline" href="../{item['pdf']}" download>PDF ↓</a><a class="btn btn-outline" href="../{item['epub']}" download>EPUB ↓</a></div><a class="text-link" href="../letters/">Browse all three Letters →</a></div></article>''','html.parser').article
    featured.replace_with(fresh)
    oldtext=BeautifulSoup(f'''<p class="letters-previous-link"><strong>Earlier in the series:</strong> <a href="../{prev['url']}">No. 02 — {html.escape(prev['title'])}</a> · <a href="../{prev0['url']}">No. 01 — {html.escape(prev0['title'])}</a></p>''','html.parser').p
    fresh.insert_after(oldtext)
    count=soup.select_one('.library-count')
    if count:
        count.select_one('span').string='04'
        small=count.select_one('small')
        if small:small.string='The foundational book + three Letters · Plus free journals and worksheets'
    library.write_text(str(soup),encoding='utf8')

    homepage=root/'index.html'
    home=BeautifulSoup(homepage.read_text('utf8'),'html.parser')
    feature=home.select_one('.letters-home-feature')
    assert feature
    feature.select_one('.eyebrow').string='New writing · Letters from H / 03'
    feature.select_one('h2').string='What do we owe to people we do not know?'
    feature.select_one('p').string=item['lead']
    primary=feature.select_one('a.btn')
    assert primary
    primary['href']=item['url']
    primary.string='Read the third Letter →'
    cover=feature.select_one('img')
    cover['src']=item['cover']
    cover['alt']='Cover of Letters from H No. 03: What Do We Owe to Strangers?'
    homepage.write_text(str(home),encoding='utf8')

    pubpath=root/'source/publications.json'
    publication=json.loads(pubpath.read_text('utf8'))
    publication['letters']={'series':'Letters from H','index':'letters/','issues':[
        {k:e[k] for k in ('id','title','url','pdf','epub','status')} for e in cat['available']
    ]}
    pubpath.write_text(json.dumps(publication,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    sitemap=root/'sitemap.xml'
    s=sitemap.read_text('utf8')
    url='https://thebookofchance.github.io/'+item['url']
    if url not in s:s=s.replace('</urlset>',f'<url><loc>{url}</loc></url>\n</urlset>')
    sitemap.write_text(s,encoding='utf8')
    info.update({'website_version':'0.13','letters_series_available':3,
         'letters_series_status':'Three editorial candidates; human approval and live deployment verification pending',
         'latest_letter_id':item['id'],'latest_letter_edition':item['edition']})
