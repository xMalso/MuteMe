import sys
import threading
import time


from systemTray import run_tray#, check_debug_process
from voiceMicControl import start_listening
# from micControl import logging
# shutdown_event = threading.Event()

# DEBUG_INSTANCE = "--debug" in sys.argv

def listener_loop():
    while start_listening():
        pass
    # shutdown_event.set()

    # try:
    #     import systemTray
    #     if systemTray.icon:
    #         systemTray.icon.stop()
    # except:
    #     pass

if __name__ == "__main__":
    # if not DEBUG_INSTANCE:
        threading.Thread(target=listener_loop, daemon=True).start()
        # threading.Thread(target=check_debug_process, daemon=True).start()
        run_tray()
    # else:
    #     print("Debug mode enabled.")
    #     print("This console will output what the program is hearing." )
    #     print("You can see what audio is being detected versus what you are saying.")
    #     print("Use this to determine relevant voice commands adjustments for your settings.")
    #     while start_listening(True):
    #         pass