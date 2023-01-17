from fastapi import APIRouter

from src.presentation.api.v1.user.auth import router as auth_router

user_router = APIRouter(prefix="/user")
user_router.include_router(auth_router)
