from datetime import timedelta
from typing import Protocol


class IJWTManager(Protocol):
    def create_jwt(self, data: dict, expires_delta: timedelta | None) -> str:
        ...

    def decode_jwt(self, jwt_token: str) -> dict:
        ...


class IHashManager(Protocol):
    def get_hash(self, value: str) -> str:
        ...

    def verify_hash(self, original_value: str, hashed_value: str) -> bool:
        ...
