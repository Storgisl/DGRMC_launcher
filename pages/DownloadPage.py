import sys
import os
import time
import threading
import subprocess
import zipfile
import shutil
import minecraft_launcher_lib as mc_lib
import requests
from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QFrame,
    QSpacerItem,
    QSizePolicy,
    QHBoxLayout
)
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtCore import Signal, Qt
from icecream import ic
from pathlib import Path
from .Page import Page

class DownloadPage(Page):
    set_status_signal = Signal(str)
    set_progress_signal = Signal(int)
    set_max_signal = Signal(int)
    download_complete = Signal()
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.setObjectName("download_page")
        self.stacked_widget = stacked_widget
        self.init_ui()
        
    def init_ui(self):
        # Navbar
        navbar_layout = QHBoxLayout()
        navbar_layout.setContentsMargins(
            40, 0, 40, 0
        )  # Добавляем отступы слева и справа
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("assets/Logo.png")
        logo_label.setPixmap(logo_pixmap)
        navbar_layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        version_label = QLabel("v2.1.1", self)
        version_label.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #F0F0F0;
                padding: 0;
                vertical-align: middle;
            }
        """
        )
        version_label.setFont(self.medium_font)
        navbar_layout.addWidget(version_label, alignment=Qt.AlignRight)
        navbar_frame = QFrame(self)
        navbar_frame.setLayout(navbar_layout)
        navbar_frame.setFixedHeight(44)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        frame = QFrame(self)
        frame.setFixedSize(427, 200)
        frame.setStyleSheet(
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
        )
        self.frame_layout.setSpacing(10)

        text_image_label = QLabel(self)
        text_image_pixmap = QPixmap("assets/Text.png")
        text_image_label.setPixmap(text_image_pixmap)
        self.frame_layout.addWidget(
            text_image_label, alignment=Qt.AlignTop | Qt.AlignHCenter
        )
        
        top_spacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.frame_layout.addItem(top_spacer)

        self.label = QLabel("Please, choose installation folder", self)
        self.label.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                color: #7247CB;
                font-weight: 200;
            }
        """
        )
        self.label.setFont(self.light_font)
        self.frame_layout.addWidget(self.label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        self.choose_dir_button = QPushButton("Choose", self)
        self.choose_dir_button.setStyleSheet(
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
        self.choose_dir_button.setFont(self.regular_font)
        self.choose_dir_button.setCursor(Qt.PointingHandCursor)
        self.choose_dir_button.clicked.connect(self.choose_directory)
        self.frame_layout.addWidget(
            self.choose_dir_button, alignment=Qt.AlignTop | Qt.AlignHCenter
        )
        
        frame.setLayout(self.frame_layout)
        main_layout.addWidget(frame, alignment=Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(navbar_frame)
        layout.addSpacing(110)
        layout.addLayout(main_layout)
        layout.addStretch()
        layout.addLayout(self.footer_layout)
        self.setLayout(layout)
        
    def choose_directory(self) -> None:
        mc_dir = QFileDialog.getExistingDirectory(self, "Choose Minecraft Directory")
        if mc_dir:
            self.mc_dir = mc_dir
            print(f"Selected directory: {mc_dir}")
            self.data_manip.save_user_data(
                new_data={"mc_dir": mc_dir},
                directory=self.config_dir,
                json_file=self.user_data_json,
            )

            self.frame_layout.removeWidget(self.choose_dir_button)
            self.choose_dir_button.deleteLater()
            self.label.setText("You are closer than you think")

            self.install_mc_button = QPushButton("Install", self)
            self.install_mc_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #503684;
                    color: #F0F0F0;
                    font-size: 14px;
                    font-weight: 400;
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
        else:
            print("No directory chosen!")
    
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
            if (
                dgrmc_dir is False
                and self.username_var not in ("", None)
                and self.password_var not in ("", None)
            ):
                return True
            else:
                ic(
                    f"Missing required folders in {self.username_var, self.password_var,dgrmc_dir}"
                )
                return False
    
    def start_installation(self) -> None:
        self.frame_layout.removeWidget(self.install_mc_button)
        self.install_mc_button.deleteLater()

        self.label.setText("Starting installation...")
        
        self.loading_gif_label = QLabel(self)
        self.loading_gif = QMovie("assets/loading2-40.gif")
        self.loading_gif_label.setMovie(self.loading_gif)
        self.loading_gif_label.setFixedSize(40, 40)
        self.loading_gif.start()
        self.frame_layout.addWidget(self.loading_gif_label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        thread = threading.Thread(target=self.install_mc, daemon=True)
        thread.start()
    
    def install_forge(self) -> None:
        self.label.setText("Intalling Minecraft...")

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
            ic("Minecraft downloaded")
        else:
            print(f"Forge {forge_version} can't be installed automatically.")
            mc_lib.forge.run_forge_installer(version=forge_version)
        self.set_status_signal.emit("Installation completed successfully!")
    
    def unzip_and_merge(self, zip_path: Path, target_dir: Path) -> None:
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                for zip_info in zip_ref.infolist():
                    extracted_path = target_dir / zip_info.filename
                    if extracted_path.exists():
                        if extracted_path.is_dir():
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
                            print(f"File {extracted_path} already exists. Skipping...")
                    else:
                        zip_ref.extract(zip_info, target_dir)
                zip_path.unlink()
            print(f"Extracted and merged contents of {zip_path.name} into {target_dir}")
        except Exception as e:
            print(f"Error during extraction and merge: {e}")
    
    def install_neccesary_files(self) -> None:
        self.label.setText("Configuring Things...")

        mc_dir = os.path.join(self.mc_dir, "DGRMClauncher")
        base_url = "https://github.com/Storgisl/dg_files/releases/download/v1.0/"
        def download_file(url: str, file_path: Path) -> None:
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
            self.label.setText("Installing Mods...")

            url = base_url + "mods.zip"
            file_path = Path(mc_dir) / "mods.zip"
            download_file(url=url, file_path=file_path)
            ic("Mods downloaded")
            self.unzip_and_merge(zip_path=file_path, target_dir=Path(mc_dir) / "mods")
            ic("Mods installed")
            self.set_status_signal.emit("Installation completed successfully!")
            self.restart_launcher()
        
        def install_rpacks() -> None:
            self.label.setText("Installing Resource packs...")

            url = base_url + "resourcepacks.zip"
            file_path = Path(mc_dir) / "resourcepacks.zip"
            download_file(url=url, file_path=file_path)
            ic("Rpacks downloaded")
            self.unzip_and_merge(
                zip_path=file_path, target_dir=Path(mc_dir) / "resourcepacks"
            )
            ic("Rpacks installed")
        
        def install_emotes() -> None:
            self.label.setText("Installing Emote packs...")

            url = base_url + "emotes.zip"
            file_path = Path(mc_dir) / "emotes.zip"
            download_file(url=url, file_path=file_path)
            ic("Emotes downloaded")
            self.unzip_and_merge(zip_path=file_path, target_dir=Path(mc_dir) / "emotes")
            ic("Emotes installed")
        
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

    # Рестарт лаунчера по оканчании загрузки
    def restart_launcher(self):
        # self.label.setText("Configuring Files...")
        # time.sleep(120)
        self.label.setText("Restarting...")
        time.sleep(5)
        # python = sys.executable
        # args = [python] + sys.argv
        # subprocess.Popen(args)
        # sys.exit()
