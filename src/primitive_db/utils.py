import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

DATA_DIR = PROJECT_ROOT / "data"

def load_metadata(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_table_data(table_name):
    DATA_DIR.mkdir(exist_ok=True)
    
    filepath = DATA_DIR / f"{table_name}.json"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_table_data(table_name, data):
    DATA_DIR.mkdir(exist_ok=True)
    
    filepath = DATA_DIR / f"{table_name}.json"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_table_filepath(table_name):
    DATA_DIR.mkdir(exist_ok=True)
    return DATA_DIR / f"{table_name}.json"

def table_data_exists(table_name):
    filepath = get_table_filepath(table_name)
    return filepath.exists()

def get_metadata_path():
    return PROJECT_ROOT / "db_meta.json"