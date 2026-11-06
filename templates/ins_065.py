"""INS-065 — two stacked photos with one white bold word on each ('yes' upper, 'but' lower), cream border.
Page 4, photos: 2.  Generated-asset dependencies: none.
"""
from templates._common import T

META = {"id": "INS-065", "photos": 2, "assets": [], "family": "big-words", "photo_notes": "2 photos"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 50, 1200, 730, focus=(0.5, 0.35))
    c.photo_rect(1, 0, 800, 1200, 750, focus=(0.5, 0.35))
    c.text(600, 470, T(ctx, "w1", "yes"), size=70, fill="#fff", weight="bold", anchor="middle")
    c.text(600, 1190, T(ctx, "w2", "but"), size=70, fill="#fff", weight="bold", anchor="middle")
