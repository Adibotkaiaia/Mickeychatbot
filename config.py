from os import getenv
from dotenv import load_dotenv

load_dotenv()

# ==========================
# === REQUIRED CONFIGS ===
# ==========================
API_ID = int(getenv("API_ID", 21446101))
API_HASH = getenv("API_HASH", "0a2594b17b59f8928aa240825d898df1")
BOT_TOKEN = getenv("BOT_TOKEN", None)
MONGO_URL = getenv("MONGO_URL", None)
OPENAI_API_KEY = getenv("OPENAI_API_KEY", None)

# ==========================
# === OWNER & ADMINS ===
# ==========================
OWNER_ID = int(getenv("OWNER_ID", None ))  # <-- apna Telegram ID
OWNER_USERNAME = getenv("OWNER_USERNAME", "I_ADI_I")

# List of additional admins (Telegram IDs)
ADMIN_IDS = [8400280060]  # <-- apne team/admin IDs yahan dal sakte ho

# ==========================
# === OPTIONAL LINKS ===
# ==========================
SUPPORT_GRP = getenv("SUPPORT_GRP", "VIP_SUPPORT_II")
UPDATE_CHNL = getenv("UPDATE_CHNL", "Il_vip_support_lI")

# ==========================
# === ECONOMY SETTINGS ===
# ==========================
DAY_SECONDS = 86400        # Daily reward cooldown in seconds (1 day)
REVIVE_SECONDS = 3600      # Time before a dead user can revive (1 hour)

# ==========================
# === RANDOM START IMAGES ===
# ==========================
IMG = [
    "https://te.legra.ph/file/5bf629d10afd4af953585.jpg",
    #"https://te.legra.ph/file/7a321b99fe99d9d8b5117.jpg",
    #"https://te.legra.ph/file/c482a7e55b459ffe07502.jpg",
]

# ==========================
# === RANDOM STICKERS ===
# ==========================
STICKER = [
    "CAACAgQAAxkBAALRi2NZXUgjZCT775L5Nr0XrLbQ6XIpAAK_EQACpvFxHq2xh5JRVJNrKgQ",
    "CAACAgQAAxkBAALRjGNZXUs6YPggISBdtg4nXaU0vjNzAALqCwACbCIRU61ZQKi3F88DKgQ",
]

# ==========================
# === EMOJIS ===
# ==========================
EMOJIOS = ["💣", "💥", "🪄", "⚡", "👻", "🎩", "🎮", "🕹", "🎵", "🎉"]
