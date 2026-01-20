from pyrogram import filters
from Mickey import MickeyBot
from Mickey.ai import get_ai_reply


@MickeyBot.on_message(filters.text & ~filters.bot)
async def ai_chat_handler(client, message):

    # private chat only (safe for cost)
    if message.chat.type != "private":
        return

    # long message control
    if len(message.text) > 600:
        await message.reply_text(
            "Itna lamba msg? Short me bol bhai 😵"
        )
        return

    try:
        reply = get_ai_reply(message.text)
        await message.reply_text(reply)
    except Exception:
        await message.reply_text(
            "Abe ruk 🤯 dimag thoda hang ho gaya"
        )
