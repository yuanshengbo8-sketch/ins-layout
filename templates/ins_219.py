"""INS-219 — breakfast table (G12 master: wooden table, upright phone with black screen, fork with bitten
croissant front-right, coffee + berries behind).  The photo is perspective-mapped into the phone screen with
'Yes!' in white bold over it; the croissant on the fork is re-composited IN FRONT of the screen.
Page 2, photos: 1.  REQUIRES masters: G12 + G12_screen.json (4 screen corners) + G12_fg.png (croissant/fork cut-out).
"""
import json

from templates._assets import require, variant_file
from templates._common import T

META = {"id": "INS-219", "photos": 1, "assets": ["G12", "G12_screen", "G12_fg"], "family": "carrier-phone",
        "photo_notes": "one portrait photo; the subject's mouth should sit near the croissant (right side of the screen)"}


def build(c, ctx):
    bg = require(ctx, "G12", "breakfast wooden table, upright phone with black screen, fork + bitten croissant, coffee")
    scr = variant_file(ctx, "G12_screen.json")
    fg = variant_file(ctx, "G12_fg.png")
    if not scr.exists() or not fg.exists():
        from templates._text import AssetMissing
        raise AssetMissing("G12_screen.json / G12_fg.png missing - run scripts/chroma_masters.py")
    quad = [(x * 1200, y * 1600) for x, y in json.loads(scr.read_text())]  # normalised corners -> canvas px
    c.image_file(bg, 0, 0, 1200, 1600, layer="bg")
    c.photo_quad(0, quad, focus=(0.5, 0.4))
    cx = sum(p[0] for p in quad) / 4; cy = sum(p[1] for p in quad) / 4
    c.text(cx + 120, cy - 80, T(ctx, "word", "Yes!"), size=70, fill="#fff", weight="bold", anchor="middle")
    c.image_file(fg, 0, 0, 1200, 1600, layer="fg")
