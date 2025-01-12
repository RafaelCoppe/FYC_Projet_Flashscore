import subprocess
import logging
from datetime import datetime

logging.basicConfig(
    filename='automation/scheduler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_script():
    try:
        subprocess.run(['python3', 'main.py'], check=True)
        logging.info("Script exécuté avec succès.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur lors de l'exécution : {e}")

if __name__ == "__main__":
    run_script()