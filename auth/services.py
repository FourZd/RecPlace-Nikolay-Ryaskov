from abc import ABC, abstractmethod
from .schemas import AuthTokensSchema
from datetime import datetime, timezone, timedelta
from users import schemas as user_schemas
from core.environment import env
import jwt


class IAuthService(ABC):

    @abstractmethod
    async def create_token(self, user) -> AuthTokensSchema:
        pass

    @abstractmethod
    async def validate_token(self, token):
        pass


class AuthService(IAuthService):

    def _add_padding_to_jwt(self, token: str) -> str:
        """Добавляем паддинг для корректной длины токена"""
        token += "=" * (4 - len(token) % 4)
        return token
    
    async def _create_access_token(self, user: user_schemas.UserDTO) -> tuple[str, datetime]:
        expiration_datetime = datetime.now(timezone.utc) + timedelta(
            minutes=env.access_token_lifetime
        )

        payload = {
            "exp": expiration_datetime,
            "id": user.id,
        }
        access_token = jwt.encode(payload, env.secret_key, algorithm=env.jwt_algorithm)
        access_token_padded = self._add_padding_to_jwt(access_token)
        return access_token_padded, expiration_datetime
    
    async def create_token(self, user) -> AuthTokensSchema:
        access_token, access_expiration = await self._create_access_token(user)

        return AuthTokensSchema(
            access_token=access_token,
            access_expiration=access_expiration,
        )

    async def validate_token(self, token):
        pass