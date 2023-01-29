from fastapi import APIRouter

from src.presentation.api.v1.task import task_router
from src.presentation.api.v1.user import user_router

router = APIRouter(prefix="/v1")

router.include_router(user_router)
router.include_router(task_router)
