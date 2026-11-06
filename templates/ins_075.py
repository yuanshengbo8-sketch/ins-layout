"""INS-075 — full photo with a pink Sims-style plumbob above the head and five small iOS tag pills floating
around the shoulders (Go on A Date, Buy Flight to Bali, Sleep, Go on SSENSE, Buy a Vintage Car).
Page 5, photos: 1.  Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T, face_box

META = {"id": "INS-075", "photos": 1, "assets": [], "family": "sticker-tags", "photo_notes": "one portrait photo with the head in the upper third"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 70, 1200, 1460, focus=(0.5, 0.3))
    fx, fy, fw, fh = face_box(ctx)
    hx, hy = fx * 1200, (fy - fh / 2) * 1600 - 40
    # plumbob
    gid = c.gradient([(0, "#F7A8F0"), (1, "#B51FB0")])
    c.path(f"M{hx} {hy - 150} L{hx + 38} {hy - 75} L{hx} {hy} L{hx - 38} {hy - 75} Z", fill=f"url(#{gid})", layer="deco")
    c.path(f"M{hx} {hy - 150} L{hx + 38} {hy - 75} L{hx} {hy - 60} Z", fill="rgba(255,255,255,0.35)", layer="deco")
    tags = [(270, 430, "🍸", T(ctx, "t1", "Go on A Date")), (740, 410, "✈", T(ctx, "t2", "Buy Flight to Bali")),
            (230, 590, "💤", T(ctx, "t3", "Sleep")), (810, 580, "🥂", T(ctx, "t4", "Go on SSENSE")),
            (690, 740, "🚗", T(ctx, "t5", "Buy a Vintage Car"))]
    for x, y, ic, s in tags:
        ui.pill(c, x, y, s, size=24, fill="#EAF3FB", color="#1C4F8C", pad=16, h=46, weight="bold", icon=ic, stroke="#C9DDF0")
