"""INS-033 — iMessage photo-attachment card on top (one photo, × close, + and emoji row, send arrow),
then a tight 3×2 photo grid below with two white hearts.  Page 2, photos: 7 (1 card + 6 grid).
Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T

META = {"id": "INS-033", "photos": 7, "assets": [], "family": "ui-message",
        "photo_notes": "7 photos: #1 goes in the message card (portrait works best), #2-#7 fill the 3x2 grid"}


def build(c, ctx):
    c.bg = "#E8E6E1"
    # message card
    cx, cy, cw, ch = 170, 70, 860, 540
    ui.ios_card(c, cx, cy, cw, ch, rx=30, shadow=False, stroke="#DCDCDC", layer="bg")
    c.photo_rect(0, cx + 20, cy + 20, cw - 40, 380, rx=22, focus=(0.5, 0.3))
    ui.icon_close(c, cx + cw - 50, cy + 50, 20, fill="#8E8E93", opacity=0.9)
    ui.icon_plus_circle(c, cx + 60, cy + 470, 30)
    c.text(cx + 120, cy + 486, T(ctx, "emoji", "🦆 💛 🌳 🥗 🩴"), size=38, font="emoji", layer="ui")
    ui.icon_send_arrow(c, cx + cw - 60, cy + 470, 30, fill="#1A5CFF")
    # grid
    ui.photo_grid(c, 0, 650, 1200, 3, 2, [1, 2, 3, 4, 5, 6], gap=6, cell_h=384, hearts={(0, 1), (0, 2)}, focus=(0.5, 0.35))
