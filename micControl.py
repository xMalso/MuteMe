from time import time, sleep
import keyboard
import logging
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# from comtypes import CLSCTX_ALL
# from ctypes import POINTER, cast

# def get_default_microphone():
#     devices = AudioUtilities.GetMicrophone()
#     interface = devices.Activate(
#         IAudioEndpointVolume._iid_,
#         CLSCTX_ALL,
#         None
#     )
#     return cast(interface, POINTER(IAudioEndpointVolume))

logging.basicConfig(
    filename="voice_log.txt",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s"
)

def mute_mic(state, cooldown,  crash_count, time_of_last_crash, keystroke):
    if not set_mic_mute(state, keystroke):
        logging.error(f'Failed to {"un" if not state else ""}mute microphone.')
        crash_count += 1
        time_of_last_crash = time()
    else:
        sleep(cooldown)
    return crash_count, time_of_last_crash

def set_mic_mute(state, keystroke):
    for i in range(3):
        try:
            # mic = get_default_microphone()
            # mic.SetMute(state, None)

            keyboard.press_and_release(keystroke)
            logging.info("Unmuted" if state else "Muted")
            # Audio cue to indicate mic state change
            # frequency = 440 if state else 880
            return True # AKA success
        except Exception as e:
            logging.warning("Error controlling microphone: " + str(e))
            if i == 1:
                logging.warning("If this keeps happening, check microphone permissions and that a microphone is properly set up.")
            if i == 2:
                logging.warning("Cancelling attempt to control microphone.")
                logging.error("If this error persists, please send the error log to me on discord, discord ign: malso")
    return False # AKA fail

