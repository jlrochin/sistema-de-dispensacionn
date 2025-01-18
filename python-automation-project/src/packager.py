import os
import subprocess
import time
import fcntl

def lock_file(file):
    """Lock the file to prevent concurrent access."""
    fcntl.flock(file, fcntl.LOCK_EX)

def unlock_file(file):
    """Unlock the file after access."""
    fcntl.flock(file, fcntl.LOCK_UN)

def package_application():
    """Package the application using PyInstaller."""
    exe_name = "your_application_name.exe"  # Replace with your application name
    pyinstaller_command = f"pyinstaller --onefile --name {exe_name} pyinstaller.spec"
    
    with open("packaging.lock", "w") as lock_file:
        lock_file(lock_file)
        try:
            print("Starting packaging process...")
            subprocess.run(pyinstaller_command, shell=True, check=True)
            print("Packaging completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error during packaging: {e}")
        finally:
            unlock_file(lock_file)

if __name__ == "__main__":
    package_application()