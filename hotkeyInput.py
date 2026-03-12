from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from micControl import logging


class HotkeyInput(QLineEdit):

    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Press hotkey...")
        self.keys = set()
        self.key_labels = {}
        self.temp_labels = {}
        self.saved_keys = {}

        self.modifier_mapping = {
            Qt.Key_Control: "Ctrl",
            Qt.Key_Shift: "Shift",
            Qt.Key_Alt: "Alt",
            Qt.Key_Meta: "Meta",
        }

        self.fkey_mapping = {
            Qt.Key_F1: "F1",
            Qt.Key_F2: "F2",
            Qt.Key_F3: "F3",
            Qt.Key_F4: "F4",
            Qt.Key_F5: "F5",
            Qt.Key_F6: "F6",
            Qt.Key_F7: "F7",
            Qt.Key_F8: "F8",
            Qt.Key_F9: "F9",
            Qt.Key_F10: "F10",
            Qt.Key_F11: "F11",
            Qt.Key_F12: "F12",
        }

    def keyPressEvent(self, event):
        key = event.key()
        if self.temp_labels != self.key_labels:
            self.key_labels = dict(self.temp_labels)

        if len(self.keys) >= 4:
            self.update_display()
            return

        if key in self.modifier_mapping:
            self.keys.add(key)
            self.key_labels[key] = self.modifier_mapping[key]
            self.temp_labels[key] = self.modifier_mapping[key]

        elif key in self.fkey_mapping:
            self.keys.add(key)
            self.key_labels[key] = self.fkey_mapping[key]
            self.temp_labels[key] = self.fkey_mapping[key]

        elif event.text() and event.text().isprintable():
            self.keys.add(key)
            self.key_labels[key] = event.text().upper()
            self.temp_labels[key] = event.text().upper()

        self.update_display()

    def keyReleaseEvent(self, event):
        key = event.key()
        # temp = self.saved_keys.copy()
        if key in self.modifier_mapping or key in self.fkey_mapping or event.text():
            if self.temp_labels == self.key_labels:
                self.saved_keys = dict(self.key_labels)
        else:
            logging.error(f"Unrecognized key released: {key} or text: {event.text()}")

        self.keys.discard(key)
        # self.key_labels.pop(key, None)
        self.temp_labels.pop(key, None)

        if self.saved_keys:
            self.setText(" + ".join(self.saved_keys.values()))
        else:
            self.update_display()

    def update_display(self):
        modifier_priority = {"Ctrl": 0, "Shift": 1, "Alt": 2, "Meta": 3}
        modifiers = []
        others = []

        for k in self.keys:
            label = self.key_labels.get(k, "")
            if k in self.modifier_mapping:
                modifiers.append(label)
            else:
                others.append(label)

        modifiers.sort(key=lambda x: modifier_priority.get(x, 99))
        self.setText(" + ".join(modifiers + others))

    def get_hotkey(self):
        return list(self.saved_keys.keys())


class HotkeyRecorder(QWidget):
    def __init__(self, label, tooltip=None):
        super().__init__()

        self.layout = QVBoxLayout()
        self.label = QLabel(label)
        self.hotkey_box = HotkeyInput()

        if tooltip:
            self.info = QLabel("ⓘ")
            self.info.setToolTip(tooltip)

        self.reset_button = QPushButton("Reset Hotkey")
        self.reset_button.clicked.connect(self.reset_hotkey)

        self.layout.addWidget(self.label)
        if tooltip:
            self.layout.addWidget(self.info)
        self.layout.addWidget(self.hotkey_box)
        self.layout.addWidget(self.reset_button)

        self.setLayout(self.layout)

    def reset_hotkey(self):
        self.hotkey_box.keys = set()
        self.hotkey_box.key_labels = {}
        self.hotkey_box.saved_keys = {}
        self.hotkey_box.setText("")
        self.hotkey_box.setPlaceholderText("Press hotkey...")

    def get_hotkey(self):
        return self.hotkey_box.text()
