"""INS-144 — portrait with a small light mini-player card top-left (cover, 'Croissant Radio', progress, ◀◀ ▮▮ ▶▶),
a white earphone cable from the card up to two buds beside the eyes, a thin star halo over the head and two music
notes right.  Page 10, photos: 1.  Album art: G23 master if present, else native cover.
"""
from components import deco, ui
from templates._common import T, face_box
from templates._assets import cover_art

META = {"id": "INS-144", "photos": 1, "assets": ["G23:optional"], "family": "ui-music", "photo_notes": "one portrait; buds and halo follow the measured head"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 60, 1200, 1480, focus=(0.5, 0.3))
    fx, fy, fw, fh = face_box(ctx)
    cx, cy = fx * 1200, fy * 1600
    r = fw * 1200 / 2
    # halo of small stars above the head
    for k in range(7):
        import math
        a = math.pi * (0.15 + 0.7 * k / 6)
        deco.star(c, cx - r * 1.1 * math.cos(a), (fy - fh / 2) * 1600 - 10 - r * 0.25 * math.sin(a), 11, "#fff", inner=0.5)
    # mini player card
    x, y, w, h = 90, 300, 300, 330
    fid = c.drop_shadow_filter(0, 4, 10, "rgba(0,0,0,0.25)")
    c.rect(x, y, w, h, "rgba(245,245,245,0.96)", rx=16, layer="ui", extra=f' filter="url(#{fid})"')
    cover_art(c, ctx, x + 40, y + 24, 220, variant="mint")
    c.text(x + w / 2, y + 272, T(ctx, "title", "Croissant Radio"), size=20, font="ui", fill="#111", weight="bold", anchor="middle", layer="ui")
    c.text(x + w / 2, y + 294, T(ctx, "sub", "a little daydream"), size=14, font="ui", fill="#777", anchor="middle", layer="ui")
    c.line(x + 30, y + 310, x + w - 30, y + 310, "#D5D5D5", 3, layer="ui", cap="round"); c.line(x + 30, y + 310, x + 110, y + 310, "#555", 3, layer="ui", cap="round")
    # cable from card to the ears
    for sx in (-1, 1):
        ex, ey = cx + sx * (r + 6), cy - fh * 1600 * 0.05
        c.circle(ex, ey, 14, "#fff", layer="deco")
        deco.earphone_cable(c, [(ex, ey + 12), (cx + sx * 40, cy + fh * 1600 * 0.7), (x + w / 2, y + h + 40), (x + w / 2, y + h)], stroke="#fff", w=5, buds=False)
    c.text(1040, 520, "♪", size=56, font="sans", fill="#fff"); c.text(1110, 600, "♪", size=56, font="sans", fill="#fff")
    deco.star(c, 1000, 440, 10, "#fff", inner=0.5)
