"""INS-128 — five red bold lines upper-left-centre; thin cream border
Page 9, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-128", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (five red bold lines upper-left-centre; thin cream border)"}

LINES = ['photo', 'ideas', 'for', 'cool', 'girls']


def build(c, ctx):
    framed_photo(c, 0, frame=(40, 40, 40, 40), focus=(0.55, 0.35))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 560, 240, 118, '#D7262C', anchor='middle', leading=1.3, weight='bold')

