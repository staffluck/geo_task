from typing import Protocol


class IJWTManager(Protocol):
    def create_access_token(self, user_id: int) -> str:
        ...

    def create_refresh_token(self, user_id: int) -> str:
        ...

    def decode_refresh_token(self, refresh_token: str) -> dict:
        ...

    def decode_access_token(self, access_token: str) -> dict:
        ...


class IHashManager(Protocol):
    def get_hash(self, value: str) -> str:
        ...

    def verify_hash(self, original_value: str, hashed_value: str) -> bool:
        ...
