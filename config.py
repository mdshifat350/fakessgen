# config.py
BOT_TOKEN = "9038564432:AAFnoSLiPKeeZgZ2hJtcyVDB5ZrYrfEm1Z0"

import os

BASE = os.path.dirname(os.path.abspath(__file__))

FONT_BOLD = os.path.join(BASE, "fonts", "Inter-Bold.ttf")
FONT_REG  = os.path.join(BASE, "fonts", "Inter-Regular.ttf")

ASSETS = os.path.join(BASE, "assets")

# প্রতিটা brand এর real color palette
BRANDS = {
    "bkash": {
        "name": "bKash",
        "header": "#E2136E",
        "accent": "#E2136E",
        "bg":     "#F5F5F5",
        "card":   "#FFFFFF",
        "text":   "#1A1A1A",
        "sub":    "#7A7A7A",
        "logo":   os.path.join(ASSETS, "bkash_logo.png"),
    },
    "nagad": {
        "name": "Nagad",
        "header": "#EE1C25",
        "accent": "#F6921E",
        "bg":     "#F5F5F5",
        "card":   "#FFFFFF",
        "text":   "#1A1A1A",
        "sub":    "#7A7A7A",
        "logo":   os.path.join(ASSETS, "nagad_logo.png"),
    },
    "rocket": {
        "name": "Rocket",
        "header": "#8C3494",
        "accent": "#8C3494",
        "bg":     "#F5F5F5",
        "card":   "#FFFFFF",
        "text":   "#1A1A1A",
        "sub":    "#7A7A7A",
        "logo":   os.path.join(ASSETS, "rocket_logo.png"),
    },
    "upay": {
        "name": "Upay",
        "header": "#FDB913",
        "accent": "#FDB913",
        "bg":     "#F5F5F5",
        "card":   "#FFFFFF",
        "text":   "#1A1A1A",
        "sub":    "#7A7A7A",
        "logo":   os.path.join(ASSETS, "upay_logo.png"),
    },
    "binance": {
        "name": "Binance",
        "header": "#0B0E11",
        "accent": "#F0B90B",
        "bg":     "#0B0E11",
        "card":   "#1E2329",
        "text":   "#EAECEF",
        "sub":    "#848E9C",
        "logo":   os.path.join(ASSETS, "binance_logo.png"),
    },
}