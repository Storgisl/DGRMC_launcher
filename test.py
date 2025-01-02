#==============================================================
# Крч как я думаю надо сделать так,
# добавить запись пути к майнкрафту в json
# например в юзер дату и через получение пути
# запускать майн.
# Я переход на мейн скрин сдеал после установки.
# Мб придется сделать так чтобы майн после скачки запукался
# после загрузки закрывался и начиналась установка форджа
# после релоад лаунчера и все можно бегать.

# Как вариант чтобы после полноценной установки майна с форджем
# изменялись параметры запуска майнкрафта, чтобы чел сразу на
# сервак конектился.

# Взаимодействия с серверной бд (MySQL) доделаем на днях)
#===============================================================
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QSlider, QFileDialog, QProgressBar
from PySide6.QtCore import Qt, QJsonDocument, QFile, QIODevice, Signal, QObject, QThread
from PySide6.QtGui import QPainter, QPixmap
from icecream import ic

import os
import time
import subprocess
import platform
import threading
import minecraft_launcher_lib as mc_lib

from data import save_user_data, load_user_data
from exceptions import UserDataException, UserDirException, UserOptionsException, CustomException

from dataclasses import dataclass
#===================================================================================================================
# MAIN LAUNCHER CLASS
#===================================================================================================================


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupWindow()
        self.initialize_variables()
        self.setupWidgets()
        self.check_user_status()
        self.check_download_status()
        self.background_image = QPixmap("back.png")  # Кэшируем изображение
        if not self.background_image or self.background_image.isNull():
            print("Ошибка: Изображение back.png не найдено или повреждено")
        self.registration_page.registration_complete.connect(self.on_registration_complete)
        self.download_page.download_complete.connect(self.on_download_complete)

    #  window setup
    def setupWindow(self) -> None:
        self.setWindowTitle("Danga Launcher <3")
        self.setFixedHeight(800)
        self.setFixedWidth(800)

    #  background setup
    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        try:
            scaled_image = self.background_image.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
            painter.drawPixmap(0, 0, scaled_image)
        finally:
            painter.end()

    #  variables setup
    def initialize_variables(self) -> None:
        # Инициализация UI компонентов
        self.progress_label = QLabel("Progress:")
        self.progress_slider = QSlider()

        # Инициализация переменных данных
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
        print("Registration completed. Switching to download frame...")
        self.show_download_frame()

    def on_download_complete(self):
        self.show_main_frame()

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

#===================================================================================================================
# REGISTRATION FRAME
#===================================================================================================================
class Page(QWidget):
    def __init__(self):
        super().__init__()
        if platform.system() == "Windows":
            self.config_dir = os.path.join(os.getenv("LOCALAPPDATA"), "DGRMC_Launcher")
        else:
            self.config_dir = os.path.expanduser("~/.dgrmc_launcher")
        self.user_data_json = "user_data.json"
        self.user_data = load_user_data(
            directory=self.config_dir,
            json_file=self.user_data_json
        )
        self.username_var = self.user_data.get("username", "")
        self.password_var = self.user_data.get("password", "")
        self.mc_dir = self.user_data.get("mc_dir", "")
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")

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
        self.register_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")

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
        if self.username_var not in ("", None) and self.password_var not in ("", None):
            return True
        else:
            return  False

    def show_error(self, message: str) -> None:
        """Показать ошибку на экране регистрации."""
        if not self.error_label:
            self.error_label = QLabel()
            self.error_label.setStyleSheet("color: red;")
            self.layout().addWidget(self.error_label)

        self.error_label.setText(message)
#===================================================================================================================
# LOGIN FRAME
#===================================================================================================================

class LoginPage(Page):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Login"))
        self.setLayout(layout)

#===================================================================================================================
# DOWNLOAD FRAME
#===================================================================================================================

