import os
import json
from micControl import logging

settings_path = "assets/txt files/settings.txt"
json_path = "assets/txt files/settings.json"

settings = {
    "hey_required": True,
    "unmute_on_exit": True,
    "double_toggle": False,
    "crash_timer_limit": 5 * 60,
    "crash_limit": 5,
    "command_cooldown": 0.5,
    "vad_aggressiveness": 0,
    "mute_commands": set(),
    "unmute_commands": set(),
    "mute_hotkey": "ctrl+f12",
}


def load_settings():
    global last_settings_update, section
    section = None
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                data["unmute_commands"] = set(data.get("unmute_commands", []))
                data["mute_commands"] = set(data.get("mute_commands", []))
                logging.info("Settings loaded from JSON.")
                return data
        except Exception as e:
            logging.error(f"Failed to load settings from JSON: {e}")
            logging.info("Falling back to text settings file.")

    if os.path.exists(settings_path):
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip().lower()

                    if line.startswith("hey required"):
                        settings["hey_required"] = "true" in line
                        section = None
                    elif line.startswith("unmute on exit"):
                        settings["unmute_on_exit"] = "true" in line
                        section = None
                    elif line.startswith("disable double toggle"):
                        settings["double_toggle"] = "true" in line
                        section = None
                    elif line.startswith("crash timer limit"):
                        val = line.split("=")[1].strip()
                        settings["crash_timer_limit"] = int(val)
                        section = None
                    elif line.startswith("crash limit"):
                        val = line.split("=")[1].strip()
                        settings["crash_limit"] = int(val)
                        section = None
                    elif line.startswith("command cooldown"):
                        val = line.split("=")[1].strip()
                        settings["command_cooldown"] = float(val)
                        section = None
                    elif line.startswith("vad aggressiveness"):
                        val = line.split("=")[1].strip()
                        settings["vad_aggressiveness"] = int(val)
                        section = None
                    elif line.startswith("mic toggle key"):
                        val = line.split("=")[1].strip()
                        settings["mute_hotkey"] = val
                        section = None
                    elif line.startswith("unmute commands"):
                        section = "unmute"
                    elif line.startswith("mute commands"):
                        section = "mute"

                    if section != None and "=" not in line:
                        fillCommands(line)
            logging.info("Settings loaded from text file.")
            try:
                save_settings_to_file(settings)
                logging.info("Settings saved to JSON after loading from text file.")
                last_settings_update = os.path.getmtime(json_path)
            except Exception as e:
                logging.error(f"Failed to save settings to JSON: {e}")
            return settings
        except Exception as e:
            logging.error(f"Failed to load settings from text file: {e}")
            logging.info("Using default settings.")
            return settings
    logging.warn("No settings or json file found. Using default settings.")
    settings["unmute_commands"] = {"mike on"}
    settings["mute_commands"] = {"mike off", "mike of"}
    return settings


def save_settings_to_file(settings_dict):
    dump_data = settings_dict.copy()
    dump_data["unmute_commands"] = list(dump_data["unmute_commands"])
    dump_data["mute_commands"] = list(dump_data["mute_commands"])
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dump_data, f, indent=4)
    # with open(settings_path, "w", encoding="utf-8") as f:
    #     f.write(f"hey required = {settings_dict['hey_required']}\n")
    #     f.write(f"unmute on exit = {settings_dict['unmute_on_exit']}\n")
    #     f.write(f"disable double toggle = {settings_dict['double_toggle']}\n")
    #     f.write(f"crash timer limit = {int(float(settings_dict['crash_timer_limit']) * 60)}\n")
    #     f.write(f"crash limit = {settings_dict['crash_limit']}\n")
    #     f.write(f"command cooldown = {settings_dict['command_cooldown']}\n")
    #     f.write(f"vad aggressiveness = {settings_dict['vad_aggressiveness']}\n")
    #     f.write(f"mic toggle key = {settings_dict['mute_hotkey']}\n")
    #     f.write("unmute commands:\n")
    #     for cmd in settings_dict["unmute_commands"]:
    #         f.write(f'"{cmd}",')
    #     f.write("\nmute commands:\n")
    #     for cmd in settings_dict["mute_commands"]:
    #         f.write(f'"{cmd}",')
    if os.path.exists(settings_path):
        try:
            os.remove(settings_path)
            logging.info("Old text settings file removed.")
        except Exception as e:
            logging.error(f"Failed to remove old text settings file: {e}")


def fillCommands(line):
    if '"' in line:
        phrases = [
            p.strip().strip('"').strip(",")
            for p in line.split(",")
            if p.strip().strip('"').strip(",")
        ]
        if section == "mute":
            settings["mute_commands"].update(phrases)

        elif section == "unmute":
            settings["unmute_commands"].update(phrases)


def get_settings_mtime():
    try:
        return os.path.getmtime(json_path)
    except:
        try:
            return os.path.getmtime(settings_path)
        except:
            pass
        return last_settings_update


try:
    last_settings_update = os.path.getmtime(json_path)
except FileNotFoundError:
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    # open(json_path, "w", encoding="utf-8").close()
    settings = load_settings()
    save_settings_to_file(settings)
    # save_settings_to_file(settings)
    last_settings_update = os.path.getmtime(json_path)
