import platform
import os
import sys

from PySide6.QtWidgets import QWidget, QLabel, QFrame, \
    QGraphicsDropShadowEffect, QVBoxLayout, QSlider, \
    QPushButton
from PySide6.QtGui import QFontDatabase, QFont, QColor, \
    QIcon
from PySide6.QtCore import QSize, Signal, QPropertyAnimation, QEasingCurve
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
        self.progress_label = QLabel("Progress:")
        self.progress_slider = QSlider()
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")

        self.uuid_var = ""
        self.token_var = ""

        self.initUI()

    def initUI(self):
        # общая переменная для шрифта
        self.font_id = QFontDatabase.addApplicationFont("PatrickHandSC-Regular.ttf")
        if self.font_id == -1:
            print("Не удалось загрузить шрифт!")
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.custom_font_label = QFont(self.font_family)
        self.custom_font_label.setPointSize(64)
        self.custom_font_button = QFont(self.font_family)
        self.custom_font_button.setPointSize(64)

        # Основной фрейм для всех элементов
        self.main_frame = QFrame()
        self.main_frame.setFrameShape(QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.main_frame.setStyleSheet("""
            QFrame {
                background-color: #342F2F;
                border-radius: 50px;
                padding: 10px;
                height: 768px;
            }
        """)
        self.main_frame.setFixedSize(400, 500)

        # Фрейм для главной и настроек
        self.glavnaya = QFrame()
        self.glavnaya.setFrameShape(QFrame.StyledPanel)
        self.glavnaya.setFrameShadow(QFrame.Raised)
        self.glavnaya.setStyleSheet("""
            QFrame {
                background-color: #342F2F;
                border-radius: 50px;
                padding: 0px;
                height: 768px;
            }
        """)
        self.glavnaya.setFixedSize(600, 600)

        # Лейауты
        self.frame_layout = QVBoxLayout(self.main_frame)
        self.frame_layout.setSpacing(0)
        self.glavnaya_layout = QVBoxLayout(self.glavnaya)
        self.glavnaya_layout.setSpacing(0)

        # Общие кнопки
        self.settings_button = QPushButton('', self)
        self.settings_button.setIcon(QIcon('assets/settings.svg'))
        self.settings_button.setIconSize(QSize(48, 48))
        self.settings_button.setFixedSize(80, 80)
        self.settings_button.setStyleSheet("border: none;")
        self.settings_button.setGeometry(150, 150, 80, 80)

        # Сигналы для обработки событий
        self.settings_button.enterEvent = self.on_hover
        self.settings_button.leaveEvent = self.on_leave

        # Анимация
        self.animation = QPropertyAnimation(self.settings_button, b"iconSize")
        self.animation.setDuration(400)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)  # Плавность анимации

        self.settings_button.clicked.connect(self.emit_signal)
        self.settings_button.hide()

    def on_hover(self, event):
        """Меняем иконку при наведении."""
        self.settings_button.setIcon(QIcon('assets/settings_hover.svg'))
        self.animation.stop()
        self.animation.setStartValue(self.settings_button.iconSize())
        self.animation.setEndValue(QSize(64, 64))
        self.animation.start()

    def on_leave(self, event):
        """Возвращаем стандартную иконку."""
        self.settings_button.setIcon(QIcon('assets/settings.svg'))
        self.animation.stop()
        self.animation.setStartValue(self.settings_button.iconSize())
        self.animation.setEndValue(QSize(48, 48))
        self.animation.start()

    def emit_signal(self):
        ic("settings button clicked")
        self.settings_clicked.emit()

