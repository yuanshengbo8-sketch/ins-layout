"""INS-193 — four horizontal photo bands (06:00 / 12:00 / 18:00 / 00:00 time stamps in white), one day in four moments.
Page 12, photos: 4.  Generated-asset dependencies: none.
"""
from templates._common import T

META = {"id": "INS-193", "photos": 4, "assets": [], "family": "ui-schedule", "photo_notes": "4 photos, landscape crops"}


def build(c, ctx):
    c.bg = "#EEECE7"
    times = T(ctx, "times", "06:00|12:00|18:00|00:00").split("|")
    pos = [(170, 200), (800, 560), (320, 940), (820, 1310)]
    for k in range(4):
        y = 20 + k * 392
        c.photo_rect(k, 0, y, 1200, 380, focus=(0.5, 0.35))
        c.text(pos[k][0], pos[k][1], times[k], size=30, font="ui", fill="#fff")
