"""INS-145 — portrait with three halftone-dotted white '?' above the head (the middle one larger and tilted), the
character 泪 raining down both sides of the face in mint, and dotted quotation marks left and right.
Page 10, photos: 1.  Generated-asset dependencies: none.
"""
import random

from components import deco
from templates._common import T, face_box

META = {"id": "INS-145", "photos": 1, "assets": [], "family": "letter-rain", "photo_notes": "one portrait; columns hug the measured face"}


def build(c, ctx):
    c.photo_full(0, focus=(0.5, 0.35))
    fx, fy, fw, fh = face_box(ctx)
    cx, cy = fx * 1200, fy * 1600
    top = (fy - fh / 2) * 1600
    deco.dotted_glyph(c, cx - 230, top - 20, "?", 230, rotate=-10, anchor="middle")
    deco.dotted_glyph(c, cx, top - 60, "?", 330, rotate=4, anchor="middle")
    deco.dotted_glyph(c, cx + 200, top - 30, "?", 220, rotate=12, anchor="middle")
    deco.dotted_glyph(c, 120, cy + 260, "“", 200, anchor="middle")
    deco.dotted_glyph(c, 1090, cy + 40, "”", 200, anchor="middle")
    ch = T(ctx, "char", "泪")
    rnd = random.Random(11)
    for side in (-1, 1):
        x0 = cx + side * (fw * 1200 / 2 + 80)
        yy = cy - 40; k = 0
        while yy < cy + 620:
            c.text(x0 + rnd.uniform(-30, 30) + (k % 2) * side * 40, yy, ch, size=rnd.uniform(44, 64), font="cjk", fill="#7FE7D8", anchor="middle")
            yy += rnd.uniform(70, 95); k += 1
