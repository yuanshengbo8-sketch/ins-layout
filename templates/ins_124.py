"""INS-124 — full-height portrait with a camera thirds grid, yellow bold 'Choose / your / fave' beside the figure and
0.5 · 1× · 2 zoom pills (1× active); cream border.  Page 9, photos: 1.  Generated-asset dependencies: none.
"""
from components import ui
from templates._text import stacked
from templates._common import T, face_box

META = {"id": "INS-124", "photos": 1, "assets": [], "family": "camera-hud", "photo_notes": "one full-length portrait"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 1520, focus=(0.5, 0.3))
    ui.camera_hud(c, 0, 40, 1200, 1520, zooms=("0.5", "1×", "2"), active=1, grid=True, color="rgba(255,255,255,0.6)")
    fx, fy, fw, fh = face_box(ctx)
    y0 = max(700, (fy + fh / 2) * 1600 + 110)
    stacked(c, T(ctx, "lines", "Choose|your|fave").split("|"), 600, y0, 86, "#F7E63B", anchor="middle", leading=1.25, weight="bold")
