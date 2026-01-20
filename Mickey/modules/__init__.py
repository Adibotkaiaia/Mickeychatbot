import glob
from os.path import basename, dirname, isfile

def __list_all_modules():
    """
    List all Python modules in this folder, excluding __init__.py
    """
    mod_paths = glob.glob(dirname(__file__) + "/*.py")

    all_modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    # Optional: always make sure ai_reply module loads last
    if "ai_reply" in all_modules:
        all_modules.remove("ai_reply")
        all_modules.append("ai_reply")

    return sorted(all_modules)


ALL_MODULES = __list_all_modules()
__all__ = ALL_MODULES + ["ALL_MODULES"]
