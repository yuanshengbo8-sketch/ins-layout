"""INS-104 — two stacked photos with outlined and solid white stars scattered on the right side, cream border.
Page 7, photos: 2.  Generated-asset dependencies: none.
"""
from components import deco

META = {"id": "INS-104", "photos": 2, "assets": [], "family": "sticker-stars", "photo_notes": "2 photos; stars avoid the faces (right side)"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 50, 1200, 730, focus=(0.5, 0.35))
    c.photo_rect(1, 0, 790, 1200, 760, focus=(0.5, 0.35))
    for (x, y, r, outline) in ((1080, 310, 50, True), (1080, 310, 34, True), (900, 240, 30, True), (1110, 150, 24, False),
                               (160, 1140, 42, True), (160, 1140, 26, True), (300, 1300, 22, True), (120, 1420, 20, False)):
        if outline:
            deco.star(c, x, y, r, "none", stroke="#fff", w=4, inner=0.5)
        else:
            deco.star(c, x, y, r, "#fff", inner=0.5)
