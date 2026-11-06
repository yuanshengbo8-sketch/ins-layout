"""INS-174 — cream polka-dot fabric (G27 master) with a monthly-recap collage: 'the / this month / outlook' bold
top-left, the year top-right, a pink 'Life is just a cup of cake' label, four photos with small typed notes
('20(26) Mer's wrapped in media', 'the november digest', 'Monthly Recap', 'girls day out'), a PNG file icon
'MY DAILY NOTES' and a 'Location · my little city' pill.  Page 12, photos: 4.  Requires master G27.
"""
from components import deco, ui
from templates._assets import by_variant, require
from templates._common import T, month_name

META = {"id": "INS-174", "photos": 4, "assets": ["G27"], "family": "carrier-collage", "photo_notes": "4 photos (2 portrait, 1 landscape, 1 small)"}


def build(c, ctx):
    c.image_file(require(ctx, "G27", "cream fabric with black polka dots"), 0, 0, 1200, 1600, layer="bg")
    d = ctx["date"]; mn = month_name(d).lower()
    # a halo in the fabric colour keeps small type readable over the dots
    halo = {"stroke": by_variant(ctx, "#D8CCBD", "#E8B0B9", "#ABAAB0"), "stroke_w": 7}
    for k, ln in enumerate(("the", "this month", "outlook")):
        c.text(24, 150 + k * 66, ln, size=56, font="sans", fill="#111", weight="bold", **halo)
    c.text(1150, 112, str(d.year), size=40, font="sans", fill="#111", weight="bold", anchor="end", **halo)
    c.rect(596, 224, 196, 86, "#F0A9C6", layer="ui")
    c.text(694, 260, T(ctx, "pink1", "Life is just a"), size=20, font="serif", fill="#fff", anchor="middle", layer="ui")
    c.text(694, 288, T(ctx, "pink2", "Cup of cake"), size=20, font="serif", fill="#fff", anchor="middle", layer="ui")
    for k, ln in enumerate(("no explanation", "just because", "it's pink")):
        c.text(662, 340 + k * 22, ln, size=20, font="sans", fill="#111", **halo)
    c.photo_rect(0, 286, 490, 310, 196, focus=(0.5, 0.35))
    c.text(436, 750, f"20({str(d.year)[-2:]})", size=56, font="sans", fill="#111", anchor="middle", **halo)
    c.text(366, 806, "Mer's", size=40, font="serif", fill="#111", italic=True, weight="bold", **halo)
    c.text(310, 834, "wrapped in media", size=22, font="sans", fill="#111", **halo)
    c.photo_rect(1, 762, 490, 142, 90, focus=(0.5, 0.3))
    for k, ln in enumerate(("the", mn, "digest")):
        c.text(768, 606 + k * 28, ln, size=26, font="sans", fill="#111", **halo)
    c.text(768, 700, "cookies, candle, and book", size=15, font="serif", fill="#111", italic=True, **halo)
    c.photo_rect(2, 760, 730, 310, 392, focus=(0.5, 0.3))
    c.text(916, 1180, "Monthly", size=46, font="sans", fill="#111", anchor="middle", **halo); c.text(916, 1222, "Recap", size=46, font="sans", fill="#111", anchor="middle", **halo)
    deco.document_icon(c, 104, 874, 104, fill="#fff", layer="ui")
    c.text(116, 900, "PNG", size=24, font="sans", fill="#111", **halo)
    c.text(102, 1022, T(ctx, "doc", "MY DAILY NOTES"), size=16, font="sans", fill="#111", italic=True, **halo)
    c.photo_rect(3, 430, 1004, 166, 212, focus=(0.5, 0.3))
    for k, ln in enumerate(("girls", "day", "out")):
        c.text(432, 1246 + k * 26, ln, size=24, font="sans", fill="#111", **halo)
    ui.pill(c, 500, 1240, "Location · my little city", size=14, fill="#fff", color="#111", pad=14, h=40)
