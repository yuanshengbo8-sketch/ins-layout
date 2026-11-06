"""Native-drawn UI components (iOS / macOS / IG style) used across the 126 layouts.

Every function draws onto a Canvas at canvas coordinates and returns the occupied box (x,y,w,h).
Nothing here is a bitmap: all vector, editable in the layered SVG.
"""
from .core import Canvas, esc, hexa, FONTS

IOS_BLUE = "#0A84FF"
IOS_GREY = "#E9E9EB"
IOS_TEXT = "#1C1C1E"
IOS_SUB = "#8E8E93"


# ---------------------------------------------------------------- icons
def icon_send_arrow(c: Canvas, cx, cy, r=22, fill=IOS_BLUE, layer="ui"):
    c.circle(cx, cy, r, fill, layer=layer)
    s = r * 0.5
    c.path(f"M{cx} {cy + s * 0.9} L{cx} {cy - s * 0.9} M{cx - s * 0.75} {cy - s * 0.15} L{cx} {cy - s * 0.9} L{cx + s * 0.75} {cy - s * 0.15}",
           stroke="#fff", w=max(2, r * 0.16), layer=layer)


def icon_plus_circle(c: Canvas, cx, cy, r=24, fill="#E5E5EA", stroke_col="#8E8E93", layer="ui"):
    c.circle(cx, cy, r, fill, layer=layer)
    s = r * 0.45
    c.path(f"M{cx - s} {cy} H{cx + s} M{cx} {cy - s} V{cy + s}", stroke=stroke_col, w=max(2, r * 0.12), layer=layer)


def icon_close(c: Canvas, cx, cy, r=16, fill="#000", opacity=0.6, layer="ui", mark="#fff"):
    c.circle(cx, cy, r, fill, layer=layer, opacity=opacity)
    s = r * 0.42
    c.path(f"M{cx - s} {cy - s} L{cx + s} {cy + s} M{cx + s} {cy - s} L{cx - s} {cy + s}", stroke=mark, w=max(2, r * 0.14), layer=layer)


def icon_check_circle(c: Canvas, cx, cy, r=18, fill=IOS_BLUE, layer="ui"):
    c.circle(cx, cy, r, fill, layer=layer, stroke="#fff", stroke_w=max(2, r * 0.12))
    s = r * 0.5
    c.path(f"M{cx - s * 0.9} {cy} L{cx - s * 0.2} {cy + s * 0.7} L{cx + s * 0.95} {cy - s * 0.65}", stroke="#fff", w=max(2, r * 0.16), layer=layer)


def icon_heart(c: Canvas, cx, cy, s=20, fill="#fff", stroke=None, layer="deco", w=2):
    d = (f"M{cx} {cy + s * 0.9} C{cx - s * 1.6} {cy - s * 0.2}, {cx - s * 0.8} {cy - s * 1.2}, {cx} {cy - s * 0.35} "
         f"C{cx + s * 0.8} {cy - s * 1.2}, {cx + s * 1.6} {cy - s * 0.2}, {cx} {cy + s * 0.9} Z")
    c.path(d, fill=fill, stroke=stroke, w=w, layer=layer)


def icon_ig_actions(c: Canvas, x, y, w, h=60, layer="ui", bg="#fff", col="#111"):
    """IG post action row: heart, comment, share ... bookmark."""
    c.rect(x, y, w, h, bg, layer=layer, rx=4)
    cy = y + h / 2
    icon_heart(c, x + 36, cy + 2, 13, fill="none", stroke=col, layer=layer, w=3)
    c.circle(x + 92, cy, 13, "none", stroke=col, stroke_w=3, layer=layer)
    c.path(f"M{x + 82} {cy + 10} L{x + 78} {cy + 20} L{x + 90} {cy + 13}", fill=col, layer=layer)
    c.path(f"M{x + 134} {cy + 12} L{x + 162} {cy - 12} L{x + 128} {cy - 2} L{x + 142} {cy + 2} Z M{x + 142} {cy + 2} L{x + 150} {cy + 14} L{x + 162} {cy - 12}",
           fill="none", stroke=col, w=3, layer=layer)
    bx = x + w - 44
    c.path(f"M{bx - 10} {cy - 14} H{bx + 10} V{cy + 14} L{bx} {cy + 6} L{bx - 10} {cy + 14} Z", fill="none", stroke=col, w=3, layer=layer)


