"""Taste-calibration mode: render several candidate layouts for ONE photo and label them A, B, C, D ...

  python scripts/candidates.py --photo p.jpg --ids 164 103 134 162 --out ./cands [--size 1080x1350] [--date YYYY-MM-DD]
                               [--text 164:l1=... 103:...]   (per-layout text overrides, "<id>:<key>=<value>")
                               [--extra p2.jpg p3.jpg]       (more photos for multi-photo layouts; photo #1 stays first)

Writes <out>/<letter>_INS-xxx.png (+svg/recipe) and <out>/sheet.jpg (2x2 contact sheet with big letters).
Record the user's answer with scripts/taste.py (A-D = pick, E = regenerate with a new set).
"""
import argparse
import datetime as dt
import sys
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from components import render as R  # noqa: E402
from scripts.render import render_one  # noqa: E402

LETTERS = "ABCDEFGH"


def sheet(items, out, label_size=120):
    tiles = [Image.open(p).convert("RGB") for _, p in items]
    tw, th = 540, int(540 * tiles[0].height / tiles[0].width)
    cols = 2; rows = (len(tiles) + 1) // 2
    im = Image.new("RGB", (cols * (tw + 20) + 20, rows * (th + 20) + 20), "#F2F2F2")
    try:
        font = ImageFont.truetype("arialbd.ttf", label_size)
    except OSError:
        font = ImageFont.load_default()
    d = ImageDraw.Draw(im)
    for k, ((letter, _), t) in enumerate(zip(items, tiles)):
        r, c = divmod(k, cols)
        x, y = 20 + c * (tw + 20), 20 + r * (th + 20)
        im.paste(t.resize((tw, th)), (x, y))
        d.rounded_rectangle([x + 16, y + 16, x + 16 + label_size * 1.1, y + 16 + label_size * 1.1], radius=20, fill=(0, 0, 0, 200))
        d.text((x + 16 + label_size * 0.55, y + 16 + label_size * 0.52), letter, fill="#FFD60A", font=font, anchor="mm")
    im.save(out, quality=88)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo", required=True)
    ap.add_argument("--extra", nargs="*", default=[])
    ap.add_argument("--ids", nargs="*", default=[])
    ap.add_argument("--auto", action="store_true", help="pick ids with scripts/recommend.py")
    ap.add_argument("--exclude", nargs="*", default=[], help="ids already shown for this photo (never repeat after E)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1080x1350")
    ap.add_argument("--date")
    ap.add_argument("--text", nargs="*", default=[])
    a = ap.parse_args()
    w, h = (int(v) for v in a.size.lower().split("x"))
    date = dt.date.fromisoformat(a.date) if a.date else None
    texts = {}
    for t in a.text:
        lid, _, kv = t.partition(":")
        k, _, v = kv.partition("=")
        texts.setdefault(lid.zfill(3), {})[k] = v
    ids = a.ids
    if a.auto or not ids:
        from scripts.recommend import recommend
        rec = recommend([a.photo], 4, a.exclude)[0]
        ids = [c["id"] for c in rec["candidates"]]
        print("auto:", ", ".join(f"{c['id']} ({c['family']} {c['score']:+.1f})" for c in rec["candidates"]))
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    items = []
    try:
        for letter, lid in zip(LETTERS, ids):
            lid3 = lid[-3:].zfill(3)
            png = render_one(f"INS-{lid3}", [a.photo] + a.extra, out, date, texts.get(lid3, {}), (w, h))
            final = out / f"{letter}_INS-{lid3}.png"
            png.replace(final)
            for ext in (".svg", ".recipe.json"):
                p = out / f"INS-{lid3}{ext}"
                if p.exists():
                    p.replace(out / f"{letter}_INS-{lid3}{ext}")
            items.append((letter, final))
            print(f"{letter} = INS-{lid3} -> {final.name}")
    finally:
        R.close()
    s = sheet(items, out / "sheet.jpg")
    print("sheet ->", s)


if __name__ == "__main__":
    main()
