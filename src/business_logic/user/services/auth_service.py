from src.business_logic.common.exceptions import BadJWTTokenError
from src.business_logic.user.dto.auth import (
    AccessTokenData,
    RefreshTokenData,
    Token,
    UserCreate,
    UserDTO,
    UserSignin,
)
from src.business_logic.user.entities.user import User
from src.business_logic.user.exceptions.auth import BadCredentialsError
from src.business_logic.user.exceptions.user import UserNotFoundError
from src.business_logic.user.protocols.security import IHashManager, IJWTManager
from src.business_logic.user.protocols.uow import IUserUoW


class AuthService:
    def __init__(
        self,
        jwt_manager: IJWTManager,
        hash_manager: IHashManager,
        user_uow: IUserUoW,
    ) -> None:
        self.jwt_manager = jwt_manager
        self.hash_manager = hash_manager
        self.user_uow = user_uow

    async def signup(self, user_data: UserCreate) -> UserDTO:
        user = User.create(
            email=user_data.email,
            password=self.hash_manager.get_hash(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )
        user = await self.user_uow.user.create_user(user)
        await self.user_uow.commit()
        return UserDTO.from_orm(user)

    async def signin(self, login_data: UserSignin) -> Token:
        try:
            user = await self.user_uow.user.get_user_by_email(login_data.email)
        except UserNotFoundError as e:
            raise BadCredentialsError from e
        if not self.hash_manager.verify_hash(login_data.password, user.password):
            raise BadCredentialsError
        access_token = self.jwt_manager.create_access_token(
            AccessTokenData(user_id=user.id)
        )
        refresh_token = self.jwt_manager.create_refresh_token(
            RefreshTokenData(user_id=user.id)
        )
        return Token(access_token=access_token, refresh_token=refresh_token)

    async def authorize_user(self, access_token: str) -> User:
        token_data = self.jwt_manager.decode_access_token(access_token)
        try:
            user = await self.user_uow.user.get_user_by_id(token_data.user_id)
        except UserNotFoundError as e:
            raise BadJWTTokenError from e
