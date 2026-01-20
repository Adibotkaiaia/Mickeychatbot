
# economy.py
from telebot import TeleBot, types
from datetime import datetime, timedelta

# ----------------------------
# Bot Instance
# ----------------------------
bot = TeleBot("YOUR_BOT_TOKEN_HERE")  # <-- Replace with your bot token

# ----------------------------
# In-Memory Users Database
# ----------------------------
users = {}  # user_id: {balance, kills, premium, protection, daily_claim}

# ----------------------------
# Helper Functions
# ----------------------------
def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "balance":0,
            "kills":0,
            "premium":False,
            "protection":None,
            "daily_claim":None
        }
    return users[user_id]

def add_balance(user_id, amount):
    user = get_user(user_id)
    user["balance"] += amount

def deduct_balance(user_id, amount):
    user = get_user(user_id)
    if user["balance"] >= amount:
        user["balance"] -= amount
        return True
    return False

def is_protected(user_id):
    user = get_user(user_id)
    if user["protection"] and user["protection"] > datetime.now():
        return True
    return False

# ----------------------------
# Commands
# ----------------------------

# /daily
@bot.message_handler(commands=['daily'])
def daily(message):
    user = get_user(message.from_user.id)
    now = datetime.now()
    reward = 2000 if user["premium"] else 1000

    if user["daily_claim"] and now - user["daily_claim"] < timedelta(hours=24):
        remaining = timedelta(hours=24) - (now - user["daily_claim"])
        bot.reply_to(message, f"Already claimed! Try after {remaining}")
        return

    user["daily_claim"] = now
    add_balance(message.from_user.id, reward)
    bot.reply_to(message, f"You received ${reward} daily reward!")

# /bal
@bot.message_handler(commands=['bal'])
def bal(message):
    user = get_user(message.from_user.id)
    prefix = "💓" if user["premium"] else "👤"
    bot.reply_to(message, f"{prefix} Your balance: ${user['balance']}")

# /pay - become premium
@bot.message_handler(commands=['pay'])
def pay(message):
    user = get_user(message.from_user.id)
    if user["premium"]:
        bot.reply_to(message, "Already premium 💓")
    else:
        cost = 5000
        if deduct_balance(message.from_user.id, cost):
            user["premium"] = True
            bot.reply_to(message, "Congrats! You are now a premium user 💓")
        else:
            bot.reply_to(message, f"You need ${cost} to become premium!")

# /give
@bot.message_handler(commands=['give'])
def give(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "Usage: /give <amount> (reply to user)")
            return
        amount = int(args[1])
        sender = get_user(message.from_user.id)

        if not message.reply_to_message:
            bot.reply_to(message, "Reply to a user to give money!")
            return

        receiver_id = message.reply_to_message.from_user.id
        receiver = get_user(receiver_id)

        fee_percent = 5 if sender["premium"] else 10
        fee = int(amount * fee_percent / 100)
        total = amount + fee

        if sender["balance"] < total:
            bot.reply_to(message, f"Not enough balance! You need ${total} including fee.")
            return

        deduct_balance(message.from_user.id, total)
        add_balance(receiver_id, amount)
        bot.reply_to(message, f"You gave ${amount} to {message.reply_to_message.from_user.first_name} (Fee: ${fee})")

    except Exception as e:
        bot.reply_to(message, "Error: " + str(e))

# /protect
@bot.message_handler(commands=['protect'])
def protect(message):
    args = message.text.split()
    user = get_user(message.from_user.id)
    if len(args) < 2:
        bot.reply_to(message, "Usage: /protect <1d|2d|3d>")
        return
    duration_map = {"1d":1, "2d":2, "3d":3}
    if args[1] not in duration_map:
        bot.reply_to(message, "Invalid duration! Choose 1d, 2d, 3d")
        return
    cost = 500 * duration_map[args[1]]
    if deduct_balance(message.from_user.id, cost):
        user["protection"] = datetime.now() + timedelta(days=duration_map[args[1]])
        bot.reply_to(message, f"Protection bought for {args[1]} ✅")
    else:
        bot.reply_to(message, f"Not enough balance! You need ${cost}")

