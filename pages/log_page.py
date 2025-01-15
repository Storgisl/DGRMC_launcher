import sys
import os

from PySide6.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manip_data import save_user_data, load_user_data
from .page import Page

class LoginPage(Page):
    login_complete = Signal()
    no_acc = Signal()

    def __init__(self):
        super().__init__()

    def initUI(self):
        super().initUI()
        self.username_text = QLineEdit()
        self.password_text = QLineEdit()

        # Заголовок
        self.title_label = QLabel("LOGIN")
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 55px;
                color: #cb92e5;
                margin-bottom: -15px;
            }
        """)
        self.title_label.setFont(self.custom_font_label)

        # Надпись над полем "Nickname"
        self.nickname_label = QLabel("NICKNAME")
        self.nickname_label.setFont(self.custom_font_label)
        self.nickname_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #d4c0d0;
                font-weight: bold;
                margin-left: 22px;
                margin-bottom: -15px;
                margin-top: -10px;
            }
        """)

        self.username_text = QLineEdit()
        self.username_text.setPlaceholderText("")
        self.username_text.setStyleSheet("""
            QLineEdit {
                background-color: #342f2f;
                border: 2px solid #4f4f4f;
                border-radius: 15px;
                min-width: 280px;
                max-width: 400px;
                min-height: 40px;
                max-height: 100px;
                font-size: 28px;
                text-align: center;
                color: #ffffff;
            }
        """)
        self.username_text.setFont(self.custom_font_button)

        # Надпись над полем "Password"
        self.password_label = QLabel("PASSWORD")
        self.password_label.setFont(self.custom_font_label)
        self.password_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #d4c0d0;
                font-weight: bold;
                margin-left: 22px;
                margin-bottom: -12px;
            }
        """)

        self.password_text = QLineEdit()
        self.password_text.setPlaceholderText("")
        self.password_text.setEchoMode(QLineEdit.Password)
        self.password_text.setStyleSheet("""
            QLineEdit {
                background-color: #342f2f;
                border: 2px solid #4f4f4f;
                border-radius: 15px;
                min-width: 280px;
                max-width: 400px;
                min-height: 40px;
                max-height: 100px;
                font-size: 16px;
                text-align: center;
                color: #ffffff;
            }
        """)
        self.password_text.setFont(self.custom_font_button)

        # Кнопка для тех кто уже смешарик
        self.no_acc_button = QPushButton("I DON`T HAVE AN ACCOUNT")
        self.no_acc_button.setStyleSheet("""
            QPushButton {
                background-color: #342f2f;
                color: #cb92e5;
                font-size: 16px;
                border: none;
                margin-top: 20px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #e2a1ff;
            }
        """)
        
        self.no_acc_button.setFont(self.custom_font_button)
        self.no_acc_button.clicked.connect(self.handle_no_acc)

        # Кнопка регистрации
        self.login_button = QPushButton("ENTER")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                color: #cb92e5;
                font-weight: bold;
                font-size: 48px;
                border: 2px solid #cb92e5;
                border-radius: 20px;
                margin-top: 20px;
                min-width: 280px;
                max-width: 400px;
            }
            QPushButton:hover {
                color: #e2a1ff;
                border: 2px solid #e2a1ff;
            }
        """)
        self.login_button.setFont(self.custom_font_button)
        self.login_button.clicked.connect(self.handle_login)

        self.title_label.setAlignment(Qt.AlignCenter)
        self.username_text.setAlignment(Qt.AlignCenter)
        self.password_text.setAlignment(Qt.AlignCenter)

        # Добавляем виджеты во фрейм
        self.frame_layout.addWidget(self.title_label, alignment=Qt.AlignTop)
        self.frame_layout.addWidget(self.nickname_label, alignment=Qt.AlignLeft)
        self.frame_layout.addWidget(self.username_text, alignment=Qt.AlignCenter)
        self.frame_layout.addWidget(self.password_label, alignment=Qt.AlignLeft)
        self.frame_layout.addWidget(self.password_text, alignment=Qt.AlignCenter)
        self.frame_layout.addWidget(self.no_acc_button)
        self.frame_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        # Основной лейаут страницы
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.main_frame)
        self.setLayout(layout)

    def handle_login(self) -> None:
        pass

    def handle_no_acc(self) -> None:
        self.no_acc.emit()