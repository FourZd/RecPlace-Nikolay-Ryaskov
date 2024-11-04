from typing import Any, Optional

from fastapi import HTTPException, status


class AuthError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Optional[dict[str, Any]] = None
    ) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, headers)