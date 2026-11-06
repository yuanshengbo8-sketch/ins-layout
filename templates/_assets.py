"""Generated-master asset slots (page-15 §05/06).

master(ctx, name) -> Path or None.  Masters live in assets/masters/<name>.png and are produced by an image
model (recorded in effects.json["masters"]).  Layouts that REQUIRE one raise AssetMissing -> status blocked.
Layouts where a native-drawn substitute is acceptable call the *_or_native helpers and record the substitution.
"""
from pathlib import Path

from templates._text import AssetMissing

MASTERS = {
    "G11": "G11_table_phone_hands.png", "G12": "G12_breakfast_phone_croissant.png", "G14": "G14_ground_coffee_shoes.png",
    "G15": "G15_leather_laptop_knit.png", "G20": "G20_gingham_notebook.png", "G21": "G21_bedsheet.png",
    "G22": "G22_denim.png", "G26": "G26_tiles_shadow.png", "G27": "G27_polka_fabric.png",
    "G23": "G23_cover_{variant}.png", "G24": "G24_mask_set.png", "G25": "G25_blue_objects.png",
    "G46": "G46_stickers_2x2.png", "G49": "G49_latte_lipgloss.png", "G50": "G50_pancakes.png",
    "ground": "ground_035_tiles9.png", "dual_phone": "dual_phone_038.png", "three_band": "three_band_138.png",
    "mask212": "mask212_cat.png", "mask218": "mask218_anime.png",
    "G46_cake": "G46_cake_cloud.png", "G46_cup": "G46_coffee_cup.png", "G46_iced": "G46_iced_coffee.png", "G46_sneakers": "G46_sneakers.png",
    "G24_eyes": "G24_eye_strip.png", "G24_cat_hat": "G24_cat_hat.png", "G24_cat_sit": "G24_cat_sitting.png", "G24_anime": "G24_anime_head.png",
    "G25_headphones": "G25_headphones.png", "G25_sunglasses": "G25_sunglasses.png", "G25_phone": "G25_phone_back.png", "G25_camera": "G25_camera.png", "G25_iced": "G25_iced_coffee.png",
    "G14_fg": "G14_fg.png", "ground_fg": "ground_035_fg.png", "G12_fg": "G12_fg.png", "dual_phone_fg": "dual_phone_038_fg.png",
}


def _existing(path):
    """The file itself, or its .webp twin (public releases ship masters as WebP to stay small)."""
    if path.exists():
        return path
    webp = path.with_suffix(".webp")
    return webp if webp.exists() else path


def variant_file(ctx, filename):
    """Path of a master or sidecar file for ctx["variant"].

    Variant n lives next to the base file as NAME__vN.ext.  Falls back to the base file when that variant
    does not exist, so a scene with one master still renders for every variant number.
    """
    d = Path(ctx.get("assets_dir")) / "masters"
    v = int(ctx.get("variant") or 1)
    if v > 1:
        stem, dot, ext = filename.rpartition(".")
        p = _existing(d / f"{stem}__v{v}.{ext}")
        if p.exists():
            return p
    return _existing(d / filename)


def by_variant(ctx, *values):
    """Pick the value for the current scene variant: by_variant(ctx, v1, v2, v3); short lists reuse the first."""
    v = int(ctx.get("variant") or 1)
    return values[v - 1] if v <= len(values) else values[0]


def master(ctx, key, **fmt):
    p = variant_file(ctx, MASTERS[key].format(**fmt))
    return p if p.exists() else None


def require(ctx, key, what, **fmt):
    p = master(ctx, key, **fmt)
    if p is None:
        raise AssetMissing(f"needs generated master {key} ({MASTERS[key].format(**fmt)}): {what}. "
                           f"Generate it into assets/masters/ (see effects.json masters) then re-run verify.")
    return p


def cover_art(c, ctx, x, y, size, variant="mint"):
    """Album cover: G23 master if present, else native-drawn cover (recorded as substitute)."""
    p = master(ctx, "G23", variant=variant)
    if p:
        c.image_file(p, x, y, size, size, layer="ui")
        return
    col = {"mint": ("#BFEFE6", "#6FB7AC"), "cream": ("#F6E8C8", "#D9B98A"), "navy": ("#2E4C8F", "#8FA9E8")}.get(variant, ("#CCC", "#888"))
    gid = c.gradient([(0, col[0]), (1, col[1])], 0, 0, 1, 1)
    c.rect(x, y, size, size, f"url(#{gid})", rx=size * 0.1, layer="ui")
    c.circle(x + size * 0.5, y + size * 0.42, size * 0.2, "rgba(255,255,255,0.85)", layer="ui")
    c.circle(x + size * 0.5, y + size * 0.42, size * 0.07, col[1], layer="ui")
    c.text(x + size * 0.5, y + size * 0.86, "RADIO", size=size * 0.13, font="sans", weight="bold", fill="#fff", anchor="middle", layer="ui", spacing=2)
    c.recipe.setdefault("substitutes", []).append({"slot": f"G23:{variant}", "used": "native cover"})
