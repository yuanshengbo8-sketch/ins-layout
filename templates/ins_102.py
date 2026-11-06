"""INS-102 — selfie dressed as an IG post: white header bar with avatar + heart, a '🎀✨' thought bubble, a dark
'me time · On' focus pill, a 'love' pin sticker, a dark music pill 'Me And My Girls / time to drink', the IG action
row and a cloud-cream strawberry cake sticker (G46) on the shoulder.  Page 7, photos: 1.  Requires master G46.
"""
from components import ui
from templates._assets import require
from templates._common import T

META = {"id": "INS-102", "photos": 1, "assets": ["G46"], "family": "ui-ig-post", "photo_notes": "one selfie, head upper third"}


def build(c, ctx):
    c.photo_full(0, focus=(0.5, 0.35))
    c.rect(200, 60, 820, 110, "#fff", rx=18, layer="ui")
    c.photo_circle(0, 250, 115, 30, focus=(0.5, 0.25))
    ui.icon_heart(c, 300, 118, 10, fill="#2F8BFF", layer="ui")
    c.text(990, 125, "•••", size=26, font="ui", fill="#111", anchor="end", layer="ui")
    ui.pill(c, 90, 260, T(ctx, "emoji", "🎀✨🎁"), size=30, fill="#fff", color="#111", pad=20, h=70)
    c.rect(860, 380, 260, 100, "#111", rx=22, layer="ui")
    ui.icon_heart(c, 905, 430, 14, fill="#FF375F", layer="ui")
    c.text(945, 422, T(ctx, "focus", "me time"), size=22, font="ui", fill="#fff", layer="ui"); c.text(945, 452, "On", size=18, font="ui", fill="#999", layer="ui")
    c.rect(70, 630, 170, 170, "#fff", layer="ui")
    c.text(155, 735, "love", size=34, font="ui", fill="#111", anchor="middle", layer="ui")
    c.circle(110, 690, 8, "#2F8BFF", layer="ui"); c.circle(195, 760, 8, "#2F8BFF", layer="ui")
    c.rect(70, 1060, 460, 90, "#111", rx=20, layer="ui")
    c.text(110, 1098, "♪", size=24, font="sans", fill="#fff", layer="ui")
    c.text(150, 1095, T(ctx, "song", "Me And My Girls"), size=22, font="ui", fill="#fff", weight="bold", layer="ui")
    c.text(150, 1125, T(ctx, "artist", "time to drink"), size=18, font="ui", fill="#aaa", layer="ui")
    ui.icon_ig_actions(c, 190, 1190, 820, 70)
    c.image_file(require(ctx, "G46_cake", "cloud-cream strawberry cake sticker"), 880, 880, 230, None, layer="deco")
