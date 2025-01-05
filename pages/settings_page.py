from PySide6.QtWidgets import QVBoxLayout, QPushButton

from .page import Page


class SettingsPage(Page):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Settings"))
        self.setLayout(layout)
