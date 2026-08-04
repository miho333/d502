from pathlib import Path
import os
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
DB_PATH = DATA_DIR / 'workforce.db'

CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")
BEA_API_KEY = os.getenv("BEA_API_KEY")

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)