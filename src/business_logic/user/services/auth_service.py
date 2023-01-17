from src.business_logic.user.protocols.security import IHashManager, IJWTManager


class AuthService:
    def __init__(self, jwt_manager: IJWTManager, hash_manager: IHashManager) -> None:
        self.jwt_manager = jwt_manager
        self.hash_manager = hash_manager
