import sys
import os

from PySide6.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manip_data import save_user_data, load_user_data
from .page import Page


class RegistrationPage(Page):
    registration_complete = Signal()
    already_registered = Signal()

    def __init__(self):
        super().__init__()

    def initUI(self):
        super().initUI()
        self.username_text = QLineEdit()
        self.password_text = QLineEdit()

        # Кнопки
        self.register_button = QPushButton("ENTER")
        self.register_button.clicked.connect(self.handle_registration)

        # Заголовок
        self.title_label = QLabel("REGISTRATION")
        self.title_label.setAlignment(Qt.AlignCenter)
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
        self.already_button = QPushButton("I`M ALREADY REGISTERED")
        self.already_button.setStyleSheet("""
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
        self.already_button.setFont(self.custom_font_button)
        self.already_button.clicked.connect(self.handle_already)

        # Кнопка регистрации
        self.register_button = QPushButton("ENTER")
        self.register_button.setStyleSheet("""
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
        self.register_button.setFont(self.custom_font_button)
        self.register_button.clicked.connect(self.handle_registration)

        self.username_text.setAlignment(Qt.AlignCenter)
        self.password_text.setAlignment(Qt.AlignCenter)

        # Добавляем виджеты во фрейм
        self.frame_layout.addWidget(self.title_label, alignment=Qt.AlignTop)
        self.frame_layout.addWidget(self.nickname_label, alignment=Qt.AlignLeft)
        self.frame_layout.addWidget(self.username_text, alignment=Qt.AlignCenter)
        self.frame_layout.addWidget(self.password_label, alignment=Qt.AlignLeft)
        self.frame_layout.addWidget(self.password_text, alignment=Qt.AlignCenter)
        self.frame_layout.addWidget(self.already_button)
        self.frame_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        # Основной лейаут страницы
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.main_frame)
        self.setLayout(layout)

    def handle_registration(self) -> None:
        username = self.username_text.text()
        password = self.password_text.text()

        # Проверка данных для регистрации
        if username and password:
            print(f"Регистрация прошла успешно: {username}")
            self.user_data = {"username": username,
                              "password": password
                             }
            save_user_data(
                new_data=self.user_data,
                directory=self.config_dir,
                json_file=self.user_data_json
            )
            self.registration_complete.emit()
        else:
            self.show_error("Заполните все поля.")

    def user_status(self) -> bool:
        self.user_data = load_user_data(
        directory=self.config_dir,
        json_file=self.user_data_json
        )
        self.username_var = self.user_data.get("username", "")
        self.password_var = self.user_data.get("password", "")
        if (self.username_var not in ("", None)
                and self.password_var not in ("", None)):
            return True
        else:
            return False

    def show_error(self, message: str) -> None:
        """Показать ошибку на экране регистрации."""
        if not self.error_label:
            self.error_label = QLabel()
            self.error_label.setStyleSheet("color: red;")
            self.layout().addWidget(self.error_label)

        self.error_label.setText(message)

    def handle_already(self) -> None:
        self.already_registered.emit()
