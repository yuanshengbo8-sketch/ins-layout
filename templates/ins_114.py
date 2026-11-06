"""INS-114 — white page: one landscape photo left, two small portraits right; serif notes 'alone / with / me' and a blue
bold caption 'When the world is too loud, I go blue screen.' between them.  Page 8, photos: 3.
Generated-asset dependencies: none.
"""
from templates._common import T

META = {"id": "INS-114", "photos": 3, "assets": [], "family": "collage-notes", "photo_notes": "#1 landscape, #2 #3 portraits"}


def build(c, ctx):
    c.bg = "#FFFFFF"
    c.photo_rect(0, 0, 320, 620, 820, focus=(0.5, 0.4))
    c.photo_rect(1, 720, 420, 320, 320, focus=(0.5, 0.35))
    c.photo_rect(2, 720, 790, 320, 320, focus=(0.5, 0.35))
    c.text(760, 370, T(ctx, "n1", "alone"), size=26, font="serif", fill="#111")
    c.text(960, 405, T(ctx, "n2", "with"), size=26, font="serif", fill="#111")
    c.text(690, 590, T(ctx, "n3", "me"), size=26, font="serif", fill="#111", anchor="end")
    lines = T(ctx, "cap", "When|the world|is too|loud,|I go|blue|screen.").split("|")
    y = 760
    for ln in lines:
        c.text(640 + (y - 760) * 0.25, y, ln, size=46, font="sans", fill="#2B2BE0", weight="bold")
        y += 54
