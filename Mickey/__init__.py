import asyncio
import logging
import time

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import Client
from pyrogram.enums import ParseMode

import config

# -------------------- FIX EVENT LOOP (HEROKU + ABG) --------------------
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from Abg import patch  # noqa: E402  (DO NOT MOVE THIS UP)

# -------------------- LOAD ENV --------------------
load_dotenv()

# -------------------- LOGGING --------------------
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler()
    ],
    level=logging.INFO,
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger("MickeyBot")

boot = time.time()

# -------------------- DATABASE --------------------
mongo = MongoCli(config.MONGO_URL)
db = mongo.Anonymous

OWNER = config.OWNER_ID

# -------------------- BOT CLASS --------------------
class MickeyBot(Client):
    def __init__(self):
        super().__init__(
            name="MickeyBot",  # 🔥 REQUIRED
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            lang_code="en",
            in_memory=True,
            parse_mode=ParseMode.DEFAULT,
        )

    async def start(self):
        await super().start()

        self.id = self.me.id
        self.name = f"{self.me.first_name} {self.me.last_name or ''}".strip()
        self.username = self.me.username
        self.mention = self.me.mention

        LOGGER.info(f"🤖 Bot started as @{self.username}")

    async def stop(self):
        await super().stop()
        LOGGER.info("🛑 Bot stopped")


# -------------------- BOT INSTANCE --------------------
app = MickeyBot()
