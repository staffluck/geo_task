from fastapi import APIRouter, Depends

from src.business_logic.task.dto.task import (
    GeoLocation,
    TaskCreate,
    TaskDTO,
    TaskFilterByGeo,
)
from src.business_logic.task.dto.user import TaskOwnerDTO
from src.business_logic.task.services.task_service import TaskService
from src.business_logic.user.dto.auth import UserDTO
from src.presentation.api.v1.depends import get_current_user, get_task_service
from src.presentation.schemas.common import LimitOffsetQuerySchema
from src.presentation.schemas.task import TaskCreateSchema, TaskFilterByGeoQuerySchema

router = APIRouter()


@router.post("/")
async def create_task(
    task_data: TaskCreateSchema,
    task_service: TaskService = Depends(get_task_service),
    user: UserDTO = Depends(get_current_user),
) -> TaskDTO:
    task = await task_service.create_task(
        TaskCreate(
            title=task_data.title,
            description=task_data.description,
            reward=task_data.reward,
            long=task_data.long,
            lat=task_data.lat,
            owner=TaskOwnerDTO(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            ),
        )
    )
    return task


@router.get("/")
async def get_tasks(
    pagination_filter: LimitOffsetQuerySchema = Depends(),
    task_service: TaskService = Depends(get_task_service),
) -> list[TaskDTO]:
    tasks = await task_service.get_tasks(
        limit=pagination_filter.limit,
        offset=pagination_filter.offset,
    )
    return tasks


@router.get("/near")
async def get_near_tasks(
    pagination_filter: LimitOffsetQuerySchema = Depends(),
    query_filter: TaskFilterByGeoQuerySchema = Depends(),
    task_service: TaskService = Depends(get_task_service),
) -> list[TaskDTO]:
    tasks = await task_service.get_near_tasks(
        TaskFilterByGeo(
            current_geo=GeoLocation(long=query_filter.long, lat=query_filter.lat)
        ),
        limit=pagination_filter.limit,
        offset=pagination_filter.offset,
    )
    return tasks
