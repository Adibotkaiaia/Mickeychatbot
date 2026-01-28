import asyncio
import importlib
from pyrogram import idle

from Mickey import LOGGER, MickeyBot
from Mickey.modules import ALL_MODULES


async def main():
    await MickeyBot.start()

    # load all modules (handlers register honge)
    for module in ALL_MODULES:
        importlib.import_module(f"Mickey.modules.{module}")

    LOGGER.info(f"@{MickeyBot.username} Started.")
    await idle()

    LOGGER.info("Stopping Mickey Bot...")


if __name__ == "__main__":
    asyncio.run(main())   # 👈 FIX HERE
