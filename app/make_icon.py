"""Draw the desktop icon: a tilted photo card on a black tile, with a gold star.  Writes app/icon.png and app/app.ico."""
import math
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).parent
S = 1024


def main():
    tile = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(tile).rounded_rectangle([24, 24, S - 24, S - 24], radius=210, fill=(16, 14, 13, 255))
    w, h = 560, 700
    card = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle([40, 40, 40 + w, 40 + h], radius=34, fill=(255, 253, 248, 255))
    pic = Image.new("RGB", (w - 76, h - 180))
    px = pic.load()
    top, bottom = (255, 158, 128), (226, 72, 118)
    for y in range(pic.height):
        t = y / pic.height
        row = tuple(int(a + (b - a) * t) for a, b in zip(top, bottom))
        for x in range(pic.width):
            px[x, y] = row
    d = ImageDraw.Draw(pic)
    d.ellipse([250, 90, 410, 250], fill=(255, 231, 170))
    d.polygon([(-30, 520), (150, 250), (300, 430), (390, 330), (540, 520)], fill=(44, 34, 58))
    card.paste(pic, (78, 78))
    bar = ImageDraw.Draw(card)
    bar.rounded_rectangle([110, h - 62, 360, h - 30], radius=16, fill=(30, 26, 24, 255))
    bar.rounded_rectangle([110, h - 8, 270, h + 16], radius=12, fill=(200, 192, 182, 255))
    card = card.rotate(-8, resample=Image.BICUBIC, expand=True)
    tile.alpha_composite(card, ((S - card.width) // 2 - 10, (S - card.height) // 2 + 34))
    cx, cy, big, small = 800, 215, 128, 54
    pts = [(cx + (big if k % 2 == 0 else small) * math.sin(k * math.pi / 5),
            cy - (big if k % 2 == 0 else small) * math.cos(k * math.pi / 5)) for k in range(10)]
    ImageDraw.Draw(tile).polygon(pts, fill=(255, 196, 42, 255))
    tile.resize((256, 256), Image.LANCZOS).save(HERE / "icon.png")
    tile.save(HERE / "app.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])


if __name__ == "__main__":
    main()
