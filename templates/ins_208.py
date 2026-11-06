"""INS-208 — four centred soft-yellow lines below the eyes
Page 14, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-208", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (four centred soft-yellow lines below the eyes)"}

LINES = ['Kinda chic', 'to feel', 'everything', 'deeply']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.3))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 600, 700, 72, '#F7E68A', anchor='middle', leading=1.2, weight='normal')

