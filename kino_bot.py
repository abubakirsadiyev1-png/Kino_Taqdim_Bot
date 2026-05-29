import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes,
)

BOT_TOKEN   = "8802276015:AAHkGGIl0Syr4d-P6NUXM5-cMFSERaBQS8w"
KANAL_ID    = "@abushi_kino1"
KANAL_LINK  = "https://t.me/abushi_kino1"
ADMIN_ID    = 8476805197
OBUNA_SHART = True

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def obuna_bormi(user_id, context):
    if not OBUNA_SHART:
        return True
    try:
        m = await context.bot.get_chat_member(KANAL_ID, user_id)
        return m.status in ("member","administrator","creator")
    except:
        return False

async def obuna_xabari(update, context):
    kb = [[InlineKeyboardButton("📢 Kanalga Azo Bolish", url=KANAL_LINK)],
          [InlineKeyboardButton("✅ Azo Boldim", callback_data="tekshir")]]
    await update.message.reply_text(
        "⚠️ <b>Botdan foydalanish uchun kanalga azo boling!</b>\n\n"
        "1️⃣ Kanalga kiring\n2️⃣ Azo boling\n3️⃣ Azo Boldim bosing",
        parse_mode="HTML", reply_markup=InlineKeyboardMarkup(kb))

async def start(update, context):
    ism = update.effective_user.first_name or "Dostim"
    if context.args:
        await kino_yuborish(update, context, context.args[0])
        return
    kb = [[InlineKeyboardButton("📢 Kanal", url=KANAL_LINK)],
          [InlineKeyboardButton("❓ Yordam", callback_data="yordam")]]
    await update.message.reply_text(
        f"🎬 <b>Assalomu Alaykum, {ism}!</b>\n\n"
        "🤖 <b>KinoTaqdimBot</b> ga xush kelibsiz!\n\n"
        "📌 Kanalimizda kino kodini toping\n"
        "🔢 Shu raqamni botga yuboring\n"
        "✅ Kino darhol yuboriladi!\n\n"
        "💰 Bepul!  ⚡ 24/7 ishlaydi!",
        parse_mode="HTML", reply_markup=InlineKeyboardMarkup(kb))

async def yordam_cmd(update, context):
    await update.message.reply_text(
        "❓ <b>YORDAM</b>\n\n"
        "1. @abushi_kino1 ga oling\n"
        "2. Kino ostidagi raqamni toping\n"
        "3. Shu raqamni botga yuboring\n"
        "4. Kino keladi! 🎬\n\n"
        "<b>Misol:</b> <code>42</code>",
        parse_mode="HTML")

async def kino_yuborish(update, context, kod):
    if not await obuna_bormi(update.effective_user.id, context):
        await obuna_xabari(update, context)
        return
    kod2 = kod.upper().replace("#","").replace(" ","")
    msg_id = None
    if kod2.isdigit():
        msg_id = int(kod2)
    elif kod2.startswith("KINO") and kod2[4:].isdigit():
        msg_id = int(kod2[4:])
    if msg_id is None:
        await update.message.reply_text(
            "❌ Notogri kod!\nMisol: <code>42</code>", parse_mode="HTML")
        return
    k = await update.message.reply_text("⏳ Qidirilmoqda...", parse_mode="HTML")
    try:
        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=KANAL_ID, message_id=msg_id)
        await k.delete()
        await update.message.reply_text(
            "✅ Mana kinongiz!\n🍿 Yaxshi tomoshalashlar!\n📢 @abushi_kino1",
            parse_mode="HTML")
    except Exception as e:
        await k.delete()
        await update.message.reply_text(
            f"❌ <b>{kod}</b> kodi topilmadi.\nKanaldan kodni qayta oling.",
            parse_mode="HTML")

async def xabar_qabul(update, context):
    await kino_yuborish(update, context, update.message.text.strip())

async def admin_cmd(update, context):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Faqat admin uchun!")
        return
    await update.message.reply_text(
        "👑 <b>ADMIN PANEL</b>\n\n✅ Bot ishlayapti\n\n"
        "<b>Kino qoshish:</b>\n"
        "1. @abushi_kino1 ga kino yuklang\n"
        "2. Post link oling: t.me/abushi_kino1/<b>42</b>\n"
        "3. Caption: 🎬 Film nomi\n🔑 Kod: 42\n"
        "4. Foydalanuvchi <code>42</code> yozsa kino ketadi ✅",
        parse_mode="HTML")

async def callback_handler(update, context):
    q = update.callback_query
    await q.answer()
    if q.data == "tekshir":
        if await obuna_bormi(q.from_user.id, context):
            await q.message.edit_text(
                "✅ Rahmat! Kino kodini yuboring 👇", parse_mode="HTML")
        else:
            await q.answer("❌ Hali azo emassiz!", show_alert=True)
    elif q.data == "yordam":
        await q.message.reply_text(
            "Kanaldan kodno olib yuboring.\nMisol: <code>42</code>",
            parse_mode="HTML")

def main():
    print("🎬 KinoTaqdimBot ishga tushdi!")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("yordam", yordam_cmd))
    app.add_handler(CommandHandler("help", yordam_cmd))
    app.add_handler(CommandHandler("admin", admin_cmd))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, xabar_qabul))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
