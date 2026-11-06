"""INS-127 — four centred cream-yellow bold lines; thin cream border
Page 9, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-127", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (four centred cream-yellow bold lines; thin cream border)"}

LINES = ['i take', 'a lot', 'of', 'pictures:']


def build(c, ctx):
    framed_photo(c, 0, frame=(40, 40, 40, 40), focus=(0.5, 0.3))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 600, 620, 128, '#F4E7A0', anchor='middle', leading=1.3, weight='bold')

