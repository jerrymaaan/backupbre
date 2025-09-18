from watcherbre import watcherbre
from notifybre import notify
import traceback

try:
    # starts watcherbre main loop
    watcherbre()
except Exception as e:
    # notifies in case an error occurs
    error_msg = traceback.format_exc()
    notify('ERROR', f'{e}\nBackupBre has terminated')
    print(error_msg)  # to see traceback while developing or using in console
