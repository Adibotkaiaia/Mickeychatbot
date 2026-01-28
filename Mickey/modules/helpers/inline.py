from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import SUPPORT_GRP, UPDATE_CHNL
from Mickey import OWNER, MickeyBot

# -----------------------------
# Helper functions to get buttons at runtime
# -----------------------------
def get_dev_buttons():
    return [
        [
            InlineKeyboardButton(text="🥀 ᴏᴡɴᴇʀ 🥀", url=f"https://t.me/{OWNER}"),
            InlineKeyboardButton(text="✨ ꜱᴜᴘᴘᴏʀᴛ ✨", url=f"https://t.me/{SUPPORT_GRP}"),
        ],
        [
            InlineKeyboardButton(
                text="🧸 ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ 🧸",
                url=f"https://t.me/{MickeyBot.username}?startgroup=true"
            ),
        ],
        [
            InlineKeyboardButton(text="🚀 ʜᴇʟᴘ & ᴄᴍᴅs 🚀", callback_data="HELP"),
        ],
        [
            InlineKeyboardButton(text="❄️ VIP NETWORK ❄️", callback_data="VIP NETWORK"),
            InlineKeyboardButton(text="☁️ ᴀʙᴏᴜᴛ ☁️", callback_data="ABOUT"),
        ],
    ]


def get_png_buttons():
    return [
        [
            InlineKeyboardButton(
                text="🧸 ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ 🧸",
                url=f"https://t.me/{MickeyBot.username}?startgroup=true"
            ),
        ],
        [
            InlineKeyboardButton(text="✨ ᴄʟᴏsᴇ ✨", callback_data="CLOSE"),
        ],
    ]


def get_help_buttons():
    return [
        [
            InlineKeyboardButton(text="🚀 ʜᴇʟᴘ 🚀", callback_data="HELP"),
            InlineKeyboardButton(text="🐳 ᴄʟᴏsᴇ 🐳", callback_data="CLOSE"),
        ]
    ]


def get_help_butn():
    return [
        [
            InlineKeyboardButton(
                text="🚀 ʜᴇʟᴘ 🚀",
                url=f"https://t.me/{MickeyBot.username}?start=help"
            ),
            InlineKeyboardButton(text="🐳 ᴄʟᴏsᴇ 🐳", callback_data="CLOSE"),
        ]
    ]


# Other static buttons (no runtime required)
BACK = [[InlineKeyboardButton(text="✨ ʙᴀᴄᴋ ✨", callback_data="BACK")]]
CLOSE_BTN = [[InlineKeyboardButton(text="❄️ ᴄʟᴏsᴇ ❄️", callback_data="CLOSE")]]
CHATBOT_ON = [[
    InlineKeyboardButton(text="ᴇɴᴀʙʟᴇ", callback_data="addchat"),
    InlineKeyboardButton(text="ᴅɪsᴀʙʟᴇ", callback_data="rmchat"),
]]
MUSIC_BACK_BTN = [[InlineKeyboardButton(text="sᴏᴏɴ", callback_data="soon")]]
CHATBOT_BACK = [[
    InlineKeyboardButton(text="✨ ʙᴀᴄᴋ ✨", callback_data="CHATBOT_BACK"),
    InlineKeyboardButton(text="❄️ ᴄʟᴏsᴇ ❄️", callback_data="CLOSE"),
]]
ABOUT_BTN = [
    [
        InlineKeyboardButton(text="🎄 sᴜᴘᴘᴏʀᴛ 🎄", url=f"https://t.me/{SUPPORT_GRP}"),
        InlineKeyboardButton(text="🚀 ʜᴇʟᴘ 🚀", callback_data="HELP"),
    ],
    [
        InlineKeyboardButton(text="🍾 ᴏᴡɴᴇʀ 🍾", url=f"https://t.me/{OWNER}"),
        InlineKeyboardButton(text="❄️ sᴏᴜʀᴄᴇ ❄️", callback_data="SOURCE"),
    ],
    [
        InlineKeyboardButton(text="🐳 ᴜᴘᴅᴀᴛᴇs 🐳", url=f"https://t.me/{UPDATE_CHNL}"),
        InlineKeyboardButton(text="✨ ʙᴀᴄᴋ ✨", callback_data="BACK"),
    ],
]
