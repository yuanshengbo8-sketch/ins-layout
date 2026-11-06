"""INS-070 — day-planner page: week strip (M..S, today circled), 'Sunday — 1 Nov 2026', hour rail 06:00-17:00 with
light grey event blocks; a collage of three photos sits over 07:00-14:00 and a note 'coffee with bestie ☕🌟' at 15:00.
The latte + lip-gloss sticker (G49) is optional: without it the collage stays, the sticker slot is skipped and recorded.
Page 1, photos: 3.
"""
from components import ui
from templates._common import T, date_long, week_of
from templates._assets import master

META = {"id": "INS-070", "photos": 3, "assets": ["G49:optional"], "family": "ui-schedule", "photo_notes": "3 photos: two portraits + one small square"}


def build(c, ctx):
    c.bg = "#F4F3EF"
    d = ctx["date"]
    nums, today = week_of(d)
    c.rect(0, 0, 1200, 300, "#F4F3EF", layer="bg")
    ui.week_strip(c, 60, 90, 1080, ["M", "T", "W", "T", "F", "S", "S"], nums, today, size=34, head_size=20)
    c.line(60, 230, 1140, 230, "#DDD", 2)
    c.text(600, 285, date_long(d), size=32, font="sans", fill="#111", anchor="middle", weight="bold")
    c.line(60, 320, 1140, 320, "#DDD", 2)
    hours = list(range(6, 18))
    ui.hour_rail(c, 130, 360, hours, 98, size=22, line_x1=150, line_x2=1140)
    # event blocks
    c.rect(160, 400, 980, 790, "#E6E4DF", layer="bg", rx=6)
    c.rect(160, 1230, 980, 90, "#ECEAE5", layer="bg", rx=6)
    c.rect(170, 1248, 6, 54, "#C9B6A8", layer="ui")
    c.text(196, 1283, T(ctx, "note", "coffee with bestie ☕🌟"), size=26, font="ui", fill="#333", weight="bold")
    # collage
    c.photo_rect(0, 180, 430, 420, 480, focus=(0.5, 0.35), shadow=(10, 0, 6, 0.15))
    c.photo_rect(1, 660, 440, 440, 520, focus=(0.5, 0.35), shadow=(10, 0, 6, 0.15))
    c.photo_rect(2, 200, 820, 340, 300, focus=(0.5, 0.35), shadow=(10, 0, 6, 0.15))
    g = master(ctx, "G49")
    if g:
        c.image_file(g, 520, 900, 300, None, layer="deco")
    else:
        c.recipe.setdefault("substitutes", []).append({"slot": "G49", "used": "omitted (optional sticker)"})
