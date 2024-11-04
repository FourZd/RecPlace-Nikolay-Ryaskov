from abc import ABC, abstractmethod
from .repositories import IUserRepository
from .schemas import UserDTO
from sqlalchemy.exc import IntegrityError
from .exceptions import UserAlreadyExists, UserNotFound
from core.environment import env
import bcrypt


class IUserService(ABC):

    @abstractmethod
    async def register_user(self, username: str, password: str) -> UserDTO:
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str):
        pass

    @abstractmethod
    async def get_user_for_auth_by_id(self, user_id: int):
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int):
        pass

    @abstractmethod
    async def create_user(self, username: str, password: str) -> UserDTO:
        pass

    @abstractmethod
    async def authenticate_and_get_user(self, username: str, password: str):
        pass
    
    
class UserService(IUserService):
    
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def _get_password_hash(self, password: str) -> str:
        peppered_password = password + env.secret_key
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(peppered_password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")
    
    async def create_user(self, username: str, hashed_password: str) -> UserDTO:
        try:
            return await self.repo.create_user(username, hashed_password)
        except IntegrityError:
            raise UserAlreadyExists()

    async def register_user(self, username: str, password: str) -> UserDTO:
        hashed_password = self._get_password_hash(password)
        return await self.create_user(username, hashed_password)
        
    async def get_user_for_auth_by_id(self, user_id: int) -> UserDTO:
        """
        В тестовом задании слой лишний, но в реальном проекте здесь могли бы быть дополнительные проверки по авторизации,
        либо форматирование данных.
        """
        return await self.get_user_by_id(user_id)

    async def get_user_by_id(self, user_id: int) -> UserDTO:
        return await self.repo.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str) -> UserDTO:
        return await self.repo.get_user_by_username(username)
        
    async def authenticate_and_get_user(self, username: str, password: str) -> UserDTO:
        user = await self.get_user_by_username(username)
        if user and bcrypt.checkpw((password + env.secret_key).encode("utf-8"), user.password.encode("utf-8")):
            return user
        raise UserNotFound()