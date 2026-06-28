from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent.parent
DB_FILE = DB_DIR / 'hdpilot.db'

engine = create_engine(
    f"sqlite:///{DB_FILE}",
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass