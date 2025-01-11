import shutil
import os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QSpinBox, QLabel, QPushButton, QWidget
)
from PySide6.QtCore import Qt, Signal
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
                font-size: 55px;
                color: #cb92e5;
            }
        """)

        self.go_back_button = QPushButton("BACK")
        self.go_back_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                color: #cb92e5;
                font-weight: bold;
                border: 2px solid #cb92e5;
                border-radius: 20px;
                font-size: 24px;
                min-height: 40px; 
                max-height: 100px;
                min-width: 100px;
                max-width: 600px;
            }
            QPushButton:hover {
                color: #e2a1ff;
                border: 2px solid #e2a1ff;
            }
        """)
        self.go_back_button.clicked.connect(self.emit_signal)

        # Minimum RAM spin box
        self.min_label = QLabel("Minimum RAM (MiB):")
        self.min_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #cb92e5;
            }
        """)

        self.min_spinbox = QSpinBox()
        self.min_spinbox.setMinimum(512)
        self.min_spinbox.setMaximum(32768)
        self.min_spinbox.setValue(512)
        self.min_spinbox.setSingleStep(128)

        # Maximum RAM spin box
        self.max_label = QLabel("Maximum RAM (MiB):")
        self.max_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #cb92e5;
            }
        """)

        self.max_spinbox = QSpinBox()
        self.max_spinbox.setMinimum(512)
        self.max_spinbox.setMaximum(32768)
        self.max_spinbox.setValue(2048)
        self.max_spinbox.setSingleStep(128)

        # Button to display JVM arguments
        self.generate_button = QPushButton("Generate JVM Arguments (Save)")
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
                color: #cb92e5;
                font-weight: bold;
                border: 2px solid #cb92e5;
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
                color: #cb92e5;
                font-weight: bold;
                border: 2px solid #cb92e5;
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
                color: #cb92e5;
                font-weight: bold;
                border: 2px solid #cb92e5;
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

        # Label to show generated JVM arguments
        self.output_label = QLabel("")
        self.output_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #cb92e5;
            }
        """)
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_label.setWordWrap(True)

        self.go_back_button.setFont(self.custom_font_label)
        self.title_label.setFont(self.custom_font_label)
        self.change_profile_button.setFont(self.custom_font_label)
        self.check_updates_button.setFont(self.custom_font_label)
        self.delete_button.setFont(self.custom_font_label)
        self.output_label.setFont(self.custom_font_label)
        self.generate_button.setFont(self.custom_font_label)

        # Add widgets to layout
        self.glavnaya_layout.addWidget(self.go_back_button, alignment=Qt.AlignRight)
        self.glavnaya_layout.addWidget(self.title_label, alignment=Qt.AlignTop)
        self.glavnaya_layout.addWidget(self.min_label, alignment=Qt.AlignCenter)
        self.glavnaya_layout.addWidget(self.min_spinbox, alignment=Qt.AlignCenter)
        self.glavnaya_layout.addWidget(self.max_label, alignment=Qt.AlignCenter)
        self.glavnaya_layout.addWidget(self.max_spinbox, alignment=Qt.AlignCenter)
        self.glavnaya_layout.addWidget(self.change_profile_button, alignment=Qt.AlignCenter)
        self.glavnaya_layout.addWidget(self.check_updates_button, alignment=Qt.AlignCenter)
        self.glavnaya_layout.addWidget(self.delete_button, alignment=Qt.AlignCenter)
        self.glavnaya_layout.addWidget(self.generate_button, alignment=Qt.AlignCenter)
        self.glavnaya_layout.addWidget(self.output_label, alignment=Qt.AlignCenter)

        # Основной лейаут страницы
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.glavnaya)
        self.setLayout(layout)

    def emit_signal(self):
        ic("settings button clicked")
        self.go_back.emit()

    def generate_jvm_arguments(self):
        min_ram = self.min_spinbox.value()
        max_ram = self.max_spinbox.value()

        if min_ram > max_ram:
            self.output_label.setText("Error: Minimum RAM cannot be greater than Maximum RAM.")
        else:
            jvm_args = f"-Xms{min_ram}M -Xmx{max_ram}M"
            self.output_label.setText(f"JVM Arguments: {jvm_args}")

    def delete_mc(self):
            try:
                shutil.rmtree(os.path.join(self.mc_dir, "DGRMClauncher"))
                self.delete_complete.emit()
            except Exception as e:
                ic(f"Error: {e}")