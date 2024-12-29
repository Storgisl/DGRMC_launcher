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

import os
import subprocess
import platform
import threading
import minecraft_launcher_lib as mc_lib

from data import save_user_data, load_user_data
from exceptions import UserDataException, UserDirException, UserOptionsException, CustomException

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
        self.background_image = QPixmap("back.png")  # Кэшируем изображение
        if not self.background_image or self.background_image.isNull():
            print("Ошибка: Изображение back.png не найдено или повреждено")


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
        self.username_var = QLineEdit()
        self.password_var = QLineEdit()
        self.uuid_var = ""
        self.token_var = ""
        self.mc_dir = ""

        # Пути к JSON файлам
        self.user_data_json = "user_data.json"
        self.user_options_json = "user_options.json"

        # Получаем директорию конфигурации в зависимости от операционной системы
        if platform.system() == "Windows":
            self.config_dir = os.path.join(os.getenv("LOCALAPPDATA"), "DGRMC_Launcher")
        else:
            self.config_dir = os.path.expanduser("~/.dgrmc_launcher")

        # Проверяем, существует ли директория, если нет — создаем
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        # Загружаем данные из JSON файлов, если они существуют
        self.user_data = {}
        self.user_options = {}

        if not os.path.exists(os.path.join(self.config_dir, self.user_data_json)):
            self.user_data = {}
            self.user_options = {}
        else:
            self.user_data = load_user_data(directory=self.config_dir, json_file=self.user_data_json)
            self.user_options = load_user_data(directory=self.config_dir, json_file=self.user_options_json)

        # Инициализация переменной mc_dir
        self.mc_dir = self.user_data.get("mc_dir", "")

        # Логирование для отладки
        print(self.user_data)
        print(self.user_options)
        print(self.mc_dir)
        print(self.user_data.get("username"))
        print(self.password_var)
    
    #  pages setup
    def setupWidgets(self) -> None:
        # Создаем QStackedWidget для переключения между страницами
        self.stacked_widget = QStackedWidget()

        # Создаем страницы и добавляем их в stacked_widget
        self.registration_page = RegistrationPage(self, self.username_var, self.password_var, self.user_data_json, self.config_dir)
        self.login_page = LoginPage()
        self.download_page = DownloadPage(self, self.config_dir, self.user_data)
        self.main_page = MainPage()
        self.settings_page = SettingsPage()

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
            if not self.user_data.get("username") or not self.user_data.get("password"):
                self.show_registration_frame()
            else:
                self.username_var = self.user_data.get("username", "")
                self.password_var = self.user_data.get("password", "")
                self.show_download_frame()

        except Exception as e:
            # Обработка ошибок
            print(f"Error: {e}")
            self.show_registration_frame()

        # Если есть логин, пароль и директория, отображаем основной фрейм
        if self.user_data.get("username") and self.user_data.get("password") and self.user_data.get("mc_dir"):
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
class RegistrationPage(QWidget):
    def __init__(self, launcher, username_var, password_var, user_data_json, config_dir, parent=None):
        super().__init__(parent)
        self.launcher = launcher 
        # Используем переданные параметры
        self.username_var = username_var
        self.password_var = password_var
        self.user_data_json = user_data_json
        self.config_dir = config_dir

        # Поле для вывода ошибок
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")

        # Кнопки
        self.register_button = QPushButton("ENTER")
        self.register_button.clicked.connect(self.handle_registration)

        self.already_registered_button = QPushButton("I'm already registered")
        self.already_registered_button.clicked.connect(self.handle_already_registered)

        # Заголовок
        self.title_label = QLabel("REGISTRATION")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Установим стиль для кнопки "ENTER"
        self.register_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.already_registered_button.setStyleSheet("background-color: #f44336; color: white;")

        # Создаем компоновку
        layout = QVBoxLayout()
        
        # Добавляем виджеты
        layout.addWidget(self.title_label)
        layout.addWidget(self.username_var)
        layout.addWidget(self.password_var)
        layout.addWidget(self.register_button)
        layout.addWidget(self.already_registered_button)
        layout.addWidget(self.error_label)

        # Устанавливаем layout для текущего виджета
        self.setLayout(layout)

    def handle_registration(self) -> None:
        username = self.username_var.text() ####
        password = self.password_var.text()

        # Проверка данных для регистрации
        if username and password:
            print(f"Регистрация прошла успешно: {username}")
            self.user_data = {"username": username, "password": password}
            save_user_data(
                new_data=self.user_data,
                directory=self.config_dir,
                json_file=self.user_data_json
            )
            self.launcher.show_download_frame()
        else:
            self.show_error("Заполните все поля.")
        self.handle_options()
    
    def handle_already_registered(self):
        print("User already registered. Redirecting to login...")
        self.launcher.show_login_frame()

    def show_error(self, message: str) -> None:
        """Показать ошибку на экране регистрации."""
        if not self.error_label:
            self.error_label = QLabel()
            self.error_label.setStyleSheet("color: red;")
            self.layout().addWidget(self.error_label)

        self.error_label.setText(message)

    def handle_options(self) -> None:
        username = self.username_var.text()

        self.user_options = {"username": username}

        save_user_data(
            new_data=self.user_options,
            directory=self.config_dir,
            json_file=self.user_options_json
        )
        self.launcher.show_main_frame()

