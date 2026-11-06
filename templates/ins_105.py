"""INS-105 — photo with a white month calendar card over it ('‹ 2026', 'November', grid), three tilted photo
cards scattered on the calendar, a round 'SNACK' label, an iced-coffee sticker right and a sneaker sticker
bottom-left (both G46).  Page 7, photos: 4.  Requires master G46.
"""
from components import ui
from templates._assets import require
from templates._common import month_name

META = {"id": "INS-105", "photos": 4, "assets": ["G46"], "family": "ui-calendar", "photo_notes": "4 photos: #1 background, #2-#4 small cards"}


def build(c, ctx):
    c.photo_full(0, focus=(0.5, 0.25))
    d = ctx["date"]
    x, y, w, h = 150, 330, 900, 770
    ui.ios_card(c, x, y, w, h, rx=28)
    c.text(x + 30, y + 60, f"‹ {d.year}", size=30, font="ui", fill="#E0245E", layer="ui")
    c.text(x + w - 30, y + 60, "▭  ⌕  +", size=26, font="ui", fill="#E0245E", anchor="end", layer="ui")
    c.text(x + 40, y + 140, month_name(d), size=56, font="ui", fill="#111", weight="bold", layer="ui")
    ui.month_grid(c, x + 30, y + 200, w - 60, d.year, d.month, size=34, row_h=92, highlight={d.day}, highlight_fill="#E0245E")
    c.circle(x + 300, y + 330, 95, "#D8D0C0", layer="deco"); c.rect(x + 255, y + 318, 90, 24, "#C9C0B0", layer="deco", rotate=-15)
    c.text(x + 300, y + 338, "SNACK", size=18, font="sans", fill="#5A5048", anchor="middle", layer="deco")
    c.photo_rect(1, 110, 560, 220, 270, rotate=-8, stroke="#fff", stroke_w=14, focus=(0.5, 0.3), shadow=(10, 0, 6, 0.25))
    c.photo_rect(2, 700, 460, 220, 260, rotate=6, stroke="#fff", stroke_w=14, focus=(0.5, 0.3), shadow=(10, 0, 6, 0.25))
    c.photo_rect(3, 440, 770, 220, 270, rotate=-5, stroke="#fff", stroke_w=14, focus=(0.5, 0.3), shadow=(10, 0, 6, 0.25))
    c.photo_rect(1, 780, 1060, 180, 240, rotate=10, stroke="#fff", stroke_w=12, focus=(0.5, 0.3), shadow=(10, 0, 6, 0.25))
    c.image_file(require(ctx, "G46_iced", "iced coffee sticker"), 960, 850, 140, None, layer="deco", rotate=12)
    c.image_file(require(ctx, "G46_sneakers", "white sneaker sticker"), 60, 1040, 260, None, layer="deco", rotate=-10)
