import json
import os
import platform

import customtkinter as ctk
from customtkinter import filedialog

from icecream import ic

from exceptions import UserDataException
# , UserDirException, UserOptionsException


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
            print(f"Warning: {user_data_file} contains invalid JSON. \
                Returning empty data.")
            return {}
    else:
        if create_if_missing:
            print(f"File {user_data_file} does not exist. \
            Creating a new one...")
            with open(user_data_file, "w") as f:
                json.dump({}, f, indent=4)
            return {}

    return {}


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.setup_window()
        self.initialize_variables()
        self.create_frames()
        self.check_user_status()

    def setup_window(self) -> None:
        self.geometry("800x600")
        self.title("DGRMC Launcher")
        ctk.set_appearance_mode("dark")
        self.font = ctk.CTkFont(family="Oswald",
                                size=20,
                                weight="bold")

    def initialize_variables(self) -> None:
        """
        эти переменные сохраняют в себе значения на момент работы приложения,
        используй как плейсхолдеры для сохранения в json'ы
        """

        self.progress_label = None
        self.progress_slider = None
        self.username_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.uuid_var = ctk.StringVar()
        self.token_var = ctk.StringVar()
        self.mc_dir = ctk.StringVar()
        self.user_data_json = "user_data.json"
        self.user_options_json = "user_options.json"

        if platform.system() == "Windows":
            self.config_dir = os.path.join(os.getenv("LOCALAPPDATA"),
                                           "DGRMC_Launcher")
        else:
            self.config_dir = os.path.expanduser("~/.dgrmc_launcher")

        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        if not os.path.exists(os.path.join(self.config_dir,
                                           self.user_data_json)):

            self.user_data = {}
            self.user_options = {}
        else:

            self.user_data = load_user_data(
                                            directory=self.config_dir,
                                            json_file=self.user_data_json
                                            )

            self.user_options = load_user_data(
                                               directory=self.config_dir,
                                               json_file=self.user_options_json
                                               )

        ic(self.user_data)
        ic(self.user_options)
        ic(self.mc_dir.get())
        ic(self.user_data.get("username"))
        ic(self.password_var.get())

    def create_frames(self) -> None:
        self.registration_frame = ctk.CTkFrame(self)
        self.directory_frame = ctk.CTkFrame(self)
        self.options_frame = ctk.CTkFrame(self)
        self.main_frame = ctk.CTkFrame(self)

    def check_user_status(self) -> None:
        try:
            if (not self.user_data.get("username")
                    or not self.user_data.get("password")):
                self.show_registration_frame()

            elif (self.user_data.get("username") and
                    self.user_data.get("password")):
                self.username_var.set(self.user_data.get("username", ""))
                self.show_directory_frame()

        except UserDataException:
            ctk.CTkLabel(master=self.registration_frame,
                         text="Не введен логин или пароль.",
                         text_color="red").pack(pady=5)
            self.show_registration_frame()

        except Exception as e:
            print(f"error: {e}")

        try:
            if self.user_data.get("mc_dir"):
                self.show_options_frame()

        except Exception as e:
            print(f"error: {e}")

        if (self.user_data.get("username")
                and self.user_data.get("password")
                and self.user_data.get("mc_dir")):
            self.show_main_frame()

    def show_registration_frame(self) -> None:
        self.clear_frames()
        self.registration_frame.pack(fill="both", expand=True)

        self.registration_frame.grid_columnconfigure(0, weight=1)
        self.registration_frame.grid_rowconfigure(0, weight=1)
        self.registration_frame.grid_rowconfigure(1, weight=1)
        self.registration_frame.grid_rowconfigure(2, weight=1)

        registration_content = ctk.CTkFrame(master=self.registration_frame)
        registration_content.grid(row=1, column=0)

        ctk.CTkLabel(
            master=registration_content,
            text="Регистрация",
            font=self.font,
        ).grid(row=0,
               column=0,
               pady=10)

        ctk.CTkLabel(
            master=registration_content,
            text="Имя пользователя:",
            font=self.font,
        ).grid(row=1,
               column=0,
               pady=5)

        ctk.CTkEntry(
            master=registration_content,
            textvariable=self.username_var,
            font=self.font,
        ).grid(row=2,
               column=0,
               pady=5)

        ctk.CTkLabel(
            master=registration_content,
            text="Пароль:",
            font=self.font
        ).grid(row=3,
               column=0,
               pady=5)

        ctk.CTkEntry(
            master=registration_content,
            textvariable=self.password_var,
            font=self.font,
            show="*"
        ).grid(row=4,
               column=0,
               pady=5)

        ctk.CTkButton(
            master=registration_content,
            text="Продолжить",
            font=self.font,
            command=self.handle_registration
        ).grid(row=5,
               column=0,
               pady=20)

    def show_directory_frame(self) -> None:
        self.clear_frames()
        self.directory_frame.pack(fill="both",
                                  expand=True)

        self.directory_frame.grid_columnconfigure(0, weight=1)
        self.directory_frame.grid_rowconfigure(0, weight=1)
        self.directory_frame.grid_rowconfigure(1, weight=1)
        self.directory_frame.grid_rowconfigure(2, weight=1)

        directory_content = ctk.CTkFrame(master=self.directory_frame)
        directory_content.grid(row=1, column=0)

        ctk.CTkButton(master=directory_content,
                      text="Выберите директорию",
                      font=self.font,
                      command=self.choose_directory).grid(
                                                          row=0,
                                                          column=0,
                                                          pady=10,
        )

    def show_options_frame(self) -> None:
        self.clear_frames()
        self.options_frame.pack(fill="both",
                                expand=True)

        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(1, weight=1)
        self.options_frame.grid_rowconfigure(2, weight=1)

        option_content = ctk.CTkFrame(master=self.options_frame)
        option_content.grid(row=1,
                            column=0)

        ctk.CTkLabel(
                     master=option_content,
                     text="Настройки для запуска",
                     font=self.font).grid(
                                    row=0,
                                    column=0,
                                    pady=10,
                                    )

        ctk.CTkLabel(
                     master=option_content,
                     text="uuid:\n(необязательно)",
                     font=self.font).grid(
                                    row=1,
                                    column=0,
                                    pady=5,
                                    )

        ctk.CTkEntry(
                     master=option_content,
                     textvariable=self.uuid_var,
                     font=self.font,
                     show="*").grid(
                                    row=2,
                                    column=0,
                                    pady=5,
                                    )

        ctk.CTkLabel(
                     master=option_content,
                     text="токен:\n(необязательно)",
                     font=self.font).grid(
                                    row=3,
                                    column=0,
                                    pady=5,
                                    )

        ctk.CTkEntry(
                     master=option_content,
                     textvariable=self.token_var,
                     font=self.font,
                     show="*").grid(
                                    row=4,
                                    column=0,
                                    pady=5,
                                    )

        ctk.CTkButton(
                      master=option_content,
                      text="Продолжить",
                      command=self.handle_options).grid(
                                    row=5,
                                    column=0,
                                    pady=10,
                                    )

    def show_main_frame(self) -> None:
        self.clear_frames()
        self.main_frame.pack(fill="both", expand=True)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        self.user_data = load_user_data(
                     directory=self.config_dir,
                     json_file=self.user_data_json
        )

        main_content = ctk.CTkFrame(master=self.main_frame)
        main_content.grid(row=1,
                          column=0)

        ctk.CTkLabel(
                     master=main_content,
                     text=f"С возвращением, {self.user_data.get("username")}",
                     font=self.font).grid(
                                    row=0,
                                    column=0,
                                    pady=10,
                                    )

        if os.path.isdir(os.path.join(self.user_data.get("mc_dir"), "DGRMClauncher")):
            ic(self.user_data.get("mc_dir"))
            ctk.CTkButton(
                          master=main_content,
                          text="Запустить",
                          font=self.font,
                          command=lambda: self.run_mc(
                                    mc_dir=self.user_data.get("mc_dir"),
                                    options=self.user_options)
                          ).grid(
                                    row=1,
                                    column=0,
                                    pady=10,
                                    )
        else:
            ctk.CTkButton(
                          master=main_content,
                          text="Установить",
                          font=self.font,
                          command=lambda: self.install_mc(
                                    mc_dir=self.user_data.get("mc_dir"),
                          )).grid(
                                    row=1,
                                    column=0,
                                    pady=10,
                                    )

    def show_installation_frame(self) -> None:
        self.clear_frames()
        self.main_frame.pack(fill="both", expand=True)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        install_content = ctk.CTkFrame(master=self.main_frame)
        install_content.grid(row=0, column=0, padx=20, pady=20)

        # Add a label for installation status
        self.progress_label = ctk.CTkLabel(
            master=install_content,
            text="Установка Minecraft...",
            font=self.font
        )
        self.progress_label.grid(row=0, column=0, pady=10)

        # Add a slider for progress
        self.progress_slider = ctk.CTkSlider(
            master=install_content,
            from_=0,
            to=100,
            number_of_steps=100,
            width=300
        )
        self.progress_slider.grid(row=1, column=0, pady=10)

    def clear_frames(self) -> None:
        for frame in [self.registration_frame,
                      self.directory_frame,
                      self.options_frame,
                      self.main_frame]:
            frame.pack_forget()

    def handle_registration(self) -> None:
        username: str = self.username_var.get()
        password: str = self.password_var.get()

        if username and password:
            print(f"Регистрация прошла успешно: {username}")
            # Save user data in the default directory
            self.user_data = {"username": username, "password": password}
            save_user_data(
                           new_data=self.user_data,
                           directory=self.config_dir,
                           json_file=self.user_data_json
            )
            self.show_directory_frame()
        else:
            if not hasattr(self, "error_label"):
                # Create the error label if it doesn't exist
                self.error_label = ctk.CTkLabel(
                                                master=self.registration_frame,
                                                text="Заполните все поля.",
                                                text_color="red"
                )
                self.error_label.pack(pady=5)
            else:
                # Update the existing error label if it already exists
                self.error_label.configure(text="Заполните все поля.")

    def handle_options(self) -> None:
        username: str = self.username_var.get()
        uuid: str = self.uuid_var.get()
        token: str = self.token_var.get()

        self.user_options: dict = {"username": username,
                                   "uuid": uuid,
                                   "token": token}

        save_user_data(
                       new_data=self.user_options,
                       directory=self.config_dir,
                       json_file=self.user_options_json
        )

        self.show_main_frame()

    def choose_directory(self) -> None:
        self.mc_dir = filedialog.askdirectory(
                title="Выберите директорию для Майнкрафта")
        ic(self.mc_dir)
        if self.mc_dir:
            self.user_data = {"mc_dir": self.mc_dir}
            print(f"Selected directory: {self.mc_dir}")
            # Save selected directory if needed
            print("Ready to launch or configure Minecraft!")
            save_user_data(
                           new_data=self.user_data,
                           directory=self.config_dir,
                           json_file=self.user_data_json
            )
            self.show_options_frame()

        elif not self.user_data.get("mc_dir"):
            ctk.CTkLabel(
                         master=self.directory_frame,
                         text="Выберите директорию.",
                         text_color="red"
            ).pack(pady=5)

    def install_mc(self, mc_dir: str) -> None:
        import threading
        import minecraft_launcher_lib as mc_lib

        # Ensure progress_label and progress_slider are initialized
        if not self.progress_label or not self.progress_slider:
            self.show_installation_frame()

        def installation_task():
            version = "1.12.2"
            minecraft_directory = os.path.join(mc_dir, "DGRMClauncher")
            os.makedirs(minecraft_directory, exist_ok=True)

            try:
                mc_lib.install.install_minecraft_version(
                    versionid=version,
                    minecraft_directory=minecraft_directory,
                    callback={"setStatus": lambda status: print(status),
                              "setProgress": progress_callback,
                              "done": done_callback}
                )
            except Exception as e:
                print(f"Error during installation: {e}")
                self.progress_label.configure(text="Установка прервана. Попробуйте снова.")

        def progress_callback(progress: int):
            """Update the slider based on progress."""
            self.progress_slider.set(progress)
            self.progress_label.configure(text=f"Установка... {progress}%")

        def done_callback():
            """Handle completion."""
            self.progress_label.configure(text="Установка завершена!")
            self.show_main_frame()

        # Run installation in a separate thread
        threading.Thread(target=installation_task, daemon=True).start()

    def run_mc(self,mc_dir: str, options: dict) -> None:
        import minecraft_launcher_lib as mc_lib
        import subprocess

        version = "1.12.2"

        minecraft_directory = mc_lib.utils.get_minecraft_directory()
        minecraft_directory = os.path.join(mc_dir, "DGRMClauncher")

        subprocess.call(
            mc_lib.command.get_minecraft_command(
                version=version,
                minecraft_directory=minecraft_directory,
                options=options,
              )
          )

if __name__ == "__main__":
    app = App()
    app.mainloop()
