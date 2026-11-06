"""INS-146 — portrait on the left 55%, a tall blue music panel on the right (album art, 'Croissant Radio',
'little joys · Personal radio', progress 1:36, ◀◀ ▮▮ ▶▶, a 'Radio' pill) with a small dark now-playing bar top-right.
Page 10, photos: 1.  Album art: G23 master if present, else native cover (registered substitute).
"""
from components import ui
from templates._common import T
from templates._assets import cover_art

META = {"id": "INS-146", "photos": 1, "assets": ["G23:optional"], "family": "ui-music", "photo_notes": "one portrait, subject on the left half"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 40, 1200, 1520, focus=(0.3, 0.3))
    # right panel
    x, y, w, h = 650, 260, 560, 1200
    c.rect(x, y, w, h, "#4A74B8", layer="ui", rx=40)
    c.rect(x + 40, y + 40, w - 40, h - 80, "#3D63A6", layer="ui", rx=34)
    cover_art(c, ctx, x + 150, y + 180, 260, variant="navy")
    c.text(x + 80, y + 560, T(ctx, "title", "Croissant Radio"), size=40, font="ui", fill="#fff", weight="bold", layer="ui")
    c.text(x + 80, y + 610, T(ctx, "sub", "little joys · Personal radio"), size=24, font="ui", fill="rgba(255,255,255,0.75)", layer="ui")
    c.line(x + 80, y + 680, x + w - 80, y + 680, "rgba(255,255,255,0.3)", 6, layer="ui", cap="round")
    c.line(x + 80, y + 680, x + 80 + (w - 160) * 0.3, y + 680, "#fff", 6, layer="ui", cap="round")
    c.text(x + 80, y + 650, "1:36", size=22, font="ui", fill="rgba(255,255,255,0.8)", layer="ui")
    ty = y + 790; s = 26
    c.path(f"M{x + 130} {ty} L{x + 130 + s} {ty - s * 0.6} V{ty + s * 0.6} Z M{x + 130 + s} {ty} L{x + 130 + 2 * s} {ty - s * 0.6} V{ty + s * 0.6} Z", fill="#fff", layer="ui")
    c.rect(x + w / 2 - 22, ty - 24, 14, 48, "#fff", layer="ui"); c.rect(x + w / 2 + 8, ty - 24, 14, 48, "#fff", layer="ui")
    c.path(f"M{x + w - 130} {ty} L{x + w - 130 - s} {ty - s * 0.6} V{ty + s * 0.6} Z M{x + w - 130 - s} {ty} L{x + w - 130 - 2 * s} {ty - s * 0.6} V{ty + s * 0.6} Z", fill="#fff", layer="ui")
    c.line(x + 80, ty + 90, x + w - 80, ty + 90, "rgba(255,255,255,0.3)", 6, layer="ui", cap="round")
    ui.pill(c, x + w / 2 - 90, ty + 140, "◉ Radio", size=24, fill="rgba(255,255,255,0.18)", color="#fff", pad=24, h=56)
    # tiny now-playing bar top-right
    c.rect(880, 60, 300, 70, "#1C2A44", rx=16, layer="ui")
    cover_art(c, ctx, 896, 72, 46, variant="navy")
    c.line(960, 95, 1150, 95, "rgba(255,255,255,0.4)", 4, layer="ui", cap="round")
