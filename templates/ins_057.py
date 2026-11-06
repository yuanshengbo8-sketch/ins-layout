"""INS-057 — two stacked landscape photos; 'hello' in big pink bold over the right of the top photo, 'nov' at the
left edge and 'ember' lower-right of the bottom photo; a tiny pink camera + polaroid sticker at the seam.
Page 4, photos: 2.  Generated-asset dependencies: none.
"""
from templates._common import T

META = {"id": "INS-057", "photos": 2, "assets": [], "family": "big-words", "photo_notes": "2 photos, landscape-ish"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 60, 1200, 720, focus=(0.5, 0.4))
    c.photo_rect(1, 0, 810, 1200, 740, focus=(0.5, 0.35))
    pink = "#F9B6D2"
    c.text(1140, 540, T(ctx, "w1", "hello"), size=210, fill=pink, weight="bold", anchor="end")
    c.text(-10, 1130, T(ctx, "w2", "nov"), size=200, fill=pink, weight="bold")
    c.text(1190, 1370, T(ctx, "w3", "ember"), size=200, fill=pink, weight="bold", anchor="end")
    # camera + polaroid stickers
    c.rect(90, 790, 90, 64, "#F7A4C8", rx=12, layer="deco"); c.circle(135, 822, 20, "#fff", layer="deco"); c.circle(135, 822, 11, "#F7A4C8", layer="deco")
    c.rect(100, 880, 80, 96, "#fff", layer="deco", rotate=-8, stroke="#DDD"); c.photo_rect(0, 108, 888, 64, 60, rotate=-8, layer="deco", focus=(0.5, 0.3))
