"""INS-206 — three centred mint bold lines over a selfie
Page 13, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-206", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (three centred mint bold lines over a selfie)"}

LINES = ['its', 'finally', 'autumn']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.3))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 600, 640, 92, '#9FF2DA', anchor='middle', leading=1.35, weight='bold')

