
class MovieNotFound(Exception):
    """Ошибка бизнес логики: фильм не найден"""
    def __init__(self, message="Movie not found"):
        self.message = message
        super().__init__(self.message)

class KinopoiskApiError(Exception):
    """Ошибка при работе с API Кинопоиска"""
    def __init__(self, message="Kinopoisk API error"):
        self.message = message
        super().__init__(self.message)

class KinopoiskBadRequest(Exception):
    """Ошибка при работе с API Кинопоиска: неверный запрос"""
    def __init__(self, message="Kinopoisk API bad request"):
        self.message = message
        super().__init__(self.message)

class AlreadyInFavorites(Exception):
    """Ошибка бизнес логики: фильм уже есть в избранном"""
    def __init__(self, message="Movie already in favorites"):
        self.message = message
        super().__init__(self.message)