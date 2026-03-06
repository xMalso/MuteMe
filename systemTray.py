import os
import subprocess
import sys
import time
from PIL import Image, ImageDraw
import pystray
import webbrowser
import ctypes
# from sympy import root
from startup import toggle_startup, is_in_startup
from micControl import logging
import debugMode
# from voiceMicControl import start_listening

for name in ["PIL", "PIL.Image", "PIL.PngImagePlugin"]:
    logging.getLogger(name).disabled = True


debug_mode = False
# debug_process = None
# DEBUG_INSTANCE = "--debug" in sys.argv
kernel32 = ctypes.windll.kernel32
CTRL_CLOSE_EVENT = 2

# def console_exists():
#     return ctypes.windll.kernel32.GetConsoleWindow() != 0
 
# def enable_console():
#     if not console_exists():
#         ctypes.windll.kernel32.AllocConsole()
#         sys.stdout = open("CONOUT$", "w", buffering=1)
#         sys.stderr = open("CONOUT$", "w", buffering=1)
#         logging.info("Debug mode enabled.")
#         return True
#     else:
#         logging.warn("Debug mode already enabled.")
#         return False

# def disable_console():
#     if console_exists():
#         ctypes.windll.kernel32.FreeConsole()
#         logging.info("Debug mode disabled.")
#         return True
#     else:
#         logging.warn("Debug mode already disabled.")
#         return False

# def console_handler(event):
#     if event == CTRL_CLOSE_EVENT:
#         # Just hide the console instead of terminating app
#         disable_console()
#         global debug_mode
#         debug_mode = False
#         return True  # Prevent default termination
#     return False

# handler = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint)(console_handler)
# kernel32.SetConsoleCtrlHandler(handler, True)

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
    webbrowser.open("https://paypal.me/xmalso")


def open_settings(icon, item):
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    settings_path = os.path.join(base_dir, "assets", "txt files", "settings.txt")
    subprocess.Popen(["notepad.exe", settings_path])

def toggle_debug_mode(icon, item):
    global debug_mode#,  debug_process
    # print(f"debug mode: {debug_mode}")
    if not debugMode.is_enabled():
        # Start debug instance with console
        # if getattr(sys, "frozen", False):
        #     # Running from EXE
        #     main_exe = sys.executable

        #     debug_process = subprocess.Popen(
        #         [main_exe, "--debug"],
        #         creationflags=subprocess.CREATE_NEW_CONSOLE
        #     )
        debugMode.enable()
        print("Debug mode enabled.")
        print("This console will output what the program is hearing." )
        print("You can see what audio is being detected versus what you are saying.")
        print("Use this to determine relevant voice commands adjustments for your settings.")
        debug_mode = True
        
    else:
        debugMode.disable()
        debug_mode = False

    icon.update_menu()

# def check_debug_process():
#     global debug_mode#, debug_process
#     while True:
#         time.sleep(2)
#         if debug_mode:
#             if not console_exists():
#                 logging.info("Debug console closed (possibly by user).")
#             # if debug_process.poll() is not None:
#                 # debug_process = None
#             debug_mode = False
#             icon.update_menu()



def run_tray():
    global icon
    icon = pystray.Icon(
        "MuteMe",
        create_image(),
        "Mute Me",
        menu=pystray.Menu(
            pystray.MenuItem("Buy me a not coffee", open_link),
            pystray.MenuItem("Options", open_settings),
            pystray.MenuItem(
                "Debug Mode", toggle_debug_mode, checked=lambda item: debugMode.is_enabled()
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

# def set_debug_process(process):
#     global debug_process
#     debug_process = process

# def get_debug_process():
    # global debug_process
    # return debug_process

def set_debug_mode(mode):
    global debug_mode
    debug_mode = mode

def get_debug_mode():
    # global debug_mode
    return debug_mode

# def minimise_to_tray():
#     root.withdraw()

# if __name__ == "__main__" and DEBUG_INSTANCE:
#     print("Debug mode enabled.")
#     print("This console will output what the program is hearing." )
#     print("You can see what audio is being detected versus what you are saying.")
#     print("Use this to determine relevant voice commands adjustments for your settings.")
#     while start_listening(True):
#         pass