from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QSpinBox, QLabel, QPushButton, QWidget
)
from PySide6.QtCore import Qt, Signal
from icecream import ic

from .page import Page


class SettingsPage(Page):
    go_back = Signal()

    def __init__(self):
        super().__init__()

    def initUI(self):
        super().initUI()
        layout = QVBoxLayout()

        self.go_back_button = QPushButton("Назад")
        self.go_back_button.clicked.connect(self.emit_signal)
        # Minimum RAM spin box
        self.min_label = QLabel("Minimum RAM (MiB):")
        self.min_spinbox = QSpinBox()
        self.min_spinbox.setMinimum(512)
        self.min_spinbox.setMaximum(32768)
        self.min_spinbox.setValue(512)
        self.min_spinbox.setSingleStep(128)

        # Maximum RAM spin box
        self.max_label = QLabel("Maximum RAM (MiB):")
        self.max_spinbox = QSpinBox()
        self.max_spinbox.setMinimum(512)
        self.max_spinbox.setMaximum(32768)
        self.max_spinbox.setValue(2048)
        self.max_spinbox.setSingleStep(128)

        # Button to display JVM arguments
        self.generate_button = QPushButton("Generate JVM Arguments")
        self.generate_button.clicked.connect(self.generate_jvm_arguments)

        # Label to show generated JVM arguments
        self.output_label = QLabel("")
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_label.setWordWrap(True)

        # Add widgets to layout
        layout.addWidget(self.go_back_button)
        layout.addWidget(self.min_label)
        layout.addWidget(self.min_spinbox)
        layout.addWidget(self.max_label)
        layout.addWidget(self.max_spinbox)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.output_label)
        self.setLayout(layout)

    def emit_signal(self):
        ic("settings button clicked")
        self.go_back.emit()

    def generate_jvm_arguments(self):
        min_ram = self.min_spinbox.value()
        max_ram = self.max_spinbox.value()

        if min_ram > max_ram:
            self.output_label.setText("Error: Minimum RAM cannot be greater than Maximum RAM.")
        else:
            jvm_args = f"-Xms{min_ram}M -Xmx{max_ram}M"
            self.output_label.setText(f"JVM Arguments: {jvm_args}")
