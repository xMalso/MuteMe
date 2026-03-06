# MuteMd

## About

MuteMe is an executable voice automation tool that lets you mute or unmute your microphone using custom audio cues.

The program is designed to be lightweight and donationware. Please do not redistribute or claim credit for this project.

---

## Usage

1. Set up a keybind to mute
2. Assign keybind in assets/txt files/settings.txt
3. Run the executable file (under releases on the right side).
4. The program will automatically start listening for voice commands.
5. Use your configured voice commands to control your microphone mute status.
6. Enable/Disable Run on Startup in System Tray
7. Exit from System Tray

---

## Configuration

Edit:

```
assets/txt files/settings.txt
```

You can customize:

* Voice trigger requirement
* Command cooldowns
* Crash handling limits
* Voice commands for mute and unmute

For best recognition results, check:

```
recommended.txt
```

This contains suggested command phrases or replacements that work better with the speech model, or even ways to see what the program is picking up.

---

## Performance Notes

The default speech model is intentionally lightweight to maintain low CPU usage and fast response times.

Using larger speech recognition models can improve recognition accuracy but may increase memory and CPU usage. The default model provides high performance without sacrificing major accuracy loss.

---

## Contact

Support and Feedback: Discord: malso

---

## Donate

Buy me a not coffee.
https://paypal.me/malsoo

## Files Included

* Executable program
* `assets/txt files/settings.txt` – User configuration
* `assets/txt files/recommended.txt` – Suggested voice commands
* `requirements.txt` – Python dependencies (if running from source)  USE PYTHON 3.11.9!!!!!

---

## Privacy

No audio data is stored or transmitted externally.  
All processing is performed locally and discarded immediately after processing.

---

## License

MIT License

Copyright (c) 2026 xMalso

This software is provided "as is" without warranty. Use at your own risk.

---

### Third-Party Libraries

This project uses Vosk Speech Recognition.
See THIRD_PARTY_LICENSES.txt for full license details.
