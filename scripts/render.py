"""Render one layout.

  python scripts/render.py --id INS-053 --photos a.jpg b.jpg --out out/ [--date 2026-11-05] [--text key=value ...]
                           [--size 1200x1600] [--test]   (--test uses assets/test images)

Outputs <out>/<ID>.png, <out>/<ID>.svg (layered) and <out>/<ID>.recipe.json.
"""
import argparse
import os
os.environ.setdefault("GLOG_minloglevel", "2"); os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import datetime as dt
import json
import sys
import time
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK))

from components.core import Canvas, load_photos  # noqa: E402
from components import render as R  # noqa: E402
from components import detect  # noqa: E402
import templates  # noqa: E402


def build_ctx(args, photos):
    date = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    text = {}
    for kv in args.text or []:
        k, _, v = kv.partition("=")
        text[k] = v
    return {"date": date, "text": text, "n": len(photos), "assets_dir": SK / "assets", "options": {}}


def render_one(layout_id, photo_paths, out_dir, date=None, text=None, size=(1200, 1600), faces=None, feet=None, objects=None, hq=True, variant=None):
    spec = templates.get(layout_id)
    photos = load_photos(photo_paths)
    need = spec.META.get("photos", 1)
    if len(photos) < need:
        raise SystemExit(f"{layout_id} needs {need} photo(s), got {len(photos)}: {spec.META.get('photo_notes', '')}")
    c = Canvas(photos=photos, assets_dir=SK / "assets")  # design space is always 1200x1600; `size` scales the output
    # rule 08: measure real photos. Anything not supplied by the caller is detected automatically (YuNet + MediaPipe pose).
    faces = dict(faces or {}); measured = {}
    auto_feet = None
    for p in photos:
        if p.path.startswith(str(SK / "assets" / "test")):
            continue  # structure test images keep the template defaults
        if p.index not in faces or (p.index == 0 and feet is None):
            m = detect.measure(p.path)
            measured[p.index] = m
            if p.index not in faces and m["faces"]:
                f = m["faces"][0]
                faces[p.index] = (f["cx"], f["cy"], f["w"], f["h"])
            if p.index == 0 and feet is None and m["feet"]:
                auto_feet = tuple(m["feet"])
    feet = feet or auto_feet
    c.faces = {int(k): tuple(v) for k, v in faces.items()}
    if variant is None:  # stable per photo set, different between users
        variant = int(photos[0].hash[:6], 16) % 3 + 1 if photos else 1
    ctx = {"date": date or dt.date.today(), "text": text or {}, "n": len(photos), "assets_dir": SK / "assets", "options": {},
           "faces": faces, "feet": feet, "objects": objects, "variant": variant}
    t0 = time.time()
    spec.build(c, ctx)
    svg = c.svg(size)
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{layout_id}.svg").write_text(svg, "utf-8")
    png = out_dir / f"{layout_id}.png"
    if hq:
        # supersample 2x then downscale: crisper text edges and smoother sticker curves
        R.render_svg(svg, png, size[0], size[1], scale=2)
        from PIL import Image as _Im
        im = _Im.open(png); im = im.resize((size[0], size[1]), _Im.LANCZOS); im.save(png, optimize=True)
    else:
        R.render_svg(svg, png, size[0], size[1])
    recipe = {
        "id": layout_id, "size": size, "date": str(ctx["date"]), "text": ctx["text"],
        "photos": [{"index": p.index, "path": p.path, "sha1_12": p.hash} for p in photos],
        "faces": faces, "feet": feet, "objects": objects,
        "measured": {k: {"faces": v["faces"], "feet": v["feet"]} for k, v in measured.items()},
        "meta": spec.META, "recipe": c.recipe, "seconds": round(time.time() - t0, 2), "hq": hq, "variant": variant,
    }
    (out_dir / f"{layout_id}.recipe.json").write_text(json.dumps(recipe, indent=1, ensure_ascii=False, default=str), "utf-8")
    return out_dir / f"{layout_id}.png"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--photos", nargs="*", default=[])
    ap.add_argument("--out", default=str(SK / "previews" / "manual"))
    ap.add_argument("--date")
    ap.add_argument("--text", nargs="*")
    ap.add_argument("--size", default="1200x1600")
    ap.add_argument("--test", action="store_true", help="use assets/test images")
    ap.add_argument("--faces", nargs="*", help="measured face boxes per photo index: 0=cx,cy,w,h (normalised 0..1)")
    ap.add_argument("--variant", type=int, help="scene variant 1-3 (default: chosen from the photo hash)")
    ap.add_argument("--feet", help="normalised shoe centre cx,cy of photo #1 (INS-195)")
    a = ap.parse_args()
    lid = a.id.upper() if a.id.upper().startswith("INS-") else f"INS-{a.id}"
    photos = a.photos
    if a.test or not photos:
        photos = sorted(str(p) for p in (SK / "assets" / "test").glob("test*.jpg"))
    w, h = (int(v) for v in a.size.lower().split("x"))
    date = dt.date.fromisoformat(a.date) if a.date else None
    text = dict(kv.partition("=")[::2] for kv in (a.text or []))
    faces = {}
    for f in a.faces or []:
        k, _, v = f.partition("=")
        faces[int(k)] = tuple(float(x) for x in v.split(","))
    feet = tuple(float(x) for x in a.feet.split(",")) if a.feet else None
    try:
        out = render_one(lid, photos, a.out, date, text, (w, h), faces, feet, variant=a.variant)
        print("rendered", out)
    finally:
        R.close()


if __name__ == "__main__":
    main()
