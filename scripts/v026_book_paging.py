"""Enhance legacy /read/<section>/ pages with local-only, page-by-page controls.

Every full website build regenerates the same interface from the canonical book.
No published text, manuscript, title, source PDF, or EPUB is changed.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import shutil, json


def apply_v026(root: Path, info: dict):
    root=Path(root)
    source=root/'source/resources'
    shutil.copyfile(source/'v026-book-pages.js',root/'assets/book-pages.js')
    css=root/'assets/site.css'
    data=css.read_text('utf8')
    marker='/* v0.26 — Screen-height, one-page-at-a-time reading'
    if marker in data:
        data=data.split(marker)[0].rstrip()+'\n'
    css.write_text(data+'\n'+(source/'v026-book-pages.css').read_text('utf8'),encoding='utf8')
    js=root/'assets/site.js'
    content=js.read_text('utf8')
    old='const updateProgress=()=>{\n      const top=article.getBoundingClientRect()'
    new="const updateProgress=()=>{\n      if(document.querySelector('script[src*=\"book-pages.js\"]')){ticking=false;return;}\n      const top=article.getBoundingClientRect()"
    if new not in content:
        legacy_guard="const updateProgress=()=>{\n      if(document.body.classList.contains('book-paged-mode')){ticking=false;return;}\n      const top=article.getBoundingClientRect()"
        if legacy_guard in content:
            content=content.replace(legacy_guard,new)
        else:
            assert old in content, 'Cannot locate old scroll-progress handler'
            content=content.replace(old,new)
        js.write_text(content,encoding='utf8')
    count=0
    for file in sorted((root/'read').glob('*/index.html')):
        soup=BeautifulSoup(file.read_text('utf8'),'html.parser')
        if not soup.select_one('article.reading-article[data-reader-slug]'):continue
        for bar in soup.select('.reader-progress'):bar.decompose()
        for tag in soup.select('script[src*="book-pages.js"]'):tag.decompose()
        tag=soup.new_tag('script',src='../../assets/book-pages.js?v=0.26',defer='')
        soup.body.append(tag)
        file.write_text(str(soup),encoding='utf8')
        count+=1
    assert count==24,count
    info['website_version']='0.26'
    info['book_reading_mode']='Paged chapter reading, visible page counts and local-only position; no scroll-progress bar'
    info['book_paged_sections']=count
    (root/'SITE_CONTENT_MANIFEST.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf8')
