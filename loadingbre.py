import os
from dotenv import load_dotenv

load_dotenv()  # load .env file

SOURCE_DIRS = os.getenv('SOURCE_DIRS').split(';')
TARGET_DIR = os.getenv('TARGET_DIR')
DRIVE_LETTER = TARGET_DIR[0]
MAX_SNAPSHOTS = int(os.getenv('MAX_SNAPSHOTS', '5'))  # default 5 if missing
VERACRYPT_PATH = os.getenv('VERACRYPT_PATH')
ABS_VOLUME_PATH = os.getenv('ABS_VOLUME_PATH')
EXTERNAL_STORAGES = os.getenv('EXTERNAL_STORAGES').split(';')
VOLUME_PATH = os.getenv('VOLUME_PATH')
POLLING_INTERVAL = os.getenv('POLLING_INTERVAL')
