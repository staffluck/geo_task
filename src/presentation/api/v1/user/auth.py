from fastapi import APIRouter, Depends

from src.business_logic.user.dto.auth import UserCreate, UserDTO
from src.business_logic.user.services.auth_service import AuthService
from src.presentation.api.v1.depends import get_auth_service

router = APIRouter()


@router.post("/signup", response_model=UserDTO)
async def signup(
    user_schema: UserCreate, auth_service: AuthService = Depends(get_auth_service)
) -> UserDTO:
    return await auth_service.signup(user_schema)
