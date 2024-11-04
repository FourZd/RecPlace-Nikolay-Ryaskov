from .models import Movie
from .schemas import MovieDTO


class MovieMapper:
    @staticmethod
    def to_dto(movie: Movie) -> MovieDTO:
        return MovieDTO(
            id=movie.id,
            name_ru=movie.name_ru,
            name_en=movie.name_en,
            year=movie.year,
            description=movie.description,
            rating=movie.rating,
            poster=movie.poster,
        )

    @staticmethod
    def to_orm(movie: MovieDTO) -> Movie:
        return Movie(
            id=movie.id,
            name_ru=movie.name_ru,
            name_en=movie.name_en,
            year=movie.year,
            description=movie.description,
            rating=movie.rating,
            poster=movie.poster,
        )