#===================================================================================================================
# LOGIN FRAME
#===================================================================================================================

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Login"))
        self.setLayout(layout)

#===================================================================================================================
# DOWNLOAD FRAME
#===================================================================================================================

class DownloadPage(QWidget):
    # Сигналы для обновления GUI из потоков
    set_status_signal = Signal(str)
    set_progress_signal = Signal(int)
    set_max_signal = Signal(int)
    switch_to_main_page_signal = Signal()  # Сигнал для переключения на MainPage

    def __init__(self, launcher, config_dir, user_data):
        super().__init__()
        self.launcher = launcher 
        self.config_dir = config_dir
        self.user_data = user_data

        # Главный лейаут
        layout = QVBoxLayout()

        # Кнопка выбора директории
        self.choose_dir_button = QPushButton("Choose Directory")
        self.choose_dir_button.clicked.connect(self.choose_directory)
        layout.addWidget(self.choose_dir_button)

        # Метка для отображения выбранной директории
        self.directory_label = QLabel("Directory not chosen")
        layout.addWidget(self.directory_label)

        # Кнопка для установки Minecraft
        self.install_mc_button = QPushButton("Install Minecraft")
        self.install_mc_button.clicked.connect(lambda: self.install_mc(self.directory_label.text()))
        layout.addWidget(self.install_mc_button)

        # Кнопка для установки Forge
        self.install_forge_button = QPushButton("Install Forge")
        self.install_forge_button.clicked.connect(lambda: self.install_forge(self.directory_label.text()))
        layout.addWidget(self.install_forge_button)

        # Прогресс-бар и метка статуса
        self.progress_label = QLabel("Status: Waiting")
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)

        # Устанавливаем лейаут для текущего виджета
        self.setLayout(layout)

        # Подключение сигналов к методам обновления интерфейса
        self.set_status_signal.connect(self.set_status)
        self.set_progress_signal.connect(self.set_progress)
        self.set_max_signal.connect(self.set_max)
        self.switch_to_main_page_signal.connect(self.show_main_page)

    def choose_directory(self) -> None:
        mc_dir = QFileDialog.getExistingDirectory(self, "Choose Minecraft Directory")
        if mc_dir:
            self.directory_label.setText(mc_dir)
            print(f"Selected directory: {mc_dir}")
        else:
            self.directory_label.setText("Directory not chosen")
            print("No directory chosen!")

    def install_mc(self, mc_dir: str) -> None:
        if not mc_dir or mc_dir == "Directory not chosen":
            self.progress_label.setText("Please choose a directory first!")
            return

        def installation_task():
            version = "1.20.1"
            minecraft_directory = os.path.join(mc_dir, "DGRMClauncher")
            os.makedirs(minecraft_directory, exist_ok=True)

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
                # После завершения установки Minecraft, генерируем сигнал для перехода на MainPage
                self.switch_to_main_page_signal.emit()  # Это вызовет переключение на MainPage

            except Exception as e:
                print(f"Error during installation: {e}")
                self.set_status_signal.emit("Installation failed. Please try again.")

        # Запуск установки Minecraft в отдельном потоке
        thread = threading.Thread(target=installation_task, daemon=True)
        thread.start()

    def install_forge(self, mc_dir: str) -> None:
        if not mc_dir or mc_dir == "Directory not chosen":
            self.progress_label.setText("Please choose a directory first!")
            return

        def forge_task():
            vanilla_version = "1.20.1"
            minecraft_directory = mc_lib.utils.get_minecraft_directory()
            forge_version = mc_lib.forge.find_forge_version(vanilla_version)
            if mc_lib.forge.supports_automatic_install(forge_version):
                callback = {"setStatus": lambda text: self.set_status_signal.emit(text)}
                mc_lib.forge.install_forge_version(forge_version, path=minecraft_directory, callback=callback)
            else:
                print(f"Forge {forge_version} can't be installed automatically.")
                mc_lib.forge.run_forge_installer(forge_version)

        # Запуск установки Forge в отдельном потоке
        thread = threading.Thread(target=forge_task, daemon=True)
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

    def show_main_page(self):
        """Переключаемся на MainPage в основном потоке"""
        self.launcher.show_main_frame()

#===================================================================================================================
# MAIN FRAME
#===================================================================================================================

class MainPage(QWidget):
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
            minecraft_directory = os.path.join(mc_dir, "DGRMClauncher")
            
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
