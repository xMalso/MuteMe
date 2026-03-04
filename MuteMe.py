import threading
import time


from systemTray import run_tray
from voiceMicControl import start_listening
from micControl import logging
from systemTray import check_debug_process

def listener_loop():
    while start_listening():
        pass


if __name__ == "__main__":
    threading.Thread(target=listener_loop, daemon=True).start()
    threading.Thread(target=check_debug_process, daemon=True).start()
    run_tray()
