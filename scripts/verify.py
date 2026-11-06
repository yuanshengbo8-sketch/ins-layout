"""Batch structural verification.

  python scripts/verify.py                 # every implemented layout with test images
  python scripts/verify.py 053 033 220     # only these
  python scripts/verify.py --sheet         # also write previews/contact_sheet.jpg (crop | render side by side)

For each layout: render with assets/test images -> previews/structure/<ID>.png, compare side by side with the
reference crop into previews/compare/<ID>.jpg, and record technical result + dependency hashes in status.json.
Visual judgement is NOT automated: open previews/compare/<ID>.jpg, look, then set `visual` via scripts/status.py.
"""
import datetime as dt
import hashlib
import json
import sys
import time
import traceback
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK))

from PIL import Image  # noqa: E402

from components import render as R  # noqa: E402
import templates  # noqa: E402
from scripts.render import render_one  # noqa: E402
from templates._text import AssetMissing  # noqa: E402

STATUS = SK / "status.json"
TEST = sorted(SK.glob("assets/test/test*.jpg"))


def dep_hash(layout_id):
    h = hashlib.sha1()
    for p in [templates.module_path(layout_id), SK / "components" / "core.py", SK / "components" / "ui.py", SK / "components" / "deco.py", SK / "components" / "imaging.py"]:
        if p and p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()[:12]


def compare(layout_id, render_png):
    crop = SK / "references" / "crops" / f"{layout_id}.png"
    if not crop.exists():  # public releases do not carry the original reference pages
        return render_png
    a = Image.open(crop).convert("RGB").resize((600, 800))
    b = Image.open(render_png).convert("RGB").resize((600, 800))
    sheet = Image.new("RGB", (1220, 800), "#fff")
    sheet.paste(a, (0, 0)); sheet.paste(b, (620, 0))
    out = SK / "previews" / "compare" / f"{layout_id}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=85)
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    variant = next((int(a.split("=")[1]) for a in sys.argv[1:] if a.startswith("--variant=")), 1)
    sheet = "--sheet" in sys.argv
    status = json.loads(STATUS.read_text("utf-8")) if STATUS.exists() else {"layouts": {}}
    ids = [f"INS-{a[-3:]}" for a in args] if args else templates.implemented()
    results = {}
    t0 = time.time()
    for lid in ids:
        ent = status["layouts"].setdefault(lid, {})
        spec = templates.get(lid)
        need = spec.META.get("photos", 1)
        photos = [str(p) for p in TEST[:max(need, 1)]]
        try:
            png = render_one(lid, photos, SK / "previews" / "structure", dt.date(2026, 11, 5), {}, (1200, 1600), hq=False, variant=variant)
            cmp_ = compare(lid, png)
            ent.update({"technical": "pass", "structure_png": str(png.relative_to(SK)), "compare": str(cmp_.relative_to(SK)),
                        "dep_hash": dep_hash(lid), "verified_at": dt.datetime.now().isoformat(timespec="seconds"), "error": None})
            if ent.get("status") in (None, "pending", "repair") and ent.get("visual") == "pass":
                ent["status"] = "ready"
            results[lid] = "pass"
            print(f"[PASS] {lid}")
        except AssetMissing as e:
            ent.update({"technical": "blocked", "status": "blocked", "blocker": str(e), "error": None,
                        "verified_at": dt.datetime.now().isoformat(timespec="seconds")})
            results[lid] = "blocked"
            print(f"[BLOCKED] {lid}: {e}")
        except Exception as e:  # noqa
            ent.update({"technical": "fail", "error": traceback.format_exc(limit=3), "status": "repair",
                        "verified_at": dt.datetime.now().isoformat(timespec="seconds")})
            results[lid] = "fail"
            print(f"[FAIL] {lid}: {e!r}")
    R.close()
    status["last_verify"] = {"at": dt.datetime.now().isoformat(timespec="seconds"), "ids": ids, "results": results, "seconds": round(time.time() - t0, 1)}
    STATUS.write_text(json.dumps(status, indent=1, ensure_ascii=False), "utf-8")
    if sheet:
        make_sheet(ids)
    npass = sum(1 for v in results.values() if v == "pass")
    print(f"{npass}/{len(ids)} technical pass in {status['last_verify']['seconds']}s -> {STATUS}")


def make_sheet(ids):
    tiles = []
    for lid in ids:
        p = SK / "previews" / "compare" / f"{lid}.jpg"
        if p.exists():
            tiles.append((lid, Image.open(p).resize((610, 400))))
    if not tiles:
        return
    cols = 2; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 620, rows * 430), "#fff")
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    for k, (lid, im) in enumerate(tiles):
        r, c = divmod(k, cols)
        sheet.paste(im, (c * 620, r * 430 + 26))
        d.text((c * 620 + 6, r * 430 + 4), lid, fill="#000")
    out = SK / "previews" / "contact_sheet.jpg"
    sheet.save(out, quality=80)
    print("sheet ->", out)


if __name__ == "__main__":
    main()
