import ctypes
import sys
import logging

kernel32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32

SW_HIDE = 0
SW_SHOW = 5

_console_allocated = False
_debug_mode = False


def is_enabled():
    return _debug_mode


def enable():
    global _debug_mode, _console_allocated
    if not _console_allocated:
        kernel32.AllocConsole()
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
        logging.info("Debug mode hidden.")
    else:
        logging.warn("Debug mode already hidden.")
    _debug_mode = False
