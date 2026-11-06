"""INS-217 — mirror selfie with the face hidden behind a soft white glow and a tiny sitting cat (G24) inside it,
plus a white bar caption 'own the moment❤❤' across the hips.  Page 14, photos: 1.  Requires master G24.
"""
from templates._assets import require
from templates._common import T, face_box

META = {"id": "INS-217", "photos": 1, "assets": ["G24"], "family": "face-mask", "photo_notes": "one full-length mirror selfie"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 1520, focus=(0.5, 0.3))
    fx, fy, fw, fh = face_box(ctx)
    cx, cy = fx * 1200, fy * 1600; r = max(fw * 1200, fh * 1600) * 0.62
    gid = c.uid("glow")
    c.defs.append(f'<radialGradient id="{gid}"><stop offset="0.55" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')
    c.circle(cx, cy, r * 1.25, f"url(#{gid})", layer="fg")
    c.image_file(require(ctx, "G24_cat_sit", "small sitting cat sticker"), cx - r * 0.35, cy - r * 0.45, r * 0.7, None, layer="fg")
    c.rect(300, 1180, 600, 56, "#fff", layer="ui")
    c.text(600, 1218, T(ctx, "cap", "own the moment❤❤"), size=26, font="ui", fill="#111", anchor="middle", layer="ui")
