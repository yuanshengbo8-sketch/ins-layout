"""INS-083 — café portrait with a thin camera thirds grid, a white speech pill 'a little café moment ⚬°₊' top-left,
a soft caption 'a quiet table, a warm drink, / and a little time to slow down' lower-right, and 1 / 2x / 5 zoom dots.
Page 6, photos: 1.  Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T

META = {"id": "INS-083", "photos": 1, "assets": [], "family": "camera-hud", "photo_notes": "one portrait, subject centred"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 1520, focus=(0.5, 0.35))
    ui.camera_hud(c, 0, 40, 1200, 1520, zooms=("1", "2x", "5"), active=1, grid=True, color="rgba(255,255,255,0.55)")
    ui.bubble(c, 150, 170, 360, 76, T(ctx, "pill", "a little café moment ⚬°₊"), size=26, fill="#fff", color="#111", tail="left", align="center")
    c.text(1060, 1290, T(ctx, "cap1", "a quiet table, a warm drink,"), size=24, font="ui", fill="rgba(255,255,255,0.85)", anchor="end")
    c.text(1060, 1326, T(ctx, "cap2", "and a little time to slow down"), size=24, font="ui", fill="rgba(255,255,255,0.85)", anchor="end")
