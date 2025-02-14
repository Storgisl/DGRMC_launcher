from PySide6.QtWidgets import (
    QLabel,
)
from PySide6.QtCore import Signal

from UI import RegistrationPageUI

from .Page import Page


class RegistrationPage(Page):
    registration_complete = Signal()
    go_to_login = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.page_logger.info("Registration page initialized")
        self.setObjectName("registration_page")
        self.stacked_widget = stacked_widget
        self.ui = RegistrationPageUI(self)

    def handle_registration(self) -> None:
        username = self.ui.username_text.text()
        password = self.ui.password_text.text()
        user_data = self.user_data
        if username and password:
            print(f"Регистрация прошла успешно: {username}")
            if not isinstance(self.user_data, dict):
                user_data = {}
            self.user_data[username] = {"password": password}

            self.data_manip.save_user_data(
                new_data=self.user_data,
                directory=self.config_dir,
                json_file=self.user_data_json,
            )

            self.registration_complete.emit()
        else:
            self.show_error("Заполните все поля.")

    def show_error(self, message: str) -> None:
        if not self.error_label:
            self.error_label = QLabel()
            self.error_label.setStyleSheet("color: red;")
            self.layout().addWidget(self.error_label)
        self.error_label.setText(message)
