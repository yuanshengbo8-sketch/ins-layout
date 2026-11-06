"""INS-035 — nine photos pasted onto a 3×3 block of pavement tiles seen at an angle, tree shadow, the wearer's
shoes at the bottom-right edge.  Each photo is mapped to ITS OWN tile's four corners (4×4 grid of tile-seam
intersections measured on the master), inset for the grout line, numbered 1-9 with small white badges.
Page 2, photos: 9.  REQUIRES masters: ground_035_tiles9.png + ground_035_grid.json (16 points) + shoes cut-out.
"""
import json

from templates._assets import require, variant_file

META = {"id": "INS-035", "photos": 9, "assets": ["ground", "ground_grid", "ground_fg"], "family": "carrier-tiles",
        "photo_notes": "9 photos, one per tile; order = reference numbering (top-left tile is 1)"}


def build(c, ctx):
    bg = require(ctx, "ground", "angled 3x3 pavement tiles with tree shadow, shoes bottom-right, tiles empty")
    grid_p = variant_file(ctx, "ground_035_grid.json")
    fg = variant_file(ctx, "ground_035_fg.png")
    if not grid_p.exists():
        from templates._text import AssetMissing
        raise AssetMissing("ground_035_grid.json (4x4 seam intersections measured on the master) missing")
    pts = [[x * 1200, y * 1600] for x, y in json.loads(grid_p.read_text())]  # normalised -> canvas px, row-major 4x4
    c.image_file(bg, 0, 0, 1200, 1600, layer="bg")
    order = [0, 5, 7, 8, 1, 3, 4, 2, 6]  # reference numbering 1..9 by tile (row-major tile index)
    for k, tile in enumerate(order):
        r, col = divmod(tile, 3)
        q = [tuple(pts[r * 4 + col]), tuple(pts[r * 4 + col + 1]), tuple(pts[(r + 1) * 4 + col + 1]), tuple(pts[(r + 1) * 4 + col])]
        c.photo_quad(k, q, inset=0.06, focus=(0.5, 0.35))
        bx, by = q[0]
        c.circle(bx + 26, by + 26, 15, "#fff", layer="ui")
        c.text(bx + 26, by + 32, str(k + 1), size=18, font="ui", fill="#111", anchor="middle", weight="bold", layer="ui")
    if fg.exists():
        c.image_file(fg, 0, 0, 1200, 1600, layer="fg")
