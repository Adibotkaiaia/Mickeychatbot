from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, Message
import random
from config import MONGO_URL
from Mickey import MickeyBot

# Single async MongoDB client
mongo = AsyncIOMotorClient(MONGO_URL)
chatai = mongo["Word"]["WordDb"]
vickdb = mongo["VickDb"]["Vick"]

@MickeyBot.on_message(
    (filters.text | filters.sticker | filters.group) & ~filters.private & ~filters.bot, group=4
)
async def chatbot_text(client: Client, message: Message):
    try:
        if message.text and message.text[0] in "!/@#?":
            return
    except Exception:
        pass

    is_vick = await vickdb.find_one({"chat_id": message.chat.id})
    if is_vick:
        return

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    K = []
    cursor = chatai.find({"word": message.text})
    async for x in cursor:
        K.append(x["text"])
    if K:
        hey = random.choice(K)
        is_text = await chatai.find_one({"text": hey})
        if is_text["check"] == "sticker":
            await message.reply_sticker(hey)
        else:
            await message.reply_text(hey)
