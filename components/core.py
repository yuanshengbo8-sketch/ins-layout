"""Core SVG builder for ins-layout.

One Canvas = one 1200x1600 (3:4) layered SVG.  Every template draws through these helpers so
coordinates, fonts and stroke widths all live in the same viewBox units.

Layers (z-order, bottom -> top): bg, photos, ui, text, deco, fg.
Each helper appends SVG to a layer; `svg()` assembles the document.
"""
import html
import math
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

from . import imaging

W, H = 1200, 1600
LAYERS = ("bg", "photos", "ui", "text", "deco", "fg")

# Font roles -> actual families verified by preflight on this machine (see reports/preflight.json).
FONTS = {
    "sans": "Arial, Helvetica, sans-serif",
    "sans_black": "'Arial Black', Arial, sans-serif",
    "sans_narrow": "'Arial Narrow', 'DIN Next LT Pro', Arial, sans-serif",
    "din": "'DIN Next LT Pro', 'Arial Narrow', Arial, sans-serif",
    "serif": "Georgia, 'Times New Roman', serif",
    "serif_display": "'Times New Roman', Georgia, serif",
    "hand": "'Comic Sans MS', 'Chalkboard', sans-serif",
    "script": "'Brush Script MT', 'Snell Roundhand', cursive",
    "mono": "'Courier New', 'Silom', monospace",
    "ui": "'Segoe UI', 'Helvetica Neue', Arial, sans-serif",
    "cjk": "'Microsoft YaHei', 'Noto Sans SC', 'PingFang SC', sans-serif",
    "kr": "'Malgun Gothic', 'Noto Sans KR', sans-serif",
    "emoji": "'Segoe UI Emoji', 'Apple Color Emoji', sans-serif",
    "rounded": "'Segoe UI', 'Arial Rounded MT Bold', Arial, sans-serif",
}


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def hexa(color: str, alpha: float) -> str:
    """'#RRGGBB' + alpha(0..1) -> rgba() string."""
    c = color.lstrip("#")
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


@dataclass
class Photo:
    path: str
    image: Image.Image
    hash: str
    index: int


