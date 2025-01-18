import os
import subprocess
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