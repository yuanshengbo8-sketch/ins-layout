"""INS-125 — full photo with a single small white word 'Alone' beside the subject; cream border.
Page 9, photos: 1.  Generated-asset dependencies: none.
"""
from templates._common import T

META = {"id": "INS-125", "photos": 1, "assets": [], "family": "big-words", "photo_notes": "one photo"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 1520, focus=(0.5, 0.35))
    c.text(840, 740, T(ctx, "word", "Alone"), size=30, font="ui", fill="#fff")
