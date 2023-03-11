from typing import List

from geoalchemy2 import func
from geoalchemy2.functions import ST_DistanceSphere  # type: ignore
from pydantic import parse_obj_as
from sqlalchemy import delete, select
from sqlalchemy.exc import NoResultFound

from src.business_logic.task.dto.task import TaskDetail, TaskFilterByGeo
from src.business_logic.task.dto.task_application import TaskApplicationDTO
from src.business_logic.task.dto.user import UserDTO
from src.business_logic.task.entities.task import Task
from src.business_logic.task.entities.task_application import TaskApplication
from src.business_logic.task.entities.user import User
from src.business_logic.task.exceptions.task import TaskNotFoundError
from src.business_logic.task.protocols.repository import ITaskReader, ITaskRepository
from src.infrastructure.data_access.postgresql.repositories.base import BaseRepository
from src.infrastructure.data_access.postgresql.tables.city import city_table


class TaskReader(BaseRepository, ITaskReader):
    async def get_task_detail(self, task_id: int) -> TaskDetail:
        query = select(Task, User).join(User, User.id == Task.owner_id).filter(Task.id == task_id)
        try:
            expr = await self.session.execute(query)
            data = expr.one()
        except NoResultFound as e:
            raise TaskNotFoundError(["id"]) from e
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
            city_name=task.city_name,
        )

    async def get_task_applications_by_task_id(
        self, task_id: int, limit: int = 100, offset: int = 0
    ) -> list[TaskApplicationDTO]:
        query = (
            select(TaskApplication)
            .filter(TaskApplication.task_id == task_id)
            .limit(limit)
            .offset(offset)
        )
        expr = await self.session.execute(query)
        return parse_obj_as(List[TaskApplicationDTO], expr.scalars().all())


class TaskRepository(BaseRepository, ITaskRepository):
    async def is_exists(self, **kwargs: str | int) -> bool:
        query = select(select(Task.id).filter_by(**kwargs).exists())
        expr = await self.session.execute(query)
        return bool(expr.scalar())

    async def create_task(self, task: Task) -> Task:
        task.geo = self._build_point(task)
        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)
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
        self, filters: TaskFilterByGeo, radius: int, limit: int = 100, offset: int = 0
    ) -> list[Task]:
        current_geo_point = func.ST_Point(filters.current_geo.long, filters.current_geo.lat)
        query = (
            select(Task)
            .filter(ST_DistanceSphere(Task.geo, current_geo_point) <= radius)
            .limit(limit)
            .offset(offset)
        )
        expr = await self.session.execute(query)
        return expr.scalars().all()

    async def delete_task(self, task_id: int) -> None:
        query = delete(Task).filter(Task.id == task_id)
        await self.session.execute(query)

    async def update_task(self, task: Task) -> Task:
        task.geo = self._build_point(task)
        self.session.add(task)
        await self.session.flush()
        return task

    def _build_point(self, task: Task) -> str:
        return f"POINT({task.long} {task.lat})"

    async def get_nearest_city_name(self, lat: float, long: float) -> str:
        point = func.ST_Point(long, lat)
        distance = func.ST_Distance(city_table.c.geo, point).label("test")
        query = select(city_table.c.name).filter(
            distance == select(func.min(func.ST_Distance(city_table.c.geo, point)))
        )
        expr = await self.session.execute(query)
        return str(expr.scalar())
