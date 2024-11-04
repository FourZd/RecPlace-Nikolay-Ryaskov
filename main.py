from fastapi import FastAPI
from core.container import Container
from auth.router import router as auth_router
from users.router import router as users_router
from movies.router import router as movies_router
from core import exception_handlers as exception_handlers
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError, HTTPException

app = FastAPI()
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(movies_router)
container = Container()
container.init_resources()
container.wire(modules=[__name__])

app.add_exception_handler(RequestValidationError, exception_handlers.validation_exception_handler)
app.add_exception_handler(HTTPException, exception_handlers.http_exception_handler)
app.add_exception_handler(StarletteHTTPException, exception_handlers.starlette_exception_handler)