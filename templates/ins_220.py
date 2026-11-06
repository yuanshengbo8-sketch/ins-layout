"""INS-220 — full photo with three paper colour cards stacked bottom-right; each card = 72% colour block +
28% white label (COLOR®, name, HEX).  Colours are sampled from the photo itself (rule 08): pass
--text c1=#hex|Name c2=... to fix them, otherwise three regions of the photo are median-sampled.
Page 14, photos: 1.  Cards are native-drawn (no master bitmap needed).
"""
from components import imaging
from templates._common import T

META = {"id": "INS-220", "photos": 1, "assets": [], "family": "colour-card",
        "photo_notes": "one photo with 2-3 distinct garment/object colours; sampled boxes recorded in recipe"}

# default sample boxes (normalised x0,y0,x1,y1) - garment-ish regions; override with ctx['color_boxes']
DEFAULT_BOXES = [(0.42, 0.40, 0.58, 0.52), (0.30, 0.62, 0.50, 0.72), (0.55, 0.75, 0.75, 0.88)]


def card(c, x, y, w, h, color, name, hexs):
    fid = c.drop_shadow_filter(0, 4, 8, "rgba(0,0,0,0.25)")
    c.rect(x, y, w, h, "#fff", layer="ui", extra=f' filter="url(#{fid})"')
    c.rect(x + 6, y + 6, w - 12, h * 0.70, color, layer="ui")
    c.text(x + 14, y + h * 0.82, "COLOR", size=w * 0.11, font="sans", weight="bold", fill="#111", layer="ui")
    c.text(x + 14 + w * 0.40, y + h * 0.78, "®", size=w * 0.06, font="sans", fill="#111", layer="ui")
    c.text(x + 14, y + h * 0.90, name, size=w * 0.065, font="sans", fill="#333", layer="ui")
    c.text(x + 14, y + h * 0.96, hexs, size=w * 0.06, font="sans", fill="#333", layer="ui")


def build(c, ctx):
    c.photo_full(0, focus=(0.5, 0.4))
    p = c.photo(0).image
    boxes = ctx.get("color_boxes") or DEFAULT_BOXES
    pw, ph = p.size
    px_boxes = [(int(a * pw), int(b * ph), int(cc * pw), int(d * ph)) for a, b, cc, d in boxes]
    sampled = imaging.dominant_colors(p, px_boxes, 3)
    names, hexes = [], []
    for k in range(3):
        spec = T(ctx, f"c{k + 1}", "")
        if spec:
            hx, _, nm = spec.partition("|")
            hexes.append(hx.upper()); names.append(nm or f"Colour {k + 1}")
        else:
            hexes.append(sampled[k]); names.append(f"Sample {k + 1}")
    c.recipe["color_samples"] = [{"box": b, "hex": h, "name": n} for b, h, n in zip(px_boxes, hexes, names)]
    w, h = 205, 270
    card(c, 780, 1000, w, h, hexes[0], names[0], hexes[0])
    card(c, 985, 1000, w, h, hexes[1], names[1], hexes[1])
    card(c, 880, 1300, w, h, hexes[2], names[2], hexes[2])
