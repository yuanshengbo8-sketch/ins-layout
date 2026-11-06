"""INS-164 — full photo with a white 'New Message' compose card lower-right ('To:' line holding the caption,
blue send arrow, +).  Page 11, photos: 1.  Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T

META = {"id": "INS-164", "photos": 1, "assets": [], "family": "ui-message", "photo_notes": "one portrait photo"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 1520, focus=(0.5, 0.3))
    x, y, w, h = 350, 960, 580, 230
    ui.ios_card(c, x, y, w, h, rx=8, shadow=True)
    c.text(x + 28, y + 60, "New Message", size=40, font="ui", fill="#111", weight="bold", layer="ui")
    ui.icon_send_arrow(c, x + w - 44, y + 44, 24, fill="#B5B5B5")
    c.line(x, y + 90, x + w, y + 90, "#E5E5EA", 2, layer="ui")
    c.text(x + 28, y + 130, "To:", size=18, font="ui", fill="#8E8E93", layer="ui")
    c.text(x + 72, y + 130, T(ctx, "l1", "changing so much that every year you feel"), size=18, font="ui", fill="#111", layer="ui")
    c.text(x + 72, y + 165, T(ctx, "l2", "like a completely different person"), size=18, font="ui", fill="#111", layer="ui")
    c.line(x + 72 + 420, y + 150, x + 72 + 420, y + 176, "#111", 2, layer="ui")
    ui.icon_plus_circle(c, x + w - 40, y + 130, 14, fill="#F2F2F7", stroke_col="#3A7BD5")
