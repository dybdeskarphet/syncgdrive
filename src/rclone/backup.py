import asyncio
from asyncio.tasks import Task
import shlex
from shared import sync_status
from utypes.enums import BackupLog, BackupStatus, CommandType, LogLevel
from utypes.models import PathItem
from utils import collapseuser, log

async def backup_command(rclone_command: list[str], source: str, dest: str, path_type: str, command_type: CommandType, verbose: bool = False):
    cmd = rclone_command + [source, dest]
    operation_name = command_type.value.capitalize() + "ing"

    log(f"{operation_name} {collapseuser(source)}", BackupLog.WAIT)
    process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    process_id = await sync_status.add_operation(source, dest, path_type, BackupStatus.IN_PROGRESS)

    stdout, stderr = await process.communicate()
    stdout = stdout.decode(errors="ignore").strip()
    stderr = stderr.decode(errors="ignore").strip()

    collapsed_source = collapseuser(source)
    match process.returncode:
        case 0:
            log(f"Backed up successfully: {collapsed_source}", BackupLog.OK)
        case 1:
            log(f"Back up operation failed: {collapsed_source}", BackupLog.ERR)
        case _:
            log(f"Back up operation failed with {process.returncode} exit code: {collapsed_source}", BackupLog.ERR)

    await sync_status.delete_operation(process_id)

    if verbose:
        if stderr: 
            log(f"{stderr}", LogLevel.WARN)
        if stdout:
            log(f"{stdout}", LogLevel.LOG)

async def backup(paths: list[PathItem], command_type: CommandType, rclone_args: list[str], semaphore: asyncio.Semaphore, verbose: bool = False):
    cmd = ["rclone", command_type.value]

    for arg in rclone_args:
        parts = shlex.split(arg)
        cmd += parts

    tasks: list[Task[None]] = []

    for path in paths:
        source, dest, path_type = path["source"], path["dest"], path["type"]

        # I have to do this because python doesn't have anon coroutines
        async def backup_task(source: str = source, dest: str = dest, path_type: str=path_type):
            async with semaphore:
                await backup_command(cmd, source, dest, path_type, command_type, verbose)

        task = asyncio.create_task(backup_task())
        tasks.append(task)

    _tasks_result = await asyncio.gather(*tasks)
