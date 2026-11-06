"""INS-139 — grey page with a white ticket (TICKET, ☐ 01/11/2026 · 10:00-15:00, ◎ My favourite place, the photo, a
dashed tear line with side notches, 'My Love' stub), a grey pill 'ఠ(๑˃ᴗ˂)ఠ My life! ×' at the top and white outline stars.
Page 10, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco, ui
from templates._common import T

META = {"id": "INS-139", "photos": 1, "assets": [], "family": "ui-ticket", "photo_notes": "one portrait photo"}


def build(c, ctx):
    c.bg = "#BDBDBD"
    d = ctx["date"]
    ui.pill(c, 330, 20, T(ctx, "top", "ఠ(๑˃ᴗ˂)ఠ My life!      ×"), size=24, fill="#A9A9A9", color="#fff", pad=40, h=70)
    x, y, w, h = 90, 230, 1020, 1300
    ny = ui.ticket(c, x, y, w, h, notch_y=y + 1030, layer="bg")
    c.text(x + 50, y + 100, "TICKET", size=38, font="ui", fill="#111", weight="bold", layer="ui")
    c.text(x + 50, y + 150, f"☐ {d.strftime('%d/%m/%Y')} · {T(ctx, 'hours', '10:00–15:00')}", size=22, font="ui", fill="#777", layer="ui")
    c.text(x + 50, y + 192, f"◎ {T(ctx, 'place', 'My favourite place')}", size=22, font="ui", fill="#777", layer="ui")
    c.photo_rect(0, x + 50, y + 240, w - 100, 720, rx=18, focus=(0.5, 0.35))
    c.rect(x, y + 1120, w, 1300 - 1120, "#F1F1F1", layer="bg")
    c.text(x + w / 2, y + 1215, T(ctx, "stub", "My Love"), size=26, font="ui", fill="#555", anchor="middle", weight="bold", layer="ui")
    for (sx, sy, r) in ((600, 140, 16), (80, 540, 18), (1120, 500, 18), (160, 890, 16), (1080, 1010, 18), (460, 1200, 16)):
        deco.star(c, sx, sy, r, "none", stroke="#fff", w=3, inner=0.5)
