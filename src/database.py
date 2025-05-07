from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from fastapi import Depends
from typing import Annotated

from src.config import settings

engine = create_async_engine(settings.db_url)

session_factory = async_sessionmaker(engine)


async def get_db():
    async with session_factory() as session:
        yield session


db_dep = Annotated[AsyncSession, Depends(get_db)]


class Base(DeclarativeBase):
    def __str__(self):
        return f"{self.__name__}(**{self.__dict__.items()})"
