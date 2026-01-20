# Don't remove This Line From Here. Tg: @Dev_Arora_0981 | @DevArora0981
# Github :- Devarora-0981 | Devarora2604

import asyncio
import random

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, Message

from config import EMOJIOS, IMG, STICKER
from Mickey import MickeyBot
from Mickey.database.chats import add_served_chat
from Mickey.database.users import add_served_user
from Mickey.modules.helpers import (
    CLOSE_BTN,
    DEV_OP,
    HELP_BTN,
    HELP_BUTN,
    HELP_READ,
    HELP_START,
    SOURCE_READ,
    START,
)


# -----------------------------
# 🎮 All-in-One Bot Start Command
# -----------------------------
@MickeyBot.on_cmd(["start", "aistart"])
async def start(_, m: Message):
    if m.chat.type == ChatType.PRIVATE:
        # Random Emoji animation
        accha = await m.reply_text(text=random.choice(EMOJIOS))
        await asyncio.sleep(1.2)
        await accha.edit("__✨ Ding Dong! Booting up your All-in-One Bot... ✨__")
        await asyncio.sleep(0.2)
        await accha.edit("__🎮 Gaming | 💬 Chatting | 🎵 Music | 🥳 Fun loading...__")
        await asyncio.sleep(0.2)
        await accha.delete()

        # Fun Sticker
        umm = await m.reply_sticker(sticker=random.choice(STICKER))
        await asyncio.sleep(2)
        await umm.delete()

        # Bot Intro Photo + Caption
        bot_intro = f"""
🎉 **Welcome to {MickeyBot.name} - Your All-in-One Bot!** 🎉
━━━━━━━━━━━━━━
🎮 Gaming | 💬 Chatting | 🎵 Music | 🥳 Fun
💎 Earn coins, play games & chat with AI
✨ Enjoy stickers, memes, music & more!
━━━━━━━━━━━━━━
**Usage:** /chatbot [ON/OFF]
<b>Hit the buttons below for commands & help!</b>
"""
        await m.reply_photo(
            photo=random.choice(IMG),
            caption=bot_intro,
            reply_markup=InlineKeyboardMarkup(DEV_OP),
        )
        await add_served_user(m.from_user.id)

    else:
        # Group start message
        await m.reply_photo(
            photo=random.choice(IMG),
            caption="""
🎉 **Hello, Group!**
━━━━━━━━━━━━━━
🎮 Play games | 💬 Chat with AI | 🎵 Enjoy Music
💎 Check /economy for economy features
""",
            reply_markup=InlineKeyboardMarkup(HELP_START),
        )
        await add_served_chat(m.chat.id)


# -----------------------------
# ℹ️ Help Command
# -----------------------------
@MickeyBot.on_cmd("help")
async def help(client: MickeyBot, m: Message):
    if m.chat.type == ChatType.PRIVATE:
        hmm = await m.reply_photo(
            photo=random.choice(IMG),
            caption="""
📜 **Bot Help & Commands**
━━━━━━━━━━━━━━
🎮 /economy - Play economy games
💬 /chatbot [ON/OFF] - AI chatting
🎵 /music - Play music in groups
🎁 /shop - View items
💰 /bal - Check your balance
""",
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )
        await add_served_user(m.from_user.id)
    else:
        await m.reply_photo(
            photo=random.choice(IMG),
            caption="**Hey! PM me for full bot commands & AI chat!**",
            reply_markup=InlineKeyboardMarkup(HELP_BUTN),
        )
        await add_served_chat(m.chat.id)


# -----------------------------
# 🔗 Repo Command
# -----------------------------
@MickeyBot.on_cmd("repo")
async def repo(_, m: Message):
    await m.reply_text(
        text=SOURCE_READ,
        reply_markup=InlineKeyboardMarkup(CLOSE_BTN),
        disable_web_page_preview=True,
    )


# -----------------------------
# 👋 Welcome New Members
# -----------------------------
@MickeyBot.on_message(filters.new_chat_members)
async def welcome(_, m: Message):
    for member in m.new_chat_members:
        await m.reply_photo(
            photo=random.choice(IMG),
            caption=f"🎉 Welcome {member.mention}! 🎉\n\n🎮 Gaming | 💬 Chatting | 🎵 Music | 🥳 Fun awaits!",
        )
