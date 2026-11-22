"""Read-only structural release-candidate checks for 11 PDF/EPUB edition pairs.

This is a production preflight, not PDF/UA certification or a screen-reader test.
Run: python scripts/verify_literature_production_v030.py
"""
from __future__ import annotations
from pathlib import Path
import hashlib, json, io, zipfile, re, sys
from urllib.parse import urlsplit, unquote
from PIL import Image
from bs4 import BeautifulSoup
import fitz

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from approved_cover_assets import check_cover

EDITIONS=[
 ('book-light','files/The_Book_of_Chance_Light_PDF_Reader_Proof.pdf','files/The_Book_of_Chance_Light.epub'),
 ('book-dark','files/The_Book_of_Chance_Dark_PDF_Reader_Proof.pdf','files/The_Book_of_Chance_Dark.epub'),
 ('letter-01','files/letters/Letters_from_H_01_On_the_People_We_Never_Meet.pdf','files/letters/Letters_from_H_01_On_the_People_We_Never_Meet.epub'),
 ('letter-02','files/letters/Letters_from_H_02_When_Good_Choices_Lead_to_Bad_Outcomes.pdf','files/letters/Letters_from_H_02_When_Good_Choices_Lead_to_Bad_Outcomes.epub'),
 ('letter-03','files/letters/Letters_from_H_03_What_Do_We_Owe_to_Strangers.pdf','files/letters/Letters_from_H_03_What_Do_We_Owe_to_Strangers.epub'),
 ('five-values','files/booklets/The_Five_Values.pdf','files/booklets/The_Five_Values.epub'),
 ('conversations','files/conversations/Conversations_of_Chance_Editorial_Proof_v0.1.pdf','files/conversations/Conversations_of_Chance_Editorial_Proof_v0.1.epub'),
 ('possibilities','files/booklets/The_Little_Book_of_Possibilities_Editorial_Proof_v0.2.pdf','files/booklets/The_Little_Book_of_Possibilities_Editorial_Proof_v0.2.epub'),
 ('parables','files/parables/The_Parables_of_Chance_Editorial_Proof_v0.2.1.pdf','files/parables/The_Parables_of_Chance_Editorial_Proof_v0.2.1.epub'),
 ('beginner','files/guides/A_Beginners_Guide_to_Confluent_Humanism_Editorial_Proof_v0.2.pdf','files/guides/A_Beginners_Guide_to_Confluent_Humanism_Editorial_Proof_v0.2.epub'),
 ('faq','files/resources/Questions_About_Chance_FAQ_Editorial_Proof_v0.3.pdf','files/resources/Questions_About_Chance_FAQ_Editorial_Proof_v0.3.epub')
]
issues=[];results=[]
for name,pdf_rel,epub_rel in EDITIONS:
    approved=check_cover(name)
    pdf=ROOT/pdf_rel;epub=ROOT/epub_rel
    detail={'id':name,'pdf':pdf_rel,'epub':epub_rel,'cover':str(approved.relative_to(ROOT))}
    if not pdf.exists() or not epub.exists():
        issues.append(name+': missing PDF or EPUB');results.append(detail);continue
    with fitz.open(pdf) as d:
        md=d.metadata
        detail['pdf_pages']=len(d)
        detail['author']=md.get('author')
        detail['title']=md.get('title')
        detail['tags']=d.xref_get_key(d.pdf_catalog(),'StructTreeRoot')[0]=='xref'
        detail['marked']=d.xref_get_key(d.pdf_catalog(),'MarkInfo')[0]=='dict'
        detail['pdf_language']=d.xref_get_key(d.pdf_catalog(),'Lang')[1]
        detail['pdf_ua_identifier']=bool(d.xref_xml_metadata() and b'pdfuaid:part="1"' in d.xref_stream(d.xref_xml_metadata()))
        detail['cover_text_characters']=len(d[0].get_text().strip())
        detail['cover_image_count']=len(d[0].get_images())
        if md.get('author')!='H' or not md.get('title'):issues.append(name+': missing PDF metadata')
        if not all((detail['tags'],detail['marked'],detail['pdf_ua_identifier'])):issues.append(name+': missing tagged PDF structure')
        if detail['cover_text_characters']:issues.append(name+': extractable former text under cover')
        if not detail['cover_image_count']:issues.append(name+': no cover image embedded')
    with zipfile.ZipFile(epub) as z:
        names=z.namelist();assets=set(names)
        detail['epub_zip_ok']=z.testzip() is None
        detail['epub_mimetype_first']=names[0]=='mimetype' and z.getinfo(names[0]).compress_type==zipfile.ZIP_STORED
        cover_images=[n for n in names if '/media/' in n.lower() and 'cover' in n.lower() and n.lower().endswith(('.png','.jpg','.webp'))]
        detail['epub_embedded_cover']=cover_images[0] if cover_images else None
        if cover_images:
            source=Image.open(approved).convert('RGBA')
            embedded=Image.open(io.BytesIO(z.read(cover_images[0]))).convert('RGBA')
            detail['cover_pixel_match']=source.size==embedded.size and source.tobytes()==embedded.tobytes()
        else:detail['cover_pixel_match']=False
        if not (detail['epub_zip_ok'] and detail['epub_mimetype_first'] and detail['cover_pixel_match']):
            issues.append(name+': epub package or cover mismatch')
        nav_problems=[]
        for p in names:
            if not p.endswith(('.xhtml','.html')):continue
            soup=BeautifulSoup(z.read(p),'html.parser')
            for anchor in soup.find_all('a',href=True):
                sp=urlsplit(anchor['href'])
                if sp.scheme or sp.netloc:continue
                target=(Path(p).parent/sp.path) if sp.path else Path(p)
                norm=__import__('posixpath').normpath(str(target))
                if norm not in assets:nav_problems.append((p,anchor['href']))
                elif sp.fragment:
                    target_doc=BeautifulSoup(z.read(norm),'html.parser')
                    if not target_doc.find(id=unquote(sp.fragment)):
                        nav_problems.append((p,anchor['href']))
        detail['epub_broken_links']=len(nav_problems)
        if nav_problems:issues.append(name+': broken EPUB navigation')
    results.append(detail)

