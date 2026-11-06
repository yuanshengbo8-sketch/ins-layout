"""INS-053 — three giant pink words stacked down the left edge, overlapping the subject
Page 3, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-053", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (three giant pink words stacked down the left edge, overlapping the subject)"}

LINES = ['live.', 'laugh.', 'love.']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.55, 0.4))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 60, 640, 240, '#F15FA6', anchor='start', leading=1.12, weight='bold')

