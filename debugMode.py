import ctypes
# import os
import sys
import logging

kernel32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32

SW_HIDE = 0
SW_SHOW = 5

# CTRL_C_EVENT = 0
# CTRL_BREAK_EVENT = 1
# CTRL_CLOSE_EVENT = 2
# CTRL_LOGOFF_EVENT = 5
# CTRL_SHUTDOWN_EVENT = 6

# def _handler(event):
#     if event in (CTRL_C_EVENT, CTRL_BREAK_EVENT, CTRL_CLOSE_EVENT, CTRL_LOGOFF_EVENT, CTRL_SHUTDOWN_EVENT):
#         disable()
#         return True
#     return False

# _handler_ref = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint)(_handler)
# kernel32.SetConsoleCtrlHandler(_handler_ref, True)

_console_allocated = False
_debug_mode = False

def is_enabled():
    return _debug_mode

# def console_exists():
#     return kernel32.GetConsoleWindow() != 0

# def hide_console():
#     hwnd = kernel32.GetConsoleWindow()
#     if hwnd:
#         # Remove from taskbar + hide completely
#         user32.ShowWindow(hwnd, SW_HIDE)
#         # user32.SetWindowLongW(hwnd, -20,
#         #     user32.GetWindowLongW(hwnd, -20) & ~0x80)

def enable():
    global _debug_mode, _console_allocated
    if not _console_allocated:
        kernel32.AllocConsole()
        # user32.ShowWindow(kernel32.GetConsoleWindow(), SW_HIDE)
        sys.stdout = open("CONOUT$", "w", buffering=1)
        sys.stderr = open("CONOUT$", "w", buffering=1)
        _console_allocated = True
        logging.info("Debug mode enabled.")
    elif not _console_allocated:
        logging.warn("Debug mode already enabled.")
    hwnd = kernel32.GetConsoleWindow()
    if hwnd:
        user32.ShowWindow(hwnd, SW_SHOW)
    _debug_mode = True

def disable():
    global _debug_mode
    hwnd = kernel32.GetConsoleWindow()
    if _console_allocated:
        if hwnd:
            user32.ShowWindow(hwnd, SW_HIDE)
        # kernel32.FreeConsole()
        logging.info("Debug mode hidden.")
    else:
        logging.warn("Debug mode already hidden.")
    # sys.stdout = open(os.devnull, "w")
    # sys.stderr = open(os.devnull, "w")
    _debug_mode = False
