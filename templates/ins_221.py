"""INS-221 — object-detection look: #1B30DD thin boxes around hair / tee / ring / shorts with blue tags
'@SOFT.HAIR' '@OOTD.DIARY' '@WHITE.TEE' '@SILVER.RING' '@GREY.SHORTS', dog-leg leader lines, and a small synced copy
of the whole frame top-right with its own tiny boxes.  Page 14, photos: 1.
Boxes come from ctx['objects'] = [(label, x,y,w,h normalised)...]; defaults are structure-test positions only.
"""
from components import ui

META = {"id": "INS-221", "photos": 1, "assets": [], "family": "object-boxes", "photo_notes": "one outfit photo; object boxes must be measured on the real photo"}

BLUE = "#1B30DD"
DEFAULT_OBJECTS = [("@SOFT.HAIR", 0.38, 0.10, 0.24, 0.16), ("@OOTD.DIARY", 0.40, 0.27, 0.78, 0.58), ("@WHITE.TEE", 0.34, 0.30, 0.42, 0.42),
                   ("@SILVER.RING", 0.47, 0.44, 0.08, 0.06), ("@GREY.SHORTS", 0.36, 0.72, 0.40, 0.22)]
TAG_POS = {"@SOFT.HAIR": (640, 120), "@OOTD.DIARY": (40, 190), "@WHITE.TEE": (40, 340), "@SILVER.RING": (680, 900), "@GREY.SHORTS": (560, 1100)}


def draw_boxes(c, objs, ox, oy, sw, sh, tags=True):
    for lab, x, y, w, h in objs:
        bx, by, bw, bh = ox + x * sw, oy + y * sh, w * sw, h * sh
        c.rect(bx, by, bw, bh, "none", layer="fg", stroke=BLUE, stroke_w=3 if tags else 1.5)
        if tags:
            tx, ty = TAG_POS.get(lab, (bx, by - 50))
            ui.label_tag(c, tx, ty, lab, size=24, layer="fg")
            # dog-leg leader from the tag to the box edge
            mx = tx + 60 if tx < bx else tx
            c.path(f"M{tx + 40} {ty + 36} V{by if ty < by else by + bh} H{bx if tx < bx else bx + bw}", stroke=BLUE, w=2, layer="fg", cap="butt")


def build(c, ctx):
    c.photo_full(0, focus=(0.5, 0.4))
    objs = ctx.get("objects") or DEFAULT_OBJECTS
    draw_boxes(c, objs, 0, 0, 1200, 1600)
    # synced mini frame top-right
    c.photo_rect(0, 850, 40, 300, 400, focus=(0.5, 0.4), stroke=BLUE, stroke_w=2)
    draw_boxes(c, objs, 850, 40, 300, 400, tags=False)
