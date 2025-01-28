import sys
import os
import time
import threading
import zipfile
import shutil

import minecraft_launcher_lib as mc_lib
import requests

from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QLabel,
    QProgressBar,
    QFrame,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Signal, Qt
from icecream import ic
from pathlib import Path

from .Page import Page


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
        self.frame.setStyleSheet(
            """
            QFrame {
                background-color: #412483;
                border-radius: 10px;
            }
        """
        )
        self.frame_layout = QVBoxLayout()
        self.frame_layout.setAlignment(
            Qt.AlignTop
        )  # Выравниваем элементы по верхней части фрейма
        self.frame_layout.setSpacing(
            10
        )  # Устанавливаем меньший отступ между элементами

        # Картинка
        text_image_label = QLabel(self)
        text_image_pixmap = QPixmap("assets/Text.png")
        text_image_label.setPixmap(text_image_pixmap)
        self.frame_layout.addWidget(
            text_image_label, alignment=Qt.AlignTop | Qt.AlignHCenter
        )

        # Добавляем небольшой отступ между картинкой и надписью
        top_spacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.frame_layout.addItem(top_spacer)

        label = QLabel("You are closer than you think", self)
        label.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                color: #7247CB;
            }
        """
        )
        label.setFont(self.light_font)
        self.frame_layout.addWidget(label, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # Кнопка Install
        self.install_mc_button = QPushButton("Install", self)
        self.install_mc_button.setStyleSheet(
            """
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
        """
        )
        self.install_mc_button.setFont(self.regular_font)
        self.install_mc_button.setCursor(Qt.PointingHandCursor)
        self.install_mc_button.clicked.connect(self.start_installation)
        self.frame_layout.addWidget(
            self.install_mc_button, alignment=Qt.AlignTop | Qt.AlignHCenter
        )

        # Метка с статусом
        self.progress_label = QLabel("Status: Waiting", self)
        self.progress_label.setFont(self.regular_font)
        self.progress_label.setVisible(False)  # Скрываем метку до начала установки

        # Прогресс-бар
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet(
            """
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
        """
        )
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
        self.frame_layout.addWidget(
            self.progress_bar, alignment=Qt.AlignTop | Qt.AlignHCenter
        )
        self.progress_label.setVisible(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setTextVisible(False)
        thread = threading.Thread(target=self.install_mc, daemon=True)
        thread.start()

    def install_forge(self) -> None:
        version = "1.20.1"
        mc_dir = os.path.join(self.mc_dir, "DGRMClauncher")
        forge_version = mc_lib.forge.find_forge_version(version)
        if mc_lib.forge.supports_automatic_install(forge_version):
            callback = {
                "setStatus": lambda status: self.set_status_signal.emit(status),
                "setProgress": lambda progress: self.set_progress_signal.emit(progress),
                "setMax": lambda max_value: self.set_max_signal.emit(max_value),
            }
            mc_lib.forge.install_forge_version(
                versionid=forge_version,
                path=mc_dir,
                callback=callback,
            )
        else:
            print(f"Forge {forge_version} can't be installed automatically.")
            mc_lib.forge.run_forge_installer(version=forge_version)
        self.download_complete.emit()
        self.set_status_signal.emit("Installation completed successfully!")

    def unzip_and_merge(self, zip_path: Path, target_dir: Path) -> None:
        """
        Unzip a file into the target directory and merge its contents with any existing files.
        Deletes the ZIP archive after extraction.

        Args:
            zip_path (Path): The path to the ZIP file.
            target_dir (Path): The directory where the contents will be extracted and merged.
        """
        try:
            # Ensure the target directory exists
            target_dir.mkdir(parents=True, exist_ok=True)

            # Open the ZIP file
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                for zip_info in zip_ref.infolist():
                    extracted_path = target_dir / zip_info.filename

                    if extracted_path.exists():
                        # If the file/folder already exists, merge them
                        if extracted_path.is_dir():
                            # Merge directories
                            temp_dir = target_dir / f"{zip_info.filename}_temp"
                            temp_dir.mkdir(parents=True, exist_ok=True)
                            zip_ref.extract(zip_info, temp_dir)
                            for item in temp_dir.iterdir():
                                dest = extracted_path / item.name
                                if item.is_file() and not dest.exists():
                                    shutil.move(item, dest)
                                elif item.is_dir():
                                    shutil.copytree(item, dest, dirs_exist_ok=True)
                            shutil.rmtree(temp_dir)
                        else:
                            # Skip or replace existing files
                            print(f"File {extracted_path} already exists. Skipping...")
                    else:
                        # Extract normally if no conflict
                        zip_ref.extract(zip_info, target_dir)
                zip_path.unlink()
            print(f"Extracted and merged contents of {zip_path.name} into {target_dir}")
        except Exception as e:
            print(f"Error during extraction and merge: {e}")

    def install_neccesary_files(self) -> None:
        """Download and install mods, resource packs, and emotes."""
        mc_dir = os.path.join(self.mc_dir, "DGRMClauncher")
        base_url = "https://github.com/Storgisl/dg_files/releases/download/v1.0/"

        def download_file(url: str, file_path: Path) -> None:
            """Download a file and update the progress bar."""
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                total_size = int(response.headers.get("content-length", 0))
                downloaded_size = 0

                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)
                            self.set_progress_signal.emit(
                                int((downloaded_size / total_size) * 100)
                            )

                print(f"{file_path.name} downloaded successfully!")
            else:
                print(f"Failed to download {file_path.name}")

        def install_mods() -> None:
            url = base_url + "mods.zip"
            file_path = Path(mc_dir) / "mods.zip"
            download_file(url=url, file_path=file_path)
            self.unzip_and_merge(zip_path=file_path, target_dir=Path(mc_dir) / "mods")

        def install_rpacks() -> None:
            url = base_url + "resourcepacks.zip"
            file_path = Path(mc_dir) / "resourcepacks.zip"
            download_file(url=url, file_path=file_path)
            self.unzip_and_merge(
                zip_path=file_path, target_dir=Path(mc_dir) / "resourcepacks"
            )

        def install_emotes() -> None:
            url = base_url + "emotes.zip"
            file_path = Path(mc_dir) / "emotes.zip"
            download_file(url=url, file_path=file_path)
            self.unzip_and_merge(zip_path=file_path, target_dir=Path(mc_dir) / "emotes")

        try:
            install_emotes()
        except Exception as e:
            print(f"error: {e}")

        try:
            install_rpacks()
        except Exception as e:
            print(f"error: {e}")

        try:
            install_mods()
        except Exception as e:
            print(f"error: {e}")

    def install_mc(self) -> None:
        mc_dir = os.path.join(self.mc_dir, "DGRMClauncher")
        os.makedirs(mc_dir, exist_ok=True)
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):
            try:
                self.install_forge()
                self.install_neccesary_files()
            except Exception as e:
                print(f"Error during installation attempt {attempt + 1}: {e}")
                self.set_status_signal.emit(
                    f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds..."
                )
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    self.set_status_signal.emit(
                        "Installation failed after multiple attempts. Please try again."
                    )

    def set_status(self, status: str):
        self.progress_label.setText(f"Status: \n {status}")

    def set_progress(self, progress: int):
        self.progress_bar.setValue(progress)

    def set_max(self, new_max: int):
        self.progress_bar.setMaximum(new_max)

    def on_download_complete(self):
        # Можно добавить дополнительные действия после завершения установки
        print("Installation complete!")
