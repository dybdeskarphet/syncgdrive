from backup import copy_command, sync_command
import backup
from get_config import (
    get_backup_list,
    get_sync_list,
)
from utils import eprint, get_home
from network import is_trusted_network
from os import path
import re
from rclone_python import rclone
import notify2
import asyncio


def replace_home(input_path):
    home_dir = get_home()
    return re.sub(r"(\$HOME|~)", home_dir, input_path, count=1)


def process_rclone_array(array, list_name="the"):
    home_expanded_array = []
    processed_array = []
    non_existent_paths = []
    is_empty = False

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

    if not processed_array:
        is_empty = True
        eprint(f"{list_name.capitalize()} list is empty", "WARN")

    return {
        "processed_array": processed_array,
        "non_existent_paths": non_existent_paths,
        "is_empty": is_empty,
    }


async def backup_and_sync_concurrently(backup_processed_array, sync_processed_array):
    tasks = []

    for item in backup_processed_array:
        tasks.append(copy_command(item["source"], item["dest"]))

    for item in sync_processed_array:
        tasks.append(sync_command(item["source"], item["dest"]))

    await asyncio.gather(*tasks)


def main():
    if not rclone.is_installed:
        eprint("Rclone is not installed on your system", "ERR")

    backup_list = process_rclone_array(get_backup_list(), "backup")
    sync_list = process_rclone_array(get_sync_list(), "sync")
    non_existent_paths = (
        backup_list["non_existent_paths"] + sync_list["non_existent_paths"]
    )
    notify2.init("syncgdrive")

    # Bail out if network is not trusted
    if not is_trusted_network():
        eprint("Connected network is not inside trusted networks", "ERR")

    # Warn the user if there are invalid paths
    if non_existent_paths:
        non_existent_string = "\n".join(non_existent_paths)
        print(end="\n")
        eprint(f"Below paths doesn't exist:", "WARN")
        print(non_existent_string)
        print(end="\n")
        non_existent_notify = notify2.Notification(
            "syncgdrive: Below paths doesn't exist",
            f"{non_existent_string}",
            "folder-sync",
        )
        non_existent_notify.show()

    if backup_list["is_empty"] and sync_list["is_empty"]:
        eprint("No backup or sync item found", "ERR")

    asyncio.run(
        backup_and_sync_concurrently(
            backup_list["processed_array"], sync_list["processed_array"]
        )
    )


if __name__ == "__main__":
    main()
