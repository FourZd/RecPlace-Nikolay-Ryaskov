from abc import ABC, abstractmethod
from .schemas import LoginResponse, LoginRequest, RegisterRequest, RegisterResponse
from .services import IAuthService
from users.services import IUserService
from users.exceptions import UserNotFound


class IAuthFacade(ABC):

    @abstractmethod
    async def login(self, schema: LoginRequest) -> LoginResponse:
        pass

    @abstractmethod
    async def register(self, schema: RegisterRequest) -> RegisterResponse:
        pass


class AuthFacade(IAuthFacade):

    def __init__(self, user_service: IUserService, auth_service: IAuthService):
        self.user_service = user_service
        self.auth_service = auth_service

    async def login(self, schema: LoginRequest) -> LoginResponse:
        user = await self.user_service.authenticate_and_get_user(
            schema.username, schema.password
        )

        token = await self.auth_service.create_token(user)
        return LoginResponse(data=token)

    async def register(self, schema: RegisterRequest) -> RegisterResponse:
        user = await self.user_service.register_user(schema.username, schema.password)
    
        token = await self.auth_service.create_token(user)
        return RegisterResponse(data=token)