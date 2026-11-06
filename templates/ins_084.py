"""INS-084 — café portrait with a yellow camera focus box on the face (sun icon beside it) and a white pill
'afternoon pick me up' at the left; cream border.  Page 6, photos: 1.  Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T, face_box

META = {"id": "INS-084", "photos": 1, "assets": [], "family": "camera-hud", "photo_notes": "one photo; focus box follows the measured face box"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 1520, focus=(0.5, 0.35))
    fx, fy, fw, fh = face_box(ctx)
    bx, by, bw, bh = (fx - fw / 2) * 1200, (fy - fh / 2) * 1600, fw * 1200, fh * 1600
    c.rect(bx, by, bw, bh, "none", layer="fg", stroke="#FFD60A", stroke_w=3)
    for (px, py, sx, sy) in ((bx, by, 1, 1), (bx + bw, by, -1, 1), (bx, by + bh, 1, -1), (bx + bw, by + bh, -1, -1)):
        c.path(f"M{px} {py + sy * 18} V{py} H{px + sx * 18}", stroke="#FFD60A", w=5, layer="fg", cap="butt")
    c.text(bx + bw + 24, by + bh / 2 + 10, "☀", size=34, font="sans", fill="#FFD60A", layer="fg")
    ui.pill(c, 60, 520, T(ctx, "pill", "afternoon pick me up"), size=28, fill="#fff", color="#111", pad=24, h=60)
