import sys
import os
import asyncio
sys.stdout.reconfigure(encoding='utf-8')

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackQueryHandler,
    filters,
)
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = 2143651307

user_step = {}
user_data = {}

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_step[user_id] = "start"

    await update.message.reply_text(
        "Hey! I can help you earn 10$ per day if you have discipline\n\n"
        "🚨Answer a few questions below to join the VIP group!"
    )

    keyboard = [[InlineKeyboardButton("YES", callback_data="experience_yes")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Do you have any trading experience?📊",
        reply_markup=reply_markup
    )

# --- BUTTON HANDLER ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if data == "experience_yes":
        user_step[user_id] = "step1"
        keyboard = [
            [InlineKeyboardButton("Crypto", callback_data="platform_crypto"),
             InlineKeyboardButton("Forex", callback_data="platform_forex")],
            [InlineKeyboardButton("Other...", callback_data="platform_other_custom")]
        ]
        await query.message.reply_text("Your best trade?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data in ["platform_crypto", "platform_forex", "platform_other_custom"]:
        user_step[user_id] = "step2"
        keyboard = [
            [InlineKeyboardButton("Binance", callback_data="platform_binance"),
             InlineKeyboardButton("Exness", callback_data="platform_exness"),
             InlineKeyboardButton("Bybit", callback_data="platform_bybit")],
            [InlineKeyboardButton("Vantage", callback_data="platform_vantage"),
             InlineKeyboardButton("FBS", callback_data="platform_fbs"),
             InlineKeyboardButton("OKX", callback_data="platform_okx")],
            [InlineKeyboardButton("Other...", callback_data="platform_other_final")]
        ]
        await query.message.reply_text(
            "Where do you usually make your profit?📈",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("platform_") and data not in ["platform_other_custom", "platform_other_final"]:
        user_step[user_id] = "step3"
        keyboard = [
            [InlineKeyboardButton("Viet Nam 🇻🇳", callback_data="country_vietnam"),
             InlineKeyboardButton("America 🇺🇸", callback_data="country_america")],
            [InlineKeyboardButton("Singapore 🇸🇬", callback_data="country_singapore"),
             InlineKeyboardButton("Australia 🇦🇺", callback_data="country_australia")],
            [InlineKeyboardButton("Other...", callback_data="country_other_custom")]
        ]
        await query.message.reply_text(
            "Thank you! which country do you live in?🌎🌍🌏",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "platform_other_final":
        user_step[user_id] = "step3"
        keyboard = [
            [InlineKeyboardButton("Viet Nam 🇻🇳", callback_data="country_vietnam"),
             InlineKeyboardButton("America 🇺🇸", callback_data="country_america")],
            [InlineKeyboardButton("Singapore 🇸🇬", callback_data="country_singapore"),
             InlineKeyboardButton("Australia 🇦🇺", callback_data="country_australia")],
            [InlineKeyboardButton("Other...", callback_data="country_other_custom")]
        ]
        await query.message.reply_text(
            "Thank you! which country do you live in?🌎🌍🌏",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("country_"):
        user_step[user_id] = "step4"

        if data == "country_other_custom":
            await send_crypto_forex_question(query)
        else:
            country_map = {
                "country_vietnam": "Viet Nam",
                "country_america": "America",
                "country_singapore": "Singapore",
                "country_australia": "Australia"
            }
            country = country_map.get(data, "somewhere")

            await query.message.reply_text(
                f"Most of my members are from {country} as well!\n\n"
                "Awesome! You're all set for the last FREE VIP spot!️🏆"
            )
            await send_crypto_forex_question(query)

    elif data == "experience_crypto1":
        user_step[user_id] = "step5"
        user_data.setdefault(user_id, {})["type"] = "Crypto"
        keyboard = [
            [InlineKeyboardButton("Binance", callback_data="experience_bnb"),
             InlineKeyboardButton("Bybit", callback_data="experience_bb")]
        ]
        await query.message.reply_text(
            "Choose an exchange you are not registered with!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "experience_bnb":
        user_step[user_id] = "finished"
        user_data.setdefault(user_id, {})["broker"] = "Binance"
        await query.message.reply_text("Nice. I will help you to open the account!👜\n\nThere are 2 steps to open.✌️")
        await query.message.reply_text("▀▄▀▄▀▄Step 1▄▀▄▀▄▀\n\nClick the link that you want to open account!")
        await query.message.reply_text("▀▄▀▄▀▄Step 2▄▀▄▀▄▀\n\nFill in referral code and do KYC.")
        await query.message.reply_text("Link:\nhttps://accounts.binance.com/en/register?ref=725428593\nCODE:\n725428593")
        await query.message.reply_text("Remember!\nWe will check the system to make sure you have completed all the steps before we can approve you as a VIP.")
        await query.message.reply_text("✔️Enter your UID if you are finished!")

    elif data == "experience_bb":
        user_step[user_id] = "finished"
        user_data.setdefault(user_id, {})["broker"] = "Bybit"
        await query.message.reply_text("Nice. I will help you to open the account!👜\n\nThere are 2 steps to open.✌️")
        await query.message.reply_text("▀▄▀▄▀▄Step 1▄▀▄▀▄▀\n\nClick the link that you want to open account!")
        await query.message.reply_text("▀▄▀▄▀▄Step 2▄▀▄▀▄▀\n\nFill in referral code and do KYC.")
        await query.message.reply_text("Link:\nhttps://www.bybitglobal.com/invite?ref=G7Y9RYY\nCODE:\nG7Y9RYY")
        await query.message.reply_text("Remember!\nWe will check the system to make sure you have completed all the steps before we can approve you as a VIP.")
        await query.message.reply_text("✔️Enter your UID if you are finished!")

    elif data == "experience_forex1":
        user_step[user_id] = "step5"
        user_data.setdefault(user_id, {})["type"] = "Forex"
        keyboard = [
            [InlineKeyboardButton("Exness", callback_data="experience_exness"),
             InlineKeyboardButton("FBS", callback_data="experience_fbs")]
        ]
        await query.message.reply_text(
            "Choose a broker you are not registered with!",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "experience_exness":
        user_step[user_id] = "finished"
        user_data.setdefault(user_id, {})["broker"] = "Exness"
        await query.message.reply_text("GOOD CHOICE!\nExness has:\n✅ VERY LOW spread widening\n✅ UNLIMITED levelrage\nI will help you to open the account!👜\n\nThere are 2 steps to open.✌️")
        await query.message.reply_text("▀▄▀▄▀▄Step 1▄▀▄▀▄▀\n\nClick the link that you want to open account!")
        await query.message.reply_text("▀▄▀▄▀▄Step 2▄▀▄▀▄▀\n\nFill in referral partner code and do KYC.")
        await query.message.reply_text("Link:\nhttps://one.exnesstrack.org/a/nz1kozjxi0\nCODE:\nnz1kozjxi0")
        await query.message.reply_text("Remember!\nWe will check the system to make sure you have completed all the steps before we can approve you as a VIP.")
        await query.message.reply_text("Enter your UID if you are finished!✔️")
        await query.message.reply_text("Try using the 1.1.1.1 app when you can't connect.")

    elif data == "experience_fbs":
        user_step[user_id] = "finished"
        user_data.setdefault(user_id, {})["broker"] = "FBS"
        await query.message.reply_text("GOOD CHOICE!\nFBS has:\n✅ LOW spread widening\n✅ LOW deposit\n✅ HIGH levelrage\nI will help you to open the account!👜\n\nThere are 2 steps to open.✌️")
        await query.message.reply_text("▀▄▀▄▀▄Step 1▄▀▄▀▄▀\n\nClick the link that you want to open account!")
        await query.message.reply_text("▀▄▀▄▀▄Step 2▄▀▄▀▄▀\n\nFill in referral partner code and do KYC.")
        await query.message.reply_text("Link:\nhttps://fbs.partners?ibl=984325&ibp=37468699\nCODE:\n37468699")
        await query.message.reply_text("Remember!\nWe will check the system to make sure you have completed all the steps before we can approve you as a VIP.")
        await query.message.reply_text("Enter your UID if you are finished!✔️")
        await query.message.reply_text("Try using the 1.1.1.1 app when you can't connect.")

# --- GỬI CÂU HỎI CHỌN CRYPTO/FOREX ---
async def send_crypto_forex_question(query):
    keyboard = [
        [InlineKeyboardButton("Crypto", callback_data="experience_crypto1"),
         InlineKeyboardButton("Forex", callback_data="experience_forex1")]
    ]
    await query.message.reply_text(
        "Do you wanna join Crypto or Forex?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- NHẬN UID ---
async def block_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text
    user = update.message.from_user

    if user_step.get(user_id) != "finished":
        await update.message.reply_text("❗Please complete all steps before submitting your UID.")
        return

    await update.message.reply_text("✅ Thank you! Please wait while we verify your account for VIP access.")
    info = user_data.get(user_id, {})
    text = (
        f"🆕 New UID submitted:\n\n"
        f"👤 Name: {user.first_name} (@{user.username or 'no username'})\n"
        f"📊 Type: {str(info.get('type', 'N/A'))}\n"
        f"🏦 Broker: {str(info.get('broker', 'N/A'))}\n"
        f"🆔 User ID: {user.id}\n"
        f"📨 UID Message: {message}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=text)

# --- CHẠY BOT ---
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    await app.bot.delete_webhook(drop_pending_updates=True)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, block_user_input))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
