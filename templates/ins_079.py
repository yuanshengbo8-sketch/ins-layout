"""INS-079 — Chinese dinner table (G11 master): the photo is perspective-mapped into the pink-framed phone lying on
the plate, 'Grab a bite' in white serif over the plate, '@little.table' bottom-right.  Page 5, photos: 1.
Requires master G11 + G11_screen.json (4 screen corners, normalised).
"""
import json

from templates._assets import require, variant_file
from templates._common import T
from templates._text import AssetMissing

META = {"id": "INS-079", "photos": 1, "assets": ["G11", "G11_screen"], "family": "carrier-phone", "photo_notes": "one landscape-ish photo for the phone screen"}


def build(c, ctx):
    bg = require(ctx, "G11", "dinner table with a phone on a plate")
    scr = variant_file(ctx, "G11_screen.json")
    if not scr.exists():
        raise AssetMissing("G11_screen.json (screen corners) missing - run scripts/chroma_masters.py")
    quad = [(x * 1200, y * 1600) for x, y in json.loads(scr.read_text())]
    c.image_file(bg, 0, 0, 1200, 1600, layer="bg")
    c.photo_quad(0, quad, focus=(0.5, 0.4))
    c.text(600, 1020, T(ctx, "title", "Grab a bite"), size=64, font="serif", fill="#fff", anchor="middle", extra=' style="filter:drop-shadow(0 2px 6px rgba(0,0,0,.6))"')
    c.text(1120, 1480, T(ctx, "handle", "@little.table"), size=22, font="sans", fill="#fff", anchor="end", extra=' style="filter:drop-shadow(0 2px 6px rgba(0,0,0,.6))"')
