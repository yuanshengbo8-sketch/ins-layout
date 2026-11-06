"""INS-056 — full photo (a table/food scene) with a large circular inset portrait in the centre and the words
'Lit tle' (top-right of the circle) and 'café dia ry' (bottom-left) in white bold, broken across lines.
Page 4, photos: 2.  Generated-asset dependencies: none.
"""
from templates._common import T

META = {"id": "INS-056", "photos": 2, "assets": [], "family": "circle-inset", "photo_notes": "#1 background scene (table/food), #2 portrait for the circle"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 50, 1200, 1500, focus=(0.5, 0.5))
    c.photo_circle(1, 600, 800, 330, focus=(0.5, 0.35))
    w1 = T(ctx, "w1", "Lit|tle").split("|")
    w2 = T(ctx, "w2", "café|dia|ry").split("|")
    y = 560
    for ln in w1:
        c.text(720, y, ln, size=62, fill="#fff", weight="bold", anchor="start"); y += 58
    y = 900
    for ln in w2:
        c.text(300, y, ln, size=62, fill="#fff", weight="bold", anchor="start"); y += 58
