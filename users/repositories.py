from abc import ABC, abstractmethod
from core.repositories import BaseRepository
from .mappers import UserMapper
from .models import User
from .schemas import UserDTO
from sqlalchemy.future import select
from typing import Optional


class IUserRepository(BaseRepository):

    @abstractmethod
    async def get_user_by_username(self, username: str):
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int):
        pass

    @abstractmethod
    async def create_user(self, username: str, password: str) -> UserDTO:
        pass

class UserRepository(IUserRepository, BaseRepository):

    async def get_user_by_username(self, username: str) -> Optional[UserDTO]:
        async with self.get_session() as session:
            results = await session.execute(
                select(User).filter(User.username == username)
            )
            user = results.scalar()
            if user:
                return UserMapper.to_dto(user)

    async def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        async with self.get_session() as session:
            user = await session.get(User, user_id)
            if user:
                return UserMapper.to_dto(user)

    async def create_user(self, username: str, password: str) -> UserDTO:
        async with self.get_session() as session:
            user = User(username=username, password=password)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return UserMapper.to_dto(user)
