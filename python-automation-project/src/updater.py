import os
import subprocess
import time

def is_exe_running(exe_name):
    try:
        # Check if the executable is running
        output = subprocess.check_output(['tasklist'], encoding='utf-8')
        return exe_name in output
    except Exception as e:
        print(f"[ERROR] Failed to check if {exe_name} is running: {e}")
        return False

def update_repository():
    try:
        # Run git pull to update the local repository
        subprocess.run(['git', 'pull'], check=True)
        print("[SUCCESS] Repository updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to update repository: {e}")

def main():
    exe_name = "your_executable_name.exe"  # Replace with your actual .exe name

    # Wait for the .exe to close if it's running
    while is_exe_running(exe_name):
        print(f"[INFO] Waiting for {exe_name} to close...")
        time.sleep(5)

    update_repository()

if __name__ == "__main__":
    main()