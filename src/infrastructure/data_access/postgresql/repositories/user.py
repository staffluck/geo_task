from sqlalchemy import select

from src.business_logic.user.entities.user import User
from src.infrastructure.data_access.postgresql.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    async def is_exists(self, **kwargs: str | int) -> bool:
        query = select(select(User.id).filter_by(**kwargs).exists())
        expr = await self.session.execute(query)
        return expr.scalar()

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        return user
