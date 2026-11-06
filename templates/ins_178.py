"""INS-178 — café portrait with a cream border and a small yellow hand-written line curving along the rim of the cup at
the bottom ('but it makes life so fun!').  Page 12, photos: 1.  Generated-asset dependencies: none.
The arc sits at --text cx= cy= r= (canvas px); defaults put it on the lower-centre where a cup usually is.
"""
from templates._common import T

META = {"id": "INS-178", "photos": 1, "assets": [], "family": "caption-notes", "photo_notes": "one café portrait; a cup or plate near the bottom centre"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 60, 1200, 1480, focus=(0.5, 0.35))
    cx, cy, r = float(T(ctx, "cx", 640)), float(T(ctx, "cy", 1560)), float(T(ctx, "r", 230))
    pid = c.uid("arc")
    c.defs.append(f'<path id="{pid}" d="M{cx - r} {cy} A{r} {r} 0 0 1 {cx + r} {cy}"/>')
    words = T(ctx, "line", "but it makes life so fun!")
    c.raw(f'<text font-family="Comic Sans MS, Chalkboard, sans-serif" font-size="30" fill="#F2DC5A" font-weight="bold">'
          f'<textPath href="#{pid}" startOffset="50%" text-anchor="middle">{words}</textPath></text>', "text")
