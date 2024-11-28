from get_config import get_backup_list, get_remote_root, get_selected_remote
from utils import eprint, get_home
from network import is_trusted_network
from os import path
import re
from rclone_python import rclone


def replace_home(input_path):
    home_dir = get_home()
    return re.sub(r"(\$HOME|~)", home_dir, input_path, count=1)


def main():
    if not rclone.is_installed:
        eprint("Rclone is not installed on your system", "ERR")

    clean_backup_paths = []
    backup_list = []
    non_existent_paths = []
    remote = get_selected_remote()
    remote_root = get_remote_root()
    remote_prefix = ""

    # Bail out if network is not trusted
    if not is_trusted_network():
        eprint("Connected network is not inside trusted networks", "ERR")

    # Check if backup_list exist and replace the ~ with $HOME
    if get_backup_list() is not None:
        for item in get_backup_list():
            if item.startswith("~"):
                clean_backup_paths.append(replace_home(item))
    else:
        eprint("No item found in backup list", "ERR")

    # Define the source dir inside the target remote
    if remote is not None:
        remote = remote + ":"

    if not remote in rclone.get_remotes():
        eprint("Selected remote is not in your remotes list", "ERR")
    else:
        remote_prefix = f"{remote}{remote_root}"

    print(remote_prefix)

    # Create the backup_list
    for item in clean_backup_paths:
        if path.exists(item):
            if path.isfile(item):
                backup_list.append(
                    {"type": "file", "source": item, "dest": path.dirname(item)}
                )
            elif path.isdir(item):
                backup_list.append({"type": "dir", "source": item, "dest": item})
        else:
            non_existent_paths.append(item)

    # Warn the user if there are invalid paths
    if non_existent_paths:
        eprint(f"Below paths doesn't exist:", "WARN")
        print(*non_existent_paths, sep="\n")

    print(backup_list)


if __name__ == "__main__":
    main()
