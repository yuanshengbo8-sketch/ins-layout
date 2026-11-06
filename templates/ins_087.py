"""INS-087 — three cyan words right-aligned beside the face; thin cream border
Page 6, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-087", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (three cyan words right-aligned beside the face; thin cream border)"}

LINES = ['Full', 'time', 'DIVA']


def build(c, ctx):
    framed_photo(c, 0, frame=(36, 36, 36, 36), focus=(0.4, 0.35))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 1120, 520, 165, '#35C4F0', anchor='end', leading=1.05, weight='normal')

