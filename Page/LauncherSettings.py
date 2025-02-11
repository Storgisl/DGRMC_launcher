import sys
import os
from PySide6.QtCore import Signal
from pathlib import Path
from UI import LauncherSettingsUI

from .Page import Page


class LauncherSettings(Page):
    to_game_settings = Signal()
    go_back = Signal()
    to_account = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.ui = LauncherSettingsUI(self)
        self.page_logger.info("LauncherSettings page initialized")
        self.setObjectName("launcher_settings_page")
        self.stacked_widget = stacked_widget

    def check_updates(self) -> None:
        pass

    def open_folder(self) -> None:
        path = str(Path(self.mc_dir) / "DGRMClauncher")
        
        if sys.platform == "win32":
            os.system(f'explorer "{path}"')
        elif sys.platform == "darwin":
            os.system(f'open "{path}"')
        else:
            os.system(f'xdg-open "{path}"')
