"""INS-109 — four yellow bold lines, generous leading, left-centre
Page 7, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-109", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (four yellow bold lines, generous leading, left-centre)"}

LINES = ['autumn', 'is for', 'coffee', 'dates']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.4))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 470, 460, 108, '#F6E9A3', anchor='middle', leading=1.5, weight='bold')

