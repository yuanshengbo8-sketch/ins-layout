"""INS-171 — café portrait with two small white serif labels 'coffee' and '& croissant' pointing at the table items with
a thin curved line, plus a tiny italic note 'a little morning ritual'.  Page 12, photos: 1.
Generated-asset dependencies: none.
"""
from components import deco
from templates._common import T

META = {"id": "INS-171", "photos": 1, "assets": [], "family": "caption-notes", "photo_notes": "one café portrait with cup/food in the lower part"}


def build(c, ctx):
    c.photo_full(0, focus=(0.5, 0.35))
    # label anchors: --text l1x= l1y= l2x= l2y= (canvas px) place each label just above its object
    l1x, l1y = float(T(ctx, "l1x", 240)), float(T(ctx, "l1y", 1440))
    l2x, l2y = float(T(ctx, "l2x", 850)), float(T(ctx, "l2y", 1410))
    c.text(l1x, l1y, T(ctx, "l1", "coffee"), size=40, font="serif", fill="#fff", anchor="middle")
    c.text(l2x, l2y, T(ctx, "l2", "& croissant"), size=40, font="serif", fill="#fff", anchor="middle")
    deco.hand_arrow(c, l2x + 30, l2y + 15, l2x, l2y + 70, stroke="#fff", w=2, curve=0.3, head=8)
    c.text(float(T(ctx, "l3x", 900)), float(T(ctx, "l3y", 1520)), T(ctx, "l3", "a little morning ritual"), size=18, font="serif", fill="#fff", italic=True, anchor="middle")
