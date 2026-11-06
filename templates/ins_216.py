"""INS-216 — selfie with a cream border and two small white Korean crying marks 'ㅠㅠ' with a dot, floating right of the
face.  Page 14, photos: 1.  Generated-asset dependencies: none.
"""
from templates._common import T, face_box

META = {"id": "INS-216", "photos": 1, "assets": [], "family": "caption-notes", "photo_notes": "one selfie; the mark sits beside the measured head"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 70, 1200, 1460, focus=(0.5, 0.35))
    fx, fy, fw, fh = face_box(ctx)
    x = min(1120, (fx + fw / 2) * 1200 + 90); y = (fy - fh / 6) * 1600
    c.text(x, y, T(ctx, "mark", "ㅠㅠ"), size=54, font="kr", fill="#fff", anchor="middle", weight="bold")
    c.text(x, y + 60, "·", size=54, font="kr", fill="#fff", anchor="middle", weight="bold")
