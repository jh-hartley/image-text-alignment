from typing import Generator

from sqlalchemy.orm import Session, sessionmaker

from .engine import engine

SessionLocal: sessionmaker = sessionmaker(engine)


def db_session() -> sessionmaker:
    return SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
