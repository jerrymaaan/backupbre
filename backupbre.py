import os
import shutil
import datetime
import subprocess

from loadingbre import DRIVE_LETTER, VERACRYPT_PATH, TARGET_DIR, MAX_SNAPSHOTS, SOURCE_DIRS


def mount_volume(abs_volume_path):
    # Mount VeraCrypt volume with interactive password prompt
    print(f'Mounting VeraCrypt volume: {abs_volume_path} -> {DRIVE_LETTER}:\\')

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
    print(f'Dismounting {DRIVE_LETTER}:\\')

    cmd = [VERACRYPT_PATH, '/d', DRIVE_LETTER, '/q']
    subprocess.run(cmd)


def create_backup():
    # Create target folder with timestamp
    timestamp = datetime.datetime.now().strftime('Backup_%Y-%m-%d_%H-%M-%S')
    target_path = os.path.join(TARGET_DIR, timestamp)

    print(f'Create Backup in: {target_path}')
    os.makedirs(target_path, exist_ok=True)

    # Copy source folders
    for src in SOURCE_DIRS:
        if not os.path.exists(src):
            print(f'Skip {src}, not found.')
            continue

        folder_name = os.path.basename(src.rstrip('\\/'))
        dest = os.path.join(target_path, folder_name)

        print(f'Copies {src} -> {dest}')
        shutil.copytree(src, dest)

    print('✅ Backup successful!')


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
        print(f'🗑️ Deleting old backup: {path_to_delete}')
        shutil.rmtree(path_to_delete)


def backupbre(abs_volume_path):
    mount_volume(abs_volume_path)
    create_backup()
    cleanup_old_backups()
    dismount_volume()
