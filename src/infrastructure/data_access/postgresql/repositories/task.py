from typing import NoReturn

from geoalchemy2 import func
from geoalchemy2.functions import ST_DistanceSphere  # type: ignore
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.business_logic.task.dto.task import TaskDetail, TaskFilterByGeo
from src.business_logic.task.dto.user import UserDTO
from src.business_logic.task.entities.task import Task
from src.business_logic.task.entities.task_application import TaskApplication
from src.business_logic.task.entities.user import User
from src.business_logic.task.exceptions.task import TaskNotFoundError
from src.business_logic.task.protocols.repository import ITaskReader, ITaskRepository
from src.infrastructure.data_access.postgresql.repositories.base import (
    BaseRepository,
    get_orig_exc,
)


# fk_task_application_task_id_task
def handle_foreign_constraint(exc: IntegrityError, field: str) -> NoReturn:
    raise TaskNotFoundError(fields=[field]) from exc


CONSTRAINT_TO_HANDLE = {"fk_task_application_task_id_task": handle_foreign_constraint}


class TaskReader(BaseRepository, ITaskReader):
    async def get_task_detail(self, task_id: int) -> TaskDetail:
        query = (
            select(Task, User)
            .join(User, User.id == Task.owner_id)
            .filter(Task.id == task_id)
        )
        try:
            expr = await self.session.execute(query)
            data = expr.one()
        except NoResultFound:
            raise TaskNotFoundError(["id"])
        task: Task = data[0]
        task_owner: User = data[1]
        return TaskDetail(
            title=task.title,
            description=task.description,
            reward=task.reward,
            long=task.long,
            lat=task.lat,
            id=task.id,
            owner=UserDTO.from_orm(task_owner),
        )


class TaskRepository(BaseRepository, ITaskRepository):
    async def is_exists(self, **kwargs: str | int) -> bool:
        query = select(select(Task.id).filter_by(**kwargs).exists())
        expr = await self.session.execute(query)
        return bool(expr.scalar())

    async def create_task(self, task: Task) -> Task:
        task.geo = f"POINT({task.long} {task.lat})"
        self.session.add(task)
        await self.session.flush()
        return task

    async def get_task_by_id(self, task_id: int) -> Task:
        query = select(Task).filter(Task.id == task_id)
        expr = await self.session.execute(query)
        task = expr.scalar()
        if not task:
            raise TaskNotFoundError(["id"])
        return task

    async def get_tasks(self, limit: int = 100, offset: int = 0) -> list[Task]:
        query = select(Task).limit(limit).offset(offset)
        expr = await self.session.execute(query)
        return expr.scalars().all()

    async def get_tasks_in_radius(
        self, filter: TaskFilterByGeo, radius: int, limit: int = 100, offset: int = 0
    ) -> list[Task]:
        current_geo_point = func.ST_Point(
            filter.current_geo.long, filter.current_geo.lat
        )
        query = (
            select(Task)
            .filter(ST_DistanceSphere(Task.geo, current_geo_point) <= radius)
            .limit(limit)
            .offset(offset)
        )
        expr = await self.session.execute(query)
        return expr.scalars().all()

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

    async def add_aplication(
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
        return task_application
