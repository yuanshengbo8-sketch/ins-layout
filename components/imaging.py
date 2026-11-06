"""Bitmap helpers: cover-crop, perspective warp into a canvas-sized RGBA layer, data URIs."""
import base64
import hashlib
import io
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps


def load_photo(path) -> Image.Image:
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    return im.convert("RGB")


def file_hash(path) -> str:
    h = hashlib.sha1()
    h.update(Path(path).read_bytes())
    return h.hexdigest()[:12]


def cover_crop(im: Image.Image, w: int, h: int, focus=(0.5, 0.45), zoom=1.0) -> Image.Image:
    """Scale/crop `im` to exactly (w,h) keeping aspect (like CSS object-fit: cover).

    focus = (fx, fy) in 0..1 picks which part of the source stays when cropping.
    zoom > 1 crops tighter around the focus point.
    """
    w, h = int(round(w)), int(round(h))
    sw, sh = im.size
    scale = max(w / sw, h / sh) * zoom
    nw, nh = max(w, int(round(sw * scale))), max(h, int(round(sh * scale)))
    im2 = im.resize((nw, nh), Image.LANCZOS)
    fx, fy = focus
    x0 = int(round((nw - w) * fx))
    y0 = int(round((nh - h) * fy))
    return im2.crop((x0, y0, x0 + w, y0 + h))


def _find_coeffs(src_pts, dst_pts):
    matrix = []
    for (x, y), (u, v) in zip(dst_pts, src_pts):
        matrix.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        matrix.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    A = np.array(matrix, dtype=float)
    B = np.array([c for pt in src_pts for c in pt], dtype=float)
    res = np.linalg.solve(A, B)
    return res.tolist()


def perspective_layer(im: Image.Image, quad, canvas_size, supersample=2) -> Image.Image:
    """Map the full image onto `quad` = [(x,y) TL, TR, BR, BL] in canvas pixels.

    Returns an RGBA layer of canvas_size, transparent outside the quad.
    """
    W, H = canvas_size
    ss = supersample
    xs = [p[0] for p in quad]; ys = [p[1] for p in quad]
    bx0, by0 = max(0, int(min(xs)) - 2), max(0, int(min(ys)) - 2)
    bx1, by1 = min(W, int(max(xs)) + 3), min(H, int(max(ys)) + 3)
    bw, bh = (bx1 - bx0) * ss, (by1 - by0) * ss
    # quad relative to bbox, supersampled
    q = [((x - bx0) * ss, (y - by0) * ss) for x, y in quad]
    src = im.convert("RGBA")
    # pre-scale source so its longest edge is about the quad size (quality + speed)
    tw = max(np.hypot(q[1][0] - q[0][0], q[1][1] - q[0][1]), np.hypot(q[2][0] - q[3][0], q[2][1] - q[3][1]))
    th = max(np.hypot(q[3][0] - q[0][0], q[3][1] - q[0][1]), np.hypot(q[2][0] - q[1][0], q[2][1] - q[1][1]))
    sw, sh = src.size
    f = min(max(tw / sw, th / sh) * 1.2, 1.0) if sw > tw and sh > th else 1.0
    if f < 1.0:
        src = src.resize((max(1, int(sw * f)), max(1, int(sh * f))), Image.LANCZOS)
    sw, sh = src.size
    coeffs = _find_coeffs([(0, 0), (sw, 0), (sw, sh), (0, sh)], q)
    warped = src.transform((bw, bh), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    # clean alpha mask from polygon so edges are crisp and nothing bleeds outside
    from PIL import ImageDraw
    mask = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(mask).polygon(q, fill=255)
    warped.putalpha(Image.fromarray(np.minimum(np.asarray(warped.split()[3]), np.asarray(mask))))
    if ss > 1:
        warped = warped.resize((bw // ss, bh // ss), Image.LANCZOS)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(warped, (bx0, by0))
    return layer


def to_data_uri(im: Image.Image, fmt="PNG", quality=92) -> str:
    buf = io.BytesIO()
    if fmt.upper() == "JPEG":
        im.convert("RGB").save(buf, "JPEG", quality=quality)
        mime = "image/jpeg"
    else:
        im.save(buf, "PNG")
        mime = "image/png"
    return f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()


def rotate_layer(im: Image.Image, angle: float, expand=True) -> Image.Image:
    return im.convert("RGBA").rotate(angle, resample=Image.BICUBIC, expand=expand)


def dominant_colors(im: Image.Image, boxes, k=3):
    """Average colour inside each (x0,y0,x1,y1) box of `im` -> list of hex strings."""
    out = []
    for b in boxes[:k]:
        reg = np.asarray(im.crop(b).convert("RGB")).reshape(-1, 3)
        med = np.median(reg, axis=0)
        out.append("#%02X%02X%02X" % tuple(int(v) for v in med))
    return out
