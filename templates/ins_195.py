"""INS-195 — ONE photo split in two windows: upper window shows the head/torso, lower window the same photo's shoes,
zoomed in; a ring of mint stars circles the shoes.  Page 13, photos: 1 (same source for both windows).
Generated-asset dependencies: none.  ctx['feet'] (normalised cx, cy) locates the shoes on real photos.
"""
from components import deco

META = {"id": "INS-195", "photos": 1, "assets": [], "family": "split-same-photo", "photo_notes": "one FULL-LENGTH photo that shows both head and shoes"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 780, focus=(0.5, 0.18), zoom=1.15)
    feet = ctx.get("feet") or (0.5, 0.9)
    # choose the cover-crop focus so the shoes land at the window centre (zoom 1.5)
    sw, sh = c.photo(0).image.size
    w, h, zoom = 1200, 740, 1.5
    scale = max(w / sw, h / sh) * zoom
    nw, nh = sw * scale, sh * scale
    fx = min(1.0, max(0.0, (feet[0] * nw - w / 2) / max(1, nw - w)))
    fy = min(1.0, max(0.0, (feet[1] * nh - h / 2) / max(1, nh - h)))
    c.photo_rect(0, 0, 820, w, h, focus=(fx, fy), zoom=zoom, lock=True)
    deco.ring_of_stars(c, 600, 1200, 300, 240, 18, 34, "#7FE7E0", seed=5)
