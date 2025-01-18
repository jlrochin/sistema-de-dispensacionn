import os
import subprocess
import time
main
import psutil

def is_exe_running(exe_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == exe_name:
            return True
    return False

def wait_for_exe_to_close(exe_name):
    while is_exe_running(exe_name):
        print(f"{exe_name} is still running. Waiting...")
        time.sleep(5)

def update_repository():
    print("Updating the local repository...")
    subprocess.run(["git", "pull"], check=True)

def main():
    exe_name = "your_executable.exe"  # Replace with your actual executable name
    wait_for_exe_to_close(exe_name)
    update_repository()
    print("Repository updated successfully.")

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
version-2.1

if __name__ == "__main__":
    main()