from pydantic import BaseModel


class StatusOkSchema(BaseModel):
    status: str = "ok"