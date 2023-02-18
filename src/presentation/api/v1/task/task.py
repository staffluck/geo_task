from fastapi import APIRouter, Depends, status

from src.business_logic.task.dto.task import (
    GeoLocation,
    TaskCreate,
    TaskDetail,
    TaskDTO,
    TaskFilterByGeo,
    TaskUpdate,
)
from src.business_logic.task.dto.user import UserDTO
from src.business_logic.task.services.task_service import TaskService
from src.presentation.api.v1.depends import get_current_user, get_task_service
from src.presentation.schemas.common import LimitOffsetQuerySchema
from src.presentation.schemas.task import (
    TaskCreateSchema,
    TaskFilterByGeoQuerySchema,
    TaskPaginatedResponseSchema,
    TaskUpdateSchema,
)

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
            owner=UserDTO(
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
) -> TaskPaginatedResponseSchema:
    tasks = await task_service.get_tasks(
        limit=pagination_filter.limit,
        offset=pagination_filter.offset,
    )
    return TaskPaginatedResponseSchema(
        total=len(tasks),
        limit=pagination_filter.limit,
        offset=pagination_filter.offset,
        data=tasks,
    )


@router.get("/near")
async def get_near_tasks(
    pagination_filter: LimitOffsetQuerySchema = Depends(),
    query_filter: TaskFilterByGeoQuerySchema = Depends(),
    task_service: TaskService = Depends(get_task_service),
) -> TaskPaginatedResponseSchema:
    tasks = await task_service.get_near_tasks(
        TaskFilterByGeo(
            current_geo=GeoLocation(long=query_filter.long, lat=query_filter.lat)
        ),
        limit=pagination_filter.limit,
        offset=pagination_filter.offset,
    )
    return TaskPaginatedResponseSchema(
        total=len(tasks),
        limit=pagination_filter.limit,
        offset=pagination_filter.offset,
        data=tasks,
    )


@router.get("/{task_id}")
async def get_task_detail(
    task_id: int, task_service: TaskService = Depends(get_task_service)
) -> TaskDetail:
    task = await task_service.get_task_detail(task_id)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
    user: UserDTO = Depends(get_current_user),
) -> None:
    await task_service.delete_task(task_id)


@router.patch("/{task_id}")
async def update_task(
    task_id: int,
    task_data: TaskUpdateSchema,
    task_service: TaskService = Depends(get_task_service),
    user: UserDTO = Depends(get_current_user),
) -> TaskDTO:
    task = await task_service.update_task(TaskUpdate(task_id=task_id, **task_data))
    return task
