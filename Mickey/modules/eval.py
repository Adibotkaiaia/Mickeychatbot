import os
import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)

from Mickey import OWNER, MickeyBot


# ---------- async exec ----------
async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message):"
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


# ---------- edit or reply ----------
async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


# ---------- EVAL COMMAND ----------
@MickeyBot.on_edited_message(
    filters.command("eval")
    & filters.user(OWNER)
    & ~filters.forwarded
    & ~filters.via_bot
)
@MickeyBot.on_message(
    filters.command("eval")
    & filters.user(OWNER)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def executor(client: Client, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(
            message, text="<b>ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴇxᴇᴄᴜᴛᴇ ?</b>"
        )

    cmd = message.text.split(" ", maxsplit=1)[1]
    t1 = time()

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = redirected_output = StringIO()
    sys.stderr = redirected_error = StringIO()

    exc = None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = exc or stderr or stdout or "Success"
    final_output = (
        f"<b>⥤ ʀᴇsᴜʟᴛ :</b>\n<pre language='python'>{evaluation}</pre>"
    )

    t2 = time()
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="⏳",
                    callback_data=f"runtime {round(t2 - t1, 3)} Seconds",
                ),
                InlineKeyboardButton(
                    text="🗑",
                    callback_data=f"forceclose abc|{message.from_user.id}",
                ),
            ]
        ]
    )

    if len(final_output) > 4096:
        with open("output.txt", "w+", encoding="utf8") as f:
            f.write(evaluation)

        await message.reply_document(
            document="output.txt",
            caption="<b>⥤ ʀᴇsᴜʟᴛ :</b>\nAttached File",
            reply_markup=keyboard,
            quote=False,
        )
        os.remove("output.txt")
        await message.delete()
    else:
        await edit_or_reply(
            message, text=final_output, reply_markup=keyboard
        )


# ---------- CALLBACK : RUNTIME ----------
@MickeyBot.on_callback_query(filters.regex(r"^runtime"))
async def runtime_func_cq(client: Client, cq: CallbackQuery):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


# ---------- CALLBACK : FORCE CLOSE ----------
@MickeyBot.on_callback_query(filters.regex(r"^forceclose"))
async def forceclose_command(client: Client, cq: CallbackQuery):
    callback_data = cq.data.strip()
    _, payload = callback_data.split(None, 1)
    _, user_id = payload.split("|")

    if cq.from_user.id != int(user_id):
        return await cq.answer(
            "» ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ.",
            show_alert=True,
        )

    await cq.message.delete()
    await cq.answer()


# ---------- SHELL COMMAND ----------
@MickeyBot.on_edited_message(
    filters.command("sh")
    & filters.user(OWNER)
    & ~filters.forwarded
    & ~filters.via_bot
)
@MickeyBot.on_message(
    filters.command("sh")
    & filters.user(OWNER)
    & ~filters.forwarded
    & ~filters.via_bot
)
async def shellrunner(client: Client, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(
            message, text="<b>ᴇxᴀᴍᴩʟᴇ :</b>\n/sh git pull"
        )

    text = message.text.split(None, 1)[1]
    shell = re.split(
        r""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text
    )

    try:
        process = subprocess.Popen(
            shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except Exception as err:
        return await edit_or_reply(
            message, text=f"<b>ERROR :</b>\n<pre>{err}</pre>"
        )

    output = process.stdout.read().decode("utf-8").strip()

    if not output:
        return await edit_or_reply(
            message, text="<b>OUTPUT :</b>\n<code>None</code>"
        )

    if len(output) > 4096:
        with open("output.txt", "w+") as f:
            f.write(output)
        await client.send_document(
            message.chat.id,
            "output.txt",
            reply_to_message_id=message.id,
            caption="<code>Output</code>",
        )
        os.remove("output.txt")
    else:
        await edit_or_reply(
            message, text=f"<b>OUTPUT :</b>\n<pre>{output}</pre>"
        )
