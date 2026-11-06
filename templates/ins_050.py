"""INS-050 — five mint words scattered around the subject plus three mint stars
Page 3, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-050", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (five mint words scattered around the subject plus three mint stars)"}

LINES = ['photo', 'ideas', 'for', 'cool', 'girls']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.35))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    c.text(380, 250, lines[0] if 0 < len(lines) else '', size=90, fill='#BFF0E8', anchor='middle', weight='normal', rotate=0)
    c.text(900, 620, lines[1] if 1 < len(lines) else '', size=90, fill='#BFF0E8', anchor='middle', weight='normal', rotate=0)
    c.text(200, 850, lines[2] if 2 < len(lines) else '', size=90, fill='#BFF0E8', anchor='middle', weight='normal', rotate=0)
    c.text(820, 1080, lines[3] if 3 < len(lines) else '', size=90, fill='#BFF0E8', anchor='middle', weight='normal', rotate=0)
    c.text(420, 1300, lines[4] if 4 < len(lines) else '', size=90, fill='#BFF0E8', anchor='middle', weight='normal', rotate=0)
    deco.star(c, 890, 300, 40, '#BFF0E8')
    deco.star(c, 130, 580, 38, '#BFF0E8')
    deco.star(c, 680, 1360, 40, '#BFF0E8')
