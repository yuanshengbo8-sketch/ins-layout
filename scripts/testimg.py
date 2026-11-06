"""Make structural test photos: numbered, direction-marked chessboards with EYE/MOUTH/HEAD/SHOE markers.

These stand in for photo CONTENT only (page-15 rule 08).  They prove window geometry, layering and
masks; they never prove real-photo fit.  Output: assets/test/test01.jpg .. test09.jpg (portrait 3:4,
two landscape 4:3, one square) plus face.jpg (tight head crop) for face-overlay layouts.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SK = Path(__file__).resolve().parents[1]
OUT = SK / "assets" / "test"

PALETTES = [
    ((235, 200, 190), (110, 60, 60)), ((200, 220, 235), (40, 80, 120)), ((220, 235, 200), (60, 110, 50)),
    ((240, 225, 190), (120, 90, 30)), ((225, 205, 235), (90, 50, 120)), ((205, 230, 225), (30, 100, 90)),
    ((235, 215, 215), (120, 40, 60)), ((215, 215, 235), (50, 50, 120)), ((230, 230, 210), (90, 90, 40)),
]


def font(sz):
    for name in ("arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def make(n, w, h, label, face=False):
    light, dark = PALETTES[(n - 1) % len(PALETTES)]
    im = Image.new("RGB", (w, h), light)
    d = ImageDraw.Draw(im)
    cell = max(w, h) // 8
    for yy in range(0, h, cell):
        for xx in range(0, w, cell):
            if ((xx // cell) + (yy // cell)) % 2 == 0:
                d.rectangle([xx, yy, xx + cell, yy + cell], fill=tuple(int(l * 0.9 + k * 0.1) for l, k in zip(light, dark)))
    # figure: head circle, eyes, mouth, body, shoes
    cx = w // 2
    hr = int(min(w, h) * (0.3 if face else 0.11))
    hy = int(h * (0.45 if face else 0.22))
    d.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=(250, 225, 205), outline=dark, width=6)
    er = max(6, hr // 7)
    for sx in (-1, 1):
        ex, ey = cx + sx * hr // 2, hy - hr // 6
        d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=dark)
        d.text((ex, ey + er + 4), "EYE", fill=dark, font=font(max(14, hr // 5)), anchor="ma")
    d.arc([cx - hr // 2, hy + hr // 8, cx + hr // 2, hy + hr // 1.6], 10, 170, fill=dark, width=6)
    d.text((cx, hy + hr // 1.6 + 6), "MOUTH", fill=dark, font=font(max(14, hr // 5)), anchor="ma")
    d.text((cx, hy - hr - 10), "HEAD", fill=dark, font=font(max(16, hr // 4)), anchor="md")
    if not face:
        bw, by0, by1 = int(w * 0.22), hy + hr, int(h * 0.72)
        d.rectangle([cx - bw, by0, cx + bw, by1], fill=tuple(int(k * 0.8 + 50) for k in dark), outline=dark, width=5)
        d.text((cx, (by0 + by1) // 2), "BODY", fill=light, font=font(max(20, w // 16)), anchor="mm")
        for sx in (-1, 1):
            sxc = cx + sx * bw // 2
            d.rectangle([sxc - bw // 3, by1, sxc + bw // 3, int(h * 0.9)], fill=(60, 60, 60))
            d.text((sxc, int(h * 0.93)), "SHOE", fill=dark, font=font(max(16, w // 24)), anchor="ma")
    # number + orientation arrows
    d.text((20, 16), f"#{n}", fill=dark, font=font(max(40, w // 9)))
    d.text((w - 20, 16), "TOP ▲", fill=dark, font=font(max(20, w // 22)), anchor="ra")
    d.text((20, h - 16), "◀ LEFT", fill=dark, font=font(max(20, w // 22)), anchor="ld")
    d.text((w - 20, h - 16), label, fill=dark, font=font(max(20, w // 22)), anchor="rd")
    d.rectangle([0, 0, w - 1, h - 1], outline=dark, width=8)
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    specs = [(1, 1200, 1600, "3:4"), (2, 1200, 1600, "3:4"), (3, 1200, 1600, "3:4"), (4, 1600, 1200, "4:3"),
             (5, 1200, 1600, "3:4"), (6, 1600, 1200, "4:3"), (7, 1200, 1200, "1:1"), (8, 1200, 1600, "3:4"), (9, 1080, 1920, "9:16")]
    for n, w, h, lab in specs:
        make(n, w, h, lab).save(OUT / f"test{n:02d}.jpg", quality=90)
    make(10, 1200, 1500, "face", face=True).save(OUT / "face.jpg", quality=90)
    print("test images ->", OUT)


if __name__ == "__main__":
    main()
