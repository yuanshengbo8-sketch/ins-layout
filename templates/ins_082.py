"""INS-082 — five centred mint bold lines over a close-up
Page 6, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-082", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (five centred mint bold lines over a close-up)"}

LINES = ['life is', 'so cool', 'when', "you don't", 'care']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.35))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 600, 380, 125, '#8FE3D8', anchor='middle', leading=1.32, weight='bold')

