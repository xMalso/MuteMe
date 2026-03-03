from datetime import datetime
import queue
import logging
# import time
from time import time, sleep
# import os
# import json
import sounddevice as sd

# from vosk import Model, KaldiRecognizer
# import webrtcvad

# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# from comtypes import CLSCTX_ALL
# from ctypes import POINTER, cast

from micControl import mute_mic
from settingsLoader import load_settings, get_settings_mtime, get_last_settings_update
from speechRecognition import create_audio_callback, process_speech_data
from vadDetection import create_voice_detected

settings = load_settings()
settings_path = "settings.txt"
last_settings_update = get_last_settings_update()

logging.basicConfig(
    filename="voice_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(message)s"
)

q = queue.Queue()
audio_callback = create_audio_callback(q)

voice_detected = create_voice_detected(settings["vad_aggressiveness"])
crash_count = 0

def start_listening():
    global crash_count, settings, last_settings_update, voice_detected
    prev_state = True
    time_of_last_crash = time()
    warning_sent = False
    prev_text = ""

    logging.info("Listening...")
    try:
        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=audio_callback
        ):

            while True:
                # logging.debug(time())
                try:
                    if time() - time_of_last_crash > settings["crash_timer_limit"]:
                        crash_count = 0
                    if get_settings_mtime() > last_settings_update + 0.2:
                        logging.info("Settings file changed, reloading settings...")
                        settings = load_settings()
                        voice_detected = create_voice_detected(settings["vad_aggressiveness"])
                        last_settings_update = get_last_settings_update()
                    data = q.get(timeout=5)
                    if not voice_detected(data):
                        continue
                    new_text = process_speech_data(data)
                    if not new_text or new_text == "":
                        continue
                    text = prev_text + " " + new_text
                    prev_text = new_text

                    logging.debug("Heard:", text)

                    if settings["hey_required"] and "hey" not in text:
                        continue
                    if any(cmd in text for cmd in settings["unmute_commands"]):
                        if prev_state == False:
                            crash_count, time_of_last_crash = mute_mic(True, settings["command_cooldown"], crash_count, time_of_last_crash, settings["mic_toggle_key"])
                            prev_state = True
                            prev_text = ""
                    elif any(cmd in text for cmd in settings["mute_commands"]):
                        if prev_state == True:
                            crash_count, time_of_last_crash = mute_mic(False, settings["command_cooldown"], crash_count, time_of_last_crash, settings["mic_toggle_key"])
                            prev_state = False
                            prev_text = ""
                except queue.Empty:
                    if not warning_sent:
                        logging.info(f"No audio input detected. for 5 seconds. This warning will only appear once per load, timestamp: {datetime.now().strftime('%A %H:%M:%S')}")
                        warning_sent = True
                    pass
                except KeyboardInterrupt:
                    if settings["unmute_on_exit"] and prev_state == False:
                        mute_mic(True, 0, crash_count, time_of_last_crash, settings["mic_toggle_key"])
                        logging.info("Unmuted microphone before exit.")
                    logging.info("Exiting...")
                    break
                except Exception as e:
                    crash_count += 1
                    time_of_last_crash = time()
                    logging.warning("Error:", e)
                    if crash_count < settings["crash_limit"]:
                        logging.info(f"Attempting again in {crash_count * 3} seconds...")
                        sleep(crash_count * 3)
                    else:
                        logging.error("Too many errors, please send the error log to me on discord, discord ign: malso") 
                        break
    except Exception as e:
        crash_count += 1
        logging.warning("Audio stream error:", e)
        if crash_count < settings["crash_limit"]:
            logging.info("Restarting listening loop...")
            sleep(2)
            return True
        logging.error("Too many errors, please send the error log to me on discord, discord ign: malso") 
        return False

if __name__ == "__main__":
    while start_listening():
        pass
