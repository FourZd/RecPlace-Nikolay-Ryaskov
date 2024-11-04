from pydantic import BaseModel
from core.schemas import StatusOkSchema
from datetime import datetime


class UserCredentialsMeta(BaseModel):
    username: str
    password: str


class LoginRequest(UserCredentialsMeta):
    pass


class RegisterRequest(UserCredentialsMeta):
    pass


class AuthTokensSchema(BaseModel):
    access_expiration: datetime
    access_token: str


class LoginResponse(StatusOkSchema):
    message: str = "success.auth.signin"
    data: AuthTokensSchema


class RegisterResponse(StatusOkSchema):
    message: str = "success.auth.signup"
    data: AuthTokensSchema

