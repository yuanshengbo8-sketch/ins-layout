"""INS-143 — grey page, the photo in a large rounded window, a pink ribbon bow above the head with 'O ᴗ O' eyes drawn
under it, and a top-left round app icon 📱 with 'J / Receiving a new day…'.  Page 10, photos: 1.
Generated-asset dependencies: none.
"""
from components import deco
from templates._common import T, face_box

META = {"id": "INS-143", "photos": 1, "assets": [], "family": "face-stickers", "photo_notes": "one portrait; bow sits above the measured head"}


def build(c, ctx):
    c.bg = "#A6A6A6"
    c.circle(130, 100, 80, "#fff", layer="ui"); c.text(130, 122, "📱", size=60, font="emoji", anchor="middle", layer="ui")
    c.text(260, 90, T(ctx, "app", "J"), size=56, font="ui", fill="#fff", weight="bold", layer="ui")
    c.text(260, 150, T(ctx, "sub", "Receiving a new day…"), size=34, font="ui", fill="#fff", layer="ui")
    c.photo_rect(0, 80, 280, 1040, 1240, rx=40, focus=(0.5, 0.3))
    fx, fy, fw, fh = face_box(ctx)
    cx, top = fx * 1200, (fy - fh / 2) * 1600
    deco.bow(c, cx, top - 20, 70)
    c.text(cx, top + 110, "O ᴗ O", size=56, font="sans", fill="#fff", anchor="middle", weight="bold", stroke="#fff", stroke_w=2)
