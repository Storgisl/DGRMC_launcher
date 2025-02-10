import subprocess
import threading

from pathlib import Path

from PySide6.QtCore import Signal
import minecraft_launcher_lib as mc_lib

from UI import MainPageUI
from .Page import Page


class MainPage(Page):
    to_settings = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.ui = MainPageUI(self)
        self.page_logger.info("Main page initialized")
        self.stacked_widget = stacked_widget

    def update_current_username(self, username: str):
        self.current_username_var = username

    def run_mc(self) -> None:
        def run_minecraft():
            version = "1.20.1"
            forge_version = mc_lib.forge.find_forge_version(version)
            forge_vers = mc_lib.forge.forge_to_installed_version(forge_version)
            minecraft_directory = str(Path(self.mc_dir) / "DGRMClauncher")
            command = mc_lib.command.get_minecraft_command(
                version=forge_vers,
                minecraft_directory=minecraft_directory,
                options=self.user_options,
            )
            try:
                subprocess.call(command)
            except Exception as e:
                print("pizdec vse slomalos")

        thread = threading.Thread(target=run_minecraft, daemon=True)
        thread.start()
