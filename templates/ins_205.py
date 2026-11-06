"""INS-205 — six yellow caps lines left-centre; photo letterboxed with cream bars
Page 13, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-205", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (six yellow caps lines left-centre; photo letterboxed with cream bars)"}

LINES = ['MY', 'OUTFITS', 'HAVE MORE', 'STRUCTURE', 'THAN MY', 'LIFE…']


def build(c, ctx):
    framed_photo(c, 0, frame=(200, 0, 180, 0), focus=(0.5, 0.3))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 330, 640, 88, '#E8D35B', anchor='middle', leading=1.3, weight='normal')

