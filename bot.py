# bot.py
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)
from config import BOT_TOKEN
from generators import wallet_ss, binance_ss

WAIT_SENDER, WAIT_RECEIVER, WAIT_AMOUNT, WAIT_TYPE = range(4)

PROVIDERS = {
    "bkash":   ("💗 bKash",   "number"),
    "nagad":   ("🟠 Nagad",   "number"),
    "rocket":  ("🚀 Rocket",  "number"),
    "upay":    ("💳 Upay",    "number"),
    "binance": ("🟡 Binance", "email"),
}


# ---------- /start ----------
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await send_menu(update.message.reply_text, ctx)


async def send_menu(reply_fn, ctx):
    kb = [
        [InlineKeyboardButton("💗 bKash",  callback_data="p:bkash"),
         InlineKeyboardButton("🟠 Nagad",  callback_data="p:nagad")],
        [InlineKeyboardButton("🚀 Rocket", callback_data="p:rocket"),
         InlineKeyboardButton("💳 Upay",   callback_data="p:upay")],
        [InlineKeyboardButton("🟡 Binance", callback_data="p:binance")],
    ]
    await reply_fn(
        "🧾 <b>Fake Payment Proof Generator</b>\n\n"
        "👇 নিচ থেকে একটা সিলেক্ট করো:",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode="HTML"
    )


# ---------- Conversation ----------
async def pick_provider(update, ctx):
    q = update.callback_query
    await q.answer()
    provider = q.data.split(":")[1]
    ctx.user_data["provider"] = provider
    label, field = PROVIDERS[provider]
    await q.edit_message_text(
        f"✅ <b>{label}</b> selected.\n\n"
        f"Send <b>sender {field}</b>:",
        parse_mode="HTML"
    )
    return WAIT_SENDER


async def get_sender(update, ctx):
    ctx.user_data["sender"] = update.message.text.strip()
    provider = ctx.user_data["provider"]
    _, field = PROVIDERS[provider]
    await update.message.reply_text(f"Send <b>receiver {field}</b>:",
                                    parse_mode="HTML")
    return WAIT_RECEIVER


async def get_receiver(update, ctx):
    ctx.user_data["receiver"] = update.message.text.strip()
    await update.message.reply_text("Send <b>amount</b> (e.g. 2500):",
                                    parse_mode="HTML")
    return WAIT_AMOUNT


async def get_amount(update, ctx):
    ctx.user_data["amount"] = update.message.text.strip()
    provider = ctx.user_data["provider"]

    if provider == "binance":
        kb = [[
            InlineKeyboardButton("Deposit",  callback_data="t:Deposit"),
            InlineKeyboardButton("Withdraw", callback_data="t:Withdraw"),
        ],[
            InlineKeyboardButton("Transfer", callback_data="t:Transfer"),
        ]]
    else:
        kb = [[
            InlineKeyboardButton("Send Money", callback_data="t:Send Money"),
            InlineKeyboardButton("Cash Out",   callback_data="t:Cash Out"),
        ]]
    await update.message.reply_text("Choose transaction type:",
                                    reply_markup=InlineKeyboardMarkup(kb))
    return WAIT_TYPE


async def get_type(update, ctx):
    q = update.callback_query
    await q.answer()
    txn_type = q.data.split(":", 1)[1]
    d = ctx.user_data
    provider = d["provider"]

    await q.edit_message_text("⏳ Generating…")

    if provider == "binance":
        path = binance_ss(d["sender"], d["receiver"], d["amount"], txn_type)
    else:
        path = wallet_ss(provider, d["sender"], d["receiver"],
                         d["amount"], txn_type)

    with open(path, "rb") as f:
        await q.message.reply_photo(
            photo=f,
            caption=f"✅ <b>{PROVIDERS[provider][0]}</b> • {txn_type}\n"
                    f"Amount: <b>{d['amount']}</b>",
            parse_mode="HTML"
        )
    try: os.remove(path)
    except: pass

    await send_menu(q.message.reply_text, ctx)
    return ConversationHandler.END


async def cancel(update, ctx):
    await update.message.reply_text("❌ Cancelled. /start দাও।")
    return ConversationHandler.END


# ---------- main ----------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(pick_provider, pattern=r"^p:")],
        states={
            WAIT_SENDER:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sender)],
            WAIT_RECEIVER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_receiver)],
            WAIT_AMOUNT:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_amount)],
            WAIT_TYPE:     [CallbackQueryHandler(get_type, pattern=r"^t:")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True, per_chat=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    print("✅ Bot running…")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()