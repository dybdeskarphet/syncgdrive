from pathlib import Path
import os
from utypes.enums import BackupLog, LogLevel, PathType
from utypes.models import PathItem

def log(message: str, logtype: LogLevel | BackupLog) -> None:
    color = "\033[32;1m"

    match logtype:
        case LogLevel.ERROR | BackupLog.ERR:
            # RED
            color = "\033[31;1m"
        case LogLevel.LOG:
            # BLUE
            color = "\033[34;1m"
        case LogLevel.INFO | BackupLog.OK:
            # GREEN
            color = "\033[32;1m"
        case LogLevel.WARN | BackupLog.WAIT:
            # YELLOW
            color = "\033[33;1m"

    full_msg = f"{color}{logtype.value}"
    if(isinstance(logtype, LogLevel)):
        full_msg = full_msg + ":"

    print(f"{full_msg}\033[0m {message}")

def organize_paths(paths: list[str], remote_name: str, root_dir: str) -> list[PathItem]:
    source_dest_array: list[PathItem] = []

    for path in paths:
        p = Path(path).expanduser()

        if p.is_dir():
            source_dest_array.append({
                "source": f"{p}",
                "dest": f"{remote_name}:{root_dir}{p}",
                "type": PathType.DIR.value
            })
        elif p.is_file():
            dest_dir = p.parent
            source_dest_array.append({
                "source": f"{p}",
                "dest": f"{remote_name}:{root_dir}{dest_dir}",
                "type": PathType.FILE.value
            })

    return source_dest_array

def collapseuser(path: str) -> str:
    """
    Opposite of path.expanduser()
    """
    home = os.path.expanduser("~")
    if path.startswith(home):
        return path.replace(home, "~", 1)
    return path
