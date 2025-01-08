from PySide6.QtWidgets import QVBoxLayout, QPushButton
from .page import Page

class LoginPage(Page):
    def __init__(self):
        super().__init__()

    def initUI(self):
        super().initUI()
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Login"))
        self.setLayout(layout)
