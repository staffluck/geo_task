from fastapi import APIRouter, Depends

from src.business_logic.task.dto.task import GeoLocation, TaskDTO, TaskFilterByGeo
from src.business_logic.task.services.task_service import TaskService
from src.presentation.api.v1.depends import get_task_service
from src.presentation.schemas.common import LimitOffsetQuerySchema
from src.presentation.schemas.task import TaskFilterByGeoQuerySchema

router = APIRouter()


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
