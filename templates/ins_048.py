"""INS-048 — iMessage thread: 'Today 4:16 PM', three rounded photo bubbles cascading down-right with a pink
heart tapback on the first, 'Read 4:16 PM', then the + / iMessage input row and home bar.
Page 2, photos: 3.  Generated-asset dependencies: none.
"""
from components import ui, deco
from templates._common import T

META = {"id": "INS-048", "photos": 3, "assets": [], "family": "ui-message",
        "photo_notes": "3 photos; #1 portrait top-right, #2 landscape middle, #3 portrait bottom"}


def build(c, ctx):
    c.bg = "#F4F4F4"
    c.rect(60, 0, 1080, 1600, "#FFFFFF", layer="bg")
    tm = T(ctx, "time", "4:16 PM")
    c.text(600, 100, f"Today {tm}", size=24, font="ui", fill="#8E8E93", anchor="middle", weight="600")
    c.photo_rect(0, 400, 110, 520, 420, rx=36, focus=(0.5, 0.3), shadow=(10, 0, 6, 0.12))
    # tapback heart
    c.circle(420, 118, 30, "#fff", layer="ui", stroke="#E5E5EA", stroke_w=2)
    deco.heart(c, 420, 118, 14, "#FF2D55", layer="ui")
    c.photo_rect(1, 520, 460, 520, 400, rx=36, focus=(0.5, 0.35), shadow=(10, 0, 6, 0.12))
    c.photo_rect(2, 410, 800, 520, 430, rx=36, focus=(0.5, 0.3), shadow=(10, 0, 6, 0.12))
    c.text(1040, 1300, f"Read {tm}", size=22, font="ui", fill="#8E8E93", anchor="end", weight="600")
    ui.icon_plus_circle(c, 150, 1410, 36)
    ui.input_field(c, 230, 1372, 830, 76, "iMessage", placeholder=True, send=False, size=30)
    c.path("M1010 1395 V1425 M1022 1402 V1418 M1034 1392 V1428 M1046 1400 V1420", stroke="#E0245E", w=4, layer="ui")
    c.rect(460, 1512, 280, 10, "#111", rx=5, layer="ui")
