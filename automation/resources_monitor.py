import psutil
import logging
from logger_config import define_logs

define_logs()

def watch_resources():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    logging.info(f"Utilisation CPU : {cpu_usage}%, Utilisation mémoire : {memory_usage}%")

if __name__ == "__main__":
    watch_resources()