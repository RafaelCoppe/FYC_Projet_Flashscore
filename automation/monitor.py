import subprocess
import time
import logging
from logger_config import define_logs

define_logs()

def watch_and_restart():
    while True:
        try:
            subprocess.run(['python3', 'main.py'], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Erreur détectée : {e}")
            time.sleep(60) 
        else:
            break

if __name__ == "__main__":
    watch_and_restart()                