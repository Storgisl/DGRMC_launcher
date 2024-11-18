import customtkinter as ctk
from customtkinter import filedialog
import json
import os


# Function to save user data
def save_user_data(data, directory):
    """Save user data to a file in the selected directory."""
    user_data_file = os.path.join(directory, "user_data.json")
    with open(user_data_file, "w") as f:
        json.dump(data, f)


# Function to load user data
def load_user_data(directory):
    """Load user data from a file in the selected directory."""
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
        self.default_dir = os.path.expanduser("~/.dgrmc_launcher")  # Default directory for user data
        os.makedirs(self.default_dir, exist_ok=True)  # Ensure the directory exists

        self.user_data = load_user_data(self.default_dir)

        if self.user_data:
            # User is already registered
            self.username_var.set(self.user_data.get("username", ""))
            print(f"Welcome back, {self.user_data['username']}!")
            self.show_directory_frame()
        else:
            # New user
            self.show_registration_frame()

    def show_registration_frame(self):
        """Show the registration frame."""
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
        """Show the directory selection frame."""
        self.clear_frames()
        self.directory_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.directory_frame, text="Select Minecraft Directory", font=("Arial", 18)).pack(pady=10)
        ctk.CTkButton(self.directory_frame, text="Choose Directory", command=self.choose_directory).pack(pady=20)

    def clear_frames(self):
        """Clear all frames."""
        for frame in [self.registration_frame, self.directory_frame]:
            frame.pack_forget()

    def handle_registration(self):
        """Handle user registration."""
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
        """Handle directory selection."""
        self.mc_dir = filedialog.askdirectory(title="Select Minecraft Directory")
        if self.mc_dir:
            print(f"Selected directory: {self.mc_dir}")
            # Save selected directory if needed
            print("Ready to launch or configure Minecraft!")


if __name__ == "__main__":
    app = App()
    app.mainloop()
