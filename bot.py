import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

def get_fortune(sign):
    fortunes = {
        "Aries": "🔥 Bold move today — your courage is contagious.",
        "Taurus": "🌿 Pause. Breathe. The answer is in your body, not your head.",
        "Gemini": "💬 Say the thing you’ve been editing in your mind. Raw > perfect.",
        "Cancer": "🌊 Feeling deep? That’s not overwhelm — it’s your super-sensitivity tuning in.",
        "Leo": "✨ You don’t need permission to shine. Adjust your orbit, not your light.",
        "Virgo": "📜 Your attention to detail is magic — just don’t forget to zoom out.",
        "Libra": "⚖️ Harmony isn’t compromise — it’s choosing peace *without* losing yourself.",
        "Scorpio": "🌀 The truth you’re avoiding? It’s not a threat — it’s your next evolution.",
        "Sagittarius": "🏹 Wander — but don’t confuse motion with direction. Where’s your arrow pointed?",
        "Capricorn": "🏔️ Slow is not behind. You’re building foundations others will name landmarks.",
        "Aquarius": "💧 Your weird idea? That’s not noise — it’s the future knocking.",
        "Pisces": "🌌 You feel everything. Remember: empathy is a gift — boundaries are the wrapping."
    }
    return fortunes.get(sign, "✨ Trust your gut — it’s been right all along.")

async def start(update, context):
    await update.message.reply_text(
        "🦊 *FortuneFox* — AI-powered insight for anyone, anywhere.\n\n🌍 Tap your sign:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("♈ Aries", callback_data="Aries"), InlineKeyboardButton("♉ Taurus", callback_data="Taurus")],
            [InlineKeyboardButton("♊ Gemini", callback_data="Gemini"), InlineKeyboardButton("♋ Cancer", callback_data="Cancer")],
            [InlineKeyboardButton("♌ Leo", callback_data="Leo"), InlineKeyboardButton("♍ Virgo", callback_data="Virgo")],
            [InlineKeyboardButton("♎ Libra", callback_data="Libra"), InlineKeyboardButton("♏ Scorpio", callback_data="Scorpio")],
            [InlineKeyboardButton("♐ Sagittarius", callback_data="Sagittarius"), InlineKeyboardButton("♑ Capricorn", callback_data="Capricorn")],
            [InlineKeyboardButton("♒ Aquarius", callback_data="Aquarius"), InlineKeyboardButton("♓ Pisces", callback_data="Pisces")]
        ]),
        parse_mode="Markdown"
    )

async def button(update, context):
    query = update.callback_query
    await query.answer()
    sign = query.data
    fortune = get_fortune(sign)
    await query.edit_message_text(
        f"🌟 *{sign}*\n\n{fortune}\n\n🦊 *FortuneFox* — Made for humans.\n\n🔁 Try another!",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Again", callback_data="restart")]])
    )

async def restart(update, context):
    if update.callback_query:
        await update.callback_query.answer()
    await start(update.callback_query or update, context)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(lambda u,c: restart(u,c) if u.callback_query.data=="restart" else button(u,c)))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()