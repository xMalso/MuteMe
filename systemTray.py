import os
import subprocess
import sys
import time
from PIL import Image, ImageDraw
import pystray
import webbrowser

# from sympy import root
from startup import toggle_startup, is_in_startup
from micControl import logging

debug_mode = False
debug_process = None
DEBUG_INSTANCE = "--debug" in sys.argv

def create_image():
    # Simple black/white square icon
    image = Image.new("RGB", (64, 64), color="black")
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill="white")
    return image


def quit_app(icon, item):
    icon.stop()
    sys.exit(0)


def open_link(icon, item):
    webbrowser.open("https://paypal.me/malsoo")


def open_settings(icon, item):
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    settings_path = os.path.join(base_dir, "assets", "txt files", "settings.txt")
    subprocess.Popen(["notepad.exe", settings_path])

def toggle_debug_mode(icon, item):
    global debug_process, debug_mode

    if not debug_mode:
        # Start debug instance with console
        debug_process = subprocess.Popen(
            [sys.executable, "--debug"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        debug_mode = True
    else:
        # Stop debug instance
        if debug_process is not None:
            debug_process.terminate()
            debug_process = None
        debug_mode = False

    icon.update_menu()

def check_debug_process(icon):
    global debug_process, debug_mode
    while True:
        time.sleep(2)
        if debug_process is not None:
            if debug_process.poll() is not None:
                debug_process = None
                debug_mode = False
                icon.update_menu()
                logging.info("Debug process closed.")




def run_tray():
    icon = pystray.Icon(
        "MuteMe",
        create_image(),
        "Mute Me Controller",
        menu=pystray.Menu(
            pystray.MenuItem("Buy me a not coffee", open_link),
            pystray.MenuItem("Options", open_settings),
            pystray.MenuItem(
                "Debug Mode", toggle_debug_mode, checked=lambda item: debug_mode
            ),
            pystray.MenuItem(
                "Run on Startup",
                toggle_startup,
                checked=lambda item: is_in_startup(),
            ),
            pystray.MenuItem("Quit", quit_app),
        ),
    )
    icon.run()

def set_debug_process(process):
    global debug_process
    debug_process = process

def get_debug_process():
    # global debug_process
    return debug_process

def set_debug_mode(mode):
    global debug_mode
    debug_mode = mode

def get_debug_mode():
    # global debug_mode
    return debug_mode

# def minimise_to_tray():
#     root.withdraw()
