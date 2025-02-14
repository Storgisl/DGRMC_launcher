from PySide6.QtCore import QObject, QThread, Signal
import requests
import shutil
import time
import os
import zipfile
from pathlib import Path
import minecraft_launcher_lib as mc_lib
from icecream import ic


class InstallWorker(QObject):
    set_status_signal = Signal(str)
    set_progress_signal = Signal(int)
    set_max_signal = Signal(int)
    finished = Signal()

    def __init__(self, mc_dir, base_url):
        super().__init__()
        self.mc_dir = Path(mc_dir)  # Ensure mc_dir is a Path object
        self.base_url = base_url

    def install_forge(self):
        self.set_status_signal.emit("Installing Minecraft...")
        version = "1.20.1"
        mc_dir = self.mc_dir / "DGRMClauncher"
        forge_version = mc_lib.forge.find_forge_version(version)
        if mc_lib.forge.supports_automatic_install(forge_version):
            callback = {
                "setProgress": lambda progress: self.set_progress_signal.emit(progress),
                "setMax": lambda max_value: self.set_max_signal.emit(max_value),
            }
            mc_lib.forge.install_forge_version(
                versionid=forge_version, path=str(mc_dir), callback=callback
            )
        else:
            mc_lib.forge.run_forge_installer(version=forge_version)
        self.set_status_signal.emit("Forge installation completed successfully!")

    def unzip_and_merge(self, zip_path: Path, target_dir: Path) -> None:
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                for zip_info in zip_ref.infolist():
                    self.set_status_signal.emit(f"Unpacking {zip_info.filename}...")
                    extracted_path = target_dir / zip_info.filename
                    if extracted_path.exists():
                        if extracted_path.is_dir():
                            temp_dir = target_dir / f"{zip_info.filename}_temp"
                            temp_dir.mkdir(parents=True, exist_ok=True)
                            zip_ref.extract(zip_info, str(temp_dir))  # Convert to string for zip_ref.extract
                            for item in temp_dir.iterdir():
                                dest = extracted_path / item.name
                                if item.is_file() and not dest.exists():
                                    shutil.move(str(item), str(dest))  # Convert to string for shutil.move
                                elif item.is_dir():
                                    shutil.copytree(str(item), str(dest), dirs_exist_ok=True)  # Convert to string for shutil.copytree
                            shutil.rmtree(str(temp_dir))  # Convert to string for shutil.rmtree
                        else:
                            print(f"File {extracted_path} already exists. Skipping...")
                    else:
                        zip_ref.extract(zip_info, str(target_dir))  # Convert to string for zip_ref.extract
            # Ensure the file is closed before deleting it
            zip_path.unlink()
            print(f"Extracted and merged contents of {zip_path.name} into {target_dir}")
        except Exception as e:
            print(f"Error during extraction and merge: {e}")

    def download_file(self, url: str, file_path: Path):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get("content-length", 0))
            downloaded_size = 0
            last_emit = -10

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        progress = int((downloaded_size / total_size) * 100)

                        if progress >= last_emit + 10 or progress == 100:
                            ic(progress)
                            ic(last_emit)
                            if progress <= 10:
                                self.set_progress_signal.emit(1)
                            else:
                                self.set_progress_signal.emit(progress // 10)
                            last_emit = progress

    def install_mods(self) -> None:
        self.set_status_signal.emit("Installing Mods...")
        url = self.base_url + "mods.zip"
        file_path = self.mc_dir / "DGRMClauncher" / "mods.zip"
        self.download_file(url=url, file_path=file_path)
        ic("Mods downloaded")
        self.unzip_and_merge(
            zip_path=file_path, target_dir=self.mc_dir / "DGRMClauncher" / "mods"
        )
        ic("Mods installed")
        self.set_status_signal.emit("Mods installation completed successfully!")

    def install_rpacks(self) -> None:
        self.set_status_signal.emit("Installing Resource packs...")
        url = self.base_url + "resourcepacks.zip"
        file_path = self.mc_dir / "DGRMClauncher" / "resourcepacks.zip"
        self.download_file(url=url, file_path=file_path)
        ic("Rpacks downloaded")
        self.unzip_and_merge(
            zip_path=file_path,
            target_dir=self.mc_dir / "DGRMClauncher" / "resourcepacks"
        )
        ic("Rpacks installed")
        self.set_status_signal.emit(
            "Resource packs installation completed successfully!"
        )

    def install_emotes(self) -> None:
        self.set_status_signal.emit("Installing Emotes...")
        url = self.base_url + "emotes.zip"
        file_path = self.mc_dir / "DGRMClauncher" / "emotes.zip"
        self.download_file(url=url, file_path=file_path)
        ic("Emotes downloaded")
        self.unzip_and_merge(
            zip_path=file_path,
            target_dir=self.mc_dir / "DGRMClauncher" / "emotes"
        )
        ic("Emotes installed")
        self.set_status_signal.emit("Emotes installation completed successfully!")

    def install_mc(self):
        mc_dir = self.mc_dir / "DGRMClauncher"
        os.makedirs(mc_dir, exist_ok=True)

        max_retries = 5
        retry_delay = 3

        for attempt in range(1, max_retries + 1):
            try:
                self.set_status_signal.emit(
                    f"Attempt {attempt}: Installing Minecraft..."
                )

                if attempt > 1:
                    shutil.rmtree(mc_dir, ignore_errors=True)
                    os.makedirs(mc_dir, exist_ok=True)

                self.install_forge()
                self.install_emotes()
                self.install_rpacks()
                self.install_mods()

                self.set_status_signal.emit("Installation completed successfully!")
                self.finished.emit()
                return
            except requests.exceptions.ConnectionError:
                self.set_status_signal.emit(
                    f"Network error. Retrying {attempt}/{max_retries}..."
                )
            except Exception as e:
                self.set_status_signal.emit(f"Critical error: {str(e)}")
                self.finished.emit()

            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                self.set_status_signal.emit(
                    "Installation failed after multiple attempts."
                )
                self.finished.emit()