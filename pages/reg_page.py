import sys
import os

from PySide6.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Signal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manip_data.save_user_data import save_user_data
from manip_data.load_user_data import load_user_data
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

        # Создаем компоновку
        layout = QVBoxLayout()

        # Добавляем виджеты
        layout.addWidget(self.title_label)
        layout.addWidget(self.username_text)
        layout.addWidget(self.password_text)
        layout.addWidget(self.register_button)
        layout.addWidget(self.error_label)

        # Устанавливаем layout для текущего виджета
        self.setLayout(layout)

    def handle_registration(self) -> None:
        username = self.username_text.text()
        password = self.password_text.text()

        # Проверка данных для регистрации
        if username and password:
            print(f"Регистрация прошла успешно: {username}")
            self.user_data = {"username": username, "password": password}
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
