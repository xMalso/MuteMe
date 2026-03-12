import os
import sys
import win32com.client
from micControl import logging

STARTUP_FOLDER = os.path.join(
    os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup"
)


def get_exe_path():
    return sys.executable


def get_exe_name():
    return os.path.splitext(os.path.basename(get_exe_path()))[0]


def get_startup_shortcut_path():
    exe_name = get_exe_name()
    return os.path.join(STARTUP_FOLDER, f"{exe_name}.lnk")


def add_to_startup():
    exe_path = get_exe_path()

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(get_startup_shortcut_path())

    shortcut.TargetPath = exe_path
    shortcut.WorkingDirectory = os.path.dirname(exe_path)
    shortcut.save()


def remove_from_startup():
    if is_in_startup():
        os.remove(get_startup_shortcut_path())
        logging.info("Removed from startup.")
    else:
        logging.warn("Startup entry not found.")


def toggle_startup(icon):
    if is_in_startup():
        remove_from_startup()
        logging.info("Removed from startup")
    else:
        add_to_startup()
        logging.info("Added to startup")
    icon.update_menu()


def is_in_startup():
    return os.path.exists(get_startup_shortcut_path())
