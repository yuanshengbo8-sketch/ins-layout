"""INS-110 — three centred yellow bold lines over a sunny street photo
Page 7, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-110", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (three centred yellow bold lines over a sunny street photo)"}

LINES = ['autumn', 'is for', 'slow days']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.3))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 600, 560, 108, '#F5E39A', anchor='middle', leading=1.6, weight='bold')

