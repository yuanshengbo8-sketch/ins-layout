"""INS-060 — three centred amber bold lines over an indoor outfit shot
Page 4, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-060", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (three centred amber bold lines over an indoor outfit shot)"}

LINES = ['wear', '&', 'where']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.35))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 600, 560, 118, '#F8B531', anchor='middle', leading=1.6, weight='bold')

