import platform
import os
import sys

from pathlib import Path

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtGui import QFont, QFontDatabase, QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Signal, Qt, QRectF
from icecream import ic

from manip_data import DataManip


class Page(QWidget):
    settings_clicked = Signal()
    go_to_main_page = Signal()
    go_to_download_page = Signal()

    def __init__(self):
        super().__init__()
        self.background_image = QPixmap("assets/Back.png")
        if not self.background_image or self.background_image.isNull():
            print("Ошибка: Изображение back.png не найдено или повреждено")
        self.data_manip = DataManip()

        if platform.system() == "Windows":
            self.config_dir = os.path.join(os.getenv("LOCALAPPDATA"), "DGRMC_Launcher")
        else:
            self.config_dir = os.path.expanduser("~/.dgrmc_launcher")

        os.makedirs(self.config_dir, exist_ok=True)
        self.user_data_json = "user_data.json"
        self.user_options_json = "user_options.json"
        self.user_data = self.data_manip.load_user_data(
            directory=self.config_dir, json_file=self.user_data_json
        )
        self.user_options = self.data_manip.load_user_data(
            directory=self.config_dir, json_file=self.user_options_json
        )
        self.current_username_var = self.user_options.get("username", "")
        self.username_var = None

        ic(self.username_var)
        ic(self.current_username_var)

        self.password_var = None
        self.mc_dir = self.user_options.get("mc_dir", "")
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.uuid_var = ""
        self.token_var = ""
        self.initUI()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Создаем маску с закругленными углами
        path = QPainterPath()
        rect = QRectF(self.rect())
        path.addRoundedRect(rect, 8, 8)  # Закругляем углы на 8px

        # Ограничиваем область рисования маской
        painter.setClipPath(path)

        # Рисуем фоновую картинку
        scaled_image = self.background_image.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding
        )
        painter.drawPixmap(0, 0, scaled_image)

        # Убираем маску для последующих рисований
        painter.setClipping(False)

    def initUI(self):
        self.regular_font_id = QFontDatabase.addApplicationFont(
            "assets/Heebo-Regular.ttf"
        )
        self.medium_font_id = QFontDatabase.addApplicationFont(
            "assets/Heebo-Medium.ttf"
        )
        self.light_font_id = QFontDatabase.addApplicationFont("assets/Heebo-Light.ttf")
        self.bold_font_id = QFontDatabase.addApplicationFont("assets/Heebo-Bold.ttf")
        self.extra_light_font_id = QFontDatabase.addApplicationFont(
            "assets/Heebo-ExtraLight.ttf"
        )
        if self.regular_font_id == -1:
            print("Ошибка: Не удалось загрузить Heebo-Regular.ttf")
        if self.medium_font_id == -1:
            print("Ошибка: Не удалось загрузить Heebo-Medium.ttf")
        if self.light_font_id == -1:
            print("Ошибка: Не удалось загрузить Heebo-Light.ttf")
        if self.bold_font_id == -1:
            print("Ошибка: Не удалось загрузить Heebo-Bold.ttf")
        if self.extra_light_font_id == -1:
            print("Ошибка: Не удалось загрузить Heebo-ExtraLight.ttf")

        self.regular_font = QFont(
            QFontDatabase.applicationFontFamilies(self.regular_font_id)[0]
        )
        self.medium_font = QFont(
            QFontDatabase.applicationFontFamilies(self.medium_font_id)[0]
        )
        self.light_font = QFont(
            QFontDatabase.applicationFontFamilies(self.light_font_id)[0]
        )
        self.bold_font = QFont(
            QFontDatabase.applicationFontFamilies(self.bold_font_id)[0]
        )
        self.extra_light_font = QFont(
            QFontDatabase.applicationFontFamilies(self.extra_light_font_id)[0]
        )

        # Footer
        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(40, 0, 40, 0)
        self.made_by_label = QLabel("Made by Kivaari", self)
        self.made_by_label.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                font-weight: 200;
                color: rgba(255, 255, 255, 20);
            }
        """
        )
        self.made_by_label.setFont(self.extra_light_font)
        self.footer_layout.addWidget(self.made_by_label, alignment=Qt.AlignCenter)

    def download_status(self) -> bool:
        dgrmc_dir = str(Path(self.mc_dir) / "DGRMClauncher")
        required_folders = [
            "assets",
            "libraries",
            "runtime",
            "versions",
            "emotes",
            "mods",
        ]
        if self.check_dirs(directory=dgrmc_dir, folders=required_folders):
            ic(dgrmc_dir)
            return True
        else:
            if (
                dgrmc_dir is False
                and self.current_user_var not in ("", None)
                and self.password_var not in ("", None)
            ):
                return False
            else:
                ic(
                    f"Missing required folders in {self.current_username_var, self.password_var, dgrmc_dir}"
                )
                return False

    def user_status(self, username: str) -> bool:
        user_info = self.user_data.get(username, {})
        password = user_info.get("password", "")

        return bool(password)

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

    def login_user(self, username: str) -> None:
        self.get_current_user(username=username)
        if self.download_status():
            self.go_to_main_page.emit()
        else:
            self.go_to_download_page.emit()

    def get_current_user(self, username: str) -> None:
        self.current_username_var = username
        ic(self.current_username_var)
        self.data_manip.save_user_data(
            new_data={"username": self.current_username_var},
            directory=self.config_dir,
            json_file=self.user_options_json,
        )

    def emit_signal(self, signal: Signal) -> None:
        signal.emit()
