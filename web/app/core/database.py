from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from fastapi import Depends
from typing import Annotated

from app.core.config import settings

engine = create_async_engine(settings.db_url, echo=False)

session_factory = async_sessionmaker(engine)


class Base(DeclarativeBase):
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    def __str__(self):
        return self.__repr__()
