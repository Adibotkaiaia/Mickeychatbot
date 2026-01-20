import os
import google.generativeai as genai
from pyrogram import Client, filters

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

AI_ENABLED = set()

@Client.on_message(filters.command("chatbot"))
async def chatbot_toggle(_, m):
    if len(m.command) < 2:
        return await m.reply_text(
            "**Usage:** /chatbot on | off"
        )

    arg = m.command[1].lower()
    uid = m.from_user.id

    if arg == "on":
        AI_ENABLED.add(uid)
        await m.reply_text("🤖 AI Chatbot Enabled")
    elif arg == "off":
        AI_ENABLED.discard(uid)
        await m.reply_text("🚫 AI Chatbot Disabled")
    else:
        await m.reply_text("Use: /chatbot on | off")


# 🔥 FIXED HANDLER
@Client.on_message(filters.text)
async def ai_chat(_, m):
    uid = m.from_user.id

    if uid not in AI_ENABLED:
        return

    # command messages ignore
    if m.text.startswith("/"):
        return

    try:
        response = model.generate_content(m.text)
        await m.reply_text(response.text)
    except Exception:
        await m.reply_text("❌ AI error, try again later")