class DownloadPage(Page):
    # Сигналы для обновления GUI из потоков
    set_status_signal = Signal(str)
    set_progress_signal = Signal(int)
    set_max_signal = Signal(int)
    download_complete = Signal()

    def __init__(self):
        super().__init__()

        # Главный лейаут
        layout = QVBoxLayout()

        # Кнопка выбора директории
        self.choose_dir_button = QPushButton("Choose Directory")
        self.choose_dir_button.clicked.connect(self.choose_directory)
        layout.addWidget(self.choose_dir_button)

        # Метка для отображения выбранной директории
        if self.mc_dir not in ("", None):
            self.directory_label = QLabel(self.mc_dir) 
        else: 
            self.directory_label = QLabel("Directory not choosen")
        layout.addWidget(self.directory_label)

        self.set_status_signal.connect(self.set_status)
        self.set_progress_signal.connect(self.set_progress)
        self.set_max_signal.connect(self.set_max)

        # Кнопка для установки Minecraft
        self.install_mc_button = QPushButton("Install Minecraft")
        self.install_mc_button.clicked.connect(lambda: self.install_mc(self.mc_dir))
        layout.addWidget(self.install_mc_button)

        # Кнопка для установки Forge
        # self.install_forge_button = QPushButton("Install Forge")
        # self.install_forge_button.clicked.connect(lambda: self.install_forge(self.mc_dir))
        # layout.addWidget(self.install_forge_button)

        # Прогресс-бар и метка статуса
        self.progress_label = QLabel("Status: Waiting")
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)

        # Устанавливаем лейаут для текущего виджета
        self.setLayout(layout)

    def choose_directory(self) -> None:
        mc_dir = QFileDialog.getExistingDirectory(self, "Choose Minecraft Directory")
        if mc_dir:
            self.directory_label.setText(mc_dir)
            print(f"Selected directory: {mc_dir}")
            save_user_data(
                    new_data={"mc_dir": mc_dir},
                    directory=self.config_dir,
                    json_file=self.user_data_json
            )
        else:
            self.directory_label.setText("Directory not chosen")
            print("No directory chosen!")

    def install_mc(self, mc_dir: str) -> None:
        if not self.mc_dir or self.mc_dir == "Directory not chosen":
            self.progress_label.setText("Please choose a directory first!")
            return

        def installation_task():
            version = "1.20.1"
            minecraft_directory = os.path.join(mc_dir, "DGRMClauncher")
            os.makedirs(minecraft_directory, exist_ok=True)

            max_retries = 3
            retry_delay = 1
            for attempt in range(max_retries):
                try:
                    mc_lib.install.install_minecraft_version(
                        versionid=version,
                        minecraft_directory=minecraft_directory,
                        callback={
                            "setStatus": lambda status: self.set_status_signal.emit(status),
                            "setProgress": lambda progress: self.set_progress_signal.emit(progress),
                            "setMax": lambda max_value: self.set_max_signal.emit(max_value),
                        }
                    )

                    forge_version = mc_lib.forge.find_forge_version(version)
                    if mc_lib.forge.supports_automatic_install(forge_version):
                        callback = {"setStatus": lambda text: self.set_status_signal.emit(text)}
                        mc_lib.forge.install_forge_version(forge_version, path=minecraft_directory, callback=callback)
                    else:
                        print(f"Forge {forge_version} can't be installed automatically.")
                        mc_lib.forge.run_forge_installer(forge_version)
                    self.download_complete.emit()
                    self.set_status_signal.emit("Installation completed successfully!")
                    break
                except Exception as e:
                    print(f"Error during installation attempt {attempt + 1}: {e}")
                    self.set_status_signal.emit(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")

                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                    else:
                        self.set_status_signal.emit("Installation failed after multiple attempts. Please try again.")


        # Starting installation task in a separate thread
        thread = threading.Thread(target=installation_task, daemon=True)
        thread.start()
    def set_status(self, status: str):
        """Метод для обновления статуса (вызывается через сигнал)"""
        self.progress_label.setText(f"Status: {status}")

    def set_progress(self, progress: int):
        """Метод для обновления прогресса (вызывается через сигнал)"""
        self.progress_bar.setValue(progress)

    def set_max(self, new_max: int):
        """Метод для установки максимума прогресс-бара (вызывается через сигнал)"""
        self.progress_bar.setMaximum(new_max)

    def check_dirs(self, directory: str, folders: list) -> bool:
        try:
            contents = os.listdir(directory)
            for folder in folders:
                if folder not in contents:
                    ic(f"folder '{folder}' is missing")
                    return False
            return True
        except FileNotFoundError:
            print(f"Directory '{directory}' not found.")
            return False

    def download_status(self) -> bool:
        dgrmc_dir = os.path.join(self.mc_dir, "DGRMClauncher")
        os.makedirs(dgrmc_dir, exist_ok=True)

        required_folders = ["assets", "libraries", "resourcepacks", "runtime", "saves", "versions"]
        if self.check_dirs(directory=dgrmc_dir, folders=required_folders):
           ic(dgrmc_dir)
           return True
        else:
           ic(f"Missing required folders in '{dgrmc_dir}'")
           return False
#===================================================================================================================
# MAIN FRAME
#===================================================================================================================

class MainPage(Page):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Кнопка для запуска Minecraft
        self.run_button = QPushButton("Запустить Minecraft")
        self.run_button.clicked.connect(self.run_mc)  # Связываем кнопку с функцией
        layout.addWidget(self.run_button)

        # Метка для отображения статуса
        self.status_label = QLabel("Статус: Готово")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def set_status(self, status: str):
        """Метод для обновления статуса на UI"""
        self.status_label.setText(f"Статус: {status}")

    def run_mc(self, mc_dir: str, options: dict = None) -> None:
        if options is None:
            options = {}  # Использовать пустой словарь, если options не передан

        def run_minecraft():
            version = "1.20.1"
            minecraft_directory = os.path.join(self.mc_dir, "DGRMClauncher")
            os.makedirs(minecraft_directory, exist_ok=True)
            # Получение команды для запуска Minecraft
            command = mc_lib.command.get_minecraft_command(
                version=version,
                minecraft_directory=minecraft_directory,
                options=options,
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

#===================================================================================================================
# SETTINGS FRAME
#===================================================================================================================

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Settings"))
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = Launcher()
    window.show()
    app.exec()
