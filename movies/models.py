from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import String, Numeric, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import BaseModel


class Movie(BaseModel):
    """
        Таблица сохранённых фильмов. 
        В роли ID используется айдишник фильма из АПИ кинопоиска.
        Реализовано, чтобы не запрашивать кинопоиск каждый раз, а проверять, существует ли запись в локальной бд.
    """
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    name_ru: Mapped[str] = mapped_column(String(255), nullable=True)
    name_en: Mapped[str] = mapped_column(String(255), nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)
    rating: Mapped[float] = mapped_column(Numeric, nullable=True)
    poster: Mapped[str] = mapped_column(String(255), nullable=True)


class UserFavoriteMovie(BaseModel):
    """Таблица M2M избранных фильмов"""
    __tablename__ = "favorite_movies"
    __table_args__ = (UniqueConstraint('user_id', 'movie_id', name='unique_user_movie'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