# ---------------------------------------------------------------- bubbles
def bubble(c: Canvas, x, y, w, h, text, *, fill=IOS_BLUE, color="#fff", size=30, tail="right", rx=None, layer="ui",
           font="ui", weight="normal", pad=22, align="left"):
    """iMessage-style rounded bubble with a small tail. text may contain '\\n'."""
    rx = rx or h / 2 if "\n" not in text else 26
    c.rect(x, y, w, h, fill, layer=layer, rx=min(rx, h / 2))
    if tail == "right":
        c.path(f"M{x + w - 14} {y + h - 2} Q{x + w + 2} {y + h + 1} {x + w + 10} {y + h - 10} Q{x + w - 4} {y + h - 4} {x + w - 6} {y + h - 18} Z", fill=fill, layer=layer)
    elif tail == "left":
        c.path(f"M{x + 14} {y + h - 2} Q{x - 2} {y + h + 1} {x - 10} {y + h - 10} Q{x + 4} {y + h - 4} {x + 6} {y + h - 18} Z", fill=fill, layer=layer)
    lines = text.split("\n")
    lead = size * 1.22
    ty = y + h / 2 - (len(lines) - 1) * lead / 2 + size * 0.35
    for i, ln in enumerate(lines):
        if align == "center":
            c.text(x + w / 2, ty + i * lead, ln, size=size, font=font, fill=color, anchor="middle", weight=weight, layer=layer)
        else:
            c.text(x + pad, ty + i * lead, ln, size=size, font=font, fill=color, weight=weight, layer=layer)
    return (x, y, w, h)


def speech_cloud(c: Canvas, x, y, w, h, text, *, fill="#fff", stroke="#222", size=24, layer="ui", font="hand", tail_to=None, sw=3):
    """Comic style speech bubble (ellipse) with a pointer toward tail_to=(x,y)."""
    cx, cy = x + w / 2, y + h / 2
    if tail_to:
        tx, ty = tail_to
        c.path(f"M{cx - w * 0.12} {cy + h * 0.42} L{tx} {ty} L{cx + w * 0.12} {cy + h * 0.38} Z", fill=fill, stroke=stroke, w=sw, layer=layer)
    c.raw(f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2}" ry="{h / 2}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>', layer)
    if tail_to:
        c.raw(f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2 - sw}" ry="{h / 2 - sw}" fill="{fill}"/>', layer)
    lines = text.split("\n"); lead = size * 1.2
    ty0 = cy - (len(lines) - 1) * lead / 2 + size * 0.35
    for i, ln in enumerate(lines):
        c.text(cx, ty0 + i * lead, ln, size=size, font=font, fill="#111", anchor="middle", layer=layer)


def pill(c: Canvas, x, y, text, *, size=26, fill="#fff", color="#111", pad=24, h=None, layer="ui", font="ui", weight="normal",
         stroke=None, opacity=1.0, icon=None):
    """Rounded pill with auto width. Returns (x,y,w,h)."""
    from .render import measure_text
    fam = FONTS.get(font, font).split(",")[0].strip("'\"")
    tw = measure_text(text, fam, size, weight)
    h = h or size * 1.9
    iw = size * 1.3 if icon else 0
    w = tw + pad * 2 + iw
    c.rect(x, y, w, h, fill, layer=layer, rx=h / 2, stroke=stroke, opacity=opacity)
    if icon:
        c.text(x + pad, y + h / 2 + size * 0.36, icon, size=size, font="emoji", layer=layer)
    c.text(x + pad + iw, y + h / 2 + size * 0.36, text, size=size, font=font, fill=color, weight=weight, layer=layer)
    return (x, y, w, h)


def label_tag(c: Canvas, x, y, text, *, size=22, fill="#1B30DD", color="#fff", pad=12, layer="ui", font="sans", weight="bold"):
    """Square blue tag like @WHITE.TEE (INS-221)."""
    from .render import measure_text
    tw = measure_text(text, "Arial", size, weight)
    h = size * 1.5
    c.rect(x, y, tw + pad * 2, h, fill, layer=layer)
    c.text(x + pad, y + h * 0.72, text, size=size, font=font, fill=color, weight=weight, layer=layer)
    return (x, y, tw + pad * 2, h)


