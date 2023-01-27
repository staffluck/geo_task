from src.business_logic.user.dto.auth import Token, UserCreate, UserDTO, UserSignin
from src.business_logic.user.entities.user import User
from src.business_logic.user.exceptions.auth import BadCredentialsError
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
        user = await self.user_uow.user.get_user_by_email(login_data.email)
        if not user:
            raise BadCredentialsError("email/password введены неверно")
        access_token = self.jwt_manager.create_access_token(user.id)
        refresh_token = self.jwt_manager.create_refresh_token(user.id)
        return Token(access_token=access_token, refresh_token=refresh_token)