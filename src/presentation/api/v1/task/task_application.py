from fastapi import APIRouter, Depends

from src.business_logic.task.dto.task_application import (
    TaskApplicationCreate,
    TaskApplicationDTO,
)
from src.business_logic.task.dto.user import UserDTO
from src.business_logic.task.services.task_application import TaskApplicationService
from src.presentation.api.depends_stub import Stub
from src.presentation.api.openapi_responses.v1.task_application import (
    add_application_reponses,
)
from src.presentation.api.v1.depends import get_current_user
from src.presentation.schemas.common import LimitOffsetQuerySchema
from src.presentation.schemas.task import (
    TaskApplicationCreateSchema,
    TaskApplPaginatedResponseSchema,
)

router = APIRouter(prefix="/application")


@router.post("/", responses=add_application_reponses)
async def add_application_to_task(
    task_application_data: TaskApplicationCreateSchema,
    task_appl_service: TaskApplicationService = Depends(Stub(TaskApplicationService)),
    user: UserDTO = Depends(get_current_user),
) -> TaskApplicationDTO:
    application = await task_appl_service.add_application(
        TaskApplicationCreate(
            text=task_application_data.text,
            user=UserDTO(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            ),
            task_id=task_application_data.task_id,
        )
    )
    return application


@router.get("/my")
async def get_user_task_applications(
    pagination_filter: LimitOffsetQuerySchema = Depends(),
    task_appl_service: TaskApplicationService = Depends(Stub(TaskApplicationService)),
    user: UserDTO = Depends(get_current_user),
) -> TaskApplPaginatedResponseSchema:
    task_applications = await task_appl_service.get_user_task_applications(
        user.id, limit=pagination_filter.limit, offset=pagination_filter.offset
    )
    return TaskApplPaginatedResponseSchema(
        total=len(task_applications),
        limit=pagination_filter.limit,
        offset=pagination_filter.offset,
        data=task_applications,
    )
