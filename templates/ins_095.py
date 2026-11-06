"""INS-095 — full photo with a dark music-player card over the lower third (artwork, 'Sidewalk Radio',
'Original Mix · Video Available', 0:49 ▬▬ -1:30, ◀◀ ▮▮ ▶▶).  Page 7, photos: 1.
Artwork: the G23 'croissant radio' cover master if assets/masters/G23_cover_mint.png exists, otherwise a
native-drawn cover (registered substitute, see effects.json).
"""
from components import ui
from templates._common import T
from templates._assets import cover_art

META = {"id": "INS-095", "photos": 1, "assets": ["G23:optional"], "family": "ui-music", "photo_notes": "one full-length portrait, card covers the legs"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 1520, focus=(0.5, 0.3))
    x, y, w, h = 180, 1040, 840, 400
    ui.music_card(c, x, y, w, h, T(ctx, "title", "Sidewalk Radio"), T(ctx, "sub", "Original Mix · Video Available"),
                  t0="0:49", t1="-1:30", progress=0.4)
    cover_art(c, ctx, x + 56, y + 56, 120, variant="mint")
