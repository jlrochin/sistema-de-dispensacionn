import os
import subprocess
import time
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

if __name__ == "__main__":
    main()