"""INS-138 — three photo bands (three_band master): the SAME photo mapped into the hand-held phone screen (top)
and into the pink flip-phone screen (middle); a white star with a tiny photo in it top-left, a '21:32 · date'
lock-screen time over the top screen, a now-playing pill and '©year' over the bottom band, grey dots.
Page 10, photos: 2 (the first is used twice).  Requires three_band + three_band_138_screens.json.
"""
import json

from components import deco, ui
from templates._assets import by_variant, require, variant_file
from templates._common import T
from templates._text import AssetMissing

META = {"id": "INS-138", "photos": 2, "assets": ["three_band", "G23:optional"], "family": "carrier-phone", "photo_notes": "#1 portrait for both screens, #2 tiny star photo"}


def build(c, ctx):
    bg = require(ctx, "three_band", "three bands: phone in hand, plush toys with flip phone, red charm")
    scr = variant_file(ctx, "three_band_138_screens.json")
    if not scr.exists():
        raise AssetMissing("three_band_138_screens.json missing - run scripts/chroma_masters.py")
    quads = json.loads(scr.read_text())
    c.image_file(bg, 0, 0, 1200, 1600, layer="bg")
    for q in quads[:2]:
        c.photo_quad(0, [(x * 1200, y * 1600) for x, y in q], focus=(0.5, 0.3))
    d = ctx["date"]
    top = quads[0]
    tx, ty = top[0][0] * 1200 + 40, top[0][1] * 1600 + 70
    c.text(tx, ty, T(ctx, "time", "21:32"), size=40, font="ui", fill="#fff", weight="300")
    c.text(tx, ty + 30, d.strftime("%B %d · %A"), size=16, font="ui", fill="#fff")
    deco.star(c, 90, 90, 80, "#fff", inner=0.5)
    c.photo_rect(1, 60, 60, 60, 60, focus=(0.5, 0.3), stroke="#F7A4C8", stroke_w=2)
    ui.now_playing_pill(c, 60, 1180, 150, 44, T(ctx, "song", "My day"), "Radio")
    light = by_variant(ctx, False, True, False)  # the cream scene needs dark ink
    c.text(1120, 1230, f"©{d.year}", size=20, font="ui", fill="#6B5A45" if light else "#fff", anchor="end")
    for (x, y, r) in ((80, 1140, 16), (60, 1290, 14), (1120, 1400, 16), (960, 1300, 10)):
        c.circle(x, y, r, "rgba(120,100,80,0.28)" if light else "rgba(255,255,255,0.35)", layer="deco")
