from sqlmodel import SQLModel, create_engine
from backend.app.models import User, Calendar, Task


def test_create_tables():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with engine.connect() as conn:
        inspector = conn.exec_driver_sql(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = {row[0] for row in inspector}
    assert {"users", "calendars", "tasks"}.issubset(tables)