# ---------------------------------------------------------------- cards
def ios_card(c: Canvas, x, y, w, h, *, fill="#fff", rx=28, layer="ui", shadow=True, opacity=1.0, stroke=None):
    if shadow:
        fid = c.drop_shadow_filter(0, 8, 14, "rgba(0,0,0,0.18)")
        c.rect(x, y, w, h, fill, layer=layer, rx=rx, opacity=opacity, extra=f' filter="url(#{fid})"', stroke=stroke)
    else:
        c.rect(x, y, w, h, fill, layer=layer, rx=rx, opacity=opacity, stroke=stroke)
    return (x, y, w, h)


def focus_row(c: Canvas, x, y, w, h, icon, title, sub=None, *, fill="rgba(255,255,255,0.92)", layer="ui", color="#111", icon_bg="#fff"):
    """iOS Focus-mode row: round icon, title, subtitle, '...'."""
    c.rect(x, y, w, h, fill, layer=layer, rx=h / 2)
    c.circle(x + h / 2, y + h / 2, h * 0.3, icon_bg, layer=layer)
    c.text(x + h / 2, y + h / 2 + h * 0.12, icon, size=h * 0.34, font="emoji", anchor="middle", layer=layer)
    tx = x + w / 2
    if sub:
        c.text(tx, y + h * 0.46, title, size=h * 0.3, font="ui", fill=color, anchor="middle", weight="600", layer=layer)
        c.text(tx, y + h * 0.75, sub, size=h * 0.2, font="ui", fill=IOS_SUB, anchor="middle", layer=layer)
    else:
        c.text(tx, y + h * 0.62, title, size=h * 0.3, font="ui", fill=color, anchor="middle", weight="600", layer=layer)
    c.text(x + w - h * 0.5, y + h * 0.58, "•••", size=h * 0.26, font="ui", fill=IOS_SUB, anchor="middle", layer=layer)


def search_bar(c: Canvas, x, y, w, h=64, text="Google Search", *, fill="#fff", color="#222", size=26, layer="ui", align="right", icon=None):
    c.rect(x, y, w, h, fill, layer=layer, rx=0)
    if align == "right":
        c.text(x + w - 24, y + h * 0.65, text, size=size, font="sans", fill=color, anchor="end", layer=layer)
    else:
        c.text(x + 24, y + h * 0.65, text, size=size, font="sans", fill=color, layer=layer)
    if icon:
        c.text(x + 20, y + h * 0.66, icon, size=size, font="sans", fill=color, layer=layer)


def input_field(c: Canvas, x, y, w, h, text, *, fill="#fff", stroke="#D1D1D6", size=30, layer="ui", send=True, color="#111", placeholder=False, caret=False):
    c.rect(x, y, w, h, fill, layer=layer, rx=h / 2, stroke=stroke, stroke_w=2)
    c.text(x + 28, y + h / 2 + size * 0.36, text, size=size, font="ui", fill=IOS_SUB if placeholder else color, layer=layer)
    if caret:
        from .render import measure_text
        tw = measure_text(text, "Segoe UI", size)
        c.line(x + 30 + tw, y + h * 0.25, x + 30 + tw, y + h * 0.75, IOS_BLUE, 3, layer=layer)
    if send:
        icon_send_arrow(c, x + w - h / 2, y + h / 2, h * 0.36, layer=layer)
    return (x, y, w, h)


def message_photo_card(c: Canvas, x, y, w, h, *, layer="ui", close=True, rx=22):
    """White card holding a photo thumbnail with (x) close - iMessage photo attachment."""
    ios_card(c, x, y, w, h, rx=rx, layer=layer, shadow=False, stroke="#E0E0E0")
    if close:
        icon_close(c, x + w - 30, y + 30, 18, fill="#8E8E93", opacity=0.9, layer=layer)


