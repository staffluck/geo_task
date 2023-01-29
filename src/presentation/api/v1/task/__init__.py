from fastapi import APIRouter

from src.presentation.api.v1.task.task import router

task_router = APIRouter(prefix="/task")
task_router.include_router(router)
