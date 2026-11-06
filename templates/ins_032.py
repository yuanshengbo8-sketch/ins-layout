"""INS-032 — overhead ground shot (G14 master: grey ground, latte in hand, blue jeans / white socks / black loafers)
with a tilted paper map plane in the middle: road network, street names, two pins, a circular avatar photo
with a blue location dot and a '3D' pill.  The map plane sits BEHIND the cup hand and shoes (foreground mask
from the same master).  Page 2, photos: 1 (avatar).  REQUIRES masters: G14 + G14 foreground mask.
"""
from templates._assets import require, variant_file
from templates._common import T

META = {"id": "INS-032", "photos": 1, "assets": ["G14", "G14_fg"], "family": "carrier-map",
        "photo_notes": "one portrait photo used as the round avatar on the map; the ground/cup/shoes come from the G14 master"}

# map plane corners in canvas px (TL, TR, BR, BL): tilted about 17°, running under the cup hand and the shoes
QUAD = [(330, 150), (1170, 400), (960, 1270), (120, 1020)]


def build(c, ctx):
    bg = require(ctx, "G14", "overhead ground + latte hand + jeans/loafers; photo window left empty in the middle")
    fg = variant_file(ctx, "G14_fg.png")
    if not fg.exists():
        from templates._text import AssetMissing
        raise AssetMissing("G14_fg.png missing - run scripts/chroma_masters.py")
    c.image_file(bg, 0, 0, 1200, 1600, layer="bg")
    # map paper
    from components import imaging
    from PIL import Image, ImageDraw
    paper = Image.new("RGBA", (900, 900), (246, 243, 236, 255))
    d = ImageDraw.Draw(paper)
    roads = [((0, 300), (900, 180)), ((0, 560), (900, 520)), ((200, 0), (320, 900)), ((620, 0), (560, 900)), ((0, 760), (900, 820)), ((420, 0), (470, 900))]
    for a, b in roads:
        d.line([a, b], fill=(255, 255, 255, 255), width=46)
        d.line([a, b], fill=(214, 211, 203, 255), width=4)
    for x in range(0, 900, 60):
        d.line([(x, 0), (x, 900)], fill=(236, 232, 224, 255), width=1)
    layer = imaging.perspective_layer(paper, QUAD, (1200, 1600))
    c.add("ui", f'<image href="{imaging.to_data_uri(layer)}" x="0" y="0" width="1200" height="1600"/>')
    # labels and pins are placed in plane coordinates (u,v in 0..1) so they follow the tilt
    def P(u, v):
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = QUAD
        tx, ty = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        bx, by = x3 + (x2 - x3) * u, y3 + (y2 - y3) * u
        return tx + (bx - tx) * v, ty + (by - ty) * v
    import math
    rot = math.degrees(math.atan2(QUAD[1][1] - QUAD[0][1], QUAD[1][0] - QUAD[0][0]))
    for u, v, txt, size, fill, w in ((0.42, 0.42, T(ctx, "street1", "SHOREDITCH"), 38, "#333", "600"), (0.30, 0.12, T(ctx, "street2", "Old Street"), 24, "#666", "normal"),
                                     (0.70, 0.30, T(ctx, "street3", "Lagan"), 22, "#666", "normal"), (0.84, 0.56, T(ctx, "poi1", "Blacklock"), 22, "#8A6A2A", "normal"),
                                     (0.34, 0.25, T(ctx, "poi2", "TOYO"), 22, "#E0245E", "normal")):
        x, y = P(u, v); c.text(x, y, txt, size=size, font="sans", fill=fill, rotate=rot, weight=w, anchor="middle", layer="ui")
    for u, v, col in ((0.24, 0.27, "#E86AA6"), (0.84, 0.62, "#F2A33A")):
        x, y = P(u, v); c.circle(x, y, 13, col, layer="ui")
    ax, ay = P(0.70, 0.70)
    c.circle(ax, ay, 58, "#fff", layer="ui")
    c.photo_circle(0, ax, ay, 50, focus=(0.5, 0.25), layer="ui")
    x, y = P(0.60, 0.78); c.circle(x, y, 10, "#2F8BFF", layer="ui", stroke="#fff", stroke_w=3)
    x, y = P(0.90, 0.80); c.circle(x, y, 40, "#fff", layer="ui"); c.text(x, y + 10, "3D", size=28, font="ui", fill="#111", anchor="middle", layer="ui")
    c.image_file(fg, 0, 0, 1200, 1600, layer="fg")
