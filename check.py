import psutil
import os
import time

def is_process_running(script_path):
    process_name = os.path.basename(script_path)
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['name'] == 'python.exe' and process.info['cmdline'] and process.info['cmdline'][1] == script_path:
            return True
    return False

def restart_if_not_running(script_path):
    while True:
        if not is_process_running(script_path):
            print(f"{script_path} is not running")
            print(f"Restarting {script_path}...")
            os.system(f"python {script_path}")
            time.sleep(5)  # Wait for the script to start
        else:
            print(f"{script_path} is running")
            time.sleep(5)  # Check every 2 minutes

if __name__ == "__main__":
    script_path = "C:\\flightradar\\flightdbs.py"
    restart_if_not_running(script_path)

