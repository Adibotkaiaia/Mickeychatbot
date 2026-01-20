import os
import google.generativeai as genai
from pyrogram import Client, filters

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

AI_CHATS = set()


@Client.on_message(filters.command("chatbot"))
async def chatbot_toggle(_, m):
    if len(m.command) < 2:
        return await m.reply_text("Use: /chatbot on | off")

    if m.command[1].lower() == "on":
        AI_CHATS.add(m.chat.id)
        await m.reply_text("🤖 AI Chat Enabled")
    else:
        AI_CHATS.discard(m.chat.id)
        await m.reply_text("🚫 AI Chat Disabled")


@Client.on_message(filters.text & ~filters.regex("^/"))
async def gemini_reply(_, m):
    if m.chat.id not in AI_CHATS:
        return

    try:
        r = model.generate_content(m.text)
        await m.reply_text(r.text)
    except Exception as e:
        await m.reply_text("❌ AI Error")
