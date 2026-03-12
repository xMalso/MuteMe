import threading
import sys
from PySide6.QtWidgets import QApplication

from systemTray import run_tray
from voiceMicControl import start_listening
from micControl import logging


def listener_loop():
    while start_listening():
        pass


if __name__ == "__main__":
    try:
        threading.Thread(target=listener_loop, daemon=True).start()
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        run_tray()
        app.exec()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
