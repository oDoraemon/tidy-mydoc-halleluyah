IGNORE_PATHS_ABS = [] # 完整路径
IGNORE_PATH_NAMES = [] # 某个文件名
IGNORE_PATH_PATTERNS = ["^\."]

IGNORE_FILES_ABS = [] # 完整路径的文件名
IGNORE_FILE_NAMES = [] # 某个特定文件名
IGNORE_FILENAME_PATTERNS = [] # 正则表达式的文件名
IGNORE_FILE_EXTS = [] # 文件类型

# ROOT = '.'
DOC_TYPES = {
    'doc': ['doc', 'docx'],
    'pdf': ['pdf'],
    'xls': ['xlsx', 'xls', 'csv'],
    'xmind': ['xmind'],
    'pic': ['png', 'jpg', 'jpeg', 'gif'],
    'video': ['mp4', 'avi', 'mkv'],
    'exe': ['exe']
}

DOC_EXTS = [ext for k, v in DOC_TYPES.items() for ext in v]