"""INS-038 — two phones on a wooden table (dual_phone master): one photo in each screen (perspective-mapped),
the tortoiseshell glasses re-composited in front, '♡ with you ♡' between cans and phones, '@monday' / '@weekend'
handles, a small heart by the finger-heart hands.  Page 2, photos: 2.
Requires masters dual_phone + dual_phone_038_screens.json + dual_phone_038_fg.png.
"""
import json

from components import deco
from templates._assets import by_variant, require, variant_file
from templates._common import T
from templates._text import AssetMissing

META = {"id": "INS-038", "photos": 2, "assets": ["dual_phone", "dual_phone_fg"], "family": "carrier-phone", "photo_notes": "2 portraits, one per screen"}


def build(c, ctx):
    bg = require(ctx, "dual_phone", "two phones on a wooden table")
    scr = variant_file(ctx, "dual_phone_038_screens.json")
    fg = variant_file(ctx, "dual_phone_038_fg.png")
    if not scr.exists() or not fg.exists():
        raise AssetMissing("dual_phone_038_screens.json / _fg.png missing - run scripts/chroma_masters.py")
    quads = json.loads(scr.read_text())
    c.image_file(bg, 0, 0, 1200, 1600, layer="bg")
    for i, q in enumerate(quads[:2]):
        c.photo_quad(i, [(x * 1200, y * 1600) for x, y in q], focus=(0.5, 0.35))
    c.image_file(fg, 0, 0, 1200, 1600, layer="fg")
    ink = by_variant(ctx, "#fff", "#4A3B32", "#fff")  # the marble scene is light
    c.text(600, 420, T(ctx, "title", "♡ with you ♡"), size=42, font="serif", fill=ink, anchor="middle")
    c.text(250, 1010, T(ctx, "h1", "@monday"), size=26, font="serif", fill=ink, anchor="middle", extra=' text-decoration="underline"')
    c.text(1020, 960, T(ctx, "h2", "@weekend"), size=26, font="serif", fill=ink, anchor="middle", extra=' text-decoration="underline"')
    deco.heart(c, 1030, 1270, 14, "#fff")
