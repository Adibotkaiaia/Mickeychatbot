from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

@Client.on_message(filters.command("mute") & filters.group)
async def mute(_, m):
    if not m.reply_to_message:
        return await m.reply_text("Reply to user")
    await m.chat.restrict_member(
        m.reply_to_message.from_user.id,
        ChatPermissions()
    )
    await m.reply_text("🔇 Muted")
