"""INS-163 — two stacked photos; the top one carries a faint camera grid and 0.5 / 1.2× zoom labels on the left edge;
over the seam a blue bubble 'the real' and a white input field 'luxuries in life' with a send arrow.
Page 11, photos: 2.  Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T

META = {"id": "INS-163", "photos": 2, "assets": [], "family": "ui-message", "photo_notes": "2 photos"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 780, focus=(0.5, 0.3))
    c.photo_rect(1, 0, 830, 1200, 730, focus=(0.5, 0.35))
    for k in (1, 2):
        c.line(1200 * k / 3, 40, 1200 * k / 3, 820, "rgba(255,255,255,0.5)", 1.5, layer="fg")
        c.line(0, 40 + 780 * k / 3, 1200, 40 + 780 * k / 3, "rgba(255,255,255,0.5)", 1.5, layer="fg")
    c.rect(28, 360, 50, 190, "rgba(0,0,0,0.5)", rx=25, layer="fg")
    c.text(53, 410, "0.5", size=20, font="ui", fill="#fff", anchor="middle", rotate=90, layer="fg")
    c.text(53, 500, "1.2×", size=20, font="ui", fill="#FFD60A", anchor="middle", rotate=90, weight="bold", layer="fg")
    ui.bubble(c, 300, 690, 170, 70, T(ctx, "b1", "the real"), size=30, tail="left", align="center")
    ui.input_field(c, 370, 770, 700, 80, T(ctx, "b2", "luxuries in life"), size=32, caret=True)
