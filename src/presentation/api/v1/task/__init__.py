from fastapi import APIRouter

from src.presentation.api.v1.task.task import router as root_router
from src.presentation.api.v1.task.task_application import (
    router as task_application_router,
)

task_router = APIRouter(prefix="/task", tags=["Task"])
task_router.include_router(root_router)
task_router.include_router(task_application_router)
