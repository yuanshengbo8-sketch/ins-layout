"""INS-194 — one lilac-pink line across the lower third; thin cream border
Page 13, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-194", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (one lilac-pink line across the lower third; thin cream border)"}

LINES = ['be urself']


def build(c, ctx):
    framed_photo(c, 0, frame=(36, 36, 36, 36), focus=(0.5, 0.3))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 50, 1010, 250, '#E7A3DC', anchor='start', leading=1, weight='normal')

