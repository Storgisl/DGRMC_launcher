import os
import subprocess
import threading

from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal
import minecraft_launcher_lib as mc_lib

from .Page import Page


class MainPage(Page):
    to_settings = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        # Центральная часть страницы
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(40, 0, 40, 0)
        text_image_label = QLabel(self)
        text_image_pixmap = QPixmap("assets/MainPageLogo.png")
        text_image_label.setPixmap(text_image_pixmap)
        main_layout.addWidget(text_image_label, alignment=Qt.AlignCenter)
        nickname = QLabel(f"Welcome back {self.username_var}", self)
        nickname.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                color: #F0F0F0;
                padding: 0;
                margin: 0;
                font-weight: 200;
            }
        """
        )
        nickname.setFont(self.extra_light_font)
        main_layout.addWidget(nickname, alignment=Qt.AlignCenter)
        top_spacer = QSpacerItem(0, 200, QSizePolicy.Minimum, QSizePolicy.Fixed)
        main_layout.addItem(top_spacer)
        start_button = QPushButton("PLAY", self)
        start_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: #F0F0F0;
                font-size: 48px;
                font-weight: 400;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """
        )
        start_button.setFont(self.light_font)
        start_button.setCursor(Qt.PointingHandCursor)
        start_button.clicked.connect(self.run_mc)
        main_layout.addWidget(start_button, alignment=Qt.AlignCenter)
        top_spacer = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        main_layout.addItem(top_spacer)
        settings_button = QPushButton("settings", self)
        settings_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: #F0F0F0;
                font-size: 16px;
                font-weight: 400;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """
        )
        settings_button.setFont(self.regular_font)
        settings_button.setCursor(Qt.PointingHandCursor)
        settings_button.clicked.connect(self.go_to_settings)
        main_layout.addWidget(settings_button, alignment=Qt.AlignCenter)
        # Объединяем все части в один макет
        layout = QVBoxLayout()
        layout.addSpacing(20)  # Добавляем отступ сверху для navbar
        layout.addWidget(self.navbar_frame)
        layout.addSpacing(20)  # Добавляем отступ после navbar
        layout.addLayout(main_layout)
        layout.addStretch()
        layout.addLayout(self.footer_layout)
        self.setLayout(layout)

    def go_to_settings(self):
        self.to_settings.emit()

    def load_accounts(self):
        user_data = load_user_data(
            directory=self.config_dir, json_file=self.user_data_json
        )
        accounts = user_data.get("accounts", [])
        return accounts

    def user_status(self) -> bool:
        self.user_data = load_user_data(
            directory=self.config_dir, json_file=self.user_data_json
        )
        self.username_var = self.user_data.get("username", "")
        self.password_var = self.user_data.get("password", "")
        if self.username_var not in ("", None) and self.password_var not in ("", None):
            return True
        else:
            return False

    def run_mc(self, mc_dir: str) -> None:
        def run_minecraft():
            version = "1.20.1"
            forge_version = mc_lib.forge.find_forge_version(version)
            forge_vers = mc_lib.forge.forge_to_installed_version(forge_version)
            minecraft_directory = os.path.join(self.mc_dir, "DGRMClauncher")
            os.makedirs(minecraft_directory, exist_ok=True)
            command = mc_lib.command.get_minecraft_command(
                version=forge_vers,
                minecraft_directory=minecraft_directory,
                options=self.user_data,
            )
            try:
                subprocess.call(command)
            except Exception as e:
                print("pizdec vse slomalos")

        thread = threading.Thread(target=run_minecraft, daemon=True)
        thread.start()
