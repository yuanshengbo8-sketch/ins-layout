"""INS-177 — two stacked photos joined by a white earphone cable that starts as two ear-buds near the upper face and
loops down to a light-blue mini player 'Croissant Radio / Little joys · Personal playlist' lower-right.
Page 12, photos: 2.  Generated-asset dependencies: none.
"""
from components import deco, ui
from templates._common import T, face_box

META = {"id": "INS-177", "photos": 2, "assets": [], "family": "ui-music", "photo_notes": "#1 portrait (buds sit at the ears), #2 portrait"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 60, 1200, 740, focus=(0.5, 0.3))
    c.photo_rect(1, 0, 810, 1200, 750, focus=(0.5, 0.3))
    fx, fy, fw, fh = face_box(ctx)
    ex, ey = fx * 1200, (fy - 0.02) * 760 + 60
    r = fw * 1200 / 2 + 10
    for sx in (-1, 1):
        c.circle(ex + sx * r, ey, 22, "#fff", layer="deco")
        deco.earphone_cable(c, [(ex + sx * r, ey + 20), (ex + sx * (r + 40), ey + 300), (ex + sx * 30, ey + 520), (620, 900)], stroke="#fff", w=6, buds=False)
    deco.earphone_cable(c, [(620, 900), (380, 1050), (520, 1180), (700, 1130)], stroke="#fff", w=6, buds=False)
    ui.mini_player(c, 660, 1040, 520, 240, T(ctx, "title", "Croissant Radio"), T(ctx, "sub", "Little joys · Personal playlist"), fill="#A8D9EA", rx=22)
