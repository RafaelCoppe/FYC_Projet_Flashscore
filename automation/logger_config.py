import logging

def define_logs():
    logging.basicConfig(
        filename='automation/system_logs.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Configuration des logs initialisée.")
