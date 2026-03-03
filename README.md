# Voice Mic Control

## About

Voice Mic Control is an executable voice automation tool that lets you mute or unmute your microphone using custom audio cues.

The program is designed to be lightweight and donationware. Please do not redistribute or claim credit for this project.

---

## Usage

1. Run the executable file (under releases on the right side).
2. The program will automatically start listening for voice commands.
3. Use your configured voice commands to control microphone mute status.

---

## Configuration

Edit:

```
settings.txt
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

This contains suggested command phrases or replacements that work better with the speech model.

---

## Performance Notes

The default speech model is intentionally lightweight to maintain low CPU usage and fast response times.

Using larger speech recognition models can improve recognition accuracy but may increase memory and CPU usage. For most users, the default model provides the best balance between accuracy and performance.

---

## Contact

Support and Feedback: Discord: malso

---

## Files Included

* Executable program
* `settings.txt` – User configuration
* `recommended.txt` – Suggested voice commands
* `requirements.txt` – Python dependencies (if running from source)

---

## Privacy

No audio data is stored or transmitted externally.  
All processing is performed locally and discarded after processing.

---

## License

MIT License

Copyright (c) 2026 xMalso

This software is provided "as is" without warranty. Use at your own risk.

---

### Third-Party Libraries

This project uses Vosk Speech Recognition.
See THIRD_PARTY_LICENSES.txt for full license details.