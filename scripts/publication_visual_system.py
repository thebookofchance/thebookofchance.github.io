"""Reusable publication visual helpers for The Book of Chance.

The goal is not to replace the original Light/Dark book covers, but to extend
that visual language across companion publications.
"""
from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
import math

try:
    import cairosvg
    from PIL import Image
except Exception:  # pragma: no cover
    cairosvg = None
    Image = None

PAPER = '#fbfbfa'
INK = '#26313B'
MUTED = '#68747c'
BLUE = '#286CB8'
SOFT = '#8e959a'
FAINT = '#d8dfe2'


def path(d, stroke, width, opacity=1.0):
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"/>'


def text(x, y, value, size, fill=INK, family="Liberation Serif,Georgia,serif", anchor='middle', italic=False, letter_spacing=None):
    style = 'font-style:italic;' if italic else ''
    ls = f' letter-spacing:{letter_spacing}px;' if letter_spacing is not None else ''
    safe = (value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{fill}" font-family="{family}" style="{style}{ls}">{safe}</text>'


def line(x1,y1,x2,y2,stroke=BLUE,width=2,opacity=1.0):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}"/>'


def circle(cx, cy, r, stroke=BLUE, fill='white', width=1.5, opacity=1.0):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}"/>'


def render_svg(title_lines, subtitle_lines, series_label, motif_svg, *, title_y=315, subtitle_y=520, top_y=92):
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1500" width="1000" height="1500">',
        f'<rect width="1000" height="1500" fill="{PAPER}"/>',
        text(500, top_y, series_label, 26, fill=BLUE, family='Lato,Liberation Sans,sans-serif', letter_spacing=5.2),
    ]
    step = 90
    for i, line_text in enumerate(title_lines):
        italic = line_text.strip().lower() == 'of'
        size = 88 if not italic else 80
        parts.append(text(500, title_y + step*i, line_text, size, fill=INK, italic=italic))
    for i, sub in enumerate(subtitle_lines):
        parts.append(text(500, subtitle_y + 42*i, sub, 28, fill=MUTED, italic=True))
    parts.append(motif_svg)
    parts.append(line(425, 1328, 575, 1328, BLUE, 2))
    parts.append(text(500, 1397, 'H', 48, fill=INK))
    parts.append('</svg>')
    return ''.join(parts)


def conversation_motif():
    # Twelve fine routes, two highlighted in blue. Based on the main book's open crossings.
    lines = []
    configs = [
        ( 35, 660, 255, 520, 410, 865, 640, 685, 970, 560, SOFT, 1.5, 0.42),
        ( 25, 715, 230, 645, 390, 910, 670, 740, 970, 645, FAINT, 1.3, 0.55),
        ( 40, 765, 245, 680, 410, 945, 645, 815, 965, 695, SOFT, 1.8, 0.48),
        ( 35, 817, 245, 715, 405, 985, 655, 870, 970, 757, FAINT, 1.3, 0.58),
        ( 25, 875, 210, 765, 420, 1045, 645, 935, 970, 825, SOFT, 1.7, 0.46),
        ( 30, 950, 205, 845, 415, 1115, 655, 990, 975, 890, FAINT, 1.3, 0.60),
        ( 35, 975, 260, 825, 490, 665, 735, 935, 970, 1075, BLUE, 3.5, 0.88),
        ( 40, 890, 275, 755, 520, 630, 730, 875, 965, 1020, INK, 2.2, 0.78),
        ( 40, 780, 290, 665, 535, 605, 728, 805, 960, 930, BLUE, 3.3, 0.82),
        ( 35, 700, 310, 605, 560, 575, 730, 710, 965, 825, INK, 2.1, 0.74),
        ( 40, 630, 325, 565, 565, 580, 730, 650, 970, 740, SOFT, 1.7, 0.52),
        ( 50, 580, 345, 550, 575, 590, 720, 595, 970, 675, FAINT, 1.2, 0.63),
    ]
    for x1,y1,c1x,c1y,c2x,c2y,c3x,c3y,x2,y2,stroke,w,op in configs:
        d = f'M {x1} {y1} C {c1x} {c1y} {c2x} {c2y} {c3x} {c3y} S {x2-120} {y2+40} {x2} {y2}'
        lines.append(path(d, stroke, w, op))
    # Add a few small open nodes to suggest multiple voices rather than a single path.
    for cx, cy in [(260, 645), (510, 665), (702, 855), (820, 950)]:
        lines.append(circle(cx, cy, 6, BLUE if cx in (510,702) else SOFT, 'white', 1.8, 0.95))
    return ''.join(lines)


def build_conversations_assets(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    svg = render_svg(
        ['Conversations', 'of Chance'],
        ['Twelve Discussions', 'for an Uncertain Life'],
        'THE BOOK OF CHANCE · COMPANIONS',
        conversation_motif(),
        title_y=298,
        subtitle_y=505,
        top_y=94,
    )
    (out_dir/'conversations-of-chance-cover.svg').write_text(svg, encoding='utf8')
    if cairosvg is None or Image is None:
        return
    png_path = out_dir/'conversations-of-chance-cover.png'
    cairosvg.svg2png(bytestring=svg.encode('utf8'), write_to=str(png_path), output_width=1000, output_height=1500)
    img = Image.open(png_path).convert('RGB')
    img.save(out_dir/'conversations-of-chance-cover.webp', 'WEBP', quality=92, method=6)


if __name__ == '__main__':
    ROOT = Path(__file__).resolve().parents[1]
    build_conversations_assets(ROOT/'assets/publications')
