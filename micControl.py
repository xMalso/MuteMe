from time import time, sleep
import keyboard
import logging

logging.basicConfig(
    filename="voice_log.txt",
    filemode="w",
    level=logging.WARN,
    format="%(asctime)s - %(message)s",
)


def mute_mic(state, cooldown, crash_count, time_of_last_crash, hotkey):
    if not set_mic_mute(state, hotkey):
        logging.error(f'Failed to {"un" if not state else ""}mute microphone.')
        crash_count += 1
        time_of_last_crash = time()
    else:
        sleep(cooldown)
    return crash_count, time_of_last_crash


def set_mic_mute(state, hotkey):
    for i in range(3):
        try:
            keyboard.press_and_release(hotkey)
            logging.info("Unmuted" if state else "Muted")
            return True  # AKA success
        except Exception as e:
            logging.warning("Error controlling microphone: " + str(e))
            if i == 1:
                logging.warning(
                    "If this keeps happening, check microphone permissions and that a microphone is properly set up."
                )
            if i == 2:
                logging.warning("Cancelling attempt to control microphone.")
                logging.error(
                    "If this error persists, please send the error log to me on discord, discord ign: malso"
                )
    return False  # AKA fail
