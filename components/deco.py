"""Vector decorations: stars, hearts, drops, clouds, dotted question marks, arrows, frames, cables, bows."""
import math
import random

from .core import Canvas


def star_path(cx, cy, r, inner=0.45, points=5, rot=-90):
    pts = []
    for i in range(points * 2):
        ang = math.radians(rot + i * 180 / points)
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


def star(c: Canvas, cx, cy, r, fill="#000", *, stroke=None, w=2, inner=0.45, rot=-90, layer="deco", opacity=1.0):
    c.path(star_path(cx, cy, r, inner, 5, rot), fill=fill, stroke=stroke, w=w, layer=layer, opacity=opacity)


def sparkle(c: Canvas, cx, cy, r, fill="#fff", *, layer="deco", opacity=1.0):
    """4-point thin sparkle."""
    c.path(star_path(cx, cy, r, 0.22, 4, -90), fill=fill, layer=layer, opacity=opacity)


def scatter_stars(c: Canvas, box, n, r_range=(10, 22), fill="#000", seed=1, *, layer="deco", avoid=None, inner=0.45):
    """Scatter n stars inside box=(x,y,w,h), skipping an avoid box (face region)."""
    rnd = random.Random(seed)
    x, y, w, h = box
    placed = 0; tries = 0
    while placed < n and tries < n * 30:
        tries += 1
        px, py = x + rnd.random() * w, y + rnd.random() * h
        if avoid and avoid[0] <= px <= avoid[0] + avoid[2] and avoid[1] <= py <= avoid[1] + avoid[3]:
            continue
        star(c, px, py, rnd.uniform(*r_range), fill, rot=rnd.uniform(-110, -70), layer=layer, inner=inner)
        placed += 1


def heart(c: Canvas, cx, cy, s, fill="#fff", *, stroke=None, w=2, layer="deco", rotate=0):
    d = (f"M{cx} {cy + s * 0.9} C{cx - s * 1.6} {cy - s * 0.2}, {cx - s * 0.8} {cy - s * 1.2}, {cx} {cy - s * 0.35} "
         f"C{cx + s * 0.8} {cy - s * 1.2}, {cx + s * 1.6} {cy - s * 0.2}, {cx} {cy + s * 0.9} Z")
    extra = f' transform="rotate({rotate} {cx} {cy})"' if rotate else ""
    c.path(d, fill=fill, stroke=stroke, w=w, layer=layer, extra=extra)


def drop(c: Canvas, cx, cy, s, fill="#3FB4F5", *, layer="deco", rotate=0, highlight=True, stroke="#fff", w=3):
    """Teardrop (round bottom, pointed top)."""
    d = f"M{cx} {cy - s} C{cx + s * 0.55} {cy - s * 0.2}, {cx + s * 0.75} {cy + s * 0.2}, {cx} {cy + s} C{cx - s * 0.75} {cy + s * 0.2}, {cx - s * 0.55} {cy - s * 0.2}, {cx} {cy - s} Z"
    extra = f' transform="rotate({rotate} {cx} {cy})"' if rotate else ""
    c.path(d, fill=fill, stroke=stroke, w=w, layer=layer, extra=extra)
    if highlight:
        c.raw(f'<ellipse cx="{cx - s * 0.22}" cy="{cy + s * 0.25}" rx="{s * 0.12}" ry="{s * 0.22}" fill="rgba(255,255,255,0.8)"{extra}/>', layer)


def cloud(c: Canvas, cx, cy, s, fill="#fff", *, stroke="#999", w=2, layer="deco", face=False):
    d = (f"M{cx - s} {cy + s * 0.4} A{s * 0.55} {s * 0.55} 0 0 1 {cx - s * 0.7} {cy - s * 0.45} "
         f"A{s * 0.7} {s * 0.7} 0 0 1 {cx + s * 0.3} {cy - s * 0.6} A{s * 0.6} {s * 0.6} 0 0 1 {cx + s * 1.05} {cy} "
         f"A{s * 0.45} {s * 0.45} 0 0 1 {cx + s * 0.9} {cy + s * 0.65} L{cx - s * 0.8} {cy + s * 0.65} A{s * 0.4} {s * 0.4} 0 0 1 {cx - s} {cy + s * 0.4} Z")
    c.path(d, fill=fill, stroke=stroke, w=w, layer=layer)
    if face:
        c.circle(cx - s * 0.2, cy, s * 0.12, "#222", layer=layer)
        c.circle(cx + s * 0.3, cy, s * 0.12, "#222", layer=layer)
        c.path(f"M{cx - s * 0.1} {cy + s * 0.3} Q{cx + s * 0.05} {cy + s * 0.15} {cx + s * 0.2} {cy + s * 0.3}", stroke="#222", w=2, layer=layer)


