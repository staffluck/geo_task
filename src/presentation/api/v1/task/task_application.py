from fastapi import APIRouter, Depends

from src.business_logic.task.dto.task_application import (
    TaskApplicationCreate,
    TaskApplicationDTO,
)
from src.business_logic.task.dto.user import UserDTO
from src.business_logic.task.services.task_service import TaskService
from src.presentation.api.v1.depends import get_current_user, get_task_service
from src.presentation.schemas.task import TaskApplicationCreateSchema

router = APIRouter(prefix="/application")


@router.post("/")
async def add_application_to_task(
    task_application_data: TaskApplicationCreateSchema,
    task_service: TaskService = Depends(get_task_service),
    user: UserDTO = Depends(get_current_user),
) -> TaskApplicationDTO:
    application = await task_service.add_application(
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