# /rob
@bot.message_handler(commands=['rob'])
def rob(message):
    if not message.reply_to_message:
        bot.reply_to(message, "Reply to a user to rob them!")
        return
    sender = get_user(message.from_user.id)
    target = get_user(message.reply_to_message.from_user.id)

    if is_protected(message.reply_to_message.from_user.id):
        bot.reply_to(message, "Target is protected! ❌")
        return

    max_amount = 100000 if sender["premium"] else 10000
    stolen = min(max_amount, target["balance"])
    tax = 5 if sender["premium"] else 10
    stolen_after_tax = stolen - int(stolen * tax / 100)

    if stolen_after_tax <= 0:
        bot.reply_to(message, "Nothing to steal! 😅")
        return

    deduct_balance(message.reply_to_message.from_user.id, stolen)
    add_balance(message.from_user.id, stolen_after_tax)
    bot.reply_to(message, f"You robbed ${stolen_after_tax} from {message.reply_to_message.from_user.first_name} (Tax: {tax}%)")

# /kill
@bot.message_handler(commands=['kill'])
def kill(message):
    if not message.reply_to_message:
        bot.reply_to(message, "Reply to a user to kill them!")
        return
    sender = get_user(message.from_user.id)
    reward = 400 if sender["premium"] else 200
    add_balance(message.from_user.id, reward)
    sender["kills"] += 1
    bot.reply_to(message, f"You killed {message.reply_to_message.from_user.first_name} and earned ${reward}")

# /revive
@bot.message_handler(commands=['revive'])
def revive(message):
    if message.reply_to_message:
        bot.reply_to(message, f"You revived {message.reply_to_message.from_user.first_name} ✅")
    else:
        bot.reply_to(message, "You revived yourself ✅")

# /toprich
@bot.message_handler(commands=['toprich'])
def toprich(message):
    top_users = sorted(users.items(), key=lambda x: x[1]["balance"], reverse=True)
    text = "🏆 Top Rich Users:\n"
    for i, (uid, info) in enumerate(top_users[:10], 1):
        prefix = "💓" if info["premium"] else "👤"
        text += f"{i}. {prefix} User {uid} - ${info['balance']}\n"
    bot.reply_to(message, text)

# /topkill
@bot.message_handler(commands=['topkill'])
def topkill(message):
    top_users = sorted(users.items(), key=lambda x: x[1]["kills"], reverse=True)
    text = "⚔️ Top Killers:\n"
    for i, (uid, info) in enumerate(top_users[:10], 1):
        prefix = "💓" if info["premium"] else "👤"
        text += f"{i}. {prefix} User {uid} - {info['kills']} kills\n"
    bot.reply_to(message, text)

# /check (premium only)
@bot.message_handler(commands=['check'])
def check(message):
    user = get_user(message.from_user.id)
    if not user["premium"]:
        bot.reply_to(message, "Only premium users can use this command 💓")
        return
    if not message.reply_to_message:
        bot.reply_to(message, "Reply to a user to check protection")
        return
    target = get_user(message.reply_to_message.from_user.id)
    if is_protected(message.reply_to_message.from_user.id):
        bot.reply_to(message, f"{message.reply_to_message.from_user.first_name} is protected until {target['protection']}")
    else:
        bot.reply_to(message, f"{message.reply_to_message.from_user.first_name} is NOT protected ❌")

# ----------------------------
# Optional Inline Menu (Buttons)
# ----------------------------
@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Balance 💰", callback_data="bal"))
    markup.add(types.InlineKeyboardButton("Daily 🗓️", callback_data="daily"))
    markup.add(types.InlineKeyboardButton("Kill ⚔️", callback_data="kill"))
    markup.add(types.InlineKeyboardButton("Rob 💵", callback_data="rob"))
    bot.send_message(message.chat.id, "Choose option:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def button_callback(call):
    if call.data == "bal":
        bal(call.message)
    elif call.data == "daily":
        daily(call.message)
    elif call.data == "kill":
        kill(call.message)
    elif call.data == "rob":
        rob(call.message)
