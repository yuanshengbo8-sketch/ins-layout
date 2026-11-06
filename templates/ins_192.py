"""INS-192 — photo with two thin detection boxes (cyan on the head, pink on an empty area), a pink treble clef, small
outline stars, and a blurred duplicate of the same photo as a lower band (letterboxed).  Page 12, photos: 1.
Generated-asset dependencies: none.
"""
from components import deco
from templates._common import face_box

META = {"id": "INS-192", "photos": 1, "assets": [], "family": "object-boxes", "photo_notes": "one portrait; the cyan box is the measured head"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 1140, focus=(0.5, 0.3))
    fid = c.blur_filter(14)
    c.photo_rect(0, 0, 1200, 1200, 380, focus=(0.5, 0.55), filter_=fid, lock=True)
    fx, fy, fw, fh = face_box(ctx)
    bx, by, bw, bh = (fx - fw / 2) * 1200 - 20, (fy - fh / 2) * 1140 + 40 - 20, fw * 1200 + 40, fh * 1140 + 40
    c.rect(bx, by, bw, bh, "none", layer="fg", stroke="#2FE3E8", stroke_w=4)
    c.rect(80, 560, 240, 380, "none", layer="fg", stroke="#F28CC8", stroke_w=4)
    c.text(1030, 900, "𝄞", size=180, font="serif", fill="#F26AB8")
    for (x, y) in ((760, 1230), (380, 1480), (1060, 1480), (640, 1540)):
        deco.star(c, x, y, 12, "none", stroke="#fff", w=2, inner=0.5)
