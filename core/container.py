from dependency_injector import containers, providers

from auth.facade import AuthFacade
from auth.services import AuthService
from core.database import Database
from core.environment import env
from core.unit_of_work import UnitOfWork
from users.facade import UserFacade
from users.repositories import UserRepository
from users.services import UserService
from movies.facade import MovieFacade
from movies.services import MovieService
from movies.repositories import MovieRepository

class Container(containers.DeclarativeContainer):
    """Контейнер зависимостей. Simple as that :)"""
    wiring_config = containers.WiringConfiguration(
        modules=[
            "auth.router",
            "auth.depends",
            "users.router",
            "movies.router"
        ]
    )

    db = providers.Singleton(
        Database,
        db_url=f"{env.DATABASE_DIALECT}+asyncpg://{env.POSTGRES_USER}:{env.POSTGRES_PASSWORD}@{env.POSTGRES_HOSTNAME}:{env.POSTGRES_PORT}/{env.POSTGRES_DB}",
    )
    unit_of_work = providers.Factory(UnitOfWork, session_factory=db.provided.session)
    user_repository = providers.Factory(
        UserRepository, session_factory=db.provided.session
    )
    movie_repository = providers.Factory(
        MovieRepository, session_factory=db.provided.session
    )

    auth_service = providers.Factory(AuthService)
    user_service = providers.Factory(UserService, repo=user_repository)
    movie_service = providers.Factory(MovieService, movie_repository=movie_repository)

    auth_facade = providers.Factory(
        AuthFacade, user_service=user_service, auth_service=auth_service
    )
    user_facade = providers.Factory(
        UserFacade
    )
    movie_facade = providers.Factory(
        MovieFacade, movie_service=movie_service, uow=unit_of_work
    )