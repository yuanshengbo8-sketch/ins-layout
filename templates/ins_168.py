"""INS-168 — 'nov em ber' stacked cream bold, each line stepping right, two big pink stars and two small yellow ones
Page 11, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-168", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block ('nov em ber' stacked cream bold, each line stepping right, two big pink stars and two small yellow ones)"}

LINES = ['nov', 'em', 'ber']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.4))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 560, 620, 175, '#F6F0A8', anchor='middle', leading=1.0, weight='bold', per_line=[None, {'dx': 40}, {'dx': 90}])
    deco.star(c, 1010, 540, 150, '#E8738F', rot=-80)
    deco.star(c, 330, 1030, 150, '#E8738F', rot=-100)
    deco.star(c, 390, 560, 55, '#F7E7A5')
    deco.star(c, 850, 980, 55, '#F7E7A5')
