"""INS-042 — pale page, 'TODAY AT 17:28' header, two tilted photo cards overlapping (first up-left, second down-right),
and a blue iMessage bubble 'fall outfit' bottom-right.  Page 3, photos: 2.  Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T

META = {"id": "INS-042", "photos": 2, "assets": [], "family": "ui-message", "photo_notes": "2 portrait photos"}


def build(c, ctx):
    c.bg = "#F5F4F0"
    c.text(600, 110, T(ctx, "time", "TODAY AT 17:28"), size=26, font="ui", fill="#8E8E93", anchor="middle", weight="600")
    c.photo_rect(0, 400, 190, 370, 500, rx=22, rotate=-8, focus=(0.5, 0.35), shadow=(14, 0, 8, 0.22))
    c.photo_rect(1, 650, 640, 370, 560, rx=22, rotate=6, focus=(0.5, 0.35), shadow=(14, 0, 8, 0.22))
    ui.bubble(c, 790, 1300, 230, 90, T(ctx, "msg", "fall outfit"), size=34, tail="right", align="center", weight="600")
