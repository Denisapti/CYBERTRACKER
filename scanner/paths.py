import os
import sys

APP_NAME = "CYBERTRACKER"

def get_base_path():
    try:
        return sys._MEIPASS  # PyInstaller temp
    except AttributeError:
        return os.path.dirname(os.path.abspath(__file__))

def resource_path(name):
    return os.path.join(get_base_path(), name)

def get_user_data_dir():
    # On Windows: use APPDATA; on other OSes: use home directory
    if sys.platform == "win32":
        base = os.getenv("APPDATA")
    else:
        # Linux/Mac: use home directory
        base = os.path.expanduser("~")
    
    path = os.path.join(base, APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path

def get_user_db_path():
    return os.path.join(get_user_data_dir(), "database.db")

def get_user_csv_path():
    return os.path.join(get_user_data_dir(), "hashes.csv")

def get_metadata_path():
    return os.path.join(get_user_data_dir(), "metadata.json")
