"""INS-191 — iMessage attachment card (photo, × close) with '+' and 'Add comment or Send' field on a pale page, then a
3×3 contact-sheet grid below (top row cropped tight, two white hearts).  Page 12, photos: 9.
Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T

META = {"id": "INS-191", "photos": 9, "assets": [], "family": "ui-message", "photo_notes": "9 photos: #1 in the card, #2-#9 in the grid (cycled)"}


def build(c, ctx):
    c.bg = "#EFEFEA"
    ui.ios_card(c, 150, 90, 900, 600, rx=28, shadow=False, stroke="#DCDCDC", layer="bg")
    c.photo_rect(0, 180, 120, 640, 440, rx=18, focus=(0.5, 0.35))
    ui.icon_close(c, 790, 160, 22, fill="#8E8E93", opacity=0.9)
    ui.icon_plus_circle(c, 60, 660, 36)
    ui.input_field(c, 180, 620, 850, 80, T(ctx, "field", "Add comment or Send"), size=32, placeholder=False, send=True)
    ui.photo_grid(c, 0, 830, 1200, 3, 3, [1, 2, 3, 4, 5, 6, 7, 8], gap=8, cell_h=250, hearts={(1, 1), (1, 2)}, focus=(0.5, 0.35))
