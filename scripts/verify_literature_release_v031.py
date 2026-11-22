from __future__ import annotations
import json,zipfile,fitz,hashlib,re,xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse,unquote
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
R=Path(__file__).resolve().parents[1]
release_routes=['booklets/the-little-book-of-possibilities/','publications/conversations-of-chance/','publications/beginners-guide-to-confluent-humanism/','publications/parables-of-chance/','questions/','journey/']
froms={};bad=[];total=0;anchors=0
for f in R.rglob('index.html'):
 if any(str(part).startswith('_build') for part in f.parts):continue
 soup=BeautifulSoup(f.read_text('utf8'),'html.parser')
 ids={el.get('id') for el in soup.find_all(id=True)}
 for tag in soup.find_all(['a','link','script','img','source']):
  for attr in ('href','src'):
   if not tag.get(attr):continue
   ref=tag[attr]
   if ref.startswith(('http:','https:','mailto:','javascript:','tel:','data:','//')):continue
   path,frag=ref.split('#',1) if '#' in ref else (ref,'')
   path=path.split('?',1)[0]
   if not path and frag:
    anchors+=1
    if frag not in ids:bad.append(f'{f.relative_to(R)} → {ref} (missing local anchor)')
    continue
   if not path:continue
   target=(f.parent/unquote(path)).resolve()
   if not target.is_relative_to(R.resolve()):bad.append(f'{f.relative_to(R)} → {ref} (outside repo)');continue
   if target.is_dir():target=target/'index.html'
   if not target.exists():
    bad.append(f'{f.relative_to(R)} → {ref} (not found)');continue
   total+=1
   if frag and target.suffix=='.html':
    anchors+=1
    anchor_ids=froms.get(target)
    if anchor_ids is None:
     anchor_ids={el.get('id') for el in BeautifulSoup(target.read_text('utf8'),'html.parser').find_all(id=True)}
     froms[target]=anchor_ids
    if frag not in anchor_ids:bad.append(f'{f.relative_to(R)} → {ref} (missing target anchor)')

sitemap=ET.parse(R/'sitemap.xml'); slocs={el.text for el in sitemap.getroot().iter() if el.tag.endswith('loc')}
for r in release_routes:
 t=R/r/'index.html'
 soup=BeautifulSoup(t.read_text('utf8'),'html.parser')
 assert not any('noindex' in (m.get('content','').lower()) for m in soup.find_all('meta',attrs={'name':'robots'})), f'noindex on {r}'
 assert 'https://thebookofchance.github.io/'+r in slocs, f'missing sitemap {r}'
assert 'noindex' in (R/'reader/index.html').read_text('utf8')
assert 'https://thebookofchance.github.io/reader/' not in slocs
assert not bad, '\n'.join(bad[:30])

pub=json.loads((R/'source/publications.json').read_text('utf8'))
letters=pub['letters']['issues']
items=(pub['available']+letters+pub['booklets']+pub['conversations']+pub['parables']+pub['guides']+pub['reader_resources'])
assert len(items)==10,len(items)
assert all('author-approved' in i.get('status','') for i in items)

refs=[]
for item in items:
 if item['id']=='book-of-chance':
  variants=[]
  for ed in item['editions']:
   variants.append({'label':ed['name'],'pdf':ed['pdf'],'epub':ed['epub'],'cover':ed['cover']})
 else:
  variants=[{'label':'Digital edition','pdf':item['pdf'],'epub':item['epub'],'cover':item.get('cover') or ('assets/letters/lfh-'+item['id'].split('-')[-1]+'-cover.webp')}]
 for v in variants:
  pf=R/v['pdf'];ef=R/v['epub'];cf=R/v['cover'];assert pf.is_file() and ef.is_file() and cf.is_file(),(item,v)
  with fitz.open(pf) as d:
   assert d.page_count>=2
   assert d.metadata.get('author')=='H',(pf,d.metadata.get('author'))
   assert d.xref_get_key(d.pdf_catalog(),'StructTreeRoot')[0]=='xref',f'PDF lacks tags: {pf}'
   text='\n'.join(p.get_text() for p in d)
   assert not any(x in text.lower() for x in ('editorial candidate','editorial proof','for author review','not a final release')),pf
   pages=d.page_count
  with zipfile.ZipFile(ef) as z:
   assert z.testzip() is None
   assert z.namelist()[0]=='mimetype' and z.getinfo('mimetype').compress_type==zipfile.ZIP_STORED,ef
   infos=[n for n in z.namelist() if n.lower().endswith('.opf')]
   assert infos,ef
   eptext=''.join(z.read(n).decode('utf8','ignore') for n in z.namelist() if n.lower().endswith(('.xhtml','.opf','.html')))
   assert not any(x in eptext.lower() for x in ('editorial candidate','editorial proof','for author review','not a final release')),ef
  refs.append({'id':item['id'],'title':item['title'],'edition':v['label'],'pdf':v['pdf'],'pdf_sha256':hashlib.sha256(pf.read_bytes()).hexdigest(),'pdf_pages':pages,'epub':v['epub'],'epub_sha256':hashlib.sha256(ef.read_bytes()).hexdigest(),'cover':v['cover'],'cover_sha256':hashlib.sha256(cf.read_bytes()).hexdigest()})
assert len(refs)==11

public_html=[]
for f in R.rglob('index.html'):
 if '_build' in str(f.relative_to(R)):continue
 t=f.read_text('utf8')
 if 'editorial candidate' in t.lower() or 'editorial proof' in t.lower():public_html.append(str(f.relative_to(R)))
assert not public_html,public_html
assert not re.search(r'\bRNG\b',' '.join(p.read_text('utf8') for p in R.glob('source/**/*.md')),re.I)

register={'release':'Author-approved digital publication release v0.31',
 'approved_by':'H (user confirmation in project conversation)',
 'approval_date':'2026-11-23','scope':'Nine library titles plus Questions About Chance FAQ',
 'status':'Author-approved digital editions; no independent accessibility certification or external editorial endorsement claimed',
 'items':refs,
 'notes':'Filename stems including Editorial_Proof are retained for URL continuity; page text and metadata describe the current author-approved digital release.'}
reg=R/'docs/Literature_Release_Register_v0.31.json';reg.write_text(json.dumps(register,indent=2,ensure_ascii=False)+'\n','utf8')
qa={'version':'0.31','html_pages_checked':sum(1 for f in R.rglob('index.html') if '_build' not in str(f)),
 'local_file_links_checked':total,'anchors_checked':anchors,'broken':bad,
 'edition_pairs_checked':11,'sitemap_new_public_pages':release_routes,
 'reader_noindex_preserved':True,'old_public_candidate_statuses_remaining':len(public_html),
 'user_form_confirmation':'reported working; not rechecked directly','independent_accessibility_compliance':'not verified'}
(R/'docs/Literature_Release_QA_v0.31.json').write_text(json.dumps(qa,indent=2)+'\n','utf8')
print(json.dumps(qa,indent=2))
