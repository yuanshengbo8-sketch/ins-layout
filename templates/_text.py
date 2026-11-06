"""Shared drawing routines for the 'big words over photo' family (page 03-13).

Each layout module still owns its own numbers (lines, anchor, size, colour, frame, extras);
this file only holds the two primitives they share.
"""
from components.core import Canvas


class AssetMissing(Exception):
    """Raised when a layout needs a generated master bitmap that does not exist yet (status: blocked)."""


def framed_photo(c: Canvas, i, frame=(0, 0, 0, 0), bg="#EEECE7", focus=(0.5, 0.4), zoom=1.0, layer="photos"):
    """Photo with a flat border; frame = (top, right, bottom, left) in canvas px."""
    t, r, b, l = frame
    if any(frame):
        c.bg = bg
    c.photo_rect(i, l, t, c.width - l - r, c.height - t - b, focus=focus, zoom=zoom, layer=layer)
    return (l, t, c.width - l - r, c.height - t - b)


def stacked(c: Canvas, lines, x, y, size, fill, *, anchor="middle", leading=1.1, weight="bold", font="sans", spacing=0,
            opacity=1.0, stroke=None, stroke_w=0, per_line=None, layer="text", italic=False):
    """Lines of display text; per_line may give (dx, dy, size_mult, fill) overrides per index."""
    yy = y
    for k, ln in enumerate(lines):
        dx, dy, sm, fl = 0, 0, 1.0, fill
        if per_line and k < len(per_line) and per_line[k]:
            o = per_line[k]
            dx, dy, sm, fl = o.get("dx", 0), o.get("dy", 0), o.get("size", 1.0), o.get("fill", fill)
        c.text(x + dx, yy + dy, ln, size=size * sm, fill=fl, anchor=anchor, weight=weight, font=font, spacing=spacing,
               opacity=opacity, stroke=stroke, stroke_w=stroke_w, layer=layer, italic=italic)
        yy += size * leading
    return yy
