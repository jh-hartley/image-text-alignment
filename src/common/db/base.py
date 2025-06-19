from uuid import UUID, uuid4

from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


def uuid() -> UUID:
    return uuid4()
