"""INS-120 — white page: two small landscape photos stepping down-left, small bold notes 'cozy day..', 'moment:',
'happiness.', a magenta bold block 'i love / simple / cozy / things.' lower-right and a faint dotted speckle top-right.
Page 8, photos: 2.  Generated-asset dependencies: none.
"""
import random

from templates._common import T

META = {"id": "INS-120", "photos": 2, "assets": [], "family": "collage-notes", "photo_notes": "2 landscape photos"}


def build(c, ctx):
    c.bg = "#FFFFFF"
    rnd = random.Random(5)
    for _ in range(140):
        c.circle(870 + rnd.random() * 280, 20 + rnd.random() * 200, rnd.uniform(1, 2.5), "#B5B5B5", layer="deco")
    c.photo_rect(0, 130, 240, 540, 360, focus=(0.5, 0.35))
    c.photo_rect(1, 130, 640, 440, 260, focus=(0.5, 0.4))
    c.text(130, 210, T(ctx, "n1", "cozy day.."), size=30, font="ui", fill="#111", weight="bold")
    c.text(720, 480, T(ctx, "n2", "moment:"), size=30, font="ui", fill="#111", weight="bold")
    c.text(260, 980, T(ctx, "n3", "happiness."), size=30, font="ui", fill="#111", weight="bold")
    y = 790
    for ln in T(ctx, "big", "i love|simple|cozy|things.").split("|"):
        c.text(560, y, ln, size=92, font="sans", fill="#E8148B", weight="bold"); y += 100
