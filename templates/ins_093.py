"""INS-093 — denim texture (G22 master, seam on the right) with a vertical strip of four photos in the middle.
Page 6, photos: 4.  Requires master G22.
"""
from templates._assets import require

META = {"id": "INS-093", "photos": 4, "assets": ["G22"], "family": "carrier-strip", "photo_notes": "4 photos, portrait"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.image_file(require(ctx, "G22", "worn blue denim with a seam"), 60, 40, 1080, 1520, layer="bg")
    for k in range(4):
        c.photo_rect(k, 465, 240 + k * 300, 270, 290, focus=(0.5, 0.3))
