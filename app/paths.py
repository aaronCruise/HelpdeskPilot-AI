from pathlib import Path

APP_DIR = Path(__file__).resolve().parent

ROOT_DIR = APP_DIR.parent

DATA_DIR = ROOT_DIR / 'data'
KNOWLEDGE_BASE_DIR = DATA_DIR / 'knowledge_base'

DB_FILE = DATA_DIR / 'hdpilot.db'
VECTOR_DB_FILE = DATA_DIR / 'knowledge_base.db'