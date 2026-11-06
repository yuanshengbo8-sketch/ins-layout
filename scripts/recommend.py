"""Recommend candidate layouts for real photos.

  python scripts/recommend.py photo1.jpg [photo2.jpg ...] [--n 4] [--json] [--exclude 203 167]

Scoring per (photo, layout):
  fit      - how much of the measured head the layout's overlay would cover (from assets/overlay), framing needs
             (full-length layouts need feet, close-up layouts want a big head), orientation
  taste    - picks/rejects per family from reports/taste.jsonl plus the SKILL.md taste profile boosts
  variety  - candidates for one photo come from different families; no layout repeats across the batch
The last slot of each set is a "control": the best-scoring layout from a family the user has NOT picked yet, so
the taste log keeps learning instead of only confirming itself.
"""
import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK))

from components import detect  # noqa: E402

OVERLAY = SK / "assets" / "overlay"
PREFERRED = {"ui-message": 1.0, "caption-notes": 1.0, "camera-hud": 0.9, "colour-card": 0.9, "ui-calendar": 0.6, "ui-music": 0.6,
             "ui-focus": 0.5, "ui-weather": 0.5, "ui-dialog": 0.4, "ui-picker": 0.3, "ui-album": 0.3}
DISLIKED = {"face-stickers": -1.2, "sticker-stars": -0.8, "sticker-tags": -0.8, "sticker-caption": -0.6, "letter-rain": -1.0,
            "split-words": -0.8, "big-words": -0.5, "face-mask": -1.5, "pixel-fragments": -0.6, "word-cloud": -0.6, "ui-browser": -0.4,
            "ui-share": -0.4, "ui-ticket": -0.4}
NEEDS_FEET = {"INS-195"}
CLOSEUP_OK = {"INS-056", "INS-134", "INS-142", "INS-143", "INS-145", "INS-162", "INS-173", "INS-212", "INS-218", "INS-208", "INS-206"}


def load_status():
    st = json.loads((SK / "status.json").read_text("utf-8"))["layouts"]
    eff = json.loads((SK / "effects.json").read_text("utf-8"))["layouts"]
    ready = {k: v for k, v in st.items() if v.get("status") == "ready"}
    return ready, eff


def taste_weights():
    picks, rejects = Counter(), Counter()
    p = SK / "reports" / "taste.jsonl"
    if p.exists():
        for ln in p.read_text("utf-8").splitlines():
            r = json.loads(ln)
            eff = json.loads((SK / "effects.json").read_text("utf-8"))["layouts"]
            if r.get("pick"):
                picks[eff.get(r["pick"], {}).get("family", "?")] += 1
            for i in r.get("rejected", []):
                rejects[eff.get(i, {}).get("family", "?")] += 1
    return picks, rejects


def measure_photo(path):
    m = detect.measure(path)
    w, h = m["size"]
    head = m["faces"][0] if m["faces"] else None
    return {"path": str(path), "w": w, "h": h, "portrait": h >= w, "head": head, "feet": m["feet"],
            "head_frac": head["w"] if head else 0.0}


def head_overlap(lid, photo):
    """Fraction of the head box covered by overlay when the photo fills the layout's main window (face-centred crop)."""
    idx = json.loads((OVERLAY / "index.json").read_text("utf-8")) if (OVERLAY / "index.json").exists() else {}
    if lid not in idx or not photo["head"] or not (OVERLAY / f"{lid}.png").exists():
        return 0.0
    win = idx[lid]["window"]
    from PIL import ImageFilter
    # dilate thin strokes into the region they occupy (a line of text counts as its box, not its ink)
    mask = np.asarray(Image.open(OVERLAY / f"{lid}.png").convert("L").filter(ImageFilter.MaxFilter(5))) > 127  # 160x120
    # window in canvas px
    wx0, wy0, wx1, wy1 = win[0] * 1200, win[1] * 1600, win[2] * 1200, win[3] * 1600
    ww, wh = wx1 - wx0, wy1 - wy0
    sw, sh = photo["w"], photo["h"]
    scale = max(ww / sw, wh / sh)
    nw, nh = sw * scale, sh * scale
    hd = photo["head"]
    fx = hd["cx"] if nw > ww + 1 else 0.5
    fy = min(1.0, max(0.0, hd["cy"] - 0.10)) if nh > wh + 1 else 0.5
    ox = (nw - ww) * fx; oy = (nh - wh) * fy
    # head box in canvas px
    hx0 = wx0 + (hd["cx"] - hd["w"] / 2) * nw - ox; hx1 = hx0 + hd["w"] * nw
    hy0 = wy0 + (hd["cy"] - hd["h"] / 2) * nh - oy; hy1 = hy0 + hd["h"] * nh
    # to mask coords (120x160 over the full canvas)
    X0, X1 = int(max(0, hx0 / 10)), int(min(120, hx1 / 10)); Y0, Y1 = int(max(0, hy0 / 10)), int(min(160, hy1 / 10))
    if X1 <= X0 or Y1 <= Y0:
        return 0.0
    sub = mask[Y0:Y1, X0:X1]
    return float(sub.mean())


