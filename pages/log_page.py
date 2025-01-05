from PySide6.QtWidgets import QVBoxLayout, QPushButton
from .page import Page

class LoginPage(Page):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Login"))
        self.setLayout(layout)
