# generators.py
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, time, os
from config import FONT_BOLD, FONT_REG, BRANDS

# ---------- helpers ----------
def font(path, size):
    try:    return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

def mask(num: str) -> str:
    num = str(num)
    if len(num) <= 4: return num
    return num[:3] + "****" + num[-3:]

def txn_id(prefix="TRX"):
    return f"{prefix}{random.randint(10**11, 10**12-1)}"

def now_str():
    return time.strftime("%d %b %Y, %I:%M %p")

def draw_rounded(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)

def center_text(d, box_x, box_w, text, fnt, fill):
    bbox = d.textbbox((0,0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    d.text((box_x + (box_w - tw)//2, 0), text, font=fnt, fill=fill)

def paste_logo(img, logo_path, x, y, w=180):
    """লোগো থাকলে পেস্ট করবে, না থাকলে টেক্সট লিখবে"""
    try:
        logo = Image.open(logo_path).convert("RGBA")
        ratio = w / logo.width
        logo = logo.resize((w, int(logo.height * ratio)), Image.LANCZOS)
        img.paste(logo, (x, y), logo)
        return True
    except Exception:
        return False

# =========================================================
#  WALLET SCREENSHOT (bKash / Nagad / Rocket / Upay)
# =========================================================
def wallet_ss(provider, sender, receiver, amount, txn_type,
              date=None, txn_ref=None):
    b = BRANDS[provider]
    txn_ref  = txn_ref or txn_id("TRX" if provider != "nagad" else "NGD")
    date     = date    or now_str()

    W, H = 720, 1400
    img  = Image.new("RGB", (W, H), b["bg"])
    d    = ImageDraw.Draw(img)

    # ---- HEADER (colored top bar) ----
    d.rectangle([0, 0, W, 320], fill=b["header"])

    # Logo (top-left)
    if not paste_logo(img, b["logo"], 40, 40, w=170):
        d.text((40, 40), b["name"], font=font(FONT_BOLD, 54), fill="#FFFFFF")

    # Top-right help icon
    d.text((W-80, 45), "?", font=font(FONT_BOLD, 40), fill="#FFFFFF")

    # Header title
    d.text((40, 130), "Transaction Successful",
           font=font(FONT_BOLD, 40), fill="#FFFFFF")

    # Big amount on header
    d.text((40, 195), f"৳ {amount}",
           font=font(FONT_BOLD, 72), fill="#FFFFFF")

    # checkmark bottom-right of header
    cx, cy, r = W-110, 240, 48
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill="#FFFFFF")
    d.text((cx-22, cy-30), "✓", font=font(FONT_BOLD, 56), fill=b["header"])

    # ---- CARD ----
    card_top = 260
    draw_rounded(d, [24, card_top, W-24, H-40], 24, b["card"])

    # Rows
    label_f = font(FONT_REG, 24)
    value_f  = font(FONT_BOLD, 30)
    tx, ty   = 60, card_top + 60
    gap      = 92

    if txn_type.lower() == "cash out":
        rows = [
            ("Cash Out Amount", f"৳ {amount}"),
            ("Agent Number",    mask(receiver)),
            ("From Number",     mask(sender)),
        ]
    else:
        rows = [
            ("Send Money Amount", f"৳ {amount}"),
            ("Receiver",          mask(receiver)),
            ("Sender",            mask(sender)),
        ]

    rows += [
        ("Transaction ID", txn_ref),
        ("Date & Time",    date),
        ("Charge",         "৳ 0.00"),
        ("Total Amount",   f"৳ {amount}"),
        ("Reference",      f"{b['name'].lower()}-proof"),
    ]

    for label, val in rows:
        d.text((tx, ty), label, font=label_f, fill=b["sub"])
        d.text((tx, ty + 32), val, font=value_f, fill=b["text"])
        d.line([(tx, ty + 76), (W-60, ty + 76)], fill="#EDEDED", width=1)
        ty += gap

    # ---- FOOTER ----
    d.text((W//2 - 170, ty + 20),
           f"Thank you for using {b['name']}",
           font=font(FONT_REG, 22), fill=b["sub"])

    # Watermark-ish verified strip
    d.rectangle([24, H-90, W-24, H-40], fill=b["header"])
    d.text((W//2 - 110, H-78), "✓ Verified Transaction",
           font=font(FONT_BOLD, 24), fill="#FFFFFF")

    out = f"ss_{provider}_{int(time.time())}.png"
    img.save(out, "PNG", quality=95)
    return out


# =========================================================
#  BINANCE SCREENSHOT
# =========================================================
def binance_ss(sender, receiver, amount, txn_type,
               date=None, ref=None):
    b    = BRANDS["binance"]
    ref  = ref  or f"BIN{random.randint(10**13, 10**14-1)}"
    date = date or now_str()

    W, H = 720, 1400
    img  = Image.new("RGB", (W, H), b["bg"])
    d    = ImageDraw.Draw(img)

    # Top bar
    d.rectangle([0, 0, W, 110], fill=b["card"])
    if not paste_logo(img, b["logo"], 40, 30, w=200):
        d.text((40, 30), "Binance", font=font(FONT_BOLD, 48), fill=b["accent"])
    d.text((W-140, 45), "Close", font=font(FONT_REG, 26), fill=b["sub"])

    # Big green check circle
    cx, cy, r = W//2, 300, 90
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill="#2EBD85")
    d.text((cx-42, cy-58), "✓", font=font(FONT_BOLD, 100), fill="#FFFFFF")

    # Title
    d.text((W//2-140, cy+r+30), "Transaction Completed",
           font=font(FONT_BOLD, 34), fill=b["text"])

    # Amount
    d.text((W//2-160, cy+r+90), f"{amount} USDT",
           font=font(FONT_BOLD, 68), fill="#2EBD85")

    # Card
    card_top = 680
    draw_rounded(d, [24, card_top, W-24, card_top+560], 20, b["card"])

    label_f = font(FONT_REG, 24)
    value_f = font(FONT_BOLD, 28)
    tx, ty  = 60, card_top + 50
    gap     = 100

    rows = [
        ("Type",           txn_type),
        ("From",           sender),
        ("To",             receiver),
        ("Amount",         f"{amount} USDT"),
        ("Transaction ID", ref),
        ("Time",           date),
        ("Status",         "✅ Completed"),
        ("Network",        "BSC (BEP20)"),
    ]
    for label, val in rows:
        d.text((tx, ty), label, font=label_f, fill=b["sub"])
        d.text((tx, ty + 30), val, font=value_f, fill=b["text"])
        d.line([(tx, ty + 82), (W-60, ty + 82)], fill="#2B3139", width=1)
        ty += gap

    # Footer button
    draw_rounded(d, [40, H-140, W-40, H-60], 16, b["accent"])
    d.text((W//2-70, H-120), "View on Explorer",
           font=font(FONT_BOLD, 28), fill="#000000")

    out = f"ss_binance_{int(time.time())}.png"
    img.save(out, "PNG", quality=95)
    return out