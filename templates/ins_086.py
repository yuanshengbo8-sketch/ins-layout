"""INS-086 — six centred pink bold lines; photo letterboxed with cream bars top and bottom
Page 6, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-086", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (six centred pink bold lines; photo letterboxed with cream bars top and bottom)"}

LINES = ['Being', 'insecure', 'is', 'such a waste', 'of', 'youth']


def build(c, ctx):
    framed_photo(c, 0, frame=(110, 0, 100, 0), focus=(0.5, 0.35))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 600, 230, 168, '#F7A3CF', anchor='middle', leading=1.33, weight='bold')

