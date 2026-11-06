"""INS-211 — landscape photo window on a cream page; a manga eye strip (G24) covers the eyes in a cream-edged band,
'my little mood' search pill top-left, white arrows, grey stars and a '(¯∧¯)' box.  Page 14, photos: 1.
Requires master G24 (eye strip).  The strip is sized from the measured head.
"""
from components import deco, ui
from templates._assets import require
from templates._common import T, face_box

META = {"id": "INS-211", "photos": 1, "assets": ["G24"], "family": "face-mask", "photo_notes": "one portrait; the strip follows the measured head"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 330, 1200, 900, focus=(0.5, 0.3))
    fx, fy, fw, fh = face_box(ctx)
    # photo window crop keeps head centred: approximate head position inside the window
    cx = fx * 1200; ey = 330 + 900 * 0.42
    sw = max(500, fw * 1200 * 2.0)
    sh = sw * 0.52
    c.rect(cx - sw / 2, ey - sh / 2 - 16, sw, 16, "#EEECE7", layer="ui"); c.rect(cx - sw / 2, ey + sh / 2, sw, 16, "#EEECE7", layer="ui")
    c.image_file(require(ctx, "G24_eyes", "manga eye strip"), cx - sw / 2, ey - sh / 2, sw, sh, layer="ui")
    ui.pill(c, 40, 400, T(ctx, "mood", "my little mood") + "          ⌞", size=20, fill="#F2F2F2", color="#555", pad=20, h=52)
    deco.big_arrow(c, 230, 620, 180, fill="#fff")
    c.path("M1000 1090 L900 1010 M900 1010 L910 1050 M900 1010 L940 1005", stroke="#fff", w=14, layer="deco")
    for (x, y, r) in ((60, 560, 26), (120, 790, 20), (320, 1070, 22), (1120, 380, 24), (1090, 560, 20), (1130, 1150, 20)):
        deco.star(c, x, y, r, "#D9D9D9", inner=0.5)
    c.rect(1000, 1060, 100, 60, "#fff", layer="ui", stroke="#555"); c.text(1050, 1100, "(¯∧¯)", size=22, font="sans", fill="#333", anchor="middle", layer="ui")
