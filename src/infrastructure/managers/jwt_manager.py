from datetime import datetime, timedelta

from jose import JWTError, jwt

from src.business_logic.common.exceptions import BadJWTTokenException
from src.config import SecuritySettings


class JWTManager:
    def __init__(self, security_settings: SecuritySettings) -> None:
        self.settings = security_settings

    def create_jwt(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode["exp"] = expire
        encoded_jwt = jwt.encode(
            to_encode, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM
        )
        return encoded_jwt

    def decode_jwt(self, jwt_token: str) -> dict:
        try:
            payload = jwt.decode(
                jwt_token,
                self.settings.SECRET_KEY,
                algorithms=[self.settings.ALGORITHM],
            )
        except JWTError as e:
            raise BadJWTTokenException from e
        return payload
