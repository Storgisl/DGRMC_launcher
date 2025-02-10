import platform
import os

from pathlib import Path

from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Signal, Qt, QRectF
from icecream import ic

from Factory import LoggerFactory

# from Utils import PageStatusChecker
from DataManip import DataManip


class Page(QWidget):
    go_to_main_page = Signal()
    go_to_download_page = Signal()
    send_current_user = Signal(str)
    send_current_page = Signal(str)

    def __init__(self):
        super().__init__()
        from Utils import PageStatusChecker

        self.page_logger = LoggerFactory("Page").get_logger()
        self.page_logger.info(f"Page init")

        self.background_image = QPixmap("assets/Back.png")

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

        self.base_url = "https://github.com/Storgisl/dg_files/releases/download/v1.0/"
        self.password_var = None
        self.mc_dir = self.user_options.get("mc_dir", "")
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.uuid_var = ""
        self.token_var = ""
        self.status_checker = PageStatusChecker()
        self.download_status = self.status_checker.check_download_status()
        self.user_status = self.status_checker.check_user_status(
            self.current_username_var
        )
        ic(self.download_status)
        ic(self.user_status)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        rect = QRectF(self.rect())
        path.addRoundedRect(rect, 8, 8)
        painter.setClipPath(path)
        scaled_image = self.background_image.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding
        )
        painter.drawPixmap(0, 0, scaled_image)
        painter.setClipping(False)

    def login_user(self, username: str) -> None:
        self.get_current_user(username=username)
        self.emit_signal(self.send_current_user, username)
        if self.download_status:
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

    def emit_signal(self, signal, *args) -> None:
        ic(f"Emitting signal: {signal}, with args: {args}")
        signal.emit(*args)
