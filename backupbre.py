import os
import shutil
import datetime
from dotenv import load_dotenv
import subprocess

load_dotenv()  # Load .env file

SOURCE_DIRS = os.getenv('SOURCE_DIRS', '').split(';')
TARGET_DIR = os.getenv('TARGET_DIR')
MAX_SNAPSHOTS = int(os.getenv('MAX_SNAPSHOTS', '5'))  # default 5 if missing
VERACRYPT_PATH = os.getenv('VERACRYPT_PATH')
VOLUME_PATH = os.getenv('VOLUME_PATH')
DRIVE_LETTER = TARGET_DIR[0]


def mount_volume():
    # Mount VeraCrypt volume with interactive password prompt
    print(f'Mounting VeraCrypt volume: {VOLUME_PATH} -> {DRIVE_LETTER}:')

    cmd = [
        VERACRYPT_PATH,
        '/v', VOLUME_PATH,
        '/l', DRIVE_LETTER,
        # '/q', '/s', '/a'  # quiet, start minimized, automount
        '/q', '/a'  # quiet, automount
    ]
    result = subprocess.run(cmd)
    # subprocess.run() waits until process is finished
    # -> no synchronisation for following functions necessary

    if result.returncode != 0:
        raise RuntimeError('Failed to mount VeraCrypt volume')


def dismount_volume():
    # Dismount VeraCrypt volume
    print(f'Dismounting {DRIVE_LETTER}:')

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


if __name__ == '__main__':
    mount_volume()
    create_backup()
    cleanup_old_backups()
    dismount_volume()
