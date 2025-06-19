from typing import Any

from pgvector.psycopg2 import register_vector
from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine

from src.config import config


def setup_database() -> Engine:
    engine = create_engine(
        f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}"
        f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
        f'{"" if not config.DB_USE_SSL else "?sslmode=require"}',
        pool_size=config.DB_POOL_SIZE,
        max_overflow=config.DB_MAX_OVERFLOW,
    )

    with engine.connect() as connection:
        connection.execute(text("SELECT pg_advisory_lock(123456)"))
        try:
            result = connection.execute(
                text("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
            )
            if not result.scalar():
                connection.execute(
                    text("CREATE EXTENSION IF NOT EXISTS vector")
                )
                connection.commit()
        finally:
            connection.execute(text("SELECT pg_advisory_unlock(123456)"))

    return engine


engine = setup_database()


@event.listens_for(engine, "connect", propagate=True)  # type: ignore[misc]
def connect(dbapi_connection: Any, _: Any) -> None:
    register_vector(dbapi_connection, arrays=True)
