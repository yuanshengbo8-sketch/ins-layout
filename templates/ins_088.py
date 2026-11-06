"""INS-088 — six centred yellow lines with two large pink stars either side
Page 6, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-088", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (six centred yellow lines with two large pink stars either side)"}

LINES = ['wait this', 'is so', 'cool', 'I need', 'to capture', 'it']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.35))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 600, 430, 118, '#F5E63B', anchor='middle', leading=1.3, weight='normal')
    deco.star(c, 270, 610, 120, '#E58CB5', rot=-80)
    deco.star(c, 930, 760, 125, '#E58CB5', rot=-100)
