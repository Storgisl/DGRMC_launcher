import sys
import os

from PySide6.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manip_data.save_user_data import save_user_data
from .page import Page


class RegistrationPage(Page):
    registration_complete = Signal()

    def __init__(self):
        super().__init__()
        self.username_text = QLineEdit()
        self.password_text = QLineEdit()
        # Кнопки
        self.register_button = QPushButton("ENTER")
        self.register_button.clicked.connect(self.handle_registration)

        # Заголовок
        self.title_label = QLabel("REGISTRATION")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Установим стиль для кнопки "ENTER"
        self.register_button.setStyleSheet("background-color: #4CAF50; \
        color: white; \
        font-weight: bold;")

        self.title_label = QLabel("REGISTRATION")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 55px;
                color: #cb92e5;
            }
        """)

        self.title_label.setFont(self.custom_font_label)

        # Текстовые поля
        self.username_text = QLineEdit()
        self.username_text.setPlaceholderText("Enter username")
        self.username_text.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
        """)

        self.password_text = QLineEdit()
        self.password_text.setPlaceholderText("Enter password")
        self.password_text.setEchoMode(QLineEdit.Password)
        self.password_text.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
        """)

        # Кнопка для тех кто уже смешарик
        self.already_button = QPushButton("I`M ALREADY REGISTERED")
        self.already_button.setStyleSheet("""
            QPushButton {
                background-color: #342f2f;
                color: #cb92e5;
                font-size: 24px;
                border: none;
                margin-top: 20px;
                underline: true;
            }
            QPushButton:hover {
                color: #e2a1ff;
            }
        """)
        self.already_button.setFont(self.custom_font_button)
        #self.already_button.clicked.connect(self.handle_already)

        # Кнопка регистрации
        self.register_button = QPushButton("ENTER")
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #342f2f;
                color: #cb92e5;
                font-weight: bold;
                font-size: 48px;
                border: 2px solid #cb92e5;
                border-radius: 20px;
                margin-top: 20px;
                min-width: 150px;
                min-height: 30px;
            }
            QPushButton:hover {
                color: #e2a1ff;
                border: 2px solid #e2a1ff;
            }
        """)
        self.register_button.setFont(self.custom_font_button)
        self.register_button.clicked.connect(self.handle_registration)

        # Добавляем виджеты во фрейм
        self.frame_layout.addWidget(self.title_label, alignment=Qt.AlignTop)
        self.frame_layout.addWidget(self.username_text)
        self.frame_layout.addWidget(self.password_text)
        self.frame_layout.addWidget(self.already_button)
        self.frame_layout.addWidget(self.register_button)

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
                              "password": password,
                              "mc_dir": ""}
            save_user_data(
                new_data=self.user_data,
                directory=self.config_dir,
                json_file=self.user_data_json
            )
            self.registration_complete.emit()
        else:
            self.show_error("Заполните все поля.")

    def user_status(self) -> bool:
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
