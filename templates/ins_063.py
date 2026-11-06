"""INS-063 — two stacked photos with three iOS Focus rows centred over the seam
(Morning Routine · On / Reading / Self care).  Page 4, photos: 2.  Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T

META = {"id": "INS-063", "photos": 2, "assets": [], "family": "ui-focus",
        "photo_notes": "2 photos; #1 landscape-ish top half, #2 bottom half"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 50, 1200, 760, focus=(0.5, 0.35))
    c.photo_rect(1, 0, 810, 1200, 760, focus=(0.5, 0.35))
    rows = [("☀", T(ctx, "r1", "Morning Routine"), "On"), ("▦", T(ctx, "r2", "Reading"), None), ("♥", T(ctx, "r3", "Self care"), None)]
    y = 600
    for ic, title, sub in rows:
        ui.focus_row(c, 320, y, 560, 120, ic, title, sub, fill="rgba(255,255,255,0.93)" if sub else "rgba(255,255,255,0.78)")
        y += 150
