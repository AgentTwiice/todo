from sqlmodel import SQLModel, Session, create_engine

from . import models  # ensure models are registered

engine = create_engine("sqlite:///./app.db", connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
