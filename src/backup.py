import asyncio
from rclone_python import rclone
from get_config import get_remote_root, get_selected_remote
from utils import eprint
import subprocess

remote = get_selected_remote()
remote_root = get_remote_root()
remote_prefix = ""

# Define the source dir inside the target remote
if remote is not None:
    remote = remote + ":"

if not remote in rclone.get_remotes():
    eprint("Selected remote is not in your remotes list", "ERR")
else:
    remote_prefix = f"{remote}{remote_root}"


async def copy_command(source, dest):
    def run_copy():
        rclone.copy(
            source,
            f"{remote_prefix}{dest}",
            show_progress=False,
            args=[
                "--transfers 30",
                "--checkers 8",
                "--contimeout 60s",
                "--timeout 300s",
                "--retries 3",
                "--low-level-retries 10",
            ],
        )

    eprint(f"Copying '{source}' to '{remote_prefix}{dest}'")
    await asyncio.to_thread(run_copy)


async def sync_command(source, dest):
    def run_sync():
        rclone.sync(
            source,
            f"{remote_prefix}{dest}",
            show_progress=False,
            args=[
                "--transfers 30",
                "--checkers 8",
                "--contimeout 60s",
                "--timeout 300s",
                "--retries 3",
                "--low-level-retries 10",
            ],
        )

    eprint(f"Synchronizing '{source}' to '{remote_prefix}{dest}'")
    await asyncio.to_thread(run_sync)
