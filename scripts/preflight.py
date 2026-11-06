"""Preflight: prove the machine can actually run ins-layout before any layout work.

Checks (each is a real test, not a version lookup):
  1. image read      - open a test image, read pixel values
  2. file I/O        - write / read back under the skill folder
  3. code            - numpy + PIL perspective warp of a test image
  4. SVG -> PNG      - render an SVG with Chinese text, emoji, alpha, clip-path via Playwright Chromium
  5. fonts           - probe which reference font families resolve (measured, not assumed)
Writes reports/preflight.json and exits non-zero on a hard failure.
"""
import json
import platform
import sys
import time
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK))
REPORT = SK / "reports" / "preflight.json"

FONT_PROBES = {
    "Arial": "Arial", "Arial Black": "Arial Black", "Arial Narrow": "Arial Narrow",
    "Georgia": "Georgia", "Times New Roman": "Times New Roman", "Comic Sans MS": "Comic Sans MS",
    "Brush Script MT": "Brush Script MT", "Courier New": "Courier New", "DIN Next LT Pro": "DIN Next LT Pro",
    "Bahnschrift": "Bahnschrift", "Segoe UI": "Segoe UI", "Microsoft YaHei": "Microsoft YaHei",
    "Noto Sans SC": "Noto Sans SC", "Malgun Gothic": "Malgun Gothic", "Segoe UI Emoji": "Segoe UI Emoji",
    "Helvetica": "Helvetica", "Futura": "Futura", "Avenir": "Avenir", "Snell Roundhand": "Snell Roundhand",
    "Chalkboard": "Chalkboard", "Silom": "Silom", "PingFang SC": "PingFang SC",
}


def main():
    t0 = time.time()
    rep = {"platform": platform.platform(), "python": sys.version.split()[0], "checks": {}, "fonts": {}}
    ok = True

    # 1. image read
    try:
        from PIL import Image
        import numpy as np
        page = Image.open(SK / "assets" / "test" / "test01.jpg")
        px = np.asarray(page.convert("RGB"))
        rep["checks"]["image_read"] = {"ok": True, "size": page.size, "mean": float(px.mean())}
    except Exception as e:  # noqa
        rep["checks"]["image_read"] = {"ok": False, "error": repr(e)}; ok = False

    # 2. file io
    try:
        p = SK / "reports" / "_io_probe.txt"
        p.write_text("probe 中文 ✓", "utf-8")
        assert p.read_text("utf-8") == "probe 中文 ✓"
        p.unlink()
        rep["checks"]["file_io"] = {"ok": True}
    except Exception as e:  # noqa
        rep["checks"]["file_io"] = {"ok": False, "error": repr(e)}; ok = False

    # 3. code: perspective warp + alpha
    try:
        from components.imaging import perspective_layer, cover_crop
        src = Image.new("RGB", (400, 600), (200, 80, 120))
        warped = perspective_layer(src, [(100, 100), (500, 160), (480, 700), (120, 640)], (1200, 1600))
        assert warped.mode == "RGBA" and warped.size == (1200, 1600)
        assert warped.getpixel((300, 400))[3] == 255 and warped.getpixel((10, 10))[3] == 0
        crop = cover_crop(src, 300, 300)
        assert crop.size == (300, 300)
        rep["checks"]["perspective_alpha_crop"] = {"ok": True}
    except Exception as e:  # noqa
        rep["checks"]["perspective_alpha_crop"] = {"ok": False, "error": repr(e)}; ok = False

    # 4. SVG -> PNG via Playwright Chromium, with font probing
    try:
        from components.render import render_svg, probe_fonts
        svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='600' height='400' viewBox='0 0 600 400'>
<defs><clipPath id='c'><circle cx='150' cy='200' r='100'/></clipPath></defs>
<rect width='600' height='400' fill='none'/>
<rect x='50' y='100' width='200' height='200' fill='#4a90e2' clip-path='url(#c)'/>
<text x='300' y='120' font-family='Microsoft YaHei' font-size='40' fill='#222'>中文字体测试</text>
<text x='300' y='200' font-family='Georgia' font-size='40' fill='#c33'>Georgia 123</text>
<text x='300' y='280' font-family='Segoe UI Emoji' font-size='40'>☕🌟🎀</text>
<rect x='300' y='320' width='200' height='60' fill='rgba(255,0,0,0.5)'/>
</svg>"""
        out = SK / "reports" / "_svg_probe.png"
        render_svg(svg, out, 600, 400, transparent=True)
        im = Image.open(out).convert("RGBA")
        assert im.size == (600, 400)
        assert im.getpixel((150, 200))[:3] == (74, 144, 226), "clip-path fill wrong"
        assert im.getpixel((20, 20))[3] == 0, "transparent background lost"
        assert im.getpixel((60, 110))[3] == 0, "clip-path not applied"
        a = im.getpixel((400, 350))
        assert a[3] not in (0, 255), "semi-transparent fill lost"
        # text actually drew something
        import numpy as np
        reg = np.asarray(im.crop((300, 80, 600, 130)))
        assert (reg[..., 3] > 0).sum() > 200, "Chinese text did not render"
        reg = np.asarray(im.crop((300, 240, 600, 300)))
        assert (reg[..., 3] > 0).sum() > 200, "emoji did not render"
        rep["checks"]["svg_to_png"] = {"ok": True, "renderer": "playwright-chromium"}
        rep["fonts"] = probe_fonts(list(FONT_PROBES.values()))
        out.unlink()
    except Exception as e:  # noqa
        rep["checks"]["svg_to_png"] = {"ok": False, "error": repr(e)}; ok = False

    rep["ok"] = ok
    rep["seconds"] = round(time.time() - t0, 1)
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(rep, indent=1, ensure_ascii=False), "utf-8")
    for k, v in rep["checks"].items():
        print(f"[{'OK' if v['ok'] else 'FAIL'}] {k} {'' if v['ok'] else v.get('error')}")
    if rep["fonts"]:
        have = [k for k, v in rep["fonts"].items() if v]
        miss = [k for k, v in rep["fonts"].items() if not v]
        print("fonts available:", ", ".join(have))
        print("fonts missing  :", ", ".join(miss))
    print("preflight", "PASSED" if ok else "FAILED", f"({rep['seconds']}s) -> {REPORT}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
