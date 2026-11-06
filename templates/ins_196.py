"""INS-196 — dark photo-picker sheet: three rounded photos stacked (first two with blue checks, white hearts), a
vertical '3 Photos Selected' label on the right rail and ☕ ★ 🎀 ♪ icons on the left rail.  Page 13, photos: 3.
Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T

META = {"id": "INS-196", "photos": 3, "assets": [], "family": "ui-picker", "photo_notes": "3 photos"}


def build(c, ctx):
    c.bg = "#1C1C1E"
    c.rect(0, 0, 1200, 1600, "#2A2A2C", layer="bg")
    c.rect(1050, 0, 150, 1600, "#1C1C1E", layer="bg")
    xs = [(170, 20, 820, 500), (170, 560, 820, 500), (170, 1100, 820, 500)]
    for k, (x, y, w, h) in enumerate(xs):
        c.photo_rect(k, x, y, w, h, rx=26, focus=(0.5, 0.35))
        ui.icon_heart(c, x + 44, y + 44, 14, fill="#fff", layer="ui")
        if k < 2:
            ui.icon_check_circle(c, x + 44, y + h - 44, 24)
    c.text(1125, 800, T(ctx, "label", "3 Photos Selected"), size=34, font="ui", fill="#fff", anchor="middle", rotate=90, weight="600")
    for k, ic in enumerate(("☕", "★", "🎀", "♪")):
        c.text(90, 1230 + k * 70, ic, size=40, font="emoji", fill="#fff", anchor="middle", layer="ui")
