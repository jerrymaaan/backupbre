import psutil
import win32api  # pywin32 needed
import time
import win32file
import win32con

from backupbre import backupbre
from loadingbre import VOLUME_PATH, EXTERNAL_STORAGES, POLLING_INTERVAL


def eject_storage(storage_letter):
    # eject a removable drive
    print(f'Ejecting {storage_letter}:\\ now')

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
    # Chat-GPT: "In der C-Welt ist ein Handle tatsächlich ein int (ein Zeiger/Wert),
    # aber pywin32 packt es in ein eigenes PyHANDLE-Objekt."


def check_for_external_storages():
    connected_storages = []

    for disk in psutil.disk_partitions(all=False):

        # tries to read volume from disk
        try:
            volume_info = win32api.GetVolumeInformation(disk.mountpoint)
            volume_letter = disk.mountpoint[0]
            volume_label = volume_info[0]
            if volume_label in EXTERNAL_STORAGES:
                # adds to list if volume is desired
                connected_storages.append({
                    'label': volume_label,
                    'letter': volume_letter,
                })
        except Exception as e:
            print(f'Error for {disk}. Exception: {e}')
            continue

    # return all connected external storages
    return connected_storages


def watcherbre():
    while True:
        # look for connected storage to start backup
        connected_storages = check_for_external_storages()

        for storage in connected_storages:
            print(f'Starting backupbre for {storage['label']}')

            # start backup
            abs_vol_path = storage['letter'] + ':\\' + VOLUME_PATH
            backupbre(abs_vol_path)

            # finished backup
            print(f'Finished backupbre for {storage['label']}')

            # eject after backup
            eject_storage(storage['letter'])

        time.sleep(int(POLLING_INTERVAL))


if __name__ == '__main__':
    watcherbre()
