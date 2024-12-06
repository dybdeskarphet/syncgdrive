from rclone_python import rclone
from get_config import get_selected_remote
from utils import eprint


def copy_command(source, dest):
    # TODO:
    # 1. Check rclone
    # 2. Get remote_dir from get_config
    # 2. Check if soruce is file or folder
    # 3. If file, use base dir as dest. If folder use itself.
    # 4. If files and folders are only home folder, dest dir starts from home folder
    # 5. If there are files and folders from root dir except HOME, dest dir starts from root

    rclone.copy(
        source,
        dest,
        show_progress=True,
        args=[
            "--transfers 30",
            "--checkers 8",
            "--contimeout 60s",
            "--timeout 300s",
            "--retries 3",
            "--low-level-retries 10",
        ],
    )


def sync_command(source, dest):
    rclone.sync(
        source,
        dest,
        show_progress=True,
        args=[
            "--transfers 30",
            "--checkers 8",
            "--contimeout 60s",
            "--timeout 300s",
            "--retries 3",
            "--low-level-retries 10",
        ],
    )
