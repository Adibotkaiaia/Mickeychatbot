from os import getenv
from dotenv import load_dotenv

load_dotenv()

# === REQUIRED ===
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
MONGO_URL = getenv("MONGO_URL")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")

# === OWNER ===
OWNER_ID = int(getenv("OWNER_ID"))
OWNER_USERNAME = getenv("OWNER_USERNAME", "I_ADI_I")

# === OPTIONAL ===
SUPPORT_GRP = getenv("SUPPORT_GRP", "VIP_SUPPORT_II")
UPDATE_CHNL = getenv("UPDATE_CHNL", "Il_vip_support_lI")

# === RANDOM START IMAGES ===
IMG = [
    "https://te.legra.ph/file/5bf629d10afd4af953585.jpg",
    "https://te.legra.ph/file/7a321b99fe99d9d8b5117.jpg",
    "https://te.legra.ph/file/c482a7e55b459ffe07502.jpg",
]

# === RANDOM STICKERS ===
STICKER = [
    "CAACAgQAAxkBAALRi2NZXUgjZCT775L5Nr0XrLbQ6XIpAAK_EQACpvFxHq2xh5JRVJNrKgQ",
    "CAACAgQAAxkBAALRjGNZXUs6YPggISBdtg4nXaU0vjNzAALqCwACbCIRU61ZQKi3F88DKgQ",
]

# === EMOJIS ===
EMOJIOS = ["💣", "💥", "🪄", "⚡", "👻", "🎩"]
