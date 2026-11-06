"""INS-049 — iOS photo picker: header '1 Photo Selected / ➤ Location Is Included' with thumbnail + 'Options ›',
× close; a big selected photo (blue check, white heart) with two neighbours peeking in from both edges.
Page 3, photos: 3.  Generated-asset dependencies: none.
"""
from components import ui

META = {"id": "INS-049", "photos": 3, "assets": [], "family": "ui-picker",
        "photo_notes": "3 photos: #1 selected centre (portrait), #2 left edge, #3 right edge"}


def build(c, ctx):
    c.bg = "#EFEFEA"
    c.rect(0, 0, 1200, 360, "#F6F6F2", layer="bg")
    c.photo_rect(0, 60, 60, 170, 190, rx=10, focus=(0.5, 0.3))
    c.text(260, 100, "1 Photo Selected", size=32, font="ui", fill="#111", weight="bold")
    c.text(260, 146, "➤ Location Is Included", size=28, font="ui", fill="#8E8E93")
    c.rect(260, 190, 240, 90, "#F6F6F2", layer="ui", rx=16, stroke="#D8D8D3", stroke_w=2)
    c.text(380, 248, "Options ›", size=30, font="ui", fill="#111", anchor="middle")
    ui.icon_close(c, 1110, 100, 32, fill="#D9D9D4", mark="#555", opacity=1)
    # carousel
    c.photo_rect(1, -620, 410, 800, 1080, rx=18, focus=(0.7, 0.35))
    c.photo_rect(2, 1020, 410, 800, 1080, rx=18, focus=(0.3, 0.35))
    c.photo_rect(0, 200, 410, 800, 1080, rx=18, focus=(0.5, 0.35))
    c.circle(90, 1420, 30, "none", layer="ui", stroke="#fff", stroke_w=4)
    c.circle(1110, 1420, 30, "none", layer="ui", stroke="#fff", stroke_w=4)
    ui.icon_heart(c, 290, 1424, 16, fill="#fff", layer="ui")
    ui.icon_check_circle(c, 940, 1420, 30)
