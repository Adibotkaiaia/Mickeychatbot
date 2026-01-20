# Mickey/__init__.py

from motor.motor_asyncio import AsyncIOMotorClient

import config

# =========================================================
# 🔹 DATABASE CONNECTION
# =========================================================
client = AsyncIOMotorClient(config.MONGO_URL)
db = client["VickDb"]

# Collections
users_col = db["users"]      # Users database
groups_col = db["groups"]    # Groups database
config_col = db["config"]    # Global settings

# =========================================================
# 🔹 IMPORT ALL MODULE HELPERS
# =========================================================
from .chats import *
from .users import *
