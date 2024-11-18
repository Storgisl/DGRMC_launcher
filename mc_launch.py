import minecraft_launcher_lib
import subprocess
import os

def launch_mc(mc_dir, options):
    version = "1.12.2"
    # Replace the minecraft folder with DGRMClauncher inside the selected directory
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
