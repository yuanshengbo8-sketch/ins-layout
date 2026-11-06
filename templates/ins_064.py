"""INS-064 — leather / laptop / crochet scene (G15 master) with a vertical photo-booth strip of four portraits on the
right, a blue 'a little photo diary' bubble and a white 'Things I learned' input with send arrow.
Page 4, photos: 4.  Requires master G15.
"""
from components import ui
from templates._assets import require
from templates._common import T

META = {"id": "INS-064", "photos": 4, "assets": ["G15"], "family": "carrier-strip", "photo_notes": "4 portraits for the strip"}


def build(c, ctx):
    c.image_file(require(ctx, "G15", "brown leather, closed laptop, crochet swatch, earphone cable, glasses"), 0, 0, 1200, 1600, layer="bg")
    x, y, w = 985, 300, 120
    c.rect(x - 6, y - 6, w + 12, 4 * 150 + 12, "#fff", layer="photos")
    for k in range(4):
        c.photo_rect(k, x, y + k * 150, w, 140, focus=(0.5, 0.3))
    ui.bubble(c, 630, 890, 350, 70, T(ctx, "b1", "a little photo diary"), size=26, tail="right", align="center")
    ui.input_field(c, 380, 985, 630, 84, T(ctx, "b2", "Things I learned"), size=30, caret=True)
