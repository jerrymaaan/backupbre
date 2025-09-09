# Backup Bre

Does encrypted full-backups on your external device.

## Requirements

- Python
- Package python-dotenv
- VeraCrypt

## Setup

1. Install all requirements.
2. Set up VeraCrypt Volume on external device.
3. Set up .env
    - SOURCE_DIRS: All directories you want to secure
    - TARGET_DIR: Directory where to save your backups.
      Supposed to be inside your mounted volume from VeraCrypt.
      Drive letter must be free on your device.
    - MAX_SNAPSHOTS: Max. amount of backup snapshots
    - VERACRYPT_PATH: Path to your VeraCrypt.exe
    - VOLUME_PATH: Path to your VeraCrypt volume file on your external device.

## Example .env

SOURCE_DIRS='C:\Path\to\folder;C:\Path\to\other\folder2'

TARGET_DIR='X:\Backups'

MAX_SNAPSHOTS='5'

VERACRYPT_PATH='C:\Program Files\VeraCrypt\VeraCrypt.exe'

VOLUME_PATH='D:\VeraCryptVolume\Backup.vc'

## Additional

Developed on Windows 11 with Python 3.13.
