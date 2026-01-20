from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

# ----------------------------
# In-Memory Database
# ----------------------------
users = {}  # user_id: data


def get_user(uid: int):
    if uid not in users:
        users[uid] = {
            "balance": 0,
            "kills": 0,
            "premium": False,
            "protection": None,
            "daily_claim": None
        }
    return users[uid]


def is_protected(uid: int):
    user = get_user(uid)
    return user["protection"] and user["protection"] > datetime.now()


# ----------------------------
# /daily
# ----------------------------
@Client.on_message(filters.command("daily"))
async def daily(_, message):
    user = get_user(message.from_user.id)
    now = datetime.now()
    reward = 2000 if user["premium"] else 1000

    if user["daily_claim"] and now - user["daily_claim"] < timedelta(hours=24):
        await message.reply_text("⏳ Daily already claimed!")
        return

    user["daily_claim"] = now
    user["balance"] += reward
    await message.reply_text(f"✅ You received **${reward}** daily reward!")


# ----------------------------
# /bal
# ----------------------------
@Client.on_message(filters.command("bal"))
async def bal(_, message):
    user = get_user(message.from_user.id)
    prefix = "💓" if user["premium"] else "👤"
    await message.reply_text(
        f"{prefix} **Balance:** ${user['balance']}"
    )


# ----------------------------
# /pay
# ----------------------------
@Client.on_message(filters.command("pay"))
async def pay(_, message):
    user = get_user(message.from_user.id)
    cost = 5000

    if user["premium"]:
        await message.reply_text("💓 You are already premium!")
        return

    if user["balance"] < cost:
        await message.reply_text(f"❌ You need ${cost} to buy premium.")
        return

    user["balance"] -= cost
    user["premium"] = True
    await message.reply_text("🎉 Congrats! You are now **Premium 💓**")


# ----------------------------
# /give
# ----------------------------
@Client.on_message(filters.command("give"))
async def give(_, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to give money!")

    args = message.text.split()
    if len(args) < 2:
        return await message.reply_text("Usage: `/give amount`", quote=True)

    amount = int(args[1])
    sender = get_user(message.from_user.id)
    receiver = get_user(message.reply_to_message.from_user.id)

    tax = 5 if sender["premium"] else 10
    fee = int(amount * tax / 100)
    total = amount + fee

    if sender["balance"] < total:
        return await message.reply_text("❌ Not enough balance!")

    sender["balance"] -= total
    receiver["balance"] += amount

    await message.reply_text(
        f"💸 Gave **${amount}** (Fee: ${fee})"
    )


# ----------------------------
# /protect
# ----------------------------
@Client.on_message(filters.command("protect"))
async def protect(_, message):
    args = message.text.split()
    if len(args) < 2:
        return await message.reply_text("Usage: /protect 1d|2d|3d")

    days_map = {"1d": 1, "2d": 2, "3d": 3}
    if args[1] not in days_map:
        return await message.reply_text("Choose: 1d / 2d / 3d")

    days = days_map[args[1]]
    cost = 500 * days
    user = get_user(message.from_user.id)

    if user["balance"] < cost:
        return await message.reply_text("❌ Not enough balance!")

    user["balance"] -= cost
    user["protection"] = datetime.now() + timedelta(days=days)
    await message.reply_text(f"🛡 Protection active for {days} days")


# ----------------------------
# /rob
# ----------------------------
@Client.on_message(filters.command("rob"))
async def rob(_, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to rob!")

    sender = get_user(message.from_user.id)
    target_id = message.reply_to_message.from_user.id
    target = get_user(target_id)

    if is_protected(target_id):
        return await message.reply_text("🛡 Target is protected!")

    max_amt = 100000 if sender["premium"] else 10000
    stolen = min(max_amt, target["balance"])

    if stolen <= 0:
        return await message.reply_text("😅 Nothing to steal!")

    tax = 5 if sender["premium"] else 10
    final_amt = stolen - int(stolen * tax / 100)

    target["balance"] -= stolen
    sender["balance"] += final_amt

    await message.reply_text(
        f"💵 Robbed **${final_amt}** (Tax {tax}%)"
    )


# ----------------------------
# /kill
# ----------------------------
@Client.on_message(filters.command("kill"))
async def kill(_, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a user to kill!")

    user = get_user(message.from_user.id)
    reward = 400 if user["premium"] else 200

    user["balance"] += reward
    user["kills"] += 1

    await message.reply_text(
        f"⚔️ You killed and earned **${reward}**"
    )


# ----------------------------
# /toprich
# ----------------------------
@Client.on_message(filters.command("toprich"))
async def toprich(_, message):
    data = sorted(users.items(), key=lambda x: x[1]["balance"], reverse=True)[:10]
    text = "🏆 **Top Rich Users**\n\n"

    for i, (_, u) in enumerate(data, 1):
        text += f"{i}. ${u['balance']}\n"

    await message.reply_text(text)


# ----------------------------
# /menu (BUTTONS)
# ----------------------------
@Client.on_message(filters.command("menu"))
async def menu(_, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Balance", callback_data="eco_bal")],
        [InlineKeyboardButton("🗓 Daily", callback_data="eco_daily")],
        [InlineKeyboardButton("⚔️ Kill", callback_data="eco_kill")],
        [InlineKeyboardButton("💵 Rob", callback_data="eco_rob")]
    ])
    await message.reply_text("📊 **Economy Menu**", reply_markup=buttons)


@Client.on_callback_query(filters.regex("^eco_"))
async def eco_buttons(_, query):
    if query.data == "eco_bal":
        await bal(_, query.message)
    elif query.data == "eco_daily":
        await daily(_, query.message)
    else:
        await query.answer("Reply required for this action!", show_alert=True)