def week_strip(c: Canvas, x, y, w, days, nums, today_idx, *, size=30, layer="ui", color="#111", muted="#9A9A9A", today_fill="#111", today_color="#fff", head_size=20, gap=None):
    """M T W T F S S row with day numbers; today in a filled circle."""
    n = len(days); gap = gap or w / n
    for i, (d, num) in enumerate(zip(days, nums)):
        cx = x + gap * i + gap / 2
        weekend = i >= 5
        c.text(cx, y, d, size=head_size, font="sans", fill=muted if weekend else color, anchor="middle", weight="bold", layer=layer)
        if i == today_idx:
            c.circle(cx, y + size * 1.55, size * 0.85, today_fill, layer=layer)
            c.text(cx, y + size * 1.55 + size * 0.36, str(num), size=size, font="sans", fill=today_color, anchor="middle", weight="bold", layer=layer)
        else:
            c.text(cx, y + size * 1.55 + size * 0.36, str(num), size=size, font="sans", fill=muted if weekend else color, anchor="middle", layer=layer)
    return (x, y, w, size * 2.6)


def hour_rail(c: Canvas, x, y, hours, step, *, size=22, color="#9A9A9A", line_col="#E3E3E3", line_x1=None, line_x2=None, layer="ui", fmt="{:02d}:00"):
    for i, hr in enumerate(hours):
        yy = y + i * step
        c.text(x, yy + size * 0.35, fmt.format(hr), size=size, font="sans", fill=color, anchor="end", layer=layer)
        if line_x1 is not None:
            c.line(line_x1, yy, line_x2, yy, line_col, 2, layer=layer)


def month_grid(c: Canvas, x, y, w, year, month, *, size=28, layer="ui", color="#111", muted="#B0B0B0", start_monday=True, head=True,
               row_h=None, highlight=None, highlight_fill="#111", highlight_color="#fff"):
    """Full month number grid (7 columns). highlight: set of day numbers drawn in a circle."""
    import calendar
    cal = calendar.Calendar(0 if start_monday else 6)
    weeks = cal.monthdayscalendar(year, month)
    gap = w / 7; row_h = row_h or size * 1.9
    yy = y
    if head:
        heads = ["M", "T", "W", "T", "F", "S", "S"] if start_monday else ["S", "M", "T", "W", "T", "F", "S"]
        for i, hd in enumerate(heads):
            c.text(x + gap * i + gap / 2, yy, hd, size=size * 0.6, font="sans", fill=muted, anchor="middle", weight="bold", layer=layer)
        yy += size * 1.2
    for wk in weeks:
        for i, d in enumerate(wk):
            if d == 0:
                continue
            cx = x + gap * i + gap / 2
            weekend = (i >= 5) if start_monday else (i in (0, 6))
            if highlight and d in highlight:
                c.circle(cx, yy + size * 0.5, size * 0.78, highlight_fill, layer=layer)
                c.text(cx, yy + size * 0.86, str(d), size=size, font="sans", fill=highlight_color, anchor="middle", weight="bold", layer=layer)
            else:
                c.text(cx, yy + size * 0.86, str(d), size=size, font="sans", fill=muted if weekend else color, anchor="middle", layer=layer)
        yy += row_h
    return (x, y, w, yy - y)


def music_card(c: Canvas, x, y, w, h, title, sub, *, fill="rgba(20,20,20,0.85)", color="#fff", layer="ui", art=None, progress=0.42,
               t0="0:49", t1="-1:30", rx=30, size=None, c_canvas=None):
    """Dark music player card: artwork, title, subtitle, progress bar, transport."""
    size = size or h * 0.11
    c.rect(x, y, w, h, fill, layer=layer, rx=rx)
    ax = x + h * 0.14; ay = y + h * 0.14; aw = h * 0.3
    if art is not None:
        c.photo_rect(art, ax, ay, aw, aw, rx=12, layer=layer)
    else:
        c.rect(ax, ay, aw, aw, "#6E8CA8", rx=12, layer=layer)
    c.text(ax + aw + 28, ay + aw * 0.42, title, size=size * 1.15, font="ui", fill=color, weight="bold", layer=layer)
    c.text(ax + aw + 28, ay + aw * 0.42 + size * 1.35, sub, size=size * 0.78, font="ui", fill="rgba(255,255,255,0.7)", layer=layer)
    py = y + h * 0.60; px0 = x + w * 0.2; px1 = x + w * 0.8
    c.text(px0 - 16, py + size * 0.3, t0, size=size * 0.8, font="ui", fill=color, anchor="end", layer=layer)
    c.text(px1 + 16, py + size * 0.3, t1, size=size * 0.8, font="ui", fill=color, layer=layer)
    c.line(px0, py, px1, py, "rgba(255,255,255,0.3)", 6, layer=layer, cap="round")
    c.line(px0, py, px0 + (px1 - px0) * progress, py, color, 6, layer=layer, cap="round")
    ty = y + h * 0.82; s = size
    c.path(f"M{x + w * 0.3} {ty} L{x + w * 0.3 + s} {ty - s * 0.6} V{ty + s * 0.6} Z M{x + w * 0.3 + s} {ty} L{x + w * 0.3 + 2 * s} {ty - s * 0.6} V{ty + s * 0.6} Z", fill=color, layer=layer)
    c.rect(x + w * 0.5 - s * 0.55, ty - s * 0.7, s * 0.4, s * 1.4, color, layer=layer)
    c.rect(x + w * 0.5 + s * 0.15, ty - s * 0.7, s * 0.4, s * 1.4, color, layer=layer)
    c.path(f"M{x + w * 0.7} {ty} L{x + w * 0.7 - s} {ty - s * 0.6} V{ty + s * 0.6} Z M{x + w * 0.7 - s} {ty} L{x + w * 0.7 - 2 * s} {ty - s * 0.6} V{ty + s * 0.6} Z", fill=color, layer=layer)


