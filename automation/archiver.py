import shutil
import os
from datetime import datetime

def archive_data():
    archive_name = f"data/archives/data_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.make_archive(archive_name, 'zip', 'data/raw')
    print(f"Archive créée : {archive_name}.zip")

if __name__ == "__main__":
    archive_data()