from typing import Protocol

from src.business_logic.user.dto.auth import AccessTokenData, RefreshTokenData


class IJWTManager(Protocol):
    def create_access_token(self, token_data: AccessTokenData) -> str:
        ...

    def create_refresh_token(self, token_data: RefreshTokenData) -> str:
        ...

    def decode_refresh_token(self, refresh_token: str) -> RefreshTokenData:
        ...

    def decode_access_token(self, access_token: str) -> AccessTokenData:
        ...


class IHashManager(Protocol):
    def get_hash(self, value: str) -> str:
        ...

    def verify_hash(self, original_value: str, hashed_value: str) -> bool:
        ...
