import sys
import os
import time
import threading

import minecraft_launcher_lib as mc_lib

from PySide6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog, QLabel, \
    QProgressBar
from PySide6.QtCore import Signal, Qt
from icecream import ic

from .page import Page
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manip_data.save_user_data import save_user_data


class DownloadPage(Page):
    set_status_signal = Signal(str)
    set_progress_signal = Signal(int)
    set_max_signal = Signal(int)
    download_complete = Signal()

    def __init__(self):
        super().__init__()


    def initUI(self):
        super().initUI()

        self.title_label = QLabel("INSTALLATION")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 55px;
                color: #cb92e5;
                margin-bottom: -15px;
            }
        """)

        self.title_label.setFont(self.custom_font_label)
        self.choose_dir_button = QPushButton("CHOOSE DIRECTORY")
        self.choose_dir_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                color: #d4c0d0;
                font-weight: bold;
                font-size: 24px;
                border: 2px solid #d4c0d0;
                border-radius: 20px;
                margin-top: 20px;
                min-width: 280px;
                max-width: 400px;
                min-height: 40px;
                max-height: 100px;
            }
            QPushButton:hover {
                color: #e2a1ff;
                border: 2px solid #e2a1ff;
            }
        """)
        self.choose_dir_button.setFont(self.custom_font_button)
        self.choose_dir_button.clicked.connect(self.choose_directory)

        # Метка для отображения выбранной директории
        if self.mc_dir not in ("", None):
            self.directory_label = QLabel(self.mc_dir)
        else:
            self.directory_label = QLabel("DIRECTORY NOT CHOOSEN")
        self.directory_label.setFont(self.custom_font_button)
        self.directory_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #ff0000;
            }
        """)

        self.set_status_signal.connect(self.set_status)
        self.set_progress_signal.connect(self.set_progress)
        self.set_max_signal.connect(self.set_max)

        self.install_mc_button = QPushButton("INSTALL MINECRAFT")
        self.install_mc_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                color: #d4c0d0;
                font-weight: bold;
                font-size: 24px;
                border: 2px solid #d4c0d0;
                border-radius: 20px;
                margin-top: 20px;
                min-width: 280px;
                max-width: 400px;
                min-height: 40px;
                max-height: 100px;
            }
            QPushButton:hover {
                color: #e2a1ff;
                border: 2px solid #e2a1ff;
            }
        """)
        self.install_mc_button.setFont(self.custom_font_button)
        self.install_mc_button.clicked.connect(lambda: self.install_mc(
            mc_dir=self.mc_dir))

        self.progress_label = QLabel("Status: Waiting")
        self.progress_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #cb92e5;
                margin-bottom: -15px;
            }
        """)
        self.progress_label.setFont(self.custom_font_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(0, 0, 0, 0);
                border-radius: 20px;
                border: 2px solid #cb92e5;
                height: 40px;
                width: 280px;
                font-size: 20px;
            }

            QProgressBar::chunk {
                background-color: rgba(203, 146, 229, 80);
                color: #50368a;
                border-radius: 10px;
            }

            QProgressBar::indicator {
                background-color: #4CAF50;
            }

            QProgressBar::text {
                color: #d4c0d0;
                text-align: center;
                padding: 0px;
            }
        """)

        # Центрируем и устанавливаем нужный шрифт
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setFont(self.custom_font_button)

        self.frame_layout.addWidget(self.title_label, alignment=Qt.AlignTop)
        self.frame_layout.addWidget(self.choose_dir_button, alignment=Qt.AlignCenter)
        self.frame_layout.addWidget(self.directory_label, alignment=Qt.AlignCenter)
        self.frame_layout.addWidget(self.install_mc_button, alignment=Qt.AlignCenter)
        self.frame_layout.addWidget(self.progress_label, alignment=Qt.AlignCenter)
        self.frame_layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        # Основной лейаут страницы
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.main_frame)
        self.setLayout(layout)

    def choose_directory(self) -> None:
        mc_dir = QFileDialog.getExistingDirectory(self,
                                                  "Choose Minecraft Directory")
        if mc_dir:
            self.directory_label.setText(mc_dir)
            self.directory_label.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    color: #d4c0d0;
                }
            """)
            self.choose_dir_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0, 0, 0, 0);
                    color: #e2a1ff;
                    font-weight: bold;
                    font-size: 24px;
                    border: 2px solid #e2a1ff;
                    border-radius: 20px;
                    margin-top: 20px;
                    min-width: 280px;
                    max-width: 400px;
                    min-height: 40px;
                    max-height: 100px;
                }
            """)
            self.mc_dir = mc_dir
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
        if not self.mc_dir or self.mc_dir == "":
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
                    forge_version = mc_lib.forge.find_forge_version(version)
                    if mc_lib.forge.supports_automatic_install(forge_version):
                        callback = {
                            "setStatus":
                                lambda status: self.set_status_signal.emit(
                                    status
                                ),
                            "setProgress":
                                lambda progress: self.set_progress_signal.emit(
                                    progress
                                ),
                            "setMax":
                                lambda max_value: self.set_max_signal.emit(
                                    max_value
                                ),
                            }
                        mc_lib.forge.install_forge_version(
                            versionid=forge_version,
                            path=minecraft_directory,
                            callback=callback)
                    else:
                        print(f"Forge {forge_version} \
                        can't be installed automatically.")
                        mc_lib.forge.run_forge_installer(
                            version=forge_version
                        )

                    self.download_complete.emit()
                    self.set_status_signal.emit(
                        "Installation completed successfully!"
                    )

                except Exception as e:
                    print(f"Error during installation attempt \
                        {attempt + 1}: {e}")
                    self.set_status_signal.emit(
                        f"Attempt {attempt + 1} failed. \
                        Retrying in {retry_delay} seconds...")

                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                    else:
                        self.set_status_signal.emit(
                            "Installation failed after \
                            multiple attempts. Please try again.")

        # Starting installation task in a separate thread
        thread = threading.Thread(target=installation_task, daemon=True)
        thread.start()

    def set_status(self, status: str):
        """Метод для обновления статуса (вызывается через сигнал)"""
        self.progress_label.setText(f"Status: \n {status}")

    def set_progress(self, progress: int):
        """Метод для обновления прогресса (вызывается через сигнал)"""
        self.progress_bar.setValue(progress)

    def set_max(self, new_max: int):
        """Метод для установки максимума
        прогресс-бара (вызывается через сигнал)"""
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

        required_folders = ["assets", "libraries", "runtime", "versions"]
        if self.check_dirs(directory=dgrmc_dir, folders=required_folders):
            ic(dgrmc_dir)
            return True
        else:
            if (dgrmc_dir is False and self.username_var not in ("", None) and
                    self.password_var not in ("", None)):
                return True
            else:
                ic(f"Missing required folders in '{self.username_var, self.password_var,dgrmc_dir}'")
                return False
