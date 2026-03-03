import os

settings_path = "settings.txt"
last_settings_update = os.path.getmtime(settings_path)

settings = {
        "hey_required": True,
        "unmute_on_exit": True,
        "crash_timer_limit": 5 * 60,
        "crash_limit": 5,
        "command_cooldown": 0.5,
        "vad_aggressiveness": 0,
        "mute_commands": [],
        "unmute_commands": [],
        "mic_toggle_key": "ctrl+f12",
}

def load_settings():
    global last_settings_update, settings, section
    # settings = {
    #     "hey_required": True,
    #     "crash_timer_limit": 5 * 60,
    #     "crash_limit": 5,
    #     "command_cooldown": 0.5,
    #     "vad_aggressiveness": 0,
    #     "mute_commands": [],
    #     "unmute_commands": [],
    #     "mic_toggle_key": "ctrl+f12",
    # }

    section = None

    with open("settings.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().lower()

            if line.startswith("hey required"):
                settings["hey_required"] = "true" in line
                section = None
            elif line.startswith("unmute on exit"):
                settings["unmute_on_exit"] = "true" in line
                section = None
            elif line.startswith("crash timer limit"):
                settings["crash_timer_limit"] = int(
                    float(
                        line.strip("crash timer limit").strip("").strip("=").strip("")
                    )
                    * 60
                )
                section = None
            elif line.startswith("crash limit"):
                settings["crash_limit"] = int(
                    line.strip("crash limit").strip("").strip("=").strip("")
                )
                section = None
            elif line.startswith("command cooldown"):
                settings["command_cooldown"] = float(
                    line.strip("command cooldown").strip("").strip("=").strip("")
                )
                section = None
            elif line.startswith("vad aggressiveness"):
                settings["vad_aggressiveness"] = int(
                    line.strip("vad aggressiveness").strip("").strip("=").strip("")
                )
                section = None
            elif line.startswith("mic toggle key"):
                settings["mic_toggle_key"] = (
                    line.strip("mic toggle key").strip("").strip("=").strip("")
                )
                section = None
            elif line.startswith("unmute commands"):
                section = "unmute"
            elif line.startswith("mute commands"):
                section = "mute"
            if section != None:
                fillCommands(line)
    last_settings_update = os.path.getmtime(settings_path)
    return settings


def fillCommands(line):
    global settings
    if '"' in line:
        phrases = [
            p.strip().strip('"') for p in line.split('","') if p.strip().strip('"')
        ]
        if section == "mute":
            settings["mute_commands"] = phrases

        elif section == "unmute":
            settings["unmute_commands"] = phrases


def get_settings_mtime():
    try:
        return os.path.getmtime(settings_path)
    except:
        return last_settings_update


def get_last_settings_update():
    return last_settings_update
