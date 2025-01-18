import os
import subprocess
main
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
import threading
import time

class Packager:
    def __init__(self, exe_name, spec_file):
        self.exe_name = exe_name
        self.spec_file = spec_file
        self.lock = threading.Lock()

    def package(self):
        with self.lock:
            if self.is_running():
                print("[WARNING] The application is currently running. Please close it before packaging.")
                return
            
            print("[INFO] Starting the packaging process...")
            try:
                subprocess.run(['pyinstaller', '--onefile', self.spec_file], check=True)
                print("[SUCCESS] Packaging completed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Packaging failed: {e}")

    def is_running(self):
        # Check if the .exe file is running
        try:
            output = subprocess.check_output(['tasklist'], encoding='utf-8')
            return self.exe_name in output
        except Exception as e:
            print(f"[ERROR] Failed to check running status: {e}")
            return False

if __name__ == "__main__":
    packager = Packager("your_executable_name.exe", "pyinstaller.spec")
    packager.package()
version-2.1
