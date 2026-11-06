"""INS-204 — five centred cyan bold lines
Page 13, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-204", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (five centred cyan bold lines)"}

LINES = ['some people', 'miss their', 'exes I miss', 'the clothes I', "didn't buy"]


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.35))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 600, 470, 110, '#28D0E8', anchor='middle', leading=1.35, weight='bold')

