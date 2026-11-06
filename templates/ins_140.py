"""INS-140 — selfie with scattered black stars, two tilted white captions on the right ('Glue down the chaos..',
'Frame your freedom..'), and a white comment card bottom-left (avatar, 'Keep the light and little joys.', 'Me love',
reactions, timestamp).  Page 1, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco
from templates._common import T, face_box

META = {"id": "INS-140", "photos": 1, "assets": [], "family": "sticker-caption", "photo_notes": "one selfie; stars avoid the face box"}


def build(c, ctx):
    c.photo_full(0, focus=(0.5, 0.35))
    fx, fy, fw, fh = face_box(ctx)
    avoid = ((fx - fw / 2) * 1200 - 40, (fy - fh / 2) * 1600 - 40, fw * 1200 + 80, fh * 1600 + 80)
    deco.scatter_stars(c, (30, 30, 1140, 1540), 11, (16, 30), "#111", seed=7, avoid=avoid)
    c.text(1120, 230, T(ctx, "cap1", "Glue down the chaos.."), size=26, fill="#fff", anchor="end", rotate=12, opacity=0.9, font="ui")
    c.text(1140, 300, T(ctx, "cap2", "Frame your freedom.."), size=26, fill="#fff", anchor="end", rotate=12, opacity=0.9, font="ui")
    c.text(1120, 380, T(ctx, "cap1", "Glue down the chaos.."), size=30, fill="#fff", anchor="end", rotate=8, font="ui")
    c.text(1140, 500, T(ctx, "cap2", "Frame your freedom.."), size=40, fill="#fff", anchor="end", rotate=4, weight="bold", font="ui")
    # comment card
    x, y, w, h = 90, 1310, 600, 190
    fid = c.drop_shadow_filter(0, 6, 10, "rgba(0,0,0,0.25)")
    c.rect(x, y, w, h, "#fff", rx=16, layer="ui", extra=f' filter="url(#{fid})"')
    c.circle(x + 60, y + 60, 32, "#E5E5EA", layer="ui")
    c.circle(x + 60, y + 50, 12, "#B9B9BE", layer="ui")
    c.path(f"M{x + 36} {y + 86} Q{x + 60} {y + 60} {x + 84} {y + 86}", fill="#B9B9BE", layer="ui")
    c.text(x + 110, y + 52, T(ctx, "comment", "Keep the light and little joys."), size=24, font="ui", fill="#111", weight="bold", layer="ui")
    c.text(x + 110, y + 86, T(ctx, "who", "Me love"), size=20, font="ui", fill="#555", layer="ui")
    c.text(x + 110, y + 124, "♡ · (๑˃̵ᴗ˂̵) ok!! · ♡", size=20, font="ui", fill="#555", layer="ui")
    d = ctx["date"]
    c.text(x + 110, y + 166, f"{d.isoformat()} 09:30 · updated 14:14", size=16, font="ui", fill="#AAA", layer="ui")
