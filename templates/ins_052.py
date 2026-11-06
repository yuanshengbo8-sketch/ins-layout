"""INS-052 — 4 centred pink lines over a full-bleed night photo
Page 3, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-052", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (4 centred pink lines over a full-bleed night photo)"}

LINES = ['I just want to dress cool,', 'travel the world', 'and drink coffee', 'every day']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.3))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 600, 720, 78, '#F7A6C8', anchor='middle', leading=1.2, weight='normal')

