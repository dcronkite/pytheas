import ZODB
from ZODB.FileStorage import FileStorage

__factory = None


def global_init(path):
    global __factory
    if not __factory:
        __factory = ZODB.DB(FileStorage(path))


def get_root(key=None):
    global __factory
    root = __factory.open().root()
    if key:
        if key in root:
            root[key] = {}  # always use a dict?
            return root[key]
    return root
