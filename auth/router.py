from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import Provide, inject
from auth.facade import IAuthFacade
from core.container import Container
from .schemas import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from users.exceptions import UserNotFound, UserAlreadyExists
from core.logger import logger

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=LoginResponse)
@inject
async def login(
    schema: LoginRequest,
    facade: IAuthFacade = Depends(Provide[Container.auth_facade]),
):
    """Эндпоинт для авторизации пользователя"""
    try:
        return await facade.login(schema)
    except UserNotFound:
        raise HTTPException(status_code=400, detail="error.auth.user_not_found")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="error.internal")
    

@router.post("/register", response_model=RegisterResponse)
@inject
async def register(
    schema: RegisterRequest,
    facade: IAuthFacade = Depends(Provide[Container.auth_facade]),
):
    """Эндпоинт для регистрации нового пользователя"""
    try:
        return await facade.register(schema)
    except UserAlreadyExists:
        raise HTTPException(status_code=400, detail="error.auth.user_already_exists")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="error.internal")