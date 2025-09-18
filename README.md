# Backup Bre

BackupBre does encrypted full-backups on your external storage. For Windows.

## Requirements

- Python
- Package python-dotenv
- VeraCrypt
- winotify

## Setup

1. Install all requirements.
2. Set up VeraCrypt Volume on external device. See VeraCrypt documentation.
3. Set up .env
    - SOURCE_DIRS: All directories you want to secure.
    - TARGET_DIR: Directory where to save your backups.
      Supposed to be inside your mounted VeraCrypt volume.
      Drive letter must be free on your device.
    - MAX_SNAPSHOTS: Max. amount of backup snapshots
    - VERACRYPT_PATH: Path to your VeraCrypt.exe
    - VOLUME_PATH: Path to your VeraCrypt volume file. Supposed to be on your external storage.
      DO NOT include the drive letter, as it may vary for each external device.
    - EXTERNAL_STORAGES: All labels of your external devices you want to use for your backup.
    - POLLING_INTERVAL: Defines time intervals (in seconds) in which the app is
      checking for external storages.
4. Start or autostart app.py. When your external storage is plugged in, BackupBre
   automatically starts and asks for your password you set up in step 2.
   After your backup is done you can unplug your external storage from your device.

## Example .env

SOURCE_DIRS='C:\Path\to\folder;C:\Path\to\other\folder2'

TARGET_DIR='X:\Backups'

MAX_SNAPSHOTS='5'

VERACRYPT_PATH='C:\Program Files\VeraCrypt\VeraCrypt.exe'

VOLUME_PATH='VeraCryptVolume\Backup.vc'

EXTERNAL_STORAGES='FlashDriveA;FlashDriveB'

POLLING_INTERVAL='5'

## Environment

Developed on Windows 11 with Python 3.13.

## Known issues

Issues with deleting read-only files and folders (e.g. /.git) in your backup. Fix coming soon!
