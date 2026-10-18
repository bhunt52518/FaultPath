import pytest

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models import equipment, alarm




@pytest.fixture
def db_session(tmp_path):
    db_path = tmp_path / "test_faultpath.db"

    engine = create_engine(f"sqlite:///{db_path.as_posix()}")

    @event.listens_for(engine,"connect")
    def enable_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    engine.dispose()