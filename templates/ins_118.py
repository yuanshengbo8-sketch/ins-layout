"""INS-118 — full photo as a camera viewfinder: thirds grid, yellow focus box with a side rail + yellow dot, a
'⊕ autumn' pill, and zoom pills 0.5× 1 2 4 8 (0.5× active).  Page 8, photos: 1.  Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T, face_box

META = {"id": "INS-118", "photos": 1, "assets": [], "family": "camera-hud", "photo_notes": "one photo; the focus box sits on the torso/outfit"}


def build(c, ctx):
    c.photo_full(0, focus=(0.5, 0.4))
    # focus box sits on the outfit just below the measured head; pill to its lower-left
    fx, fy, fw, fh = face_box(ctx)
    bw, bh = 250, 260
    bx, by = fx * 1200 - bw / 2 + 30, (fy + fh / 2) * 1600 + 30
    ui.camera_hud(c, 0, 0, 1200, 1600, zooms=("0.5×", "1", "2", "4", "8"), active=0, grid=True, box=(bx, by, bw, bh), color="rgba(255,255,255,0.7)")
    ui.pill(c, max(60, bx - 250), by + bh - 20, T(ctx, "label", "⊕ autumn"), size=30, fill="rgba(255,255,255,0.35)", color="#fff", pad=20, h=64)
