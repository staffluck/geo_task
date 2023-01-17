from src.business_logic.user.dto.auth import UserCreate, UserDTO
from src.business_logic.user.entities.user import User
from src.business_logic.user.protocols.security import IHashManager, IJWTManager
from src.business_logic.user.protocols.uow import IUserUoW


class AuthService:
    def __init__(
        self, jwt_manager: IJWTManager, hash_manager: IHashManager, user_uow: IUserUoW
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
