"""INS-089 — full photo with a vertical stack of four iOS Focus rows (Do not disturb · On, Sleep, Personal · Time for myself,
Work · One thing at a time) sitting over the torso.  Page 1, photos: 1.  Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T, face_box

META = {"id": "INS-089", "photos": 1, "assets": [], "family": "ui-focus", "photo_notes": "one portrait photo, rows cover the torso not the face"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 50, 1200, 1500, focus=(0.5, 0.3))
    rows = [("☾", T(ctx, "r1", "Do not disturb"), "On", 0.95), ("▬", T(ctx, "r2", "Sleep"), None, 0.75),
            ("●", T(ctx, "r3", "Personal"), "Time for myself", 0.6), ("▣", T(ctx, "r4", "Work"), "One thing at a time", 0.5)]
    fx, fy, fw, fh = face_box(ctx)
    face_bottom = (fy + fh / 2) * 1600
    y = max(600, face_bottom + 70)  # never cover the face (rule 07)
    for ic, title, sub, op in rows:
        ui.focus_row(c, 330, y, 520, 96, ic, title, sub, fill=f"rgba(255,255,255,{op})")
        y += 100
