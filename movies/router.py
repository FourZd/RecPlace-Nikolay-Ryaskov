from fastapi import APIRouter, Depends, HTTPException, Query
from dependency_injector.wiring import Provide, inject
from core.container import Container
from core.logger import logger
from .schemas import MovieListResponse, GetMovieResponse, AddFavoriteRequest, AddFavoriteResponse
from .facade import IMovieFacade
from users.schemas import UserDTO
from auth.depends import get_current_user
from .exceptions import MovieNotFound, KinopoiskApiError, KinopoiskBadRequest, AlreadyInFavorites


router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)


@router.get("/search", response_model=MovieListResponse)
@inject
async def search_movies(
    query: str = Query(..., min_length=1, description="Параметр для поиска фильмов по названию"),
    movie_facade: IMovieFacade = Depends(Provide[Container.movie_facade]),
    current_user: UserDTO = Depends(get_current_user)
):
    """Эндпоинт для поиска фильмов по названию при помощи API Кинопоиска"""
    try:
        return await movie_facade.search_movies(query)
    except KinopoiskApiError:
        raise HTTPException(status_code=500, detail="error.kinopoisk.internal_error")
    except KinopoiskBadRequest:
        raise HTTPException(status_code=400, detail="error.kinopoisk.bad_request")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="error.internal")
    

@router.get("/{kinopoisk_id:int}", response_model=GetMovieResponse)
@inject
async def get_movie(
    kinopoisk_id: int,
    movie_facade: IMovieFacade = Depends(Provide[Container.movie_facade]),
    current_user: UserDTO = Depends(get_current_user)
):
    """Эндпоинт для получения информации о фильме по его ID в Кинопоиске"""
    try:
        return await movie_facade.get_movie(kinopoisk_id)
    except MovieNotFound:
        raise HTTPException(status_code=404, detail="error.movie.not_found")
    except KinopoiskApiError:
        raise HTTPException(status_code=500, detail="error.kinopoisk.internal_error")
    except KinopoiskBadRequest:
        raise HTTPException(status_code=400, detail="error.kinopoisk.bad_request")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="error.internal")
    

@router.post("/favorites", response_model=AddFavoriteResponse)
@inject
async def add_favorite(
    schema: AddFavoriteRequest,
    movie_facade: IMovieFacade = Depends(Provide[Container.movie_facade]),
    current_user: UserDTO = Depends(get_current_user)
):
    """Эндпоинт для добавления фильма в избранное. Если фильм уже есть в локальной базе, то добавляется только связь с пользователем"""
    try:
        return await movie_facade.add_favorite(schema, current_user)
    except MovieNotFound:
        raise HTTPException(status_code=404, detail="error.movie.not_found")
    except AlreadyInFavorites:
        raise HTTPException(status_code=400, detail="error.movie.already_in_favorites")
    except KinopoiskApiError:
        raise HTTPException(status_code=500, detail="error.kinopoisk.internal_error")
    except KinopoiskBadRequest:
        raise HTTPException(status_code=400, detail="error.kinopoisk.bad_request")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="error.internal")
    

@router.delete("/favorites/{kinopoisk_id:int}")
@inject
async def remove_favorite(
    kinopoisk_id: int,
    movie_facade: IMovieFacade = Depends(Provide[Container.movie_facade]),
    current_user: UserDTO = Depends(get_current_user)
):
    """Эндпоинт для удаления фильма из избранного. Сам фильм остается в бд и доступен для других пользователей"""
    try:
        await movie_facade.remove_favorite(kinopoisk_id, current_user)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="error.internal")
    

@router.get("/favorites", response_model=MovieListResponse)
@inject
async def get_favorites(
    movie_facade: IMovieFacade = Depends(Provide[Container.movie_facade]),
    current_user: UserDTO = Depends(get_current_user)
):
    """Эндпоинт для получения списка избранных фильмов пользователя"""
    try:
        return await movie_facade.get_favorites(current_user)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="error.internal")
    