from telebot import types
from datetime import timedelta
from .economy import bot


# ---------- Helper ----------
def is_admin(chat_id, user_id):
    admins = bot.get_chat_administrators(chat_id)
    return any(admin.user.id == user_id for admin in admins)


# ---------- BAN ----------
@bot.message_handler(commands=["ban"])
def ban_user(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "❌ Reply to a user to ban")

    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ Admin only")

    user_id = message.reply_to_message.from_user.id
    bot.ban_chat_member(message.chat.id, user_id)
    bot.reply_to(message, "🚫 User banned successfully")


# ---------- KICK ----------
@bot.message_handler(commands=["kick"])
def kick_user(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "❌ Reply to a user to kick")

    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ Admin only")

    user_id = message.reply_to_message.from_user.id
    bot.kick_chat_member(message.chat.id, user_id)
    bot.unban_chat_member(message.chat.id, user_id)
    bot.reply_to(message, "👢 User kicked")


# ---------- MUTE ----------
@bot.message_handler(commands=["mute"])
def mute_user(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "❌ Reply to a user")

    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ Admin only")

    try:
        minutes = int(message.text.split()[1])
    except:
        return bot.reply_to(message, "Usage: /mute <minutes>")

    until = timedelta(minutes=minutes)
    bot.restrict_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
        until_date=until,
        permissions=types.ChatPermissions(can_send_messages=False)
    )
    bot.reply_to(message, f"🔇 Muted for {minutes} minutes")


# ---------- UNMUTE ----------
@bot.message_handler(commands=["unmute"])
def unmute_user(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "❌ Reply to a user")

    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ Admin only")

    bot.restrict_chat_member(
        message.chat.id,
        message.reply_to_message.from_user.id,
        permissions=types.ChatPermissions(can_send_messages=True)
    )
    bot.reply_to(message, "🔊 User unmuted")


# ---------- PURGE ----------
@bot.message_handler(commands=["purge"])
def purge(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ Admin only")

    count = 10
    if len(message.text.split()) > 1:
        count = int(message.text.split()[1])

    msg_id = message.message_id
    for i in range(count):
        try:
            bot.delete_message(message.chat.id, msg_id - i)
        except:
            pass


# ---------- PIN ----------
@bot.message_handler(commands=["pin"])
def pin(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "❌ Reply to a message")

    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ Admin only")

    bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
    bot.reply_to(message, "📌 Message pinned")


# ---------- TAG ALL ----------
@bot.message_handler(commands=["tagall"])
def tagall(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ Admin only")

    members = bot.get_chat_administrators(message.chat.id)
    text = "📢 Attention everyone!\n\n"

    for admin in members:
        if admin.user.username:
            text += f"@{admin.user.username} "
        else:
            text += f"{admin.user.first_name} "

    bot.send_message(message.chat.id, text)