# Check only public HTML, excluding intermediate HTML used for printing.
links=0;broken=[];anchors=0;bad_anchors=[]
htmlfiles=[p for p in ROOT.rglob('*.html') if not any(part.startswith('_build') for part in p.relative_to(ROOT).parts)]
soups={p.resolve():BeautifulSoup(p.read_text('utf-8'),'html.parser') for p in htmlfiles}
for file,soup in soups.items():
    for element in soup.find_all(['a','img','script','link','source']):
        raw=element.get('href') or element.get('src')
        if not raw:continue
        parsed=urlsplit(raw)
        if parsed.scheme or parsed.netloc:continue
        if raw.startswith(('data:','mailto:','tel:')):continue
        target=(ROOT/unquote(parsed.path).lstrip('/')) if parsed.path.startswith('/') else (file.parent/unquote(parsed.path))
        if not parsed.path:target=file
        target=target.resolve()
        if not target.is_relative_to(ROOT.resolve()):continue
        if target.is_dir():target=target/'index.html'
        links+=1
        if not target.exists():broken.append((str(file.relative_to(ROOT)),raw));continue
        if parsed.fragment and element.name=='a' and target in soups:
            anchors+=1
            if not soups[target].find(id=unquote(parsed.fragment)) and not soups[target].find(attrs={'name':unquote(parsed.fragment)}):
                bad_anchors.append((str(file.relative_to(ROOT)),raw))
if broken:issues.append(str(len(broken))+' broken public HTML references')
if bad_anchors:issues.append(str(len(bad_anchors))+' broken public HTML anchors')
info={'edition_count':len(EDITIONS),'html_count':len(htmlfiles),'internal_refs_checked':links,
      'broken_links':broken,'anchors_checked':anchors,'broken_anchors':bad_anchors,
      'results':results,'issues':issues,
      'qualification':'Programmatic PDF tagging checks do not establish PDF/UA certification or screen-reader accessibility.'}
print(json.dumps(info,ensure_ascii=False,indent=2))
if issues:raise SystemExit(1)
