import glob
from os.path import basename, dirname, isfile

def __list_all_modules():
    files = glob.glob(dirname(__file__) + "/*.py")
    return [
        basename(f)[:-3]
        for f in files
        if isfile(f) and not f.endswith("__init__.py")
    ]

ALL_MODULES = __list_all_modules()
