from fastapi import APIRouter, Depends

from src.business_logic.user.dto.auth import Token, UserCreate, UserDTO, UserSignin
from src.business_logic.user.services.auth_service import AuthService
from src.presentation.api.v1.depends import get_auth_service, get_current_user

router = APIRouter()


@router.post("/signup", response_model=UserDTO)
async def signup(
    user_schema: UserCreate, auth_service: AuthService = Depends(get_auth_service)
) -> UserDTO:
    return await auth_service.signup(user_schema)


@router.post("/signin", response_model=Token)
async def signin(
    signin_data: UserSignin, auth_service: AuthService = Depends(get_auth_service)
) -> Token:
    return await auth_service.signin(signin_data)


@router.get("/check-access-token")
async def test(user: UserDTO = Depends(get_current_user)) -> str:
    return "ok"