@dataclass
class Canvas:
    width: int = W
    height: int = H
    photos: list = field(default_factory=list)
    defs: list = field(default_factory=list)
    layers: dict = field(default_factory=lambda: {k: [] for k in LAYERS})
    bg: str = "#FFFFFF"
    _n: int = 0
    recipe: dict = field(default_factory=dict)  # filled by templates: windows, text, assets used
    assets_dir: Path = None
    faces: dict = field(default_factory=dict)  # photo index -> (cx, cy, w, h) normalised head box, measured per photo

    # ---- ids / layers -------------------------------------------------
    def uid(self, prefix="e"):
        self._n += 1
        return f"{prefix}{self._n}"

    def add(self, layer: str, s: str):
        self.layers[layer].append(s)

    def photo(self, i: int) -> Photo:
        if i >= len(self.photos):
            raise IndexError(f"template needs photo #{i + 1} but only {len(self.photos)} given")
        return self.photos[i]

    # ---- photo windows ------------------------------------------------
    def smart_focus(self, i, focus, w, h):
        """Cover-crop focus that keeps the measured head in frame (rule 07: never lose the face to a crop).

        The template's focus is a hint; when the head of photo i is known, the crop is centred on it (slightly
        above, so the head sits in the upper part of the window) unless the template locked the focus.
        """
        f = self.faces.get(i)
        if not f:
            return focus
        fx, fy, fw, fh = f
        sw, sh = self.photo(i).image.size
        # only axes that are actually cropped need a decision
        scale = max(w / sw, h / sh)
        cx = fx if sw * scale > w + 1 else focus[0]
        cy = min(1.0, max(0.0, fy - 0.10)) if sh * scale > h + 1 else focus[1]
        return (cx, cy)

    def photo_rect(self, i, x, y, w, h, *, layer="photos", focus=(0.5, 0.45), zoom=1.0, rx=0, rotate=0,
                   opacity=1.0, stroke=None, stroke_w=0, shadow=None, filter_=None, clip_path=None, fmt="JPEG", lock=False):
        """Place photo i in a rect window (x,y,w,h) with object-fit cover.  rotate is degrees about the centre.
        lock=True keeps the given focus even when a head box is known (deliberate crops such as INS-195's shoe window)."""
        p = self.photo(i)
        if not lock:
            focus = self.smart_focus(i, focus, w, h)
        im = imaging.cover_crop(p.image, w, h, focus=focus, zoom=zoom)
        href = imaging.to_data_uri(im, fmt)
        iid = self.uid("ph")
        cx, cy = x + w / 2, y + h / 2
        tf = f' transform="rotate({rotate} {cx} {cy})"' if rotate else ""
        clip = ""
        if rx or clip_path:
            cid = self.uid("clip")
            shape = clip_path or f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>'
            self.defs.append(f'<clipPath id="{cid}">{shape}</clipPath>')
            clip = f' clip-path="url(#{cid})"'
        flt = f' filter="url(#{filter_})"' if filter_ else ""
        g = [f'<g id="{iid}"{tf}{flt}>']
        if shadow:
            g.append(self._shadow_rect(x, y, w, h, rx, shadow))
        g.append(f'<g{clip}><image href="{href}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="none" opacity="{opacity}"/></g>')
        if stroke:
            g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="{stroke}" stroke-width="{stroke_w}"/>')
        g.append("</g>")
        self.add(layer, "".join(g))
        self.recipe.setdefault("windows", []).append({"photo": i, "shape": "rect", "box": [x, y, w, h], "rx": rx, "rotate": rotate, "focus": focus, "zoom": zoom})
        return iid

    def photo_circle(self, i, cx, cy, r, *, layer="photos", focus=(0.5, 0.4), zoom=1.0, stroke=None, stroke_w=0, lock=False):
        p = self.photo(i)
        if not lock:
            focus = self.smart_focus(i, focus, 2 * r, 2 * r)
        im = imaging.cover_crop(p.image, 2 * r, 2 * r, focus=focus, zoom=zoom)
        href = imaging.to_data_uri(im, "JPEG")
        cid = self.uid("clip")
        self.defs.append(f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>')
        s = f'<g clip-path="url(#{cid})"><image href="{href}" x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}"/></g>'
        if stroke:
            s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{stroke}" stroke-width="{stroke_w}"/>'
        self.add(layer, s)
        self.recipe.setdefault("windows", []).append({"photo": i, "shape": "circle", "c": [cx, cy], "r": r, "focus": focus, "zoom": zoom})

    def photo_quad(self, i, quad, *, layer="photos", focus=(0.5, 0.45), zoom=1.0, inset=0.0, opacity=1.0):
        """Perspective-map photo i onto quad [(x,y)*4 TL,TR,BR,BL] (canvas px).  Bitmap layer embedded as PNG."""
        p = self.photo(i)
        if inset:
            cx = sum(q[0] for q in quad) / 4; cy = sum(q[1] for q in quad) / 4
            quad = [(cx + (x - cx) * (1 - inset), cy + (y - cy) * (1 - inset)) for x, y in quad]
        # crop the source to the quad's aspect first so the subject isn't squashed
        tw = max(math.dist(quad[0], quad[1]), math.dist(quad[3], quad[2]))
        th = max(math.dist(quad[0], quad[3]), math.dist(quad[1], quad[2]))
        src = imaging.cover_crop(p.image, int(tw * 1.5), int(th * 1.5), focus=focus, zoom=zoom)
        layer_im = imaging.perspective_layer(src, quad, (self.width, self.height))
        href = imaging.to_data_uri(layer_im, "PNG")
        self.add(layer, f'<image href="{href}" x="0" y="0" width="{self.width}" height="{self.height}" opacity="{opacity}"/>')
        self.recipe.setdefault("windows", []).append({"photo": i, "shape": "quad", "quad": quad, "focus": focus, "zoom": zoom})

    def photo_full(self, i, *, focus=(0.5, 0.45), zoom=1.0, layer="photos", filter_=None):
        return self.photo_rect(i, 0, 0, self.width, self.height, focus=focus, zoom=zoom, layer=layer, filter_=filter_)

    def image_file(self, path, x, y, w=None, h=None, *, layer="deco", opacity=1.0, rotate=0, fmt="PNG"):
        """Embed an asset bitmap (sticker / carrier) from disk, keeping aspect if one of w/h is None."""
        im = Image.open(path).convert("RGBA")
        if w is None and h is None:
            w, h = im.size
        elif w is None:
            w = h * im.width / im.height
        elif h is None:
            h = w * im.height / im.width
        href = imaging.to_data_uri(im, fmt)
        tf = f' transform="rotate({rotate} {x + w / 2} {y + h / 2})"' if rotate else ""
        self.add(layer, f'<image href="{href}" x="{x}" y="{y}" width="{w}" height="{h}" opacity="{opacity}"{tf}/>')
        self.recipe.setdefault("assets", []).append({"path": str(path), "box": [x, y, w, h], "rotate": rotate})

    def _shadow_rect(self, x, y, w, h, rx, shadow):
        fid = self.uid("sh")
        blur, dx, dy, op = shadow if isinstance(shadow, (tuple, list)) else (18, 0, 10, 0.35)
        self.defs.append(f'<filter id="{fid}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="{blur}"/></filter>')
        return f'<rect x="{x + dx}" y="{y + dy}" width="{w}" height="{h}" rx="{rx}" fill="rgba(0,0,0,{op})" filter="url(#{fid})"/>'

    # ---- primitives ---------------------------------------------------
    def rect(self, x, y, w, h, fill="#fff", *, layer="ui", rx=0, stroke=None, stroke_w=1, opacity=1.0, rotate=0, extra=""):
        tf = f' transform="rotate({rotate} {x + w / 2} {y + h / 2})"' if rotate else ""
        st = f' stroke="{stroke}" stroke-width="{stroke_w}"' if stroke else ""
        op = f' opacity="{opacity}"' if opacity != 1.0 else ""
        self.add(layer, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}{op}{tf}{extra}/>')

    def circle(self, cx, cy, r, fill="#fff", *, layer="ui", stroke=None, stroke_w=1, opacity=1.0):
        st = f' stroke="{stroke}" stroke-width="{stroke_w}"' if stroke else ""
        self.add(layer, f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{st} opacity="{opacity}"/>')

    def line(self, x1, y1, x2, y2, stroke="#000", w=2, *, layer="ui", dash=None, cap="butt", opacity=1.0):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(layer, f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="{cap}"{d} opacity="{opacity}"/>')

    def path(self, d, fill="none", stroke=None, w=2, *, layer="deco", opacity=1.0, cap="round", join="round", extra=""):
        st = f' stroke="{stroke}" stroke-width="{w}" stroke-linecap="{cap}" stroke-linejoin="{join}"' if stroke else ""
        self.add(layer, f'<path d="{d}" fill="{fill}"{st} opacity="{opacity}"{extra}/>')

    def raw(self, s, layer="deco"):
        self.add(layer, s)

    def blur_filter(self, std=8):
        fid = self.uid("blur")
        self.defs.append(f'<filter id="{fid}" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="{std}"/></filter>')
        return fid

    def drop_shadow_filter(self, dx=0, dy=6, std=10, color="rgba(0,0,0,0.35)"):
        fid = self.uid("ds")
        self.defs.append(f'<filter id="{fid}" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="{dx}" dy="{dy}" stdDeviation="{std}" flood-color="{color}"/></filter>')
        return fid

    def gradient(self, stops, x1=0, y1=0, x2=0, y2=1):
        gid = self.uid("gr")
        st = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
        self.defs.append(f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{st}</linearGradient>')
        return gid

    # ---- text -----------------------------------------------------------
    def text(self, x, y, s, *, size=40, font="sans", fill="#000", weight="normal", anchor="start", layer="text",
             italic=False, spacing=0, stroke=None, stroke_w=0, opacity=1.0, rotate=0, baseline="alphabetic", extra="", transform=""):
        fam = FONTS.get(font, font)
        tf = ""
        if rotate:
            tf = f' transform="rotate({rotate} {x} {y})"'
        elif transform:
            tf = f' transform="{transform}"'
        st = f' stroke="{stroke}" stroke-width="{stroke_w}" paint-order="stroke" stroke-linejoin="round"' if stroke else ""
        it = ' font-style="italic"' if italic else ""
        ls = f' letter-spacing="{spacing}"' if spacing else ""
        op = f' opacity="{opacity}"' if opacity != 1.0 else ""
        self.add(layer, f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" dominant-baseline="{baseline}"{it}{ls}{st}{op}{tf}{extra}>{esc(s)}</text>')
        self.recipe.setdefault("text", []).append({"s": s, "x": x, "y": y, "size": size, "font": font, "fill": fill})

    def text_lines(self, x, y, lines, *, size=40, leading=1.1, **kw):
        """Several lines starting with baseline y; returns y after the last line."""
        for i, ln in enumerate(lines):
            self.text(x, y + i * size * leading, ln, size=size, **kw)
        return y + len(lines) * size * leading

    def text_box(self, x, y, w, s, *, size=24, leading=1.3, **kw):
        """Greedy word-wrap using width measured in Chromium; returns y after last line."""
        from .render import measure_many
        fam_key = kw.get("font", "sans"); fam = FONTS.get(fam_key, fam_key).split(",")[0].strip("'\"")
        words = s.split(" ")
        widths = measure_many([{"text": w_, "family": fam, "size": size, "weight": kw.get("weight", "normal")} for w_ in words])
        sp = measure_many([{"text": " ", "family": fam, "size": size}])[0]
        lines, cur, cw = [], [], 0
        for wd, ww in zip(words, widths):
            if cur and cw + sp + ww > w:
                lines.append(" ".join(cur)); cur, cw = [wd], ww
            else:
                cw = cw + (sp if cur else 0) + ww; cur.append(wd)
        if cur:
            lines.append(" ".join(cur))
        return self.text_lines(x, y, lines, size=size, leading=leading, **kw)

    # ---- assembly -----------------------------------------------------
    def svg(self, out_size=None) -> str:
        """Assemble the document. out_size=(w,h) scales the fixed 1200x1600 design to another canvas
        (centre-slice when the aspect differs, e.g. 1080x1350 for the IG 4:5 feed)."""
        defs = "".join(self.defs)
        body = []
        for k in LAYERS:
            if self.layers[k]:
                body.append(f'<g id="layer-{k}">' + "".join(self.layers[k]) + "</g>")
        ow, oh = out_size or (self.width, self.height)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{ow}" height="{oh}" '
                f'viewBox="0 0 {self.width} {self.height}" preserveAspectRatio="xMidYMid slice"><defs>{defs}</defs>'
                f'<rect id="layer-base" width="{self.width}" height="{self.height}" fill="{self.bg}"/>' + "".join(body) + "</svg>")


def load_photos(paths) -> list:
    out = []
    for i, p in enumerate(paths):
        out.append(Photo(str(p), imaging.load_photo(p), imaging.file_hash(p), i))
    return out
