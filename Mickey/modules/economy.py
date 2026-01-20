from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

users = {}

def get_user(uid):
    if uid not in users:
        users[uid] = {
            "balance": 0,
            "kills": 0,
            "premium": False,
            "protection": None,
            "daily": None
        }
    return users[uid]

def is_protected(uid):
    u = get_user(uid)
    return u["protection"] and u["protection"] > datetime.now()

@Client.on_message(filters.command("daily"))
async def daily(_, m):
    u = get_user(m.from_user.id)
    if u["daily"] and datetime.now() - u["daily"] < timedelta(hours=24):
        return await m.reply_text("⏳ Already claimed")
    u["daily"] = datetime.now()
    reward = 2000 if u["premium"] else 1000
    u["balance"] += reward
    await m.reply_text(f"✅ ${reward} added")

@Client.on_message(filters.command("bal"))
async def bal(_, m):
    u = get_user(m.from_user.id)
    e = "💓" if u["premium"] else "👤"
    await m.reply_text(f"{e} Balance: ${u['balance']}")

@Client.on_message(filters.command("rob"))
async def rob(_, m):
    if not m.reply_to_message:
        return await m.reply_text("Reply to user")
    s = get_user(m.from_user.id)
    t_id = m.reply_to_message.from_user.id
    t = get_user(t_id)
    if is_protected(t_id):
        return await m.reply_text("🛡 Protected")
    max_amt = 100000 if s["premium"] else 10000
    stolen = min(max_amt, t["balance"])
    if stolen <= 0:
        return await m.reply_text("😅 Nothing")
    tax = 5 if s["premium"] else 10
    final = stolen - int(stolen * tax / 100)
    t["balance"] -= stolen
    s["balance"] += final
    await m.reply_text(f"💵 Robbed ${final}")

@Client.on_message(filters.command("kill"))
async def kill(_, m):
    if not m.reply_to_message:
        return await m.reply_text("Reply to user")
    u = get_user(m.from_user.id)
    reward = 400 if u["premium"] else 200
    u["balance"] += reward
    u["kills"] += 1
    await m.reply_text(f"⚔️ Killed +${reward}")

@Client.on_message(filters.command("menu"))
async def menu(_, m):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Balance", callback_data="eco_bal")],
        [InlineKeyboardButton("🗓 Daily", callback_data="eco_daily")]
    ])
    await m.reply_text("📊 Economy", reply_markup=kb)

@Client.on_callback_query(filters.regex("^eco_"))
async def eco_cb(_, q):
    if q.data == "eco_bal":
        await bal(_, q.message)
    elif q.data == "eco_daily":
        await daily(_, q.message)
