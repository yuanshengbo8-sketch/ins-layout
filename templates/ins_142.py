"""INS-142 — selfie with a blue comic speech bubble '0.o?' top-right and two blue '¿' hooks under the eyes.
Page 10, photos: 1.  Face position from the measured face box (rule 08).  Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T, face_box

META = {"id": "INS-142", "photos": 1, "assets": [], "family": "face-stickers", "photo_notes": "one selfie, face centred"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 60, 1200, 1480, focus=(0.5, 0.3))
    fx, fy, fw, fh = face_box(ctx)
    cx, cy = fx * 1200, fy * 1600
    ui.speech_cloud(c, 700, 90, 280, 160, T(ctx, "msg", "0.o?"), size=60, font="hand", fill="#EAF5FF", stroke="#1E6FD9", sw=5, tail_to=(cx + 60, cy - fh * 800 + 40))
    for sx in (-1, 1):
        c.text(cx + sx * fw * 1200 * 0.28, cy + fh * 1600 * 0.28, "¿", size=70, font="sans", fill="#1E8CF0", anchor="middle", weight="bold")
