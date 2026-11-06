"""INS-062 — portrait on a pale page with a white iOS Calendar card over the chest (month name, week strip with today
circled, 'Sunday — 1 Nov 2026', an 'all-day ✱ NOVEMBER NOTES' event), a 🥳 emoji badge and a grey
'↗ Save this little moment' pill.  Page 4, photos: 1.  Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T, date_long, week_of, month_name

META = {"id": "INS-062", "photos": 1, "assets": [], "family": "ui-calendar", "photo_notes": "one portrait photo, head in the upper third"}


def build(c, ctx):
    c.bg = "#F3F2EE"
    c.photo_rect(0, 90, 50, 1020, 1500, focus=(0.5, 0.3))
    d = ctx["date"]
    x, y, w, h = 170, 440, 650, 300
    ui.ios_card(c, x, y, w, h, rx=16, fill="rgba(255,255,255,0.96)")
    c.text(x + 76, y + 48, month_name(d), size=26, font="ui", fill="#E0245E", layer="ui")
    c.text(x + w - 24, y + 48, "▦  ⌕  +", size=24, font="ui", fill="#E0245E", anchor="end", layer="ui")
    nums, today = week_of(d)
    ui.week_strip(c, x + 10, y + 84, w - 20, ["S", "M", "T", "W", "T", "F", "S"], [nums[6]] + nums[:6], (today + 1) % 7, size=24, head_size=16)
    c.text(x + w / 2, y + 190, date_long(d), size=22, font="ui", fill="#111", anchor="middle", weight="bold", layer="ui")
    c.line(x, y + 206, x + w, y + 206, "#E5E5EA", 2, layer="ui")
    c.text(x + 20, y + 240, "all-day", size=16, font="ui", fill="#8E8E93", layer="ui")
    c.rect(x + 110, y + 222, w - 130, 30, "#CFF1F6", layer="ui", rx=4)
    c.text(x + 122, y + 244, T(ctx, "event", "✱ NOVEMBER NOTES").upper(), size=16, font="ui", fill="#1B6F80", weight="bold", layer="ui")
    c.text(x + 20, y + 284, "09:00", size=14, font="ui", fill="#8E8E93", layer="ui")
    c.circle(x + 20, y + 20, 48, "#fff", layer="deco"); c.text(x + 20, y + 36, "🥳", size=46, font="emoji", anchor="middle", layer="deco")
    ui.pill(c, 330, 790, T(ctx, "save", "↗ Save this little moment"), size=24, fill="rgba(120,120,120,0.7)", color="#fff", pad=20, h=52)
