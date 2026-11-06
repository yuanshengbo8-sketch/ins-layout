"""INS-113 — left column: 'SWAG' tall condensed white-on-grey over 'YES' tall white-on-black; right 60%: the photo with
scattered black stars and a white speech bubble 'just on my way'.  Page 8, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco, ui
from templates._common import T

META = {"id": "INS-113", "photos": 1, "assets": [], "family": "split-words", "photo_notes": "one portrait, subject on the right"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.rect(60, 0, 400, 790, "#8F8F8F", layer="bg")
    c.rect(60, 790, 400, 810, "#111", layer="bg")
    c.photo_rect(0, 460, 0, 740, 1600, focus=(0.5, 0.3))
    # tall condensed words: horizontal text stretched vertically (not rotated), as in the reference
    c.text(0, 0, T(ctx, "w1", "SWAG"), size=120, font="sans_narrow", fill="#fff", anchor="middle", weight="bold", transform="translate(260 760) scale(1.25 8.2)")
    c.text(0, 0, T(ctx, "w2", "YES"), size=120, font="sans_narrow", fill="#fff", anchor="middle", weight="bold", transform="translate(260 1580) scale(1.6 8.6)")
    for (x, y, r) in ((1130, 320, 26), (1000, 460, 16), (1130, 500, 16), (1120, 1030, 22), (560, 1180, 22), (1040, 1520, 34), (620, 1480, 22), (860, 1540, 18)):
        deco.star(c, x, y, r, "#111")
    ui.speech_cloud(c, 1000, 160, 230, 110, T(ctx, "msg", "just on my way"), size=22, font="ui", stroke="none", tail_to=(960, 300))
