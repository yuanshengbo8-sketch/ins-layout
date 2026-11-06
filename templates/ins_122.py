"""INS-122 — two stacked photos with small white serif notes in brackets: '(little trip)' '(sunday)' on the upper photo,
'(< 3)' twice on the lower; cream border.  Page 8, photos: 2.  Generated-asset dependencies: none.
"""
from templates._common import T

META = {"id": "INS-122", "photos": 2, "assets": [], "family": "big-words", "photo_notes": "2 photos"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 80, 1200, 720, focus=(0.5, 0.35))
    c.photo_rect(1, 0, 800, 1200, 720, focus=(0.5, 0.4))
    c.text(300, 770, T(ctx, "n1", "(little trip)"), size=40, font="serif", fill="#fff")
    c.text(790, 630, T(ctx, "n2", "(sunday)"), size=40, font="serif", fill="#fff")
    c.text(990, 1030, T(ctx, "n3", "(< 3)"), size=40, font="serif", fill="#fff")
    c.text(340, 1330, T(ctx, "n3", "(< 3)"), size=40, font="serif", fill="#fff")
