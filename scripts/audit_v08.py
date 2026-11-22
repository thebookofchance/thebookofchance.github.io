"""Source-based release checks for Book of Chance v0.8.
Use python scripts/audit_v08.py after regenerating and producing PDFs.
Dependencies: beautifulsoup4 and PyMuPDF (from requirements.txt).
Browser device tests are supplemental and were performed separately for v0.8.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import fitz, json, subprocess
root=Path(__file__).resolve().parents[1]
issues=[];checked=0
pages=sorted(root.rglob('index.html'))
for page in pages:
    soup=BeautifulSoup(page.read_text('utf8'),'html.parser')
    if len(soup.select('main h1'))!=1:issues.append(f'Incorrect page heading: {page.relative_to(root)}')
    for tag in soup.select('[href],[src]'):
        ref=tag.get('href') or tag.get('src') or ''
        if not ref or ref.startswith(('http:','https:','mailto:','tel:','data:','javascript:')):continue
        uri,sep,fragment=ref.partition('#')
        target=(page.parent/uri.split('?')[0]).resolve() if uri else page
        if target.is_dir():target=target/'index.html'
        if not target.is_file():issues.append(f'Missing target: {page.relative_to(root)} -> {ref}')
        elif fragment and target.suffix=='.html' and not BeautifulSoup(target.read_text('utf8'),'html.parser').find(id=fragment):
            issues.append(f'Missing anchor: {page.relative_to(root)} -> {ref}')
        checked+=1
for rel in ('assets/site.js','assets/reflect.js'):
    if subprocess.run(['node','--check',str(root/rel)],capture_output=True).returncode:issues.append('Invalid JavaScript: '+rel)
assets=list((root/'files/reflection').glob('*.pdf'))
for p in assets:
    pdf=fitz.open(p)
    widgets=sum(len(list(pg.widgets() or [])) for pg in pdf)
    if '_Fillable' in p.stem and not widgets:issues.append('Missing form widgets: '+str(p))
    if 'Proof' in p.stem and widgets:issues.append('Unexpected widgets in print-layout proof: '+str(p))
    if p.name=='The_Reflection_Journal_Fillable.pdf' and len(pdf)!=28:issues.append('Journal page count changed')
    pdf.close()
result={'version':'v0.8','html_pages':len(pages),'local_references_checked':checked,'fillable_pdfs':4,'print_layout_proofs':1,'issues':issues}
print(json.dumps(result,indent=2))
if issues:raise SystemExit(1)
