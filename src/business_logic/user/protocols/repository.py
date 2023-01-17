from typing import Protocol

from src.business_logic.user.entities.user import User


class IUserRepoistory(Protocol):
    async def create_user(self, user: User) -> User:
        ...

    async def is_exists(self, **kwargs: str | int) -> User:
        ...
