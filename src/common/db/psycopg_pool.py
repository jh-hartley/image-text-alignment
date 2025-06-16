from typing import Any, cast

from psycopg_pool import ConnectionPool
from psycopg_pool.pool_async import AsyncConnectionPool

from src.config import config


class ConnectionProvider:
    @staticmethod
    def psycopgpool() -> ConnectionPool[Any]:
        connection_kwargs = {
            "autocommit": True,
            "prepare_threshold": 0,
        }
        pool = ConnectionPool(
            conninfo=ConnectionProvider.connection_url(),
            max_size=config.DB_POOL_SIZE,
            kwargs=connection_kwargs,
        )
        return cast(ConnectionPool[Any], pool)

    @staticmethod
    def async_psycopgpool() -> AsyncConnectionPool[Any]:
        connection_kwargs = {
            "autocommit": True,
            "prepare_threshold": 0,
        }
        pool = AsyncConnectionPool(
            conninfo=ConnectionProvider.connection_url(),
            max_size=config.DB_ASYNC_POOL_SIZE,
            kwargs=connection_kwargs,
        )
        return cast(AsyncConnectionPool[Any], pool)

    @staticmethod
    def connection_url() -> str:
        conninfo = (
            f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}"
            f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
        )
        if config.DB_USE_SSL:
            conninfo += "?sslmode=require"
        return conninfo
