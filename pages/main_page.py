import os
import subprocess
import threading
import shutil

from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from icecream import ic

import minecraft_launcher_lib as mc_lib

from .page import Page


class MainPage(Page):
    delete_complete = Signal()

    def __init__(self):
        super().__init__()

    def initUI(self):
        super().initUI()
        layout = QVBoxLayout()

        # Кнопка для запуска Minecraft
        self.run_button = QPushButton("Запустить Minecraft")
        self.run_button.clicked.connect(self.run_mc)
        self.delete_button = QPushButton("Удалить Minecraft")
        self.delete_button.clicked.connect(self.delete_mc)
        self.settings_button.show()
        layout.addWidget(self.run_button)
        layout.addWidget(self.delete_button)
        # Метка для отображения статуса
        self.status_label = QLabel("Статус: Готово")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def set_status(self, status: str):
        """Метод для обновления статуса на UI"""
        self.status_label.setText(f"Статус: {status}")

    def run_mc(self, mc_dir: str) -> None:
        def run_minecraft():
            version = "1.20.1"
            forge_version = mc_lib.forge.find_forge_version(version)
            forge_vers = mc_lib.forge.forge_to_installed_version(forge_version)
            minecraft_directory = os.path.join(self.mc_dir, "DGRMClauncher")
            os.makedirs(minecraft_directory, exist_ok=True)
            # Получение команды для запуска Minecraft
            command = mc_lib.command.get_minecraft_command(
                version=forge_vers,
                minecraft_directory=minecraft_directory,
                options=self.user_data,
            )

            try:
                self.set_status("Запуск Minecraft...")
                subprocess.call(command)
                self.set_status("Minecraft запущен!")
            except Exception as e:
                self.set_status(f"Ошибка при запуске: {e}")

        # Запуск Minecraft в отдельном потоке
        thread = threading.Thread(target=run_minecraft, daemon=True)
        thread.start()

    def delete_mc(self):
        try:
            shutil.rmtree(os.path.join(self.mc_dir, "DGRMClauncher"))
            self.delete_complete.emit()
        except Exception as e:
            ic(f"Error: {e}")
