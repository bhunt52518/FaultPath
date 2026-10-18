from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from collections.abc import Generator



# Locate the FaultPath project root
BASE_DIR = Path(__file__).resolve().parents[2]

# SQLite database configuration
DATABASE_PATH = BASE_DIR / "faultpath.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

# Database connectivity managment
engine = create_engine(DATABASE_URL, echo=False)

# Factory used to create database sessions
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

#Enforces SQLite use of Forgein Keys
@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# FastAPI dependency for database sessions
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()