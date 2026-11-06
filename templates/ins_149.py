"""INS-149 — full photo with royal-blue object tiles (G25 master cut per object: headphones, sunglasses, phone back,
camera, iced coffee) placed around the subject, blue hashtag notes and small blue stars.
Page 1, photos: 1.  Requires master G25 (split into G25_*.png).
"""
from components import deco
from templates._assets import require
from templates._common import T

META = {"id": "INS-149", "photos": 1, "assets": ["G25"], "family": "sticker-objects", "photo_notes": "one portrait with space left and right of the figure"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 1520, focus=(0.5, 0.35))
    tiles = [("G25_headphones", 60, 330, 250), ("G25_sunglasses", 980, 60, 170), ("G25_phone", 90, 1040, 160), ("G25_camera", 900, 1200, 250), ("G25_iced", 800, 1300, 160)]
    for key, x, y, w in tiles:
        c.image_file(require(ctx, key, "blue object tile"), x, y, w, None, layer="deco")
    blue = "#1B3FD6"
    c.text(300, 140, T(ctx, "t1", "#Love s3333"), size=24, font="sans", fill=blue, weight="bold")
    c.text(60, 920, T(ctx, "t2", "#Just vibing"), size=24, font="sans", fill=blue, weight="bold")
    c.text(1000, 1090, T(ctx, "t3", "#My pov."), size=24, font="sans", fill=blue, weight="bold")
    c.text(220, 1500, T(ctx, "t4", "#Just me and the moment"), size=24, font="sans", fill=blue, weight="bold")
    for (x, y) in ((620, 60), (460, 390), (960, 430), (140, 760), (420, 1200), (1090, 1500), (1020, 720)):
        deco.star(c, x, y, 12, blue, inner=0.5)
