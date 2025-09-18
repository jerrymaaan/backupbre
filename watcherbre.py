import psutil
import win32api  # pywin32 needed
import time
import win32file
import win32con

from backupbre import backupbre
from loadingbre import VOLUME_PATH, EXTERNAL_STORAGES, POLLING_INTERVAL
from notifybre import notify


def eject_storage(storage_letter):
    path = f'\\\\.\\{storage_letter}:'
    handle = win32file.CreateFile(
        path,
        win32con.GENERIC_READ,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
        None,
        win32con.OPEN_EXISTING,
        0,
        None
    )
    win32file.DeviceIoControl(handle, 0x2D4808, None, 0)  # noqa
    win32api.CloseHandle(handle)  # noqa
    # Chat-GPT: "In the C world, a handle is actually just an int (a pointer/value).
    # But pywin32 wraps it in its own PyHANDLE object."

    notify('WatcherBre', f'Ejected {storage_letter}:\\. External storage can be removed.')


def check_for_external_storages():
    # list all connected external storages here
    connected_storages = []

    for disk in psutil.disk_partitions(all=False):

        # tries to read volume from disk
        try:
            volume_info = win32api.GetVolumeInformation(disk.mountpoint)
            volume_letter = disk.mountpoint[0]
            volume_label = volume_info[0]
            if volume_label in EXTERNAL_STORAGES:
                # adds to connected_storages if volume is in list of desired EXTERNAL_STORAGES
                connected_storages.append({
                    'label': volume_label,
                    'letter': volume_letter,
                })
        except Exception as e:
            notify('WatcherBre', f'Error for {disk}. Exception: {e}', dev=True)
            continue

    # return all connected external storages where to save a backup
    return connected_storages


def watcherbre():
    # notify once that watcherbre is active
    notify('WatcherBre', 'Starting watch now!')

    while True:
        # look for connected storage to start backup
        connected_storages = check_for_external_storages()

        for storage in connected_storages:
            notify('WatcherBre', f'Starting backupbre for {storage['label']}')

            # start backup
            abs_vol_path = storage['letter'] + ':\\' + VOLUME_PATH
            backupbre(abs_vol_path)

            # finished backup
            notify('WatcherBre', f'Finished backupbre for {storage['label']}', dev=True)

            # eject after backup
            eject_storage(storage['letter'])

        time.sleep(int(POLLING_INTERVAL))
