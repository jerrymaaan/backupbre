from winotify import Notification, audio


def notify(bre, msg, dev=False):
    # windows notification
    if not dev:
        toast = Notification(app_id='BackupBre',
                             title=f'{bre} says:',
                             msg=msg,
                             duration='short')
        toast.set_audio(audio.Default, loop=False)
        toast.show()

    # print for console
    print(f'[{bre}]: {msg}')
