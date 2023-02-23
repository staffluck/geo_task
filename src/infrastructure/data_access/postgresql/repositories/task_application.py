from typing import NoReturn

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.business_logic.task.entities.task_application import TaskApplication
from src.business_logic.task.exceptions.task import TaskNotFoundError
from src.business_logic.task.protocols.repository import (
    ITaskApplicationReader,
    ITaskApplicationRepository,
)
from src.infrastructure.data_access.postgresql.repositories.base import (
    BaseRepository,
    get_orig_exc,
)


# fk_task_application_task_id_task
def handle_foreign_constraint(exc: IntegrityError, field: str) -> NoReturn:
    raise TaskNotFoundError(fields=[field]) from exc


CONSTRAINT_TO_HANDLE = {"fk_task_application_task_id_task": handle_foreign_constraint}


class TaskApplicationRepository(BaseRepository, ITaskApplicationRepository):
    async def user_has_application(self, user_id: int, task_id: int) -> bool:
        query = select(
            select(TaskApplication.id)
            .filter(
                TaskApplication.task_id == task_id, TaskApplication.user_id == user_id
            )
            .exists()
        )
        expr = await self.session.execute(query)
        return bool(expr.scalar())

    async def create_application(
        self, task_application: TaskApplication
    ) -> TaskApplication:
        try:
            self.session.add(task_application)
            await self.session.flush()
        except IntegrityError as e:
            exc = get_orig_exc(e)
            if exc.constraint_name in CONSTRAINT_TO_HANDLE:
                CONSTRAINT_TO_HANDLE[exc.constraint_name](e, "id")
            raise
        await self.session.refresh(task_application)
        return task_application


class TaskApplicationReader(BaseRepository, ITaskApplicationReader):
    ...
