"""INS-137 — mirror selfie with a word cloud in the top-right (Lucky, Travel, Money, Drive, Mocha … in blue, black and
grey, mixed sizes).  Page 10, photos: 1.  Generated-asset dependencies: none.  Words from --text words=a|b|c.
"""
import random

from templates._common import T

META = {"id": "INS-137", "photos": 1, "assets": [], "family": "word-cloud", "photo_notes": "one portrait, subject left/centre; cloud sits in the upper-right"}

DEFAULT = "Lucky:90:#3CA7F5|Travel:110:#111|Money:60:#3CA7F5|Drive:56:#3CA7F5|Mocha:48:#3CA7F5|Cherry:44:#3CA7F5|Family:40:#3CA7F5|Love:44:#111|Sleep:40:#111|Shopping:34:#111|Snacks:30:#111|Netflix:28:#111|Ice cream:36:#3CA7F5|Spicy food:36:#111|Friends:34:#111|Yogurt:28:#111|Sauna:30:#111|Money:34:#111"
POS = [(760, 230), (870, 470), (900, 390), (760, 330), (640, 140), (960, 300), (1010, 650), (980, 570), (680, 590), (990, 330), (810, 400), (610, 70), (820, 80), (870, 130), (990, 190), (640, 280), (690, 430), (660, 510)]


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 20, 1200, 1560, focus=(0.4, 0.4))
    items = [w.split(":") for w in T(ctx, "words", DEFAULT).split("|")]
    for k, it in enumerate(items[:len(POS)]):
        word, size, col = it[0], int(it[1]) if len(it) > 1 else 40, it[2] if len(it) > 2 else "#111"
        x, y = POS[k]
        c.text(x, y, word, size=size, font="sans", fill=col, weight="bold")
