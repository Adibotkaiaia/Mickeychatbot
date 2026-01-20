import time
import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import OWNER_ID, ADMIN_IDS, DAY_SECONDS, REVIVE_SECONDS
from Mickey import MickeyBot
from Mickey.database.users import users_col
from Mickey.database.chats import groups_col, config_col

# =========================================================
# 🛍️ SHOP ITEMS DATA
# =========================================================
SHOP_ITEMS = {
    "rose": {"name": "Rose", "icon": "🌹", "price": 500},
    "chocolate": {"name": "Chocolate", "icon": "🍫", "price": 800},
    "ring": {"name": "Ring", "icon": "💍", "price": 2000},
    "teddy": {"name": "Teddy Bear", "icon": "🧸", "price": 1500},
    "pizza": {"name": "Pizza", "icon": "🍕", "price": 600},
    "surprise": {"name": "Surprise Box", "icon": "🎁", "price": 2500},
    "puppy": {"name": "Puppy", "icon": "🐶", "price": 3000},
    "cake": {"name": "Cake", "icon": "🎂", "price": 1000},
    "letter": {"name": "Love Letter", "icon": "💌", "price": 400},
    "cat": {"name": "Cat", "icon": "🐱", "price": 2500}
}

# =========================================================
# 🛠️ HELPER FUNCTIONS
# =========================================================

def is_admin(uid):
    return str(uid) == str(OWNER_ID) or uid in ADMIN_IDS

async def get_user(uid, name):
    uid = int(uid)
    user = users_col.find_one({"_id": uid})
    if not user:
        user = {
            "_id": uid,
            "name": name,
            "balance": 1000,
            "kills": 0,
            "status": "alive",
            "death_time": 0,
            "protection": 0,
            "last_daily": 0,
            "last_ubi": 0,
            "inventory": {}
        }
        users_col.insert_one(user)
    else:
        if user["name"] != name:
            users_col.update_one({"_id": uid}, {"$set": {"name": name}})

    # Auto daily income
    now = time.time()
    last_ubi = user.get("last_ubi", 0)
    if now - last_ubi > DAY_SECONDS:
        users_col.update_one(
            {"_id": uid},
            {"$inc": {"balance": 1000}, "$set": {"last_ubi": now}}
        )
        user["balance"] += 1000

    return user

def check_death(uid):
    uid = int(uid)
    user = users_col.find_one({"_id": uid})
    if not user: return False
    if user["status"] == "dead":
        if time.time() > user["death_time"] + REVIVE_SECONDS:
            users_col.update_one({"_id": uid}, {"$set": {"status": "alive", "death_time": 0}})
            return False
        return True
    return False

async def can_play(chat_id):
    cfg = config_col.find_one({"_id": "settings"})
    if cfg and cfg.get("locked", False):
        await MickeyBot.send_message(chat_id, "🔒 Global Economy is locked by Owner.")
        return False
    grp = groups_col.find_one({"_id": chat_id})
    if grp and grp.get("eco_disabled", False):
        await MickeyBot.send_message(chat_id, "🚫 Economy commands are disabled in this group.")
        return False
    return True

# =========================================================
# 👤 USER COMMANDS
# =========================================================

@MickeyBot.on_message(filters.private & filters.command("daily"))
async def daily(_, m: Message):
    if not await can_play(m.chat.id): return
    uid = m.from_user.id
    u = await get_user(uid, m.from_user.first_name)
    if time.time() - u["last_daily"] < DAY_SECONDS:
        rem = int(DAY_SECONDS - (time.time() - u["last_daily"]))
        hours, mins = rem // 3600, (rem % 3600) // 60
        return await m.reply(f"⏳ Come back in <b>{hours}h {mins}m</b>")
    users_col.update_one({"_id": uid}, {"$inc": {"balance": 1500}, "$set": {"last_daily": time.time()}})
    await m.reply("✅ You received: $1500 daily reward!")

@MickeyBot.on_message(filters.private & filters.command("bal"))
async def balance(_, m: Message):
    uid = m.reply_to_message.from_user.id if m.reply_to_message else m.from_user.id
    name = m.reply_to_message.from_user.first_name if m.reply_to_message else m.from_user.first_name
    u = await get_user(uid, name)
    rank = users_col.count_documents({"balance": {"$gt": u["balance"]}}) + 1
    status = "dead" if check_death(uid) else "alive"
    msg = f"👤 <b>Name:</b> {u['name']}\n💰 <b>Balance:</b> ${u['balance']}\n🏆 <b>Global Rank:</b> {rank}\n❤️ <b>Status:</b> {status}\n⚔️ <b>Kills:</b> {u['kills']}"
    await m.reply(msg)

@MickeyBot.on_message(filters.private & filters.command("shop"))
async def shop(_, m: Message):
    text = "🛒 <b>ITEM SHOP</b>\n\n"
    for k, v in SHOP_ITEMS.items():
        text += f"{v['icon']} <b>{v['name']}</b> — ${v['price']}\n"
    text += "\n🎁 Usage: /gift (reply) itemname"
    await m.reply(text)

# =========================================================
# 🫡 ADMIN COMMANDS (Owner)
# =========================================================

@MickeyBot.on_message(filters.private & filters.user(OWNER_ID) & filters.command("setbal"))
async def setbal(_, m: Message):
    if not m.reply_to_message: return await m.reply("⚠️ Reply to user.")
    try: amt = int(m.text.split()[1])
    except: return await m.reply("⚠️ Usage: /setbal <amount>")
    tid = m.reply_to_message.from_user.id
    await get_user(tid, m.reply_to_message.from_user.first_name)
    users_col.update_one({"_id": tid}, {"$set": {"balance": amt}})
    await m.reply(f"✅ Balance set to ${amt}.")

# =========================================================
# 👥 GROUP COMMANDS
# =========================================================

@MickeyBot.on_message(filters.group & filters.command("close"))
async def close_group(_, m: Message):
    member = await MickeyBot.get_chat_member(m.chat.id, m.from_user.id)
    if member.status not in ["administrator", "creator"] and not is_admin(m.from_user.id):
        return await m.reply("⚠️ Only admins can use this.")
    groups_col.update_one({"_id": m.chat.id}, {"$set": {"eco_disabled": True}}, upsert=True)
    await m.reply("✅ Economy commands disabled in this group.")

@MickeyBot.on_message(filters.group & filters.command("open"))
async def open_group(_, m: Message):
    member = await MickeyBot.get_chat_member(m.chat.id, m.from_user.id)
    if member.status not in ["administrator", "creator"] and not is_admin(m.from_user.id):
        return await m.reply("⚠️ Only admins can use this.")
    groups_col.update_one({"_id": m.chat.id}, {"$set": {"eco_disabled": False}}, upsert=True)
    await m.reply("✅ Economy commands enabled in this group.")
