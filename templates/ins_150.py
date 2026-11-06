"""INS-150 — full photo with glossy blue 3D question marks of several sizes around the figure and a white
hand-written note box 'I thought that I was dreaming / when you said you love me.' bottom-right.
Page 11, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco
from templates._common import T

META = {"id": "INS-150", "photos": 1, "assets": [], "family": "face-stickers", "photo_notes": "one photo, subject centred"}


def build(c, ctx):
    c.photo_full(0, focus=(0.5, 0.4))
    for (x, y, s, r) in ((190, 180, 260, -12), (1080, 300, 110, 8), (1000, 440, 190, -6), (240, 1110, 230, 10), (1060, 1110, 80, -4), (1110, 1230, 140, 6)):
        deco.question_3d(c, x, y, s, rotate=r)
    x, y, w, h = 560, 1340, 560, 130
    c.rect(x, y, w, h, "#fff", layer="ui", stroke="#111", stroke_w=2)
    c.text(x + w / 2, y + 52, T(ctx, "l1", "I thought that I was dreaming"), size=26, font="mono", fill="#111", anchor="middle", layer="ui")
    c.text(x + w / 2, y + 96, T(ctx, "l2", "when you said you love me."), size=26, font="mono", fill="#111", anchor="middle", layer="ui")
