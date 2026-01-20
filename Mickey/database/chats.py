# Mickey/database/chats.py
from Mickey import db

# 🔹 Collections
groups_col = db.groups   # Group info / economy settings
config_col = db.config   # Global settings like economy lock

# =========================================================
# ✅ SERVED GROUPS HELPERS
# =========================================================

async def is_served_chat(chat_id: int) -> bool:
    """
    Check if a group/chat exists in DB
    """
    chat = await groups_col.find_one({"_id": chat_id})
    return bool(chat)


async def get_served_chats() -> list:
    """
    Get all served groups/chats
    """
    chats_list = []
    async for chat in groups_col.find({"_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def add_served_chat(chat_id: int, title: str = None):
    """
    Add a new chat/group to the database
    """
    if await is_served_chat(chat_id):
        return
    data = {"_id": chat_id, "name": title or "Unknown", "eco_disabled": False, "bonus_claimed": False}
    await groups_col.insert_one(data)


async def remove_served_chat(chat_id: int):
    """
    Remove a chat/group from the database
    """
    if not await is_served_chat(chat_id):
        return
    await groups_col.delete_one({"_id": chat_id})
