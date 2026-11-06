"""INS-147 — two stacked photos; the upper one is rotated 90° (lying on its side), a row of five pale-blue dots runs
along the seam.  Page 11, photos: 2.  Generated-asset dependencies: none.
"""
META = {"id": "INS-147", "photos": 2, "assets": [], "family": "stacked-dots", "photo_notes": "#1 portrait (shown sideways), #2 portrait"}


def build(c, ctx):
    c.bg = "#EEECE7"
    # sideways photo: window 1200x720, source rotated -90 so the head faces left
    from components import imaging
    p = c.photo(0)
    im = imaging.cover_crop(p.image, 720, 1200, focus=(0.5, 0.3)).rotate(-90, expand=True)
    href = imaging.to_data_uri(im, "JPEG")
    c.add("photos", f'<image href="{href}" x="0" y="40" width="1200" height="720"/>')
    c.recipe.setdefault("windows", []).append({"photo": 0, "shape": "rect-rotated90", "box": [0, 40, 1200, 720]})
    c.photo_rect(1, 0, 800, 1200, 760, focus=(0.5, 0.35))
    for k in range(5):
        c.circle(100 + k * 250, 780, 68, "#B9DCF5", layer="deco")
