from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import Provide, inject
from .facade import IUserFacade
from . import schemas as user_schemas
from auth.depends import get_current_user
from core.container import Container
from core.logger import logger


router = APIRouter(
    prefix="/users",
    tags=["/users"],
)


@router.get("/profile", response_model=user_schemas.GetProfileResponse)
@inject
async def get_profile(
    facade: IUserFacade = Depends(Provide[Container.user_facade]),
    current_user: user_schemas.UserDTO = Depends(get_current_user),
):
    """Эндпоинт для получения информации о текущем пользователе"""
    try:
        return await facade.get_profile(current_user)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="error.internal")
    
