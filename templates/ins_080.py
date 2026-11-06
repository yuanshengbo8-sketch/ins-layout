"""INS-080 — 'November' planner: bold month name, week strip (today circled in red), hour rail 09:00-14:00 with a
yellow note 'slow morning rituals & breakfast for the skin', a pink sticky 'morning SKIN CARE', a 3-photo collage
and the pancake sticker (G50).  Page 6, photos: 3.  Requires master G50.
"""
from components import ui
from templates._assets import require
from templates._common import T, month_name, week_of

META = {"id": "INS-080", "photos": 3, "assets": ["G50"], "family": "ui-schedule", "photo_notes": "3 photos"}


def build(c, ctx):
    c.bg = "#F4F3EF"
    d = ctx["date"]; nums, today = week_of(d)
    c.text(80, 150, month_name(d), size=84, font="sans", fill="#111", weight="bold")
    ui.week_strip(c, 60, 220, 1080, ["M", "T", "W", "T", "F", "S", "S"], nums, today, size=46, head_size=22, today_fill="#E8383D")
    c.line(60, 370, 1140, 370, "#DDD", 2)
    ui.hour_rail(c, 190, 470, [9, 10, 11, 12, 13, 14], 190, size=24, line_x1=210, line_x2=1140)
    c.rect(220, 500, 920, 760, "#E9E7E2", layer="bg")
    c.rect(250, 500, 900, 90, "#F6ED9A", layer="ui"); c.rect(250, 500, 8, 90, "#D9B400", layer="ui")
    c.text(280, 557, T(ctx, "note", "slow morning rituals & breakfast for the skin"), size=28, font="ui", fill="#5A4A00", weight="bold", layer="ui")
    c.rect(1040, 590, 160, 170, "#F6A4B8", layer="deco", rotate=8)
    c.text(1120, 650, "morning", size=16, font="hand", fill="#8A2F49", anchor="middle", rotate=8, layer="deco")
    c.text(1120, 690, "SKIN CARE", size=22, font="hand", fill="#8A2F49", anchor="middle", weight="bold", rotate=8, layer="deco")
    c.photo_rect(0, 290, 650, 360, 480, focus=(0.5, 0.3))
    c.photo_rect(1, 660, 630, 480, 400, focus=(0.5, 0.3))
    c.photo_rect(2, 660, 1000, 330, 400, focus=(0.5, 0.3))
    c.image_file(require(ctx, "G50", "pancake stack sticker"), 430, 1200, 300, None, layer="deco")
