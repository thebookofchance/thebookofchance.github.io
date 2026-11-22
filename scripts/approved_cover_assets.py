"""Approved cover assets are *inputs* to publication builds; never regenerate them."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'source/approved_cover_assets_v030.json'
def check_cover(name):
    item=json.loads(MANIFEST.read_text(encoding='utf-8'))['covers'][name]
    path=ROOT/item['path']
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:
        raise RuntimeError('Approved cover missing or modified: '+str(path))
    return path
