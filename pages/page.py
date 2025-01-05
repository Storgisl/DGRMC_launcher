import platform
import os

from PySide6.QtWidgets import QWidget, QLabel, QFrame, \
    QGraphicsDropShadowEffect, QVBoxLayout, QSlider
from PySide6.QtGui import QFontDatabase, QFont, QColor
from manip_data.load_user_data import load_user_data


class Page(QWidget):
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

        # Создаем эффект тени
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(1)  # Радиус размытия тени
        self.shadow_effect.setColor(QColor("#6D0088"))  # Цвет тени
        self.shadow_effect.setOffset(0, 0)  # Смещение тени

        # Применяем эффект к фрейму
        self.main_frame.setGraphicsEffect(self.shadow_effect)

        # Лейаут для фрейма
        self.frame_layout = QVBoxLayout(self.main_frame)
        self.frame_layout.setSpacing(15)

