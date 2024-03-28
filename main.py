import mysql.connector
from mysql.connector import Error
import subprocess
import datetime
import time
import signal
import sys
import psutil

terminate_flag = False

def check_last_insert_time():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='flight details',
            user='root'
        )
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(record_insert_time) FROM flights")
            last_insert_time = cursor.fetchone()[0]
            if last_insert_time is not None:
                current_time = datetime.datetime.now()
                time_difference = current_time - last_insert_time
                if time_difference.total_seconds() > 30:  # Check if last insert was more than 10 seconds ago
                    print("Last database insert was more than 10 seconds ago. Restarting database update program...")
                    restart_program()
            else:
                print("No records found in the database.")
    except Error as e:
        print('Error:', e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print('Database connection closed')

def restart_program():
    global terminate_flag
    python_executable = sys.executable  
    script_path = "C:\\flightradar\\flightdbs.py" 
    for proc in psutil.process_iter():
        try:
            if terminate_flag:
                break
            if proc.name() == "python.exe" and script_path in proc.cmdline():
                proc.terminate()
                print("Previous process terminated successfully.")
        except psutil.NoSuchProcess:
            pass
    if not terminate_flag:
        subprocess.Popen([python_executable, script_path])
        print("New process started.")

def signal_handler(sig, frame):
    global terminate_flag
    print("Ctrl+C pressed. Stopping the script.")
    terminate_flag = True

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    try:
        while not terminate_flag:
            check_last_insert_time()
            time.sleep(5)  # Check every 5 seconds
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)  # Manually call the signal handler for KeyboardInterrupt