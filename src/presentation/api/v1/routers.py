from fastapi import APIRouter

from src.presentation.api.v1.user import user_router

router = APIRouter()

router.include_router(user_router, prefix="/v1")
