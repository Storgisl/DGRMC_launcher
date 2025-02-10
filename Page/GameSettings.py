import shutil
import psutil
import re

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from icecream import ic

from UI import GameSettingsUI

from .Page import Page


class GameSettings(Page):
    to_launcher_settings = Signal()
    delete_complete = Signal()
    go_back = Signal()

    def __init__(self, stacked_widget) -> None:
        super().__init__()
        self.page_logger.info("GameSettings page initialized")
        self.setObjectName("game_settings_page")
        self.stacked_widget = stacked_widget
        self.ram_value = self.get_numbers_from_string(
            self.user_options.get("jvmArguments", ["2048"])[-1]
        )[-1]
        ic(self.ram_value)

        self.res_width = self.user_options.get("resolutionWidth", 1920)
        self.res_height = self.user_options.get("resolutionHeight", 1080)
        ic(self.res_width)
        ic(self.res_height)
        self.ui = GameSettingsUI(self)

    def get_max_system_ram(self) -> int:
        total_ram = psutil.virtual_memory().total
        return total_ram // (1024 * 1024)

    def generate_jvm_arguments(self, ram_value: str) -> None:
        self.ram_value = int(ram_value)
        self.data_manip.save_user_data(
            new_data={
                "jvmArguments": [
                    f"-Xms{self.ram_value // 2}M",
                    f"-Xmx{self.ram_value}M",
                ]
            },
            directory=self.config_dir,
            json_file=self.user_options_json,
        )

    def set_resolution(self, width: str, height: str) -> None:
        self.res_width = str(width)
        self.res_height = str(height)
        self.data_manip.save_user_data(
            new_data={
                "customResolution": True,
                "resolutionWidth": self.res_width,
                "resolutionHeight": self.res_height,
            },
            directory=self.config_dir,
            json_file=self.user_options_json,
        )

    def delete_mc(self) -> None:
        if self.ui.delete_line.text().lower() == "delete":
            try:
                shutil.rmtree(str(Path(self.mc_dir) / "DGRMClauncher"))
                self.delete_complete.emit()
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("no text")
            pass

    def on_checkbox_state_changed(self, state):
        if state == Qt.Checked:
            print("Checkbox is checked")
        else:
            print("Checkbox is unchecked")

    def save_config(self):
        # Default values
        DEFAULT_RAM = 2048
        DEFAULT_WIDTH = 1920
        DEFAULT_HEIGHT = 1080
        validation_passed = True

        # Validate RAM value
        ram_text = self.ui.value_line.text().replace(" MiB", "")
        if not ram_text.isdigit() or (ram_value := int(ram_text)) <= 0:
            self.ui.ram_error_label.setText(
                "<span style='color: red;'>Invalid RAM! Using default (2048 MiB)</span>"
            )
            ram_value = DEFAULT_RAM
            self.ui.value_line.setText(f"{DEFAULT_RAM} MiB")
            validation_passed = False
        else:
            self.ui.ram_error_label.setText("")

        # Validate resolution values
        try:
            width = int(self.res_width)
            height = int(self.res_height)
            if width <= 0 or height <= 0:
                raise ValueError
        except (ValueError, TypeError):
            self.ui.res_error_label.setText(
                "<span style='color: red;'>Invalid resolution! Using default (1920x1080)</span>"
            )
            width = DEFAULT_WIDTH
            height = DEFAULT_HEIGHT
            self.res_width = width
            self.res_height = height
            self.ui.update_resolution_value()
            validation_passed = False
        else:
            self.ui.res_error_label.setText("")

        # Only save if validation passed
        if validation_passed:
            self.generate_jvm_arguments(str(ram_value))
            self.set_resolution(str(width), str(height))
        else:
            # Save default values to config
            self.generate_jvm_arguments(str(DEFAULT_RAM))
            self.set_resolution(DEFAULT_WIDTH, DEFAULT_HEIGHT)

    def get_numbers_from_string(self, s):
        return [int(num) for num in re.findall(r"\d+", s)]