def dotted_glyph(c: Canvas, x, y, text, size, *, font="sans_black", fill="#fff", dot="#C9C9C9", spacing=11, layer="deco", rotate=0, anchor="start"):
    """Halftone-filled text (e.g. '?' in INS-145/148/162): text filled with a dot pattern + white underlay."""
    pid = c.uid("dots")
    c.defs.append(f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="{spacing}" height="{spacing}">'
                  f'<rect width="{spacing}" height="{spacing}" fill="{fill}"/><circle cx="{spacing / 2}" cy="{spacing / 2}" r="{spacing * 0.3}" fill="{dot}"/></pattern>')
    c.text(x, y, text, size=size, font=font, fill=f"url(#{pid})", weight="900", layer=layer, rotate=rotate, anchor=anchor)


def question_3d(c: Canvas, cx, cy, size, *, layer="deco", rotate=0, color=("#CFE4FF", "#2F6FD6")):
    """Glossy blue 3D-ish question mark (INS-150): gradient fill + dark offset + white highlight."""
    gid = c.gradient([(0, color[0]), (0.55, "#6FA4F2"), (1, color[1])], 0, 0, 0.3, 1)
    extra = f' transform="rotate({rotate} {cx} {cy})"' if rotate else ""
    c.raw(f'<text x="{cx + size * 0.05}" y="{cy + size * 0.05}" font-family="Arial Black, Arial" font-weight="900" font-size="{size}" fill="#1C4DA8" text-anchor="middle" dominant-baseline="middle"{extra}>?</text>', layer)
    c.raw(f'<text x="{cx}" y="{cy}" font-family="Arial Black, Arial" font-weight="900" font-size="{size}" fill="url(#{gid})" text-anchor="middle" dominant-baseline="middle"{extra}>?</text>', layer)
    c.raw(f'<ellipse cx="{cx - size * 0.1}" cy="{cy - size * 0.28}" rx="{size * 0.09}" ry="{size * 0.05}" fill="rgba(255,255,255,0.85)"{extra}/>', layer)


