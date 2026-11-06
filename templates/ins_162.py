"""INS-162 — close selfie with three halftone-dotted white '?' above the head, small black stars scattered, and
'#inmyfeelings' in white (hashtag thin, word bold) across the chest; cream border.  Page 11, photos: 1.
Generated-asset dependencies: none.
"""
from components import deco
from templates._common import T, face_box

META = {"id": "INS-162", "photos": 1, "assets": [], "family": "face-stickers", "photo_notes": "one close selfie"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 60, 40, 1080, 1520, focus=(0.5, 0.35))
    fx, fy, fw, fh = face_box(ctx)
    cx, top = fx * 1200, (fy - fh / 2) * 1600
    deco.dotted_glyph(c, cx - 260, top - 20, "?", 230, rotate=-8, anchor="middle")
    deco.dotted_glyph(c, cx, top - 50, "?", 300, rotate=3, anchor="middle")
    deco.dotted_glyph(c, cx + 240, top - 20, "?", 220, rotate=10, anchor="middle")
    avoid = ((fx - fw / 2) * 1200 - 60, top - 60, fw * 1200 + 120, fh * 1600 + 120)
    deco.scatter_stars(c, (80, 60, 1040, 1480), 12, (10, 22), "#111", seed=4, avoid=avoid)
    tag = T(ctx, "tag", "#inmyfeelings")
    c.text(cx - 20, 1330, tag[:5], size=100, font="sans", fill="#fff", anchor="end")
    c.text(cx - 20, 1330, tag[5:], size=100, font="sans", fill="#fff", weight="bold")
