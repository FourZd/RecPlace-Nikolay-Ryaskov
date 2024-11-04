from pydantic import BaseModel
from core.schemas import StatusOkSchema


class ProfileSchema(BaseModel):
    username: str


class GetProfileResponse(StatusOkSchema):
    data: ProfileSchema


class UserDTO(BaseModel):
    id: int
    username: str
    password: str

