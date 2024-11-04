from typing import Optional

import jwt
from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from core.container import Container
from core.environment import env
from core.exceptions import AuthError
from users import schemas as user_schemas
from users.services import IUserService
from .auth_handlers import JWTBearer
from core.logger import logger


@inject
async def get_current_user(
    user_service: IUserService = Depends(Provide[Container.user_service]),
    token: Optional[str] = Depends(JWTBearer()),
) -> user_schemas.UserDTO:
    logger.warning(f"fefe {token}")
    if not token:
        raise AuthError(detail="error.auth.token_not_provided")
    payload = jwt.decode(token, env.secret_key, algorithms=[env.jwt_algorithm])
    current_user: user_schemas.UserDTO = await user_service.get_user_for_auth_by_id(payload["id"])
    if not current_user:
        raise AuthError(detail="error.auth.user.not_found")
    return current_user