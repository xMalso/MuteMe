from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
)


class CommandList(QWidget):

    def __init__(self, label, tooltip=None, current_settings=None):
        super().__init__()

        self.layout = QVBoxLayout()
        self.inputs = []
        self.label = QLabel(label)
        if tooltip:
            self.info = QLabel("ⓘ")
            self.info.setToolTip(tooltip)

        self.layout.addWidget(self.label)
        if tooltip:
            self.layout.addWidget(self.info)
        self.setLayout(self.layout)

        # Start with two empty rows
        if current_settings:
            for cmd in current_settings:
                self.add_row(cmd)
        self.validate_rows()

        # if current_settings:
        #     for cmd in current_settings:
        #         if cmd.strip(",").strip('"'):
        #             self.add_row(cmd)

    # Create a command input row
    def add_row(self, text=""):
        box = QLineEdit()
        box.setPlaceholderText("Enter command...")
        box.setText(text)
        box.textChanged.connect(self.validate_rows)

        self.layout.addWidget(box)
        self.inputs.append(box)

    # Remove extra empty rows (keep only 1 empty row)
    def cleanup_empty_rows(self):
        empty_boxes = [b for b in self.inputs if not b.text().strip()]

        # Keep only 1 empty box
        for box in empty_boxes[:-1]:
            self.layout.removeWidget(box)
            box.deleteLater()
            self.inputs.remove(box)

    # Check if we need a new row
    def validate_rows(self):
        filled_boxes = [b for b in self.inputs if b.text().strip()]

        if len(filled_boxes) == 0:
            while len(self.inputs) < 2:
                self.add_row()
        else:
            self.cleanup_empty_rows()

        # If all boxes are filled → add new row
        if all(box.text().strip() for box in self.inputs):
            self.add_row()

    def get_commands(self):
        return set([b.text().strip() for b in self.inputs if b.text().strip()])
