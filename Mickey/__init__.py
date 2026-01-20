import logging
import time
import os

from Abg import patch
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import Client
from pyrogram.enums import ParseMode
from dotenv import load_dotenv

import config

# Load .env variables
load_dotenv()

# Logging setup
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
LOGGER = logging.getLogger(__name__)

boot = time.time()

# MongoDB
mongo = MongoCli(config.MONGO_URL)
db = mongo.Anonymous

# Owner
OWNER = config.OWNER_ID


class MickeyBot(Client):
    def __init__(self):
        super().__init__(
            name="MickeyBot",
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

        LOGGER.info(f"Logged in as @{self.username}")

    async def stop(self):
        await super().stop()
        LOGGER.info("Bot stopped")


# Bot instance
MickeyBot = MickeyBot()
