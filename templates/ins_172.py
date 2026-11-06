"""INS-172 — landscape photo window in the middle of a cream page, with a small white now-playing pill
('Coffee Radio / Little daydream') over the top-left of the photo.  Page 12, photos: 1.
Album art: G23 master if present, else native cover.
"""
from components import ui
from templates._common import T
from templates._assets import cover_art

META = {"id": "INS-172", "photos": 1, "assets": ["G23:optional"], "family": "ui-music", "photo_notes": "one photo (landscape crop), subject centred"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 340, 1200, 900, focus=(0.5, 0.4))
    x, y, w, h = 400, 440, 330, 110
    fid = c.drop_shadow_filter(0, 4, 8, "rgba(0,0,0,0.2)")
    c.rect(x, y, w, h, "#fff", rx=12, layer="ui", extra=f' filter="url(#{fid})"')
    cover_art(c, ctx, x + 14, y + 14, 82, variant="cream")
    c.text(x + 112, y + 48, T(ctx, "title", "Coffee Radio"), size=26, font="ui", fill="#111", weight="bold", layer="ui")
    c.text(x + 112, y + 82, T(ctx, "sub", "Little daydream"), size=20, font="ui", fill="#666", layer="ui")
