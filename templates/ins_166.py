"""INS-166 — street photo with blue desktop folders down the left edge (selfie, new hobbies, outfits, beauty-as-document),
'random' folder on the right, a white speech pill 'life recently' with a coffee emoji, and a small 'Diary' window with a
second photo bottom-right.  Page 11, photos: 2.  Generated-asset dependencies: none.
"""
from components import deco, ui
from templates._common import T

META = {"id": "INS-166", "photos": 2, "assets": [], "family": "desktop-icons", "photo_notes": "#1 full-length portrait, #2 small window photo"}


def build(c, ctx):
    c.photo_full(0, focus=(0.5, 0.3))
    labels = T(ctx, "folders", "selfie|new hobbies|outfits").split("|")
    y = 120
    for lab in labels:
        deco.folder_icon(c, 60, y, 130, label=lab, label_size=22); y += 280
    deco.document_icon(c, 240, 960, 110, label=T(ctx, "doc", "beauty"), label_size=22, fill="#F4F4F4")
    deco.folder_icon(c, 60, 1140, 130)
    deco.folder_icon(c, 1100, 330, 130, label=T(ctx, "right", "random"), label_size=22)
    ui.pill(c, 420, 520, T(ctx, "msg", "life recently"), size=46, fill="#fff", color="#111", pad=36, h=100)
    c.circle(880, 560, 56, "#fff", layer="deco"); c.text(880, 578, "☕", size=46, font="emoji", anchor="middle", layer="deco")
    c.rect(1030, 640, 190, 700, "#F6F6F6", rx=6, layer="ui", stroke="#D0D0D0")
    c.text(1050, 670, "• • Diary", size=14, font="ui", fill="#555", layer="ui")
    c.photo_rect(1, 1040, 690, 170, 630, focus=(0.5, 0.3))
