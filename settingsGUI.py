import math

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QCheckBox,
    QPushButton,
)
from PySide6.QtGui import QIntValidator, QDoubleValidator
from commandList import CommandList
from hotkeyInput import HotkeyRecorder
from settingsLoader import save_settings_to_file, load_settings

checked = False

def load_gui():
    def on_close(event):
        global settings_window
        settings_window = None
        event.accept()

    current_settings = load_settings()
    window = QWidget()
    window.setWindowTitle("MuteMe Settings")
    layout = QVBoxLayout()
    window.setLayout(layout)
    window.closeEvent = on_close

    hey_req = create_checkbox(
        "Hey Required", "Would you like to require 'hey' to be said before commands?"
    )
    hey_req.setChecked(current_settings["hey_required"])
    unmute_on_exit = create_checkbox(
        "Unmute on Exit",
        "Would you like the microphone to be unmuted if it believes it to be muted when the application is closed?",
    )
    unmute_on_exit.setChecked(current_settings["unmute_on_exit"])
    double_toggle = create_checkbox(
        "Double Toggle",
        "Would you like to allow the program to toggle the microphone via an unmute command if it is not in a muted state or vice versa?",
    )
    double_toggle.setChecked(current_settings["double_toggle"])

    crash_timer = create_input_box(
        "Crash Timer Limit (minutes)",
        "How long to wait in minutes until reseting crash counter.",
        doubles_only=True,
        range=(0, float("inf")),
    )
    crash_timer[1].setText(f"{current_settings['crash_timer_limit']/60:.2f}")
    crash_limit = create_input_box(
        "Crash Limit",
        "How many errors to allow (while logging) before allowing the program to crash.",
        int_only=True,
        range=(0, 2147483647),
    )
    crash_limit[1].setText(str(current_settings["crash_limit"]))
    command_cooldown = create_input_box(
        "Command Cooldown (seconds)",
        "How long to wait in seconds before processing audio input after toggling microphone.",
        doubles_only=True,
        range=(0, float("inf")),
    )
    command_cooldown[1].setText(f"{current_settings['command_cooldown']:.3f}")
    vad_aggressiveness = create_dropdown(
        "VAD Aggressiveness",
        [
            "0, Least Aggressive",
            "1, Less Aggressive",
            "2, More Aggressive",
            "3, Most Aggressive",
        ],
        "How aggressive the VAD should be in filtering out background noise. 0 is least aggressive, 3 is most aggressive.",
    )
    vad_aggressiveness[1].setCurrentIndex(int(current_settings["vad_aggressiveness"]))

    mute_commands = CommandList(
        "Mute Commands",
        "The voice commands you would like to toggle mic off, check recommended.txt or use debug mode to experiment and test settings.",
        current_settings["mute_commands"],
    )

    unmute_commands = CommandList(
        "Unmute Commands",
        "The voice commands you would like to toggle mic on, check recommended.txt or use debug mode to experiment and test settings.",
        current_settings["unmute_commands"],
    )

    mute_hotkey = HotkeyRecorder(
        "Discord Mute Hotkey",
        "The hotkey to simulate pressing when a voice command is recognized. This should be set to your Discord toggle mute hotkey too.",
    )
    mute_hotkey.hotkey_box.setText(current_settings["mute_hotkey"])

    save_button = QPushButton("Save")
    save_button.clicked.connect(
        lambda checked=False: save_settings(
            save_button,
            hey_req,
            unmute_on_exit,
            double_toggle,
            crash_timer[1],
            crash_limit[1],
            command_cooldown[1],
            vad_aggressiveness[1],
            mute_commands,
            unmute_commands,
            mute_hotkey,
        )
    )

    for widget in [hey_req, unmute_on_exit, double_toggle]:
        layout.addWidget(widget)

    for label, box in [crash_timer, crash_limit, command_cooldown, vad_aggressiveness]:
        layout.addWidget(label)
        layout.addWidget(box)

    for widget in [mute_commands, unmute_commands, mute_hotkey]:
        layout.addWidget(widget.label)
        layout.addWidget(widget)

    layout.addWidget(save_button)

    return window


def create_input_box(
    label, placeholder="", tooltip=None, int_only=False, doubles_only=False, range=None
):
    input_label = QLabel(label)
    input_box = QLineEdit()
    input_box.setPlaceholderText(placeholder)
    if tooltip:
        input_box.setToolTip(tooltip)
    if int_only:
        if range is None:
            range = (0, 100)
        input_box.setValidator(QIntValidator(*range))
    if doubles_only:
        if range is None:
            range = (float("-inf"), float("inf"))
        input_box.setValidator(QDoubleValidator(*range, 2))
    return input_label, input_box


def create_dropdown(label, options, tooltips=None):
    dropdown_label = QLabel(label)
    dropdown = QComboBox()
    dropdown.addItems(options)
    if tooltips:
        dropdown.setToolTip(tooltips)
    return dropdown_label, dropdown


def create_checkbox(label, tooltip=None):
    checkbox = QCheckBox(label)
    if tooltip:
        checkbox.setToolTip(tooltip)
    return checkbox


def save_settings(
    button,
    hey_req,
    unmute_on_exit,
    double_toggle,
    crash_timer,
    crash_limit,
    command_cooldown,
    vad_aggressiveness,
    mute_commands,
    unmute_commands,
    mute_hotkey,
):
    global checked
    checked = True
    if button:
        button.setEnabled(False)
        button.setText("Saving...")
    settings = {
        "hey_required": hey_req.isChecked(),
        "unmute_on_exit": unmute_on_exit.isChecked(),
        "double_toggle": double_toggle.isChecked(),
        "crash_timer_limit": int(float(crash_timer.text()) * 60),
        "crash_limit": int(crash_limit.text()),
        "command_cooldown": float(command_cooldown.text()),
        "vad_aggressiveness": vad_aggressiveness.currentIndex(),
        "mute_commands": mute_commands.get_commands(),
        "unmute_commands": unmute_commands.get_commands(),
        "mute_hotkey": mute_hotkey.get_hotkey(),
    }
    save_settings_to_file(settings)
    if button:
        button.setEnabled(True)
        button.setText("Save")


# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     window = load_gui()
#     window.show()

#     sys.exit(app.exec())
