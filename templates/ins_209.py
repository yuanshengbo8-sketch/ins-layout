"""INS-209 — six yellow lines, right-of-centre, from top to bottom
Page 14, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-209", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (six yellow lines, right-of-centre, from top to bottom)"}

LINES = ['yes,', 'i planned', 'the', 'outfit', 'before', 'the plans']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.4))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 740, 230, 128, '#F7E86B', anchor='middle', leading=1.33, weight='normal')

