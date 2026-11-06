"""INS-112 — two stacked photos with a dark iOS weather widget ('☀ 14° / Mostly Sunny / ↑18° ↓6°') over the top
of the lower photo.  Page 7, photos: 2.  Generated-asset dependencies: none.  Weather text comes from --text.
"""
from components import ui
from templates._common import T

META = {"id": "INS-112", "photos": 2, "assets": [], "family": "ui-weather", "photo_notes": "2 photos"}


def build(c, ctx):
    c.bg = "#EEECE7"
    c.photo_rect(0, 0, 50, 1200, 740, focus=(0.5, 0.3))
    c.photo_rect(1, 0, 800, 1200, 750, focus=(0.5, 0.45))
    ui.weather_widget(c, 230, 850, 740, 170, T(ctx, "temp", "14°"), T(ctx, "desc", "Mostly Sunny"), T(ctx, "hi", "18°"), T(ctx, "lo", "6°"))
