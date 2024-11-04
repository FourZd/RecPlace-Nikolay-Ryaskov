from datetime import datetime, timezone
import jwt
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.environment import env
from core.exceptions import AuthError
from users import schemas as user_schemas
from core.logger import logger


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthError(detail="error.auth.scheme.invalid")
            if not self.verify_jwt(credentials.credentials):
                raise AuthError(detail="error.auth.token.invalid")
            return credentials.credentials
        else:
            return None

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = JWTBearer.decode_jwt(jwt_token)
        except Exception:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid

    @staticmethod
    def decode_jwt(token: str) -> dict:
        try:
            decoded_token = jwt.decode(
                token, env.secret_key, algorithms=[env.jwt_algorithm]
            )
            return (
                decoded_token
                if decoded_token["exp"]
                >= int(round(datetime.now(timezone.utc).timestamp()))
                else None
            )
        except Exception:
            logger.error("An error occurred while decoding token", exc_info=True)
            return {}