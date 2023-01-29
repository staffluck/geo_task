from fastapi import APIRouter, Depends

from src.business_logic.task.dto.task import TaskDTO
from src.business_logic.task.services.task_service import TaskService
from src.presentation.api.v1.depends import get_task_service
from src.presentation.schemas.common import LimitOffsetQuerySchema

router = APIRouter()


@router.get("/")
async def get_tasks(
    query_filter: LimitOffsetQuerySchema = Depends(),
    task_service: TaskService = Depends(get_task_service),
) -> list[TaskDTO]:
    tasks = await task_service.get_tasks(
        limit=query_filter.limit, offset=query_filter.offset
    )
    return tasks
