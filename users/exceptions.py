class UserAlreadyExists(Exception):
    """Ошибка бизнес логики: пользователь уже существует"""
    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)


class UserNotFound(Exception):
    """Ошибка бизнес логики: пользователь не найден"""
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)