"""INS-059 — 'i need to' light green, 'Create®' huge bold green offset right-down; thin cream border
Page 4, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-059", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block ('i need to' light green, 'Create®' huge bold green offset right-down; thin cream border)"}

LINES = ['i need to', 'Create®']


def build(c, ctx):
    framed_photo(c, 0, frame=(40, 40, 40, 40), focus=(0.5, 0.35))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    c.text(80, 720, lines[0] if 0 < len(lines) else '', size=82.0, fill='#C6F23A', anchor='start', weight='normal')
    c.text(300, 952, lines[1] if 1 < len(lines) else '', size=151.70000000000002, fill='#C6F23A', anchor='start', weight='bold')

