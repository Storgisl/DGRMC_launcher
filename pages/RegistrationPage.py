import sys
import os

from PySide6.QtWidgets import (
    QLineEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal

from .Page import Page


class RegistrationPage(Page):
    registration_complete = Signal()
    go_to_login = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.setObjectName("registration_page")
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        navbar_reg_layout = QHBoxLayout()
        navbar_reg_layout.setContentsMargins(40, 0, 40, 0)
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("assets/Logo.png")
        logo_label.setPixmap(logo_pixmap)
        navbar_reg_layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        navbar_reg_layout.addSpacing(165)

        sign_in_button = QPushButton("Sign In", self)
        sign_in_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #F0F0F0;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """
        )
        sign_in_button.setCursor(Qt.PointingHandCursor)
        sign_in_button.clicked.connect(self.show_sign_in_page)
        sign_in_button.setFont(self.medium_font)
        navbar_reg_layout.addWidget(sign_in_button)

        navbar_reg_layout.addStretch()

        sign_up_button = QPushButton("Sign Up", self)
        sign_up_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #7C58FF;
                font-size: 16px;
                border: none;
            }
        """
        )
        sign_up_button.setFont(self.medium_font)
        navbar_reg_layout.addWidget(sign_up_button)

        navbar_reg_layout.addStretch()
        version_label = QLabel("v2.1.1", self)
        version_label.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #F0F0F0;
                padding: 0;
                vertical-align: middle;
            }
        """
        )
        version_label.setFont(self.medium_font)
        navbar_reg_layout.addWidget(version_label, alignment=Qt.AlignCenter)

        navbar_reg_frame = QFrame(self)
        navbar_reg_frame.setLayout(navbar_reg_layout)
        navbar_reg_frame.setFixedHeight(44)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        frame = QFrame(self)
        frame.setFixedSize(440, 300)
        frame.setStyleSheet(
            """
            QFrame {
                background-color: #412483;
                border-radius: 10px;
            }
        """
        )
        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignCenter)

        text_image_label = QLabel(self)
        text_image_pixmap = QPixmap("assets/TextRegister.png")
        text_image_label.setPixmap(text_image_pixmap)
        frame_layout.addWidget(
            text_image_label, alignment=Qt.AlignTop | Qt.AlignHCenter
        )

        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        frame_layout.addItem(top_spacer)

        nickname_label = QLabel("Nickname", self)
        nickname_label.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                color: #B3A1C7;
            }
        """
        )
        nickname_label.setFont(self.regular_font)
        frame_layout.addWidget(nickname_label, alignment=Qt.AlignLeft | Qt.AlignHCenter)

        self.username_text = QLineEdit(self)
        self.username_text.setPlaceholderText("")
        self.username_text.setAlignment(Qt.AlignCenter)
        self.username_text.setStyleSheet(
            """
            QLineEdit {
                background-color: #503684;
                color: #B3A1C7;
                font-size: 14px;
                border-radius: 5px;
                min-height: 30px;
                max-height: 30px;
                max-width: 360px;
                min-width: 360px;
            }
        """
        )
        self.username_text.setFont(self.regular_font)
        frame_layout.addWidget(
            self.username_text, alignment=Qt.AlignTop | Qt.AlignHCenter
        )

        password_label = QLabel("Password", self)
        password_label.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                color: #B3A1C7;
            }
        """
        )
        password_label.setFont(self.regular_font)
        frame_layout.addWidget(password_label, alignment=Qt.AlignLeft | Qt.AlignHCenter)

        self.password_text = QLineEdit(self)
        self.password_text.setPlaceholderText("")
        self.password_text.setAlignment(Qt.AlignCenter)
        self.password_text.setEchoMode(QLineEdit.Password)
        self.password_text.setStyleSheet(
            """
            QLineEdit {
                background-color: #503684;
                color: #B3A1C7;
                font-size: 14px;
                border-radius: 5px;
                min-height: 30px;
                max-height: 30px;
                max-width: 360px;
                min-width: 360px;
            }
        """
        )
        self.password_text.setFont(self.regular_font)
        frame_layout.addWidget(
            self.password_text, alignment=Qt.AlignTop | Qt.AlignHCenter
        )

        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        frame_layout.addItem(top_spacer)

        enter_button = QPushButton("Register", self)
        enter_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #F0F0F0;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """
        )
        enter_button.setFont(self.regular_font)
        enter_button.setCursor(Qt.PointingHandCursor)
        enter_button.clicked.connect(self.handle_registration)
        frame_layout.addWidget(enter_button, alignment=Qt.AlignTop | Qt.AlignHCenter)

        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        frame_layout.addItem(top_spacer)
        frame.setLayout(frame_layout)
        main_layout.addWidget(frame, alignment=Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(navbar_reg_frame)
        layout.addSpacing(60)
        layout.addLayout(main_layout)
        layout.addStretch()
        layout.addLayout(self.footer_layout)
        self.setLayout(layout)

    def handle_registration(self) -> None:
        username = self.username_text.text()
        password = self.password_text.text()

        if username and password:
            print(f"Регистрация прошла успешно: {username}")

            user_data = self.data_manip.load_user_data(
                directory=self.config_dir, json_file=self.user_data_json
            )

            # Update the structure with the new format
            if not isinstance(user_data, dict):
                user_data = {}
            user_data[username] = {"password": password}

            self.data_manip.save_user_data(
                new_data=user_data,
                directory=self.config_dir,
                json_file=self.user_data_json,
            )

            self.registration_complete.emit()
        else:
            self.show_error("Заполните все поля.")

    def user_status(self) -> bool:
        user_data = self.data_manip.load_user_data(
            directory=self.config_dir, json_file=self.user_data_json
        )

        if isinstance(user_data, dict):
            for username, details in user_data.items():
                if isinstance(details, dict) and "password" in details:
                    self.username_var = username
                    self.password_var = details["password"]
                    return True

        return False

    def show_error(self, message: str) -> None:
        if not self.error_label:
            self.error_label = QLabel()
            self.error_label.setStyleSheet("color: red;")
            self.layout().addWidget(self.error_label)
        self.error_label.setText(message)

    def show_sign_in_page(self):
        self.go_to_login.emit()
