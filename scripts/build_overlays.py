"""Build per-layout overlay maps used by the recommender.

For each implemented layout, render twice with flat-colour stand-in photos (two greys).  Pixels that change
between the two renders belong to photo windows; pixels inside the main window that do NOT change are overlay
(text, UI, stickers, frames drawn over the photo).  Saves assets/overlay/<ID>.png (120x160, white = overlay)
and assets/overlay/index.json with each layout's main window box (normalised) and overlay ratio.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK))

from components import render as R  # noqa: E402
from scripts.render import render_one  # noqa: E402
import templates  # noqa: E402

OUT = SK / "assets" / "overlay"
FLAT = SK / "assets" / "test"


def flats(n, grey):
    paths = []
    for k in range(n):
        p = FLAT / f"flat{grey}_{k}.jpg"
        if not p.exists():
            Image.new("RGB", (1200, 1600), (grey, grey, grey)).save(p, quality=95)
        paths.append(str(p))
    return paths


def main(ids=None):
    OUT.mkdir(parents=True, exist_ok=True)
    index = json.loads((OUT / "index.json").read_text("utf-8")) if (OUT / "index.json").exists() else {}
    ids = ids or templates.implemented()
    tmp = SK / "previews" / "_overlay_tmp"
    try:
        for lid in ids:
            spec = templates.get(lid)
            n = spec.META.get("photos", 1)
            try:
                a = render_one(lid, flats(n, 118), tmp / "a", None, {}, (1200, 1600), hq=False)
                b = render_one(lid, flats(n, 150), tmp / "b", None, {}, (1200, 1600), hq=False)
            except Exception as e:  # noqa
                print(f"[skip] {lid}: {e!r}"); continue
            A = np.asarray(Image.open(a).convert("RGB")).astype(int)
            B = np.asarray(Image.open(b).convert("RGB")).astype(int)
            changed = np.abs(A - B).sum(axis=2) > 12  # photo pixels
            ys, xs = np.where(changed)
            if len(xs) == 0:
                print(f"[skip] {lid}: no photo pixels"); continue
            x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
            win = np.zeros_like(changed); win[y0:y1 + 1, x0:x1 + 1] = True
            overlay = win & ~changed
            # downscale masks to 120x160
            ov = Image.fromarray((overlay * 255).astype(np.uint8)).resize((120, 160), Image.BOX)
            ov.save(OUT / f"{lid}.png")
            ratio = float(overlay.sum()) / float(win.sum())
            index[lid] = {"window": [x0 / 1200, y0 / 1600, (x1 + 1) / 1200, (y1 + 1) / 1600], "overlay_ratio": round(ratio, 4),
                          "photos": n, "family": spec.META.get("family")}
            print(f"{lid} window={index[lid]['window']} overlay={ratio:.2f}")
    finally:
        R.close()
    (OUT / "index.json").write_text(json.dumps(index, indent=1), "utf-8")
    print(f"{len(index)} overlay maps -> {OUT}")


if __name__ == "__main__":
    main([f"INS-{a[-3:]}" for a in sys.argv[1:]] or None)
