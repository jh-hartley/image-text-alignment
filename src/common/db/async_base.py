from typing import Any, Generic, TypeVar, cast

from psycopg import AsyncConnection
from psycopg.rows import dict_row
from psycopg.sql import SQL, Composed

from src.common.db.psycopg_pool import ConnectionProvider

T = TypeVar("T")


class AsyncBaseRepository(Generic[T]):
    def __init__(self) -> None:
        self._pool = ConnectionProvider.async_psycopgpool()

    async def _execute(
        self, query: SQL | Composed, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        async with self._pool.connection() as raw_conn:
            conn = cast(AsyncConnection, raw_conn)
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(query, params or {})
                return await cur.fetchall()

    async def _execute_one(
        self, query: SQL | Composed, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        async with self._pool.connection() as raw_conn:
            conn = cast(AsyncConnection, raw_conn)
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(query, params or {})
                return await cur.fetchone()

    async def _execute_many(
        self, query: SQL | Composed, params_list: list[dict[str, Any]]
    ) -> None:
        async with self._pool.connection() as raw_conn:
            conn = cast(AsyncConnection, raw_conn)
            async with conn.cursor() as cur:
                await cur.executemany(query, params_list)
