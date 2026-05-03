import os
import shutil
import datetime
import subprocess
import stat

from loadingbre import DRIVE_LETTER, VERACRYPT_PATH, TARGET_DIR, MAX_SNAPSHOTS, SOURCE_DIRS
from notifybre import notify


def mount_volume(abs_volume_path):
    # Mount VeraCrypt volume with interactive password prompt
    notify('BackupBre', f'Mounting VeraCrypt volume: {abs_volume_path} -> {DRIVE_LETTER}:\\', dev=True)

    cmd = [
        VERACRYPT_PATH,
        '/v', abs_volume_path,
        '/l', DRIVE_LETTER,
        '/q', '/a'  # quiet, automount
        # '/q', '/s', '/a'  # quiet, start minimized, automount (doesn't work correctly)
    ]
    result = subprocess.run(cmd)
    # subprocess.run() waits until process is finished
    # -> no synchronisation for following functions necessary

    if result.returncode != 0:
        raise RuntimeError('Failed to mount VeraCrypt volume')


def dismount_volume():
    # Dismount VeraCrypt volume
    notify('BackupBre', f'Dismounting {DRIVE_LETTER}:\\', dev=True)

    cmd = [VERACRYPT_PATH, '/d', DRIVE_LETTER, '/q']
    subprocess.run(cmd)


def create_backup():
    # Create target folder with timestamp
    timestamp = datetime.datetime.now().strftime('Backup_%Y-%m-%d_%H-%M-%S')
    target_path = os.path.join(TARGET_DIR, timestamp)

    notify('BackupBre', f'Create Backup in: {target_path}', dev=True)
    os.makedirs(target_path, exist_ok=True)

    # Copy source folders
    for src in SOURCE_DIRS:
        if not os.path.exists(src):
            notify('BackupBre', f'Skip {src}, not found.', dev=True)
            continue

        folder_name = os.path.basename(src.rstrip('\\/'))
        dest = os.path.join(target_path, folder_name)

        notify('BackupBre', f'Copies {src} -> {dest}', dev=True)
        # does not back up desktop.ini
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns("desktop.ini"))

    notify('BackupBre', 'Backup successful!', dev=True)


def cleanup_old_backups():
    # Find all backup folders in the target drive
    entries = [
        directory for directory in os.listdir(TARGET_DIR)
        if os.path.isdir(os.path.join(TARGET_DIR, directory))
           and directory.startswith('Backup_')
    ]

    # Sort entries (lexical sort works because of YYYY-MM-DD format)
    entries.sort()

    # If too many backups exist, delete oldest
    while len(entries) > MAX_SNAPSHOTS:
        oldest = entries.pop(0)
        path_to_delete = os.path.join(TARGET_DIR, oldest)
        notify('BackupBre', f'Deleting old backup: {path_to_delete}', dev=True)

        # deletes path and desktop.ini, without permission errors
        for root, dirs, files in os.walk(path_to_delete):
            for name in files:
                if name == "desktop.ini":
                    os.chmod(os.path.join(root, name), stat.S_IWRITE)

        os.chmod(path_to_delete, stat.S_IWRITE)
        shutil.rmtree(path_to_delete)


def backupbre(abs_volume_path):
    mount_volume(abs_volume_path)
    create_backup()
    cleanup_old_backups()
    dismount_volume()
