"""Static route, asset and anchor verification for the full v0.24 website.

Run from the repo root: python scripts/audit_journey_v024.py
This does not assert live GitHub Pages deployment or accessible PDF tagging.
"""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
SKIP={'_build_book','_build_parables','_build_beginner_guide','_build_conversations','_build_faq','_build_possibilities'}
htmls=[p for p in ROOT.rglob('*.html') if not any(part in SKIP or part.startswith('_build') for part in p.relative_to(ROOT).parts)]
ids={p:set(tag.get('id') for tag in BeautifulSoup(p.read_text('utf8'),'html.parser').select('[id]') if tag.get('id')) for p in htmls}
count=0; errors=[]; assets=0
for p in htmls:
    s=BeautifulSoup(p.read_text('utf8'),'html.parser')
    for item in s.select('[href], img[src], script[src]'):
        attr='href' if item.has_attr('href') else 'src'
        val=item[attr]
        if not val or val.startswith(('mailto:','tel:','data:','javascript:','blob:')):continue
        parsed=urlsplit(val)
        if parsed.scheme or parsed.netloc:continue
        raw=unquote(parsed.path)
        if raw.startswith('/'):
            target=ROOT/raw.lstrip('/')
        else:
            target=p.parent/raw if raw else p
        if target.is_dir():target/= 'index.html'
        target=target.resolve()
        count+=1
        if not target.exists():errors.append(f'{p.relative_to(ROOT)}: missing {val}')
        elif parsed.fragment:
            anchor=unquote(parsed.fragment)
            if target.suffix=='.html':
                if anchor not in ids.get(target,set()):errors.append(f'{p.relative_to(ROOT)}: missing anchor {val}')
        if item.name in ('img','script','link'):assets+=1
assert not errors, '\n'.join(errors[:35])
journey=json.loads((ROOT/'source/resources/guided-reading-journey.json').read_text('utf8'))
assert len(journey['paths'])==8 and sum(len(p['steps']) for p in journey['paths'])==24
assert (ROOT/'journey/index.html').is_file() and (ROOT/'assets/journey.js').is_file()
for p in (ROOT/'journey/index.html',ROOT/'source/resources/guided-reading-journey.json',ROOT/'assets/journey.js'):
    assert 'RNG' not in p.read_text('utf8')
print(json.dumps({'html_pages':len(htmls),'internal_refs_checked':count,'missing_paths_or_anchors':len(errors),'journey_paths':8,'journey_stops':24,'result':'passed'},indent=2))
