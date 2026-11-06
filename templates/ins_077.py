"""INS-077 — striped bedsheet (G21 master) with an iOS AirDrop receive card in the centre holding the photo
(Decline | Accept).  Page 5, photos: 1.  Requires master G21.
"""
from components import ui
from templates._assets import require

META = {"id": "INS-077", "photos": 1, "assets": ["G21"], "family": "carrier-airdrop", "photo_notes": "one close portrait (landscape crop inside the card)"}


def build(c, ctx):
    c.image_file(require(ctx, "G21", "grey-white striped bedsheet"), 0, 0, 1200, 1600, layer="bg")
    ui.airdrop_card(c, 290, 420, 620, photo=0)
