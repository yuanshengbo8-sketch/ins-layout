"""INS-207 — four centred lilac lines
Page 13, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-207", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (four centred lilac lines)"}

LINES = ["i've been", 'ghosting you', "cause I'm", 'working']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.4))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    stacked(c, lines, 600, 640, 92, '#A9A6F2', anchor='middle', leading=1.35, weight='normal')

