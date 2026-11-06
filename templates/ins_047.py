"""INS-047 — a concrete-tile board (G26 master) on a cream page with a white search pill
('AA  what have you been up to today?  C') and a 3×2 grid of small photo thumbnails with white borders and
file-name captions (outfit.jpg, happy.jpg, details.jpg / coffee.jpg, little break.jpg, good food.jpg).
Page 3, photos: 6.  Requires master G26.
"""
from templates._assets import require
from templates._common import T

META = {"id": "INS-047", "photos": 6, "assets": ["G26"], "family": "carrier-tiles", "photo_notes": "6 photos, portrait thumbnails"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.image_file(require(ctx, "G26", "light grey paving tiles with tree shadow"), 80, 100, 1040, 1400, layer="bg")
    c.rect(180, 220, 840, 64, "#fff", rx=32, layer="ui")
    c.text(210, 262, "AA", size=20, font="ui", fill="#555", layer="ui")
    c.text(600, 262, T(ctx, "q", "what have you been up to today?"), size=22, font="ui", fill="#111", anchor="middle", layer="ui")
    c.text(990, 264, "C", size=22, font="ui", fill="#555", anchor="end", layer="ui")
    names = T(ctx, "names", "outfit.jpg|happy.jpg|details.jpg|coffee.jpg|little break.jpg|good food.jpg").split("|")
    for k in range(6):
        r, col = divmod(k, 3)
        x, y = 170 + col * 300, 360 + r * 390
        c.rect(x - 8, y - 8, 236, 296, "#fff", rx=14, layer="photos")
        c.photo_rect(k, x, y, 220, 280, rx=10, focus=(0.5, 0.35))
        c.text(x + 110, y + 318, names[k % len(names)], size=20, font="ui", fill="#fff", anchor="middle")
