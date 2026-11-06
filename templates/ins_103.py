"""INS-103 — full photo with three tilted white 'Google Search' browser frames (× left, label right) descending
across the figure, and a black 'Private  +  Done' tab bar at the bottom.  Page 1, photos: 1.
Generated-asset dependencies: none.
"""
from components.core import Canvas

META = {"id": "INS-103", "photos": 1, "assets": [], "family": "ui-browser", "photo_notes": "one portrait photo, arms-up poses suit the frames"}


def frame(c: Canvas, x, y, w, h, rot, bar=58):
    cx, cy = x + w / 2, y + h / 2
    c.raw(f'<g transform="rotate({rot} {cx} {cy})">', "ui")
    c.rect(x, y, w, bar, "#fff", layer="ui")
    c.rect(x, y, w, h, "none", layer="ui", stroke="#fff", stroke_w=6)
    c.text(x + 18, y + bar * 0.7, "✕", size=30, font="sans", fill="#111", weight="bold", layer="ui")
    c.text(x + w - 24, y + bar * 0.68, "Google Search", size=26, font="sans", fill="#222", anchor="end", layer="ui")
    c.raw("</g>", "ui")


def build(c, ctx):
    c.photo_full(0, focus=(0.5, 0.4))
    frame(c, 250, 150, 640, 220, -2)
    frame(c, 190, 450, 760, 330, 1.5)
    frame(c, 190, 820, 790, 420, -1)
    c.rect(170, 1400, 820, 100, "#111", layer="ui")
    c.text(230, 1465, "Private", size=36, font="ui", fill="#fff", layer="ui")
    c.text(580, 1470, "+", size=48, font="ui", fill="#fff", anchor="middle", weight="bold", layer="ui")
    c.text(930, 1465, "Done", size=36, font="ui", fill="#fff", anchor="end", weight="600", layer="ui")
