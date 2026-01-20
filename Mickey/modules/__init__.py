import glob
from os.path import basename, dirname, isfile

# ----------------------------
# Load all modules automatically
# ----------------------------
def __list_all_modules():
    mod_paths = glob.glob(dirname(__file__) + "/*.py")

    modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f)
        and f.endswith(".py")
        and not f.endswith("__init__.py")
    ]

    # ai_reply ko last load karna (safe)
    if "ai_reply" in modules:
        modules.remove("ai_reply")
        modules.append("ai_reply")

    return modules


ALL_MODULES = __list_all_modules()
