from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.business_logic.user.entities.user import User
from src.business_logic.user.exceptions.user import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.business_logic.user.protocols.repository import IUserRepoistory
from src.infrastructure.data_access.postgresql.repositories.base import BaseRepository


class UserRepository(BaseRepository, IUserRepoistory):
    async def is_exists(self, **kwargs: str | int) -> bool:
        query = select(select(User.id).filter_by(**kwargs).exists())
        expr = await self.session.execute(query)
        return bool(expr.scalar())

    async def create_user(self, user: User) -> User:
        try:
            self.session.add(user)
            await self.session.flush()
        except IntegrityError as e:
            exc_message = str(e.__cause__)
            if "uq_user_email" in exc_message:
                raise UserAlreadyExistsError(["email"]) from e
            raise
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        query = select(User).filter(User.id == user_id)
        expr = await self.session.execute(query)
        user = expr.scalar()
        if not user:
            raise UserNotFoundError(["id"])
        return user

    async def get_user_by_email(self, email: str) -> User:
        query = select(User).filter(User.email == email)
        expr = await self.session.execute(query)
        user = expr.scalar()
        if not user:
            raise UserNotFoundError(["email"])
        return user
