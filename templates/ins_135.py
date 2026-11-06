"""INS-135 — IG profile share card over a blurred photo: header (avatar, 'my.daybook' ✓, 'Personal archive', Following),
3×2 grid, stats row (posts / followers / following), then a white sheet with 'View profile ◎' and 'Send ➤'.
Page 10, photos: 6.  Generated-asset dependencies: none.
"""
from components import ui
from templates._common import T

META = {"id": "INS-135", "photos": 6, "assets": [], "family": "ui-profile", "photo_notes": "6 photos; #1 is also the avatar"}


def build(c, ctx):
    fid = c.blur_filter(18)
    c.photo_full(0, focus=(0.5, 0.4), filter_=fid)
    c.rect(0, 0, 1200, 1600, "rgba(200,200,200,0.35)", layer="photos")
    x, y, w = 40, 150, 1120
    c.rect(x, y, w, 1110, "#fff", rx=22, layer="bg")
    ui.profile_header(c, x, y + 10, w, T(ctx, "name", "my.daybook"), T(ctx, "sub", "Personal archive"), avatar=0)
    ui.photo_grid(c, x, y + 140, w, 3, 2, [0, 1, 2, 3, 4, 5], gap=6, cell_h=370, focus=(0.5, 0.35))
    ui.stats_row(c, x, y + 900, w, [(T(ctx, "posts", "2,315"), "posts"), (T(ctx, "followers", "4.4M"), "followers"), (T(ctx, "following", "3"), "following")])
    c.rect(x, 1310, 780, 240, "#fff", rx=22, layer="ui")
    c.text(x + 40, 1395, "View profile", size=38, font="ui", fill="#111", weight="bold", layer="ui")
    c.circle(x + 700, 1382, 20, "none", stroke="#111", stroke_w=4, layer="ui"); c.circle(x + 700, 1382, 8, "none", stroke="#111", stroke_w=4, layer="ui")
    c.line(x, 1430, x + 780, 1430, "#E5E5EA", 2, layer="ui")
    c.text(x + 40, 1510, "Send", size=38, font="ui", fill="#111", weight="bold", layer="ui")
    c.path(f"M{x + 680} {1510} L{x + 722} {1470} L{x + 660} {1485} L{x + 690} {1495} Z M{x + 690} {1495} L{x + 700} {1518} L{x + 722} {1470}", fill="none", stroke="#111", w=4, layer="ui")
