from abc import ABC, abstractmethod
from core.repositories import BaseRepository
from .schemas import MovieDTO
from typing import List, Optional
from sqlalchemy import insert, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import UserFavoriteMovie, Movie
from .mappers import MovieMapper
from core.logger import logger

class IMovieRepository(ABC):

    @abstractmethod
    async def add_favorite(self, movie_id: int, user_id: int, external_session: Optional[AsyncSession] = None):
        pass

    @abstractmethod
    async def remove_favorite(self, movie_id: int, user_id: int):
        pass

    @abstractmethod
    async def get_favorites(self, user_id: int) -> List[MovieDTO]:
        pass

    @abstractmethod
    async def get_movie(self, movie_id: int) -> MovieDTO:
        pass

    @abstractmethod
    async def add_movie(self, movie: MovieDTO, session: AsyncSession):
        pass
    

    
class MovieRepository(IMovieRepository, BaseRepository):
    
    async def add_favorite(self, movie_id: int, user_id: int, external_session: Optional[AsyncSession] = None):
        async with self.get_session(external_session) as session:
            await session.execute(
                insert(UserFavoriteMovie).values(user_id=user_id, movie_id=movie_id)
            )
            if external_session:
                await session.flush()
            else:
                await session.commit()

    async def remove_favorite(self, movie_id: int, user_id: int):
        async with self.get_session() as session:
            await session.execute(
                delete(UserFavoriteMovie).where(
                    UserFavoriteMovie.user_id == user_id, UserFavoriteMovie.movie_id == movie_id
                )
            )
            await session.commit()

    async def get_favorites(self, user_id: int) -> List[MovieDTO]:
        async with self.get_session() as session:
            result = await session.execute(
                select(Movie)
                .join(UserFavoriteMovie, UserFavoriteMovie.movie_id == Movie.id)
                .where(UserFavoriteMovie.user_id == user_id)
                .order_by(UserFavoriteMovie.created_at.desc())
            )
            movies = result.scalars().all()
            return [MovieMapper.to_dto(movie) for movie in movies]

    async def get_movie(self, movie_id: int) -> Optional[MovieDTO]:
        async with self.get_session() as session:
            result = await session.execute(
                select(Movie).where(Movie.id == movie_id)
            )
            movie = result.scalar()
            if movie:
                return MovieMapper.to_dto(movie)
            
    async def add_movie(self, movie: MovieDTO, external_session: AsyncSession):
        async with self.get_session(external_session) as session:
            session.add(MovieMapper.to_orm(movie))
            logger.info(f"Adding movie {movie.name_ru} with id {movie.id}")
            if external_session:
                await session.flush()
            else:
                await session.commit()
            