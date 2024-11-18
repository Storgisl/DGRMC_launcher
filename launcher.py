import customtkinter as ctk
from customtkinter import filedialog
import json
import os
import platform


# Function to save user data
def save_user_data(data, directory):
    user_data_file = os.path.join(directory, "user_data.json")
    with open(user_data_file, "w") as f:
        json.dump(data, f)


# Function to load user data
def load_user_data(directory):
    user_data_file = os.path.join(directory, "user_data.json")
    if os.path.exists(user_data_file):
        with open(user_data_file, "r") as f:
            return json.load(f)
    return None


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        self.title("DGRMC Launcher")

        # Variables
        self.username_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.mc_dir = ""

        # Frames
        self.registration_frame = ctk.CTkFrame(self)
        self.directory_frame = ctk.CTkFrame(self)

        # Check if user is already registered
        if platform.system() == "Windows":
       # For Windows, use the APPDATA directory
          self.default_dir = os.path.join(os.getenv("LOCALAPPDATA"), "DGRMC_Launcher")
        else:
          # For Linux/Mac, use a hidden folder in the home directory
          self.default_dir = os.path.expanduser("~/.dgrmc_launcher")

        if self.default_dir:
            os.makedirs(self.default_dir, exist_ok=True)  # Ensure the directory exists

        self.user_data = load_user_data(self.default_dir)

        if self.user_data == None:
            # User is already registered
            self.show_registration_frame()
        elif self.user_data["username"] and self.user_data["password"]:
            # New user
            self.username_var.set(self.user_data.get("username", ""))
            ctk.CTkLabel(self.directory_frame, text=f"Welcome back, {self.user_data["username"]}", font=("Arial", 18)).pack(pady=15)
            self.show_directory_frame()

    def show_registration_frame(self):
        self.clear_frames()
        self.registration_frame.pack(fill="both", expand=True)

        # Registration Form
        ctk.CTkLabel(self.registration_frame, text="Register", font=("Arial", 18)).pack(pady=10)
        ctk.CTkLabel(self.registration_frame, text="Username:").pack(pady=5)
        ctk.CTkEntry(self.registration_frame, textvariable=self.username_var).pack(pady=5)

        ctk.CTkLabel(self.registration_frame, text="Password:").pack(pady=5)
        ctk.CTkEntry(self.registration_frame, textvariable=self.password_var, show="*").pack(pady=5)

        ctk.CTkButton(self.registration_frame, text="Next", command=self.handle_registration).pack(pady=20)

    def show_directory_frame(self):
        self.clear_frames()
        self.directory_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.directory_frame, text="Select Minecraft Directory", font=("Arial", 18)).pack(pady=10)
        ctk.CTkButton(self.directory_frame, text="Choose Directory", command=self.choose_directory).pack(pady=20)

    def clear_frames(self):
        for frame in [self.registration_frame, self.directory_frame]:
            frame.pack_forget()

    def handle_registration(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if username and password:
            print(f"Registration successful for user: {username}")
            # Save user data in the default directory
            self.user_data = {"username": username, "password": password}
            save_user_data(self.user_data, self.default_dir)
            self.show_directory_frame()
        else:
            ctk.CTkLabel(self.registration_frame, text="Please fill in all fields.", text_color="red").pack(pady=5)

    def choose_directory(self):
        self.mc_dir = filedialog.askdirectory(title="Select Minecraft Directory")
        if self.mc_dir:
            print(f"Selected directory: {self.mc_dir}")
            # Save selected directory if needed
            print("Ready to launch or configure Minecraft!")

if __name__ == "__main__":
    app = App()
    app.mainloop()
