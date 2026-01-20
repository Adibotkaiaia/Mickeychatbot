from motor.motor_asyncio import AsyncIOMotorClient
import config

# =========================================================
# 🔹 DATABASE CONNECTION
# =========================================================
client = AsyncIOMotorClient(config.MONGO_URL)

# Main database (use ONE db everywhere)
db = client["MickeyDB"]

# =========================================================
# 🔹 COLLECTIONS (USED BY GAMING / ECONOMY)
# =========================================================
users_col = db["users"]        # economy users
groups_col = db["groups"]      # group settings
config_col = db["config"]      # global config / locks

# =========================================================
# 🔹 OLD SUPPORT (for callback.py & legacy code)
# =========================================================
# Some old modules expect `vick`
vick = db["vick"]

# =========================================================
# 🔹 EXPORTS
# =========================================================
__all__ = [
    "db",
    "users_col",
    "groups_col",
    "config_col",
    "vick",
]
