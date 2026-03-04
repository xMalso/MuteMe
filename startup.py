import os
# import shutil
import sys
import win32com.client
# import pystray
from micControl import logging

exe_name =  os.path.basename(sys.executable)
STARTUP_FOLDER = os.path.join(
    os.environ["APPDATA"],
    r"Microsoft\Windows\Start Menu\Programs\Startup"
)

def add_to_startup():
    exe_path = sys.executable
    shortcut_path = os.path.join(STARTUP_FOLDER, f"{exe_name}.lnk")

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)

    shortcut.TargetPath = exe_path
    shortcut.WorkingDirectory = os.path.dirname(exe_path)
    shortcut.save()

def remove_from_startup():
    startup_folder = os.path.join(
        os.environ["APPDATA"],
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )

    exe_name = os.path.basename(sys.executable)
    startup_file = os.path.join(startup_folder, f"{exe_name}.lnk")

    if os.path.exists(startup_file):
        os.remove(startup_file)
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
    shortcut_path = os.path.join(STARTUP_FOLDER, f"{exe_name}.lnk")
    return os.path.exists(shortcut_path)