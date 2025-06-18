from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import config

ASYNC_DB_URL = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    f"{'?sslmode=require' if config.DB_USE_SSL else ''}"
)
async_engine = create_async_engine(ASYNC_DB_URL, echo=False)
AsyncSessionLocal = sessionmaker(expire_on_commit=False, class_=AsyncSession)
