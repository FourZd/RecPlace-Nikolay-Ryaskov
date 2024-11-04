from .models import User
from .schemas import UserDTO


class UserMapper:
    @staticmethod
    def to_dto(entity: User) -> UserDTO:
        return UserDTO(
            id=entity.id,
            username=entity.username,
            password=entity.password
        )