def mini_player(c: Canvas, x, y, w, h, title, sub, *, fill="#fff", color="#111", layer="ui", art=None, rx=16, progress=0.3):
    """Small light player (INS-144/177 style) with artwork + two text lines + progress + ◀ ▮▮ ▶."""
    fid = c.drop_shadow_filter(0, 4, 8, "rgba(0,0,0,0.2)")
    c.rect(x, y, w, h, fill, layer=layer, rx=rx, extra=f' filter="url(#{fid})"')
    s = h * 0.1
    c.text(x + w / 2, y + h * 0.16, title, size=s * 1.2, font="ui", fill=color, weight="bold", anchor="middle", layer=layer)
    c.text(x + w / 2, y + h * 0.16 + s * 1.5, sub, size=s * 0.85, font="ui", fill="#777", anchor="middle", layer=layer)
    py = y + h * 0.5
    c.text(x + w * 0.1, py + s * 0.3, "2:14", size=s * 0.6, font="ui", fill="#777", layer=layer)
    c.line(x + w * 0.22, py, x + w * 0.9, py, "#D5D5D5", 4, layer=layer, cap="round")
    c.line(x + w * 0.22, py, x + w * 0.22 + w * 0.68 * progress, py, "#555", 4, layer=layer, cap="round")
    ty = y + h * 0.78
    c.path(f"M{x + w * 0.32} {ty} L{x + w * 0.32 + s} {ty - s * 0.6} V{ty + s * 0.6} Z M{x + w * 0.32 + s} {ty} L{x + w * 0.32 + 2 * s} {ty - s * 0.6} V{ty + s * 0.6} Z", fill=color, layer=layer)
    c.rect(x + w * 0.5 - s * 0.55, ty - s * 0.7, s * 0.4, s * 1.4, color, layer=layer)
    c.rect(x + w * 0.5 + s * 0.15, ty - s * 0.7, s * 0.4, s * 1.4, color, layer=layer)
    c.path(f"M{x + w * 0.68} {ty} L{x + w * 0.68 - s} {ty - s * 0.6} V{ty + s * 0.6} Z M{x + w * 0.68 - s} {ty} L{x + w * 0.68 - 2 * s} {ty - s * 0.6} V{ty + s * 0.6} Z", fill=color, layer=layer)


def now_playing_pill(c: Canvas, x, y, w, h, title, sub, *, layer="ui", art=None, fill="#fff", color="#111"):
    """Small horizontal 'now playing' pill with square artwork (INS-172/138)."""
    fid = c.drop_shadow_filter(0, 4, 8, "rgba(0,0,0,0.2)")
    c.rect(x, y, w, h, fill, layer=layer, rx=10, extra=f' filter="url(#{fid})"')
    aw = h * 0.74
    if art is not None:
        c.photo_rect(art, x + h * 0.13, y + h * 0.13, aw, aw, rx=6, layer=layer)
    else:
        c.rect(x + h * 0.13, y + h * 0.13, aw, aw, "#7FA7C9", rx=6, layer=layer)
    c.text(x + aw + h * 0.3, y + h * 0.45, title, size=h * 0.27, font="ui", fill=color, weight="bold", layer=layer)
    c.text(x + aw + h * 0.3, y + h * 0.78, sub, size=h * 0.2, font="ui", fill="#777", layer=layer)


