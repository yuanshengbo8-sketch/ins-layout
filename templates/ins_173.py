"""INS-173 — portrait with the letters of 'emotion' raining down both sides of the face in mint hand-written
caps, pooling along the bottom; a small grey raincloud with a face top-right dropping three drops.
Page 1, photos: 1.  Letter paths follow the face box (rule 08: measured per photo, defaults for structure tests).
"""
import math
import random

from components import deco
from templates._common import T, face_box

META = {"id": "INS-173", "photos": 1, "assets": [], "family": "letter-rain", "photo_notes": "one portrait; face box drives the two letter columns"}


def build(c, ctx):
    c.photo_full(0, focus=(0.5, 0.35))
    word = T(ctx, "word", "emotion")
    fx, fy, fw, fh = face_box(ctx)
    cx, cy = fx * 1200, fy * 1600
    half = fw * 1200 / 2 + 70
    rnd = random.Random(3)
    col = "#8FF0E0"
    # two columns hugging the face, from eye level down to the chest
    for side in (-1, 1):
        x0 = cx + side * half
        yy = cy - 60
        k = 0
        while yy < 1180:
            ch = word[k % len(word)]
            c.text(x0 + rnd.uniform(-18, 18) + side * (yy - cy) * 0.08, yy, ch, size=rnd.uniform(44, 60), font="hand", fill=col, anchor="middle", rotate=rnd.uniform(-25, 25))
            yy += rnd.uniform(60, 85); k += 1
    # pool of letters along the bottom
    for i in range(40):
        x = 60 + rnd.random() * 1080; y = 1230 + rnd.random() * 220
        c.text(x, y, word[rnd.randrange(len(word))], size=rnd.uniform(40, 62), font="hand", fill=col, anchor="middle", rotate=rnd.uniform(-40, 40))
    deco.cloud(c, 1090, 110, 50, "#E8E8E8", stroke="#CFCFCF", face=True)
    for i, (dx, dy) in enumerate(((-30, 90), (20, 130), (60, 100))):
        deco.drop(c, 1090 + dx, 110 + dy, 14, "#9FD8F5", stroke="none", highlight=False)
