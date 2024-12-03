from backup import copy_command, sync_command
from get_config import (
    get_backup_list,
    get_remote_root,
    get_selected_remote,
    get_sync_list,
)
from utils import eprint, get_home
from network import is_trusted_network
from os import path
import re
from rclone_python import rclone
import notify2


def replace_home(input_path):
    home_dir = get_home()
    return re.sub(r"(\$HOME|~)", home_dir, input_path, count=1)


def process_rclone_array(array, list_name="the"):
    home_expanded_array = []
    processed_array = []
    non_existent_paths = []

    if array is not None:
        for item in array:
            if item.startswith("~"):
                home_expanded_array.append(replace_home(item))
    else:
        eprint("No item found in backup list", "ERR")

    for item in home_expanded_array:
        if path.exists(item):
            if path.isfile(item):
                processed_array.append(
                    {"type": "file", "source": item, "dest": path.dirname(item)}
                )
            elif path.isdir(item):
                processed_array.append({"type": "dir", "source": item, "dest": item})
        else:
            non_existent_paths.append(item)

    return {
        "processed_array": processed_array,
        "non_existent_paths": non_existent_paths,
    }


def main():
    if not rclone.is_installed:
        eprint("Rclone is not installed on your system", "ERR")

    backup_list = process_rclone_array(get_backup_list(), "backup")
    sync_list = process_rclone_array(get_sync_list(), "sync")
    remote = get_selected_remote()
    remote_root = get_remote_root()
    remote_prefix = ""
    non_existent_paths = (
        backup_list["non_existent_paths"] + sync_list["non_existent_paths"]
    )
    notify2.init("syncgdrive")

    # Bail out if network is not trusted
    if not is_trusted_network():
        eprint("Connected network is not inside trusted networks", "ERR")

    # Define the source dir inside the target remote
    if remote is not None:
        remote = remote + ":"

    if not remote in rclone.get_remotes():
        eprint("Selected remote is not in your remotes list", "ERR")
    else:
        remote_prefix = f"{remote}{remote_root}"

    # Warn the user if there are invalid paths
    if non_existent_paths:
        non_existent_string = "\n".join(non_existent_paths)
        eprint(f"Below paths doesn't exist:", "WARN")
        print(non_existent_string)
        print(end="\n")
        non_existent_notify = notify2.Notification(
            "syncgdrive: Below paths doesn't exist",
            f"{non_existent_string}",
            "folder-sync",
        )
        non_existent_notify.show()

    for item in backup_list["processed_array"]:
        copy_command(item["source"], f"{remote_prefix}{item["dest"]}")

    for item in sync_list["processed_array"]:
        sync_command(item["source"], f"{remote_prefix}{item["dest"]}")


if __name__ == "__main__":
    main()