def weather_widget(c: Canvas, x, y, w, h, temp, desc, hi, lo, *, layer="ui", fill="rgba(60,40,60,0.85)", color="#fff"):
    c.rect(x, y, w, h, fill, layer=layer, rx=24)
    s = h * 0.22
    c.text(x + 28, y + h * 0.38, f"☀ {temp}", size=s, font="ui", fill=color, layer=layer)
    c.text(x + 28, y + h * 0.63, desc, size=s * 0.95, font="ui", fill=color, layer=layer)
    c.text(x + 28, y + h * 0.86, f"↑{hi} ↓{lo}", size=s * 0.8, font="ui", fill="rgba(255,255,255,0.75)", layer=layer)


def camera_hud(c: Canvas, x, y, w, h, *, layer="fg", zooms=("0.5", "1×", "2"), active=1, grid=True, box=None, color="rgba(255,255,255,0.9)"):
    """Camera thirds grid + zoom pills + optional yellow focus box (x,y,w,h)."""
    if grid:
        for k in (1, 2):
            c.line(x + w * k / 3, y, x + w * k / 3, y + h, color, 1.5, layer=layer, opacity=0.8)
            c.line(x, y + h * k / 3, x + w, y + h * k / 3, color, 1.5, layer=layer, opacity=0.8)
    if box:
        bx, by, bw, bh = box
        c.rect(bx, by, bw, bh, "none", layer=layer, stroke="#FFD60A", stroke_w=3)
        c.line(bx + bw + 30, by - 40, bx + bw + 30, by + bh + 40, "#FFD60A", 2, layer=layer)
        c.circle(bx + bw + 30, by + bh / 2, 9, "#FFD60A", layer=layer)
    n = len(zooms); cy = y + h - 110; gap = 112
    x0 = x + w / 2 - gap * (n - 1) / 2
    for i, z in enumerate(zooms):
        cx = x0 + gap * i
        if i == active:
            c.circle(cx, cy, 52, "rgba(0,0,0,0.6)", layer=layer)
            c.text(cx, cy + 12, z, size=34, font="ui", fill="#FFD60A", anchor="middle", weight="600", layer=layer)
        else:
            c.text(cx, cy + 12, z, size=34, font="ui", fill="#fff", anchor="middle", layer=layer)


def airdrop_card(c: Canvas, x, y, w, *, layer="ui", title="AirDrop", photo=0):
    """AirDrop receive sheet: title, photo, Decline | Accept. Returns height."""
    ph = w * 0.72
    h = 90 + ph + 110
    ios_card(c, x, y, w, h, rx=22, layer=layer, shadow=True, fill="#F7F7F7")
    c.text(x + w / 2, y + 58, title, size=36, font="ui", fill="#111", weight="bold", anchor="middle", layer=layer)
    c.line(x, y + 90, x + w, y + 90, "#DADADA", 2, layer=layer)
    c.photo_rect(photo, x + 14, y + 104, w - 28, ph, rx=6, layer=layer)
    yy = y + 104 + ph + 20
    c.line(x, yy, x + w, yy, "#DADADA", 2, layer=layer)
    c.line(x + w / 2, yy, x + w / 2, y + h, "#DADADA", 2, layer=layer)
    c.text(x + w / 4, yy + 56, "Decline", size=28, font="ui", fill="#3A7BD5", anchor="middle", layer=layer)
    c.text(x + 3 * w / 4, yy + 56, "Accept", size=28, font="ui", fill="#3A7BD5", anchor="middle", layer=layer)
    return h


def rename_dialog(c: Canvas, x, y, w, title, value, *, layer="ui", buttons=("Cancel", "Save")):
    h = 190
    c.rect(x, y, w, h, "#2C2C2E", layer=layer, rx=20)
    c.text(x + w / 2, y + 44, title, size=24, font="ui", fill="#fff", weight="600", anchor="middle", layer=layer)
    c.rect(x + 24, y + 66, w - 48, 44, "#1C1C1E", layer=layer, rx=10)
    c.text(x + w / 2, y + 96, value, size=22, font="ui", fill="#fff", anchor="middle", layer=layer)
    icon_close(c, x + w - 44, y + 88, 9, fill="#8E8E93", layer=layer)
    c.line(x, y + 128, x + w, y + 128, "#3A3A3C", 2, layer=layer)
    c.line(x + w / 2, y + 128, x + w / 2, y + h, "#3A3A3C", 2, layer=layer)
    c.text(x + w / 4, y + 166, buttons[0], size=24, font="ui", fill="#5AA0FF", anchor="middle", layer=layer)
    c.text(x + 3 * w / 4, y + 166, buttons[1], size=24, font="ui", fill="#5AA0FF", anchor="middle", layer=layer)
    return h


