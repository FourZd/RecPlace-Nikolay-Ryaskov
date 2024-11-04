from abc import ABC, abstractmethod
from .schemas import MovieListResponse, GetMovieResponse, AddFavoriteRequest, AddFavoriteResponse
from .services import IMovieService
from users.schemas import UserDTO
from core.unit_of_work import UnitOfWork

class IMovieFacade(ABC):

    @abstractmethod
    async def search_movies(self, query: str) -> MovieListResponse:
        pass

    @abstractmethod
    async def get_movie(self, kinopoisk_id: int) -> GetMovieResponse:
        pass

    @abstractmethod
    async def add_favorite(self, schema: AddFavoriteRequest, current_user: UserDTO) -> AddFavoriteResponse:
        pass

    @abstractmethod
    async def remove_favorite(self, kinopoisk_id: int, current_user: UserDTO):
        pass

    @abstractmethod
    async def get_favorites(self, current_user: UserDTO) -> MovieListResponse:
        pass


class MovieFacade(IMovieFacade):

    def __init__(self, movie_service: IMovieService, uow: UnitOfWork):
        self.movie_service = movie_service
        self.uow = uow

    async def search_movies(self, query: str) -> MovieListResponse:
        movies = await self.movie_service.search_movies(query)
        return MovieListResponse(data=movies)
    
    async def get_movie(self, kinopoisk_id: int) -> GetMovieResponse:
        movie = await self.movie_service.get_movie(kinopoisk_id)
        return GetMovieResponse(data=movie)
    
    async def add_favorite(self, schema: AddFavoriteRequest, current_user: UserDTO) -> AddFavoriteResponse:
        movie = await self.movie_service.get_movie_from_db(schema.kinopoisk_id)
        if movie:
            await self.movie_service.add_favorite(movie.id, current_user.id)
            return AddFavoriteResponse(data=movie)
        
        movie = await self.movie_service.get_movie(schema.kinopoisk_id)
        await self.uow.begin()
        session = await self.uow.get_session()
        await self.movie_service.add_movie(movie, session)
        await self.movie_service.add_favorite(movie.id, current_user.id, session)
        await self.uow.commit()
        return AddFavoriteResponse(data=movie)
    
    async def remove_favorite(self, kinopoisk_id: int, current_user: UserDTO):
        await self.movie_service.remove_favorite(kinopoisk_id, current_user.id)

    async def get_favorites(self, current_user: UserDTO) -> MovieListResponse:
        movies = await self.movie_service.get_favorites(current_user.id)
        return MovieListResponse(data=movies)