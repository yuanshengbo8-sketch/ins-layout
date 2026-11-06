"""INS-037 — the letters N O V E M B E R scattered large in pink around the figure, small date note and yellow stars
Page 2, photos: 1.  Generated-asset dependencies: none.
"""
from components import deco  # noqa: F401
from templates._text import framed_photo, stacked
from templates._common import T

META = {"id": "INS-037", "photos": 1, "assets": [], "family": "big-words",
        "photo_notes": "one portrait photo; keep the face clear of the text block (the letters N O V E M B E R scattered large in pink around the figure, small date note and yellow stars)"}

LINES = ['N', 'O', 'V', 'E', 'M', 'B', 'E', 'R']


def build(c, ctx):
    framed_photo(c, 0, frame=(0, 0, 0, 0), focus=(0.5, 0.4))
    lines = T(ctx, "lines", None)
    lines = lines.split("|") if lines else LINES
    c.text(170, 290, lines[0] if 0 < len(lines) else '', size=330, fill='#F39ACB', anchor='middle', weight='normal', rotate=-8)
    c.text(470, 300, lines[1] if 1 < len(lines) else '', size=330, fill='#F39ACB', anchor='middle', weight='normal', rotate=6)
    c.text(940, 460, lines[2] if 2 < len(lines) else '', size=330, fill='#F39ACB', anchor='middle', weight='normal', rotate=-10)
    c.text(910, 700, lines[3] if 3 < len(lines) else '', size=330, fill='#F39ACB', anchor='middle', weight='normal', rotate=20)
    c.text(540, 900, lines[4] if 4 < len(lines) else '', size=330, fill='#F39ACB', anchor='middle', weight='normal', rotate=-4)
    c.text(200, 1130, lines[5] if 5 < len(lines) else '', size=330, fill='#F39ACB', anchor='middle', weight='normal', rotate=-6)
    c.text(480, 1300, lines[6] if 6 < len(lines) else '', size=330, fill='#F39ACB', anchor='middle', weight='normal', rotate=8)
    c.text(990, 1100, lines[7] if 7 < len(lines) else '', size=330, fill='#F39ACB', anchor='middle', weight='normal', rotate=12)
    c.text(980, 900, '1st week of', size=40, fill='#F39ACB', anchor='middle', rotate=-12)
    c.text(990, 950, 'november', size=40, fill='#F39ACB', anchor='middle', rotate=-12)
    c.text(1000, 1000, str(ctx['date'].year), size=40, fill='#F39ACB', anchor='middle', rotate=-12)
    deco.star(c, 95, 85, 22, '#F2D34B')
    deco.star(c, 1070, 740, 20, '#F2D34B')
    deco.star(c, 190, 1460, 22, '#F2D34B')
    deco.heart(c, 1010, 760, 16, '#E8303A')
