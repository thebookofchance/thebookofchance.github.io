"""Static site and journal collection verification for v0.9."""
from pathlib import Path
from bs4 import BeautifulSoup
import fitz, json, subprocess, hashlib
root=Path(__file__).resolve().parents[1]
errors=[];checked=0
pages=sorted(root.rglob('index.html'))
for page in pages:
    soup=BeautifulSoup(page.read_text('utf8'),'html.parser')
    if len(soup.select('main h1'))!=1:errors.append('Heading '+str(page.relative_to(root)))
    for element in soup.select('[src],[href]'):
        url=element.get('href') or element.get('src') or ''
        if not url or url.startswith(('http:','https:','mailto:','tel:','data:','javascript:')):continue
        path,_,anchor=url.partition('#')
        target=(page.parent/path.split('?')[0]).resolve() if path else page
        if target.is_dir():target=target/'index.html'
        if not target.is_file():errors.append('Broken file '+str(page.relative_to(root))+' -> '+url)
        elif anchor and target.suffix=='.html' and not BeautifulSoup(target.read_text('utf8'),'html.parser').find(id=anchor):errors.append('Missing anchor '+url)
        checked+=1
for path in ('assets/site.js','assets/reflect.js'):
    result=subprocess.run(['node','--check',str(root/path)],capture_output=True)
    if result.returncode:errors.append('JS '+path)
required={
    'The_Reflection_Journal_Fillable.pdf':(48,116),
    'The_Reflection_Journal_Dark_Fillable.pdf':(48,116),
    'The_Daily_Reflection_Journal_Fillable.pdf':(40,116),
    'The_Possibility_Journal_Fillable.pdf':(40,110),
    'The_Reflection_Journal_Print_Layout_Proof.pdf':(48,0)
}
for name,(pages_want,widgets_want) in required.items():
    p=root/'files/reflection'/name
    pdf=fitz.open(p);actual=sum(len(list(pg.widgets() or [])) for pg in pdf)
    if len(pdf)!=pages_want:errors.append(f'Page count {name}: {len(pdf)}')
    if actual!=widgets_want:errors.append(f'Fields {name}: {actual}')
    if len(pdf[0].get_text())<100:errors.append('No cover text '+name)
    for page in pdf:
        for widget in page.widgets() or []:
            if not page.rect.contains(widget.rect):errors.append('Widget outside page '+name)
        for blk in page.get_text('blocks'):
            x0,y0,x1,y1,*rest=blk
            if min(x0,y0)<-1 or x1>page.rect.width+1 or y1>page.rect.height+1:
                errors.append(f'Text clipped? {name}, page {page.number+1}, {x0,y0,x1,y1}')
    pdf.close()
# Digital covers can differ, interior PDF text must remain identical
l=fitz.open(root/'files/reflection/The_Reflection_Journal_Fillable.pdf')
d=fitz.open(root/'files/reflection/The_Reflection_Journal_Dark_Fillable.pdf')
for i in range(1,len(l)):
    if l[i].get_text()!=d[i].get_text():errors.append('Interior differs between Light/Dark page '+str(i+1))
l.close();d.close()
# a form entry is persistent, not just a display trick
pdf=fitz.open(root/'files/reflection/The_Reflection_Journal_Fillable.pdf')
testfile=root/'files/reflection/__form_test_tmp__.pdf'
firstpage=pdf[5]
first=next(iter(firstpage.widgets()))
first.field_value='2026-11-22 TEST'
first.update()
pdf.save(testfile);pdf.close()
reopen=fitz.open(testfile)
if not any(x.field_value=='2026-11-22 TEST' for x in reopen[5].widgets()):errors.append('PDF field value did not persist')
reopen.close();testfile.unlink()
for name in ['reflection-light','reflection-dark','daily','possibility']:
    if not (root/'assets/journals'/(name+'.webp')).is_file():errors.append('Cover image missing '+name)
res=json.loads((root/'source/publications.json').read_text('utf8'))
for entry in res['resources']:
    if entry['file'].endswith('.pdf') and not (root/entry['file']).is_file():errors.append('Resource catalogue '+entry['id'])
result={'release':'v0.9','html_pages':len(pages),'local_references_checked':checked,'journal_editions':4,'print_proofs':1,'errors':errors}
print(json.dumps(result,indent=2))
if errors:raise SystemExit(1)
