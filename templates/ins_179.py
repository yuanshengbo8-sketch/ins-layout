"""INS-179 — street portrait with a small yellow list written on a flat surface left of the subject
('becoming a collector: / of old photos / quirky mugs / good skincare / random notes'), indented like a note.
Page 12, photos: 1.  Generated-asset dependencies: none.  Anchor with --text x= y= (canvas px).
"""
from templates._common import T

META = {"id": "INS-179", "photos": 1, "assets": [], "family": "caption-notes", "photo_notes": "one portrait with an empty surface (table, wall, ground) left of the subject"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 60, 1200, 1480, focus=(0.5, 0.35))
    x, y = float(T(ctx, "x", 120)), float(T(ctx, "y", 1180))
    c.text(x, y, T(ctx, "head", "becoming a collector:"), size=28, font="ui", fill="#F2DC5A", weight="600")
    items = T(ctx, "items", "of old photos|quirky mugs|good skincare|random notes").split("|")
    for k, it in enumerate(items):
        c.text(x + 40 + (k % 2) * 30, y + 60 + k * 40, it, size=26, font="ui", fill="#F2DC5A")
