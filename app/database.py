# Configures SQLAlchemy and database variables
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.paths import DB_FILE

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