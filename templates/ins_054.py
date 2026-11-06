"""INS-054 — 'I' top-left, 'choose' mid-left, 'Myself' bottom-right in pink bold
Page 3, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-054", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block ('I' top-left, 'choose' mid-left, 'Myself' bottom-right in pink bold)"}

LINES = ['I', 'choose', 'Myself']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.35))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    c.text(70, 430, lines[0] if 0 < len(lines) else '', size=170.0, fill='#F49AC1', anchor='start', weight='bold')
    c.text(70, 770.0, lines[1] if 1 < len(lines) else '', size=170.0, fill='#F49AC1', anchor='start', weight='bold')
    c.text(1140, 1100.0, lines[2] if 2 < len(lines) else '', size=170.0, fill='#F49AC1', anchor='end', weight='bold')

