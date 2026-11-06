"""INS-058 — 'Favourites' album: hero photo on top with the title and '▦ 73 items', a pink 'Ask me a question'
sticker with a white answer card top-right, then a 3×2 grid with white hearts.  Page 4, photos: 7.
Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T

META = {"id": "INS-058", "photos": 7, "assets": [], "family": "ui-album", "photo_notes": "7 photos: #1 landscape hero, #2-#7 grid"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 50, 1200, 680, focus=(0.5, 0.3))
    c.text(40, 610, T(ctx, "title", "Favourites"), size=78, font="ui", fill="#fff", weight="300")
    c.text(44, 672, T(ctx, "count", "▦ 73 items"), size=30, font="ui", fill="#fff")
    # question sticker
    c.rect(740, 220, 370, 190, "#fff", rx=18, layer="ui")
    c.rect(740, 220, 370, 60, "#FF4D8D", rx=18, layer="ui")
    c.rect(740, 250, 370, 30, "#FF4D8D", layer="ui")
    c.text(925, 262, T(ctx, "q_head", "Ask me a question"), size=26, font="ui", fill="#fff", anchor="middle", weight="600", layer="ui")
    c.text(925, 330, T(ctx, "q1", "What's your"), size=30, font="ui", fill="#111", anchor="middle", layer="ui")
    c.text(925, 372, T(ctx, "q2", "favorite color?"), size=30, font="ui", fill="#111", anchor="middle", layer="ui")
    ui.photo_grid(c, 0, 740, 1200, 3, 2, [1, 2, 3, 4, 5, 6], gap=6, cell_h=400, hearts={(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)}, focus=(0.5, 0.35))
