import os
import os.path
from config import *
import re
from collections import deque
from datetime import datetime
import pyexcel

CACHED = False
dirs = deque()
result = []

def timestamp2datetime(ts):
    if isinstance(ts, (int, float, str)):
        try:
            ts = int(ts)
        except ValueError:
            raise

        if len(str(ts)) == 13:
            ts = ts // 1000
        if len(str(ts)) != 10:
            raise ValueError
    else:
        raise ValueError("")

    return datetime.fromtimestamp(ts)

def is_ignore(path):
    if path in IGNORE_PATHS_ABS or path in IGNORE_FILES_ABS:
        return True

    _, name = os.path.split(path)
    if os.path.isdir(path):
        if name in IGNORE_PATH_NAMES:
            return True
        if IGNORE_PATH_PATTERNS:
            for pattern in IGNORE_PATH_PATTERNS:
                if re.match(pattern, name) is not None:
                    return True
    
    if os.path.isfile(path):
        if name in IGNORE_FILE_NAMES:
            return True
        if IGNORE_FILENAME_PATTERNS:
            for pattern in IGNORE_FILENAME_PATTERNS:
                if re.match(pattern, name) is not None:
                    return True
        _, ext = os.path.split(name)
        if ext in IGNORE_FILE_EXTS:
            return True
        
def overview(path):
    global CACHED
    CACHED = True

def is_cached(path):
    if CACHED:
        return True
    return False

def load_cache(path):
    return True

def handle_path(path):
    global dirs, result
    for entry in os.scandir(path):
        if is_ignore(entry.path):
            continue

        if entry.is_dir():
            dirs.append(entry.path)
        
        if entry.is_file():
            _, ext = os.path.splitext(entry.name)
            ext = ext[1:] # 去掉点号
            # if ext not in DOC_EXTS:
            #     continue
            stats = entry.stat()
            result.append({
                'file_name': entry.name,
                'path': entry.path,
                'ext': ext,
                'last_access_time': timestamp2datetime(stats.st_atime),
                'create_time': timestamp2datetime(stats.st_ctime),
                'last_modify_time': timestamp2datetime(stats.st_mtime),
                'size': _hsize(stats.st_size)
                })

def _classify(path):
    if path.startswith('.'):
        path = os.path.abspath(path)

    handle_path(path)

    while dirs:
        path = dirs.pop()
        handle_path(path)

def _hsize(size):
    if size < 1024:
        return f"{size} bytes"
    elif size < 1024 * 1024:
        return f"{size//1024} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size/1024/1024:.0f} MB"
    else:
        return f"{size/1024/1024/1024:.2f} GB"

def classify(path):
    if is_cached(path):
        path_obj = load_cache(path)
    else:
        _classify(path)
        path_obj = result
    
    pyexcel.save_as(dest_file_name="classify.csv", records=path_obj)

if __name__ == "__main__":
    path = 'C:\\Users\\Molic\\Desktop'
    classify(path)
