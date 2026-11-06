"""INS-068 — open notebook on gingham (G20 master): left page a date tag and a short hand-typed diary, right page
three round avatars (ME / YOU / US), a main photo, 'our small map' with hand-drawn roads and four small photos
pinned with blue numbered markers.  Page 5, photos: 8 (3 avatars, 1 main, 4 small).  Requires master G20.
"""
from templates._assets import require
from templates._common import T

META = {"id": "INS-068", "photos": 8, "assets": ["G20"], "family": "carrier-notebook", "photo_notes": "8 photos: 3 faces for avatars, 1 main, 4 small"}


def build(c, ctx):
    c.image_file(require(ctx, "G20", "open blank notebook on gingham cloth"), 0, 0, 1200, 1600, layer="bg")
    d = ctx["date"]
    # left page (the notebook spans x 80..1070, y 430..1190 in canvas px; the spine is at x 565)
    c.rect(140, 460, 170, 40, "#EAD9DD", rx=4, layer="ui")
    c.text(225, 488, d.strftime("%d %b %Y").upper(), size=18, font="mono", fill="#7A4B55", anchor="middle", layer="ui")
    lines = T(ctx, "diary", "A small day, kept here.|Coffee after the rain,|a walk with nowhere to be.|We talked about little things|and stayed a little longer.|These ordinary moments|are the ones I want to keep.").split("|")
    for k, ln in enumerate(lines):
        c.text(140, 550 + k * 38, ln, size=19, font="mono", fill="#333")
    # right page
    for k, lab in enumerate(("ME", "YOU", "US")):
        cx = 690 + k * 115
        c.photo_circle(k, cx, 500, 40, focus=(0.5, 0.3))
        c.text(cx, 562, lab, size=14, font="mono", fill="#555", anchor="middle")
    c.photo_rect(3, 630, 590, 390, 250, stroke="#fff", stroke_w=8, focus=(0.5, 0.3))
    c.text(825, 872, T(ctx, "map", "our small map"), size=16, font="mono", fill="#555", anchor="middle")
    c.text(120, 1000, T(ctx, "walk", "coffee walk"), size=15, font="mono", fill="#555")
    for seg in ("M110 930 L300 920 L330 880", "M110 1050 L250 1050 L260 980", "M340 960 L520 960", "M620 930 L700 920 L720 880", "M760 1000 L1040 985", "M880 900 L900 1000 L880 1160", "M300 1120 L520 1110"):
        c.path(seg, stroke="#9A9A9A", w=3, layer="deco")
    pins = [(4, 320, 900, 110, "16"), (5, 860, 900, 110, "10"), (6, 640, 1000, 110, "2"), (7, 130, 1060, 96, "6")]
    for (i, x, y, w, n) in pins:
        c.photo_rect(i, x, y, w, w * 1.0, stroke="#fff", stroke_w=5, focus=(0.5, 0.3))
        c.circle(x + w + 6, y - 2, 18, "#2F8BFF", layer="ui")
        c.text(x + w + 6, y + 5, n, size=17, font="ui", fill="#fff", anchor="middle", weight="bold", layer="ui")
