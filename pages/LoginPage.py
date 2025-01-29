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


class LoginPage(Page):
    go_to_reg = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.setObjectName("login_page")
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        navbar_layout = QHBoxLayout()
        navbar_layout.setContentsMargins(40, 0, 40, 0)
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("assets/Logo.png")
        logo_label.setPixmap(logo_pixmap)
        navbar_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        navbar_layout.addSpacing(165)

        sign_in_button = QPushButton("Sign In", self)
        sign_in_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #7C58FF;
                font-size: 16px;
                border: none;
            }
        """
        )
        sign_in_button.setFont(self.medium_font)
        navbar_layout.addWidget(sign_in_button)

        navbar_layout.addStretch()

        sign_up_button = QPushButton("Sign Up", self)
        sign_up_button.setStyleSheet(
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
        sign_up_button.setFont(self.medium_font)
        sign_up_button.setCursor(Qt.PointingHandCursor)
        sign_up_button.clicked.connect(self.show_sign_up_page)
        navbar_layout.addWidget(sign_up_button)

        navbar_layout.addStretch()
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
        navbar_layout.addWidget(version_label, alignment=Qt.AlignCenter)

        navbar_frame = QFrame(self)
        navbar_frame.setLayout(navbar_layout)
        navbar_frame.setFixedHeight(44)

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
        text_image_pixmap = QPixmap("assets/TextLogin.png")
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

        enter_button = QPushButton("Enter", self)
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
        enter_button.clicked.connect(self.handle_login)
        frame_layout.addWidget(enter_button, alignment=Qt.AlignTop | Qt.AlignHCenter)
        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        frame_layout.addItem(top_spacer)
        frame.setLayout(frame_layout)
        main_layout.addWidget(frame, alignment=Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(navbar_frame)
        layout.addSpacing(60)
        layout.addLayout(main_layout)
        layout.addStretch()
        layout.addLayout(self.footer_layout)
        self.setLayout(layout)

    def show_error(self, message: str) -> None:
        if not self.error_label:
            self.error_label = QLabel()
            self.error_label.setStyleSheet("color: red;")
            self.layout().addWidget(self.error_label)
        self.error_label.setText(message)

    def handle_login(self) -> None:
        print("login idi nahui")

    def show_sign_up_page(self):
        self.go_to_reg.emit()
