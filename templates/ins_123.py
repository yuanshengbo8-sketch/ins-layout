"""INS-123 — three photos (top wide, two below) with a top-down coffee cup sticker (G46) in the centre carrying
'YOUR / NOVEMBER / reset / GUIDE' in white and '(so you can lock it in)' beneath.  Page 9, photos: 3.
Requires master G46.
"""
from templates._assets import require
from templates._common import T, month_name

META = {"id": "INS-123", "photos": 3, "assets": ["G46"], "family": "collage-sticker", "photo_notes": "3 photos: #1 landscape top, #2 #3 portraits"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 760, focus=(0.5, 0.3))
    c.photo_rect(1, 0, 800, 600, 760, focus=(0.5, 0.3))
    c.photo_rect(2, 600, 800, 600, 760, focus=(0.5, 0.3))
    c.image_file(require(ctx, "G46_cup", "top-down coffee cup sticker"), 400, 540, 400, None, layer="ui")
    cx, cy = 600, 760
    c.text(cx, cy - 60, T(ctx, "l1", "YOUR"), size=42, font="sans", fill="#fff", weight="bold", anchor="middle")
    c.text(cx, cy, month_name(ctx["date"]).upper(), size=42, font="sans", fill="#fff", weight="bold", anchor="middle")
    c.text(cx, cy + 60, T(ctx, "l3", "reset"), size=38, font="serif", fill="#fff", italic=True, anchor="middle")
    c.text(cx, cy + 120, T(ctx, "l4", "GUIDE"), size=42, font="sans", fill="#fff", weight="bold", anchor="middle")
    c.text(cx, cy + 230, T(ctx, "l5", "(so you can lock it in)"), size=26, font="sans", fill="#fff", anchor="middle")
