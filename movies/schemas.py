from pydantic import BaseModel
from core.schemas import StatusOkSchema
from typing import List, Optional


class MovieDTO(BaseModel):
    id: int
    name_ru: Optional[str]
    name_en: Optional[str]
    year: Optional[int]
    description: Optional[str]
    rating: Optional[float]
    poster: Optional[str]

class MovieListResponse(StatusOkSchema):
    data: List[MovieDTO]

class GetMovieResponse(StatusOkSchema):
    data: MovieDTO

class AddFavoriteRequest(BaseModel):
    kinopoisk_id: int

class AddFavoriteResponse(StatusOkSchema):
    message: str = "success.movie.added_to_favorites"
    data: MovieDTO

class RemoveFavoriteRequest(BaseModel):
    kinopoisk_id: int
