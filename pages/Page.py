import platform
import os
import sys

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QFrame
from PySide6.QtGui import QFont, QFontDatabase, QPixmap
from PySide6.QtCore import Signal, Qt
from icecream import ic

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manip_data.load_user_data import load_user_data

class Page(QWidget):
    settings_clicked = Signal()

    def __init__(self):
        super().__init__()
        if platform.system() == "Windows":
            self.config_dir = os.path.join(os.getenv("LOCALAPPDATA"), "DGRMC_Launcher")
        else:
            self.config_dir = os.path.expanduser("~/.dgrmc_launcher")
        os.makedirs(self.config_dir, exist_ok=True)
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
        self.uuid_var = ""
        self.token_var = ""
        self.initUI()

    def initUI(self):
        self.regular_font_id = QFontDatabase.addApplicationFont("assets/Heebo-Regular.ttf")
        self.medium_font_id = QFontDatabase.addApplicationFont("assets/Heebo-Medium.ttf")
        self.light_font_id = QFontDatabase.addApplicationFont("assets/Heebo-Light.ttf")
        self.bold_font_id = QFontDatabase.addApplicationFont("assets/Heebo-Bold.ttf")
        self.extra_light_font_id = QFontDatabase.addApplicationFont("assets/Heebo-ExtraLight.ttf")
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
        self.regular_font = QFont(QFontDatabase.applicationFontFamilies(self.regular_font_id)[0])
        self.medium_font = QFont(QFontDatabase.applicationFontFamilies(self.medium_font_id)[0])
        self.light_font = QFont(QFontDatabase.applicationFontFamilies(self.light_font_id)[0])
        self.bold_font = QFont(QFontDatabase.applicationFontFamilies(self.bold_font_id)[0])
        self.extra_light_font = QFont(QFontDatabase.applicationFontFamilies(self.extra_light_font_id)[0])
    
        # Navbar
        self.navbar_layout = QHBoxLayout()
        self.navbar_layout.setContentsMargins(40, 0, 40, 0)  # Добавляем отступы слева и справа
        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap("assets/Logo.png")
        self.logo_label.setPixmap(self.logo_pixmap)
        self.navbar_layout.addWidget(self.logo_label, alignment=Qt.AlignLeft)
        self.version_label = QLabel("v2.1.1", self)
        self.version_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #F0F0F0;
                padding: 0;
                vertical-align: middle;
            }
        """)
        self.version_label.setFont(self.medium_font)
        self.navbar_layout.addWidget(self.version_label, alignment=Qt.AlignRight)
        self.navbar_frame = QFrame(self)
        self.navbar_frame.setLayout(self.navbar_layout)
        self.navbar_frame.setFixedHeight(44)

        # Footer
        self.footer_layout = QHBoxLayout()
        self.footer_layout.setContentsMargins(40, 0, 40, 0)
        self.made_by_label = QLabel("Made by Kivaari", self)
        self.made_by_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 200;
                color: rgba(255, 255, 255, 20);
            }
        """)
        self.made_by_label.setFont(self.extra_light_font)
        self.footer_layout.addWidget(self.made_by_label, alignment=Qt.AlignCenter)

    def emit_signal(self):
        ic("settings button clicked")
        self.settings_clicked.emit()
