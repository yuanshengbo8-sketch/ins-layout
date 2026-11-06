"""INS-197 — tall portrait inset on a cream page (wide side margins), with a tiny yellow italic 'morrrn' and a small
yellow butter-block sticker drawn natively beside the subject.  Page 13, photos: 1.  Generated-asset dependencies: none.
"""
from templates._common import T, face_box

META = {"id": "INS-197", "photos": 1, "assets": [], "family": "caption-notes", "photo_notes": "one portrait; the note sits beside the shoulder"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 160, 40, 880, 1520, focus=(0.5, 0.3))
    fx, fy, fw, fh = face_box(ctx)
    nx = max(200, min(900, fx * 1200 - fw * 1200 / 2 - 160)); ny = (fy + fh / 2) * 1600 + 60
    c.text(nx, ny, T(ctx, "note", "morrrn"), size=26, font="serif", fill="#F2DC5A", italic=True)
    # butter block: a small yellow prism
    bx, by = nx + 110, ny - 30
    c.path(f"M{bx} {by} L{bx + 46} {by - 10} L{bx + 60} {by + 6} L{bx + 14} {by + 16} Z", fill="#F7E27A", layer="deco")
    c.path(f"M{bx + 14} {by + 16} L{bx + 60} {by + 6} L{bx + 60} {by + 24} L{bx + 14} {by + 34} Z", fill="#E8C94A", layer="deco")
    c.path(f"M{bx} {by} L{bx + 14} {by + 16} L{bx + 14} {by + 34} L{bx} {by + 18} Z", fill="#D9B53A", layer="deco")
