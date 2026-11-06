"""INS-107 — the same photo twice (top / bottom halves, slight re-crop) with a script line 'reset your pace' across the
seam and a cream sticky note 'a little pause. / sit down, breathe, enjoy your little everyday moments.' with three
grey dots on its left edge.  Page 7, photos: 1.  Generated-asset dependencies: none.
"""
from templates._common import T

META = {"id": "INS-107", "photos": 1, "assets": [], "family": "duplicate-note", "photo_notes": "one portrait photo, used twice"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 60, 1200, 720, focus=(0.5, 0.3), zoom=1.05)
    c.photo_rect(0, 0, 820, 1200, 740, focus=(0.5, 0.55), zoom=1.05, lock=True)
    c.text(620, 590, T(ctx, "script", "reset your pace"), size=54, font="script", fill="#fff", anchor="middle", italic=True)
    x, y, w, h = 350, 650, 540, 190
    c.rect(x, y, w, h, "#F3EFE0", layer="ui", opacity=0.96)
    for k in range(3):
        c.circle(x + 18, y + 40 + k * 48, 9, "#8E8E8E", layer="ui")
    c.text(x + 50, y + 54, T(ctx, "n1", "a little pause."), size=24, font="ui", fill="#111", weight="bold", layer="ui")
    c.text(x + 50, y + 100, T(ctx, "n2", "sit down, breathe, enjoy your"), size=22, font="ui", fill="#333", layer="ui")
    c.text(x + 50, y + 136, T(ctx, "n3", "little everyday moments."), size=22, font="ui", fill="#333", layer="ui")
