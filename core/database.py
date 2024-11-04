from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Callable

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=True)
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
        )

    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractAsyncContextManager[AsyncSession]]:
        # Генерация новой сессии для каждого запроса
        async with self._session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
