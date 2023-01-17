from passlib.context import CryptContext

from src.business_logic.user.protocols.security import IHashManager
from src.config import SecuritySettings


class HashManager(IHashManager):
    def __init__(self, security_settings: SecuritySettings) -> None:
        self.security_settings = security_settings
        self.hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_hash(self, value: str) -> str:
        return self.hash_context.hash(value)

    def verify_hash(self, original_value: str, hashed_value: str) -> bool:
        return self.hash_context.verify(original_value, hashed_value)
