from typing import AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.business_logic.task.access_policy import TaskAccessPolicy, TaskApplicationAccessPolicy
from src.business_logic.task.services.task_application import TaskApplicationService
from src.business_logic.task.services.task_service import TaskService
from src.business_logic.user.dto.auth import UserDTO
from src.business_logic.user.services.auth_service import AuthService
from src.config import SecuritySettings
from src.infrastructure.data_access.postgresql.repositories.task import TaskReader, TaskRepository
from src.infrastructure.data_access.postgresql.repositories.task_application import (
    TaskApplicationReader,
    TaskApplicationRepository,
)
from src.infrastructure.data_access.postgresql.repositories.user import UserRepository
from src.infrastructure.data_access.postgresql.uow import SQLAlchemyUoW
from src.infrastructure.managers.hash_manager import HashManager
from src.infrastructure.managers.jwt_manager import JWTManager
from src.presentation.api.depends_stub import Stub

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/signin")


async def get_session(
    sessionmaker: sessionmaker[AsyncSession] = Depends(Stub(sessionmaker)),
) -> AsyncGenerator:
    session = sessionmaker()
    async with session:
        yield session


def get_jwt_manager(
    security_settings: SecuritySettings = Depends(Stub(SecuritySettings)),
) -> JWTManager:
    return JWTManager(security_settings)


def get_hash_manager(
    security_settings: SecuritySettings = Depends(Stub(SecuritySettings)),
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
    return await auth_service.authorize_user(token)


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
    return TaskApplicationService(task_appl_uow=uow, access_policy=access_policy)
    return TaskApplicationService(task_appl_uow=uow, access_policy=access_policy)
