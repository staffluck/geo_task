import logging

from fastapi import APIRouter, Depends

from src.business_logic.user.dto.auth import Token, UserCreate, UserDTO, UserSignin
from src.business_logic.user.services.auth_service import AuthService
from src.presentation.api.depends_stub import Stub
from src.presentation.api.openapi_responses.v1.user import signin_responses, signup_responses
from src.presentation.api.v1.depends import get_current_user

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/signup", responses=signup_responses)  #
async def signup(
    user_schema: UserCreate, auth_service: AuthService = Depends(Stub(AuthService))
) -> UserDTO:
    return await auth_service.signup(user_schema)


@router.post("/signin", responses=signin_responses)
async def signin(
    signin_data: UserSignin, auth_service: AuthService = Depends(Stub(AuthService))
) -> Token:
    return await auth_service.signin(signin_data)


@router.get("/check-access-token")
async def test(user: UserDTO = Depends(get_current_user)) -> str:
    return "ok"
