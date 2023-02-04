from asyncpg import IntegrityConstraintViolationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


def get_orig_exc(exc: IntegrityError) -> IntegrityConstraintViolationError:
    return exc.__cause__.__cause__  # type: ignore
