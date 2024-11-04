from abc import ABC, abstractmethod
from typing import List, Optional
from .schemas import MovieDTO
from .repositories import IMovieRepository
from core.environment import env
import aiohttp
from aiocache import cached
from core.logger import logger
from sqlalchemy.exc import IntegrityError
from .exceptions import MovieNotFound, KinopoiskApiError, KinopoiskBadRequest, AlreadyInFavorites
from sqlalchemy.ext.asyncio import AsyncSession

class IMovieService(ABC):

    @abstractmethod
    async def search_movies(self, query: str) -> List[MovieDTO]:
        pass

    @abstractmethod
    async def get_movie(self, kinopoisk_id: int) -> MovieDTO:
        pass

    @abstractmethod
    async def add_movie(self, movie: MovieDTO, session):
        pass

    @abstractmethod
    async def add_favorite(self, movie_id: int, user_id: int, session):
        pass

    @abstractmethod
    async def remove_favorite(self, kinopoisk_id: int, user_id: int):
        pass

    @abstractmethod
    async def get_favorites(self, user_id: int) -> List[MovieDTO]:
        pass

    @abstractmethod
    async def get_movie_from_db(self, kinopoisk_id: int) -> MovieDTO:
        pass


class MovieService(IMovieService):

    def __init__(self, movie_repository: IMovieRepository):
        self.repo = movie_repository

    @cached(ttl=3600)
    async def search_movies(self, query: str) -> List[MovieDTO]:
        url = f"https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={query}"
        headers = {
            'X-API-KEY': f'{env.kinopoisk_api_key}'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 400:
                    raise KinopoiskBadRequest()
                elif response.status == 500:
                    raise KinopoiskApiError()
                data = await response.json()
                
                films = data.get('films', [])
                
                movie_list = [
                    MovieDTO(
                        id=film.get('filmId'),
                        name_ru=film.get('nameRu') if film.get('nameRu') and film.get('nameRu') != "null" else None,
                        name_en=film.get('nameEn') if film.get('nameEn') and film.get('nameEn') != "null" else None,
                        year=int(film.get('year')) if film.get('year') and film.get('year') != "null" else None,
                        description=film.get('description') if film.get('description') and film.get('description') != "null" else None,
                        rating=float(film.get('rating')) if film.get('rating') and film.get('rating') != "null" else None,
                        poster=film.get('posterUrl') if film.get('posterUrl') and film.get('posterUrl') != "null" else None
                    )
                    for film in films
                ]
                
                return movie_list
            
    @cached(ttl=3600)
    async def get_movie(self, kinopoisk_id: int) -> MovieDTO:
        url = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/{kinopoisk_id}"
        headers = {
            'X-API-KEY': f'{env.kinopoisk_api_key}'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 404:
                    raise MovieNotFound()
                elif response.status == 400:
                    raise KinopoiskBadRequest()
                elif response.status == 500:
                    raise KinopoiskApiError()
                
                film = await response.json()
                logger.info(f"Got movie: {response.status}")
                movie = MovieDTO(
                    id=film.get('kinopoiskId'),
                    name_ru=film.get('nameRu') if film.get('nameRu') and film.get('nameRu') != "null" else None,
                    name_en=film.get('nameEn') if film.get('nameEn') and film.get('nameEn') != "null" else None,
                    year=int(film.get('year')) if film.get('year') and film.get('year') != "null" else None,
                    description=film.get('description') if film.get('description') and film.get('description') != "null" else None,
                    rating=float(film.get('rating')) if film.get('rating') and film.get('rating') != "null" else None,
                    poster=film.get('posterUrl') if film.get('posterUrl') and film.get('posterUrl') != "null" else None
                )
                
                return movie
    
    async def add_movie(self, movie: MovieDTO, session):
        await self.repo.add_movie(movie, session)

    async def add_favorite(self, movie_id: int, user_id: int, session: Optional[AsyncSession] = None):
        try:
            await self.repo.add_favorite(movie_id, user_id, session)
        except IntegrityError as e:
            raise AlreadyInFavorites()

    async def remove_favorite(self, kinopoisk_id: int, user_id: int):
        await self.repo.remove_favorite(kinopoisk_id, user_id)

    async def get_favorites(self, user_id: int) -> List[MovieDTO]:
        return await self.repo.get_favorites(user_id)
    
    async def get_movie_from_db(self, kinopoisk_id: int) -> MovieDTO:
        return await self.repo.get_movie(kinopoisk_id)