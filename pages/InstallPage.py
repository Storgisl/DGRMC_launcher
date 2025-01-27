import sys
import os
import time
import threading
import minecraft_launcher_lib as mc_lib
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QProgressBar, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Signal, Qt
from icecream import ic
from .Page import Page
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class InstallPage(Page):
    set_status_signal = Signal(str)
    set_progress_signal = Signal(int)
    set_max_signal = Signal(int)
    download_complete = Signal()
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.setObjectName("install_page")
        self.stacked_widget = stacked_widget
        self.init_ui()
    
    def init_ui(self):
        # Центральная часть страницы
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Фрейм с размером 427x418
        self.frame = QFrame(self)
        self.frame.setFixedSize(427, 200)
        self.frame.setStyleSheet("""
            QFrame {
                background-color: #412483;
                border-radius: 10px;
            }
        """)
        self.frame_layout = QVBoxLayout()
        self.frame_layout.setAlignment(Qt.AlignTop)  # Выравниваем элементы по верхней части фрейма
        self.frame_layout.setSpacing(10)  # Устанавливаем меньший отступ между элементами
        
        # Картинка
        text_image_label = QLabel(self)
        text_image_pixmap = QPixmap("assets/Text.png")
        text_image_label.setPixmap(text_image_pixmap)
        self.frame_layout.addWidget(text_image_label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        # Добавляем небольшой отступ между картинкой и надписью
        top_spacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.frame_layout.addItem(top_spacer)
        
        label = QLabel("You are closer than you think", self)
        label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #7247CB;
            }
        """)
        label.setFont(self.light_font)
        self.frame_layout.addWidget(label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        # Кнопка Install
        self.install_mc_button = QPushButton("Install", self)
        self.install_mc_button.setStyleSheet("""
            QPushButton {
                background-color: #503684;
                color: #F0F0F0;
                font-size: 14px;
                border-radius: 8px;
                min-height: 30px;
                max-height: 30px;
                min-width: 150px;
                max-width: 150px;
            }
            QPushButton:hover {
                background-color: #7247CB;
            }
        """)
        self.install_mc_button.setFont(self.regular_font)
        self.install_mc_button.setCursor(Qt.PointingHandCursor)
        self.install_mc_button.clicked.connect(self.start_installation)
        self.frame_layout.addWidget(self.install_mc_button, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        # Метка с статусом
        self.progress_label = QLabel("Status: Waiting", self)
        self.progress_label.setFont(self.regular_font)
        self.progress_label.setVisible(False)  # Скрываем метку до начала установки
        
        # Прогресс-бар
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #503684;
                border-radius: 8px;
                height: 30px;
                width: 385px;
            }

            QProgressBar::chunk {
                background-color: #7247CB;
                border-radius: 8px;
            }

            QProgressBar::indicator {
                background-color: #7247CB;
                border-radius: 8px;
            }
        """)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setFont(self.regular_font)
        self.progress_bar.setVisible(False)
        
        self.frame.setLayout(self.frame_layout)
        main_layout.addWidget(self.frame, alignment=Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(self.navbar_frame)
        layout.addSpacing(110)
        layout.addLayout(main_layout)
        layout.addStretch()
        layout.addLayout(self.footer_layout)
        self.setLayout(layout)

        self.set_status_signal.connect(self.set_status)
        self.set_progress_signal.connect(self.set_progress)
        self.set_max_signal.connect(self.set_max)
        self.download_complete.connect(self.on_download_complete)
    
    def start_installation(self) -> None:
        self.frame_layout.removeWidget(self.install_mc_button)
        self.install_mc_button.deleteLater()

        self.frame_layout.addWidget(self.progress_bar, alignment=Qt.AlignTop | Qt.AlignHCenter)

        self.progress_label.setVisible(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setTextVisible(False)

        thread = threading.Thread(target=self.install_mc, args=(self.mc_dir,), daemon=True)
        thread.start()
    
    def install_mc(self, mc_dir: str) -> None:
        version = "1.20.1"
        #############################################################
        #minecraft_directory = os.path.join(mc_dir, "DGRMClauncher")#
        #############################################################
        os.makedirs(minecraft_directory, exist_ok=True)
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):
            try:
                forge_version = mc_lib.forge.find_forge_version(version)
                if mc_lib.forge.supports_automatic_install(forge_version):
                    callback = {
                        "setStatus": lambda status: self.set_status_signal.emit(status),
                        "setProgress": lambda progress: self.set_progress_signal.emit(progress),
                        "setMax": lambda max_value: self.set_max_signal.emit(max_value),
                    }
                    mc_lib.forge.install_forge_version(
                        versionid=forge_version,
                        path=minecraft_directory,
                        callback=callback
                    )
                else:
                    print(f"Forge {forge_version} can't be installed automatically.")
                    mc_lib.forge.run_forge_installer(version=forge_version)
                self.download_complete.emit()
                self.set_status_signal.emit("Installation completed successfully!")
            except Exception as e:
                print(f"Error during installation attempt {attempt + 1}: {e}")
                self.set_status_signal.emit(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    self.set_status_signal.emit("Installation failed after multiple attempts. Please try again.")
    
    def set_status(self, status: str):
        self.progress_label.setText(f"Status: \n {status}")
    
    def set_progress(self, progress: int):
        self.progress_bar.setValue(progress)
    
    def set_max(self, new_max: int):
        self.progress_bar.setMaximum(new_max)
    
    def on_download_complete(self):
        # Можно добавить дополнительные действия после завершения установки
        print("Installation complete!")