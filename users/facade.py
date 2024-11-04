from abc import ABC, abstractmethod
from . import schemas as user_schemas


class IUserFacade(ABC):

    @abstractmethod
    async def get_profile(self, user: user_schemas.UserDTO) -> user_schemas.GetProfileResponse:
        pass


class UserFacade(IUserFacade):
    """Фасад для работы с пользовательской логикой"""
    async def get_profile(self, user: user_schemas.UserDTO) -> user_schemas.GetProfileResponse:
        return user_schemas.GetProfileResponse(
            data={**user.model_dump()}
        )