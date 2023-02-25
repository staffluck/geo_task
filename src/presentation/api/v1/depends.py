from typing import AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.business_logic.task.access_policy import (
    TaskAccessPolicy,
    TaskApplicationAccessPolicy,
)
from src.business_logic.task.services.task_application import TaskApplicationService
from src.business_logic.task.services.task_service import TaskService
from src.business_logic.user.dto.auth import UserDTO
from src.business_logic.user.services.auth_service import AuthService
from src.config import (
    DatabaseSettings,
    SecuritySettings,
    database_settings,
    security_settings,
)
from src.infrastructure.data_access.postgresql.db import Session
from src.infrastructure.data_access.postgresql.repositories.task import (
    TaskReader,
    TaskRepository,
)
from src.infrastructure.data_access.postgresql.repositories.task_application import (
    TaskApplicationReader,
    TaskApplicationRepository,
)
from src.infrastructure.data_access.postgresql.repositories.user import UserRepository
from src.infrastructure.data_access.postgresql.uow import SQLAlchemyUoW
from src.infrastructure.managers.hash_manager import HashManager
from src.infrastructure.managers.jwt_manager import JWTManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signin")


async def get_session() -> AsyncGenerator:
    session = Session()
    try:
        yield session
    finally:
        await session.rollback()


def get_db_settings() -> DatabaseSettings:
    return database_settings


def get_security_settings() -> SecuritySettings:
    return security_settings


def get_jwt_manager(
    security_settings: SecuritySettings = Depends(get_security_settings),
) -> JWTManager:
    return JWTManager(security_settings)


def get_hash_manager(
    security_settings: SecuritySettings = Depends(get_security_settings),
) -> HashManager:
    return HashManager(security_settings)


def get_uow(session: AsyncSession = Depends(get_session)) -> SQLAlchemyUoW:
    return SQLAlchemyUoW(
        session=session,
        user_repo=UserRepository,
        task_repo=TaskRepository,
        task_reader=TaskReader,
        task_appl=TaskApplicationRepository,
        task_appl_reader=TaskApplicationReader,
    )


def get_auth_service(
    uow: SQLAlchemyUoW = Depends(get_uow),
    jwt_manager: JWTManager = Depends(get_jwt_manager),
    hash_manager: HashManager = Depends(get_hash_manager),
) -> AuthService:
    return AuthService(
        jwt_manager=jwt_manager,
        hash_manager=hash_manager,
        user_uow=uow,
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserDTO:
    user = await auth_service.authorize_user(token)
    return user


def get_task_access_policy(
    user: UserDTO = Depends(get_current_user),
) -> TaskAccessPolicy:
    return TaskAccessPolicy(user)


def get_task_service(
    uow: SQLAlchemyUoW = Depends(get_uow),
    access_policy: TaskAccessPolicy = Depends(get_task_access_policy),
) -> TaskService:
    return TaskService(task_uow=uow, access_policy=access_policy)


def get_task_appl_access_policy(
    user: UserDTO = Depends(get_current_user),
) -> TaskApplicationAccessPolicy:
    return TaskApplicationAccessPolicy(user)


def get_task_appl_service(
    uow: SQLAlchemyUoW = Depends(get_uow),
    access_policy: TaskApplicationAccessPolicy = Depends(get_task_access_policy),
) -> TaskApplicationService:
    return TaskApplicationService(task_uow=uow, access_policy=access_policy)
