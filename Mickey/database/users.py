# Mickey/database/users.py
from config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient

# 🔹 MongoDB setup
mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo.Anonymous  # database name

# 🔹 Users collection
users_col = db.users


# =========================================================
# ✅ SERVED USERS HELPERS
# =========================================================

async def is_served_user(user_id: int) -> bool:
    """
    Check if the user already exists in served users collection
    """
    user = await users_col.find_one({"user_id": user_id})
    return bool(user)


async def get_served_users() -> list:
    """
    Get list of all served users
    """
    users_list = []
    async for user in users_col.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    """
    Add a new user to served users
    """
    if await is_served_user(user_id):
        return
    await users_col.insert_one({"user_id": user_id})
