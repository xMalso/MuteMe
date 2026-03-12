import sys
import threading
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtGui import QGuiApplication
from PIL import Image, ImageDraw
import pystray
import webbrowser
import ctypes

from startup import toggle_startup, is_in_startup
from micControl import logging
from settingsGUI import load_gui
import debugMode

for name in ["PIL", "PIL.Image", "PIL.PngImagePlugin"]:
    logging.getLogger(name).disabled = True

debug_mode = False
kernel32 = ctypes.windll.kernel32
CTRL_CLOSE_EVENT = 2
settings_window = None
icon = None


# --- Signal bridge (thread-safe Qt communication) ---
class TraySignals(QObject):
    open_settings_signal = Signal()
    quit_signal = Signal()


tray_signals = TraySignals()


def create_image():
    image = Image.new("RGB", (64, 64), color="black")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill="white")
    return image


def show_window():
    global settings_window
    if settings_window is None:
        logging.debug("Loading settings window...")
        screen = QGuiApplication.primaryScreen().availableGeometry()
        width = int(screen.width() * 0.8)
        height = int(screen.height() * 0.8)
        x = screen.x() + (screen.width() - width) // 2
        y = screen.y() + (screen.height() - height) // 2
        settings_window = load_gui()
        settings_window.setGeometry(x, y, width, height)
        # settings_window.setAttribute(Qt.WA_DeleteOnClose, False)
        # settings_window.destroyed.connect(reset_settings_window)
    else:
        logging.debug("Settings window already open. Bringing it to the front.")
    settings_window.showNormal()
    settings_window.raise_()


# def reset_settings_window():
#     global settings_window
#     settings_window = None


def open_settings(icon, item):
    tray_signals.open_settings_signal.emit()


def _do_quit():
    global icon
    icon.stop()
    app = QApplication.instance()
    if app:
        app.quit()


def quit_app(icon, item):
    tray_signals.quit_signal.emit()


def open_link(icon, item):
    webbrowser.open("https://paypal.me/MohamedAlsowmely")


def toggle_debug_mode(icon, item):
    global debug_mode
    if not debugMode.is_enabled():
        debugMode.enable()
        print("Debug mode enabled.")
        print("This console will output what the program is hearing.")
        print("You can see what audio is being detected versus what you are saying.")
        print(
            "Use this to determine relevant voice commands adjustments for your settings."
        )
        print(
            "DO NOT CLOSE USING THE X BUTTON, USE THE DEBUG MODE OPTION IN THE TRAY MENU TO CLOSE THIS CONSOLE. otherwise the program will end."
        )
        debug_mode = True
    else:
        debugMode.disable()
        debug_mode = False
    icon.update_menu()


tray_signals.open_settings_signal.connect(show_window)
tray_signals.quit_signal.connect(_do_quit)


def run_tray():
    global icon

    icon = pystray.Icon(
        "MuteMe",
        create_image(),
        "Mute Me",
        menu=pystray.Menu(
            pystray.MenuItem("Buy me a not coffee", open_link),
            pystray.MenuItem("Settings", open_settings),
            pystray.MenuItem(
                "Debug Mode",
                toggle_debug_mode,
                checked=lambda item: debugMode.is_enabled(),
            ),
            pystray.MenuItem(
                "Run on Startup",
                toggle_startup,
                checked=lambda item: is_in_startup(),
            ),
            pystray.MenuItem("Quit", quit_app),
        ),
    )
    threading.Thread(target=icon.run, daemon=True).start()


def set_debug_mode(mode):
    global debug_mode
    debug_mode = mode


def get_debug_mode():
    return debug_mode
