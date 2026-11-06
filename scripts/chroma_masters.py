"""Derive screen quads and foreground cut-outs from green-screen twins of the scene masters.

For each master M with a twin M_GREEN.png (same scene, screens or ground painted #00FF00):
  green mask  -> each connected green region = one photo window; its 4 corners (approxPolyDP) -> <name>_screen(s).json
  foreground  -> pixels inside the window's convex hull that are NOT green (croissant, glasses) -> <name>_fg.png (RGBA from M)
  ground type -> everything NOT green is foreground (hand, cup, shoes) -> <name>_fg.png
Coordinates are normalised to the master size.  Previews are written to assets/masters/_preview_<name>.jpg.
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFilter

SK = Path(__file__).resolve().parents[1]
M = SK / "assets" / "masters"

JOBS = {
    # name: (green twin, mode, out json, out fg, expected windows)
    "G11_table_phone_hands": ("G11_GREEN.png", "screen", "G11_screen.json", None, 1),
    "G12_breakfast_phone_croissant": ("G12_GREEN.png", "screen", "G12_screen.json", "G12_fg.png", 1),
    "dual_phone_038": ("dual_phone_038_GREEN.png", "screen", "dual_phone_038_screens.json", "dual_phone_038_fg.png", 2),
    "three_band_138": ("three_band_138_GREEN.png", "screen", "three_band_138_screens.json", None, 2),
    "G14_ground_coffee_shoes": ("G14_GREEN.png", "ground", None, "G14_fg.png", 0),
    "ground_035_tiles9": ("ground_035_GREEN.png", "ground", None, "ground_035_fg.png", 0),
}


def green_mask(rgb):
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    m = (h > 40) & (h < 85) & (s > 120) & (v > 90)
    m = cv2.morphologyEx(m.astype(np.uint8) * 255, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    return m


def order_quad(pts):
    pts = np.array(pts, dtype=float)
    s = pts.sum(axis=1); d = pts[:, 0] - pts[:, 1]
    tl = pts[np.argmin(s)]; br = pts[np.argmax(s)]; tr = pts[np.argmax(d)]; bl = pts[np.argmin(d)]
    return [tl.tolist(), tr.tolist(), br.tolist(), bl.tolist()]


def fit_quad(contour, passes=3):
    """Corners of a screen from its contour: fit a straight line to each side and intersect them.

    Taking corners straight from the hull fails twice over: rounded phone corners give arbitrary points, and food
    or fingers in front of the screen bite into a side.  Only contour points that lie close to the current side
    and away from its ends vote, so a bite (far from the side) and the rounded corners (near the ends) are ignored.
    """
    pts = contour.reshape(-1, 2).astype(np.float32)
    quad = np.array(order_quad(cv2.boxPoints(cv2.minAreaRect(cv2.convexHull(contour)))), dtype=np.float32)
    size = np.sqrt(cv2.contourArea(cv2.convexHull(contour)))
    for tol in np.linspace(0.05, 0.02, passes) * size:
        lines = []
        for k in range(4):
            a, b = quad[k], quad[(k + 1) % 4]
            d = b - a; length = float(np.linalg.norm(d)); d = d / length
            rel = pts - a
            along = rel @ d
            dist = np.abs(rel[:, 0] * d[1] - rel[:, 1] * d[0])
            keep = (dist < tol) & (along > 0.12 * length) & (along < 0.88 * length)
            if keep.sum() < 8:  # side hidden: keep the current estimate
                lines.append((d, a)); continue
            vx, vy, x0, y0 = cv2.fitLine(pts[keep], cv2.DIST_HUBER, 0, 0.01, 0.01).ravel()
            lines.append((np.array([vx, vy]), np.array([x0, y0])))
        new = []
        for k in range(4):  # corner k sits between side k-1 and side k
            (d1, p1), (d2, p2) = lines[k - 1], lines[k]
            t = np.linalg.solve(np.array([d1, -d2]).T, p2 - p1)
            new.append(p1 + t[0] * d1)
        quad = np.array(new, dtype=np.float32)
    return quad.tolist()


def quads_from_mask(mask, n_expected):
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:n_expected]
    quads, hulls = [], []
    for c in cnts:
        quads.append(fit_quad(c)); hulls.append(cv2.convexHull(c))
    # sort left-to-right / top-to-bottom for stable indices
    order = sorted(range(len(quads)), key=lambda i: (quads[i][0][1] // 200, quads[i][0][0]))
    return [quads[i] for i in order], [hulls[i] for i in order]


def expand_variants():
    """Yield the base job plus one job per NAME__vN.png master that has a TWIN__vN.png."""
    for name, (twin, mode, out_json, out_fg, n) in JOBS.items():
        yield name, twin, mode, out_json, out_fg, n
        for v in (2, 3):
            if (M / f"{name}__v{v}.png").exists():
                sv = lambda f: f and f.replace(".", f"__v{v}.")  # noqa: E731
                yield f"{name}__v{v}", sv(twin), mode, sv(out_json), sv(out_fg), n


def main(only=None):
    for name, twin, mode, out_json, out_fg, n in expand_variants():
        if only and not any(name.startswith(o) for o in only):
            continue
        mp, tp = M / f"{name}.png", M / twin
        if not tp.exists():
            print(f"[skip] {name}: no twin {twin}"); continue
        master = Image.open(mp).convert("RGB"); green = Image.open(tp).convert("RGB").resize(master.size)
        g = green_mask(np.asarray(green))
        W, H = master.size
        if mode == "screen":
            quads, hulls = quads_from_mask(g, n)
            norm = [[[round(x / W, 4), round(y / H, 4)] for x, y in q] for q in quads]
            (M / out_json).write_text(json.dumps(norm[0] if n == 1 else norm))
            print(f"{name}: {len(quads)} window(s) -> {out_json}", norm)
            if out_fg:
                hull_mask = np.zeros((H, W), np.uint8)
                for h in hulls:
                    cv2.fillConvexPoly(hull_mask, h, 255)
                fg = (hull_mask > 0) & (g == 0)
                alpha = cv2.GaussianBlur((fg * 255).astype(np.uint8), (3, 3), 0)
                rgba = master.convert("RGBA"); rgba.putalpha(Image.fromarray(alpha)); rgba.save(M / out_fg)
                print(f"   fg -> {out_fg} ({int(fg.sum())} px)")
        else:
            fg = g == 0
            fg = cv2.morphologyEx(fg.astype(np.uint8) * 255, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
            alpha = cv2.GaussianBlur(fg, (3, 3), 0)
            rgba = master.convert("RGBA"); rgba.putalpha(Image.fromarray(alpha)); rgba.save(M / out_fg)
            print(f"{name}: ground fg -> {out_fg} ({int((fg > 0).sum())} px)")
        # preview: master with quads / fg tinted
        prev = np.asarray(master).copy()
        if mode == "screen":
            for q in quads:
                cv2.polylines(prev, [np.array(q, np.int32)], True, (255, 0, 255), 4)
        else:
            prev[fg > 0] = (prev[fg > 0] * 0.5 + np.array([255, 0, 255]) * 0.5).astype(np.uint8)
        Image.fromarray(prev).resize((W // 2, H // 2)).save(M / f"_preview_{name}.jpg", quality=85)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
