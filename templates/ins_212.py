"""INS-212 — selfie with an opaque cartoon cat face (mask212 master) covering the head, pastel stars around, and a
white speech bubble '귀여워..!!!' by the hand.  Page 14, photos: 1.  Requires master mask212.
The mask is scaled and placed from the measured head (rule 08: new photos get their own placement).
"""
from components import deco, ui
from templates._assets import require
from templates._common import T, face_box

META = {"id": "INS-212", "photos": 1, "assets": ["mask212"], "family": "face-mask", "photo_notes": "one selfie; mask sized from the measured head"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 1520, focus=(0.5, 0.3))
    fx, fy, fw, fh = face_box(ctx)
    cx, cy = fx * 1200, fy * 1600
    w = fw * 1200 * 1.75
    c.image_file(require(ctx, "mask212", "round cat face mask"), cx - w / 2, cy - w * 0.55, w, None, layer="fg")
    for (x, y, r, col) in ((80, 180, 18, "#F6A3C9"), (200, 110, 14, "#FFFFFF"), (520, 60, 20, "#F6A3C9"), (1090, 110, 18, "#FFFFFF"), (960, 300, 16, "#F6A3C9"), (1100, 460, 18, "#FFFFFF"), (130, 640, 22, "#F6A3C9"), (1040, 700, 14, "#FFFFFF")):
        deco.star(c, x, y, r, col, inner=0.5)
    ui.speech_cloud(c, 760, 560, 260, 110, T(ctx, "kr", "귀여워..!!!"), size=26, font="kr", stroke="none", tail_to=(720, 700))
