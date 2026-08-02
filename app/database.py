# Configures SQLAlchemy and database variables
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.paths import DB_FILE

DATABASE_URL = os.environ.get("HDPILOT_DB_URL", f"sqlite:///{DB_FILE}")

engine = create_engine(
    DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass