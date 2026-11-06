"""INS-108 — five pastel bold words right of the face, two small yellow stars
Page 7, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-108", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (five pastel bold words right of the face, two small yellow stars)"}

LINES = ['i', 'take', 'a LOT', 'of', 'pictures']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.35, 0.45))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 840, 270, 112, '#FFFFFF', anchor='middle', leading=1.1, weight='bold', per_line=[None, None, {'fill': '#A9EDE0'}, {'fill': '#F9E3C0'}, {'fill': '#CDBDF2'}])
    deco.star(c, 1055, 205, 34, '#F2D34B')
    deco.star(c, 570, 500, 36, '#F2D34B')
