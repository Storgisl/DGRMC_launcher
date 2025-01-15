import shutil
import psutil
import os

from PySide6.QtWidgets import (
    QVBoxLayout, QSlider, QLabel, QPushButton
)
from PySide6.QtGui import QFontDatabase, QFont, QColor, \
    QIcon
from PySide6.QtCore import Qt, QSize, Signal, QPropertyAnimation, QEasingCurve
from icecream import ic

from .page import Page


class SettingsPage(Page):
    go_back = Signal()
    delete_complete = Signal()

    def __init__(self):
        super().__init__()

    def initUI(self):
        super().initUI()

        self.title_label = QLabel(f"SETTINGS")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                font-size: 55px;
                color: #cb92e5;
                padding: 0;
                margin: 0;
                text-align: center;
                vertical-align: middle;
                margin-top: -20px;
            }
        """)

        self.go_back_button = QPushButton("") #background-color: rgba(0, 0, 0, 0);
        self.go_back_button.setIcon(QIcon('assets/back.svg'))
        self.settings_button.setIconSize(QSize(48, 48))
        self.settings_button.setFixedSize(80, 80)
        self.settings_button.setStyleSheet("border: none;")
        self.settings_button.setGeometry(150, 150, 200, 200)
        self.go_back_button.setStyleSheet("""
            QPushButton {
                background-color: red;
            }
        """)
        self.go_back_button.clicked.connect(self.emit_signal)

        # Получение максимального объёма оперативной памяти
        self.max_ram = self.get_max_system_ram()
        self.min_label = QLabel("RAM (MiB):")
        self.min_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                background-color: red;
                color: #cb92e5;
                padding: 0;
            }
        """)

        # Слайдер для выбора минимальной оперативной памяти
        self.min_slider = QSlider(Qt.Horizontal)
        self.min_slider.setMinimum(2048)
        self.min_slider.setMaximum(self.max_ram)
        self.min_slider.setValue(2048)
        self.min_slider.setSingleStep(512)
        self.min_slider.setStyleSheet("""
            QSlider {
                height: 12px;
                width: 520px;
                background: #333333;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: #cb92e5;
                border: 2px solid #8f4e96;
                width: 20px;
                height: 20px;
                border-radius: 5px;
                margin-top: -4px; /* Позиционирование ручки */
                margin-bottom: -4px;
                margin-left: -40px;
            }
            QSlider::handle:horizontal:hover {
                background: #e2a1ff;
            }
            QSlider::add-page:horizontal {
                background: #e2a1ff;
                border-radius: 5px;
            }
            QSlider::sub-page:horizontal {
                background: #8f4e96;
                border-radius: 5px;
            }
        """)

        # Метка для отображения текущего значения
        self.value_label = QLabel(f"Selected: {self.min_slider.value()} MiB")
        self.value_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #e2a1ff;
            }
        """)

        # Подключение изменения значения слайдера к обновлению метки
        self.min_slider.valueChanged.connect(self.update_value)

        # Button to display JVM arguments
        self.generate_button = QPushButton("Save")
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                color: #cb92e5;
                font-weight: bold;
                border: 2px solid #cb92e5;
                border-radius: 20px;
                font-size: 24px;
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
        self.generate_button.clicked.connect(self.generate_jvm_arguments)

        # Change profile
        self.change_profile_button = QPushButton("CHANGE ACCOUNT")
        self.change_profile_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                color: #D4C0D0;
                font-weight: bold;
                border: 2px solid #D4C0D0;
                border-radius: 20px;
                font-size: 24px;
                min-height: 40px; 
                max-height: 100px;
                min-width: 300px;
                max-width: 600px;
            }
            QPushButton:hover {
                color: #e2a1ff;
                border: 2px solid #e2a1ff;
            }
        """)

        # Check updates
        self.check_updates_button = QPushButton("CHECK FOR UPDATES")
        self.check_updates_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                color: #D4C0D0;
                font-weight: bold;
                border: 2px solid #D4C0D0;
                border-radius: 20px;
                font-size: 24px;
                min-height: 40px; 
                max-height: 100px;
                min-width: 300px;
                max-width: 600px;
            }
            QPushButton:hover {
                color: #e2a1ff;
                border: 2px solid #e2a1ff;
            }
        """)

        # Кнопка для удаления Minecraft (перекинуть в настройки)
        self.delete_button = QPushButton("DELETE MINECRAFT")
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                color: #D4C0D0;
                font-weight: bold;
                border: 2px solid #D4C0D0;
                border-radius: 20px;
                font-size: 24px;
                min-height: 40px; 
                max-height: 100px;
                min-width: 300px;
                max-width: 600px;
            }
            QPushButton:hover {
                color: #e2a1ff;
                border: 2px solid #e2a1ff;
            }
        """)
        self.delete_button.clicked.connect(self.delete_mc)

        self.go_back_button.setFont(self.custom_font_label)
        self.title_label.setFont(self.custom_font_label)
        self.change_profile_button.setFont(self.custom_font_label)
        self.check_updates_button.setFont(self.custom_font_label)
        self.delete_button.setFont(self.custom_font_label)
        self.generate_button.setFont(self.custom_font_label)
        self.min_label.setFont(self.custom_font_label)
        self.min_slider.setFont(self.custom_font_label)
        self.value_label.setFont(self.custom_font_label)

        # Add widgets to layout
        self.glavnaya_layout.addWidget(self.go_back_button, alignment=Qt.AlignLeft)
        self.glavnaya_layout.addWidget(self.title_label, alignment=Qt.AlignTop)
        self.glavnaya_layout.addWidget(self.min_label, alignment=Qt.AlignLeft)
        self.glavnaya_layout.addWidget(self.min_slider, alignment=Qt.AlignCenter)
        self.glavnaya_layout.addWidget(self.value_label, alignment=Qt.AlignCenter)
        self.glavnaya_layout.addWidget(self.change_profile_button, alignment=Qt.AlignCenter)
        self.glavnaya_layout.addWidget(self.check_updates_button, alignment=Qt.AlignCenter)
        self.glavnaya_layout.addWidget(self.delete_button, alignment=Qt.AlignCenter)
        self.glavnaya_layout.addWidget(self.generate_button, alignment=Qt.AlignBottom)

        # Основной лейаут страницы
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.glavnaya)
        self.setLayout(layout)

    def update_value(self, value):
        """Обновление метки с текущим значением."""
        max_ram = self.get_max_system_ram()
        self.value_label.setText(f"Selected: {value}/{max_ram} MiB")

    def get_max_system_ram(self):
        """Возвращает общий объём оперативной памяти в MiB."""
        total_ram = psutil.virtual_memory().total  # Получение общей памяти в байтах
        return total_ram // (1024 * 1024)  # Конвертация в Mi

    def emit_signal(self):
        ic("settings button clicked")
        self.go_back.emit()

    def generate_jvm_arguments(self):
        min_ram = self.min_slider.value()
        max_ram = self.max_ram
        pass
        # if min_ram > max_ram:
        #     self.output_label.setText("Error: Minimum RAM cannot be greater than Maximum RAM.")
        # else:
        #     jvm_args = f"-Xms{min_ram}M -Xmx{max_ram}M"
        #     self.output_label.setText(f"JVM Arguments: {jvm_args}")

    def delete_mc(self):
            try:
                shutil.rmtree(os.path.join(self.mc_dir, "DGRMClauncher"))
                self.delete_complete.emit()
            except Exception as e:
                ic(f"Error: {e}")