def adaptive(lid):
    """Layouts that place their elements from the measured face box keep clear of the head by construction."""
    p = SK / "templates" / f"ins_{lid[-3:]}.py"
    return p.exists() and "face_box(" in p.read_text("utf-8")


def score(lid, fam, photo, picks, rejects):
    s = 0.0; why = []
    ov = 0.0 if adaptive(lid) else head_overlap(lid, photo)
    if ov > 0.02:
        s -= 3.0 * ov; why.append(f"covers {ov:.0%} of head")
    if lid in NEEDS_FEET:
        if not photo["feet"]:
            return None
        why.append("full-length, feet found")
    hf = photo["head_frac"]
    if hf >= 0.22 and lid not in CLOSEUP_OK and fam in ("big-words",):
        s -= 0.4; why.append("close-up vs big text")
    if hf and hf < 0.10 and fam in ("face-stickers", "letter-rain", "face-mask"):
        s -= 1.0; why.append("head too small for face layouts")
    if not photo["portrait"]:
        s -= 0.5; why.append("landscape photo")
    s += PREFERRED.get(fam, 0.0) + DISLIKED.get(fam, 0.0)
    s += 0.6 * picks.get(fam, 0) - 0.25 * rejects.get(fam, 0)
    return s, why


def recommend(photo_paths, n=4, exclude=()):
    ready, eff = load_status()
    picks, rejects = taste_weights()
    used = set(f"INS-{e[-3:]}" for e in exclude)
    out = []
    for path in photo_paths:
        photo = measure_photo(path)
        scored = []
        for lid, st in ready.items():
            if lid in used or eff.get(lid, {}).get("photos", 1) != 1:
                continue
            fam = eff.get(lid, {}).get("family", "?")
            r = score(lid, fam, photo, picks, rejects)
            if r is None:
                continue
            scored.append((r[0], lid, fam, r[1]))
        scored.sort(reverse=True)
        chosen, fams = [], set()
        for sc, lid, fam, why in scored:
            if fam in fams:
                continue
            chosen.append({"id": lid, "family": fam, "score": round(sc, 2), "why": why}); fams.add(fam)
            if len(chosen) == n - 1:
                break
        # control slot: best from a family never picked yet
        for sc, lid, fam, why in scored:
            if fam in fams or picks.get(fam, 0) > 0:
                continue
            chosen.append({"id": lid, "family": fam, "score": round(sc, 2), "why": why + ["control: unpicked family"]}); break
        used.update(c["id"] for c in chosen)
        out.append({"photo": str(path), "head": photo["head"], "feet": photo["feet"], "candidates": chosen})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photos", nargs="+")
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--exclude", nargs="*", default=[])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    res = recommend(a.photos, a.n, a.exclude)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1, default=lambda o: round(o, 3) if isinstance(o, float) else str(o)))
    else:
        for r in res:
            print(Path(r["photo"]).name, "head", {k: round(v, 2) for k, v in r["head"].items() if isinstance(v, float)} if r["head"] else None)
            for k, c in zip("ABCDEFGH", r["candidates"]):
                print(f"  {k} {c['id']} {c['family']:14} {c['score']:+.2f}  {'; '.join(c['why'])}")


if __name__ == "__main__":
    main()
