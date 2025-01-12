import shutil
import os
from datetime import datetime

def create_directories():
    # Vérifier si les répertoires existent, sinon les créer
    directories = ['/data', '/data/raw', '/data/archives']
    for directory in directories:
        if not os.path.exiss(directory):
            print(f"Le dossier {directory} n'existe pas. Création...")
            os.makedirs(directory)
        else:
            print(f"Le dossier {directory} existe déjà.")

def archive_data():
    archive_name = f"data/archives/data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.make_archive(archive_name, 'zip', 'data/raw')
    print(f"Archive créée : {archive_name}.zip")

if __name__ == "__main__":
    archive_data()