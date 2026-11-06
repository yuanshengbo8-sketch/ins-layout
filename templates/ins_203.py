"""INS-203 — two short yellow bold lines at the centre; thin cream border
Page 13, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-203", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (two short yellow bold lines at the centre; thin cream border)"}

LINES = ['wtf is', 'stay home']


def build(c, ctx):
    framed_photo(c, 0, frame=(40, 40, 40, 40), focus=(0.5, 0.45))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 600, 780, 82, '#F5E64B', anchor='middle', leading=1.1, weight='bold')

