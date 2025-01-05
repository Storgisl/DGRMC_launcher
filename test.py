from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QSlider, QFileDialog, QProgressBar
from PySide6.QtCore import Qt, QJsonDocument, QFile, QIODevice, Signal, QObject, QThread
from PySide6.QtGui import QPainter, QPixmap
from icecream import ic

import os
import shutil
import time
import subprocess
import platform
import threading
import minecraft_launcher_lib as mc_lib

from data import save_user_data, load_user_data
from exceptions import UserDataException, UserDirException, UserOptionsException, CustomException
from pages import 
from dataclasses import dataclass

class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupWindow()
        self.initialize_variables()
        self.setupWidgets()
        self.check_user_status()
        self.check_download_status()
        self.background_image = QPixmap("assets/back.png")
        if not self.background_image or self.background_image.isNull():
            print("Ошибка: Изображение back.png не найдено или повреждено")
        self.registration_page.registration_complete.connect(self.on_registration_complete)
        self.download_page.download_complete.connect(self.on_download_complete)
        self.main_page.delete_complete.connect(self.on_delete_complete)

    def setupWindow(self) -> None:
        self.setWindowTitle("Danga Launcher <3")
        self.setFixedHeight(800)
        self.setFixedWidth(800)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        try:
            scaled_image = self.background_image.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
            painter.drawPixmap(0, 0, scaled_image)
        finally:
            painter.end()

    def initialize_variables(self) -> None:
        self.progress_label = QLabel("Progress:")
        self.progress_slider = QSlider()

        self.uuid_var = ""
        self.token_var = ""

        # Пути к JSON файлам
        self.user_data_json = "user_data.json"

        if platform.system() == "Windows":
            self.config_dir = os.path.join(os.getenv("LOCALAPPDATA"), "DGRMC_Launcher")
        else:
            self.config_dir = os.path.expanduser("~/.dgrmc_launcher")
        os.makedirs(self.config_dir, exist_ok=True)
        # Загружаем данные из JSON файлов, если они существуют
        self.user_data = {}

        if not os.path.exists(os.path.join(self.config_dir, self.user_data_json)):
            self.user_data = {}
        else:
            self.user_data = load_user_data(directory=self.config_dir, json_file=self.user_data_json)

        # Инициализация переменной mc_dir
        self.mc_dir = self.user_data.get("mc_dir", "")

        # Логирование для отладки
        ic(self.user_data)

    def setupWidgets(self) -> None:
        # Создаем QStackedWidget для переключения между страницами
        self.stacked_widget = QStackedWidget()

        # Создаем страницы и добавляем их в stacked_widget
        self.registration_page = RegistrationPage()
        self.login_page = LoginPage()
        self.download_page = DownloadPage()
        self.main_page = MainPage()
        self.settings_page = SettingsPage()
        ic(self.registration_page.user_status())
        ic(self.download_page.download_status())
        self.stacked_widget.addWidget(self.registration_page)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.download_page)
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.settings_page)

        # Устанавливаем виджет как центральный
        self.setCentralWidget(self.stacked_widget)

        # Переключаемся на страницу регистрации (по умолчанию)
        self.stacked_widget.setCurrentWidget(self.registration_page)

    #  user checker
    def check_user_status(self) -> None:
        try:
            if self.registration_page.user_status() == True:
                self.show_download_frame()
            else:
                self.show_registration_frame()

        except Exception as e:
            # Обработка ошибок
            print(f"Error: {e}")
            self.show_registration_frame()

    def check_download_status(self) -> None:
        try:
            if self.download_page.download_status() == True:
                self.show_main_frame()
            else:
                if self.registration_page.user_status() == False:
                    self.show_registration_frame()
                else:
                    self.show_download_frame()
        except Exception as e:
                print(f"error {e}")


    def on_registration_complete(self):
        self.show_download_frame()

    def on_download_complete(self):
        self.show_main_frame()

    def on_delete_complete(self):
        self.show_download_frame()

    #  show registration frame
    def show_registration_frame(self):
        """Показать страницу регистрации"""
        self.clear_frames()
        self.stacked_widget.setCurrentWidget(self.registration_page)
        self.registration_page.show()

    #  show login frame
    def show_login_frame(self):
        """Показать страницу регистрации"""
        self.clear_frames()
        self.stacked_widget.setCurrentWidget(self.login_page)
        self.login_page.show()

    #  show settings frame
    def show_settings_frame(self):
        """Показать страницу регистрации"""
        self.clear_frames()
        self.stacked_widget.setCurrentWidget(self.settings_page)
        self.settings_page.show()

    #  show download frame
    def show_download_frame(self):
        """Показать страницу загрузки"""
        self.clear_frames()
        self.stacked_widget.setCurrentWidget(self.download_page)
        self.download_page.show()

    #  show main frame
    def show_main_frame(self):
        """Показать основную страницу"""
        self.clear_frames()
        self.stacked_widget.setCurrentWidget(self.main_page)
        self.main_page.show()

    #  clear frames
    def clear_frames(self) -> None:
        self.registration_page.hide()
        self.download_page.hide()
        self.main_page.hide()
        self.login_page.hide()
        self.settings_page.hide()


if __name__ == "__main__":
    app = QApplication([])
    window = Launcher()
    window.show()
    app.exec()
