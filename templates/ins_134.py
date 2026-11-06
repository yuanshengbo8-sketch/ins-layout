"""INS-134 — the photo blurred full-bleed as background, a sharp rounded copy of the same photo in the centre, and a
light iOS quick-action sheet (Share / Favorite / Delete, Copy, Duplicate, Hide, Add to album) bottom-left.
Page 9, photos: 1.  Generated-asset dependencies: none.
"""
from components import ui

META = {"id": "INS-134", "photos": 1, "assets": [], "family": "ui-share", "photo_notes": "one portrait photo"}


def build(c, ctx):
    fid = c.blur_filter(22)
    c.photo_full(0, focus=(0.5, 0.4), filter_=fid)
    c.rect(0, 0, 1200, 1600, "rgba(255,255,255,0.15)", layer="photos")
    c.photo_rect(0, 130, 390, 590, 720, rx=18, focus=(0.5, 0.35), shadow=(20, 0, 10, 0.3))
    ui.share_sheet(c, 130, 1150, 430, [("▣", "Copy"), ("⊞", "Duplicate"), ("◉", "Hide"), ("▱", "Add to album")])