def share_sheet(c: Canvas, x, y, w, items, *, layer="ui"):
    """Light share/quick-action sheet with 3 top icons + list rows (INS-134)."""
    rh = 64
    h = 110 + rh * len(items)
    c.rect(x, y, w, h, "#F2F2F7", layer=layer, rx=18)
    for i, (ic, lab, col) in enumerate((("♣", "Share", "#111"), ("♡", "Favorite", "#111"), ("▦", "Delete", "#E0245E"))):
        cx = x + w * (0.2 + 0.3 * i)
        c.text(cx, y + 48, ic, size=30, font="sans", fill=col, anchor="middle", layer=layer)
        c.text(cx, y + 82, lab, size=16, font="ui", fill=col, anchor="middle", layer=layer)
    c.line(x, y + 104, x + w, y + 104, "#D9D9DE", 2, layer=layer)
    for i, (ic, lab) in enumerate(items):
        yy = y + 110 + rh * i
        c.text(x + 28, yy + 40, ic, size=22, font="sans", fill="#111", layer=layer)
        c.text(x + 68, yy + 40, lab, size=22, font="ui", fill="#111", layer=layer)
        if i < len(items) - 1:
            c.line(x + 68, yy + rh, x + w, yy + rh, "#E5E5EA", 1.5, layer=layer)
    return h


def profile_header(c: Canvas, x, y, w, name, sub, *, layer="ui", avatar=None, verified=True, button="Following"):
    c.rect(x, y, w, 120, "#fff", layer=layer)
    if avatar is not None:
        c.photo_circle(avatar, x + 60, y + 60, 40, layer=layer)
    else:
        c.circle(x + 60, y + 60, 40, "#DDD", layer=layer)
    c.text(x + 120, y + 52, name, size=30, font="serif", fill="#111", weight="bold", layer=layer)
    if verified:
        from .render import measure_text
        tw = measure_text(name, "Georgia", 30, "bold")
        c.circle(x + 120 + tw + 22, y + 42, 12, IOS_BLUE, layer=layer)
        c.path(f"M{x + 120 + tw + 15} {y + 42} L{x + 120 + tw + 20} {y + 47} L{x + 120 + tw + 29} {y + 37}", stroke="#fff", w=3, layer=layer)
    c.text(x + 120, y + 84, sub, size=20, font="ui", fill="#777", layer=layer)
    c.rect(x + w - 200, y + 34, 170, 52, "#EFEFEF", layer=layer, rx=10)
    c.text(x + w - 115, y + 68, button, size=22, font="ui", fill="#111", anchor="middle", weight="600", layer=layer)


def stats_row(c: Canvas, x, y, w, stats, *, layer="ui", color="#111"):
    n = len(stats)
    for i, (num, lab) in enumerate(stats):
        cx = x + w * (i + 0.5) / n
        c.text(cx, y + 30, num, size=28, font="ui", fill=color, weight="bold", anchor="middle", layer=layer)
        c.text(cx, y + 62, lab, size=22, font="ui", fill=color, anchor="middle", weight="600", layer=layer)


def ticket(c: Canvas, x, y, w, h, *, layer="ui", fill="#fff", notch_r=36, notch_y=None):
    """Ticket card with side notches and a dashed tear line."""
    ny = notch_y or y + h * 0.78
    d = (f"M{x + 24} {y} H{x + w - 24} Q{x + w} {y} {x + w} {y + 24} V{ny - notch_r} A{notch_r} {notch_r} 0 0 0 {x + w} {ny + notch_r} "
         f"V{y + h - 24} Q{x + w} {y + h} {x + w - 24} {y + h} H{x + 24} Q{x} {y + h} {x} {y + h - 24} V{ny + notch_r} "
         f"A{notch_r} {notch_r} 0 0 0 {x} {ny - notch_r} V{y + 24} Q{x} {y} {x + 24} {y} Z")
    c.path(d, fill=fill, layer=layer)
    c.line(x + notch_r + 10, ny, x + w - notch_r - 10, ny, "#CFCFCF", 2, layer=layer, dash="10 10")
    return ny


