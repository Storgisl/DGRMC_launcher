import sys
import os

from PySide6.QtWidgets import (
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


class LauncherSettings(Page):
    to_game_settings = Signal()
    go_back = Signal()
    to_account = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.setObjectName("launcher_settings_page")
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        # Navbar
        navbar_settings_layout = QHBoxLayout()
        navbar_settings_layout.setContentsMargins(40, 0, 40, 0)
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("assets/Logo.png")
        logo_label.setPixmap(logo_pixmap)
        navbar_settings_layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        navbar_settings_layout.addSpacing(140)
        sign_in_button = QPushButton("Launcher settings", self)
        sign_in_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #7C58FF;
                font-size: 16px;
                font-weight: 500;
                border: none;
            }
        """
        )
        sign_in_button.setFont(self.medium_font)
        navbar_settings_layout.addWidget(sign_in_button)
        navbar_settings_layout.addSpacing(160)
        # Кнопка Sign Up
        sign_up_button = QPushButton("Game settings", self)
        sign_up_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: #F0F0F0;
                font-size: 16px;
                font-weight: 500;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """
        )
        sign_up_button.setFont(self.medium_font)
        sign_up_button.setCursor(Qt.PointingHandCursor)
        sign_up_button.clicked.connect(self.show_game_settings_page)
        navbar_settings_layout.addWidget(sign_up_button)
        # Добавляем растяжку для равномерного распределения элементов
        navbar_settings_layout.addStretch()
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
        navbar_settings_layout.addWidget(version_label, alignment=Qt.AlignCenter)
        navbar_settings_frame = QFrame(self)
        navbar_settings_frame.setLayout(navbar_settings_layout)
        navbar_settings_frame.setFixedHeight(44)
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        frame = QFrame(self)
        frame.setFixedSize(400, 400)
        frame.setStyleSheet(
            """
            QFrame {
                background-color: #412483;
                border-radius: 10px;
            }
        """
        )
        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignTop)
        inner_navbar_settings_layout = QHBoxLayout()
        inner_navbar_settings_layout.setAlignment(Qt.AlignLeft)
        back_button = QPushButton(self)
        back_button.setStyleSheet(
            """
            QPushButton {
                background-image: url(assets/GoBack.png);
                background-repeat: no-repeat;
                background-position: left;
                background-color: transparent;
                border: none;
                padding-left: 15px;
                padding-right: 0;
                min-height: 30px;
                max-height: 30px;
                min-width: 40px;
                max-width: 40px;
                font-size: 14px;
                color: #7247CB;
                text-align: left;
                margin-left: 15px;
                margin-top: 5px;
                font-weight: 200;
            }
            QPushButton:hover {
                background-image: url(assets/GoBackHover.png);
                color: #F0F0F0;
            }
        """
        )
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.setText("back")
        back_button.setFont(self.extra_light_font)
        back_button.clicked.connect(self.go_back_to_main)
        inner_navbar_settings_layout.addWidget(back_button)
        frame_layout.addLayout(inner_navbar_settings_layout)
        ###########################################################
        top_spacer = QSpacerItem(0, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)
        frame_layout.addItem(top_spacer)
        change_account = QLabel("You may change account", self)
        change_account.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #7247CB;
                font-weight: 200;
            }
        """
        )
        change_account.setFont(self.extra_light_font)
        frame_layout.addWidget(change_account, alignment=Qt.AlignCenter)
        change_button = QPushButton("Change", self)
        change_button.setStyleSheet(
            """
            QPushButton {
                background-color: #503684;
                color: #F0F0F0;
                font-size: 16px;
                border-radius: 10px;
                min-height: 35px;
                max-height: 35px;
                min-width: 170px;
                max-width: 170px;
                font-weight: 400;
            }
            QPushButton:hover {
                background-color: #7247CB;
            }
        """
        )
        change_button.setFont(self.regular_font)
        change_button.setCursor(Qt.PointingHandCursor)
        change_button.clicked.connect(self.go_to_account)
        frame_layout.addWidget(change_button, alignment=Qt.AlignCenter)
        top_spacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        frame_layout.addItem(top_spacer)
        check_updates = QLabel("Check for updates", self)
        check_updates.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #7247CB;
                font-weight: 200;
            }
        """
        )
        check_updates.setFont(self.extra_light_font)
        frame_layout.addWidget(check_updates, alignment=Qt.AlignCenter)
        check_upd_button = QPushButton("Check", self)
        check_upd_button.setStyleSheet(
            """
            QPushButton {
                background-color: #503684;
                color: #F0F0F0;
                font-size: 16px;
                border-radius: 10px;
                min-height: 35px;
                max-height: 35px;
                min-width: 170px;
                max-width: 170px;
                font-weight: 400;
            }
            QPushButton:hover {
                background-color: #7247CB;
            }
        """
        )
        check_upd_button.setFont(self.regular_font)
        check_upd_button.setCursor(Qt.PointingHandCursor)
        check_upd_button.clicked.connect(self.check_updates)
        frame_layout.addWidget(check_upd_button, alignment=Qt.AlignCenter)
        top_spacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        frame_layout.addItem(top_spacer)
        open_folder_label = QLabel("Open game folder", self)
        open_folder_label.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #7247CB;
                font-weight: 200;
            }
        """
        )
        open_folder_label.setFont(self.extra_light_font)
        frame_layout.addWidget(open_folder_label, alignment=Qt.AlignCenter)
        open_folder_button = QPushButton("Open folder", self)
        open_folder_button.setStyleSheet(
            """
            QPushButton {
                background-color: #503684;
                color: #F0F0F0;
                font-size: 16px;
                border-radius: 10px;
                min-height: 35px;
                max-height: 35px;
                min-width: 170px;
                max-width: 170px;
                font-weight: 400;
            }
            QPushButton:hover {
                background-color: #7247CB;
            }
        """
        )
        open_folder_button.setFont(self.regular_font)
        open_folder_button.setCursor(Qt.PointingHandCursor)
        open_folder_button.clicked.connect(self.open_folder)
        frame_layout.addWidget(open_folder_button, alignment=Qt.AlignCenter)
        frame.setLayout(frame_layout)
        main_layout.addWidget(frame, alignment=Qt.AlignCenter)
        # Объединяем все части в один макет
        layout = QVBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(navbar_settings_frame)
        layout.addSpacing(40)
        layout.addLayout(main_layout)
        layout.addStretch()
        layout.addLayout(self.footer_layout)
        self.setLayout(layout)

    def show_game_settings_page(self) -> None:
        self.to_game_settings.emit()

    def go_to_account(self) -> None:
        self.to_account.emit()

    def go_back_to_main(self) -> None:
        self.go_back.emit()

    def check_updates(self) -> None:
        pass

    def open_folder(self) -> None:
        pass