def hand_arrow(c: Canvas, x1, y1, x2, y2, *, stroke="#222", w=3, layer="deco", curve=0.25, head=14):
    """Hand-drawn style curved arrow from (x1,y1) to (x2,y2)."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    px, py = mx - dy * curve, my + dx * curve
    c.path(f"M{x1} {y1} Q{px} {py} {x2} {y2}", stroke=stroke, w=w, layer=layer)
    ang = math.atan2(y2 - py, x2 - px)
    for s in (-1, 1):
        a = ang + s * math.radians(150)
        c.path(f"M{x2} {y2} L{x2 + head * math.cos(a)} {y2 + head * math.sin(a)}", stroke=stroke, w=w, layer=layer)


def big_arrow(c: Canvas, x, y, L, *, dir="down", fill="#fff", layer="deco", w=22, head=40):
    """Thick solid arrow (INS-211)."""
    if dir == "down":
        d = f"M{x - w / 2} {y} H{x + w / 2} V{y + L - head} H{x + head * 0.9} L{x} {y + L} L{x - head * 0.9} {y + L - head} H{x - w / 2} Z"
    else:  # diagonal up-left (dx,dy given as dir tuple)
        d = f"M{x - w / 2} {y} H{x + w / 2} V{y + L - head} H{x + head * 0.9} L{x} {y + L} L{x - head * 0.9} {y + L - head} H{x - w / 2} Z"
    c.path(d, fill=fill, layer=layer)


def polaroid(c: Canvas, i, x, y, w, *, layer="photos", rotate=0, pad=18, bottom=70, caption=None, shadow=True, fill="#fff", focus=(0.5, 0.4)):
    """Polaroid frame with photo i; returns total height."""
    ph = w - 2 * pad
    h = ph + pad + bottom
    cx, cy = x + w / 2, y + h / 2
    g = f'<g transform="rotate({rotate} {cx} {cy})">' if rotate else "<g>"
    c.add(layer, g)
    if shadow:
        fid = c.drop_shadow_filter(0, 6, 10, "rgba(0,0,0,0.3)")
        c.rect(x, y, w, h, fill, layer=layer, extra=f' filter="url(#{fid})"')
    else:
        c.rect(x, y, w, h, fill, layer=layer)
    c.photo_rect(i, x + pad, y + pad, ph, ph, layer=layer, focus=focus)
    if caption:
        c.text(cx, y + ph + pad + bottom * 0.62, caption, size=bottom * 0.32, font="hand", fill="#333", anchor="middle", layer=layer)
    c.add(layer, "</g>")
    return h


def film_strip(c: Canvas, photos, x, y, w, *, layer="photos", gap=10, n=4, cell_h=None, fill="#111", holes=True):
    """Vertical photo-booth strip."""
    ch = cell_h or w * 1.25
    h = n * ch + (n + 1) * gap
    c.rect(x, y, w, h, fill, layer=layer)
    for k in range(n):
        i = photos[k % len(photos)]
        c.photo_rect(i, x + gap, y + gap + k * (ch + gap), w - 2 * gap, ch, layer=layer)
    return h


def folder_icon(c: Canvas, x, y, w, *, fill="#3EA6FF", layer="deco", label=None, label_color="#fff", label_size=18):
    h = w * 0.78
    c.path(f"M{x} {y + h * 0.18} Q{x} {y + h * 0.1} {x + w * 0.05} {y + h * 0.1} H{x + w * 0.38} L{x + w * 0.46} {y + h * 0.2} H{x + w * 0.95} Q{x + w} {y + h * 0.2} {x + w} {y + h * 0.28} V{y + h * 0.92} Q{x + w} {y + h} {x + w * 0.95} {y + h} H{x + w * 0.05} Q{x} {y + h} {x} {y + h * 0.92} Z", fill=fill, layer=layer)
    c.rect(x, y + h * 0.32, w, h * 0.68, "#5DB7FF", layer=layer, rx=w * 0.05)
    if label:
        c.text(x + w / 2, y + h + label_size * 1.2, label, size=label_size, font="sans", fill=label_color, anchor="middle", layer=layer)
    return h


def document_icon(c: Canvas, x, y, w, *, fill="#fff", layer="deco", stroke="#CCC", label=None, label_color="#fff", label_size=18):
    h = w * 1.25; f = w * 0.3
    c.path(f"M{x} {y} H{x + w - f} L{x + w} {y + f} V{y + h} H{x} Z", fill=fill, stroke=stroke, w=1.5, layer=layer)
    c.path(f"M{x + w - f} {y} V{y + f} H{x + w}", fill="#E8E8E8", stroke=stroke, w=1.5, layer=layer)
    if label:
        c.text(x + w / 2, y + h + label_size * 1.2, label, size=label_size, font="sans", fill=label_color, anchor="middle", layer=layer)
    return h


def earphone_cable(c: Canvas, pts, *, stroke="#fff", w=5, layer="deco", buds=True, bud_r=16):
    """Smooth cable through points [(x,y)...]; first two points get ear-buds."""
    d = f"M{pts[0][0]} {pts[0][1]}"
    for k in range(1, len(pts) - 1):
        x0, y0 = pts[k]; x1, y1 = pts[k + 1]
        d += f" Q{x0} {y0} {(x0 + x1) / 2} {(y0 + y1) / 2}"
    d += f" T{pts[-1][0]} {pts[-1][1]}"
    c.path(d, stroke=stroke, w=w, layer=layer)
    if buds:
        for (x, y) in pts[:1]:
            c.circle(x, y, bud_r, stroke, layer=layer)


def bow(c: Canvas, cx, cy, s, fill="#F5A3B5", *, stroke="#E5607F", layer="deco", w=3):
    """Ribbon bow (INS-143)."""
    for sgn in (-1, 1):
        c.path(f"M{cx} {cy} C{cx + sgn * s * 0.6} {cy - s * 0.9}, {cx + sgn * s * 1.4} {cy - s * 0.6}, {cx + sgn * s * 1.1} {cy + s * 0.1} "
               f"C{cx + sgn * s * 0.9} {cy + s * 0.5}, {cx + sgn * s * 0.3} {cy + s * 0.3}, {cx} {cy} Z", fill=fill, stroke=stroke, w=w, layer=layer)
        c.path(f"M{cx} {cy} L{cx + sgn * s * 0.45} {cy + s * 1.3} L{cx + sgn * s * 0.15} {cy + s * 1.15} Z", fill=fill, stroke=stroke, w=w, layer=layer)
    c.circle(cx, cy, s * 0.22, fill, stroke=stroke, stroke_w=w, layer=layer)


def ring_of_stars(c: Canvas, cx, cy, rx, ry, n, r, fill="#7FE7E0", *, seed=2, layer="deco"):
    rnd = random.Random(seed)
    for k in range(n):
        a = 2 * math.pi * k / n + rnd.uniform(-0.15, 0.15)
        star(c, cx + rx * math.cos(a), cy + ry * math.sin(a), r * rnd.uniform(0.6, 1.3), fill, rot=rnd.uniform(-110, -70), layer=layer)


def pixel_blocks(c: Canvas, cells, size, fill="#F9B4D9", *, layer="deco", origin=(0, 0)):
    """Pixel-fragment blocks at grid cells [(col,row,w,h)] * size."""
    ox, oy = origin
    for col, row, w, h in cells:
        c.rect(ox + col * size, oy + row * size, w * size, h * size, fill, layer=layer)


def corner_marks(c: Canvas, x, y, w, h, *, stroke="#E05050", L=14, sw=2, layer="deco"):
    """Red crop/focus corner marks (INS-130)."""
    for (px, py, sx, sy) in ((x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        c.path(f"M{px} {py + sy * L} V{py} H{px + sx * L}", stroke=stroke, w=sw, layer=layer, cap="butt")


def checker_tiles(c: Canvas, x, y, w, h, n, *, fill="#D9D9D9", line="#B8B8B8", layer="bg"):
    """Flat tile grid (used only as a NON-perspective fallback when a ground master is missing)."""
    c.rect(x, y, w, h, fill, layer=layer)
    for k in range(1, n):
        c.line(x + w * k / n, y, x + w * k / n, y + h, line, 3, layer=layer)
        c.line(x, y + h * k / n, x + w, y + h * k / n, line, 3, layer=layer)


def dot_pattern_rect(c: Canvas, x, y, w, h, *, bg="#D6D6D6", dot="#FFFFFF", spacing=18, r=3, layer="bg"):
    pid = c.uid("dp")
    c.defs.append(f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="{spacing}" height="{spacing}">'
                  f'<rect width="{spacing}" height="{spacing}" fill="{bg}"/><circle cx="{spacing / 2}" cy="{spacing / 2}" r="{r}" fill="{dot}"/></pattern>')
    c.rect(x, y, w, h, f"url(#{pid})", layer=layer)


def heart_border(c: Canvas, x, y, w, h, *, bg="#000", fg="#fff", spacing=46, size=11, layer="bg"):
    c.rect(x, y, w, h, bg, layer=layer)
    for px in range(int(x + spacing / 2), int(x + w), spacing):
        heart(c, px, y + 22, size, fg, layer=layer)
        heart(c, px, y + h - 22, size, fg, layer=layer)
    for py in range(int(y + spacing), int(y + h - spacing / 2), spacing):
        heart(c, x + 22, py, size, fg, layer=layer)
        heart(c, x + w - 22, py, size, fg, layer=layer)


def gingham(c: Canvas, x, y, w, h, *, col="#C9CDD3", bg="#F1F2F4", cell=70, layer="bg"):
    pid = c.uid("gg")
    c.defs.append(f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="{cell}" height="{cell}">'
                  f'<rect width="{cell}" height="{cell}" fill="{bg}"/><rect width="{cell / 2}" height="{cell}" fill="{col}" opacity="0.45"/>'
                  f'<rect width="{cell}" height="{cell / 2}" fill="{col}" opacity="0.45"/></pattern>')
    c.rect(x, y, w, h, f"url(#{pid})", layer=layer)