def mac_open_dialog(c: Canvas, x, y, w, h, *, layer="ui", title="Open", folder="Documents", photo=None,
                    side=("Files", "Calendar", "Document", "Network", "Links", "Pictures", "Desktop")):
    """Classic-Mac style Open dialog (INS-119): sidebar list, name/date header, photo in file area."""
    c.rect(x, y, w, h, "#F5F5F5", layer=layer, rx=10, stroke="#BDBDBD", stroke_w=2)
    c.text(x + w / 2, y + 36, title, size=24, font="ui", fill="#222", anchor="middle", layer=layer)
    # nav buttons + path field
    c.rect(x + 20, y + 56, 60, 30, "#E8E8E8", layer=layer, rx=6, stroke="#C8C8C8")
    c.text(x + 50, y + 77, "◁ ▷", size=16, font="sans", fill="#444", anchor="middle", layer=layer)
    c.rect(x + 96, y + 56, 60, 30, "#E8E8E8", layer=layer, rx=6, stroke="#C8C8C8")
    c.text(x + 126, y + 77, "☷ ▭", size=16, font="sans", fill="#444", anchor="middle", layer=layer)
    c.rect(x + 176, y + 56, w - 196, 30, "#fff", layer=layer, rx=6, stroke="#C8C8C8")
    c.text(x + w / 2 + 80, y + 77, folder, size=16, font="ui", fill="#333", anchor="middle", layer=layer)
    # sidebar
    sx, sy, sw, sh = x + 20, y + 100, 120, h - 170
    c.rect(sx, sy, sw, sh, "#fff", layer=layer, stroke="#C8C8C8")
    for i, it in enumerate(side):
        c.text(sx + 12, sy + 28 + i * 26, it, size=15, font="ui", fill="#333", layer=layer)
    # file area
    fx, fy, fw, fh = sx + sw + 12, sy, w - sw - 52, sh
    c.rect(fx, fy, fw, fh, "#fff", layer=layer, stroke="#C8C8C8")
    c.text(fx + 12, fy + 24, "Name", size=15, font="ui", fill="#555", layer=layer)
    c.text(fx + fw - 12, fy + 24, "↓ Date  ↗", size=15, font="ui", fill="#555", anchor="end", layer=layer)
    c.line(fx, fy + 34, fx + fw, fy + 34, "#DDD", 1, layer=layer)
    if photo is not None:
        c.photo_rect(photo, fx + 10, fy + 44, fw - 20, fh - 54, layer=layer)
    # buttons
    by = y + h - 56
    for i, lab in enumerate(("Cancel", "Open")):
        bx = x + w - 20 - (2 - i) * 100 + 10
        c.rect(bx, by, 86, 32, "#E8E8E8", layer=layer, rx=8, stroke="#B5B5B5")
        c.text(bx + 43, by + 22, lab, size=16, font="ui", fill="#222", anchor="middle", layer=layer)


def photo_grid(c: Canvas, x, y, w, cols, rows, photos, *, gap=6, cell_h=None, layer="photos", hearts=None, rx=0, focus=(0.5, 0.4), numbers=None):
    """Simple grid of photo windows; photos is a list of photo indices (cycled if short)."""
    cw = (w - gap * (cols - 1)) / cols
    ch = cell_h or cw * 4 / 3
    k = 0
    for r in range(rows):
        for cc in range(cols):
            i = photos[k % len(photos)]; k += 1
            px, py = x + cc * (cw + gap), y + r * (ch + gap)
            c.photo_rect(i, px, py, cw, ch, layer=layer, rx=rx, focus=focus)
            if hearts and (r, cc) in hearts:
                icon_heart(c, px + 28, py + ch - 30, 13, fill="#fff", layer="ui")
            if numbers:
                c.circle(px + cw - 24, py + 24, 14, "rgba(0,0,0,0.5)", layer="ui")
                c.text(px + cw - 24, py + 30, str(k), size=16, font="ui", fill="#fff", anchor="middle", layer="ui")
    return (x, y, w, rows * ch + gap * (rows - 1))
