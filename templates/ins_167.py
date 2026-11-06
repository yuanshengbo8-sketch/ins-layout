"""INS-167 — sunny full photo with white stars, a blue italic serif 'blue autumn' top-right, '( soft energy )' mid-right,
and a white Korean note box '"넌 늘 웃더라."' lower-left.  Page 11, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco
from templates._common import T

META = {"id": "INS-167", "photos": 1, "assets": [], "family": "sticker-stars", "photo_notes": "one outdoor portrait"}


def build(c, ctx):
    c.photo_full(0, focus=(0.5, 0.35))
    for (x, y, r) in ((360, 760, 38), (1000, 620, 38), (600, 1340, 40), (1040, 1480, 24)):
        deco.star(c, x, y, r, "#fff", inner=0.48)
    c.text(1120, 250, T(ctx, "t1", "blue autumn"), size=46, font="serif", fill="#2F7BE8", italic=True, weight="bold", opacity=0.9, anchor="end")
    c.text(960, 1010, T(ctx, "t2", "( soft energy )"), size=36, font="serif", fill="#2F7BE8", italic=True, weight="bold", anchor="middle")
    c.rect(130, 1220, 400, 100, "#fff", rx=6, layer="ui", opacity=0.95)
    c.text(330, 1284, T(ctx, "kr", "“넌 늘 웃더라.”"), size=34, font="kr", fill="#111", anchor="middle", layer="ui")
