import glob
from os.path import basename, dirname, isfile

# ----------------------------
# Load all modules automatically
# ----------------------------
def __list_all_modules():
    mod_paths = glob.glob(dirname(__file__) + "/*.py")

    all_modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    # ai_reply ko last load karna (safe)
    if "ai_reply" in all_modules:
        all_modules.remove("ai_reply")
        all_modules.append("ai_reply")

    return sorted(all_modules)


ALL_MODULES = __list_all_modules()
__all__ = ALL_MODULES + ["ALL_MODULES"]

# ----------------------------
# Import bot instance
# ----------------------------
try:
    # Heroku / module run
    from .economy import bot
except ModuleNotFoundError:
    # Local / fallback
    from economy import bot


# ----------------------------
# Import feature modules
# (IMPORTANT: sirf import, polling nahi)
# ----------------------------
try:
    from . import gaming
    from . import group
    from . import ai_reply
except ModuleNotFoundError:
    import gaming
    import group
    import ai_reply


# ----------------------------
# Start Bot
# ----------------------------
if __name__ == "__main__":
    print("✅ Bot is running with Economy + Gaming + Group + AI")
    bot.infinity_polling(skip_pending=True)
