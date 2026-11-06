"""INS-218 — selfie with an anime face band (mask218 master) laid over the eyes-to-chin region and green ':3' marks
scattered around.  Page 14, photos: 1.  Requires master mask218.  Band sized from the measured head.
"""
from templates._assets import require
from templates._common import T, face_box

META = {"id": "INS-218", "photos": 1, "assets": ["mask218"], "family": "face-mask", "photo_notes": "one front-facing selfie"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 1520, focus=(0.5, 0.3))
    fx, fy, fw, fh = face_box(ctx)
    cx, cy = fx * 1200, fy * 1600
    w = fw * 1200 * 1.55; h = w * 0.62
    c.image_file(require(ctx, "mask218", "anime face band"), cx - w / 2, cy - h * 0.42, w, h, layer="fg")
    for (x, y, s) in ((90, 150, 70), (90, 560, 48), (1030, 760, 48), (160, 820, 48), (1000, 1150, 44)):
        c.text(x, y, T(ctx, "mark", ":3"), size=s, font="sans", fill="#49E31C", weight="bold")
