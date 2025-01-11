import os
import subprocess
import threading

from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor, Qt
from icecream import ic

import minecraft_launcher_lib as mc_lib

from .page import Page

class MainPage(Page):

    def __init__(self):
        super().__init__()

    def initUI(self):
        super().initUI()

        # Кнопошка настроек
        self.settings_button.show()
        #self.settings_button.setStyleSheet()
        #self.run_button.clicked.connect()

        # ник надо вытащить из джсона
        nickname = "{username}"
        self.title_label = QLabel(f"WELCOME \n {nickname}")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 70px;
                color: #cb92e5;
                margin-top: 80px;
            }
        """)
        self.title_label.setFont(self.custom_font_label)

        # Кнопка для запуска Minecraft
        self.run_button = QPushButton("PLAY")
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                color: #cb92e5;
                font-weight: bold;
                font-size: 48px;
                border: 2px solid #cb92e5;
                border-radius: 20px;
                margin-top: 70px;
                min-height: 60px; 
                max-height: 100px;
                min-width: 500px;
                max-width: 600px;
            }
            QPushButton:hover {
                color: #e2a1ff;
                border: 2px solid #e2a1ff;
            }
        """)
        self.run_button.setFont(self.custom_font_button)
        self.run_button.clicked.connect(self.run_mc)

        # Метка для отображения статуса
        self.status_label = QLabel("STATUS: READY")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #cb92e5;
                margin-top: 10px;
            }
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(self.custom_font_label)

        self.glavnaya_layout.addWidget(self.settings_button, alignment=Qt.AlignRight)
        self.glavnaya_layout.addWidget(self.title_label, alignment=Qt.AlignTop)
        self.glavnaya_layout.addWidget(self.run_button, alignment=Qt.AlignCenter)
        # статус скрыл
        #self.glavnaya_layout.addWidget(self.status_label, alignment=Qt.AlignBottom)

        # Основной лейаут страницы
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.glavnaya)
        self.setLayout(layout)

    def set_status(self, status: str):
        self.status_label.setText(f"STATUS: {status}")

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
                self.set_status("LAUNCHING MINECRAFT...")
                subprocess.call(command)
                self.set_status("MINECRAFT IS RUNNING!")
            except Exception as e:
                self.set_status(f"ERROR WHILE RUNNING: {e}")

        # Запуск Minecraft в отдельном потоке
        thread = threading.Thread(target=run_minecraft, daemon=True)
        thread.start()
