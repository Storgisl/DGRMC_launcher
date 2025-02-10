import os
import platform

from pathlib import Path
from DataManip import DataManip

from icecream import ic


class PageStatusChecker:
    def __init__(self):
        self.data_manip = DataManip()

        if platform.system() == "Windows":
            self.config_dir = os.path.join(os.getenv("LOCALAPPDATA"), "DGRMC_Launcher")
        else:
            self.config_dir = os.path.expanduser("~/.dgrmc_launcher")

        self.user_data_json = "user_data.json"
        self.user_options_json = "user_options.json"
        self.user_data = self.data_manip.load_user_data(
            directory=self.config_dir, json_file=self.user_data_json
        )
        self.user_options = self.data_manip.load_user_data(
            directory=self.config_dir, json_file=self.user_options_json
        )

        self.mc_dir = self.user_options.get("mc_dir", "")
        self.current_username_var = self.user_options.get("username", "")
        self.password_var = None

    def download_status(self) -> bool:
        dgrmc_dir = str(Path(self.mc_dir) / "DGRMClauncher")
        required_folders = [
            "assets",
            "libraries",
            "runtime",
            "versions",
            "emotes",
            "mods",
        ]
        if self.check_dirs(directory=dgrmc_dir, folders=required_folders):
            ic(dgrmc_dir)
            return True
        else:
            return False

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

    def user_status(self, username: str) -> bool:
        user_info = self.user_data.get(username, {})
        password = user_info.get("password", "")

        return bool(password)

    def check_user_status(self, username: str) -> bool:
        try:
            user_status = self.user_status(username=username)
            return bool(user_status)

        except Exception as e:
            print(f"Error in check_user_status: {e}")
            return False

    def check_download_status(self) -> bool:
        try:
            download_status = self.download_status()
            return bool(download_status)
        except Exception as e:
            print(f"Error in check_download_status: {e}")
            return False
