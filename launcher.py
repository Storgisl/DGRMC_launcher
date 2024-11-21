import json
import os
import platform

import customtkinter as ctk
from customtkinter import filedialog

from icecream import ic

from exceptions import UserDataException
from exceptions import UserOptionsException


def save_user_data(new_data, directory, json_file):
    user_data_file = os.path.join(directory, json_file)

    if not os.path.exists(user_data_file):
        with open(user_data_file, "w") as f:
            json.dump({}, f, indent=4)

    with open(user_data_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    data.update(new_data)

    with open(user_data_file, "w") as f:
        json.dump(data, f, indent=4)


def load_user_data(directory, json_file, create_if_missing=True):
    user_data_file = os.path.join(directory, json_file)

    if os.path.isfile(user_data_file):
        try:
            with open(user_data_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {user_data_file} contains invalid JSON. Returning empty data.")
            return {}
    else:
        if create_if_missing:
            print(f"File {user_data_file} does not exist. Creating a new one...")
            with open(user_data_file, "w") as f:
                json.dump({}, f, indent=4)
            return {}

    return {}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("DGRMC Launcher")
        ctk.set_appearance_mode("dark")
        self.font = ctk.CTkFont(family="Oswald",
                                size=40,
                                weight="bold")
        # Variables
        self.username_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.uuid_var = ctk.StringVar()
        self.token_var = ctk.StringVar()
        self.mc_dir = ctk.StringVar()
        self.user_data_json = "user_data.json"
        self.user_options_json = "user_options.json"
        # Frames
        self.registration_frame = ctk.CTkFrame(self)
        self.directory_frame = ctk.CTkFrame(self)
        self.options_frame = ctk.CTkFrame(self)
        self.main_frame = ctk.CTkFrame(self)

        # Check if user is already registered
        if platform.system() == "Windows":
            # For Windows, use the APPDATA directory
            self.default_dir = os.path.join(os.getenv("LOCALAPPDATA"),
                                            "DGRMC_Launcher")
        else:
            # For Linux/Mac, use a hidden folder in the home directory
            self.default_dir = os.path.expanduser("~/.dgrmc_launcher")

        ic(self.default_dir)

        if self.default_dir:
            os.makedirs(self.default_dir, exist_ok=True)

        self.user_data = load_user_data(directory=self.default_dir,
                                        json_file=self.user_data_json)

        self.user_options = load_user_data(directory=self.default_dir,
                                           json_file=self.user_options_json)
        ic(self.user_data)
        ic(self.user_options)
        ic(self.mc_dir.get())
        ic(self.username_var.get())
        ic(self.password_var.get())
        try:
            if (not self.user_data.get("username")
                    or not self.user_data.get("password")):
                self.show_registration_frame()

            elif (self.user_data.get("username") and
                    self.user_data.get("password")):
                self.username_var.set(self.user_data.get("username", ""))
                self.show_directory_frame()

        except UserDataException:
            ctk.CTkLabel(self.registration_frame,
                         text="Не введен логин или пароль.",
                         text_color="red").pack(pady=5)
            self.show_registration_frame()

        except Exception as e:
            print(f"error: {e}")

        try:
            if not self.user_options.get("mc_dir"):
                raise UserOptionsException

            elif self.user_options.get("mc_dir"):
                self.show_options_frame()

        except UserOptionsException:
            ctk.CTkLabel(self.directory_frame,
                         text="Выберите директорию.",
                         text_color="red").pack(pady=5)

        except Exception as e:
            print(f"error: {e}")

        if self.user_data.get("username") and self.user_data.get("password") and self.user_options.get("mc_dir"):
            self.show_main_frame()

    def show_registration_frame(self):
        self.clear_frames()
        self.registration_frame.pack(fill="both",
                                     expand=True)

        ctk.CTkLabel(self.registration_frame,
                     text="Регистрация",
                     font=("Arial", 18)).pack(pady=10)

        ctk.CTkLabel(self.registration_frame,
                     text="Имя пользователя:").pack(pady=5)
        ctk.CTkEntry(self.registration_frame,
                     textvariable=self.username_var).pack(pady=5)

        ctk.CTkLabel(self.registration_frame,
                     text="Пароль:").pack(pady=5)
        ctk.CTkEntry(self.registration_frame,
                     textvariable=self.password_var, show="*").pack(pady=5)

        ctk.CTkButton(self.registration_frame,
                      text="Продолжить",
                      command=self.handle_registration).pack(pady=20)

    def show_directory_frame(self):
        self.clear_frames()
        self.directory_frame.pack(fill="both",
                                  expand=True)

        ctk.CTkLabel(self.directory_frame,
                     text="Выберите директорию для лаунчера",
                     font=("Arial", 18)).pack(pady=10)
        ctk.CTkButton(self.directory_frame,
                      text="Выберите директорию",
                      command=self.choose_directory).pack(pady=20)

    def show_options_frame(self):
        self.clear_frames()
        self.options_frame.pack(fill="both",
                                expand=True)

        ctk.CTkLabel(self.options_frame,
                     text="Настройки для запуска",
                     font=("Arial", 18)).pack(pady=10)

        ctk.CTkLabel(self.options_frame,
                     text="uuid:\n(необязательно)").pack(pady=5)
        ctk.CTkEntry(self.options_frame,
                     textvariable=self.uuid_var,
                     show="*").pack(pady=5)

        ctk.CTkLabel(self.options_frame,
                     text="токен:\n(необязательно)").pack(pady=5)
        ctk.CTkEntry(self.options_frame,
                     textvariable=self.token_var,
                     show="*").pack(pady=5)

        ctk.CTkButton(self.options_frame,
                      text="Продолжить",
                      command=self.handle_options).pack(pady=20)

    def show_main_frame(self):
        self.clear_frames()
        self.main_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.main_frame,
                     text=f"С возвращением, {self.user_data.get("username")}",
                     font=self.font).pack(pady=15)

        if self.user_options.get("mc_dir"):
            if os.path.isdir(self.user_options.get("mc_dir")):
                ctk.CTkButton(self.main_frame,
                              text="Запустить",
                              font=self.font,
                              command=lambda: self.launch_mc(self.user_options.get("mc_dir"),
                                                             self.user_options)
                              ).pack(pady=20)
        else:
            ctk.CTkButton(self.main_frame,
                          text="Установить",
                          font=self.font,
                          command=lambda: self.launch_mc(self.mc_dir,
                                                         self.user_options)
                          ).pack(pady=20)

    def clear_frames(self):
        for frame in [self.registration_frame,
                      self.directory_frame,
                      self.options_frame,
                      self.main_frame]:
            frame.pack_forget()

    def handle_registration(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if username and password:
            print(f"Регистрация прошла успешно: {username}")
            # Save user data in the default directory
            self.user_data = {"username": username, "password": password}
            save_user_data(new_data=self.user_data,
                           directory=self.default_dir,
                           json_file="user_data.json")
            self.show_directory_frame()
        else:
            if not hasattr(self, "error_label"):
                # Create the error label if it doesn't exist
                self.error_label = ctk.CTkLabel(self.registration_frame,
                                                text="Заполните все поля.",
                                                text_color="red")
                self.error_label.pack(pady=5)
            else:
                # Update the existing error label if it already exists
                self.error_label.configure(text="Заполните все поля.")

    def handle_options(self):
        uuid = self.uuid_var.get()
        token = self.token_var.get()
        self.user_options = {"uuid": uuid, "token": token}
        save_user_data(new_data=self.user_options,
                       directory=self.default_dir,
                       json_file=self.user_options_json)
        self.show_main_frame()

    def choose_directory(self):
        mc_dir = filedialog.askdirectory(
                title="Выберите директорию для Майнкрафта")
        self.mc_dir = mc_dir
        ic(self.mc_dir)
        if self.mc_dir:
            self.user_options["mc_dir"] = self.mc_dir
            print(f"Selected directory: {self.mc_dir}")
            # Save selected directory if needed
            print("Ready to launch or configure Minecraft!")
            save_user_data(new_data=self.user_options,
                           directory=self.default_dir,
                           json_file=self.user_options_json)
            self.mc_dir = self.user_options["mc_dir"]
            self.show_options_frame()

    def launch_mc(self, mc_dir, options):
        import minecraft_launcher_lib
        import subprocess
        version = "1.12.2"

        minecraft_directory = os.path.join(mc_dir, "DGRMClauncher")

        # Ensure the directory exists
        os.makedirs(minecraft_directory, exist_ok=True)

        # Install the specified Minecraft version
        minecraft_launcher_lib.install.install_minecraft_version(
            versionid=version,
            minecraft_directory=minecraft_directory
          )

        # Launch Minecraft
        subprocess.call(
            minecraft_launcher_lib.command.get_minecraft_command(
                version=version,
                minecraft_directory=minecraft_directory,
                options=options
              )
          )


if __name__ == "__main__":
    app = App()
    app.mainloop()
